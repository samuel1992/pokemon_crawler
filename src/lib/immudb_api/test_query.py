from .query import EQ, Comparison, OrderBy, Query


def test_comparison():
    comparison = Comparison(field='id', value='test', operator=EQ)

    assert comparison.to_dict() == {
        'field': 'id',
        'value': 'test',
        'operator': EQ
    }


def test_order_by():
    order_by = OrderBy(field='id', desc=False)

    assert order_by.to_dict() == {
        'field': 'id',
        'desc': False
    }

    order_by = OrderBy(field='id', desc=True)

    assert order_by.to_dict() == {
        'field': 'id',
        'desc': True
    }

def test_query():
    query = Query()

    assert query.to_dict() == {
        'keepOpen': True,
        'query': {
            'limit': 0
        },
        'page': 1,
        'perPage': 100
    }


def test_query_with_comparisons():
    comparison = Comparison(field='id', value='test', operator=EQ)
    query = Query(comparisons=[comparison], page=1, per_page=100)

    assert query.to_dict() == {
        'keepOpen': True,
        'query': {
            'expressions': [
                { 'fieldComparisons': [comparison.to_dict()] }
            ],
            'limit': 0
        },
        'page': 1,
        'perPage': 100
    }

def test_query_with_order_by():
    comparison = Comparison(field='id', value='test', operator=EQ)
    order_by = OrderBy(field='id', desc=False)
    query = Query(comparisons=[comparison], order_by=[order_by], page=1, per_page=100)

    assert query.to_dict() == {
        'keepOpen': True,
        'query': {
            'expressions': [
                { 'fieldComparisons': [comparison.to_dict()] }
            ],
            'orderBy': [
                order_by.to_dict()
            ],
            'limit': 0
        },
        'page': 1,
        'perPage': 100
    }
