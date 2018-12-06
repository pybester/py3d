"""
通用函数库
"""

import os
import random

############################################################
def rand_to_list(n, type=None, range=None):
    """
    随机三位数

    [n=int]:随机数量,默认值为1
    [type=str]:随机类型，目前只有三种"zhixuan","zusan","zuliu"
    [range=list,tuple]:随机范围,最大范围为(0,1,2,3,4,5,6,7,8,9)

    [return=list]

    """
    # 默认值
    default_range = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    default_types = ("zhixuan", "zusan", "zuliu")
    default_count = 1

    # 返回列表
    result = []

    # 判断随机个数
    if(isinstance(n, int) and n > 0):
        r_count = n
    else:
        r_count = default_count

    # 判断类型
    if(isinstance(type, str) and type in default_types):
        r_type = type
    else:
        r_type = default_types[0]  # "zhixuan"

    # 判断范围:必须为list,tuple类型;不重复的长度在4~10之间，且必须为default_range子集
    if(isinstance(range, (list, tuple)) and len(set(range)) > 3 and set(range) <= set(default_range)):
        r_range = tuple(set(range))
    else:
        r_range = default_range

    # 直选随机:每一位从范围中选取，不需要排序
    if(r_type == "zhixuan"):
        i = 0
        while i < r_count:
            i = i+1
            result.append((random.choice(r_range), random.choice(
                r_range), random.choice(r_range)))

    # 组三随机:从范围中选取二个不同的数字，每组都并从小到大排序
    elif(r_type == "zusan"):
        r_range = tuple(set(r_range))
        i = 0
        while i < r_count:
            i = i+1
            result.append(tuple(sorted(random.sample(r_range, 2))))

    # 组六随机:从范围中选取三个不同的数字，每组都并从小到大排序
    elif(r_type == "zuliu"):
        r_range = tuple(set(r_range))
        i = 0
        while i < r_count:
            i = i+1
            result.append(tuple(sorted(random.sample(r_range, 3))))

    # 返回结果
    return result


############################################################
def sum_to_list(n, type=None):
    """
    和为n的所有三位数列表

    [n=int]:和值必填，范围0~27
    [type=str]:类型，目前有四种"zhixuan","zuxuan","zusan","zuliu"

    [return=list]
    """

    # 默认值
    default_count = 0
    default_types = ("zhixuan", "zuxuan", "zusan", "zuliu")

    # 返回列表
    result = []

    # 判断n必须为数字且在0~27之间
    if(not isinstance(n, int) or n < 0 or n > 27):
        raise Exception("参数[n]必须为数字，且在0~27之间")

    # 判断类型
    if(type and type in default_types):
        s_type = type
    else:
        s_type = default_types[0]

    # 直选:和值正确的所有组合全部输出
    if(s_type == "zhixuan"):
        for x in range(0, 10):
            for y in range(0, 10):
                for z in range(0, 10):
                    if((x+y+z) == n):
                        result.append((x, y, z))
                    else:
                        continue
    # 组选:包含组三和组六,后面的数字大于等于前面的数字
    elif(s_type == "zuxuan"):
        for x in range(0, 10):
            for y in range(x, 10):
                for z in range(y, 10):
                    if((x+y+z) == n):
                        result.append((x, y, z))
                    else:
                        continue

    # 组三:有一个相同的数字，输出之前需要先排序
    elif(s_type == "zusan"):
        for x in range(0, 10):
            for y in range(x+1, 10):
                if((x+y+y) == n):
                    result.append((x, y, y))
                elif((x+x+y) == n):
                    result.append((x, x, y))
                else:
                    continue
        result = sorted(result)

    # 组六:三个数字各不相同
    elif(s_type == "zuliu"):
        for x in range(0, 10):
            for y in range(x+1, 10):
                for z in range(y+1, 10):
                    if((x+y+z) == n):
                        result.append((x, y, z))
                    else:
                        continue
    # 返回列表
    return result
