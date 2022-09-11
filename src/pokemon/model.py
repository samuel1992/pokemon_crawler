from extensions import db


class Ability(db.Model):
    __table__name = 'abilities'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    pokemon_id = db.Column(db.Integer(), db.ForeignKey('pokemons.id'))


class Pokemon(db.Model):
    __tablename__ = 'pokemons'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    abilities = db.relationship('Ability')

    def add_description(self, height: int, weight: int, species_name: str):
        self.description = (
            f'This pokemon has height: {height}, weight: {weight}'
            f' and belongs to {species_name}'
        )
        db.session.add(self)
        db.session.commit()
