import HTMLTestRunner
import os
import unittest
from selenium import webdriver

from core.contracts.Controller import Controller
from products.Products import Products
from products.Menus import Menus
from products.Pizza import Pizza
import ReportMail as mail


class ProductController(Controller):
    def run(self):
        dir = os.getcwd()
        driver = webdriver
        # get all tests from SearchText and HomePageTest class
        products = unittest.TestLoader().loadTestsFromTestCase(Products)
        #productGroups = unittest.TestLoader().loadTestsFromTestCase(ProductGroups)
        menus = unittest.TestLoader().loadTestsFromTestCase(Menus)
        pizza = unittest.TestLoader().loadTestsFromTestCase(Pizza)

        # create a test suite combining search_text and home_page_test
        test_suite = unittest.TestSuite([products, menus, pizza])
        #test_suite = unittest.TestSuite([productGroups])
        #test_suite = unittest.TestSuite([menus, pizza])


        # open the report file
        #outfile = open(dir + "\\reports\ProductsTestReport.html", "w")
        with open(dir + "\\reports\ProductsTestReport.html", "w") as outfile:
            # configure HTMLTestRunner options
            runner = HTMLTestRunner.HTMLTestRunner(stream=outfile, title='Product Test Report', description='Acceptance Tests')

            # run the suite using HTMLTestRunner
            runner.run(test_suite)
        mail.sendReport(dir + '\\reports\ProductsTestReport.html')

