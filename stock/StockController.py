import HTMLTestRunner
import os
import unittest

from selenium import webdriver
from core.contracts.Controller import Controller
from stock.RawMaterial import RawMaterial
from stock.Warehouses import Test
from stock.StockMovement import StockMovement
from stock.BarCheckings import BarCheckings


class StockController(Controller):
    def run(self):
        dir = os.getcwd()
        driver = webdriver
        # get all tests from SearchText and HomePageTest class
        warehouses = unittest.TestLoader().loadTestsFromTestCase(Test)
        rawMaterial = unittest.TestLoader().loadTestsFromTestCase(RawMaterial)
        stockMovement = unittest.TestLoader().loadTestsFromTestCase(StockMovement)
        barCheckings = unittest.TestLoader().loadTestsFromTestCase(BarCheckings)

        # create a test suite combining search_text and home_page_test
        test_suite = unittest.TestSuite([warehouses, rawMaterial, stockMovement, barCheckings])


        # open the report file
        outfile = open(dir + "\\reports\StocksTestReport.html", "w")

        # configure HTMLTestRunner options
        runner = HTMLTestRunner.HTMLTestRunner(stream=outfile, title='Stock Test Report', description='Acceptance Tests')

        # run the suite using HTMLTestRunner
        runner.run(test_suite)

