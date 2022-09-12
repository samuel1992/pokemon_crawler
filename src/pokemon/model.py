from typing import List

from extensions import db


class Ability(db.Model):
    __table__name = 'abilities'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    pokemon_id = db.Column(db.Integer(), db.ForeignKey('pokemons.id'))


class Pokemon(db.Model):
    __tablename__ = 'pokemons'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    abilities = db.relationship('Ability')

    def add_abilities(self, abilities: List[Ability]):
        for ability in abilities:
            ability.pokemon_id = self.id
            self.abilities.append(ability)

        db.session.commit()
