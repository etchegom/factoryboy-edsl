from __future__ import annotations

import pytest
from factory_edsl import EDSLDocumentFactory, EDSLInnerDocFactory

from .documents import PostDocument
from .factories import (
    CommentInnerDocFactory,
    CommentInnerDocFactoryNoStrip,
    PostDocumentFactory,
    PostDocumentFactoryNoStrip,
)


class IndexBasedTest:
    def _delete_index(self):
        PostDocument._index.delete(ignore=404)

    def setup(self):
        self._delete_index()
        PostDocument.init()

    def teardown(self):
        self._delete_index()


class TestEDSLDocumentFactory:
    @pytest.mark.parametrize("meta_id", ["1", 2, "dummy"])
    def test_meta_id(self, meta_id):
        assert PostDocumentFactory.build(meta_id=meta_id).meta.id == meta_id

    @pytest.mark.parametrize(
        "factory_class, expected_extra_fields",
        [
            (PostDocumentFactory, False),
            (PostDocumentFactoryNoStrip, True),
            (CommentInnerDocFactory, False),
            (CommentInnerDocFactoryNoStrip, True),
        ],
    )
    def test_strip_unknown_fields(self, factory_class, expected_extra_fields):
        doc = factory_class.build(tag="tag", extra_field="extra")
        assert doc.tag == "tag"
        if expected_extra_fields:
            assert hasattr(doc, "extra_field")
            assert doc.extra_field == "extra"
        else:
            assert not hasattr(doc, "extra_field")

    def test_nested_documents(self):
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
        PostDocumentFactory.create(meta_id="999", title="tag")
        doc = PostDocument.get(id="999")
        assert doc.title == "tag"

        PostDocumentFactory.create(meta_id="999", title="Post title 2")
        doc = PostDocument.get(id="999")
        assert doc.title == "Post title 2"

    def test_do_not_strip_unknown_fields(self):
        PostDocumentFactoryNoStrip.create(meta_id="888", title="tag", extra_field="extra")
        doc = PostDocument.get(id="888")
        assert doc.title == "tag"
        assert hasattr(doc, "extra_field")
        assert doc.extra_field == "extra"

    def test_nested_documents(self):
        comments = CommentInnerDocFactory.create_batch(10)
        doc = PostDocumentFactory(meta_id="777", comments=comments)
        doc = PostDocument.get(id="777")
        assert doc.comments == comments
