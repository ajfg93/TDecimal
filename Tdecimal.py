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
            decimal_point_index = num.find(".")
            if decimal_point_index == -1:
                self.int_part = int(num)
                self.decimal_point_length = 0
            else:
                # 小数点位数
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
        # 懂了，那就是先拿一个最大的小数位数
        # 草，为什么这里other没有 智能方法提示，
        # 有了，先用着，DONE: 晚点回来看下:
        # https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
        diff = abs(self.decimal_point_length - other.decimal_point_length)

        if self.decimal_point_length >= other.decimal_point_length:
            d_sum = self.int_part + other.int_part * (10 ** diff)
            dec_pt_len = self.decimal_point_length
        else:
            d_sum = self.int_part * (10 ** diff) + other.int_part
            dec_pt_len = other.decimal_point_length

        # round precision
        # round 要在这里做，而不是在print的地方做
        if len(str(d_sum)) > self.precision:
            new_num = self._round_precision(TDecimal(d_sum, dec_pt_len))
        else:
            new_num = TDecimal(d_sum, dec_pt_len)
        return new_num

    def _round_precision(self, d_num: 'TDecimal') -> 'TDecimal':
        # Dec('1.31') + Dec('1.216111') = Decimal('2.53')
        # 1310000 + 1216111 = 2526111
        # 输入是 d_result = 2526111, dec_pt_len = 6
        # 假设 precision = 3
        # 输出需要是 d_result = 253, dec_pt_len = 2
        # 用 rounding towards -INF 的方式，现实生活算钱也是应该是 rounding towards -INF 吧？ DONE: 需要确认下
        # 现实生活中算钱是 rounding away from 0 的
        # e.g. -1.5 -> -2
        # 负数和 0， 正数和 1
        d_result, dec_pt_len = d_num.int_part, d_num.decimal_point_length
        d_result_sign = 0 if d_result < 0 else 1
        d_result_str = str(d_result).strip("-")
        new_dec_pt_len = self.precision - (len(d_result_str) - dec_pt_len)
        if int(d_result_str[self.precision]) >= 5:
            new_d_result = int(d_result_str[: self.precision]) + 1
        else:
            new_d_result = int(d_result_str[: self.precision])
        new_d_result = new_d_result if d_result_sign else -new_d_result
        return TDecimal(new_d_result, new_dec_pt_len)

    def __sub__(self, other: "TDecimal") -> "TDecimal":
        return self.__add__(-other)

    def __neg__(self):
        self.int_part = - self.int_part
        return self

    def __mul__(self, other: "TDecimal") -> "TDecimal":
        d_multi = self.int_part * other.int_part
        dec_pt_len = self.decimal_point_length + other.decimal_point_length
        if len(str(d_multi)) > self.precision:
            new_num = self._round_precision(TDecimal(d_multi, dec_pt_len))
        else:
            new_num = TDecimal(d_multi, dec_pt_len)
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
    # print(TDecimal('123.45') + TDecimal('2.135'))
    # print(TDecimal('1.31') + TDecimal('1.216111'))
    # print(TDecimal('0.1') + TDecimal('-0.1'))
    # print(TDecimal('999.526111') + TDecimal('0.1'))
    # print(TDecimal('1.1') - TDecimal('2.2'))

    # print(TDecimal('1.5') * TDecimal('1.62123'))
    # print(TDecimal('1.5') * TDecimal('1.62623'))
    # print(TDecimal('1236123') / TDecimal('1283182'))
    print(TDecimal('1')/ TDecimal('3'))
    pass
