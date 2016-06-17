from django.test import TestCase

class ContentTypeModelTest(TestCase):
    def test_bad_math(self):
        self.assertEqual(1+1+1, 3, 'Your maths is wrong!')