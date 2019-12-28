---
layout: default
---

# [](#header-1)reobject QuerySet API

The result of a reobject query is a QuerySet.

### [](#header-2)QuerySet methods


##### [](#header-5)filter(*args, **kwargs)

Returns a new `QuerySet` containing objects that match the given lookup
parameters.

The lookup parameters should be specified as `**kwargs` and must conform to a
specific format which bears close resemblance with the Django ORM.

It also possible to construct complex `Q` objects and pass them to the
`filter()` as `*args`.

Multiple parameters (`*args` or `**kwargs`) are joined together with a logical
`AND`.

For example, some ways to filter all objects in `queryset` where
`0 <= value < 1` are shown below.

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

##### [](#header-5)get(*args, **kwargs)

Returns the object matching the given lookup parameters.
The lookup parameter syntax is same as that in `filter()`.

`get()` raises `MultipleObjectsReturned` if more than one object was found.

`get()` raises a `DoesNotExist` exception if an object wasn’t found for the given parameters.

Example:

```py
>>> queryset.get(nom='Doe', prenom='John')
```

##### [](#header-5)all()

Returns the same queryset on which it is operated on. It is an identity method. 

##### [](#header-5)exclude(*args, **kwargs)

Returns a new `QuerySet` containing objects that *do not* match the given
lookup parameters.

The format of lookup parameters is the same as that of `filter()`. Multiple
parameters are joined via `AND`, and the whole thing is enclosed in a `NOT`.


For example, some ways to exclude all objects in `queryset` where
`0 <= value < 1` are shown below.

```py
>>> # Multiple keyword-only query
>>> queryset.exclude(value__gte=0, value__lt=1)
```

```py
>>> # Arg-only query with a single Q object: Q & Q => Q
>>> queryset.exclude(Q(value__gte=0) & Q(value__lt=1))
```

```py
>>> # Applying De Morgan's
>>> queryset.filter(~Q(value__gte=0) | ~Q(value__lt=1)))
```

##### [](#header-5)count()

Returns an integer representing the number of objects in the `QuerySet`. Same
as performing a `len()` on the `QuerySet`.

```py
>>> # Number of entries whose headline contains 'Lennon'
>>> Entry.objects.filter(headline__contains='Lennon').count()
7
```

##### [](#header-5)delete()

Removes all objects in the `QuerySet`, and returns the number of objects
deleted and a dictionary with the number of deletions per object type.

<p class="note">
  <strong>Note:</strong> Deleting an object only untracks it from reobject
  store, and doesn't actually garbage collect it.
</p>

```py
>>> # Delete entries whose headline contains 'Lennon'
>>> Entry.objects.filter(headline__contains='Lennon').delete()
(7, {'Entry': 7})
```

##### [](#header-5)latest(field_name='created')

Returns the latest object in the queryset, by date, using the `fieldname`.
By default, the `created` field is used as `fieldname`.

```py
>>> # Most recently updated entry whose headline is 'Lennon'
>>> Entry.objects.filter(headline='Lennon').latest('updated')
```

##### [](#header-5)earliest(field_name='created')

Works otherwise like `latest()` except the direction is changed.

##### [](#header-5)last()

Returns the last object matched by the queryset, or `None`
if there is no matching object.

##### [](#header-5)first()

Works like `last()`, but returns the first object in the queryset.

##### [](#header-5)reverse()

Reverses the order in which a queryset’s elements are returned.

##### [](#header-5)random()

Returns a random object matched by the queryset, or `None`
if there is no matching object.

##### [](#header-5)none()

Returns instance of an `EmptyQuerySet`.

##### [](#header-5)order_by(*fields)

Returns a `QuerySet` ordered by `fields`. Ascending order is implied by default.

**Example:**

```py
>>> Character.objects.all()
[Character(first_name='Ned', last_name='Stark'),
 Character(first_name='Catelyn', last_name='Stark'),
 Character(first_name='Robert', last_name='Baratheron')]

>>> Character.objects.filter().order_by('last_name', 'first_name')
[Character(first_name='Robert', last_name='Baratheron'),
 Character(first_name='Catelyn', last_name='Stark'),
 Character(first_name='Ned', last_name='Stark')]
```

<p class="note">
  <strong>Note:</strong> To indicate descending order, prepend the ordering 
  field with a negative sign, like <code>-age</code>. Ordering by descending
  order is only supported for integer fields.
</p>


##### [](#header-5)distinct(*fields)

Returns a new `QuerySet` with all objects with duplicate fields removed.

For a `distinct()` call without arguments, each field in each object
is compared when determining which objects are distinct. For a `distinct()`
call with specified field names, only the specified field names are compared.

