from typing import List, Optional

from .dto import AbilityDTO, PokemonDTO


class Repository:
    def __init__(self, storage, dto_class):
        self.storage = storage
        self.entity = dto_class

    def get_by_id(self, id: str):
        return self.storage.get_by(self.entity, 'id', id)

    def get_by_name(self, name):
        return self.storage.get_by(self.entity, 'name', name)

    def get_total(self) -> int:
        return self.storage.count(self.entity)

    def get_all(self, amount: Optional[int] = None):
        instances = self.storage.get_all(self.entity, amount)
        return [self.entity.from_instance(i) for i in instances]

    def create(self, dto):
        id = self.storage.create(dto)
        if id is not None:
            return self.get_by_id(id)

    def update(self, dto):
        if dto.id is None:
            return None

        self.storage.update(dto)
        return self.get_by_id(dto.id)
