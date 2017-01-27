from random import randint
import unittest

from reobject.model import Model
from reobject.query import QuerySet


class SomeModel(Model):
    def __init__(self, p, q=None):
        self.p = p
        self.q = q or randint(1, 10000)


class TestQuerySet(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        SomeModel.objects._clear()

    def test_count(self):
        SomeModel.objects.create(p='foo')
        SomeModel.objects.create(p='bar')

        self.assertEqual(SomeModel.objects.filter().count(), 2)

    def test_delete(self):
        SomeModel.objects.create(p='foo')
        SomeModel.objects.create(p='bar')

        SomeModel.objects.filter(p='bar').delete()
        self.assertFalse(SomeModel.objects.filter(p='bar').exists())

    def test_distinct(self):
        SomeModel.objects.create(p='foo')
        SomeModel.objects.create(p='foo')
        SomeModel.objects.create(p='foo')

        self.assertEqual(SomeModel.objects.filter().distinct('p').count(), 1)
        self.assertEqual(SomeModel.objects.filter().distinct('q').count(), 3)
        self.assertEqual(SomeModel.objects.filter().distinct('p', 'q').count(), 3)
        self.assertEqual(SomeModel.objects.filter().distinct('q', 'p').count(), 3)

    def test_exists(self):
        SomeModel.objects.create(p='foo')

        self.assertTrue(SomeModel.objects.filter(p='foo').exists())
        self.assertFalse(SomeModel.objects.filter(p='bar').exists())

    def test_none(self):
        self.assertFalse(SomeModel.objects.none().exists())

    def test_order_by(self):
        SomeModel.objects.create(p='foo', q=3)
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='foo', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('q').values_list('q'),
            QuerySet([
                (1,),
                (2,),
                (3,)
            ])
        )

    def test_order_by_reverse(self):
        SomeModel.objects.create(p='foo', q=3)
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='foo', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values_list('q'),
            QuerySet([
                (3,),
                (2,),
                (1,)
            ])
        )

    def test_reverse(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='foo', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('q').reverse().values_list('q'),
            QuerySet([
                (2,),
                (1,)
            ])
        )

        self.assertEqual(
            SomeModel.objects.filter().order_by('q').reverse().reverse()
                .values_list('q'),
            QuerySet([
                (1,),
                (2,)
            ])
        )

    def test_values(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='foo', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values('q'),
            QuerySet([
                {'q': 2},
                {'q': 1},
            ])
        )