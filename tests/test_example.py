import unittest


class TestExample(unittest.TestCase):
    def test_example(self) -> None:
        self.assertEqual(1 + 1, 2)
        self.assertGreater(10, 5)