# ReObject

[![Build Status](https://travis-ci.org/onyb/reobject.svg?branch=master)](https://travis-ci.org/onyb/reobject) [![codecov](https://codecov.io/gh/onyb/reobject/branch/master/graph/badge.svg)](https://codecov.io/gh/onyb/reobject)

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

### FAQ
- **What?**

  reobject provides a mixin which your classes can inherit to give their objects the ability to be tracked, and queried at runtime!
  
- **Why?**

  If your Python code is starting to look like a Christmas tree, and you care about easy testability: reobject can help you!

  With reobject, you can, in most cases, condense your code into a one-liner which will be easy to maintain and reason about. It encourages you to encapsulate related logic in classes, just like database models. To know what you can do with reobject, head over to the Examples section.
  
- **Is it a clone of Django ORM?**

  Not really. The interface, query syntax, and philosophy is inspired by Django ORM, but it also implements additional features which Django ORM could not due to limitations imposed by relational databases. From an implementation point of view, there is little or no similarity.
  
- **What about performance?**

  To do
  
- **Can I use it in production?**

  At your own risk. This is an alpha software, and the API is subject to changes without notice.


### Contributing

#### How to contribute

- Check the `bitesize` tag for beginner-level issues.
- Add API documentation.
- Increase test coverage.
- Propose and/or implement enhancements.

#### Pull Requests
I would like to have a 100% acceptance rate for pull requests. Here is what you can do to help me achieve that:

- Write short and meaningful commit messages. Try to include the GitHub issue ID if it exists.
  Example: `[GH-7] Add support for imaginary feature` 
- Keep PEP8 fixes (if any) in a separate commit.
- Make sure your patches include a proof of fix, aka unit tests.
- Add or update relevant documentation.

#### Bugs
If you are reporting a bug, please remember to:

- Add examples for current behavior and expected behavior.
- Include steps to reliably reproduce the bug.
- Include your Python version: `python --version` 
