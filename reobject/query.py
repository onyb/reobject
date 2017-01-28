from collections import OrderedDict

from reobject.utils import cmp


class QuerySet(list):
    def __init__(self, *args, **kwargs):
        super(QuerySet, self).__init__(*args, **kwargs)

    @property
    def _attrs(self):
        return self[0]._attrs if self.exists() else set()

    def count(self):
        return len(self)

    def delete(self):
        for item in self:
            item.delete()

    def distinct(self, *attrs):
        if not attrs:
            attrs = self._attrs - {'created', 'updated'}

        meta = [
            (cmp(*attrs)(obj), obj)
            for obj in self.reverse()
        ]

        return type(self)(
            OrderedDict(meta).values()
        )

    def exists(self):
        return bool(self)

    def none(self):
        return EmptyQuerySet()

    def order_by(self, *attrs):
        if not attrs:
            raise AttributeError

        return type(self)(
            sorted(self, key=cmp(*attrs))
        )

    def reverse(self):
        return type(self)(
            reversed(self)
        )

    def values(self, *attrs):
        if not attrs:
            attrs = self._attrs

        print(attrs)
        return type(self)(
            dict(
                zip(attrs, obj)
            )
            for obj in map(cmp(*attrs), self)
        )

    def values_list(self, *attrs):
        if not attrs:
            attrs = self._attrs

        # TODO: Allow order_by on values_list
        return type(self)(
            map(cmp(*attrs), self)
        )


class EmptyQuerySet(QuerySet):
    def __init__(self, *args, **kwargs):
        super(QuerySet, self).__init__(*args, **kwargs)
