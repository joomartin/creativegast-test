from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from stock.StockAssert import StockAssert


class ManufactureSeed:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.stockAssert = StockAssert(self.html, self.driver)