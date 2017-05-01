#!/bin/bash

pandoc --from=markdown --to=rst --output=README.rst README.md
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
