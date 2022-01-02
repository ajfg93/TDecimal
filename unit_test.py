import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp...')

    def test_something(self):
        self.assertEqual(True, True)

    def tearDown(self):
        print('tearDown...')


if __name__ == '__main__':
    unittest.main()
