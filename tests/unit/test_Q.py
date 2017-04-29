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

        obj = SomeModel(question='What?')
        self.assertTrue(q_obj.comparator(obj))

        obj = SomeModel(question='When?')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_attrs(self):
        q_obj = Q(secret__gem='ruby')
        obj = SomeModel()
        self.assertTrue(q_obj.comparator(obj))

    def test_nested_contains(self):
        q_obj = Q(secret__gem__contains='ub')
        obj = SomeModel()
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__contains='rby')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_endswith(self):
        q_obj = Q(secret__gem__endswith='uby')
        obj = SomeModel()
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__endswith='rb')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_iendswith(self):
        q_obj = Q(secret__gem__iendswith='uBy')
        obj = SomeModel()
        self.assertTrue(q_obj.comparator(obj))

    def test_exact(self):
        q_obj = Q(secret__gem__exact='ruby')
        obj = SomeModel()
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__exact='Ruby')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_icontains(self):
        q_obj = Q(secret__gem__icontains='UB')
        obj = SomeModel()
        self.assertTrue(q_obj.comparator(obj))

    def test_iexact(self):
        q_obj = Q(secret__gem__iexact='Ruby')
        obj = SomeModel()
        self.assertTrue(q_obj.comparator(obj))

        obj = SomeModel(secret='BUẞE')
        q_obj = Q(secret__gem__iexact='busse')
        self.assertTrue(q_obj.comparator(obj))

    def test_nested_gt(self):
        obj = SomeModel(secret=7)

        q_obj = Q(secret__gem__gt=6)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__gt=8)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_gte(self):
        obj = SomeModel(secret=7)

        q_obj = Q(secret__gem__gte=6)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__gte=7)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__gte=8)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_in(self):
        obj = SomeModel(secret=7)

        q_obj = Q(secret__gem__in=[1, 2, 3, 4, 5, 6, 7])
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__in=[1, 2, 3])
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_iin(self):
        obj = SomeModel()
        q_obj = Q(secret__gem__iin=['RuBy', 'PeaRls', 'DiamOnds'])
        self.assertTrue(q_obj.comparator(obj))

    def test_isnone(self):
        obj = SomeModel(question=None)

        q_obj = Q(question__isnone=True)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__isnone=True)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_lt(self):
        obj = SomeModel(secret=7)

        q_obj = Q(secret__gem__lt=8)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__lt=6)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_lte(self):
        obj = SomeModel(secret=7)

        q_obj = Q(secret__gem__lte=8)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__lte=7)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__lte=6)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_startswith(self):
        q_obj = Q(secret__gem__startswith='rub')
        obj = SomeModel()
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__startswith='rb')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_istartswith(self):
        q_obj = Q(secret__gem__istartswith='RUB')
        obj = SomeModel()
        self.assertTrue(q_obj.comparator(obj))
