"""
配置中心
"""

################################################################################
"""数据配置"""
DataConfig={
    #sqlite数据库文件路径
    "sqlite":{
        "dbfile":"F:\\Database\\sqlite\\py3d.db",
        "dbtable":"kaijiang",
        "kaijiang":{
            "all_asc":"select * from kaijiang order by id asc",
            "all_desc":"select * from kaijiang order by id desc",
        },
    },
    #pickle文件保存路径
    "pickle":{
        "dbpath":"F:\\Database\\pickle\\py3d\\",
    },
    #mysql数据库配置
    "mysql":{},
    #microsoft sql server数据库配置
    "mssql":{},
}

################################################################################
"""模型配置"""
ModelConfig={
    "sqlite":{
        "dbfile":"F:\\Database\\sqlite\\py3d.db",
        "dbtable":"kaijiang",
    },
    "pickle":{
        "dbpath":"F:\\Database\\pickle\\py3d\\",
        "kjnumpath":"F:\\Database\\pickle\\py3d\\kjnum\\",
        "kjnumfile":"F:\\Database\\pickle\\py3d\\kaijiang\\kjnum.pk",
    },
}

################################################################################
"""运行配置"""
RunConfig={

}

################################################################################
"""爬虫配置"""
SpiderConfig={
    #财经网爬虫配置
    "cjcp":{
        #主页,可以获取最新ID
        "homeurl":"https://m.cjcp.com.cn/kaijiang/3d/",
        #基本网址，可以根据ID生成网址
        "baseurl":"https://m.cjcp.com.cn/kaijiang/3d{id}.html",
        #网页编码
        "encoding":"utf-8",
        #是否计时
        "istimer":True,
        #抓取时是否打印
        "isprint":False,
        #是否自动更新
        "isautoupdate":True,
        #保存类型
        "savetype":"sqlite",
        "sqlite":{
            "dbfile":"F:\\Database\\sqlite\\py3d.db",
            "dbtable":"kaijiang",
        },
        "pickle":{
            "dbpath":"F:\\Database\\pickle\\py3d\\",
            "dbfile":"tmp.pk",
        },
        #每年ID范围
        "idyear":{
            2002:[2002001,2002359],
            2003:[2003001,2003360],
            2004:[2004001,2004360],
            2005:[2005001,2005359],
            2006:[2006001,2006358],
            2007:[2007001,2007358],
            2008:[2008001,2008360],
            2009:[2009001,2009359],
            2010:[2010001,2010359],
            2011:[2011001,2011359],
            2012:[2012001,2012360],
            2013:[2013001,2013359],
            2014:[2014001,2014358],
            2015:[2015001,2015359],
            2016:[2016001,2016360],
            2017:[2017001,2017359],
            2018:[2018001,2018313],
        },
    },
}

################################################################################
"""统计分析配置"""
StatisConfig={

}

################################################################################
"""测试配置"""
TestConfig={

}

################################################################################
"""通用类库配置"""
UtilConfig={

}



