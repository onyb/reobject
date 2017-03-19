import unittest
from random import randint

from reobject.exceptions import DoesNotExist, MultipleObjectsReturned
from reobject.model import Model
from reobject.query import QuerySet, EmptyQuerySet


class SomeModel(Model):
    def __init__(self, p, q=None, r=None):
        self.p = p
        self.q = q or randint(1, 10000)
        self.r = r


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

    def test_manager_count(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        self.assertEqual(SomeModel.objects.count(), 2)

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

    def test_earliest(self):
        obj = SomeModel.objects.earliest()
        self.assertEqual(obj, None)

        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=0)

        obj = SomeModel.objects.earliest()

        self.assertEqual(obj.p, 'foo')

    def test_exists(self):
        SomeModel.objects.create(p='foo')

        self.assertTrue(SomeModel.objects.filter(p='foo').exists())
        self.assertFalse(SomeModel.objects.filter(p='bar').exists())

    def test_exclude(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=0)

        self.assertEqual(SomeModel.objects.filter(q__gte=1).exclude(p='foo').count(), 1)
        self.assertEqual(SomeModel.objects.filter().exclude(q__gte=0).count(), 0)

    def test_manager_exclude_some_multiple_kwargs(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        objs = SomeModel.objects.exclude(q=3, r=4)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].p, 1)
        self.assertEqual(objs[0].q, 2)
        self.assertEqual(objs[0].r, 3)

        self.assertEqual(SomeModel.objects.exclude(q=3, r=3).count(), 2)

    def test_manager_filter_nokwargs(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        self.assertEqual(len(SomeModel.objects.filter()), 2)

    def test__manager_filter_none(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        self.assertEqual(SomeModel.objects.filter(p=2), EmptyQuerySet(model=SomeModel))

    def test_manager_filter_some_single_kwarg(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        objs = SomeModel.objects.filter(q=2)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].p, 1)
        self.assertEqual(objs[0].q, 2)
        self.assertEqual(objs[0].r, 3)

    def test_manager_filter_some_multiple_kwargs(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        objs = SomeModel.objects.filter(q=3, r=4)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].p, 1)
        self.assertEqual(objs[0].q, 3)
        self.assertEqual(objs[0].r, 4)

        self.assertEqual(SomeModel.objects.filter(q=3, r=3), EmptyQuerySet(model=SomeModel))

    def test_queryset_get(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=0)

        self.assertEqual(SomeModel.objects.filter(q__gte=0).get(p='foo').q, 1)

    def test_manager_get_success(self):
        _id = SomeModel.objects.create(p=1, q=2, r=3).id

        obj = SomeModel.objects.get(id=_id)
        self.assertEqual(obj.p, 1)
        self.assertEqual(obj.q, 2)
        self.assertEqual(obj.r, 3)

    def test_manager_get_does_not_exist(self):
        SomeModel.objects.create(p=1, q=2, r=3)

        with self.assertRaises(DoesNotExist):
            SomeModel.objects.get(p=2)

    def test_manager_get_multiple_objects_returned(self):
        SomeModel.objects.create(p=1, q=2, r=3)
        SomeModel.objects.create(p=1, q=3, r=4)

        with self.assertRaises(MultipleObjectsReturned):
            SomeModel.objects.get(p=1)

    def test_get_or_create(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=0)

        obj, created = SomeModel.objects.filter(q__gte=0).get_or_create(p='foo')

        self.assertEqual(obj.q, 1)
        self.assertFalse(created)

        obj, created = SomeModel.objects.exclude(q__gte=0).get_or_create(p='foo', defaults={'q': 2})
        self.assertEqual(obj.q, 2)
        self.assertTrue(created)

    def test_latest(self):
        obj = SomeModel.objects.latest()
        self.assertEqual(obj, None)

        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=0)

        obj = SomeModel.objects.latest()

        self.assertEqual(obj.p, 'bar')

    def test_none(self):
        self.assertFalse(SomeModel.objects.none().exists())

    def test_order_by(self):
        SomeModel.objects.create(p='foo', q=3)
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='foo', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('q').values_list('q'),
            QuerySet(
                [(1,), (2,), (3,)],
                model=SomeModel
            )
        )

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values_list('q'),
            QuerySet(
                [(3,), (2,), (1,)],
                model=SomeModel
            )
        )

        with self.assertRaises(AttributeError):
            SomeModel.objects.filter().order_by()

    def test_reverse(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='foo', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('q').reverse().values_list('q'),
            QuerySet(
                [(2,), (1,)],
                model=SomeModel
            )
        )

        self.assertEqual(
            SomeModel.objects.filter().order_by('q').reverse().reverse()
                .values_list('q'),
            QuerySet(
                [(1,), (2,)],
                model=SomeModel
            )
        )

    def test_values(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values('q'),
            QuerySet(
                [{'q': 2}, {'q': 1}, ],
                model=SomeModel
            )
        )

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values('p', 'q'),
            QuerySet(
                [
                    {'q': 2, 'p': 'bar'},
                    {'q': 1, 'p': 'foo'},
                ],
                model=SomeModel
            )
        )

        self.assertSetEqual(
            set(SomeModel.objects.filter().order_by('-q').values()[0].keys()),
            {'p', 'q', 'r', 'created', 'updated', 'id'}
        )

    def test_values_list(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values_list('p', 'q'),
            QuerySet(
                [
                    ('bar', 2,),
                    ('foo', 1,)
                ],
                model=SomeModel
            )
        )

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values_list('q', 'p'),
            QuerySet(
                [
                    (2, 'bar',),
                    (1, 'foo',)
                ],
                model=SomeModel
            )
        )

    def test_values_list_flat(self):
        SomeModel.objects.create(p='foo', q=1)
        SomeModel.objects.create(p='bar', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values_list('p', flat=True),
            QuerySet(
                ['bar', 'foo'],
                model=SomeModel
            )
        )

        with self.assertRaises(TypeError):
            SomeModel.objects.filter().order_by('-q').values_list('p', 'q', flat=True)
