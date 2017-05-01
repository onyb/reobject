# reobject

[![Build Status](https://travis-ci.org/onyb/reobject.svg?branch=master)](https://travis-ci.org/onyb/reobject)
[![PyPI version](https://badge.fury.io/py/reobject.svg)](https://badge.fury.io/py/reobject)
[![PyPI](https://img.shields.io/pypi/pyversions/reobject.svg)](https://pypi.python.org/pypi/reobject)
[![codecov](https://codecov.io/gh/onyb/reobject/branch/master/graph/badge.svg)](https://codecov.io/gh/onyb/reobject)

*reobject* is an ORM layer for your objects. Add a mixin to your Python classes and assume the ability to track and query objects at runtime!

**Warning:** This is an alpha software, and the API is subject to change.

### Installation

```sh
pip install reobject
```

### Example usage

Inherit from the `Model` class.
```py3
from reobject.model import Model

class Book(Model):
    def __init__(self, title, authors, price):
        self.title, self.authors, self.price = title, authors, price
```

Create a bunch of objects:
```py3
>>> Book(title='The C Programming Language', authors=['Kernighan', 'Ritchie'], price=52)
>>> Book(title='The Go Programming Language', authors=['Donovan', 'Kernighan'], price=30)
>>> Book(title='The AWK Programming Language', authors=['Aho', 'Kernighan'], price=127)
```
Get all books
```py3
>>> Book.objects.all()
[<Book: 140707840041088>, <Book: 140707840125584>, <Book: 140707840083056>]
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

### Why?

Reasons why you should consider using reobject:

* You are refactoring a codebase with years of accumulated code-vomit.
* Your code looks like a Christmas tree.
* You want to implement design patterns without all that boilerplate.
* You care about maintainability, and cleanliness.

### Contributing

Want to help? Please review the [contributing guidelines](CONTRIBUTING.md), and take a look at some [good first bugs](https://github.com/onyb/reobject/issues?q=is%3Aissue+is%3Aopen+label%3Abitesize)!
