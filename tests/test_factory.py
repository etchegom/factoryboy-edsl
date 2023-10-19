from __future__ import annotations

import factory
from factory_edsl import EDSLDocumentFactory

from .utils import IndexBasedTest, PostDocument


class PostDocumentFactory(EDSLDocumentFactory):
    class Meta:
        model = PostDocument

    title = factory.Faker("sentence", nb_words=4)
    title_suggest = factory.Faker("sentence", nb_words=4)
    published = factory.Faker("pybool")
    rating = factory.Faker("pyint", min_value=1, max_value=5)
    rank = factory.Faker("pyfloat", positive=True)


class MyDocumentFactoryNoStrip(PostDocumentFactory):
    class Meta:
        model = PostDocument
        strip_unknown_fields = False


class TestEDSLDocumentFactory:
    def test_meta_id(self):
        doc = PostDocumentFactory.build(meta_id="1")
        assert doc.meta.id == "1"
        doc = PostDocumentFactory.build(meta_id=2)
        assert doc.meta.id == 2

    def test_allow_extra_fields(self):
        doc = PostDocumentFactory.build(title="Post title 1", extra_field="extra")
        assert doc.title == "Post title 1"
        assert not hasattr(doc, "extra_field")

        doc = MyDocumentFactoryNoStrip.build(title="Post title 1", extra_field="extra")
        assert doc.title == "Post title 1"
        assert hasattr(doc, "extra_field")
        assert doc.extra_field == "extra"


class TestEDSLDocumentFactoryWithPersistence(IndexBasedTest):
    def test_build_is_not_written(self):
        PostDocumentFactory.build(meta_id="999")
        assert not PostDocument.exists(id="999")

    def test_create_and_update(self):
        PostDocumentFactory.create(meta_id="999", title="Post title 1")
        doc = PostDocument.get(id="999")
        assert doc.title == "Post title 1"

        PostDocumentFactory.create(meta_id="999", title="Post title 2")
        doc = PostDocument.get(id="999")
        assert doc.title == "Post title 2"

    def test_no_strip(self):
        MyDocumentFactoryNoStrip.create(meta_id="888", title="Post title 1", extra_field="extra")
        doc = PostDocument.get(id="888")
        assert doc.title == "Post title 1"
        assert hasattr(doc, "extra_field")
        assert doc.extra_field == "extra"
