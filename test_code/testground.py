def cal_num_length(num: int) -> int:
    num_len = 1
    divisor = 10
    while num // divisor > 0:
        num_len += 1
        divisor *= 10
    return num_len

# print(cal_num_length(12345))


def f(x):
    return x * x


a,b,c = map(f, [1, 2, 3])

print(a)
dividend = 1
divisor = 2
dividend, divisor = map(lambda x: x + 1, [dividend, divisor])
print(locals())

print("abc"
      "def")