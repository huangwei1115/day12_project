"""
    ============
    Author:hw
    data:2020/10/28 17:36
    ============
"""
import logging
import os
from common.handle_path import LOG_DIR,CONF_DIR
from common.handle_conf import Conf
import logging.handlers
cfg=Conf(filename=os.path.join(CONF_DIR,"conf.ini"))
class Log:
    @staticmethod
    def create_log():
        #创建日志收集器
        mylog=logging.getLogger()
        mylog.setLevel(cfg.get("log","log_level"))
        print(cfg.get("log","log_level"))
        #创建渠道
        fh=logging.FileHandler(filename=os.path.join(LOG_DIR,"log.log"),encoding="utf-8")
        rh=logging.handlers.TimedRotatingFileHandler(filename=os.path.join(LOG_DIR,"log.log"),encoding="utf-8")
        fh.setLevel(cfg.get("log","log_level"))
        rh.setLevel(cfg.get("log", "log_level"))
        mylog.addHandler(rh)
        #设置输出格式
        mat=logging.Formatter("%(asctime)s-[%(filename)s--->line%(lineno)d] - %(levelname)s:%(message)s")
        fh.setFormatter(mat)
        return mylog


