from typing import Union, Tuple
from TDecimalException import (
    UnknownNumberTypeException, WrongArgumentException, DivisorIsZeroException,
    ShouldntBeHereException, ComparisonException)


class TDecimal:
    # imitation of: decimal.getcontext().prec = 28
    precision: int = 28

    def __init__(self, num: Union[int, str], decimal_point_length: int = None) -> None:
        # Let's only process strings for now
        # num could be str or int
        if isinstance(num, int):
            self.int_part = num
            self.decimal_point_length = decimal_point_length
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
                    # 计算有几位小数点
                    self.decimal_point_length = len(num) - decimal_point_index - 1
                    self.int_part = int(num.replace(".", ""))
        else:
            raise UnknownNumberTypeException(
                f"TDecimal only accepts `int` or `str`, num is {type(num)}"
            )

    def __add__(self, other: "TDecimal") -> "TDecimal":
        # e.g. 123.45 + 2.135
        # 下面这样+就错了
        # 12345
        #  2135
        # 得是
        # 123450
        #   2135
        # 那就是先拿一个最大的小数位数
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
        while num // divisor > 0:
            num_len += 1
            divisor *= 10
        return num_len

    @staticmethod
    def _round_int(num_int: int, precision: int, num_length: int) -> int:
        # My Algorithm: 1234567, precision: 5
        # 1234567 // (7-5) ** 10 -> 1234567 // 100 = 12345
        # 123456 % 100 = 56, 56 // (7-5-1) ** 10 = 5
        # if 5 >= 5, 1234 + 1; else 1234
        divisor = 10 ** (num_length - precision)
        new_num_int = num_int // divisor
        round_pos_num = (num_int % divisor) // (10 ** (num_length - precision - 1))
        if abs(round_pos_num) >= 5:
            if num_int > 0:
                new_num_int += 1
            else:
                new_num_int -= 1
        return new_num_int

    def _round_precision(self, d_num: 'TDecimal') -> 'TDecimal':
        # 用 rounding away from 0 的方法，现实生活中算钱是 rounding away from 0 的
        # e.g. -1.5 -> -2
        # num_length 计算 self.int_part 有多少位数
        if d_num.int_part == 0:
            return d_num
        else:
            num_length = self._cal_num_length(d_num.int_part)
            if num_length <= self.precision:
                return d_num
            else:
                new_int_part = self._round_int(d_num.int_part, self.precision, num_length)
                if d_num.int_part / 10 ** d_num.decimal_point_length > 0:
                    # 实际数字是 > 0的
                    if self.precision <= num_length - d_num.decimal_point_length:
                        new_dec_pt_len = 0
                    else:
                        new_dec_pt_len = self.precision - (num_length - d_num.decimal_point_length)

                else:
                    # 实际数字是 < 0 的，0.xxx
                    new_dec_pt_len = d_num.decimal_point_length - num_length + d_num.precision

                new_num = TDecimal(new_int_part, new_dec_pt_len)
                return new_num

    def __sub__(self, other: "TDecimal") -> "TDecimal":
        return self.__add__(-other)

    def __neg__(self):
        self.int_part = - self.int_part
        return self

    def __eq__(self, other: Union[str, int, 'TDecimal']) -> bool:
        if isinstance(other, str):
            return self.__str__() == other
        elif isinstance(other, int):
            return self.int_part == other
        elif isinstance(other, TDecimal):
            diff = abs(self.decimal_point_length - other.decimal_point_length)
            if self.decimal_point_length >= other.decimal_point_length:
                right_int = other.int_part * 10 ** diff
                left_int = self.int_part
            else:
                left_int = self.int_part * 10 ** diff
                right_int = other.int_part
            return left_int == right_int
        else:
            raise ComparisonException("__eq__ accepts a `str`, `int` or another `TDecimal`"
                                      f"as a compare candiate, {type(other)} is not"
                                      "allowed")

    def __ne__(self, other: Union[str, int, 'TDecimal']) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Union[str, int, 'TDecimal']) -> bool:
        if isinstance(other, str):
            return self < TDecimal(other)
        elif isinstance(other, int):
            return self.int_part < other
        elif isinstance(other, TDecimal):
            diff = abs(self.decimal_point_length - other.decimal_point_length)
            if self.decimal_point_length >= other.decimal_point_length:
                right_int = other.int_part * 10 ** diff
                left_int = self.int_part
            else:
                left_int = self.int_part * 10 ** diff
                right_int = other.int_part
            return left_int < right_int
        else:
            raise ComparisonException("__lt__ accepts a `str`, `int` or another `TDecimal`"
                                      f"as a compare candiate, {type(other)} is not"
                                      "allowed")

    def __le__(self, other: Union[str, int, 'TDecimal']) -> bool:
        return self < other or self == other

    def __gt__(self, other: Union[str, int, 'TDecimal']) -> bool:
        if isinstance(other, str):
            return self > TDecimal(other)
        elif isinstance(other, int):
            return self.int_part > other
        elif isinstance(other, TDecimal):
            diff = abs(self.decimal_point_length - other.decimal_point_length)
            if self.decimal_point_length >= other.decimal_point_length:
                right_int = other.int_part * 10 ** diff
                left_int = self.int_part
            else:
                left_int = self.int_part * 10 ** diff
                right_int = other.int_part
            return left_int > right_int
        else:
            raise ComparisonException("__gt__ accepts a `str`, `int` or another `TDecimal`"
                                      f"as a compare candiate, {type(other)} is not"
                                      "allowed")

    def __ge__(self, other: Union[str, int, 'TDecimal']) -> bool:
        return self > other or self == other

    def __mul__(self, other: "TDecimal") -> "TDecimal":
        d_multi = self.int_part * other.int_part
        dec_pt_len = self.decimal_point_length + other.decimal_point_length
        new_num = self._round_precision(TDecimal(d_multi, dec_pt_len))
        return new_num

    @staticmethod
    def _find_pattern(num_str: str) -> Tuple[bool, str]:
        has_pattern = False
        pattern = ""
        for i in range(0, len(num_str) // 2 + 1):
            p = num_str[: i + 1]
            num_str_list = num_str.split(p)
            if num_str_list[0] == num_str_list[1]:
                pattern = p
                has_pattern = True
                break
        return has_pattern, pattern

    @staticmethod
    def _div_get_quotient_and_round(dividend: int, divisor: int, precision: int) -> 'Tdecimal':
        # quotient 位数要比 precision 多1位
        if divisor == 0:
            raise DivisorIsZeroException("Divisor can't be 0 ")
        if dividend == 0:
            return TDecimal(0, 0)

        if dividend % divisor == 0:
            return TDecimal(dividend // divisor, 0)

        # 除不尽
        # My Algorithm is fucking Genius ;P !
        # I am so happy I made it !
        dec_pt_len = 0
        tmp_quotient = quotient = dividend // divisor
        quotient_length = TDecimal._cal_num_length(quotient)
        while quotient_length < (precision + 1):
            dividend = dividend - (tmp_quotient * divisor)
            tmp_quotient = dividend // divisor
            while tmp_quotient == 0:
                dividend = dividend * 10
                if quotient_length < precision:
                    # quotient_length == precision 不处理
                    # quotient_length < (precision + 1) , 是为了多拿1位 tmp_quotient
                    dec_pt_len += 1
                    quotient = quotient * 10
                tmp_quotient = dividend // divisor

            # When it's out of the above loop,
            # tmp_quotient would not be 0 and have a number
            if quotient_length < precision:
                quotient += tmp_quotient
                quotient_length = TDecimal._cal_num_length(quotient)
            else:
                # Do rounding here, rouding away from 0
                if tmp_quotient >= 5:
                    if quotient < 0:
                        quotient -= 1
                    elif quotient > 0:
                        quotient += 1
                    else:
                        raise ShouldntBeHereException(
                            "Normally, you should never get to this code brand."
                            "Go fuck the author's tutor if you get this Exception")
                # exit No.2
                break
        return TDecimal(quotient, dec_pt_len)

    def __truediv__(self, other: "TDecimal") -> "TDecimal":
        dividend, divisor = self.int_part, other.int_part
        max_dec_len = max(self.decimal_point_length, other.decimal_point_length)
        dividend, divisor = map(lambda x: x * 10 ** max_dec_len, [dividend, divisor])

        new_num = self._div_get_quotient_and_round(dividend, divisor, self.precision)
        return new_num

    def _insert_decimal_point(self) -> str:
        if self.int_part == 0:
            return "0"
        int_part_str = str(self.int_part)
        if self.decimal_point_length == 0:
            return int_part_str
        else:
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
            return print_str

    def __str__(self) -> str:
        return self._insert_decimal_point()


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
    pass
