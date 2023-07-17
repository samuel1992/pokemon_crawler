import unittest
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple
from unittest.mock import MagicMock, Mock, patch

from requests import Response

from .client import ImmuDBClient
from .schema import Document


class ImmuDBClientTests(unittest.TestCase):
    def setUp(self):
        self.client = ImmuDBClient(token='test_token', ledger='test_ledger', collection='test_collection')

    @patch('requests.put')
    def test_create_document_success(self, put_mock):
        document_data = {'key': 'value'}
        response_data = {'documentId': 'doc_id', 'transactionId': 'trans_id'}
        response_mock = Mock(spec=Response)
        response_mock.ok = True
        response_mock.json.return_value = response_data
        put_mock.return_value = response_mock

        document = self.client.create_document(document_data)

        put_mock.assert_called_once_with(
            self.client.url + f'/ledger/{self.client.ledger}/collection/{self.client.collection}/document',
            headers=self.client.headers,
            json=document_data
        )
        self.assertEqual(document.id, response_data['documentId'])
        self.assertEqual(document.transactionId, response_data['transactionId'])

    @patch('requests.put')
    def test_create_document_failure(self, put_mock):
        document_data = {'key': 'value'}
        response_mock = Mock(spec=Response)
        response_mock.ok = False
        response_mock.raise_for_status.side_effect = Exception('Error message')
        put_mock.return_value = response_mock

        with self.assertRaises(Exception) as cm:
            self.client.create_document(document_data)

        self.assertEqual(str(cm.exception), 'Error message')

    @patch('requests.post')
    def test_update_document_success(self, post_mock):
        document = Document(id='doc_id', transactionId='trans_id', data={'key': 'value'})
        query = MagicMock()
        query.to_dict = MagicMock()
        response_data = {'documentId': 'updated_doc_id', 'transactionId': 'updated_trans_id'}
        response_mock = Mock(spec=Response)
        response_mock.ok = True
        response_mock.json.return_value = response_data
        post_mock.return_value = response_mock

        updated_document = self.client.update_document(document, query)

        post_mock.assert_called_once_with(
            self.client.url + f'/ledger/{self.client.ledger}/collection/{self.client.collection}/document',
            headers=self.client.headers,
            json={'document': document.data, 'query': query.to_dict()}
        )
        self.assertEqual(updated_document.id, response_data['documentId'])
        self.assertEqual(updated_document.transactionId, response_data['transactionId'])

    @patch('requests.post')
    def test_search_success(self, post_mock):
        document_response = {
            "document": {
                "_id": "test",
                "_vault_md": {
                    "creator": "test",
                    "ts": 1689544328
                }
            },
            "revision": "",
            "transactionId": "",
        }
        query = MagicMock()
        query.to_dict = MagicMock()
        response_data = {'searchId': 'search_id', 'revisions': [document_response]}
        response_mock = Mock(spec=Response)
        response_mock.ok = True
        response_mock.json.return_value = response_data
        post_mock.return_value = response_mock

        documents = self.client.search(query)

        post_mock.assert_called_once_with(
            self.client.url + f'/ledger/{self.client.ledger}/collection/{self.client.collection}/documents/search',
            headers=self.client.headers,
            json=query.to_dict()
        )
        self.assertEqual(len(documents), len(response_data['revisions']))

    @patch('requests.post')
    def test_count_success(self, post_mock):
        query = MagicMock()
        query.to_dict = MagicMock()
        response_data = {'count': 10}
        response_mock = Mock(spec=Response)
        response_mock.ok = True
        response_mock.json.return_value = response_data
        post_mock.return_value = response_mock

        count = self.client.count(query)

        post_mock.assert_called_once_with(
            self.client.url + f'/ledger/{self.client.ledger}/collection/{self.client.collection}/documents/count',
            headers=self.client.headers,
            json=query.to_dict()
        )
        self.assertEqual(count, response_data['count'])
