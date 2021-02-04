from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math
import json

with open('config.json', 'r') as config:
    params = json.load(config)['Parameters']

local_server = False
app = Flask(__name__)
app.secret_key = 'my secret key'

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
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
    if 'user' in session and session['user'] == params['admin_user']:
        blogs = Blogs.query.all()
        return render_template('dashboard.html', params=params, blogs=blogs)
    if request.method == 'POST':
        username = request.form.get('name')
        password = request.form.get('password')
        if username == params['admin_user'] and password == params['admin_password']:
            session['user'] = username
            blogs = Blogs.query.all()
            return render_template('dashboard.html', params=params, blogs=blogs)
        else:
            return render_template('login.html', params=params)
    else:
        return render_template('login.html', params=params)


@app.route('/edit/<string:serialnum>', methods=["GET", "POST"])
def edit(serialnum):
    if 'user' in session and session['user'] == params['admin_user']:
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
    if 'user' in session and session['user'] == params['admin_user']:
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


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route('/delete/<string:serialnum>', methods=["GET", "POST"])
def delete(serialnum):
    if 'user' in session and session['user'] == params['admin_user']:
        blog = Blogs.query.filter_by(sno=serialnum).first()
        db.session.delete(blog)
        db.session.commit()
        return redirect('/dashboard')


if __name__ == "__main__":
    app.run(debug=True)
