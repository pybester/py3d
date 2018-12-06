"""
网络爬虫类库
"""

import os
import datetime
import time
import pickle
import sqlite3

import requests
from pyquery import PyQuery as pq

from config import SpiderConfig as cfg

################################################################################
class SpiderException(Exception):
    """爬虫异常类"""
    pass

################################################################################
class Spider_cjcp(object):
    """
    彩经网3d开奖数据爬虫

    """
    # 配置字典
    config = {}
    # 本地最新ID
    local_latest_id = 0
    # 网站最新ID
    web_latest_id = 0
    # 最后一次抓取的数据
    last_get_data = []
    # 最小ID
    minid = 2002001
    # 最大ID
    maxid = int(str(time.localtime()[0])+"360")

    ############################################################
    def __init__(self):
        """构造函数"""
        # 配置
        self.config = cfg["cjcp"]
        # 本地最新ID
        self.local_latest_id = self.__local_latest_id()
        # 网上最新ID
        self.web_latest_id = self.__web_latest_id()
        # 自动抓取最新数据
        if(self.config["isautoupdate"]):
            self.update()

    ############################################################
    def get(self, urls=None, ids=None, year=None):
        """
        批量获取网址数据

        根据条件生成总的网址列表

        [urls=str,list,tuple]:网址或网址列表
        [ids=int,range,list,tuple]:期数或期数列表，转化为网址列表
        [year=int]:调用配置中心的年份，转化为年份网址列表

        [return:list]:[{},{},{}]
        """

        # 返回列表
        result = []

        # 总的网址列表
        urllist = []

        # 判断参数urls,并将网址赋值到urllist
        if(isinstance(urls, str) and urls):
            urllist.append(urls)
        elif(isinstance(urls, list) and urls):
            urllist = urls
        elif(isinstance(urls, tuple) and urls):
            urllist = list(urls)

        # 判断参数ids，并根据id转化为网址添加到urllist
        if(isinstance(ids, int) and self.__is_valid_id(ids)):
            urllist = urllist+self.__id_to_url(ids)
        elif(isinstance(ids, (list, tuple, range)) and ids):
            urllist = urllist+self.__id_to_url(ids)

        # 判断年份,生成年份网址列表，添加到urllist
        if(isinstance(year, int) and year in self.config["idyear"].keys()):
            tmplist = list(
                range(self.config["idyear"][year][0], self.config["idyear"][year][1]))
            urllist = urllist+self.__id_to_url(tmplist)

        # 如果为空网址列表，则返回空列表
        if(not urllist):
            return result

        for url in urllist:
            if(isinstance(url, str) and url):
                try:
                    # 如果抓取到数据则添加到返回列表
                    tmpdata = self.__get_one_page(url)
                    if(tmpdata):
                        result.append(tmpdata)
                    else:
                        continue
                except:
                    continue
            else:
                continue

        # 最后一次获取的数据列表
        self.last_get_data = result

        return result

    ############################################################
    def save(self, data, pkfile=None):
        """
        保存数据

        [data=list]
        [pkfile=str]

        [return=None]
        """
        if(not isinstance(data, list) or not data):
            raise SpiderException("数据不能为空")

        # 保存为pickle文件
        if(isinstance(pkfile, str) and pkfile):
            tmpfile = self.config["pickle"]["dbpath"]+pkfile
            fw = open(tmpfile, "wb")
            pickle.dump(data, fw)
            fw.close()
            print("数据成功保存到["+tmpfile+"]")
        # 保存到sqlite数据库
        else:
            conn = sqlite3.connect(self.config["sqlite"]["dbfile"])
            cursor = conn.cursor()
            for row in data:
                kjnum = ",".join(map(str, row["kjnum"]))
                sjnum = ",".join(map(str, row["sjnum"]))
                try:
                    cursor.execute("insert into "+self.config["sqlite"]["dbtable"]+" (id,kjnum,sjnum,kjdate,sales,zhixuan,zusan,zuliu) values ("+str(
                        row['id'])+",'"+kjnum+"','"+sjnum+"','"+row['date']+"',"+str(row['sales'])+","+str(row['zhixuan'])+","+str(row['zusan'])+","+str(row['zuliu'])+")")
                except:
                    continue
            conn.commit()
            cursor.close()
            conn.close()

            print(str(len(data))+" 条数据成功被保存!\n 数据库:["+self.config["sqlite"]
                  ["dbfile"]+"] \n 表:["+self.config["sqlite"]["dbtable"]+"]")

    ############################################################
    def update(self):
        """
        自动抓取最新数据
        """
        if(self.web_latest_id-self.local_latest_id < 100 and self.web_latest_id-self.local_latest_id > 0):
            idrange = range(self.local_latest_id+1, self.web_latest_id+1)
            data = self.get(ids=idrange)
            self.save(data)

            try:
                os.remove(self.config["pickle"]["dbpath"]+"latest_id\\local-" +
                          datetime.datetime.now().strftime("%Y-%m-%d")+".pk")
                os.remove(self.config["pickle"]["dbpath"]+"latest_id\\web-" +
                          datetime.datetime.now().strftime("%Y-%m-%d")+".pk")
            except:
                pass

        return

    ############################################################
    def __get_one_page(self, url):
        """
        获取单个页面开奖数据

        [url=str]
        [return=dict]
        {
            "id":int,
            "kjnum":str,
            "sjnum":str,
            "date":str,
            "sales":int,
            "zhixuan":int,
            "zusan":int,
            "zuliu":int,
        }
        """
        # 输出结果
        result = {}

        # 是否计时
        if(self.config["istimer"]):
            starttime = time.time()

        if(isinstance(url, str) and url):
            # 页面请求
            response = requests.get(url)
            # 只有正常连接并且网址没有跳转才继续
            if(response.status_code == 200 and response.url == url):

                # 页面编码
                response.encoding = self.config['encoding']

                # 包含有效数据的Html
                html = pq(response.text)("div.public_info")

                # 期号
                idq = html("h1 em").eq(1)
                tmpid = idq.text()
                tmpid = tmpid.replace("第", "").replace("期", "").strip()
                try:
                    id = int(tmpid)
                # 期号不存在则返回空数据
                except:
                    return result

                # 开奖号码
                kjq = html("div.public_num p span")
                kjnum = []
                for x in kjq.items():
                    kjnum.append(int(x("span").text()))
                kjnum = tuple(kjnum)

                # 试机号
                sjq = html("div.public_num p em")
                sjnum = []
                for x in sjq.items():
                    sjnum.append(int(x("em").text()))
                sjnum = tuple(sjnum)

                # 开奖日期
                date = ""
                dateq = html("ul li").eq(1)
                date = dateq.text()
                date = date.replace("开奖时间：", "").replace("20:32", "").strip()

                # 销售额
                salesq = html("ul li").eq(2)
                tmpsale = salesq.text()
                tmpsale = tmpsale.replace("本期销量：", "").replace(
                    "元", "").replace(",", "").strip()
                try:
                    sales = int(tmpsale)
                except:
                    sales = 0

                # 包含有效数据的html
                html = pq(response.text)("div.public_zst")

                # 直选数
                zhixuanq = html("td").eq(1)
                try:
                    zhixuan = int(zhixuanq.text())
                except:
                    zhixuan = 0

                # 组三数
                zusanq = html("td").eq(4)
                try:
                    zusan = int(zusanq.text())
                except:
                    zusan = 0

                # 组六数
                zuliuq = html("td").eq(7)
                try:
                    zuliu = int(zuliuq.text())
                except:
                    zuliu = 0

                # 返回的数据字典
                result["id"] = id
                result["kjnum"] = kjnum
                result["sjnum"] = sjnum
                result["date"] = date
                result["sales"] = sales
                result["zhixuan"] = zhixuan
                result["zusan"] = zusan
                result["zuliu"] = zuliu

                # 是否计时以及打印数据
                if(self.config["istimer"]):
                    endtime = time.time()
                    usetime = endtime-starttime
                    print(url+"   ====>  " + format(usetime, "0.4f") + "s")
                    if(self.config["isprint"]):
                        print(result)
                else:
                    print(url)
                    if(self.config["isprint"]):
                        print(result)

        return result

    ############################################################
    def __url_to_id(self, url):
        """
        根据网址获取期数
        将网址公共部分替换掉，就剩下期数

        [url=str]
        [return=int]

        """
        result = 0
        rstr = self.config["baseurl"].split('{id}')
        if(isinstance(url, str) and url):
            idstr = url.replace(rstr[0], "").replace(rstr[1], "")
            try:
                result = int(idstr)
            except:
                return result
        else:
            return result
        return result

    ############################################################
    def __id_to_url(self, ids):
        """
        根据期数获取网址
        将基准网址中的占位符替换为期数

        [ids=int,list,range,tuple]
        [return=list]
        """

        # 返回列表
        result = []

        # 期数列表
        idlist = []

        # 根据参数获取期数列表
        if(isinstance(ids, int)):
            idlist.append(ids)
        elif(isinstance(ids, list)):
            idlist = ids
        elif(isinstance(ids, (range, tuple))):
            idlist = list(ids)

        # 如何列表不为空就将符合条件的期数转化为网址
        if(idlist):
            for id in idlist:
                if(self.__is_valid_id(id)):
                    result.append(
                        self.config["baseurl"].replace("{id}", str(id)))
                else:
                    continue
            return result
        else:
            return result

    ############################################################
    def __is_valid_id(self, id):
        """
        判断是否是有效的ID

        [id=int]:最小值为minid,最大值为maxid；后三位数字在0-360之间
        [return=bool]

        """
        if(isinstance(id, int)):
            # 在最小与最大值之间
            if(id >= self.minid and id <= self.maxid):
                # 后三位在1~360之间
                tmpid = int(str(id)[-3:])
                if(tmpid >= 1 and tmpid <= 360):
                    return True
                else:
                    return False
            else:
                return False
        # 非数字类型先试着转换为数字类型，在执行本函数
        else:
            try:
                tmpid = int(id)
                return self.__is_valid_id(tmpid)
            except:
                return False

    ############################################################
    def __local_latest_id(self):
        """
        数据库中最新期数

        先看本地是否有保存，有就直接读取，没有就从数据库中获取；
        本地文件按日期生成，每天最多从数据库只获取一次数据 

        [return=int]      
        """

        # 返回数字
        result = 0

        # 保存数据库最新期数的文件
        idfile = self.config["pickle"]["dbpath"]+"latest_id\\local-" + \
            datetime.datetime.now().strftime("%Y-%m-%d")+".pk"

        # 如果本地文件存在就从本地文件读取
        if(os.path.isfile(idfile)):
            fr = open(idfile, "rb")
            result = pickle.load(fr)
            fr.close()
        # 如果本地文件不存在，就从数据库获取，并保存到本地
        else:
            # sql语句
            sql_code = "select id from " + \
                self.config["sqlite"]["dbtable"] + " order by id desc limit 1"

            # 连接数据库获取数据
            conn = sqlite3.connect(self.config["sqlite"]["dbfile"])
            cursor = conn.cursor()
            cursor.execute(sql_code)
            result = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            # 保存数据到本地
            fw = open(idfile, "wb")
            pickle.dump(result, fw)
            fw.close()

        return result

    ############################################################
    def __web_latest_id(self):
        """
        获取网上最新期数

        先看本地是否有保存，有就直接读取，没有就从网上获取；
        本地文件按日期生成，每天最多从网上只获取一次数据

        [return=int]
        """
        # 返回数字
        result = 0

        # 保存网上最新期数的文件，
        idfile = self.config["pickle"]["dbpath"]+"latest_id\\web-" + \
            datetime.datetime.now().strftime("%Y-%m-%d")+".pk"

        # 如果本地文件存在就从本地文件读取
        if(os.path.isfile(idfile)):
            fr = open(idfile, "rb")
            result = pickle.load(fr)
            fr.close()
        # 如果本地文件不存在，就从网上获取，并保存到本地
        else:
            # 获取数据的网址
            url = self.config["homeurl"]
            # 发送请求
            response = requests.get(url)
            # 如果连接正常且没有跳转则可以获取数据
            if(response.status_code == 200 and response.url == url):
                # 页面编码
                response.encoding = self.config["encoding"]
                html = pq(response.text)("div.kj_num")
                idq = html("h1 em").eq(1)
                tmpid = idq.text()
                tmpid = tmpid.replace("第", "").replace("期", "").strip()
                try:
                    result = int(tmpid)
                except:
                    raise SpiderException("网址无法收集到有效数据：["+url+"]")
            else:
                raise SpiderException("网址无效：["+url+"]")

            # 保存到本地
            fw = open(idfile, "wb")
            pickle.dump(result, fw)
            fw.close()

        return result
