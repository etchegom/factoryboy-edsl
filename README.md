# Factoryboy-edsl
Factoryboy helpers for [Elasticsearch-dsl](https://elasticsearch-dsl.readthedocs.io/en/latest/) documents.

[![PyPI version](https://badge.fury.io/py/factoryboy-edsl.svg)](https://badge.fury.io/py/factoryboy-edsl)
![Generic badge](https://github.com/etchegom/factoryboy-edsl/actions/workflows/main.yml/badge.svg)


## Installation

```
pip install factoryboy-edsl
```

## Usage

Simple usage:

```python
from factory_edsl import EDSLDocumentFactory, EDSLInnerDocFactory
from elasticsearch_dsl import Document, InnerDoc

# Define elasticsearch-dsl documents

class CommentDocument(InnerDoc):
    author = Text()
    content = Text()

class PostDocument(Document):
    title = Text()
    comments = Nested(CommentDocument)

    class Index:
        name = "index_name"

# Define factories

class CommentInnerDocFactory(EDSLInnerDocFactory):
    class Meta:
        model = CommentDocument

    author = factory.Faker("name")
    content = factory.Faker("sentence", nb_words=4)


class PostDocumentFactory(EDSLDocumentFactory):
    class Meta:
        model = PostDocument

    title = factory.Faker("sentence", nb_words=4)

# Build your test data

comments = CommentInnerDocFactory.create_batch(10)
post = PostDocumentFactory(comments=comments)
print(post.to_dict())
```

The factory-boy [strategies](https://factoryboy.readthedocs.io/en/stable/introduction.html#strategies) are applied:

```python
post = PostDocumentFactory.build() # in-memory only
post = PostDocumentFactory.create() # write to elastic cluster
```

Use `meta_id` arg to update an existing document:

```python
post = PostDocumentFactory(meta_id="999")
assert post.meta.id == "999"
assert PostDocument.exists(id="999")

post = PostDocumentFactory(meta_id="999", title="hello")
assert PostDocument.get(id="999").title == "hello"
```

Set option `strip_unknown_fields` to False to allow extra fields:

```python

class PostDocumentFactory(EDSLDocumentFactory):
    class Meta:
        model = PostDocument
        strip_unknown_fields = False

post = PostDocumentFactory(title="hello", extra_field="extra")

assert doc.title == "hello"
assert doc.extra_field == "extra"
```
