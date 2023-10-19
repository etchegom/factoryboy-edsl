from __future__ import annotations

import factory
from factory_edsl import EDSLDocumentFactory

from .utils import IndexBasedTest, MyDocument


class MyDocumentFactory(EDSLDocumentFactory):
    class Meta:
        model = MyDocument

    name = factory.Faker("name")
    age = factory.Faker("pyint", min_value=1, max_value=100)
    date = factory.Faker("date")
    score = factory.Faker("pyfloat", positive=True)


class MyDocumentFactoryNoStrip(MyDocumentFactory):
    class Meta:
        model = MyDocument
        strip_unknown_fields = False


class TestEDSLDocumentFactory:
    def test_meta_id(self):
        doc = MyDocumentFactory.build(meta_id="1")
        assert doc.meta.id == "1"
        doc = MyDocumentFactory.build(meta_id=2)
        assert doc.meta.id == 2

    def test_allow_extra_fields(self):
        doc = MyDocumentFactory.build(name="Anakin Skywalker", extra_field="extra")
        assert doc.name == "Anakin Skywalker"
        assert not hasattr(doc, "extra_field")

        doc = MyDocumentFactoryNoStrip.build(name="Anakin Skywalker", extra_field="extra")
        assert doc.name == "Anakin Skywalker"
        assert hasattr(doc, "extra_field")
        assert doc.extra_field == "extra"


class TestEDSLDocumentFactoryWithPersistence(IndexBasedTest):
    def test_build_is_not_written(self):
        MyDocumentFactory.build(meta_id="999")
        assert not MyDocument.exists(id="999")

    def test_create_and_update(self):
        MyDocumentFactory.create(meta_id="999", name="Anakin Skywalker")
        doc = MyDocument.get(id="999")
        assert doc.name == "Anakin Skywalker"

        MyDocumentFactory.create(meta_id="999", name="Obi-Wan Kenobi")
        doc = MyDocument.get(id="999")
        assert doc.name == "Obi-Wan Kenobi"

    def test_no_strip(self):
        MyDocumentFactoryNoStrip.create(meta_id="888", name="Anakin Skywalker", extra_field="extra")
        doc = MyDocument.get(id="888")
        assert doc.name == "Anakin Skywalker"
        assert hasattr(doc, "extra_field")
        assert doc.extra_field == "extra"
