import HTMLTestRunner
import os
import unittest

from core.contracts.Controller import Controller
from users.Users import Users
from users.Groups import Groups
import ReportMail as mail


class UsersController(Controller):

    def run(self):
        dir = os.getcwd()
        # get all tests from SearchText and HomePageTest class

        users = unittest.TestLoader().loadTestsFromTestCase(Users)
        groups = unittest.TestLoader().loadTestsFromTestCase(Groups)
        # create a test suite combining search_text and home_page_test
        test_suite = unittest.TestSuite([users, groups])

        # open the report file
        #outfile = open(dir + "\\reports\\UsersTestReport.html", "w")
        with open(dir + '\\reports\\UsersTestReport.html', 'w') as outfile:
            # configure HTMLTestRunner options
            runner = HTMLTestRunner.HTMLTestRunner(stream=outfile, title='Users Test Report', description='Acceptance Tests')

            # run the suite using HTMLTestRunner
            runner.run(test_suite)

        mail.sendReport(dir + '\\reports\\UsersTestReport.html')

