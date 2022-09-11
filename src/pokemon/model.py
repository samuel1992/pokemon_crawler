from app.extensions import db


class Ability:
    __table__name = 'abilities'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    pokemon_id = db.Column(db.Integer(), db.ForeignKey('pokemons.id'))


class Pokemon:
    __tablename__ = 'pokemons'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    abilities = db.relationship('Ability')
