
import HTMLTestRunner
import os
import unittest
from selenium import webdriver

from core.Options import Options
from stock.StockController import StockController
from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy

sc = StockController()
sc.run()
