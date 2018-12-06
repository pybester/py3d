"""
测试类库
"""
import numpy as np

from model import Kjnum

a = Kjnum()

b = a.miss_now()

for x in b:
    print(x)
