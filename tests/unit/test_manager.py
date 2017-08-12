import unittest
from datetime import datetime

from reobject.models.fields import Field, ManyToManyField
from reobject.models.manager import Manager
from reobject.models.model import Model


class SomeModel(Model):
    p = Field()
    q = Field()
    r = Field()


class TestQuery(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        SomeModel.objects.all().delete()

    def test_descriptor_cls(self):
        try:
            SomeModel.objects
            SomeModel.objects.filter
        except AttributeError:
            self.assertFalse(True)
        else:
            pass  # AttributeError was not raised

    def test_descriptor_instance(self):
        obj = SomeModel(1, 2, 3)
        with self.assertRaises(AttributeError):
            obj.objects
            obj.objects.foo

    def test_create(self):
        obj = SomeModel(p=1, q=2, r=1)

        self.assertEqual(obj.p, 1)
        self.assertEqual(obj.q, 2)
        self.assertEqual(obj.r, 1)
        self.assertEqual(obj.id, id(obj))
        self.assertLess(obj.created, datetime.utcnow())
        self.assertEqual(obj.created, obj.updated)

    def test_none(self):
        self.assertFalse(SomeModel.objects.none())

    def test_all(self):
        SomeModel(p=0, q=0, r=1)
        SomeModel(p=0, q=1, r=0)
        SomeModel(p=1, q=0, r=0)

        self.assertEqual(len(SomeModel.objects.all()), 3)

    def test_manager_model(self):
        self.assertEqual(SomeModel.objects.model, SomeModel)


class Teacher(Model):
    pass


class Student(Model):
    teacher = ManyToManyField(Teacher)


class TestRelatedManager(unittest.TestCase):
    def setUp(self):
        self.teacher_a = Teacher()
        self.teacher_b = Teacher()

        Student(teacher=self.teacher_a)
        Student(teacher=self.teacher_a)
        Student(teacher=self.teacher_a)
        Student(teacher=self.teacher_b)
        Student(teacher=self.teacher_b)

    def tearDown(self):
        Teacher.objects.all().delete()
        Student.objects.all().delete()

    def test_manager_cls(self):
        self.assertIsInstance(Teacher.objects, Manager)
        self.assertIsInstance(Student.objects, Manager)

        self.assertEqual(self.teacher_a.student_set.__class__.__name__, 'RelatedManager')
        self.assertEqual(self.teacher_a.student_set.model, Student)

    def test_many_to_many_relationship(self):
        self.assertEqual(
            self.teacher_a.student_set.all(),
            Student.objects.filter(teacher__pk=self.teacher_a.pk)
        )

        self.assertEqual(
            self.teacher_a.student_set.count(), 3
        )

        self.assertEqual(
            self.teacher_b.student_set.all(),
            Student.objects.filter(teacher__pk=self.teacher_b.pk)
        )

        self.assertEqual(
            self.teacher_b.student_set.count(), 2
        )
