from datetime import datetime
import unittest

from reobject.model import Model
from reobject.exceptions import DoesNotExist, MultipleObjectsReturned
from reobject.query import EmptyQuerySet

class TestModel(Model):
    def __init__(self, p, q, r):
        self.p = p
        self.q = q
        self.r = r

class TestQuery(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        TestModel.objects._clear()

    def test_descriptor_cls(self):
        try:
            TestModel.objects
            TestModel.objects.create
        except AttributeError:
            self.assertFalse(True)
        else:
            pass  # AttributeError was not raised

    def test_descriptor_instance(self):
        obj = TestModel(1, 2, 3)
        with self.assertRaises(AttributeError):
            obj.objects
            obj.objects.foo

    def test_create(self):
        obj = TestModel.objects.create(p=1, q=2, r=1)

        self.assertEqual(obj.p, 1)
        self.assertEqual(obj.q, 2)
        self.assertEqual(obj.r, 1)
        self.assertEqual(obj.id, id(obj))
        self.assertLess(obj.created, datetime.utcnow())
        self.assertEqual(obj.created, obj.updated)

    def test_none(self):
        self.assertFalse(TestModel.objects.none())

    def test_all(self):
        TestModel.objects.create(p=0, q=0, r=1)
        TestModel.objects.create(p=0, q=1, r=0)
        TestModel.objects.create(p=1, q=0, r=0)

        self.assertEqual(len(TestModel.objects.all()), 3)

    def test_manager_model(self):
        self.assertEqual(TestModel.objects.model, TestModel)

    def test_get_success(self):
        _id = TestModel.objects.create(p=1, q=2, r=3).id

        obj = TestModel.objects.get(id=_id)
        self.assertEqual(obj.p, 1)
        self.assertEqual(obj.q, 2)
        self.assertEqual(obj.r, 3)

    def test_get_does_not_exist(self):
        TestModel.objects.create(p=1, q=2, r=3)

        with self.assertRaises(DoesNotExist):
            TestModel.objects.get(p=2)

    def test_get_multiple_objects_returned(self):
        TestModel.objects.create(p=1, q=2, r=3)
        TestModel.objects.create(p=1, q=3, r=4)

        with self.assertRaises(MultipleObjectsReturned):
            TestModel.objects.get(p=1)

    def test_filter_nokwargs(self):
        TestModel.objects.create(p=1, q=2, r=3)
        TestModel.objects.create(p=1, q=3, r=4)

        self.assertEqual(len(TestModel.objects.filter()), 2)

    def test_filter_none(self):
        TestModel.objects.create(p=1, q=2, r=3)
        TestModel.objects.create(p=1, q=3, r=4)

        self.assertEqual(TestModel.objects.filter(p=2), EmptyQuerySet())

    def test_filter_some_single_kwarg(self):
        TestModel.objects.create(p=1, q=2, r=3)
        TestModel.objects.create(p=1, q=3, r=4)

        objs = TestModel.objects.filter(q=2)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].p, 1)
        self.assertEqual(objs[0].q, 2)
        self.assertEqual(objs[0].r, 3)

    def test_filter_some_multiple_kwargs(self):
        TestModel.objects.create(p=1, q=2, r=3)
        TestModel.objects.create(p=1, q=3, r=4)

        objs = TestModel.objects.filter(q=3, r=4)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].p, 1)
        self.assertEqual(objs[0].q, 3)
        self.assertEqual(objs[0].r, 4)

        self.assertEqual(TestModel.objects.filter(q=3, r=3), EmptyQuerySet())
