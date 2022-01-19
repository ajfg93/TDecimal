import unittest
from TDecimal import TDecimal
from TDecimalException import (
    UnknownNumberTypeException, WrongArgumentException, DivisorIsZeroException,
    ComparisonTypeNotAllowedException
)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # print('setUp...')
        pass

    def test_initialization(self):
        self.assertRaises(WrongArgumentException, TDecimal, '3', 2)
        self.assertRaises(WrongArgumentException, TDecimal, '12.3a4')
        self.assertRaises(UnknownNumberTypeException, TDecimal, [1, 2, 3])

    def test_print(self):
        self.assertEqual(str(TDecimal("1.320000000008989")), "1.320000000008989")
        self.assertEqual(str(TDecimal("0.00001")), "0.00001")
        self.assertEqual(str(TDecimal("123")), "123")
        self.assertEqual(str(TDecimal("-123")), "-123")
        self.assertEqual(repr(TDecimal('1.321')), '1.321')

    def test_addtion(self):
        TDecimal.precision = 6
        self.assertEqual(TDecimal("1.1") + TDecimal("2.2"), "3.3")
        self.assertEqual(TDecimal("123.45") + TDecimal("2.135"), "125.585")
        TDecimal.precision = 5
        self.assertEqual(TDecimal("123.45") + TDecimal("2.135"), "125.59")
        TDecimal.precision = 10
        self.assertEqual(TDecimal("1.31") + TDecimal("1.216111"), "2.526111")
        TDecimal.precision = 3
        self.assertEqual(TDecimal("1.31") + TDecimal("1.216111"), "2.53")
        self.assertEqual(TDecimal("0.1") + TDecimal("-0.1"), "0")
        TDecimal.precision = 20
        self.assertEqual(TDecimal("999.526111") + TDecimal("0.1"), "999.626111")
        TDecimal.precision = 3
        self.assertEqual(TDecimal("999.526111") + TDecimal("0.1"), "1000")
        TDecimal.precision = 5
        self.assertEqual(TDecimal("999.526111") + TDecimal("0.1"), "999.63")

    def test_substraction(self):
        TDecimal.precision = 6
        self.assertEqual(TDecimal("1.1") - TDecimal("2.2"), "-1.1")
        TDecimal.precision = 5
        self.assertEqual(TDecimal("-1.23455") - TDecimal("0.00001"), "-1.2346")
        self.assertEqual(TDecimal("-0.0123456") - TDecimal("0.01"), "-0.022346")

    def test_multiple(self):
        TDecimal.precision = 20
        self.assertEqual(TDecimal("1.5") * TDecimal("1.62123"), "2.431845")
        TDecimal.precision = 2
        self.assertEqual(TDecimal("1.5") * TDecimal("1.62123"), "2.4")
        TDecimal.precision = 3
        self.assertEqual(TDecimal("1.5") * TDecimal("1.62623"), "2.44")
        self.assertEqual(TDecimal("0.003267") * TDecimal("1"), "0.00327")

    def test_divide(self):
        TDecimal.precision = 28
        self.assertEqual(
            TDecimal('1') / TDecimal('3'), "0.3333333333333333333333333333"
        )
        self.assertEqual(
            TDecimal('1') / TDecimal('7'), "0.1428571428571428571428571429"
        )
        self.assertEqual(
            TDecimal('100') / TDecimal('7'), "14.28571428571428571428571429"
        )

        self.assertEqual(
            TDecimal("1236123") / TDecimal("1283182"), "0.9633263247146546631732677048"
        )
        TDecimal.precision = 6
        self.assertEqual(TDecimal('1') / TDecimal('300'), "0.00333333")

        with self.assertRaises(DivisorIsZeroException):
            TDecimal('1') / TDecimal('0')

        self.assertEqual(TDecimal(0) / TDecimal('123'), '0')
        self.assertEqual(TDecimal(102) / TDecimal(3), 34)
        TDecimal.precision = 5
        self.assertEqual(
            TDecimal("-1236123") / TDecimal("1283182"), "-0.96333"
        )

        self.assertEqual(
            TDecimal("-1236123") / TDecimal("12831820"), "-0.096333"
        )

        self.assertEqual(
            TDecimal("10") / TDecimal("0.3"), "33.333"
        )
        self.assertEqual(
            TDecimal("0.01") / TDecimal("0.3"), "0.033333"
        )
        TDecimal.precision = 6
        self.assertEqual(
            TDecimal("1") / TDecimal("9999"), "0.000100010"
        )

    def test_comparison(self):
        self.assertTrue(TDecimal('1.1') == TDecimal('1.1'))
        self.assertTrue(TDecimal('1.1') == '1.1')
        self.assertTrue(TDecimal('1') == '1')
        self.assertTrue(TDecimal('1234.0') == 1234)
        self.assertFalse(TDecimal('1') != '1')
        self.assertFalse(TDecimal('11.1') == TDecimal('1.11'))

        self.assertTrue(TDecimal('0.231') > '0.22222')
        self.assertTrue(TDecimal('0.231') > TDecimal('0.22222'))
        self.assertTrue(TDecimal('35') > 22)

        self.assertTrue(TDecimal('355') < 22456)
        self.assertTrue(TDecimal('-1.2358') < 22456)
        self.assertTrue(TDecimal('-1.2358') < '22456')
        self.assertTrue(TDecimal('-1.2358') < TDecimal('12.1'))

        self.assertTrue(TDecimal('123.45') >= '123.442123')
        self.assertTrue(TDecimal('123.45') >= '123.45')
        self.assertTrue(TDecimal('123.45') <= '123.45')
        self.assertTrue(TDecimal('123.45') <= '123.451')
        self.assertTrue(TDecimal('0') >= -1)
        self.assertTrue(TDecimal('-2') <= 0)

        self.assertFalse(TDecimal('123.45') == 123.45)
        with self.assertRaises(ComparisonTypeNotAllowedException):
            TDecimal('123.45') < 123.45

        with self.assertRaises(ComparisonTypeNotAllowedException):
            TDecimal('123.45') > 123.451

    def tearDown(self):
        # print('tearDown...')
        pass


if __name__ == "__main__":  # pragma: no cover
    # unittest.main()
    # print('123')
    pass
