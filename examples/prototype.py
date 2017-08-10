# -*- coding: utf-8 -*-

import unittest
from copy import deepcopy

from reobject.models import Model


class Prototype(Model):
    value = 'default'

    def clone(self, **attrs):
        obj = deepcopy(self)
        obj.__dict__.update(attrs)
        return obj


class TestPrototype(unittest.TestCase):
    def setUp(self):
        self.prototype = Prototype()
        self.prototype.clone()
        self.prototype.clone(value='a-value', category='a')
        self.prototype.clone(value='b-value', is_checked=True)

    def test_dispatcher(self):
        self.assertEqual(Prototype.objects.count(), 4)

        self.assertSetEqual(
            set(Prototype.objects.all().values_list('value', flat=True)),
            {'a-value', 'default', 'b-value'}
        )


if __name__ == '__main__':
    unittest.main()
