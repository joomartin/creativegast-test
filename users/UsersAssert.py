import unittest

from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy


class UserAssert(unittest.TestCase):

    def __init__(self, htmlProxy, driver):
        super().__init__()
        self.html = htmlProxy
        self.menu = MainMenuProxy(driver)
















