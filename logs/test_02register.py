"""
    ============
    Author:hw
    data:2020/10/28 17:39
    ============
"""
import unittest
import os
from common.handle_excel import Excel
from common import myddt
from common.handle_log import Log
from common.handle_path import DATA_DIR,CONF_DIR
import requests
import random
import json
from common.handle_conf import Conf
from common.handle_db1 import Db
sh=Excel(os.path.join(DATA_DIR,"case.xlsx"),"register")
sh.open()
case_data=sh.read_excel()
log=Log.create_log()
conf=Conf(os.path.join(CONF_DIR,"conf.ini"))
@myddt.ddt
class TestRegister(unittest.TestCase):

    @myddt.data(*case_data)
    def test_register(self,item):
        if "#mobile_phone#" in item["params"]:
            self.mobile_id=self.random_phone()
            item["params"]=item["params"].replace("#mobile_phone#",str(self.mobile_id))
        params=eval(item["params"])
        url=conf.get("api","baseUrl")+item["url"]
        expected=eval(item["expected"])
        headers=eval(conf.get("api","headers"))
        resp=requests.post(url=url,json=params,headers=headers)
        res1=json.loads(resp.text)
        print(type(res1))
        res2={}
        res2["code"]=res1["code"]
        res2["msg"]=res1["msg"]

        print(res2)
        try:
            self.assertEqual(res2,expected)
        except AssertionError as e:
            log.error("{}用例不通过".format(item["title"]))
            sh.write_excel(item["case_id"]+1,8,"执行不通过")

            raise e
        else:
            log.info("{}用例通过".format(item["title"]))
            sh.write_excel(item["case_id"]+1, 8, "执行通过")
    @staticmethod
    def random_phone():
        db = Db()
        db.connect()
        # while True:
        #     mobile_id = random.randint(13000000000, 13099999999)
        #     sql = db.find_data("select * from member where mobile_phone={}".format(mobile_id))
        #     if not sql:
        #         return mobile_id
        sql=True
        while sql:
            mobile_id = random.randint(13000000000, 13099999999)
            sql = db.find_data("select * from member where mobile_phone={}".format(mobile_id))
            if not sql:
                return mobile_id

if __name__=="__main__":
    unittest.main()
