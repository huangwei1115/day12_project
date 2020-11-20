"""
    ============
    Author:hw
    data:2020/11/17 12:33
    ============
"""
import jsonpath
import requests

from common.handle_db import db
from common.handle_conf import conf
from common.handle_path import DATA_DIR
from common.handle_excel import Excel
from common import myddt
from common.handle_log import Log
import os
import unittest
sh=Excel(os.path.join(DATA_DIR,"case.xlsx"),"withdraw")
sh.open()
case_data=sh.read_excel()
log=Log.create_log()
@myddt.ddt
class TestWithdraw(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        url=conf.get("api","baseUrl")+"/member/login"
        params={"mobile_phone":conf.get("testdata","mobile_phone"),"pwd":conf.get("testdata","pwd")}
        headers=eval(conf.get("api","headers"))
        response=requests.post(url=url,json=params,headers=headers)
        res=response.text
        token=jsonpath.jsonpath(eval(res),"$..token")[0]
        cls.token_result="Bearer"+" "+token
        cls.member_id = jsonpath.jsonpath(eval(res), "$..id")[0]

    @myddt.data(*case_data)
    def test_recharge(self,item):
        if "#member_id#" in item["params"]:
            item["params"]=item["params"].replace("#member_id#",str(self.member_id))
        params=eval(item["params"])
        expected=eval(item["expected"])
        # if "#member_id#" in item["check_sql"]:
        #     item["check_sql"]=item["check_sql"].replace("#member_id#",str(self.mobile_id))
        url=conf.get("api","baseUrl")+item["url"]
        headers=eval(conf.get("api","headers"))
        headers["Authorization"]=self.token_result
        check_sql = item["check_sql"]
        if check_sql:
            check_sql_before=db.find_data(check_sql.format(self.member_id))
            print(check_sql_before,type(check_sql_before),check_sql_before[0])
            leave_amount_before=check_sql_before[0]["leave_amount"]
        response=requests.post(url=url,json=params,headers=headers)
        res=response.json()
        if check_sql:
            check_sql_after = db.find_data(check_sql.format(self.member_id))
            leave_amount_after = check_sql_after[0]["leave_amount"]
        # print(leave_amount_before,leave_amount_after,type(leave_amount_before),type(leave_amount_after))
        res2={}
        res2["code"]=res["code"]
        res2["msg"]=res["msg"]
        print("预期结果为{}".format(expected))
        print("实际结果为{}".format(res2))
        try:
            self.assertEqual(res2,expected)
            if item["check_sql"]:
                self.assertEqual(float(leave_amount_before-leave_amount_after),float(params["amount"]))

        except AssertionError as e:
            log.error("{}用例执行失败".format(item["title"]))
            sh.write_excel(item["case_id"] + 1, 8, "执行不通过")
            raise e
        else:
            log.info("{}用例执行通过".format(item["title"]))
            sh.write_excel(item["case_id"] + 1, 8, "执行通过")













