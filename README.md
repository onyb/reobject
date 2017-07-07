# reobject

[![Build Status](https://travis-ci.org/onyb/reobject.svg?branch=master)](https://travis-ci.org/onyb/reobject)
[![PyPI version](https://badge.fury.io/py/reobject.svg)](https://badge.fury.io/py/reobject)
[![PyPI](https://img.shields.io/pypi/pyversions/reobject.svg)](https://pypi.python.org/pypi/reobject)
[![codecov](https://codecov.io/gh/onyb/reobject/branch/master/graph/badge.svg)](https://codecov.io/gh/onyb/reobject)

*reobject* is an ORM layer for your objects. Simple, add a mixin to your Python class and assume the ability to track and query objects at runtime!

**Warning:** This is an alpha software, and the API is subject to change.

### Installation

```sh
pip install reobject
```

### Example usage

```py3
from reobject.model import Model

class Book(Model):
    def __init__(self, title, authors, price):
        self.title, self.authors, self.price = title, authors, price

>>> # Create a bunch of objects:
>>> Book(title='The C Programming Language', authors=['Kernighan', 'Ritchie'], price=52)
>>> Book(title='The Go Programming Language', authors=['Donovan', 'Kernighan'], price=30)

>>> # Get all books
>>> Book.objects.all()
[<Book: 140707840041088>, <Book: 140707840125584>]

>>> # Get the titles of all books which cost less than 50 USD:
>>> Book.objects.filter(price__lt=50).values('title')
[{'title': 'The Go Programming Language'}, {'title': 'The C Programming Language'}]

>>> # Get titles of all books co-authored by Brian Kernighan:
>>> Book.objects.filter(authors__contains='Kernighan').values_list('title', flat=True)
['The Go Programming Language', 'The C Programming Language']
```

### Features

* Elegant data-model syntax inspired by Django ORM.
* Plug and play: works without refactoring your existing codebase.
* Chainable operations on querysets.
* Transactions.
* [TBA] Attribute indexes for fast lookups.
* [TBA] Many-to-one class relationships.

### Crunching Design Patterns

|  Pattern      |                        Description                       | Pure Python | reobject |
|:-------------:|:--------------------------------------------------------:|:--------:|:-----------:|
| Flyweight     | Reuse existing instances of objects with identical state | [Link](https://github.com/faif/python-patterns/blob/master/structural/flyweight.py) | [Link](examples/flyweight.py) |
| Memento       | Transactional rollback of an object to a previous state in case of an exception | [Link](https://github.com/faif/python-patterns/blob/master/behavioral/memento.py) | [Link](tests/unit/test_transaction.py) |
| Prototype     | Create clones of a prototype without instantiation       | [Link](https://github.com/faif/python-patterns/blob/master/creational/prototype.py) | [Link](examples/prototype.py) |
| Singleton     | Restrict a class to provide only a single instance       | [Link](http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html) | [Link](examples/singleton.py) |
| Facade        | Encapsulate a complex subsystem within a single interface object | [Link](https://github.com/faif/python-patterns/blob/master/structural/facade.py) | [Link](examples/facade.py) |
| Flux          | Event-driven state management inspired by Facebook Flux  | [Link](https://github.com/onyb/python-flux/blob/master/flux/store.py) | [Link](examples/flux.py) |

<sub><b>Note:</b> The idea is not to provide accurate implementations of various patterns, but to demonstrate what <i>reobject</i> is capable of. Pull requests are most welcome.</sub>

### Why?

* You are refactoring a codebase with years of accumulated code-vomit.
* Your code looks like a Christmas tree.
* You want to implement design patterns without the boilerplate.
* You care about maintainability, and cleanliness.


### Contributing

Want to help? Please review the [contributing guidelines](CONTRIBUTING.md), and take a look at some [good first bugs](https://github.com/onyb/reobject/issues?q=is%3Aissue+is%3Aopen+label%3Abitesize)!
