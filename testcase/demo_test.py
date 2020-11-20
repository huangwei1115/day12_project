"""
    ============
    Author:hw
    data:2020/11/10 14:56
    ============
"""
# list=[1,3,4,5,3,4,6,7,"a","b","a"]
# for i in range(len(list)):
#     for j in range(i+1,len(list)):
#         if list[i]==list[j]:
#            print(i,j)

# import requests
# url="http://api.lemonban.com/futureloan/member/register"
# params={"mobile_phone":"18309999999","pwd":"11111111"}
# headers={"X-Lemonban-Media-Type":"lemonban.v1","content-type":"application/json"}
# response=requests.post(url=url,json=params,headers=headers)
# res=response.text
# print(res,type(res))


#获取token
import os
import requests
from common.handle_conf import Conf
from common.handle_path import CONF_DIR
import jsonpath
conf=Conf(os.path.join(CONF_DIR,"conf.ini"))
url = conf.get("api", "baseUrl")+ "/member/login"
params = {"mobile_phone": conf.get("testdata", "mobile_phone"), "pwd": conf.get("testdata", "pwd")}
headers = eval(conf.get("api", "headers"))
response = requests.post(url=url, json=params, headers=headers)
res = response.text
print(res,type(res))
# token_info=jsonpath.jsonpath(eval(res),"$..token_info")
# print(type(token_info))
token=jsonpath.jsonpath(eval(res),"$..token")[0]
print(token)
token_result="Bearer"+" "+str(token)
print(token_result)
mobile_id=jsonpath.jsonpath(eval(res),"$..id")[0]
print(mobile_id)