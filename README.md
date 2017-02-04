# ReObject

[![Build Status](https://travis-ci.org/onyb/reobject.svg?branch=master)](https://travis-ci.org/onyb/reobject) [![codecov](https://codecov.io/gh/onyb/reobject/branch/master/graph/badge.svg)](https://codecov.io/gh/onyb/reobject)

If your Python code is starting to look like a Christmas tree (damn you indents!), and you care about testability, ReObject can help you! It provides a mixin which your classes can inherit and assume the ability to track and query its objects at runtime!

Code written using ReObject, is significantly easier to maintain and reason about. It encourages you to encapsulate related logic in classes, just like database models. To get a quick introduction to the library, read the Examples section.

**Warning:** This is an alpha software, and the API is subject to change without notice.

### Examples

```py3
from reobject.model import Model

class Book(Model):
    def __init__(self, title, authors, price):
        self.title = title
        self.authors = author
        self.price = price

In : Book.objects.create(
...:     title='The C Programming Language', authors=['Kernighan', 'Ritchie'], price=52.89
...: )

In : Book.objects.create(
...:     title='The Go Programming Language', authors=['Donovan', 'Kernighan'], price=30.83
...: )

In : Book.objects.create(
...:     title='The AWK Programming Language', authors=['Aho', 'Kernighan'], price=127.17
...: )

# Get all books
In : Book.objects.all()
Out: [<Book: 140707840041088>, <Book: 140707840125584>, <Book: 140707840083056>]

# Get the K&R book
In : Book.objects.get(title='The C Programming Language')
Out: <Book: 140707840083056>

# Get the titles of all books which cost less than 100 USD, sorted by price.
In : Book.objects.filter(price__lte=100).order_by('price').values('title')
Out: [{'title': 'The Go Programming Language'}, {'title': 'The C Programming Language'}]

# Get titles of all books co-authored by Brian Kernighan
In : Book.objects.filter(authors__contains='Kernighan').values_list('title', flat=True)
Out: ['The Go Programming Language', 'The C Programming Language', 'The AWK Programming Language']
```

### Contributing

Want to help? Please review the [contributing guidelines](CONTRIBUTING.md), and take a look at some [good first bugs](https://github.com/onyb/reobject/issues?q=is%3Aissue+is%3Aopen+label%3Abitesize)!
