from django.test import TestCase


class Testtest(TestCase):
    def test_test(self):
        a = 1
        self.assertEqual(a, 1)