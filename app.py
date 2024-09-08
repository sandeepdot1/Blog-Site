from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math
import json

with open('config.json', 'r') as config:
    params = json.load(config)['Parameters']

local_server = True
app = Flask(__name__)
app.secret_key = 'my secret key'

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']

    # sesion name changed for testing
    app.config['SESSION_COOKIE_NAME'] = "session_details"

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):
    """
    sno, email, phone_num, type, message, date,
    """
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=False, nullable=False)
    phone_num = db.Column(db.String(12), unique=False, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Blogs(db.Model):
    '''
    sno, title,content, date,slug
    '''
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False, nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(25), nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Users(db.Model):
    '''
    id, email, username, password
    '''
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing ID
    email = db.Column(db.String(120), nullable=False, unique=True)  # Email as a string, must be unique
    username = db.Column(db.String(50), nullable=False, unique=True)  # Username as a string, must be unique
    password = db.Column(db.String(200), nullable=False)  # Password as a string
    created_date = db.Column(db.String(12), nullable=True)



@app.route("/", methods=["GET"])
def home():
    page = request.args.get('page', 1, type=int)
    total = Blogs.query.all()
    last = math.ceil(len(total) / params['per_page'])

    prev = page
    next = page

    if page == 1:
        prev = '/?page=' + str(page)
        next = '/?page=' + str(page + 1)
    elif page == last:
        prev = '/?page=' + str(page - 1)
        next = '/?page=' + str(page)
    else:
        prev = '/?page=' + str(page - 1)
        next = '/?page=' + str(page + 1)

    blogs = Blogs.query.paginate(page=page, per_page=params['per_page'])
    # num = int(params['no_of_blogs'])
    return render_template('index.html', params=params, blogs=blogs, prev=prev, next=next)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''fetch data from frontend(contact page)'''
        email = request.form.get('email')
        phone = request.form.get('phone')
        tp = request.form.get('type')
        msg = request.form.get('message')
        '''Add entry to database'''
        entry = Contacts(email=email, phone_num=phone, type=tp, message=msg, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)


@app.route('/layout')
def layout():
    return render_template('layout.html', params=params)


@app.route('/blog/<string:blog_slug>', methods=["GET"])
def blog(blog_slug):
    new_blog = Blogs.query.filter_by(slug=blog_slug).first()
    new_blog.date = new_blog.date.strftime('%Y-%m-%d')
    return render_template('blog.html', params=params, blog=new_blog)


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if 'user' in session:
        blogs = Blogs.query.all()
        return render_template('dashboard.html', params=params, blogs=blogs)
    else:
        return redirect('/')


@app.route('/edit/<string:serialnum>', methods=["GET", "POST"])
def edit(serialnum):
    if 'user' in session:
        if request.method == 'POST':
            title = request.form.get('title')
            slug = request.form.get('slug')
            tp = request.form.get('type')
            content = request.form.get('content')
            img = request.form.get('img_file')
            date = datetime.now()

            blog = Blogs.query.filter_by(sno=serialnum).first()
            blog.title = title
            blog.slug = slug
            blog.type = tp
            blog.content = content
            blog.img_file = img
            blog.date = date
            db.session.commit()
            return redirect('/edit/' + serialnum)

        blog = Blogs.query.filter_by(sno=serialnum).first()
        return render_template('edit.html', params=params, blog=blog)


@app.route('/add',methods=["GET", "POST"])
def add():
    if 'user' in session:
        if request.method == 'POST':
            title = request.form.get('title')
            slug = request.form.get('slug')
            tp = request.form.get('type')
            content = request.form.get('content')
            img = request.form.get('img_file')
            date = datetime.now()
            blog = Blogs(title=title, slug=slug, type=tp, content=content, img_file=img, date=date)
            db.session.add(blog)
            db.session.commit()
        return render_template('add.html',params=params)
    else:
        return redirect('/dashboard')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if 'user' in session:
            return redirect('/dashboard')
        else:
            user_name = request.form.get('name')
            user_password = request.form.get('password')
            auth_user = Users.query.filter_by(username=user_name, password=user_password).first()
            print(auth_user)

            if auth_user:
                session['user'] = user_name
                return redirect('/dashboard')
            else:
                return render_template('login.html', params=params)
    else:
        return render_template('login.html', params=params)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_email = request.form.get('email')
        user_name = request.form.get('name')
        user_password = request.form.get('password')
        curr_user = Users.query.filter_by(email=user_email, username=user_name).first()
        print(curr_user)

        if curr_user:
            return render_template('signup.html', params=params)
        else:
            signup_user = Users(email=user_email, username=user_name, password=user_password, created_date=datetime.now())
            db.session.add(signup_user)
            db.session.commit()
            session['user'] = user_name
            return redirect('/dashboard')
    else:
        return render_template('signup.html', params=params)


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


@app.route('/delete/<string:serialnum>', methods=["GET", "POST"])
def delete(serialnum):
    if 'user' in session and session['user'] == params['admin_user']:
        blog = Blogs.query.filter_by(sno=serialnum).first()
        db.session.delete(blog)
        db.session.commit()
        return redirect('/dashboard')


if __name__ == "__main__":
    app.run(debug=True)
