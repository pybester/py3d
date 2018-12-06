"""
数据处理类库
"""

import os
import pickle
import sqlite3

from config import DataConfig as cfg 

################################################################################
class DataException(Exception):
    """数据异常处理"""
    pass

################################################################################
class Data(object):
    """Sqlite数据库操作基类"""

    #sqlite数据库文件
    dbfile=""
    #执行过的sql语句
    sqllist=[]

    ############################################################
    def __init__(self,dbfile=None):
        """构造函数"""
        #设置Sqlite数据库文件
        if(isinstance(dbfile,str) and os.path.isfile(dbfile)):
            self.dbfile=dbfile
        else:
            self.dbfile=cfg["sqlite"]["dbfile"]

    ############################################################
    def get(self,sql):
        """
        执行Select语句，获取数据列表

        [sql=str,dict]
        [return=list]
        """
        #返回结果
        result=[]

        #设置操作类型为"select"
        if(isinstance(sql,dict)):
            sql["type"]="select"

        #将参数转化为SQL语句
        sqlcode=self.__dict_to_sql(sql)

        #如果SQL语句为空则输出异常
        if(not sqlcode):
            raise DataException(str(sql)+"无法转换为有效的SQL语句")
        
        #执行SQL语句，如果无法执行则输出异常
        try:
            conn=sqlite3.connect(self.dbfile)
            cursor=conn.cursor()
            cursor.execute(sqlcode)
            result=cursor.fetchall()
            cursor.close()
            conn.close()
        except:
            raise DataException("SQL语句执行错误["+sqlcode+"]")

        #返回结果
        return result
        
    ############################################################
    def exec(self,sql):
        """
        执行Insert,Update,Delete等SQL语句

        [sql=str,dict]
        [return=bool]
        """
        #将参数转化为SQL语句
        sqlcode=self.__dict_to_sql(sql)

        #如果SQL语句为空则输出异常
        if(not sqlcode):
            raise DataException(str(sql)+"无法转换为有效的SQL语句")

        #执行语句，如果无法执行则输出异常
        try:
            conn=sqlite3.connect(self.dbfile)
            cursor=conn.cursor()
            cursor.execute(sqlcode)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except:
            raise DataException("SQL语句执行错误["+sqlcode+"]")

    ############################################################
    def __dict_to_sql(self,sqldict):
        """
        根据参数生成SQL语句

        [sqldict=str,dict]:如何为字符串则直接判定为SQL语句，如果为字典则根据条件转化为SQL语句

        [return=str]
        """
        #sql语句
        sqlcode=""

        #操作类型
        sqltype=""

        #操作类型列表
        sqltypelist=["insert","update","delete","select"]

        #如果sqldict为字符串，则默认为sql语句
        if(isinstance(sqldict,str) and sqldict):
            sqlcode=sqldict
        #如果sqldict为字典类型，将键值转化为SQL语句
        elif(isinstance(sqldict,dict) and sqldict):

            #数据表
            if("table" in sqldict.keys() and isinstance(sqldict["table"],str) and sqldict["table"]):
                table=sqldict["table"]
            else:
                raise DataException("参数[sqldict]必须包含[table]键") 

            #SQL操作类型
            if("type" in sqldict.keys() and sqldict["type"] in sqltypelist):
                sqltype=sqldict["type"]
            else:
                raise DataException("参数[sqldict]必须包含[type]键") 

            #删除语句
            #DELETE FROM TABLE WHERE id=9
            if(sqltype=="delete"):
                sqlcode="DELETE FROM "+table+" "
                if("where" in sqldict.keys() and isinstance(sqldict["where"],str) and sqldict["where"]):
                    sqlcode=sqlcode+" WHERE "+sqldict["where"]
                    
            #更新修改语句
            #UPDATE TABLE SET field1=value1,field2=value2 where id=9
            elif(sqltype=="update"):
                sqlcode="UPDATE "+table+" SET "
                if("fields" in sqldict.keys() and sqldict["fields"]):
                    fields=sqldict["fields"]
                    if(isinstance(fields,str)):
                        sqlcode=sqlcode+fields
                    elif(isinstance(fields,(list,tuple))):
                        sqlcode=sqlcode+",".join(fields)
                    elif(isinstance(fields,dict)):
                        tmplist=[]
                        for k,v in fields.items():
                            if(isinstance(v,str)):
                                tmplist.append(k+"="+"'"+v+"'")
                            elif(isinstance(v,(int,float))):
                                tmplist.append(k+"="+str(v))
                            else:
                                tmplist.append(k+"="+"'"+str(v)+"'")
                        sqlcode=sqlcode+",".join(tmplist)
                    else:
                        raise DataException("参数[sqldict]中必须有[fields]键，且该键必须可转化")
                else:
                    raise DataException("参数[sqldict]中必须有[fields]键，且该键必须可转化")

                if("where" in sqldict.keys() and isinstance(sqldict["where"],str) and sqldict["where"]):
                    sqlcode=sqlcode+" WHERE "+sqldict["where"]
            
            #插入语句
            #INSERT INTO TABLE (field1,field2,field3...) VALUES (value1,value2,value3...)
            elif(sqltype=="insert"):
                sqlcode="INSERT INTO "+table+" "
                if("fields" in sqldict.keys() and sqldict["fields"]):
                    fields=sqldict["fields"]
                    if(isinstance(fields,str)):
                        sqlcode=sqlcode+" VALUES ("+fields+")"
                    elif(isinstance(fields,(list,tuple))):
                        sqlcode=sqlcode+" VALUES ("+",".join(fields)+")"
                    elif(isinstance(fields,dict)):
                        keys=fields.keys()
                        vals=[]
                        for v in fields.values():
                            if(isinstance(v,str)):
                                vals.append("'"+v+"'")
                            elif(isinstance(v,(int,float))):
                                vals.append(str(v))
                            else:
                                vals.append("'"+str(v)+"'")
                        sqlcode=sqlcode+" ("+",".join(keys)+") VALUES ("+",".join(vals)+")"
                    
                    else:
                        raise DataException("参数[sqldict]中必须有[fields]键，且该键必须可转化")               
                else:
                    raise DataException("参数[sqldict]中必须有[fields]键，且该键必须可转化")

            #获取数据
            #SELECT field1,field2... FROM TABLE WHERE ID=1
            elif(sqltype=="select"):
                sqlcode="SELECT "
                if("fields" in sqldict.keys() and sqldict["fields"]):
                    fields=sqldict["fields"]
                    if(isinstance(fields,str)):
                        sqlcode=sqlcode+" "+fields
                    elif(isinstance(fields,(list,tuple))):
                        sqlcode=sqlcode+" "+",".join(fields)
                    else:
                        sqlcode=sqlcode+" * "
                else:
                    sqlcode=sqlcode+" * "
                
                sqlcode=sqlcode+" FROM "+table

                if("where" in sqldict.keys() and isinstance(sqldict["where"],str) and sqldict["where"]):
                    sqlcode=sqlcode+" WHERE "+sqldict["where"]
                
                if("order" in sqldict.keys() and isinstance(sqldict["order"],str) and sqldict["order"]):
                    sqlcode=sqlcode+" ORDER BY "+sqldict["order"]

                if("limit" in sqldict.keys() and isinstance(sqldict["limit"],int) and sqldict["limit"]>0):
                    sqlcode=sqlcode+" LIMIT "+str(sqldict["limit"])
                            
            
        #将语句加入到sqllist
        if(isinstance(sqlcode,str) and sqlcode):
            self.sqllist.append(sqlcode)

        return sqlcode


