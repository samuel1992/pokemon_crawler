from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List, Optional

from .model import Ability, Pokemon


@dataclass
class DTO:
    id: Optional[str]

    def to_dict(self):
        return asdict(self)

    def __post_init__(self):
        if self.id is not None:
            self.id = str(self.id)


@dataclass
class AbilityDTO(DTO):
    instance_class = Ability

    name: str
    pokemon_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AbilityDTO':
        return cls(
            id=str(data['url'].split('/')[6]),
            name=data['name'],
            pokemon_id=data.get('pokemon_id', None)
        )

    @classmethod
    def from_instance(cls, instance: Ability) -> 'AbilityDTO':
        return cls(
            id=str(instance.id),
            name=instance.name,
            pokemon_id=instance.pokemon_id
        )

    def to_instance(self):
        return Ability(**self.to_dict())


@dataclass
class PokemonDTO(DTO):
    instance_class = Pokemon

    name: str
    abilities: Optional[List[AbilityDTO]] = field(
        default_factory=lambda: []
    )
    last_update: Optional[datetime] = datetime.now()

    @classmethod
    def from_dict(cls, data: dict) -> 'PokemonDTO':
        return cls(
            id=str(data['url'].split('/')[6]),
            name=data['name']
        )

    @classmethod
    def from_instance(cls, instance: Pokemon) -> 'PokemonDTO':
        abilities = [
            AbilityDTO.from_instance(i) for i in instance.abilities
        ]

        return cls(
            id=str(instance.id),
            name=instance.name,
            abilities=abilities,
            last_update=instance.last_update
        )

    def to_instance(self):
        abilities = [Ability(**i.to_dict()) for i in self.abilities]
        pokemon_data = self.to_dict()
        pokemon_data['abilities'] = abilities
        return Pokemon(**pokemon_data)
