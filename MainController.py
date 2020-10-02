
import HTMLTestRunner
import os
import unittest
from selenium import webdriver
from stock.StockController import StockController

dir = os.getcwd()
driver = webdriver

# get all tests from SearchText and HomePageTest class
warehouses = unittest.TestLoader().loadTestsFromTestCase(Test)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([warehouses])

# run the suite
#unittest.TextTestRunner(verbosity=2).run(test_suite)

# open the report file
outfile = open(dir + "\SeleniumPythonTestSummary.html", "w")

# configure HTMLTestRunner options
runner = HTMLTestRunner.HTMLTestRunner(stream=outfile, title='Test Report', description='Acceptance Tests')

# run the suite using HTMLTestRunner
runner.run(test_suite)


