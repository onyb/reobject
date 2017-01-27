import unittest
from datetime import datetime

from reobject.exceptions import DoesNotExist, MultipleObjectsReturned
from reobject.model import Model
from reobject.query import EmptyQuerySet


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
            SomeModel.objects.create
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
        obj = SomeModel.objects.create(p=1, q=2, r=1)

        self.assertEqual(obj.p, 1)
        self.assertEqual(obj.q, 2)
        self.assertEqual(obj.r, 1)
        self.assertEqual(obj.id, id(obj))
        self.assertLess(obj.created, datetime.utcnow())
        self.assertEqual(obj.created, obj.updated)

    def test_none(self):
        self.assertFalse(SomeModel.objects.none())

    def test_all(self):
        SomeModel.objects.create(p=0, q=0, r=1)
        SomeModel.objects.create(p=0, q=1, r=0)
        SomeModel.objects.create(p=1, q=0, r=0)

        self.assertEqual(len(SomeModel.objects.all()), 3)

    def test_manager_model(self):
        self.assertEqual(SomeModel.objects.model, SomeModel)

    def test_get_success(self):
        _id = SomeModel.objects.create(p=1, q=2, r=3).id

        obj = SomeModel.objects.get(id=_id)
        self.assertEqual(obj.p, 1)
        self.assertEqual(obj.q, 2)
        self.assertEqual(obj.r, 3)

    def test_get_does_not_exist(self):
        SomeModel.objects.create(p=1, q=2, r=3)

        with self.assertRaises(DoesNotExist):
            SomeModel.objects.get(p=2)

    def test_get_multiple_objects_returned(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        with self.assertRaises(MultipleObjectsReturned):
            SomeModel.objects.get(p=1)

    def test_filter_nokwargs(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        self.assertEqual(len(SomeModel.objects.filter()), 2)

    def test_filter_none(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        self.assertEqual(SomeModel.objects.filter(p=2), EmptyQuerySet())

    def test_filter_some_single_kwarg(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        objs = SomeModel.objects.filter(q=2)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].p, 1)
        self.assertEqual(objs[0].q, 2)
        self.assertEqual(objs[0].r, 3)

    def test_filter_some_multiple_kwargs(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        objs = SomeModel.objects.filter(q=3, r=4)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].p, 1)
        self.assertEqual(objs[0].q, 3)
        self.assertEqual(objs[0].r, 4)

        self.assertEqual(SomeModel.objects.filter(q=3, r=3), EmptyQuerySet())
