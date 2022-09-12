from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from typing import List

from extensions import Base, db


class Ability(Base):
    __tablename__ = 'abilities'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), unique=True, nullable=False)
    pokemon_id = Column(Integer(), ForeignKey('pokemons.id'))


class Pokemon(Base):
    __tablename__ = 'pokemons'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    abilities = relationship('Ability')

    def add_abilities(self, abilities: List[Ability]):
        for ability in abilities:
            ability.pokemon_id = self.id
            self.abilities.append(ability)

        db.commit()
