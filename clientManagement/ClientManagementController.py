import HTMLTestRunner
import os
import unittest

from core.contracts.Controller import Controller
from clientManagement.Regulars import Regulars


class ClientManagementController(Controller):

    def run(self):
        dir = os.getcwd()
        # get all tests from SearchText and HomePageTest class

        regulars = unittest.TestLoader().loadTestsFromTestCase(Regulars)

        # create a test suite combining search_text and home_page_test
        test_suite = unittest.TestSuite([regulars])


        # open the report file
        outfile = open(dir + "\\reports\ClientManagementTestReport.html", "w")

        # configure HTMLTestRunner options
        runner = HTMLTestRunner.HTMLTestRunner(stream=outfile, title='Client Management Test Report', description='Acceptance Tests')

        # run the suite using HTMLTestRunner
        runner.run(test_suite)


