from database.db_gino import db


class ConceiveWord(db.Model):
    __tablename__ = 'conceive_words'

    id = db.Column(db.BigInteger(), primary_key=True)
    word = db.Column(db.String(5), unique=True)
