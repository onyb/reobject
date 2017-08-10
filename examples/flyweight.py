# -*- coding: utf-8 -*-

import unittest

from reobject.models import Model, Field


class Card(Model):
    suit = Field()
    color = Field()


class TestCard(unittest.TestCase):
    def test_flyweight(self):
        c1, _ = Card.objects.get_or_create(suit='K', color='♥')
        c2, _ = Card.objects.get_or_create(suit='K', color='♥')
        c3, _ = Card.objects.get_or_create(suit='A', color='♠')

        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)

        self.assertIs(c1, c2)
        self.assertIsNot(c1, c3)

        self.assertEqual(Card.objects.count(), 2)

        c1.delete()
        self.assertEqual(Card.objects.count(), 1)

        self.assertNotIn(c2, Card.objects.all())

        c3.delete()
        self.assertEqual(Card.objects.count(), 0)


if __name__ == '__main__':
    unittest.main()