<p class="note">
  <strong>Note:</strong> Performing <code>distinct()</code> gives you the
  first object for each duplicate entry. It is therefore important to make
  sure that the queryset on which <code>distinct()</code> is applied, has
  been ordered using <code>order_by()</code>. If you don't specify an order,
  you'll get some arbitrary row.
</p>

**Example:** applying `distinct()` by `last_name` on the queryset defined in the
example of `order_by()`.

```py
>>> queryset.distinct('last_name')
[Character(first_name='Robert', last_name='Baratheron'),
 Character(first_name='Catelyn', last_name='Stark')]
```

##### [](#header-5)map(func)

Applies a `callable` function on each item in the `QuerySet` and yields
a generator `map` object containing the result.

**Example:**
```py
>>> queryset
[Character(first_name='robert', last_name='baratheron'),
 Character(first_name='catelyn', last_name='stark')]
>>> list(queryset.map(lambda x: x.first_name.upper()))
['ROBERT', 'CATELYN']
```

##### [](#header-5)values(*fields)

Returns a `QuerySet` that returns dictionaries, rather than model instances.
Each of those dictionaries represents an object, with the keys corresponding
to the attribute names of model objects.

If no field is specified, the dictionaries will contain all the attributes.

**Example:**

```py
>>> Book.objects.filter(price__lt=50).values('title')
[{'title': 'The Go Programming Language'}, ...]
```

##### [](#header-5)values_list(*fields, flat=False)

Same as `values()`, but returns tuples instead of dictionaries.

For one-tuple values, passing the `flat` parameter will flatten them and return
single values.

**Example:**
```py
>>> Character.objects.filter().values_list('first_name', flat=True)
['Robert', 'Catelyn', 'Ned']
```

### [](#header-2)Field lookups

Field lookup parameters are specified as keyword arguments to the `QuerySet`
methods `filter()`, `exclude()` and `get()`.

By default, when no lookup type is provided the lookup type is assumed to be
`exact`.

##### [](#header-5)exact

Exact match.

**Examples:**

```py
>>> Entry.objects.get(id__exact=14)
>>> Entry.objects.get(id__exact=None)
```

##### [](#header-5)iexact

Case-insensitive exact match.

**Examples:**

```py
>>> Character.objects.get(first_name__iexact='NeD')
Character(first_name='Ned', last_name='Stark')
```

##### [](#header-5)contains

Case-sensitive containment test.

**Examples:**

```py
>>> Character.objects.filter(first_name__contains='Cate')
Character(first_name='Catelyn', last_name='Stark')

>>> # Also works for non-string iterables
>>> SomeModel.objects.filter(list_attr__contains='item')
SomeModel(list_attr=['item', 'another item', ...])
```

##### [](#header-5)icontains

Case-insensitive containment test.

**Examples:**

```py
>>> Character.objects.filter(first_name__icontains='cAtE')
Character(first_name='Catelyn', last_name='Stark')

>>> # Also works for non-string iterables
>>> SomeModel.objects.filter(list_attr__icontains='item')
SomeModel(list_attr=['ITEM', ...])
```

##### [](#header-5)in

In a given list.

**Examples:**

```py
>>> Character.objects.filter(last_name__in='Starks')
[Character(first_name='Ned', last_name='Stark'),
 Character(first_name='Catelyn', last_name='Stark')]

>>> # Also works for non-string iterables
>>> Character.objects.filter(last_name__in=['Stark', 'Baratheon'])
[Character(first_name='Ned', last_name='Stark'),
 Character(first_name='Catelyn', last_name='Stark'),
 Character(first_name='Robert', last_name='Baratheron')]
```

##### [](#header-5)iin

Case-insensitive lookup in a given list.

**Examples:**

```py
>>> Character.objects.filter(last_name__iin='starks')
[Character(first_name='Ned', last_name='Stark'),
 Character(first_name='Catelyn', last_name='Stark')]

>>> # Also works for non-string iterables
>>> Character.objects.filter(last_name__iin=['stark', 'baratheon'])
[Character(first_name='Ned', last_name='Stark'),
 Character(first_name='Catelyn', last_name='Stark'),
 Character(first_name='Robert', last_name='Baratheron')]
```

##### [](#header-5)gt

Greater than.

##### [](#header-5)gte

Greater than or equal to.

##### [](#header-5)lt

Less than.

##### [](#header-5)lte

Less than or equal to.

##### [](#header-5)startswith

Case-sensitive starts-with.

##### [](#header-5)istartswith

Case-insensitive starts-with.

##### [](#header-5)endsswith

Case-sensitive ends-with.

##### [](#header-5)iendswith

Case-insensitive ends-with.

##### [](#header-5)isnone

Checks if the value is equal to Python `NoneType`.