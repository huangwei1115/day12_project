import re
def replace_data(cls,data):
    #部分用例实现失败，因为调用此方法就会走下面三步，会出错
    # rep_data=re.search("#(.+?)#",data)
    # rep=rep_data.group()
    # key=rep_data.group(1)
    # if rep in data:
    #     value=getattr(cls,key)
    #     data = data.replace(rep, str(value))
    # return data
    while re.search("#(.+?)#",data):
        rep_data=re.search("#(.+?)#",data)
        rep=rep_data.group()
        key=rep_data.group(1)
        value=getattr(cls,key)
        data = data.replace(rep, str(value))
    return data