# -*- coding: utf-8 -*-

import unittest

from reobject.models import Model, Field


class Singleton(Model):
    value = Field(default=None)

    def __new__(cls, *args, **kwargs):
        if cls.objects.count() == 0:
            return super().__new__(cls)
        else:
            return cls.objects.get()


class TestSingleton(unittest.TestCase):
    def setUp(self):
        Singleton()
        Singleton(value='foo')

    def test_count(self):
        self.assertEqual(Singleton.objects.count(), 1)

    def test_instance(self):
        obj = Singleton('bar')
        self.assertIs(Singleton.objects.get(), obj)
        self.assertEqual(Singleton.objects.get().value, 'bar')


if __name__ == '__main__':
    unittest.main()
