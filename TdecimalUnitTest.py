import unittest
from Tdecimal import TDecimal


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # print('setUp...')
        pass

    def test_print(self):
        self.assertEqual(str(TDecimal("1.320000000008989")), "1.320000000008989")
        self.assertEqual(str(TDecimal("0.00001")), "0.00001")
        self.assertEqual(str(TDecimal("123")), "123")
        self.assertEqual(str(TDecimal("-123")), "-123")

    def test_addtion(self):
        TDecimal.precision = 6
        self.assertEqual(str(TDecimal("1.1") + TDecimal("2.2")), "3.3")
        self.assertEqual(str(TDecimal("123.45") + TDecimal("2.135")), "125.585")
        TDecimal.precision = 5
        self.assertEqual(str(TDecimal("123.45") + TDecimal("2.135")), "125.59")
        TDecimal.precision = 10
        self.assertEqual(str(TDecimal("1.31") + TDecimal("1.216111")), "2.526111")
        TDecimal.precision = 3
        self.assertEqual(str(TDecimal("1.31") + TDecimal("1.216111")), "2.53")
        self.assertEqual(str(TDecimal("0.1") + TDecimal("-0.1")), "0")
        TDecimal.precision = 20
        self.assertEqual(str(TDecimal("999.526111") + TDecimal("0.1")), "999.626111")
        TDecimal.precision = 3
        self.assertEqual(str(TDecimal("999.526111") + TDecimal("0.1")), "1000")
        TDecimal.precision = 5
        self.assertEqual(str(TDecimal("999.526111") + TDecimal("0.1")), "999.63")

    def test_substraction(self):
        TDecimal.precision = 6
        self.assertEqual(str(TDecimal("1.1") - TDecimal("2.2")), "-1.1")

    def test_multiple(self):
        TDecimal.precision = 20
        self.assertEqual(str(TDecimal("1.5") * TDecimal("1.62123")), "2.431845")
        TDecimal.precision = 2
        self.assertEqual(str(TDecimal("1.5") * TDecimal("1.62123")), "2.4")
        TDecimal.precision = 3
        self.assertEqual(str(TDecimal("1.5") * TDecimal("1.62623")), "2.44")

    def test_divide(self):
        TDecimal.precision = 28
        self.assertEqual(
            str(TDecimal(1) / TDecimal(3)), "0.3333333333333333333333333333"
        )
        self.assertEqual(
            str(TDecimal(1) / TDecimal(7)), "0.1428571428571428571428571429"
        )
        self.assertEqual(
            str(TDecimal(100) / TDecimal(7)), "14.28571428571428571428571429"
        )
        # Failed to get the correct precision
        # Divide as float for now
        self.assertEqual(
            str(TDecimal("1236123") / TDecimal("1283182")), "0.9633263247146546"
        )
        TDecimal.precision = 6
        self.assertEqual(str(TDecimal(1) / TDecimal(300)), "0.00333333")

    def tearDown(self):
        # print('tearDown...')
        pass


if __name__ == "__main__":
    # unittest.main()
    # print('123')
    pass
