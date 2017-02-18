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

    def test_pipe(self):
        SomeModel.objects.create(p='foo')
        SomeModel.objects.create(p='bar')

        self.assertEqual(
            (
                SomeModel.objects.filter(p='foo') | SomeModel.objects.filter(p='bar')
            ).order_by('q'),
            SomeModel.objects.all().order_by('q')
        )

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

    def test_filter(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=0)

        self.assertEqual(SomeModel.objects.filter(q__gte=1).filter(p='foo').count(), 1)
        self.assertEqual(SomeModel.objects.filter().filter(q__gte=0).count(), 2)


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

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values_list('q'),
            QuerySet([
                (3,),
                (2,),
                (1,)
            ])
        )

        with self.assertRaises(AttributeError):
            SomeModel.objects.filter().order_by()

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
        SomeModel.objects.create(p='bar', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values('q'),
            QuerySet([
                {'q': 2},
                {'q': 1},
            ])
        )

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values('p', 'q'),
            QuerySet([
                {'q': 2, 'p': 'bar'},
                {'q': 1, 'p': 'foo'},
            ])
        )

        self.assertSetEqual(
            set(SomeModel.objects.filter().order_by('-q').values()[0].keys()),
            {'p', 'q', 'created', 'updated', 'id'}
        )

    def test_values_list(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values_list('p', 'q'),
            QuerySet([
                ('bar', 2,),
                ('foo', 1,)
            ])
        )

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values_list('q', 'p'),
            QuerySet([
                (2, 'bar',),
                (1, 'foo',)
            ])
        )

    def test_values_list_flat(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values_list('p', flat=True),
            QuerySet(['bar', 'foo'])
        )

        with self.assertRaises(TypeError):
            SomeModel.objects.filter().order_by('-q').values_list('p', 'q', flat=True)
