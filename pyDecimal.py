from decimal import Decimal as Dec

print(Dec(1) + Dec(2))

print('===============')
print(Dec(1.1) + Dec(2.2))
print(1.1 + 2.2)
print('{0:.28f}'.format(1.1 + 2.2))
print(Dec('1.1') + Dec('2.2'))
print(Dec('1.100000') + Dec('2.2'))



# print('===============')
# print(Dec(1.1) + Dec(2.2) - Dec(3.3))
# print(1.1 + 2.2 - 3.3)
# print('{0:.28f}'.format(1.1 + 2.2 - 3.3))

# 草你吗我说怎么不对劲，原来python的Decimal库要按Decimal算，传入的得是str
print(Dec(1236123) / Dec(1283182))
print('{0:.28f}'.format(1236123000000 / 1283182))