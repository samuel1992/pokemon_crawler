from abc import ABC, abstractmethod
from typing import Optional

import sqlalchemy
from sqlalchemy import desc


class Storage(ABC):
    @abstractmethod
    def create(self, item) -> Optional[int]:
        pass

    @abstractmethod
    def get_by_id(self, item_id):
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


class PostgresStorage(Storage):
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def create(self, item) -> Optional[int]:
        try:
            self.db_engine.add(item)
            self.db_engine.commit()
            self.db_engine.flush()
            item_id = item.id
        except sqlalchemy.exc.IntegrityError:
            return None
        finally:
            self.db_engine.close()

        return item_id

    def update(self, item_class, new_data: dict):
        item_id = new_data.get('id')
        if item_id is None:
            return

        self.db_engine.query(item_class).filter(
            item_class.id == item_id
        ).update(new_data)

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

    def delete(self, item_id: int):
        pass
