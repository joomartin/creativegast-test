
import HTMLTestRunner
import os
import unittest
from selenium import webdriver
#from Teszt.UnitTestCase1 import Test
from Teszt.UnitTestCase2 import Test2
from TestCase1.Raktarak import Test

dir = os.getcwd()
driver = webdriver

# get all tests from SearchText and HomePageTest class
raktarak = unittest.TestLoader().loadTestsFromTestCase(Test)
#test1 = unittest.TestLoader().loadTestsFromTestCase(Test)
#test2 = unittest.TestLoader().loadTestsFromTestCase(Test2)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([raktarak])

# run the suite
#unittest.TextTestRunner(verbosity=2).run(test_suite)

# open the report file
outfile = open(dir + "\SeleniumPythonTestSummary.html", "w")

# configure HTMLTestRunner options
runner = HTMLTestRunner.HTMLTestRunner(stream=outfile,title='Test Report', description='Acceptance Tests')

# run the suite using HTMLTestRunner
runner.run(test_suite)


