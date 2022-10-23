from database.db_gino import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), primary_key=True)
    tg_id = db.Column(db.BigInteger(), unique=True)
    deep_link = db.Column(db.String(64))

    username = db.Column(db.String(32))
    is_active = db.Column(db.Boolean(), default=True)
