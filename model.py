"""
模型类库
"""

import os
import pickle

from config import ModelConfig as cfg 

################################################################################
class Kjnum():
    """开奖号码数据处理类"""

    #开奖数据列表
    kjnumlist=[]

    ############################################################
    def __init__(self):
        """构造函数"""
        fr=open(cfg["pickle"]["kjnumfile"],"rb")
        self.kjnumlist=pickle.load(fr)
        fr.close()

    ############################################################
    def repeat_count_bynum(self):
        "重复数统计,按数字分类输出"

        #结果初始化
        result={}
        for x in range(0,10):
            result[x]=[0,0,0]

        maxid=len(self.kjnumlist)-1

        #统计重复数
        for i in range(0,maxid):
            if(i+1<=maxid):
                if(self.kjnumlist[i][0]==self.kjnumlist[i+1][0]):
                    result[self.kjnumlist[i][0]][0]+=1
                if(self.kjnumlist[i][1]==self.kjnumlist[i+1][1]):
                    result[self.kjnumlist[i][0]][1]+=1
                if(self.kjnumlist[i][2]==self.kjnumlist[i+1][2]):
                    result[self.kjnumlist[i][0]][2]+=1
            else:
                break

        return result

    ############################################################
    def repeat_count_byorder(self):
        "重复数统计，按位次分类输出"

        #结果初始化
        result=[{},{},{}]
        for x in range(0,10):
            result[0][x]=0
            result[1][x]=0
            result[2][x]=0

        maxid=len(self.kjnumlist)-1

        #统计重复数
        for i in range(0,maxid):
            if(i+1<=maxid):
                if(self.kjnumlist[i][0]==self.kjnumlist[i+1][0]):
                    result[0][self.kjnumlist[i][0]]+=1
                if(self.kjnumlist[i][1]==self.kjnumlist[i+1][1]):
                    result[1][self.kjnumlist[i][0]]+=1
                if(self.kjnumlist[i][2]==self.kjnumlist[i+1][2]):
                    result[2][self.kjnumlist[i][0]]+=1
            else:
                break

        return result

    ############################################################
    def appear_count_bynum(self):
        """出现次数统计，按数字分类输出"""

        #结果初始化
        result={}
        for x in range(0,10):
            result[x]=[0,0,0]
        
        #统计出现次数
        for x in self.kjnumlist:
            result[x[0]][0]+=1
            result[x[1]][1]+=1
            result[x[2]][2]+=1

        return result

    ############################################################
    def appear_count_byorder(self):
        """出现次数统计，按位次分类输出"""

        #结果初始化
        result=[{},{},{}]
        for x in range(0,10):
            result[0][x]=0
            result[1][x]=0
            result[2][x]=0
        
        #统计出现次数
        for x in self.kjnumlist:
            result[0][x[0]]+=1
            result[1][x[1]]+=1
            result[2][x[2]]+=1

        return result

    ############################################################
    def sum_count(self):
        """和值次数统计"""

        #结果初始化
        result={}
        for x in range(0,28):
            result[x]=0
        
        for x in self.kjnumlist:
            result[sum(x)]+=1
        
        return result

    ############################################################
    def num_count(self):
        """每一个三位数出现次数统计"""
        result={}
        for x in range(0,10):
            for y in range(0,10):
                for z in range(0,10):
                    result[(x,y,z)]=0
        
        for x in self.kjnumlist:
            result[x]+=1
        
        return result

    ############################################################
    def miss_history(self):
        """历史遗漏数据统计"""

        #结果初始化
        result=[{},{},{}]
        for x in range(0,10):
            result[0][x]=[]
            result[1][x]=[]
            result[2][x]=[]
        
        maxid=len(self.kjnumlist)-1

        tmpresult=result
        for i in range(0,maxid):
            tmpresult[0][self.kjnumlist[i][0]].append(i)
            tmpresult[1][self.kjnumlist[i][1]].append(i)
            tmpresult[2][self.kjnumlist[i][2]].append(i)
        
        for x in range(0,3):
            for y in range(0,10):
                tmplist=tmpresult[x][y]
                result[x][y]=[tmplist[i+1]-tmplist[i] for i in range(len(tmplist)-1)]
        
        return result

    ############################################################
    def miss_now(self):
        """当前遗漏数据统计"""

        #结果初始化
        result=[{},{},{}]
        for x in range(0,10):
            result[0][x]=[]
            result[1][x]=[]
            result[2][x]=[]
        
        maxid=len(self.kjnumlist)

        tmpresult=result
        for i in range(0,maxid):
            tmpresult[0][self.kjnumlist[i][0]].append(i)
            tmpresult[1][self.kjnumlist[i][1]].append(i)
            tmpresult[2][self.kjnumlist[i][2]].append(i)
        
        for x in range(0,3):
            for y in range(0,10):
                tmplist=tmpresult[x][y]
                result[x][y]=maxid-tmplist[-1]-1
        
        return result


