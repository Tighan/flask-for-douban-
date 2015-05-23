from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash

#configuration
DATABASE="flaskr.db"
DEBUG=True
SECRET_KEY="development key"
USERNAME="admin"
PASSWORD="admin"
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])      
# [in this case] app.config['DATABASE'] ==> DATABASE = 'flaskr.db'


# *initialize db*
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# [organical solution: request with database for opening and closing ]
# organically open database session before request
@app.before_request
def before_request():
    g.db = connect_db()

# organically close database session after request
@app.teardown_request
def teardown_request(exception):
    db = getattr(g,'db',None)
    if db is not None:
        db.close()






@app.route("/")
def show_entries():
    cur=g.db.execute("select title,text from entries order by id desc")
    entries=[dict(title=row[0],text=row[1],name="hello")for row in cur.fetchall()]
    return render_template("show_entries.html",entries=entries)

@app.route("/add",methods=["post"])
def add():
    if not session.get("logged_in"):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?,?)',[request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for("show_entries"))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error = error)
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route("/html")
def show_html():
    movies=[dict(title="hello")]
    return render_template('blog.html',movies=movies)

if __name__=="__main__":
    app.run()