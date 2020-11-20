"""
    ============
    Author:hw
    data:2020/10/23 16:57
    ============
"""
import unittest
from unittestreport import TestRunner
from common.handle_path import REPORT_DIR
from common.handle_path import CASE_DIR

#第一种方式，将测试类加入到测试套件中
# suite=unittest.TestSuite()
# loader=unittest.TestLoader()
# suite.addTest(loader.loadTestsFromTestCase(TestRegister))
# runner=unittest.TextTestRunner()
# runner.run(suite)
#第二种方式，将模块加入到测试套件中
# suite=unittest.TestSuite()
# loader=unittest.TestLoader()
# suite.addTest(loader.loadTestsFromModule(testcase))
# runner=unittest.TextTestRunner()
# runner.run(suite)
#第三种方式，将文件夹中的测试用例加入到测试套件中
suite=unittest.defaultTestLoader.discover(CASE_DIR)
runner=TestRunner(suite,filename="report.html",report_dir=REPORT_DIR,title="测试报告",tester="hw",desc="登录测试报告",templates=1)
runner.run()
