import csv
import os

from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


Base=declarative_base()
class Books(Base):
  __tablename__='books'
  id=Column(Integer,primary_key=True)
  isbn=Column(String(255),unique=True)
  title=Column(String(255))
  author=Column(String(255))
  year=Column(String(255))
  
class Users(Base):
  __tablename__='users'
  id=Column(Integer,primary_key=True)
  username=Column(String(255),unique=True)
  password=Column(String(255))
  firstname=Column(String(255))
  lastname=Column(String(255))
  children = relationship("Reviews")

class Reviews(Base):
  __tablename__='reviews'
  id=Column(Integer,primary_key=True)
  user_id=Column(Integer, ForeignKey('users.id'))
  book_id=Column(Integer)
  user_name=Column(String(255))
  rating=Column(Integer)
  content=Column(String(600))


if __name__ == "__main__":
 # Set up the database
 engine = create_engine(os.getenv("DATABASE_URL"))
 Base.metadata.create_all(bind=engine)

db = scoped_session(sessionmaker(bind=engine))

def main():

    projectpath= (os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)))
    os.chdir(projectpath) 
    f = open("books.csv")
    reader = csv.reader(f)
    for i, t, a, y in reader:
        db.execute("INSERT INTO books (isbn, title, author,year) VALUES (:isbn, :title, :author,:year)",
                    {"isbn": i, "title": t, "author": a,"year":y})
        db.commit()
    print("  The books from books.csv have ben imported into 'books' table")  

if __name__ == "__main__":
    main()
