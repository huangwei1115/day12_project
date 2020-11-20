"""
    ============
    Author:hw
    data:2020/11/6 12:00
    ============
"""
import pymysql
from common.handle_conf import conf

class Db:
    def __init__(self,host,port,user,password):
        self.con=pymysql.Connect(host=host,port=port,user=user,password=password,charset="utf8",cursorclass=pymysql.cursors.DictCursor)
        self.cur=self.con.cursor()
    def find_data(self,sql):
        self.con.commit()
        self.cur.execute(sql)
        data=self.cur.fetchall()
        return data
db=Db(
    host = conf.get("mysql", "host"),
    port = conf.getint("mysql", "port"),
    user = conf.get("mysql", "user"),
    password = conf.get("mysql", "password")
)

