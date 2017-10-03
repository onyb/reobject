import unittest

from reobject.models import Model, Field
from reobject.query import Q


class StringSecret(object):
    def __init__(self, gem='ruby'):
        self.gem = gem


class NumericSecret(object):
    def __init__(self, gem=7):
        self.gem = gem


class IterableSecret(object):
    def __init__(self, gem=('A', 'B', 'C',)):
        self.gem = gem


class SecretModel(Model):
    question = Field(default='')
    secret = Field(default=None)


class TestQ(unittest.TestCase):
    def tearDown(self):
        SecretModel.objects.all().delete()

    def test_simple(self):
        q_obj = Q(question='What?')

        obj = SecretModel(question='What?')
        self.assertTrue(q_obj.comparator(obj))

        obj = SecretModel(question='When?')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_attrs(self):
        q_obj = Q(secret__gem='ruby')
        obj = SecretModel(secret=StringSecret())
        self.assertTrue(q_obj.comparator(obj))

    def test_nested_contains(self):
        q_obj = Q(secret__gem__contains='ub')
        obj = SecretModel(secret=StringSecret())
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__contains='rby')
        self.assertFalse(q_obj.comparator(obj))

        q_obj = Q(secret__gem__contains='C')
        obj = SecretModel(secret=IterableSecret())
        self.assertTrue(q_obj.comparator(obj))

    def test_nested_endswith(self):
        q_obj = Q(secret__gem__endswith='uby')
        obj = SecretModel(secret=StringSecret())
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__endswith='rb')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_iendswith(self):
        q_obj = Q(secret__gem__iendswith='uBy')
        obj = SecretModel(secret=StringSecret())
        self.assertTrue(q_obj.comparator(obj))

    def test_exact(self):
        q_obj = Q(secret__gem__exact='ruby')
        obj = SecretModel(secret=StringSecret())
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__exact='Ruby')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_icontains(self):
        q_obj = Q(secret__gem__icontains='UB')
        obj = SecretModel(secret=StringSecret())
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__icontains='c')
        obj = SecretModel(secret=IterableSecret())
        self.assertTrue(q_obj.comparator(obj))

    def test_iexact(self):
        q_obj = Q(secret__gem__iexact='Ruby')
        obj = SecretModel(secret=StringSecret())
        self.assertTrue(q_obj.comparator(obj))

        obj = SecretModel(secret=StringSecret('BUẞE'))
        q_obj = Q(secret__gem__iexact='busse')
        self.assertTrue(q_obj.comparator(obj))

    def test_nested_gt(self):
        obj = SecretModel(secret=NumericSecret())

        q_obj = Q(secret__gem__gt=6)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__gt=8)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_gte(self):
        obj = SecretModel(secret=NumericSecret())

        q_obj = Q(secret__gem__gte=6)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__gte=7)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__gte=8)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_in(self):
        obj = SecretModel(secret=NumericSecret())

        q_obj = Q(secret__gem__in=[1, 2, 3, 4, 5, 6, 7])
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__in=[1, 2, 3])
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_iin(self):
        obj = SecretModel(secret=StringSecret())
        q_obj = Q(secret__gem__iin=['RuBy', 'PeaRls', 'DiamOnds'])
        self.assertTrue(q_obj.comparator(obj))

    def test_isnone(self):
        obj = SecretModel(question=None)

        q_obj = Q(question__isnone=True)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__isnone=True)
        self.assertTrue(q_obj.comparator(obj))

    def test_nested_lt(self):
        obj = SecretModel(secret=NumericSecret())

        q_obj = Q(secret__gem__lt=8)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__lt=6)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_lte(self):
        obj = SecretModel(secret=NumericSecret())

        q_obj = Q(secret__gem__lte=8)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__lte=7)
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__lte=6)
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_startswith(self):
        q_obj = Q(secret__gem__startswith='rub')
        obj = SecretModel(secret=StringSecret())
        self.assertTrue(q_obj.comparator(obj))

        q_obj = Q(secret__gem__startswith='rb')
        self.assertFalse(q_obj.comparator(obj))

    def test_nested_istartswith(self):
        q_obj = Q(secret__gem__istartswith='RUB')
        obj = SecretModel(secret=StringSecret())
        self.assertTrue(q_obj.comparator(obj))

    def test_nested_dict_istartswith(self):
        q_obj = Q(secret__gem__istartswith='RUB')
        obj = SecretModel(secret={'gem': 'ruby'})
        self.assertTrue(q_obj.comparator(obj))