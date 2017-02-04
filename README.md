# ReObject

[![Build Status](https://travis-ci.org/onyb/reobject.svg?branch=master)](https://travis-ci.org/onyb/reobject) [![codecov](https://codecov.io/gh/onyb/reobject/branch/master/graph/badge.svg)](https://codecov.io/gh/onyb/reobject)

If your Python code is starting to look like a Christmas tree (damn you indents!), and you care about testability, ReObject can help you! It provides a mixin which your classes can inherit and assume the ability to track and query its objects at runtime!

Code written using ReObject, is significantly easier to maintain and reason about. It encourages you to encapsulate related logic in classes, just like database models. To get a quick introduction to the library, read the Example section below.

**Warning:** This is an alpha software, and the API is subject to change without notice.

### Example

Inherit from the `Model` class.
```py3
from reobject.model import Model

class Book(Model):
    def __init__(self, title, authors, price):
        self.title = title
        self.authors = author
        self.price = price
```

Create a bunch of objects, but instead of `Book(...)` use the `Book.objects.create(...)` syntax.
```py3
>>> Book.objects.create(title='The C Programming Language', authors=['Kernighan', 'Ritchie'], price=52)
>>> Book.objects.create(title='The Go Programming Language', authors=['Donovan', 'Kernighan'], price=30)
>>> Book.objects.create(title='The AWK Programming Language', authors=['Aho', 'Kernighan'], price=127)
```
Get all books
```py3
>>> Book.objects.all()
[<Book: 140707840041088>, <Book: 140707840125584>, <Book: 140707840083056>]
```

Get the K&R book
```py3
>>> Book.objects.get(title='The C Programming Language')
<Book: 140707840083056>
```

Get the titles of all books which cost less than 100 USD, sorted by price.
```py3
>>> Book.objects.filter(price__lte=100).order_by('price').values('title')
[{'title': 'The Go Programming Language'}, {'title': 'The C Programming Language'}]
```
Get titles of all books co-authored by Brian Kernighan
```py3
>>> Book.objects.filter(authors__contains='Kernighan').values_list('title', flat=True)
['The Go Programming Language', 'The C Programming Language', 'The AWK Programming Language']
```

### Contributing

Want to help? Please review the [contributing guidelines](CONTRIBUTING.md), and take a look at some [good first bugs](https://github.com/onyb/reobject/issues?q=is%3Aissue+is%3Aopen+label%3Abitesize)!
