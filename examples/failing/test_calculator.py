import unittest
from calculator import subtotal
class TestSubtotal(unittest.TestCase):
    def test_total(self):self.assertEqual(subtotal([100,200]),300)
    def test_empty(self):self.assertEqual(subtotal([]),0)
    def test_negative(self):
        with self.assertRaises(ValueError):subtotal([-1])
