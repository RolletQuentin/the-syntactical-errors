import unittest


class TestExample(unittest.TestCase):
    """Example test case"""

    def test_example(self) -> None:
        """Example test function"""
        self.assertEqual(1 + 1, 2)
        self.assertGreater(10, 5)
