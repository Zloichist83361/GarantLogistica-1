class Article:
    def fromDB(self, article_id, db):
        self.__user = db.getArticle(article_id)
        return self

