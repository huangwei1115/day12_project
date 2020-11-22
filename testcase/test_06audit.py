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
sh=Excel(os.path.join(DATA_DIR,"case.xlsx"),"loanaudit")
sh.open()
case_data=sh.read_excel()
log=Log.create_log()
@myddt.ddt
class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #管理员账户登录并新增项目
        url=conf.get("api","baseUrl")+"/member/login"
        params={"mobile_phone":conf.get("testdata","admin_mobile"),"pwd":conf.get("testdata","admin_pwd")}
        headers=eval(conf.get("api","headers"))
        response=requests.post(url=url,json=params,headers=headers)
        res=response.text
        token=jsonpath.jsonpath(eval(res),"$..token")[0]
        cls.token_result="Bearer"+" "+token
        cls.invest_member_id = jsonpath.jsonpath(eval(res), "$..id")[0]
        add_loan_url = conf.get("api", "baseUrl") + "/loan/add"
        params = {"member_id":cls.invest_member_id,"title":"按月借贷项目","amount":1100000,"loan_rate":16.5,"loan_term":10,"loan_date_type":1,"bidding_days":8}
        headers["Authorization"] = cls.token_result
        response = requests.post(url=add_loan_url, json=params, headers=headers)
        cls.loan_id=jsonpath.jsonpath(response.json(),"$..id")[0]
        cls.pass_loan_id=cls.loan_id
    @myddt.data(*case_data)
    def test_loan_add(self,item):
        rep=replace_data(TestAudit,item["params"])
        print(rep)
        params=eval(rep)
        expected=eval(item["expected"])
        url=conf.get("api","baseUrl")+item["url"]
        headers=eval(conf.get("api","headers"))
        headers["Authorization"]=self.token_result
        response=requests.patch(url=url,json=params,headers=headers)
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
                sql = db.find_data(item["check_sql"].format(self.loan_id))[0]
                self.assertEqual(2,sql["status"])
        except AssertionError as e:
            log.error("{}用例执行失败".format(item["title"]))
            sh.write_excel(item["case_id"] + 1, 8, "执行不通过")
            raise e
        else:
            log.info("{}用例执行通过".format(item["title"]))
            sh.write_excel(item["case_id"] + 1, 8, "执行通过")
if __name__=="__main__":
    unittest.main()












