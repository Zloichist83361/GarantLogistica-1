import sqlite3
import datetime
from flask import Blueprint, render_template, url_for, redirect, session, request, flash, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.add_news', 'title': 'Создать новость'},
        {'url': '.list_news', 'title': 'Добавить новость на сайт'},
        {'url': '.list_users', 'title': 'Список пользователей'},
        {'url': '.logout', 'title': 'Выйти'}]


def isLogged():
    return True if session.get('admin_logged') else False


def login_admin():
    session['admin_logged'] = 1


admin.permanent_session_lifetime = datetime.timedelta(days=10)


def logout_admin():
    session.pop('admin_logged', None)


db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))

    return render_template('admin/admin_index.html', menu=menu, title='Админ-панель')


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))

    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "admin":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", "error")

    return render_template('admin/admin_login.html', title='Админ-панель')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))


@admin.route('/list-news')
def list_news():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f'SELECT title, text FROM articles')
            list = cur.fetchall()
        except sqlite3.Error as e:
            print('Ошибка получения новости из БД' + str(e))

    return render_template('admin/list_news.html', title='Добавить новость на сайт', menu=menu, list=list)


@admin.route('/add-news', methods=('GET', 'POST'))
def add_news():
    if not isLogged():
        return redirect(url_for('.login'))

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        if not title:
            flash('Введите заголовок!')
        else:
            cur = db.cursor()
            cur.execute(f'INSERT INTO articles (title, text) VALUES (?, ?)', (title, text))
            db.commit()
            db.close()
            return redirect(url_for('.list_news'))
    return render_template('admin/add_news.html', title='Создать новость', menu=menu)


@admin.route('/list-users')
def list_users():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT login, email FROM users")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template('admin/list_users.html', title='Список пользователей', menu=menu, list=list)
