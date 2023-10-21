from __future__ import annotations

import pytest
from factory_edsl import EDSLDocumentFactory, EDSLInnerDocFactory

from .documents import PostDocument
from .factories import CommentInnerDocFactory, PostDocumentFactory, PostDocumentFactoryNoStrip


class IndexBasedTest:
    def _delete_index(self):
        PostDocument._index.delete(ignore=404)

    def setup(self):
        self._delete_index()
        PostDocument.init()

    def teardown(self):
        self._delete_index()


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

        doc = PostDocumentFactoryNoStrip.build(title="Post title 1", extra_field="extra")
        assert doc.title == "Post title 1"
        assert hasattr(doc, "extra_field")
        assert doc.extra_field == "extra"

    def test_nested(self):
        comment = PostDocumentFactory.build()
        doc = PostDocumentFactory.build(comments=[comment])
        assert doc.comments == [comment]

    def test_wrong_model_class(self):
        class DummyModelClass:
            def __init__(self, *args, **kwargs) -> None:
                pass

        with pytest.raises(TypeError):

            class PostDocumentFactoryWrongModelClass(EDSLDocumentFactory):
                class Meta:
                    model = DummyModelClass

        with pytest.raises(TypeError):

            class CommentDocumentFactoryWrongModelClass(EDSLInnerDocFactory):
                class Meta:
                    model = DummyModelClass


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
        PostDocumentFactoryNoStrip.create(meta_id="888", title="Post title 1", extra_field="extra")
        doc = PostDocument.get(id="888")
        assert doc.title == "Post title 1"
        assert hasattr(doc, "extra_field")
        assert doc.extra_field == "extra"

    def test_nested(self):
        comments = CommentInnerDocFactory.create_batch(10)
        doc = PostDocumentFactory(meta_id="777", comments=comments)
        doc = PostDocument.get(id="777")
        assert doc.comments == comments
