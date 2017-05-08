import unittest

from reobject import Transaction, transactional
from reobject.model import Model


class Number(Model):
    def __init__(self, value):
        self.value = value

    @transactional
    def kaboom(self):
        self.value = '1111'  # invalid value
        self.value += 1  # should rollback


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.num = Number(value=-1)

    def tearDown(self):
        Number.objects._clear()

    def test_transaction_decorator(self):
        self.assertEqual(self.num.value, -1)
        try:
            self.num.kaboom()
        except TypeError as e:
            self.assertEqual(self.num.value, -1)

    def test_transaction_ctx_manager(self):
        try:
            with Transaction(self.num):
                self.num.value = 7
                self.num.value += 1
                self.assertEqual(self.num.value, 8)

                self.num.value = '7'
                self.num.value += 1
        except TypeError:
            self.assertEqual(self.num.value, -1)


if __name__ == '__main__':
    unittest.main()
