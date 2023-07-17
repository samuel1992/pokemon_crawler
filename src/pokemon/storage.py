from abc import ABC, abstractmethod
from typing import Optional

import sqlalchemy
from sqlalchemy import desc

from extensions import db


class Storage(ABC):
    @abstractmethod
    def create(self, item) -> Optional[int]:
        pass

    @abstractmethod
    def get_by(self, item, field, value):
        pass

    @abstractmethod
    def get_all(
        self, item, limit: Optional[int] = None, order_by: Optional[str] = None
    ):
        pass

    @abstractmethod
    def update(self, item, new_data: dict):
        pass

    @abstractmethod
    def delete(self, item_id):
        pass

    @abstractmethod
    def count(self, item):
        pass

    @abstractmethod
    def rollback(self):
        pass


class PostgresStorage(Storage):
    def __init__(self, db_engine=None):
        self.db_engine = db_engine or db

    def create(self, dto) -> Optional[int]:
        instance = dto.to_instance()
        try:
            self.db_engine.add(instance)
            self.db_engine.commit()
            item_id = instance.id
        except sqlalchemy.exc.IntegrityError:
            self.db_engine.rollback()
            return None
        finally:
            self.db_engine.close()

        return item_id

    def update(self, dto):
        instance = dto.to_instance()
        self.db_engine.merge(instance)
        self.db_engine.commit()
        self.db_engine.close()

    def get_all(
        self, dto, limit: Optional[int] = None, order_by: Optional[str] = None
    ):
        item_class = dto.instance_class
        query = self.db_engine.query(item_class)

        if order_by is not None:
            query.order_by(desc(getattr(item_class, order_by)))

        return [dto.from_instance(i) for i in query.limit(limit).all()]

    def count(self, dto) -> int:
        item_class = dto.instance_class
        return self.db_engine.query(item_class).count()

    def get_by(self, dto, field, value):
        instance = self.db_engine.query(dto.instance_class).filter(
            getattr(dto.instance_class, field) == value
        ).first()
        if instance is not None:
            return dto.from_instance(instance)

    def rollback(self):
        self.db_engine.rollback()

    def delete(self, item_id: int):
        pass


class ImmuDBStorage(Storage):
    def create(self, item) -> Optional[int]:
        pass

    def get_by(self, item, field, value):
        pass

    def get_all(
        self, item, limit: Optional[int] = None, order_by: Optional[str] = None
    ):
        pass

    def update(self, item, new_data: dict):
        pass

    def delete(self, item_id):
        pass

    def count(self, item):
        pass

    def rollback(self):
        pass
