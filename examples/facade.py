# -*- coding: utf-8 -*-

import time
import unittest

from reobject.models import Model, Field


# Complex Parts
class A(Model):
    def run(self):
        time.sleep(0.1)
        return 3


class B(Model):
    def run(self):
        time.sleep(0.5)
        return 4


class Facade(Model):
    def __new__(cls, *args, **kwargs):
        if Facade.objects.count():
            return Facade.objects.get()
        else:
            return super().__new__(cls, *args, **kwargs)

    def run_all(self):
        qs = A.objects.all() | B.objects.all()
        return [i for i in qs.map(lambda x: x.run())]  # QuerySet.map is lazy


class TestFacade(unittest.TestCase):
    def setUp(self):
        Facade()
        A() and B() and A()

    def test_facade(self):
        response = Facade().run_all()
        self.assertEqual(sum(response), 10)  # 3 + 4 + 3


if __name__ == '__main__':
    unittest.main()
