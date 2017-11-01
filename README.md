# reobject

[![Build Status](https://travis-ci.org/onyb/reobject.svg?branch=master)](https://travis-ci.org/onyb/reobject)
[![PyPI version](https://badge.fury.io/py/reobject.svg)](https://badge.fury.io/py/reobject)
[![PyPI](https://img.shields.io/pypi/pyversions/reobject.svg)](https://pypi.python.org/pypi/reobject)
[![codecov](https://codecov.io/gh/onyb/reobject/branch/master/graph/badge.svg)](https://codecov.io/gh/onyb/reobject)

*reobject* is an ORM layer for your objects. Track and query objects at runtime
using a familiar query langauge inspired by Django ORM


**This is a highly experimental code.**

### Installation

```sh
pip install reobject
```

### Example usage

```py3
from reobject.models import Model, Field

class Book(Model):
    title = Field()
    authors = Field()
    price = Field()

>>> # Create a bunch of objects
>>> Book(title='The C Programming Language', authors=['Kernighan', 'Ritchie'], price=52)
>>> Book(title='The Go Programming Language', authors=['Donovan', 'Kernighan'], price=30)

>>> Book.objects.all()  # All books
[Book(title='The C Programming Language', authors=['Kernighan', 'Ritchie'], price=52),
 Book(title='The Go Programming Language', authors=['Donovan', 'Kernighan'], price=30)]

>>> Book.objects.filter(price__lt=50).values('title')  # Titles of books priced under $50
[{'title': 'The Go Programming Language'}, {'title': 'The C Programming Language'}]

>>> # Titles of books co-authored by Brian Kernighan
>>> Book.objects.filter(authors__contains='Kernighan').values_list('title', flat=True)
['The Go Programming Language', 'The C Programming Language']
```

### Features

* Elegant data-model syntax inspired by Django ORM.
* Class-level model fields, out of the box object protocols, pretty reprs; powered by [attrs](http://attrs.org).
* Advanced query language and chainable querysets. Read the [QuerySet API docs](https://onyb.github.io/reobject/querysets).
* Transactions. See [example](tests/unit/test_transaction.py#L7-L13).
* Many-to-one model relationships. See [example](tests/unit/test_manager.py#L61-L108)
* [TBA] Attribute indexes for fast lookups.

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

* Your boss asked you to refactor a codebase with years of accumulated code-vomit.
* Your code is starting to look like a Christmas tree.
* You want to implement/invent design patterns without the boilerplate.

### Contributing

Want to help? You can contribute to the project by:

* Using reobject in your projects, finding bugs, and proposing new features.
* Sending pull requests with recipes cooked using reobject.
* Trying your hand at some [good first bugs](https://github.com/onyb/reobject/issues?q=is%3Aissue+is%3Aopen+label%3Abitesize).
* Improving test coverage, and writing documentation.

<sub>I even added some [Contributing guidelines](CONTRIBUTING.md) to make GitHub happy.</sub>
