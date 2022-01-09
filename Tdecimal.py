from typing import Union, Tuple
from TDecimalException import (
    UnknownNumberTypeException, WrongArgumentException)


class TDecimal:
    # imitation of: decimal.getcontext().prec = 28
    precision: int = 5

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

    def __truediv__(self, other: "TDecimal") -> "TDecimal":
        d_div = self.int_part / other.int_part

        d_div_str = str(d_div)

        prefix, suffix = d_div_str.split(".")
        less_than_zero = True if prefix == "0" else False
        zero_count_in_suffix = 0
        for c in suffix:
            if c == "0":
                zero_count_in_suffix += 1
            else:
                break

        num_str = str(int(prefix + suffix))
        has_pattern, pattern = self._find_pattern(num_str)

        if not has_pattern:
            return TDecimal(d_div_str)
        else:
            p = pattern
            while len(p) <= self.precision:
                p = p + pattern
            final_p = p[0 : self.precision + 1]
            if less_than_zero:
                dec_pt_len = len(final_p) + zero_count_in_suffix

            else:
                dec_pt_len = len(final_p) - len(prefix)

            new_num = self._round_precision(TDecimal(int(final_p), dec_pt_len))
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
    print(TDecimal('123.45') + TDecimal('2.135'))
    # print(TDecimal('1.31') + TDecimal('1.216111'))
    # print(TDecimal('0.1') + TDecimal('-0.1'))
    # print(TDecimal('999.526111') + TDecimal('0.1'))
    # print(TDecimal('1.1') - TDecimal('2.2'))

    # print(TDecimal('1.5') * TDecimal('1.62123'))
    # print(TDecimal('1.5') * TDecimal('1.62623'))
    # print(TDecimal('1236123') / TDecimal('1283182'))
    # print(TDecimal('1')/ TDecimal('3'))
    # a = TDecimal('1.1')
    # print(a.int_part)
    # print(a.decimal_point_length)
    pass
