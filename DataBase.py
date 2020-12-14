import sqlite3
import logging

logger = logging.getLogger('FDataBase')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('gl.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[LINE:%(lineno)d]# %(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addUser(self, login, email, hash):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE login LIKE '{login}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                logger.info("Пользователь с таким логином уже существует")
                return False

            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (login, email, hash))
            self.__db.commit()
        except sqlite3.Error as e:
            logger.error("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                logger.info("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            logger.error("Ошибка получения данных из БД " + str(e))

        return False

    def getUserByLogin(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                logger.info("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            logger.error("Ошибка получения данных из БД " + str(e))

        return False

    def getArticle(self, article_id):
        try:
            self.__cur.execute(f"SELECT * FROM articles WHERE id = {article_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                logger.info("Статья не найдена")
                return False
            return res
        except sqlite3.Error as e:
            logger.error("Ошибка получения данных из БД " + str(e))
        return False
