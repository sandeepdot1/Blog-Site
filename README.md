# CodingBlog

A Blog Site made using Flask and Python

https://github.com/user-attachments/assets/85957040-0441-45d7-9b49-f0947a5a2167

# Flask App Setup

## Prerequisites

Ensure you have the following installed:

- Python 3.8+ (3.8.5 recommended for compatibility)
- Docker & Docker Compose
- MySQL (or use Docker for MySQL)
- Virtual environment (optional but recommended)

## Setup Instructions

### 1. Clone the Repository

```sh
$ git clone <your-repo-url>
$ cd <your-repo-folder>
```

### 2. Create a Virtual Environment & Install Dependencies

```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
$ pip install -r requirements.txt
```

### 3. Configure Database

Create a `config.json` file in the project root with the following structure (Sample json attached):

```json
{
  "Parameters": {
    "local_uri": "mysql+pymysql://root:root@localhost/mydb",
    "production_uri": "mysql+pymysql://root:root@localhost/mydb",
    "per_page": 5,
    "admin_user": "admin_username",
    "login_image": "login_image.png"
    "blog_name": "CodingBlog",
    "current_year": 2025
  }
}
```

> **Note:** The Flask app connects to MySQL using the standard URI format:
>
> ```
> mysql+pymysql://username:password@host:port/database_name
> ```
>
> Example:
>
> ```
> mysql+pymysql://root:yourpassword@localhost:3306/yourdatabase
> ```
>
> Ensure that `pymysql` is installed to use this format.

> **Note:** If you are getting an issue during flask app run due to mysql like this,
>
> ```
> line 31, in mysql_config
>        raise OSError("{} not found".format(_mysql_config_path))
>    OSError: mysql_config not found
>    ----------------------------------------
> ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
> ```
>
> install the following libraries (for Ubuntu/Debian)
>
> ```
> sudo apt update
> sudo apt install libmysqlclient-dev
> ```
>
> install the following libraries (for Mac)
>
> ```
> brew install mysql-client
> echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.bashrc
> source ~/.bashrc
> ```

### 4. Run MySQL Using Docker (Optional)

If you don't have MySQL installed locally, you can run it using Docker:

```sh
$ docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=yourpassword -e MYSQL_DATABASE=yourdatabase -p 3306:3306 -d mysql:5.7
```

### 5. Initialize Database

To create tables used in app, use the `create_tables.sql` script:

```sh
$ mysql -u root -p yourpassword < create_tables.sql
```

### 6. Run the Application

```sh
$ flask run
```

or

```sh
$ python3 app.py
```

Your Flask app should now be running at `http://127.0.0.1:5000`.

### 7. Dropping Existing Tables (If Needed)

To reset the database, run the following SQL commands:

```sql
DROP TABLE IF EXISTS blogs;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS users;
```

---

Happy coding! 🚀
