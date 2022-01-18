from typing import Union, Tuple
from TDecimalException import (
    UnknownNumberTypeException, WrongArgumentException, DivisorIsZeroException,
    ComparisonTypeNotAllowedException
)


class TDecimal:
    # imitation of: decimal.getcontext().prec = 28
    precision: int = 28

    def __init__(self, num: Union[int, str], decimal_point_length: int = None) -> None:
        # Let's only process strings for now
        # num could be str or int
        if isinstance(num, int):
            self.int_part = num
            self.decimal_point_length = decimal_point_length if decimal_point_length else 0
        elif isinstance(num, str):
            if decimal_point_length:
                raise WrongArgumentException(
                    "decimal_point_length is not allowed when `num` is str type"
                )
            else:
                decimal_point_index = num.find(".")
                if decimal_point_index == -1:
                    self.int_part = int(num)
                    self.decimal_point_length = 0
                else:
                    # calculator how many decimal points there are
                    self.decimal_point_length = len(num) - decimal_point_index - 1
                    self.int_part = int(num.replace(".", ""))
        else:
            raise UnknownNumberTypeException(
                f"TDecimal only accepts `int` or `str`, num is {type(num)}"
            )

    def __add__(self, other: "TDecimal") -> "TDecimal":
        # e.g. 123.45 + 2.135
        # Adding like this is wrong:
        # 12345
        #  2135
        # should be:
        # 123450
        #   2135
        # which means I need to get a largest decimal point length first
        diff = abs(self.decimal_point_length - other.decimal_point_length)

        if self.decimal_point_length >= other.decimal_point_length:
            d_sum = self.int_part + other.int_part * (10 ** diff)
            dec_pt_len = self.decimal_point_length
        else:
            d_sum = self.int_part * (10 ** diff) + other.int_part
            dec_pt_len = other.decimal_point_length

        new_num = self._round_precision(TDecimal(d_sum, dec_pt_len))
        return new_num

    @staticmethod
    def _cal_num_length(num: int) -> int:
        num_len = 1
        divisor = 10
        abs_num = abs(num)
        while abs_num // divisor > 0:
            num_len += 1
            divisor *= 10
        return num_len

    @staticmethod
    def _round_int(num_int: int, precision: int, num_length: int) -> int:
        # My Algorithm: 1234567, precision: 5
        # 1234567 / (7-5) ** 10 -> 1234567 / 100 = 12345
        # 123456 % 100 = 56, 56 / (7-5-1) ** 10 = 5
        # <del>use int( a / b), not a // b, the latter is a floor div</del>
        # Use `truncate_div` for now
        # if 5 >= 5, 1234 + 1; else 1234
        divisor = 10 ** (num_length - precision)
        new_num_int = TDecimal.truncate_div(num_int, divisor)
        # -12 % 10 = 8, 12 % -10 = -8
        # 12 % 10 = 2
        round_pos_num = TDecimal.truncate_div(abs(num_int) % divisor, 10 ** (num_length - precision - 1))

        if round_pos_num >= 5:
            if num_int > 0:
                new_num_int += 1
            else:
                new_num_int -= 1
        return new_num_int

    def _round_precision(self, d_num: 'TDecimal') -> 'TDecimal':
        # I use rounding away from 0 method, in real life we use rounding away from 0 for money:
        # e.g. You own me $5.5 (-5.5), we are friends, just give me $5 (-5) back.
        # e.g. The food is $5.5 (+5.5), let's just make it $6 (+6) for simplicity.
        # num_length: calculator decimal length of self.int_part
        if d_num.int_part == 0:
            return d_num
        else:
            num_length = self._cal_num_length(d_num.int_part)
            if num_length <= self.precision:
                return d_num
            else:
                new_int_part = self._round_int(d_num.int_part, self.precision, num_length)
                if d_num.int_part / 10 ** d_num.decimal_point_length > 0:
                    # If real num > 0
                    if self.precision <= num_length - d_num.decimal_point_length:
                        new_dec_pt_len = 0
                    else:
                        new_dec_pt_len = self.precision - (num_length - d_num.decimal_point_length)

                else:
                    # If real num < 0, e.g 0.xxxx
                    new_dec_pt_len = d_num.decimal_point_length - num_length + d_num.precision

                new_num = TDecimal(new_int_part, new_dec_pt_len)
                return new_num

    def __sub__(self, other: "TDecimal") -> "TDecimal":
        return self.__add__(-other)

    def __neg__(self) -> 'TDecimal':
        self.int_part = - self.int_part
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.__str__() == other
        elif isinstance(other, int):
            return self.int_part == other * 10 ** self.decimal_point_length
        elif isinstance(other, TDecimal):
            left_int, right_int = TDecimal._boom_intpart_same_magnitude(self, other)
            return left_int == right_int
        else:
            # `self.assertIsNone(TDecimal('123.45') == 123.45)` is wrong,
            # I should do `assertFalse`, reason why:
            # `TDecimal('123.45') == 123.45` eventually delegate to so-called:
            # "If A’s __eq__() also returned NotImplemented, then the runtime would fall back to the built-in behaviour"
            # "for equality which is based on object identity (which in CPython, is the object’s address in memory)."
            # Source https://s16h.medium.com/pythons-notimplemented-type-2d720137bf41
            # TODO: Try to debug the CPython source code and validate that behavior
            # If it's `return 1`, then it returns `1`
            return NotImplemented

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @staticmethod
    def _boom_intpart_same_magnitude(left: 'TDecimal', right: 'TDecimal') -> Tuple[int, int]:
        diff = abs(left.decimal_point_length - right.decimal_point_length)
        if left.decimal_point_length >= right.decimal_point_length:
            right_int = right.int_part * 10 ** diff
            left_int = left.int_part
        else:
            left_int = left.int_part * 10 ** diff
            right_int = right.int_part
        return left_int, right_int

    def __lt__(self, other: object) -> bool:
        if isinstance(other, str):
            return self < TDecimal(other)
        elif isinstance(other, int):
            return self.int_part < other * 10 ** self.decimal_point_length
        elif isinstance(other, TDecimal):
            left_int, right_int = TDecimal._boom_intpart_same_magnitude(self, other)
            return left_int < right_int
        else:
            raise ComparisonTypeNotAllowedException(
                f"compare with {type(other)} type is not defined."
            )

    def __le__(self, other: object) -> bool:
        return not (self > other)

    def __gt__(self, other: object) -> bool:
        if isinstance(other, str):
            return self > TDecimal(other)
        elif isinstance(other, int):
            return self.int_part > other * 10 ** self.decimal_point_length
        elif isinstance(other, TDecimal):
            left_int, right_int = TDecimal._boom_intpart_same_magnitude(self, other)
            return left_int > right_int
        else:
            raise ComparisonTypeNotAllowedException(
                f"compare with {type(other)} type is not defined."
            )

    def __ge__(self, other: object) -> bool:
        return not (self < other)

    def __mul__(self, other: "TDecimal") -> "TDecimal":
        d_multi = self.int_part * other.int_part
        dec_pt_len = self.decimal_point_length + other.decimal_point_length
        new_num = self._round_precision(TDecimal(d_multi, dec_pt_len))
        return new_num

    @staticmethod
    def truncate_div(dividend: int, divisor: int) -> int:
        if (dividend < 0 < divisor) or (dividend > 0 > divisor):
            return - (abs(dividend) // abs(divisor))
        return dividend // divisor

    @staticmethod
    def _div_get_quotient_and_round(dividend: int, divisor: int, precision: int) -> 'TDecimal':
        # I need: len(quotention) == len(precision + 1)
        if divisor == 0:
            raise DivisorIsZeroException("Divisor can't be 0 ")
        if dividend == 0:
            return TDecimal(0, 0)

        if dividend % divisor == 0:
            return TDecimal(dividend // divisor, 0)

        # If can't not divide exactly
        dec_pt_len = 0
        tmp_quotient = quotient = TDecimal.truncate_div(dividend, divisor)
        quotient_length = TDecimal._cal_num_length(quotient)
        while quotient_length < (precision + 1):
            dividend = dividend - (tmp_quotient * divisor)
            tmp_quotient = TDecimal.truncate_div(dividend, divisor)
            while tmp_quotient == 0:
                dividend = dividend * 10
                tmp_quotient = TDecimal.truncate_div(dividend, divisor)
                dec_pt_len += 1
                quotient = quotient * 10
                quotient_length = TDecimal._cal_num_length(quotient)
                if quotient_length == (precision + 1):
                    break

            # When it's out of the above loop, g
            # tmp_quotient would not be 0 and have a number
            quotient += tmp_quotient

        f_quotient = TDecimal.truncate_div(quotient, 10)
        f_dec_pt_len = dec_pt_len - 1
        round_pos_num = abs(quotient) % 10

        if round_pos_num >= 5:
            if f_quotient < 0:
                f_quotient -= 1
            else:
                f_quotient += 1

        return TDecimal(f_quotient, f_dec_pt_len)

    def __truediv__(self, other: "TDecimal") -> "TDecimal":
        dividend, divisor = self.int_part, other.int_part
        dec_len_diff = abs(self.decimal_point_length - other.decimal_point_length)
        if self.decimal_point_length > other.decimal_point_length:
            divisor *= 10 ** dec_len_diff
        else:
            dividend *= 10 ** dec_len_diff

        new_num = self._div_get_quotient_and_round(dividend, divisor, self.precision)
        return new_num

    def _insert_decimal_point(self) -> str:
        if self.int_part == 0:
            return "0"
        if self.decimal_point_length == 0:
            return str(self.int_part)
        else:
            less_than_zero = 1 if self.int_part < 0 else 0
            int_part_str = str(self.int_part).strip('-')
            if len(int_part_str) > self.decimal_point_length:
                insert_index = len(int_part_str) - self.decimal_point_length
                print_str = (
                    int_part_str[:insert_index] + "." + int_part_str[insert_index:]
                )
            else:
                int_part_str = (
                    "0" * (abs(len(int_part_str) - self.decimal_point_length) + 1)
                    + int_part_str
                )
                insert_index = len(int_part_str) - self.decimal_point_length
                print_str = (
                    int_part_str[:insert_index] + "." + int_part_str[insert_index:]
                )
            if less_than_zero:
                print_str = '-' + print_str
            return print_str

    def __str__(self) -> str:
        return self._insert_decimal_point()

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == "__main__":

    # print(TDecimal('1.320000000008989'))
    # print(TDecimal('0.00001'))
    # print(TDecimal('1.1') + TDecimal('2.2'))
    # print(TDecimal('123.45') + TDecimal('2.135'))
    # print(TDecimal('1.31') + TDecimal('1.216111'))
    # print(TDecimal('0.1') + TDecimal('-0.1'))
    # print(TDecimal('999.526111') + TDecimal('0.1'))
    # print(TDecimal('1.1') - TDecimal('2.2'))

    # print(TDecimal('1.5') * TDecimal('1.62123'))
    # print(TDecimal('1.5') * TDecimal('1.62623'))
    # print(TDecimal('1236123') / TDecimal('1283182'))
    # print(TDecimal('20')/ TDecimal('3'))
    # a = TDecimal('1.1')
    # print(a.int_part)
    # print(a.decimal_point_length)
    # print(TDecimal('1.2') >= '1.1')
    # print(TDecimal('1234.0') == 1234)
    # TDecimal.precision = 6
    # print(TDecimal("-1236123") / TDecimal("1283182"))
    # print(TDecimal("-123"))
    # print(TDecimal("1.1") - TDecimal("2.2"))
    # print(TDecimal("-1236123") / TDecimal("1283182"))
    # TDecimal.precision = 5
    # print(TDecimal("-1.23455") - TDecimal("0.00001"))
    # print(TDecimal("1.5") * TDecimal("1.62623"))
    # print(TDecimal("10") / TDecimal("0.3"))
    # print(TDecimal("1") / TDecimal("9999"))
    # TDecimal.precision = 28
    # print(TDecimal('1') / TDecimal('3'))
    # print(TDecimal('0.999') / TDecimal('1'))
    # print(TDecimal("1.23") / TDecimal("-22.3334"))
    # print(TDecimal('123.45') == 123.45)
    # print(TDecimal('123.45') < 123.45)
    pass
