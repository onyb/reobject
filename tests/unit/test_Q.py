from random import randint
import unittest

from reobject.model import Model
from reobject.query import Q


class Secret(object):
    def __init__(self, gem):
        self.gem = gem or 'ruby'


class SomeModel(Model):
    def __init__(self, question='', secret=None):
        self.question = question
        self.secret = Secret(secret)


class TestQ(unittest.TestCase):
    def tearDown(self):
        SomeModel.objects._clear()

    def test_simple(self):
        q_obj = Q(question='What?')

        obj = SomeModel.objects.create(question='What?')
        self.assertTrue(q_obj.comparator(obj))

        obj = SomeModel.objects.create(question='When?')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_attrs(self):
        q_obj = Q(secret__gem='ruby')
        obj = SomeModel.objects.create()
        self.assertTrue(q_obj.comparator(obj))

    def test_nested_contains(self):
        q_obj = Q(secret__gem__contains='ub')
        obj = SomeModel.objects.create()
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__contains='rby')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_endswith(self):
        q_obj = Q(secret__gem__endswith='uby')
        obj = SomeModel.objects.create()
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__endswith='rb')
        self.assertFalse(q_obj.comparator(obj))

    def test_exact(self):
        q_obj = Q(secret__gem__exact='ruby')
        obj = SomeModel.objects.create()
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__exact='Ruby')
        self.assertFalse(q_obj.comparator(obj))

    def test_iexact(self):
        q_obj = Q(secret__gem__iexact='Ruby')
        obj = SomeModel.objects.create()
        self.assertTrue(q_obj.comparator(obj))

        obj = SomeModel.objects.create(secret='BUẞE')
        q_obj = Q(secret__gem__iexact='busse')
        self.assertTrue(q_obj.comparator(obj))

    def test_nested_gt(self):
        obj = SomeModel.objects.create(secret=7)

        q_obj = Q(secret__gem__gt=6)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__gt=8)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_gte(self):
        obj = SomeModel.objects.create(secret=7)

        q_obj = Q(secret__gem__gte=6)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__gte=7)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__gte=8)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_in(self):
        obj = SomeModel.objects.create(secret=7)

        q_obj = Q(secret__gem__in=[1, 2, 3, 4, 5, 6, 7])
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__in=[1, 2, 3])
        self.assertFalse(q_obj.comparator(obj))

    def test_isnull(self):
        obj = SomeModel.objects.create(question=None)

        q_obj = Q(question__isnull=True)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__isnull=True)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_lt(self):
        obj = SomeModel.objects.create(secret=7)

        q_obj = Q(secret__gem__lt=8)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__lt=6)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_lte(self):
        obj = SomeModel.objects.create(secret=7)

        q_obj = Q(secret__gem__lte=8)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__lte=7)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__lte=6)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_startswith(self):
        q_obj = Q(secret__gem__startswith='rub')
        obj = SomeModel.objects.create()
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__startswith='rb')
        self.assertFalse(q_obj.comparator(obj))