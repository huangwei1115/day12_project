import jsonpath
import requests
from common.handle_db import db
from common.handle_conf import conf
import random

def random_phone():
    phone="131"
    while True:
        for i in range(8):
            ran=random.randint(0,9)
            phone+=str(ran)
        if not db.find_data("select * from futureloan.member where mobile_phone={}".format(phone)):
            return phone

def register(user_conf,pwd_conf,type):
    """

    :param user_conf:保存到配置文件的配置项的用户名称
    :param pwd_conf:保存到配置文件的配置项的密码名称
    :param type:注册用户的类型，0：管理员  默认1：普通用户
    :return:
    """
    #第一步，普通账号注册账户
    register_url=conf.get("api","baseUrl")+"/member/register"
    headers=conf.get("api","headers")
    params={
        "mobile_phone":random_phone(),
        "pwd":11111111,
        "type":type
    }
    response=requests.post(url=register_url,json=params,headers=headers)
    res=response.json()
    if res["code"]==0:
        print("==============初始化注册成功===============")
        conf.write(section="testdata",option=user_conf,value=params["mobile_phone"])
        conf.write(section="testdata",option=pwd_conf,value=pwd_conf)
def login():
        #第二步登录并充值
        login_url=conf.get("api","baseUrl")+"/member/login"
        login_params={
            "mobile_phone":conf.get("testdata","mobile_phone"),
            "pwd":conf.get("testdata","pwd")
        }
        response=requests.post(url=login_url,json=login_params,headers=headers)
        if response.json()["code"]==0:
            print("登录初始成功")
            token=jsonpath.jsonpath(response.json(),"$..token")[0]
            member_id=jsonpath.jsonpath(response.json(),"$..id")[0]
            #充值500000
            recharge_url=conf.get("api","baseUrl")+"/member/recharge"
            headers["Authorization"]=token
            recharge_params={
                "member_id":member_id,
                "amount":500000
            }
            response=requests.post(url=recharge_url,params=recharge_params,headers=headers)
            if response.json()["code"]==0:
                print("==================充值500000成功==================")
                sql = "SELECT * FROM futureloan.member WHERE id={}"
                leave_amount = db.find_data(sql.format(member_id))[0]["leave_amount"]
                print("用户当前余额为{}".format(leave_amount))
            else:
                raise ValueError("普通用户初始化充值失败")
        else:
            raise ValueError("普通账号初始化登录异常")
    else:
        raise ValueError("普通账号初始化注册异常")
if __name__=="__main__":
    print(init_env_data())






