from database.db_gino import db


class Guess(db.Model):
    __tablename__ = 'guesses'

    id = db.Column(db.BigInteger(), primary_key=True)
    game_id = db.Column(db.ForeignKey('games.id'))
    user_input_word = db.Column(db.String(5))
