"""
运行类库
"""
from spider import Spider_cjcp as cjcp
from data import Data_kaijiang as kj

# 更新数据


def update_data():
    a = cjcp()
    b = kj()
    b.all_dict(pkfile="all_dict.pk")
    b.all_list(pkfile="all_list.pk")
    b.kjnum(pkfile="kjnum.pk")
    b.sjnum(pkfile="sjnum.pk")


update_data()
