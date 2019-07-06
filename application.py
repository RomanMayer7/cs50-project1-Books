import os
import json
import requests
from flask import Flask,render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__,static_url_path = "/static")

# Set up the session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


# Set up the database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def home():
 return render_template("home.html")

@app.route("/signup")
def signup():
 return render_template("signup.html")

@app.route("/reg_submit",methods=["POST"])
def reg_submit():
  u_name = request.form.get("username")
  p_word = request.form.get("password")
  f_name = request.form.get("fname")
  l_name = request.form.get("lname")
  db.execute("INSERT INTO users (username,password, firstname, lastname) VALUES (:u,:p,:f,:l)",
  {"u":u_name,"p": p_word, "f": f_name, "l": l_name})
  db.commit()
  return render_template("reg_submit.html")

@app.route("/search",methods=["GET", "POST"])
def search():
 # Get login form information if you just logged in
  if session["current_user"]is None:
   usr_name = request.form.get("username")
   psswrd = request.form.get("password")
   user_exist = db.execute("SELECT * FROM users WHERE username=:usr AND password=:psw",{"usr":usr_name,"psw":psswrd}).fetchone()
   print(user_exist)
   if user_exist is None:
    return render_template("error.html")
   else:
    if user_exist[3] is '':
     #storing user credentials inside session by username
     session["current_user"] = user_exist[1]
     print(session["current_user"])
     return render_template("search.html")
    else:
     #storing user credentials inside session by firstname and lastname
     session["current_user"] = user_exist[3]+" "+user_exist[4]
     print(session["current_user"])
     return render_template("search.html")
  else:
    return render_template("search.html")
 
   

@app.route("/search_results", methods=["POST"])
def search_results():
  # Get form information.
  s_key=request.form.get("search_by")
  s_value ="%"+request.form.get("search_input")+"%"
  #books_result = db.execute("SELECT * FROM books WHERE year='1997'").fetchall()
  print("SELECT * FROM books WHERE "+s_key+" LIKE :searchval", {"searchval":s_value})
  books_result = db.execute("SELECT * FROM books WHERE "+s_key+" LIKE :searchval", {"searchval":s_value}).fetchall()
  return render_template("search_results.html", books=books_result)

@app.route("/book_review/<int:this_book_id>")
def book_review(this_book_id):
  print(session["current_user"])
  if session.get("current_user") is None:
    return render_template("error.html")
  my_book = db.execute("SELECT * FROM books WHERE id=:this_id",{"this_id":this_book_id}).fetchone()
  res = requests.get("https://www.goodreads.com/book/review_counts.json", 
  params={"key": "hXM6focKcUQarBQcoykEIg", "isbns": my_book.isbn})
  x=res.json()
  y=json.dumps(x)
  z=json.loads(y)
  v=z["books"]
  info=v[0]
  av_rating=info["average_rating"]
  rv_count=info["reviews_count"]
  reviews = db.execute("SELECT * FROM reviews WHERE book_id=:this_id",{"this_id":this_book_id}).fetchall()
  return render_template("book_review.html",id=this_book_id,book=my_book,reviews=reviews,rating=av_rating,rcount=rv_count)

@app.route("/review_submit/<int:this_book_id>",methods=["GET", "POST"])
def review_submit(this_book_id):
  this_user=session["current_user"]
  b_id=this_book_id
  print(this_user)
  rtng=request.form.get("rating")
  cmnt=request.form.get("comment")
  #Check if the same user already have an review in database
  gotreview=db.execute("SELECT * FROM reviews WHERE user_name=:this_usr",{"this_usr":this_user}).fetchone()
  print(gotreview)
  if gotreview is None:#if not let him review the book
    db.execute("INSERT INTO reviews (book_id,user_name, rating, content) VALUES (:bid,:un,:r,:c)",
    {"bid":b_id,"un": this_user, "r": rtng, "c": cmnt})
    db.commit()
    return render_template("submit_review.html")
  else:
   return render_template("review_error.html")

@app.route("/logout")
def logout():
 session["current_user"]=None #reseting the session
 return render_template("logout.html")

@app.route("/api/<string:isbn>")
def api(isbn):
  my_book = db.execute("SELECT * FROM books WHERE isbn=:this_isbn",{"this_isbn":isbn}).fetchone()
  if my_book is None:#if ISBN notexist in Databse throw  404 error page
    return render_template("error404.html")
  res = requests.get("https://www.goodreads.com/book/review_counts.json", 
  params={"key": "hXM6focKcUQarBQcoykEIg", "isbns":isbn})
  x=res.json()
  y=json.dumps(x)
  z=json.loads(y)
  v=z["books"]
  info=v[0]
  av_rating=info["average_rating"]
  rv_count=info["reviews_count"]
  return render_template("api.html",book=my_book,av_score=av_rating,rv_count=rv_count)

if __name__=='__main__':app.run()