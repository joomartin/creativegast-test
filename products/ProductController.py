import HTMLTestRunner
import os
import unittest
from selenium import webdriver

from core.contracts.Controller import Controller
from products.ProductGroups import ProductGroups


class ProductController(Controller):
    def run(self):
        dir = os.getcwd()
        driver = webdriver
        # get all tests from SearchText and HomePageTest class
        productGroups = unittest.TestLoader().loadTestsFromTestCase(ProductGroups)

        # create a test suite combining search_text and home_page_test
        test_suite = unittest.TestSuite([productGroups])


        # open the report file
        outfile = open(dir + "\\reports\SeleniumPythonTestSummary.html", "w")

        # configure HTMLTestRunner options
        runner = HTMLTestRunner.HTMLTestRunner(stream=outfile, title='Test Report', description='Acceptance Tests')

        # run the suite using HTMLTestRunner
        runner.run(test_suite)

