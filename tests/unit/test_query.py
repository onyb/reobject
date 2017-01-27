import unittest

from reobject.model import Model


class TestModel(Model):
    def __init__(self, p, q, r):
        self.p = 1
        self.q = 2
        self.r = 1


class TestQuery(unittest.TestCase):
    def setUp(self):
        pass
