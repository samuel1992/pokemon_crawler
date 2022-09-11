from dataclasses import dataclass, asdict, field

from typing import List, Optional

from .model import Pokemon, Ability


@dataclass
class Schema:
    def to_dict(self):
        return asdict(self)


@dataclass
class AbilitySchema(Schema):
    id: int
    name: str
    pokemon_id: Optional[int] = None

    @classmethod
    def from_instance(cls, instance: Ability):
        return cls(
            id=instance.id,
            name=instance.name,
            pokemon_id=instance.pokemon_id
        )


@dataclass
class PokemonSchema(Schema):
    id: int
    name: str
    description: str
    abilities: Optional[List[AbilitySchema]] = field(
        default_factory=lambda: []
    )

    @classmethod
    def from_instance(cls, instance: Pokemon):
        abilities = [AbilitySchema.from_instance(i) for i in instance.abilities]

        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            abilities=abilities
        )
