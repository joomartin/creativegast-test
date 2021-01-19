from core.HtmlProxy import HtmlProxy
from Config import read_section


class MainMenuProxy:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        config = read_section()
        self.baseUrl = (config.get('path'))

    def openRestaurant(self):
        self.navigate('restaurant/index')
        self.wait()

    def openProducts(self):
        self.navigate('products')
        self.wait()

    def openStocks(self):
        self.navigate('warehouse')
        self.wait()

    def openReceiving(self):
        self.navigate('receiving')
        self.wait()

    def openStatistics(self):
        self.navigate('statistics/itemsale')
        self.wait()

    def openProduction(self):
        self.navigate('conveniences')
        self.wait()

    def openTableMapEditor(self):
        self.navigate('tablemapeditor/index')
        self.wait()

    def wait(self):
        self.html.wait()

    def navigate(self, destination):
        self.driver.get(self.baseUrl + '/' + destination)


