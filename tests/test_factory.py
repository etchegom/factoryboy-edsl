from __future__ import annotations

import factory
from elasticsearch_dsl import Date, Document, Float, Integer, Keyword, Text
from factory_edsl import EDSLDocumentFactory


class MyDocument(Document):
    class Index:
        name = "my-index"

    name = Text()
    age = Integer()
    tags = Keyword(many=True)
    date = Date()
    score = Float()


class MyDocumentFactory(EDSLDocumentFactory):
    name = factory.Faker("name")
    age = factory.Faker("pyint", min_value=1, max_value=100)
    tags = factory.Faker("words", nb=3)
    date = factory.Faker("date")
    score = factory.Faker("pyfloat", positive=True)


class TestEDSLDocumentFactory:
    def test_simple(self):
        MyDocumentFactory.build()
