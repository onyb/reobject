---
layout: default
---

# [](#header-1)reobject QuerySet API

The result of a reobject query is a QuerySet.

### [](#header-2)Methods that return new QuerySets


##### [](#header-5)all()

##### [](#header-5)filter(*args, **kwargs)

Returns a new `QuerySet` containing objects that match the given lookup parameters.

The lookup parameters should be specified as `**kwargs` and must conform to a
specific format which bears close resemblance with the Django ORM.

It also possible to construct complex `Q` objects and pass them to the `filter()`
as `*args`.

Multiple parameters (`*args` or `**kwargs`) are joined together with a logical AND.

For example, some ways to filter all objects in `queryset` where `0 <= value < 1`
are shown below.

```py
>>> # Multiple keyword-only query
>>> queryset.filter(value__gte=0, value__lt=1)
```

```py
>>> # Chained keyword-only query
>>> queryset.filter(value__gte=0).filter(value__lt=1)
```

```py
>>> # Mixed query containing Q object and kwargs
>>> queryset.filter(Q(value__gte=0), value__lt=1)
```

```py
>>> # Arg-only query with a single Q object: Q & Q => Q
>>> queryset.filter(Q(value__gte=0) & Q(value__lt=1))
```
