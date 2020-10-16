from core.HtmlProxy import HtmlProxy
class MainMenuProxy:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)

    def openRestaurant(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[1] / span").click()
        self.wait()

    def openProducts(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[2] / span").click()
        self.wait()

    def openStocks(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[3] / span").click()
        self.wait()

    def openReceiving(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[4] / span").click()
        self.wait()

    def openStatistics(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[5] / span").click()
        self.wait()

    def openProduction(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[6] / span").click()
        self.wait()

    def wait(self):
        self.html.wait()

