from typing import List, Optional

from .dto import AbilityDTO, PokemonDTO


class IntegrityError(Exception):
    pass


class PokemonRepository:
    def __init__(self, storage, entity):
        self.storage = storage
        self.entity = entity

    def get_by_id(self, id: int) -> PokemonDTO:
        instance = self.storage.get_by_id(self.entity, id)
        return PokemonDTO.from_instance(instance)

    def get_total(self) -> int:
        return self.storage.count(self.entity)

    def get_all(self, amount: Optional[int] = None) -> List[PokemonDTO]:
        instances = self.storage.get_all(self.entity, amount)
        return [PokemonDTO.from_instance(i) for i in instances]

    def create(self, pokemon_dto: PokemonDTO) -> PokemonDTO:
        id = self.storage.create(pokemon_dto.to_instance)
        if id is None:
            raise IntegrityError()

        return self.get_by_id(id)


class AbilityRepository:
    def __init__(self, storage, entity):
        self.storage = storage
        self.entity = entity

    def get_by_id(self, id: int) -> AbilityDTO:
        instance = self.storage.get_by_id(self.entity, id)
        return AbilityDTO.from_instance(instance)

    def get_total(self) -> int:
        return self.storage.count(self.entity)

    def create(self, ability_dto: AbilityDTO) -> AbilityDTO:
        id = self.storage.create(ability_dto.to_instance)
        if id is None:
            raise IntegrityError()

        return self.get_by_id(id)

    def update(self, ability_dto: AbilityDTO) -> Optional[AbilityDTO]:
        if ability_dto.id is None:
            return None

        self.storage.update(self.entity, ability_dto.to_dict())
        return self.get_by_id(ability_dto.id)
