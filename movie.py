from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash
pagelist=range(0,250)
page=[]
for i in range(0,len(pagelist),5):
    k=pagelist[i:i+5]
    page.append(k)

idlist=['1292052', '1295644', '1292720', '1291546', '1292063', '1292001', '1295124', '1291561', '2131459', '1292722', '3541415', '3793023', '1291549', '3011091', '1291560', '1291841', '1292213', '1300267', '1291828', '1292000', '1849031', '1292064', '1291552', '1293839', '3442220', '1293350', '6786002', '1293182', '1291583', '1291858', '1292224', '2129039', '1299398', '3319755', '1900841', '1292215', '1309046', '1307914', '1298624', '1851857', '1291572', '1291571', '5912992', '1306029', '1292365', '1299131', '1292370', '1292223', '1929463', '1292220', '1294639', '1308807', '1291548', '1292262', '1296736', '1294408', '1780330', '1301753', '1787291', '1303021', '3072124', '1291832', '2149806', '1292343', '1293544', '1485260', '1291545', '1316510', '1291843', '1291875', '1297359', '1292849', '1297630', '3742360', '1292208', '4917726', '1291818', '1292656', '1293318', '1292402', '1418019', '1292434', '1305164', '1291999', '3443389', '1292679', '1296339', '1291990', '1291585', '1295865', '1298070', '4268598', '2353023',
        '1296909', '1652587', '1297052', '1297192', '1292401', '1293359', '5322596', '2334904', '1417598', '1292274', '1294371', '1292528', '3287562', '4202302', '1292328', '1937946', '3792799', '1293964', '1291870', '2209573', '1295399', '1418834', '1309163', '1304447', '1578507', '1305487', '1291579', '1297447', '1291822', '2043546', '1306861', '1293460', '1858711', '1300960', '1302827', '1907966', '3008247', '1388216', '3007773', '1294240', '1760622', '21937445', '1418200', '1295409', '1297574', '1291578', '1300992', '1295038', '1292281', '2297265', '1300299', '1905462', '1293172', '1978709', '1308857', '6985810', '1292270', '1303037', '1397546', '1296141', '2213597', '1419936', '1307793', '1291879', '5964718', '1300374', '21937452', '1865703', '4798888', '5989818', '1292728', '1296753', '1291853', '2363506', '1292217', '1308817', '1294638', '3011235', '1304102', '1292659', '2053515', '1293181', '1297478', '1308767', '1305690', '1292233', '3157605', '1308575', '11525673', '2300586', '1299361', '1302476', '2365260', '1292056', '1293764', '1292218', '1307811', '1292214', '1307315', '1291557', '1401118', '1309027', '1299327', '1306249', '1291844', '1292062', '1308777', '1291992', '1292287', '3217169', '1303394', '1301171', '1293908', '1302425', '1959195', '1302467', '4739952', '1867345', '10777687', '3011051', '1291568', '1301169', '1438652', '3075287', '1756073', '1301617', '1292055', '1316572', '1298653', '1292329', '4023638', '1428175', '1293530', '6146955', '1962116', '1293399', '1291565', '3073124', '1305725', '1293929', '21360417', '1292925', '1844413', '1292348', '1395091', '5908478', '6534248', '1304073', '3824274', '1369747', '1292047', '1291824', '1300117', '1293708', '1300741', '1862151', '1304056']
iddict=dict(zip(pagelist,idlist))
nextid=1

#configuration
DATABASE="movies.db"
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
def index():
   return render_template('index.html')
@app.route("/<int:pageid>")
def show_html(pageid):
    paged=page[(pageid-1)]
    m1,m2,m3,m4,m5=paged[0],paged[1],paged[2],paged[3],paged[4]
    cond1="select year,directors,title,summary,casts,genres,url from movie where id like '%"+iddict[m1]+"%' "
    cond2="select year,directors,title,summary,casts,genres,url from movie where id like '%"+iddict[m2]+"%' "
    cond3="select year,directors,title,summary,casts,genres,url from movie where id like '%"+iddict[m3]+"%' "
    cond4="select year,directors,title,summary,casts,genres,url from movie where id like '%"+iddict[m4]+"%' "
    cond5="select year,directors,title,summary,casts,genres,url from movie where id like '%"+iddict[m5]+"%' "
    m1=g.db.execute(cond1)
    m2=g.db.execute(cond2)
    m3=g.db.execute(cond3)
    m4=g.db.execute(cond4)
    m5=g.db.execute(cond5)
    movies1=[dict(year=row[0],directors=row[1],title=row[2],summary=row[3],casts=row[4],genres=row[5],url=row[6]) for row in m1.fetchall()]
    movies2=[dict(year=row[0],directors=row[1],title=row[2],summary=row[3],casts=row[4],genres=row[5],url=row[6]) for row in m2.fetchall()]
    movies3=[dict(year=row[0],directors=row[1],title=row[2],summary=row[3],casts=row[4],genres=row[5],url=row[6]) for row in m3.fetchall()]
    movies4=[dict(year=row[0],directors=row[1],title=row[2],summary=row[3],casts=row[4],genres=row[5],url=row[6]) for row in m4.fetchall()]
    movies5=[dict(year=row[0],directors=row[1],title=row[2],summary=row[3],casts=row[4],genres=row[5],url=row[6]) for row in m5.fetchall()]
    return render_template('blog.html',movies1=movies1,movies2=movies2,movies3=movies3,movies4=movies4,movies5=movies5)
@app.route('/next')
def next():
    global nextid
    nextid=nextid+1
    return redirect(url_for('show_html',pageid=nextid))
@app.route('/back')
def back():
    global nextid
    nextid=nextid-1
    return redirect(url_for('show_html',pageid=nextid))
@app.route('/<title>')
def each_blog(title):
    cond="select year,directors,title,summary,casts,genres,url from movie where title like '%"+title+"%' "
    m=g.db.execute(cond)
    movie=[dict(year=row[0],directors=row[1],title=row[2],summary=row[3],casts=row[4],genres=row[5],url=row[6]) for row in m.fetchall()]
    return render_template('each_blog.html',movie=movie)

@app.route("/search",methods=["post"])
def search():
    title1=request.form['title']
    return redirect(url_for('each_blog',title=title1))
if __name__=="__main__":
    app.run()
