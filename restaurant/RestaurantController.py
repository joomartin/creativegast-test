import HTMLTestRunner
import os
import unittest

from selenium import webdriver
from core.contracts.Controller import Controller
from stock.Warehouses import Test
from restaurant.TableMapEdit import TableMapEdit
import ReportMail as mail

class RestaurantController(Controller):
    def run(self):
        dir = os.getcwd()
        driver = webdriver
        # get all tests from SearchText and HomePageTest class
        tableMap = unittest.TestLoader().loadTestsFromTestCase(TableMapEdit)

        # create a test suite combining search_text and home_page_test
        test_suite = unittest.TestSuite([tableMap])


        # open the report file
        outfile = open(dir + "\\reports\RestaurantTestReport.html", "w")

        # configure HTMLTestRunner options
        runner = HTMLTestRunner.HTMLTestRunner(stream=outfile, title='Restaurant Test Report', description='Acceptance Tests')

        # run the suite using HTMLTestRunner
        runner.run(test_suite)
        #mail.sendReport(dir + '\\reports\RestaurantTestReportTestReport.html')