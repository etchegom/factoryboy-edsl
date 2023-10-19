from __future__ import annotations

from factory import base


class EDSLFactoryOptions(base.FactoryOptions):
    def _build_default_options(self):
        return super()._build_default_options() + [
            base.OptionDefault("strip_unknown_fields", True, inherit=True)
        ]


class EDSLDocumentFactory(base.Factory):
    _options_class = EDSLFactoryOptions

    class Meta:
        abstract = True

    @classmethod
    def _get_field_names(cls):
        doc_cls = cls._meta.model
        for name in doc_cls._doc_type.mapping:
            yield name

        if hasattr(doc_cls.__class__, "_index"):
            if not cls._index._mapping:
                return
            for name in doc_cls._index._mapping:
                # don't return fields that are in _doc_type
                if name in doc_cls._doc_type.mapping:
                    continue
                yield name

    @classmethod
    def _get_object(cls, model_class, *args, **kwargs):
        meta_id = kwargs.pop("meta_id", None)

        if cls._meta.strip_unknown_fields:
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in cls._get_field_names()}
        else:
            filtered_kwargs = kwargs

        obj = model_class(*args, **filtered_kwargs)
        if meta_id:
            obj.meta.id = meta_id
        return obj

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        return cls._get_object(model_class, *args, **kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = cls._get_object(model_class, *args, **kwargs)
        obj.save()
        return obj