################################################################################
class Data_kaijiang(Data):
    """开奖数据处理类"""

    #表名
    table="kaijiang"
    #操作类别
    sqltype="select"
    #pickle文件保存路径
    pkpath=cfg["pickle"]["dbpath"]+"kaijiang\\"

    ############################################################
    def __init__(self):
        """构造函数"""
        #初始化父类
        Data.__init__(self)

    ############################################################
    def __save_pickle(self,data,pkfile=None):
        if(isinstance(pkfile,str) and pkfile and data):
            fw=open(self.pkpath+pkfile,"wb")
            pickle.dump(data,fw)
            fw.close()

    ############################################################
    def all_dict(self,pkfile=None):
        """
        获取所有数据，每行数据以Dict形式输出

        [pkfile=str]:填写则保存，不填写则不保存
        [return=list]
        """

        #结果列表
        result=[]

        #SQL语句转换参数
        sqldict={"table":self.table,"type":self.sqltype,"order":"id asc"}

        #调用父类函数获取数据
        tmplist=self.get(sqldict)

        #将数据转化为字典格式
        for row in tmplist:
            tmpdict={}
            tmpdict["id"]=row[0]
            tmpdict["kjnum"]=tuple(map(int,row[1].split(",")))
            tmpdict["sjnum"]=tuple(map(int,row[2].split(",")))
            tmpdict["kjdate"]=row[3]
            tmpdict["sales"]=row[4]
            tmpdict["zhixuan"]=row[5]
            tmpdict["zusan"]=row[6]
            tmpdict["zuliu"]=row[7]
            result.append(tmpdict)

        #将数据保存到pickle文件中
        self.__save_pickle(result,pkfile)

        #返回结果
        return result    

    ############################################################
    def all_list(self,pkfile=None):
        """
        获取所有数据，每行数据以tuple形式输出

        [pkfile=str]:填写则保存，不填写则不保存
        [return=list]
        """

        #结果列表
        result=[]

        #SQL语句转换参数
        sqldict={"table":self.table,"type":self.sqltype,"order":"id asc"}

        #调用父类函数获取数据
        tmplist=self.get(sqldict)

        #将数据转化为字典格式
        for row in tmplist:
            tmptuple=(row[0],tuple(map(int,row[1].split(","))),tuple(map(int,row[2].split(","))),row[3],row[4],row[5],row[6],row[7])
            result.append(tmptuple)

        #将结果保存到pickle文件中
        self.__save_pickle(result,pkfile)

        #返回结果
        return result   

    ############################################################
    def kjnum(self,pkfile=None):
        """
        获取开奖字段所有数据，每行以tuple形式输出
        
        [pkfile=str]:填写则保存，不填写则不保存
        [return=list]
        """

        #结果列表
        result=[]

        #SQL语句转换参数
        sqldict={"table":self.table,"type":self.sqltype,"fields":"kjnum","order":"id asc"}

        #调用父类函数获取数据
        tmplist=self.get(sqldict)

        #将数据转化为字典格式
        for row in tmplist:
            result.append(tuple(map(int,row[0].split(","))))

        #将结果保存到pickle文件中
        self.__save_pickle(result,pkfile)

        #返回结果
        return result  

    ############################################################
    def sjnum(self,pkfile=None):
        """
        获取试机号字段所有数据，每行以tuple形式输出
        
        [pkfile=str]:填写则保存，不填写则不保存
        [return=list]
        """

        #结果列表
        result=[]

        #SQL语句转换参数
        sqldict={"table":self.table,"type":self.sqltype,"fields":"sjnum","order":"id asc"}

        #调用父类函数获取数据
        tmplist=self.get(sqldict)

        #将数据转化为字典格式
        for row in tmplist:
            result.append(tuple(map(int,row[0].split(","))))

        #将结果保存到pickle文件中
        self.__save_pickle(result,pkfile)

        #返回结果
        return result  

