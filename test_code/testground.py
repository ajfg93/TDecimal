def cal_num_length(num: int) -> int:
    num_len = 1
    divisor = 10
    while num // divisor > 0:
        num_len += 1
        divisor *= 10
    return num_len

print(cal_num_length(12345))
