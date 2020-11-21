# import configparser
# config=configparser.ConfigParser()
# config.read(r"F:\py_learn\day07_log\conf\conf.ini")
# value=config.get("log","sh_level")
# print(value)
# class Conf:
#     def conf(self,section,key,filename):
#         self.section=section
#         self.key=key
#         self.filename=filename
#         config=configparser.ConfigParser()
#         config.read(self.filename)
#         value=config.get(self.section,self.key)
#         return value
# if __name__=='__main__':
#     section='log'
#     key='sh_level'
#     c=Conf()
#     dd=c.conf(section=section,key=key,filename=r"D:\lemon\day08_project\conf\conf.ini")
#     print(dd)
import configparser
import os
from common.handle_path import CONF_DIR
class Conf(configparser.ConfigParser):
    def __init__(self,filename,encoding="utf-8"):
        super().__init__()
        self.read(filename,encoding=encoding)
        self.filename=filename
        self.encoding=encoding
    def write_data(self,section,option,value):
        self.set(section,option,value)
        self.write(fp=open(self.filename,"w",encoding="utf-8"))
conf = Conf(os.path.join(CONF_DIR, "conf.ini"))