import HTMLTestRunner
import os
import unittest
from selenium import webdriver

from core.contracts.Controller import Controller
from receiving.Partners import Partners
from receiving.Receiving import Receiving
import ReportMail as mail


class ReceivingController(Controller):
    def run(self):
        dir = os.getcwd()
        driver = webdriver
        # get all tests from SearchText and HomePageTest class
        partners = unittest.TestLoader().loadTestsFromTestCase(Partners)
        receiving = unittest.TestLoader().loadTestsFromTestCase(Receiving)

        # create a test suite combining search_text and home_page_test
        test_suite = unittest.TestSuite([partners, receiving])
        #test_suite = unittest.TestSuite([partners])


        # open the report file
        # outfile = open(dir + "\\reports\ReceivingTestReport.html", "w")
        with open(dir + "\\reports\ReceivingTestReport.html", "w") as outfile:
            # configure HTMLTestRunner options
            runner = HTMLTestRunner.HTMLTestRunner(stream=outfile, title='Receiving Test Report', description='Acceptance Tests')

            # run the suite using HTMLTestRunner
            runner.run(test_suite)

        '''
        # alternativ megoldas
        runner = unittest.TextTestRunner()
        runner.run(test_suite)
        '''
        #outfile.close()
        mail.sendReport(dir + '\\reports\ReceivingTestReport.html')
