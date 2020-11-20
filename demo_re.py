"""
    ============
    Author:hw
    data:2020/11/20 16:23
    ============
"""
"""
^((([5-9]\d)|([1-9]\d{2})|([1-4]\d{3})|5000)(\,(([5-9]\d)|([1-9]\d{2})|([1-4]\d{3})|5000)){0,4})$
"""
#^([5-9]\d)|([1-9]\d{2})|([1-4]\d{3})|5000$
import re
# res=input("输入50-5000：")
# ret=re.match("[5-9]\d",res)
# print(ret.group())
text = "apple price is $99,orange price is $10"
ret = re.search(r".*(\$\d+).*(\$\d+)",text)
print(ret.group())
print(ret.group(0))
print(ret.group(1))
print(ret.group(2))
print(ret.groups())