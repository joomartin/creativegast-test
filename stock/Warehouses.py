from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest
from core.HtmlProxy import HtmlProxy
from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy
from Config import read_section


class Test(unittest.TestCase):
    def createWarehouse(self, warehouseName):
        self.html.clickElement('Új raktár felvitele', 'a')
        self.html.switchFrame("iframe")

        self.html.fillInput('Raktár neve', warehouseName)
        self.html.clickElement("Rögzít")
        self.html.switchFrame()
        self.html.refresh()

    def deleteWarehouse(self, warehouseName):
        self.html.wait(2)
        self.html.clickElement(warehouseName, 'td[@class="sorting_1"]', Options(following='a'))
        self.html.clickElement('Igen')

    @classmethod
    def setUpClass(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--auto-open-devtools-for-tabs')
        self.driver = webdriver.Chrome(executable_path='C:\Webdrivers/chromedriver.exe')
        self.driver.maximize_window()

        config = read_section('creative-gast')
        self.driver.get(config.get('path'))

        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)

        self.html.fillInput('Felhasználónév', 'admin', selector='placeholder')
        self.html.fillInput('Jelszó', 'admin', selector='placeholder')

        self.html.clickElement('Belépés')
        self.html.fillInput('Belépési kód', 'admin', selector='placeholder')
        self.html.clickElement('Belépés')

        self.menu.openStocks()
        self.html.clickElement('Raktárak', 'a')

    def testCreateWarehouse(self):
        self.createWarehouse("1newWH")
        self.assertTrue(self.html.getElementInTable("1newWH", "sorting_1").is_displayed())
        self.deleteWarehouse("1newWH")

    def testCantCreate(self):
        self.createWarehouse("2newWH")
        self.html.clickElement('Új raktár felvitele', 'a')
        self.html.switchFrame("iframe")

        self.html.fillInput('Raktár neve', '2newWH', )
        self.html.clickElement("Rögzít")
        self.assertTrue(self.html.getElement('iframe', 'body', Options(htmlAttribute='class')).is_displayed())

        self.html.clearInput('Raktár neve')
        self.html.clickElement("Mégsem")

        self.deleteWarehouse("2newWH")

    def testEdit(self):
        self.createWarehouse("3newWH")
        self.html.clickElement(None,
                               "//tr[contains(., '3newWH')]//a[contains(@class, 'edit') and contains(@class, 'actionButton')]",
                               Options(uniqueSelector=True))

        self.html.switchFrame("iframe")
        self.html.fillInput('Raktár neve', '33newWH')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()

        self.assertTrue(self.html.getElementInTable('33newWH', 'sorting_1').is_displayed())

        self.deleteWarehouse("33newWH")

    def testDelete(self):
        self.createWarehouse("4newWH")
        self.html.clickElement('4newWH', 'td[@class="sorting_1"]', Options(following='a'))
        self.html.clickElement("Igen", waitSeconds=2)

        with self.assertRaises(NoSuchElementException):
            self.html.getElementInTable("4newWH", "sorting_1")

    @classmethod
    def tearDownClass(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
