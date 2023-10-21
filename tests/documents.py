from __future__ import annotations

from datetime import datetime

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

    def age(self):
        return datetime.now() - self.created_at


class PostDocument(Document):
    title = Text()
    title_suggest = Completion()
    created_at = Date()
    published = Boolean()
    rating = Integer()
    rank = Float()

    comments = Nested(CommentDocument)

    class Index:
        name = INDEX_NAME

    def add_comment(self, author, content):
        self.comments.append(
            CommentDocument(
                author=author,
                content=content,
                created_at=datetime.now(),
            )
        )

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super().save(**kwargs)
