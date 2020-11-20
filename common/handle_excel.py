"""
    ============
    Author:hw
    data:2020/10/27 9:34
    ============
"""
import openpyxl
class Excel:
    def __init__(self,file_name,sheet_name):
        self.file_name=file_name
        self.sheet_name=sheet_name
    def open(self):
        self.wb=openpyxl.load_workbook(self.file_name)
        self.sh=self.wb[self.sheet_name]

    def read_excel(self):
        item=list(self.sh.rows)
        """
        title=[]
        for i in item[0]:
            print(i.value)
            title.append(i.value)
        """
        #列表推导式
        title=[i.value for i in item[0]]
        case=[]
        for i in item[1:]:
            """
            data=[]
            for j in i:
                data.append(j.value)
            """
            data=[j.value for j in i]
            case.append(dict(zip(title,data)))
        return case
    def write_excel(self,row,column,value):
        self.row=row
        self.column=column
        self.value=value
        self.sh.cell(self.row,self.column,self.value)
        self.wb.save(self.file_name)
        self.wb.close()
if __name__=="__main__":
    file_name=r"D:\lemon\day09_project\test_data\case.xlsx"
    sheet_name="Sheet1"
    sh=Excel(file_name,sheet_name)
    sh.open()
    sh.write_excel(1,2,"nihao")



