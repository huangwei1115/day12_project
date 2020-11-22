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
from common.handle_replacedata import replace_data
sh=Excel(os.path.join(DATA_DIR,"case.xlsx"),"loanadd")
sh.open()
case_data=sh.read_excel()
log=Log.create_log()
@myddt.ddt
class TestLoanAdd(unittest.TestCase):
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
    def test_loan_add(self,item):
        # if "#member_id#" in item["params"]:
        #     item["params"]=item["params"].replace("#member_id#",str(self.member_id))
        rep=replace_data(TestLoanAdd,item["params"])
        print(rep)
        params=eval(rep)
        expected=eval(item["expected"])
        url=conf.get("api","baseUrl")+item["url"]
        headers=eval(conf.get("api","headers"))
        headers["Authorization"]=self.token_result
        response=requests.post(url=url,json=params,headers=headers)
        res=response.json()
        print("预期结果为{}".format(expected))
        print("实际结果为{}".format(res))
        try:
            self.assertEqual(res["code"],expected["code"])
            self.assertEqual(res["msg"],expected["msg"])
            # if item["check_sql"]:
            #     loan_id = jsonpath.jsonpath(res, "$..id")[0]
            #     sql = db.find_data(item["check_sql"].format(loan_id))
            #     self.assertTrue(sql)
            if item["check_sql"]:
                loan_id = jsonpath.jsonpath(res, "$..id")[0]
                sql = db.find_data(item["check_sql"].format(loan_id))[0]
                self.assertEqual(loan_id,sql["id"])
        except AssertionError as e:
            log.error("{}用例执行失败".format(item["title"]))
            sh.write_excel(item["case_id"] + 1, 8, "执行不通过")
            raise e
        else:
            log.info("{}用例执行通过".format(item["title"]))
            sh.write_excel(item["case_id"] + 1, 8, "执行通过")
if __name__=="__main__":
    unittest.main()












