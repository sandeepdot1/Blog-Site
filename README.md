# Blog-Site

A Blogging website made using Flask and Python

Setup Guide

Prerequisites

Ensure you have the following installed:

Python 3.8+

Docker & Docker Compose

MySQL (or use Docker for MySQL)

Virtual environment (optional but recommended)

Setup Instructions

1. Clone the Repository

$ git clone <your-repo-url>
$ cd <your-repo-folder>

2. Create a Virtual Environment & Install Dependencies

$ python -m venv venv
$ source venv/bin/activate # On Windows use `venv\\Scripts\\activate`
$ pip install -r requirements.txt

3. Configure Database

Create a config.json file in the project root with the following structure:

{
"mysql": {
"host": "localhost",
"user": "root",
"password": "yourpassword",
"database": "yourdatabase"
}
}

4. Run MySQL Using Docker (Optional)

If you don't have MySQL installed locally, you can run it using Docker:

$ docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=yourpassword -e MYSQL_DATABASE=yourdatabase -p 3306:3306 -d mysql:latest

5. Initialize Database

$ python

> > > from app import db
> > > db.create_all()
> > > exit()

6. Run the Application

$ flask run

Your Flask app should now be running at http://127.0.0.1:5000.

7. Dropping Existing Tables (If Needed)

To reset the database, run the following SQL commands:

drop table blogs;
drop table contacts;
drop table users;

Happy coding! 🚀
