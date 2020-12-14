import sqlite3
import sqlite3 as sql
import json
import logging

from flask_login import login_user, current_user, login_required
from flask import render_template, url_for, request, redirect, flash, g, make_response
from werkzeug.exceptions import abort

from werkzeug.security import generate_password_hash, check_password_hash

from app import app, login_manager
from UserData import UserLogin
from DataBase import DataBase


logger = logging.getLogger('view')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('gl.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[LINE:%(lineno)d]# %(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@login_manager.user_loader
def load_user(user_id):
    logger.info("Пользователь вошел")
    return UserLogin().fromDB(user_id, dbase)


@app.route('/cookie/')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response('Setting a cookie')
        res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
    else:
        res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
    return res


def connect_db():
    conn = sqlite3.connect(app.config['db'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Основные страницы +
@app.route('/')
@app.route('/home')
@app.route('/index')
@app.route('/domoy')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")
# Основные страницы -


# Отслеживание +
@app.route('/tracking')
def tracking():
    return render_template("tracking.html")


@app.route("/tracking/status", methods=["GET"])
def tracking_status():
    track = request.args.get('tracknumber')
    con = sql.connect("garant_logistica.db")
    cur = con.cursor()
    cur.execute("SELECT status, date_status_users, payment, date_delivery, direction FROM order_status WHERE track = '" + track + "'")
    result = cur.fetchall()
    if len(result) != 0:
        response = {"order_status": result[0][0],
                    "date_order_users": result[0][1],
                    "payment": result[0][2],
                    "date_delivery": result[0][3],
                    "direction": result[0][4]}
    else:
        response = {"order_status": None, "date_order_users": None}
    return json.dumps(response)
# Отслеживание -


# Регистрация +
@app.route('/reqlog', methods=["POST", "GET"])
def reqlog_enter():
    if current_user.is_authenticated:
        #return redirect(url_for('profile'))
        return render_template('profile.html')
    return render_template('reqlog.html')


@app.route('/reqlog/reg', methods=["POST", "GET"])
def reg():
    if request.method == "POST":
        if len(request.form['login']) > 1 and len(request.form['email']) > 1 \
                and len(request.form['psw']) > 1:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['login'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы")
                return redirect(url_for('reqlog_enter'))
            else:
                flash("Пользователь с таким логином уже существует")
        else:
            flash("Неверно заполнены поля")
    return render_template('reqlog.html')


@app.route('/reqlog/log', methods=["POST", "GET"])
def log():
    if current_user.is_authenticated:
        return redirect(url_for('reqlog_enter'))

    if request.method == "POST":
        user = dbase.getUserByLogin(request.form['login'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            flash("Вы успешно зашли")
            return redirect(url_for("index"))

        flash("Неверная пара логин/пароль")
    return render_template('reqlog.html')
# Регистрация -


@app.route('/profile')
@login_required
def profile(param=''):
    # loadpage = namedtuple("loadpage", "main settings extra")
    # loadpage.main = False
    # loadpage.settings = False
    # loadpage.extra = False
    return render_template("profile.html", loadpage=param)


@app.route('/calculate')
@login_required
def calculate():
    return render_template("index.html")


@app.route('/order')
@login_required
def order():
    return render_template("index.html")


@app.route('/news')
def show_all_news():
    db = get_db()
    dbase = DataBase(db)
    allnews = dbase.getAllNews()
    return render_template('news.html', allnews='allnews', posts=allnews)


@app.route('/news/<int:id_news>')
def show_news(id_news):
    db = get_db()
    dbase = DataBase(db)
    title, text = dbase.getNews(id_news)
    if not title:
        abort(404)

    return render_template('news.html', title=title, text=text)
