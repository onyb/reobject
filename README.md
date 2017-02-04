# ReObject


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
