"""
    ============
    Author:hw
    data:2020/11/10 17:27
    ============
"""
import json
import os
from common.handle_conf import conf
from common.handle_path import DATA_DIR
from common.handle_excel import Excel
from common.handle_log import Log
from common import myddt
import unittest
import requests
sh=Excel(os.path.join(DATA_DIR,"case.xlsx"),"login")
sh.open()
case_data=sh.read_excel()
log=Log.create_log()
@myddt.ddt
class TestLogin(unittest.TestCase):
    @myddt.data(*case_data)
    def test_login(self,item):
        url=conf.get("api","baseUrl")+item["url"]
        params=eval(item["params"])
        expected=eval(item["expected"])
        headers=eval(conf.get("api","headers"))
        response=requests.post(url=url,json=params,headers=headers)
        res=json.loads(response.text)
        print("预期结果为{}".format(expected))
        print("实际结果为{}".format(res))
        try:
            self.assertEqual(res["code"], expected["code"])
            self.assertEqual(res["msg"], expected["msg"])
        except AssertionError as e:
            log.error("{}用例执行失败".format(item["title"]))
            sh.write_excel(item["case_id"]+1,8,"执行不通过")
            raise e
        else:
            log.info("{}用例执行通过".format(item["title"]))
            sh.write_excel(item["case_id"]+1,8,"执行通过")






