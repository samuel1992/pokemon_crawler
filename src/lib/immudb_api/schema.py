from dataclasses import dataclass
from typing import Optional


@dataclass
class Document:
    id: Optional[str] = None
    timestamp: Optional[str] = None
    creator: Optional[str] = None
    revision: str = ""
    transactionId: str = ""
    data: Optional[dict] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Document':
        document = data['document']
        document_data = {key: document[key]
                         for key in document if not key.startswith('_')}
        return cls(
            id=document['_id'],
            timestamp=document['_vault_md']['ts'],
            creator=document['_vault_md']['creator'],
            revision=data['revision'],
            transactionId=data['transactionId'],
            data=document_data
        )
