from dataclasses import dataclass, asdict, field

from typing import List, Optional

from .model import Pokemon, Ability


@dataclass
class Schema:
    def to_dict(self):
        return asdict(self)


@dataclass
class AbilitySchema(Schema):
    id: Optional[int]
    name: str
    pokemon_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AbilitySchema':
        return cls(
            id=int(data['url'].split('/')[6]),
            name=data['name'],
            pokemon_id=data.get('pokemon_id', None)
        )

    @classmethod
    def from_instance(cls, instance: Ability) -> 'AbilitySchema':
        return cls(
            id=instance.id,
            name=instance.name,
            pokemon_id=instance.pokemon_id
        )

    def to_instance(self):
        return Ability(**self.to_dict())


@dataclass
class PokemonSchema(Schema):
    id: Optional[int]
    name: str
    abilities: Optional[List[AbilitySchema]] = field(
        default_factory=lambda: []
    )

    @classmethod
    def from_dict(cls, data: dict) -> 'PokemonSchema':
        return cls(
            id=int(data['url'].split('/')[6]),
            name=data['name']
        )

    @classmethod
    def from_instance(cls, instance: Pokemon) -> 'PokemonSchema':
        abilities = [
            AbilitySchema.from_instance(i) for i in instance.abilities
        ]

        return cls(
            id=instance.id,
            name=instance.name,
            abilities=abilities
        )

    def to_instance(self):
        abilities = [Ability(**i.to_dict()) for i in self.abilities]
        pokemon_data = self.to_dict()
        pokemon_data['abilities'] = abilities
        return Pokemon(**pokemon_data)
