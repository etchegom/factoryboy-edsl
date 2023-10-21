from __future__ import annotations

from elasticsearch_dsl import Document, InnerDoc, connections
from elasticsearch_dsl.field import (
    Boolean,
    Completion,
    Date,
    Float,
    Integer,
    Keyword,
    Nested,
    Text,
)

connections.configure(
    default={
        "hosts": "http://localhost:9200",
    }
)

INDEX_NAME = "testing-edsl-factory"


class CommentDocument(InnerDoc):
    author = Text(fields={"raw": Keyword()})
    content = Text(analyzer="snowball")
    created_at = Date()
    tag = Keyword()


class PostDocument(Document):
    title = Text()
    title_suggest = Completion()
    published = Boolean()
    rating = Integer()
    rank = Float()
    tag = Keyword()

    comments = Nested(CommentDocument)

    class Index:
        name = INDEX_NAME
