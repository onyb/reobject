# -*- coding: utf-8 -*-

import unittest

from reobject import Model


class Singleton(Model):
    def __init__(self, value=None):
        self.value = value

    def __new__(cls, *args, **kwargs):
        pool = Singleton.objects.filter()
        if pool.exists():
            return pool.get()
        else:
            return super().__new__(cls, *args, **kwargs)


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
