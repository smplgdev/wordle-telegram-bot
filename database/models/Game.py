from database.db_gino import db


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.BigInteger, primary_key=True)
    game_message_id = db.Column(db.Integer)
    user_telegram_id = db.Column(db.ForeignKey('users.tg_id'))
    conceived_word = db.Column(db.String(5))
    date = db.Column(db.Date)

    # ['run', 'end']
    status = db.Column(db.String(3), default=None)
