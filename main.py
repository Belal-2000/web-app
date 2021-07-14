from enum import unique
from flask import Flask , redirect , url_for , render_template , session , request , flash
from flask_sqlalchemy import SQLAlchemy
import re
from cipher import cipher
from string import ascii_lowercase


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False
app.url_map.strict_slashes = False
app.secret_key = 'MA3AREK'


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(22), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique = False, nullable=False)

    def __init__(self , usr_n , email , pass_w):
        self.email = email
        self.username = usr_n
        self.password = pass_w

    def __repr__(self):
        return f'<User {self.username}>' 


class Msg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(22), unique=False, nullable=True)





reg = '[^@]+@[^@]+\.[^@]+'


@app.route('/')
def home():
    name = None
    if 'name' in session: 
        name = session['name']
    return render_template('home.html' , name = name)


@app.route('/sign-in' , methods = ['POST' , 'GET'])
def sign_in():
    if request.method == 'POST':
        if request.form['name'] == '' or request.form['pass'] == '':
            flash('can\'t leave any field empty ..' , 'error')
            return redirect(url_for('sign_in'))
        elif len(request.form['pass']) < 8 :
            flash('Password can\'t be less than 8 chars .. ' , 'error')
            return redirect(url_for('sign_in'))
        else:
            res = User.query.filter_by(username=request.form['name']).first()
            if res:
                if res.password == request.form['pass']:
                    session['name'] = request.form['name']
                    flash('signed in successfully .. ' , 'massge')
                    return redirect(url_for('home'))
            else:
                flash('wrong user name or password ..' , 'error')
                return redirect(url_for('sign_in'))
    if 'name' in session:
        flash('you are already signed in ..' , 'error')
        return  redirect(url_for('home'))
    else:
        return render_template('sign_in.html')


@app.route('/sign-up' , methods = ['POST' , 'GET'])
def sign_up():
    if request.method == 'POST':
        if request.form['email'] == '' or request.form['name'] == '' or request.form['pass'] == '' or request.form['re_pass'] == '':
            flash('can\'t leave any field empty ..' , 'error')
            return redirect(url_for('sign_up'))
        elif request.form['pass'] != request.form['re_pass']:
            flash('password dosn\'t mach ..' , 'error')
            return redirect(url_for('sign_up'))
        elif not re.match(reg , request.form['email']):
            flash('enter a valid email ..' , 'error')
            return redirect(url_for('sign_up'))
        elif len(request.form['pass']) < 8 :
            flash('Password can\'t be less than 8 chars .. ' , 'error')
            return redirect(url_for('sign_up'))
        elif len(request.form['email']) > 50 or len(request.form['name']) > 50 or len(request.form['pass']) > 50  :
            flash('50 chars maximum at any field ..' , 'error')
            return redirect(url_for('sign_up'))
        else:
            res1 = User.query.filter_by(username=request.form['name']).first()
            res2 = User.query.filter_by(email=request.form['email']).first()
            if res1 :
                flash('user name already taken ..' , 'error')
                return redirect(url_for('sign_up'))
            elif res2 :
                flash('email used before ..' , 'error')
                return redirect(url_for('sign_up'))
            else:
                n = request.form['name']
                e = request.form['email']
                p = request.form['pass']
                user = User(n , e , p)
                db.session.add(user)
                db.session.commit()
                flash('signed up successfully' , 'massge')
                flash('now you can sign in here ..' , 'massge')
                return redirect(url_for('sign_in'))
    else:
        if 'name' in session:
            flash('you are already signed in ..', 'error')
            return  redirect(url_for('home'))
        else:
            return render_template('sign_up.html')


@app.route('/cipher' ,methods = ['POST' , 'GET'])
def c():
    res = None
    if 'name' not in session:
        flash('You have to login first ..', 'error')
        return  redirect(url_for('sign_in'))
    else:
        if request.method == 'POST':
            if request.form['msg'] == '' or request.form['key'] == '':
                flash('cant leave any field empty ..' , 'error')
                return redirect(url_for('c'))
            else:
                msg = request.form['msg']
                k = request.form['key'].lower()
                case = request.form['case']
                for i in k:
                    if i not in ascii_lowercase :
                        flash('key must be only text ..' , 'error')
                        return redirect(url_for('c'))
                session['msg'] = msg
                session['key'] = k
                res = cipher.cifer(msg , k , case)
                return render_template('chiper.html' , res = res)
        else:
            return render_template('chiper.html' , res = res)



@app.route('/log-out')
def log_out():
    session.pop('name' , None)
    flash('Loged out successfully .. ' , 'massge')
    return redirect(url_for('home'))


if __name__ == '__main__':
    db.create_all()
    app.run()
