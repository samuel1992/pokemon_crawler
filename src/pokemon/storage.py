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
    def get_by_id(self, item_id):
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

    def create(self, item) -> Optional[int]:
        try:
            self.db_engine.add(item)
            self.db_engine.commit()
            item_id = item.id
        except sqlalchemy.exc.IntegrityError:
            self.db_engine.rollback()
            return None
        finally:
            self.db_engine.close()

        return item_id

    def update(self, item):
        self.db_engine.merge(item)
        self.db_engine.commit()
        self.db_engine.close()

    def get_all(
        self, item_class, limit: Optional[int] = None, order_by: Optional[str] = None
    ):
        query = self.db_engine.query(item_class)

        if order_by is not None:
            query.order_by(desc(getattr(item_class, order_by)))

        return [i for i in query.limit(limit).all()]

    def count(self, item_class) -> int:
        return self.db_engine.query(item_class).count()

    def get_by_id(self, item_class, item_id):
        return self.db_engine.query(item_class).get(item_id)

    def get_by(self, item_class, field, value):
        return self.db_engine.query(item_class).filter(
            getattr(item_class, field) == value
        ).first()

    def rollback(self):
        self.db_engine.rollback()

    def delete(self, item_id: int):
        pass
