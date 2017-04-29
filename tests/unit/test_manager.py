import unittest
from datetime import datetime

from reobject.model import Model


class SomeModel(Model):
    def __init__(self, p, q, r):
        self.p = p
        self.q = q
        self.r = r


class TestQuery(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        SomeModel.objects._clear()

    def test_descriptor_cls(self):
        try:
            SomeModel.objects
            SomeModel.objects.filter
        except AttributeError:
            self.assertFalse(True)
        else:
            pass  # AttributeError was not raised

    def test_descriptor_instance(self):
        obj = SomeModel(1, 2, 3)
        with self.assertRaises(AttributeError):
            obj.objects
            obj.objects.foo

    def test_create(self):
        obj = SomeModel(p=1, q=2, r=1)

        self.assertEqual(obj.p, 1)
        self.assertEqual(obj.q, 2)
        self.assertEqual(obj.r, 1)
        self.assertEqual(obj.id, id(obj))
        self.assertLess(obj.created, datetime.utcnow())
        self.assertEqual(obj.created, obj.updated)

    def test_none(self):
        self.assertFalse(SomeModel.objects.none())

    def test_all(self):
        SomeModel(p=0, q=0, r=1)
        SomeModel(p=0, q=1, r=0)
        SomeModel(p=1, q=0, r=0)

        self.assertEqual(len(SomeModel.objects.all()), 3)

    def test_manager_model(self):
        self.assertEqual(SomeModel.objects.model, SomeModel)
