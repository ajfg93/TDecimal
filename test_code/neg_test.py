class Foo:
    def __init__(self, num):
        print('__init__')
        self.num = num

    def __add__(self, other):
        print('__add__')
        return self.num + other.num

    def __sub__(self, other):
        print('__sub__')
        other.num = - other.num
        return self.num + other.num

    def __neg__(self):
        print('__neg__')
        self.num = - self.num


a, b = Foo(1), Foo(3)
print(a + b)  # 4
print(a - b)  # -2
print(- b)
print(b.num)  # 3
