from __future__ import annotations

from elasticsearch_dsl import Document, connections
from elasticsearch_dsl.field import Date, Float, Integer, Text

connections.configure(
    default={
        "hosts": "http://localhost:9200",
    }
)

INDEX_NAME = "testing-edsl-factory"


class MyDocument(Document):
    class Index:
        name = INDEX_NAME

    name = Text()
    age = Integer()
    date = Date()
    score = Float()


class IndexBasedTest:
    def _delete_index(self):
        MyDocument._index.delete(ignore=404)

    def setup(self):
        self._delete_index()
        MyDocument.init()

    def teardown(self):
        self._delete_index()
