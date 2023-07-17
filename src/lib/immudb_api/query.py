from typing import List, Optional

EQ = 'EQ'


class Comparison:
    def __init__(self, field: str, value: str = '', operator: str = EQ):
        assert field, 'Field is required'

        self.field = field
        self.value = value
        self.operator = operator

    def to_dict(self):
        return {
            'field': self.field,
            'value': self.value,
            'operator': self.operator
        }


class OrderBy:
    def __init__(self, field: str, desc: bool = True):
        self.field = field
        self.desc = desc

    def to_dict(self):
        return {
            'field': self.field,
            'desc': self.desc
        }


class Query:
    def __init__(
        self,
        comparisons: Optional[List[Comparison]] = None,
        order_by: Optional[List[OrderBy]] = None,
        page: int = 1,
        per_page: int = 100
    ):
        self.comparisons = comparisons
        self.order_by = order_by
        self.page = page
        self.per_page = per_page

    def to_dict(self):
        query = {
            'keepOpen': True,
            'query': {
                'limit': 0
            },
            'page': self.page,
            'perPage': self.per_page
        }

        if self.comparisons is not None:
            query['query']['expressions'] = [i.to_dict() for i in self.comparisons]

        if self.order_by is not None:
            query['query']['orderBy'] = [i.to_dict() for i in self.order_by]

        return query
