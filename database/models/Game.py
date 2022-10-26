from database.db_gino import db


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.BigInteger, primary_key=True)
    game_message_id = db.Column(db.Integer)
    user_telegram_id = db.Column(db.ForeignKey('users.tg_id'))
    conceived_word_id = db.Column(db.ForeignKey('conceived_words.id'))
    date = db.Column(db.Date)

    # ['run', 'win', 'los']
    status = db.Column(db.String(3), default=None)
