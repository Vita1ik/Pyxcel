import unittest
from modules.calculator import Calculator

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_addition(self):
        result = self.calc.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calc.evaluate("10 - 3")
        self.assertEqual(result, 7)

    def test_multiplication(self):
        result = self.calc.evaluate("4 * 6")
        self.assertEqual(result, 24)

    def test_division(self):
        result = self.calc.evaluate("8 / 4")
        self.assertEqual(result, 2)

    def test_combined_operations(self):
        result = self.calc.evaluate("3 + 5 * 2 - 8 / 4")
        self.assertEqual(result, 11)

    def test_parentheses(self):
        result = self.calc.evaluate("(3 + 5) * 2")
        self.assertEqual(result, 16)

    def test_nested_parentheses(self):
        result = self.calc.evaluate("3 + (2 * (2 + 3)) - 6 / (4 - 1)")
        self.assertEqual(result, 11)

    def test_zero_division(self):
        result = self.calc.evaluate("5 / 0")
        self.assertEqual(result, 'NaN')

    def test_empty_expression(self):
        result = self.calc.evaluate("")
        self.assertEqual(result, 'SYNTAX_ERROR')

    def test_invalid_expression(self):
        result = self.calc.evaluate("")
        self.assertEqual(result, 'SYNTAX_ERROR')

if __name__ == '__main__':
    unittest.main()
