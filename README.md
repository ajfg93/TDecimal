

1. 利用了python的int是unlimited length的，进行了大程度的作弊行为。  
python的int居然不是一个primitive type，这真的出乎意料。  
换成C++我还真不知道该怎么写。不过我用python写凭啥不能利用int？
   

2. 加减乘应该没问题了，除法不知道怎么处理 `1236123/1283182 = 0.9633263247146546` 这种。直接交作业了

3. 没有写单元测试。。。之前没写过，简单看了下教程会写了，需要再补。
而且我感觉这种布置作业的，应该是老师给测试用例。TDD写起来其实更舒服，因为不用学生自己去想用例。
   
4. 保留有效数字，没有做类似python decimal的 科学计数法输出

例如
```python
from decimal import Decimal as Dec
getcontext().prec = 3
print(Dec('1222.31') + Dec('1.216'))
```
输出结果是： `1.22E+3`

我没做处理这个
