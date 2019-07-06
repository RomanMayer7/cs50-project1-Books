# Project 1
Web Programming with Python and JavaScript
-----------------------------------------------
Project Name :Books:"Librarian"
-----------------------------------------------
The WebSite enables multiple users to interract 
with   Books Database in order to get
basic information about a book
(Like author and year of publication),
 watch other's reviews and submit their own.User
can rate book,as well ,on five grade scale.
User can vote for each book only for one time.
User should create his own account and put 
his credentials in order to use the website
User can get all basic book info in JASON
format,using API,which is special route
by itself,accessible through /api/isbn-number
and via Search Result page,by clicking on book's
isbn number.Moreover user is provided with realtime
information regarding the 'average rating' and
'number of reviews' for each book through the
Goodreads API :https://www.goodreads.com/api  
-----------------------------------------------
*The application have "requirements.txt" file,
listing all the additional modules ,which are 
should be preinstalled before running the app

*The database connection route,including credentials
should be represented inside DATABASE_URL enviromental
variable in your system!It is used by "import.py"
and by "application.py"  itself as well 

*"import.py" file should be launched in order
to create all the tables inside the Database
and import book data from "books.csv"(included in the main folder)
It will create three tables inside your database:"books","users","reviews" 
and will populate "books" with data

*There is 'static' directory, inside the main folder.
It have 'img' folder inside of it,with all the  
media files used in the website.

*'flask_session' folder is reserved for storing the user sessions
which  is managed by the flask special module,included in App

*All the HTML pages, including 'layout.html',
which are used in order to represent different routes of the website:
stored inside 'templates' folder.Most of the styling(CSS and Bootstrap) references
are included inside layout.html and some additional styling included in 
some pages as well. 

*The 'applicaton.py',which contains all the logic of the application-should be executed
in order to start the Website.Most of the application's logic is writen in PYTHON,but some of it located inside HTML files ,created using JINJA2

*All the queries to database are written in 'RAW SQL' and executed through the 
SQLAlchemy's method "db.execute",without usage of it's ORM

*In order to run my web application i used Postegre SQL Database hosted on Heroku www.heroku.com
----------------------------------------------------------------------------------------
by Roman Meyerson 2019/Started :Jan 26, 2019-Finished:Jan 30, 2019