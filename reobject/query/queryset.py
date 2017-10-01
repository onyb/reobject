import random
from collections import OrderedDict
from itertools import chain
from typing import Tuple, Optional as Maybe, Dict, Any, Iterable

from reobject.exceptions import DoesNotExist, MultipleObjectsReturned
from reobject.query.parser import Q
from reobject.utils import cmp, flatmap

from ..types import LookupParams, Fields


class QuerySet(list):
    def __init__(self, *args, model, **kwargs):
        super(QuerySet, self).__init__(*args, **kwargs)
        self.model = model

    @property
    def _attrs(self):
        return self[0]._attrs if self.exists() else set()

    def __or__(self, other: 'QuerySet') -> 'QuerySet':
        return type(self)(
            chain(self, other),
            model=self.model
        ).distinct('id')

    def count(self) -> int:  # type: ignore
        return len(self)

    def delete(self) -> Tuple[int, dict]:
        _len = self.count()
        _type = self.model.__name__

        for item in self:
            item.delete()

        return _len, {_type: _len}

    def distinct(self, *fields: Fields) -> 'QuerySet':
        if not fields:
            fields = self._attrs - {'created', 'updated'}

        meta = [
            (cmp(*fields)(obj), obj)
            for obj in self.reverse()
        ]

        return type(self)(
            OrderedDict(meta).values(),
            model=self.model
        ).reverse()

    def earliest(self, field_name: str = 'created') -> Maybe['Model']:
        try:
            obj = self.filter(
                **{field_name + '__isnone': False}
            ).order_by(
                field_name
            )[0]
        except IndexError:
            return None
        else:
            return obj

    def exclude(self, *args: Tuple[Q, ...], **kwargs: LookupParams) -> 'QuerySet':
        q = ~(Q.from_Qs(*args) & Q(**kwargs))

        return type(self)(
            filter(q.comparator, self),
            model=self.model
        )

    def exists(self) -> bool:
        return bool(self)

    def filter(self, *args: Tuple[Q, ...], **kwargs: LookupParams) -> 'QuerySet':
        q = Q.from_Qs(*args) & Q(**kwargs)

        return type(self)(
            filter(q.comparator, self),
            model=self.model
        )

    def first(self) -> Maybe['Model']:  # type: ignore
        try:
            obj = self[0]
        except IndexError:
            return None
        else:
            return obj

    def get(self, *args: Tuple[Q, ...], **kwargs: LookupParams):
        result_set = self.filter(*args, **kwargs)

        if len(result_set) == 0:
            raise DoesNotExist(
                '{model} object matching query does not exist.'.format(
                    model=self.model.__name__
                )
            )

        elif len(result_set) == 1:
            return result_set[0]
        else:
            raise MultipleObjectsReturned(
                'get() returned more than one {model} object '
                '-- it returned {num}!'.format(
                    model=self.model.__name__, num=len(result_set)
                )
            )

    def get_or_create(self, defaults=None, **kwargs: LookupParams):
        try:
            obj = self.get(**kwargs)
        except DoesNotExist:
            params = {k: v for k, v in kwargs.items() if '__' not in k}

            if defaults:
                params.update(defaults)

            obj = self.model(**params)
            return obj, True
        else:
            return obj, False

    def last(self) -> Maybe['Model']:  # type: ignore
        try:
            obj = self[-1]
        except IndexError:
            return None
        else:
            return obj

    def latest(self, field_name: str = 'created') -> Maybe['Model']:  # type: ignore
        try:
            obj = self.filter(
                **{field_name + '__isnone': False}
            ).order_by(
                field_name
            )[-1]
        except IndexError:
            return None
        else:
            return obj

    def map(self, func) -> Iterable:
        if not callable(func):
            raise TypeError(
                'Expected a callable, got {}'.format(type(func))
            )

        return map(func, self)

    def none(self) -> 'EmptyQuerySet':
        return EmptyQuerySet(model=self.model)

    def order_by(self, *fields: Fields):
        if not fields:
            raise AttributeError

        return type(self)(
            sorted(self, key=cmp(*fields)),
            model=self.model
        )

    def random(self) -> Maybe['Model']:  # type: ignore
        try:
            obj = random.choice(self)
        except IndexError:
            return None
        else:
            return obj

    def reverse(self) -> 'QuerySet':
        return type(self)(
            reversed(self),
            model=self.model
        )

    def values(self, *fields: Fields) -> 'QuerySet':
        if not fields:
            fields = self._attrs

        return type(self)(
            (
                dict(zip(fields, obj))
                for obj in map(cmp(*fields), self)
            ),
            model=self.model
        )

    def values_list(self, *fields: Fields, flat: bool=False) -> 'QuerySet':
        # TODO: Allow order_by on values_list

        if not fields:
            fields = self._attrs

        if len(fields) > 1 and flat:
            raise TypeError(
                '/flat/ is not valid when values_list is called with more than '
                'one field.'
            )

        return type(self)(
            (flatmap if flat else map)(cmp(*fields), self),
            model=self.model
        )


class EmptyQuerySet(QuerySet):
    def __init__(self, model: 'Model', *args, **kwargs) -> None:  # type: ignore
        super(QuerySet, self).__init__(*args, **kwargs)
        self.model = model
