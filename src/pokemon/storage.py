from abc import ABC, abstractmethod
from typing import Optional

import sqlalchemy
from sqlalchemy import desc

from extensions import db
from lib.immudb_api import EQ, Comparison, ImmuDBClient, OrderBy, Query


class Storage(ABC):
    @abstractmethod
    def create(self, dto) -> Optional[str]:
        pass

    @abstractmethod
    def get_by(self, dto, field, value):
        pass

    @abstractmethod
    def get_all(
        self, dto, limit: Optional[int] = None, order_by: Optional[str] = None
    ):
        pass

    @abstractmethod
    def update(self, dto, new_data: dict):
        pass

    @abstractmethod
    def delete(self, dto):
        pass

    @abstractmethod
    def count(self, dto):
        pass

    @abstractmethod
    def rollback(self):
        pass


class PostgresStorage(Storage):
    def __init__(self, db_engine=None):
        self.db_engine = db_engine or db

    def create(self, dto) -> Optional[str]:
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

        return str(item_id)

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

    def delete(self, dto):
        pass


class ImmuDBStorage(Storage):
    def __init__(self, immudb_client=None):
        self.client = immudb_client or ImmuDBClient('')

    def create(self, dto) -> Optional[str]:
        if hasattr(dto, 'last_update'):
            dto.last_update = dto.last_update.strftime('%Y-%M-%d %H:%M:%S')

        document = self.client.create_document(dto.to_dict())
        return document.id

    def get_by(self, dto, field, value):
        comparison = Comparison(field=field, value=value)
        query = Query(comparisons=[comparison])
        result = self.client.search(query)
        if result is not None:
            dto.from_dict(result[0].data)

    def get_all(
        self, dto, limit: Optional[int] = None, order_by: Optional[str] = None
    ):
        query = Query()
        result = self.client.search(query)
        if result is not None:
            return [dto.from_instance(i.data) for i in result]

    def update(self, dto, new_data: dict):
        if hasattr(dto, 'last_update'):
            dto.last_update = dto.last_update.strftime('%Y-%M-%d %H:%M:%S')

        comparison = Comparison(field='id', value=dto.id)
        query = Query(comparisons=[comparison])
        document = self.client.update_document(new_data, query)
        return document.id

    def count(self, item_id=None):
        query = Query()
        return self.client.count(query)

    def delete(self, item_id):
        pass

    def rollback(self):
        pass
