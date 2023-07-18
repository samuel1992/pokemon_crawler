import requests

from typing import Optional, List

from .schema import Document
from .query import Query


class ImmuDBClient:
    api_version = 'v1'
    base_url = 'https://vault.immudb.io/ics/api'

    def __init__(self, token: str, ledger='default', collection='default'):
        self.token = token
        self.ledger = ledger
        self.collection = collection

    @property
    def url(self):
        return f'{self.base_url}/{self.api_version}'

    @property
    def headers(self):
        return {
            'X-API-KEY': self.token,
            'Content-Type': 'application/json'
        }

    def create_collection(self, specification: dict) -> bool:
        endpoint = f'/ledger/{self.ledger}/collection/{self.collection}'
        url = self.url + endpoint
        requests.delete(url, headers=self.headers)
        response = requests.put(url, headers=self.headers, json=specification)
        return response.ok

    def create_document(self, document_data: dict) -> Optional[Document]:
        endpoint = f'/ledger/{self.ledger}/collection/{self.collection}/document'
        url = self.url + endpoint
        response = requests.put(url, headers=self.headers, json=document_data)
        if not response.ok:
            response.raise_for_status()

        response_data = response.json()
        return Document(id=response_data['documentId'],
                        transactionId=response_data['transactionId'])

    def update_document(self, document: Document, query: Query) -> Optional[Document]:
        endpoint = f'/ledger/{self.ledger}/collection/{self.collection}/document'
        url = self.url + endpoint
        data = {
            'document': document.data,
            'query': query.to_dict()
        }
        response = requests.post(url, headers=self.headers, json=data)
        if not response.ok:
            response.raise_for_status()

        response_data = response.json()
        return Document(id=response_data['documentId'],
                        transactionId=response_data['transactionId'])

    def search(self, query: Query) -> List[Optional[Document]]:
        endpoint = f'/ledger/{self.ledger}/collection/{self.collection}/documents/search'
        url = self.url + endpoint
        response = requests.post(url, headers=self.headers, json=query.to_dict())
        if not response.ok:
            response.raise_for_status()

        search_id = response.json().get('searchId')
        return [Document.from_dict(i) for i in response.json()['revisions']]

    def count(self, query: Query) -> int:
        endpoint = f'/ledger/{self.ledger}/collection/{self.collection}/documents/count'
        url = self.url + endpoint
        response = requests.post(url, headers=self.headers, json=query.to_dict())
        if not response.ok:
            response.raise_for_status()

        return response.json()['count']
