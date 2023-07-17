from .schema import Document


def test_create_document_from_immudb_api_response():
    id = "64b4616a000000000000000cdb10e50c"
    timestamp = 1689544328
    creator = "a:0ce01a9e-4c06-4c22-95d6-e4325821a6c2"
    revision = ""
    transactionId = ""
    data = {
        "name": "test samuel",
        "newfield": [
                "test",
            "test 3"
        ]
    }

    document_response = {
        "document": {
            "_id": id,
            "_vault_md": {
                "creator": creator,
                "ts": timestamp
            },
            **data
        },
        "revision": revision,
        "transactionId": transactionId,
    }
    document = Document.from_dict(document_response)

    assert document.id == id
    assert document.timestamp == timestamp
    assert document.creator == creator
    assert document.data == data
    assert document.revision == revision
    assert document.transactionId == transactionId


def test_create_document_to_send_to_immudb_api():
    document = Document(
        id="sometestid",
        timestamp=1689544328,
        creator="a:testsomecretor124",
        data={}
    )

    assert document is not None
