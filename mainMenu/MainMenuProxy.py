
class MainMenuProxy:

    def __init__(self, driver):
        self.driver = driver

    def openRestaurant(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[1] / span").click()

    def openProducts(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[2] / span").click()

    def openStocks(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[3] / span").click()

    def openReceiving(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[4] / span").click()

    def openStatistics(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[5] / span").click()

    def openProduction(self):
        self.driver.find_element_by_xpath("/ html / body / section / div / a[6] / span").click()

