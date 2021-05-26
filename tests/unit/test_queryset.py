import unittest
from random import randint

from reobject.exceptions import DoesNotExist, MultipleObjectsReturned
from reobject.models import Model, Field
from reobject.query import QuerySet, EmptyQuerySet


class SomeModel(Model):
    p = Field()
    q = Field(default=lambda: randint(1, 10000))
    r = Field(default=None)


class TestQuerySet(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        SomeModel.objects.all().delete()

    def test_pipe(self):
        SomeModel(p='foo')
        SomeModel(p='bar')

        self.assertEqual(
            (
                SomeModel.objects.filter(p='foo') | SomeModel.objects.filter(p='bar')
            ).order_by('q'),
            SomeModel.objects.all().order_by('q')
        )

    def test_count(self):
        SomeModel(p='foo')
        SomeModel(p='bar')

        self.assertEqual(SomeModel.objects.filter().count(), 2)

    def test_manager_count(self):
        SomeModel(p=1, q=2, r=3)
        SomeModel(p=1, q=3, r=4)

        self.assertEqual(SomeModel.objects.count(), 2)

    def test_delete(self):
        SomeModel(p='foo')
        SomeModel(p='bar')

        _len, _type = SomeModel.objects.filter(p='bar').delete()
        self.assertFalse(SomeModel.objects.filter(p='bar').exists())
        self.assertEqual(_len, 1)
        self.assertEqual(_type, {'SomeModel': 1})

    def test_distinct(self):
        SomeModel(p='foo')
        SomeModel(p='foo')
        SomeModel(p='foo')

        self.assertEqual(SomeModel.objects.filter().distinct('p').count(), 1)
        self.assertEqual(SomeModel.objects.filter().distinct('q').count(), 3)
        self.assertEqual(SomeModel.objects.filter().distinct('p', 'q').count(), 3)
        self.assertEqual(SomeModel.objects.filter().distinct('q', 'p').count(), 3)

    def test_earliest(self):
        obj = SomeModel.objects.earliest()
        self.assertIsNone(obj)

        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=0)

        obj = SomeModel.objects.earliest()

        self.assertEqual(obj.p, 'foo')

    def test_exists(self):
        SomeModel(p='foo')

        self.assertTrue(SomeModel.objects.filter(p='foo').exists())
        self.assertFalse(SomeModel.objects.filter(p='bar').exists())

    def test_exclude(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=0)

        self.assertEqual(SomeModel.objects.filter(q__gte=1).exclude(p='foo').count(), 0)
        self.assertEqual(SomeModel.objects.filter().exclude(q__gte=0).count(), 0)

    def test_manager_exclude_some_multiple_kwargs(self):
        SomeModel(p=1, q=2, r=3)
        SomeModel(p=1, q=3, r=4)

        objs = SomeModel.objects.exclude(q=3, r=4)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].p, 1)
        self.assertEqual(objs[0].q, 2)
        self.assertEqual(objs[0].r, 3)

        self.assertEqual(SomeModel.objects.exclude(q=3, r=3).count(), 2)

    def test_manager_filter_nokwargs(self):
        SomeModel(p=1, q=2, r=3)
        SomeModel(p=1, q=3, r=4)

        self.assertEqual(len(SomeModel.objects.filter()), 2)

    def test_manager_filter_none(self):
        SomeModel(p=1, q=2, r=3)
        SomeModel(p=1, q=3, r=4)

        self.assertEqual(SomeModel.objects.filter(p=2), EmptyQuerySet(model=SomeModel))

    def test_manager_filter_some_single_kwarg(self):
        SomeModel(p=1, q=2, r=3)
        SomeModel(p=1, q=3, r=4)

        objs = SomeModel.objects.filter(q=2)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].p, 1)
        self.assertEqual(objs[0].q, 2)
        self.assertEqual(objs[0].r, 3)

    def test_manager_filter_some_multiple_kwargs(self):
        SomeModel(p=1, q=2, r=3)
        SomeModel(p=1, q=3, r=4)

        objs = SomeModel.objects.filter(q=3, r=4)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].p, 1)
        self.assertEqual(objs[0].q, 3)
        self.assertEqual(objs[0].r, 4)

        self.assertEqual(SomeModel.objects.filter(q=3, r=3), EmptyQuerySet(model=SomeModel))

    def test_queryset_get(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=0)

        self.assertEqual(SomeModel.objects.filter(q__gte=0).get(p='foo').q, 1)

    def test_manager_get_success(self):
        _id = SomeModel(p=1, q=2, r=3).id

        obj = SomeModel.objects.get(id=_id)
        self.assertEqual(obj.p, 1)
        self.assertEqual(obj.q, 2)
        self.assertEqual(obj.r, 3)

    def test_manager_get_does_not_exist(self):
        SomeModel(p=1, q=2, r=3)

        with self.assertRaises(DoesNotExist):
            SomeModel.objects.get(p=2)

    def test_manager_get_multiple_objects_returned(self):
        SomeModel(p=1, q=2, r=3)
        SomeModel(p=1, q=3, r=4)

        with self.assertRaises(MultipleObjectsReturned):
            SomeModel.objects.get(p=1)

    def test_get_or_create(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=0)

        obj, created = SomeModel.objects.filter(q__gte=0).get_or_create(p='foo')

        self.assertEqual(obj.q, 1)
        self.assertFalse(created)

        obj, created = SomeModel.objects.exclude(q__gte=0).get_or_create(p='foo', defaults={'q': 2})
        self.assertEqual(obj.q, 2)
        self.assertTrue(created)

    def test_latest(self):
        obj = SomeModel.objects.latest()
        self.assertIsNone(obj)

        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=0)

        obj = SomeModel.objects.latest()

        self.assertEqual(obj.p, 'bar')

    def test_none(self):
        self.assertFalse(SomeModel.objects.all().none().exists())

    def test_order_by(self):
        SomeModel(p='foo', q=3)
        SomeModel(p='foo', q=1)
        SomeModel(p='foo', q=2)

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
        SomeModel(p='foo', q=1)
        SomeModel(p='foo', q=2)

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
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

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
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

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

    def test_invalid_lookup_params(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        with self.assertRaises(TypeError):
            SomeModel.objects.all().values_list('p', 0)

    def test_values_list_flat(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        self.assertEqual(
            SomeModel.objects.filter().order_by('-q').values_list('p', flat=True),
            QuerySet(
                ['bar', 'foo'],
                model=SomeModel
            )
        )

        with self.assertRaises(TypeError):
            SomeModel.objects.filter().order_by('-q').values_list('p', 'q', flat=True)

    def test_first(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        obj = SomeModel.objects.all().order_by('-q').first()

        self.assertEqual(obj.q, 2)

    def test_manager_first(self):
        self.assertIsNone(SomeModel.objects.first())

        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        obj = SomeModel.objects.first()

        self.assertEqual(obj.q, 1)

    def test_first_none(self):
        self.assertIsNone(SomeModel.objects.all().first())

    def test_last(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        obj = SomeModel.objects.all().order_by('q').last()

        self.assertEqual(obj.q, 2)

    def test_manager_last(self):
        self.assertIsNone(SomeModel.objects.last())

        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        obj = SomeModel.objects.last()

        self.assertEqual(obj.q, 2)

    def test_last_none(self):
        self.assertIsNone(SomeModel.objects.all().last())

    def test_manager_random(self):
        self.assertIsNone(SomeModel.objects.random())

        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        obj = SomeModel.objects.random()

        self.assertIn(obj, SomeModel.objects.all())

    def test_manager_random_queryset(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        objs = SomeModel.objects.random_queryset()
        for obj in objs:
            self.assertIn(obj, SomeModel.objects.all())

    def test_manager_map(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        result = SomeModel.objects.map(
            func=lambda obj: obj.p.upper()
        )

        self.assertEqual(set(result), {'FOO', 'BAR'})

    def test_map(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        result = SomeModel.objects.filter().map(
            func=lambda obj: obj.p.upper()
        )

        self.assertEqual(set(result), {'FOO', 'BAR'})

    def test_manager_map_non_callable(self):
        SomeModel(p='foo', q=1)
        SomeModel(p='bar', q=2)

        with self.assertRaises(TypeError):
            result = SomeModel.objects.map(func=1)
