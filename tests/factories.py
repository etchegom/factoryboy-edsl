from __future__ import annotations

import factory
from factory_edsl import EDSLDocumentFactory, EDSLInnerDocFactory

from .documents import CommentDocument, PostDocument


class CommentInnerDocFactory(EDSLInnerDocFactory):
    class Meta:
        model = CommentDocument

    author = factory.Faker("name")
    content = factory.Faker("sentence", nb_words=4)
    created_at = factory.Faker("date_time")
    tag = factory.Faker("word")


class PostDocumentFactory(EDSLDocumentFactory):
    class Meta:
        model = PostDocument

    title = factory.Faker("sentence", nb_words=4)
    title_suggest = factory.Faker("sentence", nb_words=4)
    published = factory.Faker("pybool")
    rating = factory.Faker("pyint", min_value=1, max_value=5)
    rank = factory.Faker("pyfloat", positive=True)
    tag = factory.Faker("word")


class CommentInnerDocFactoryNoStrip(CommentInnerDocFactory):
    class Meta:
        model = CommentDocument
        strip_unknown_fields = False


class PostDocumentFactoryNoStrip(PostDocumentFactory):
    class Meta:
        model = PostDocument
        strip_unknown_fields = False


class PostDocumentFactoryWithComments(PostDocumentFactory):
    class Meta:
        model = PostDocument
