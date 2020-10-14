import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy


class RawMaterial(unittest.TestCase):

    def createRawMaterial(self, materialName):
        # new raw material button
        self.html.clickElement('Új nyersanyag felvitele', 'a')
        # create a raw material without an opening stock
        # switch to iframe
        sleep(1)
        self.html.switchFrame('iframe')
        # name
        self.html.fillInput('Nyersanyag neve', materialName)
        # ME
        self.html.clickDropdown('ME', 'liter')
        # Warehause
        self.html.clickDropdown('Raktár', 'Pult')

        # Save
        self.html.clickElement('Rögzít')
        # switch back to the browser
        self.html.switchFrame()
        self.driver.refresh()
        sleep(2)
        self.assertTrue(self.html.getElement(materialName, 'td').is_displayed())

    def deleteRawMaterial(self, name):
        self.html.clickElement(name, 'td', options={'following':'a'})
        sleep(2)
        self.html.clickElement('Törlés', 'a')
        self.html.clickElement('Igen')

    @classmethod
    def setUpClass(self):
        # On the virtual machines we have to add chromedriver.exe to the Path environmental variable
        test = RawMaterial()
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # waiting to server response
        self.driver.implicitly_wait(10)
        # destination URL
        self.driver.get('https://ricsi.creativegast.hu/login')

        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)

        self.html.fillInput('Felhasználónév', 'admin', 'placeholder')
        # password textfield and type 'admin'
        self.html.fillInput('Jelszó', 'admin', 'placeholder')

        # click 'Belépés' button
        self.html.clickElement('Belépés')
        # self.assertEqual(self.driver.title, 'Felhasználó váltás | CreativeGAST')

        self.html.fillInput('Belépési kód', 'admin', 'placeholder')
        self.html.clickElement('Belépés')
        self.driver.implicitly_wait(10)

        self.driver.implicitly_wait(10)
        self.menu.openStocks()

    def testCreate(self):
        # This case we simply test the process of creation
        testName = 'Abszint'
        self.createRawMaterial(testName)
        self.deleteRawMaterial(testName)

    def testUpdate(self):
        # here we test the update of a raw material
        testName = 'Abszint'
        price = '1 010.00'
        self.createRawMaterial(testName)
        self.html.clickElement(testName, 'td', options={'following':'a'})
        #self.html.getElementByClassName('edit').click()
        self.html.getElement('edit', 'a', options={'htmlAttribute':'class'}).click()
        self.html.switchFrame('iframe')
        self.html.fillInput('Bruttó beszerzési egységár', price)
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.driver.refresh()
        sleep(2)
        new = self.html.getTxtFromTable('1', '6')
        self.assertEqual(price, new)
        self.deleteRawMaterial(testName)

    def testOpening(self):
        # Here we test the creation of raw material with opening stock and assert the values
        testName = 'Abszint'
        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')
        # név
        self.html.fillInput('Nyersanyag neve', testName)
        # gross purchase price
        self.html.fillInput('Bruttó beszerzési egységár', '1000')
        # ME
        self.html.clickDropdown('ME', 'liter')
        # setting opening stock
        self.html.fillInput('Nyitó mennyiség', '10')
        # Warehouse
        self.html.clickDropdown('Raktár', 'Pult')
        # Save
        self.html.clickElement('Rögzít')
        # switch back to browser
        self.html.switchFrame()
        self.driver.refresh()
        # checking the counted fields
        sleep(4)
        quantity = self.html.getTxtFromTable(1, 3)
        self.assertEqual('10.00', quantity)
        netprice = self.html.getTxtFromTable(1, 5)
        self.assertEqual(netprice, '787.40')
        nettvalue = self.html.getTxtFromTable(1, 7)
        self.assertEqual(nettvalue, '7 874.02')
        # checking the warehouses

        self.html.clickElement(testName,'td', options={'following':'a'})
        #self.html.getElementByClassName('storages').click()
        self.html.getElement('storages', 'a', options={'htmlAttribute': 'class'}).click()
        self.html.switchFrame('iframe')
        whause = self.html.getTxtFromTable(2, 2)
        self.assertEqual(whause, 'Pult')
        grossPrice = self.html.getTxtFromTable(2, 3)
        self.assertEqual(grossPrice, '1000')
        qty = self.html.getTxtFromTable(2, 4)
        self.assertEqual(qty, '10')
        whValue = self.html.getTxtFromTable(2, 5)
        self.assertEqual(whValue, '10000')
        #self.html.getElementByClassName('iframe').send_keys(Keys.ESCAPE)
        self.html.pressKey('iframe',Keys.ESCAPE)
        self.html.switchFrame()
        self.menu.openStocks()
        sleep(2)
        self.deleteRawMaterial(testName)

    def testDuplicate(self):
        testName = 'Abszint'
        # Here we check if the system lets us create two raw materials with the same name
        self.html.clickElement('Új nyersanyag felvitele', 'a')
        # create a raw material without an opening stock
        # switch to iframe
        sleep(1)
        self.html.switchFrame('iframe')
        # name
        self.html.fillInput('Nyersanyag neve', testName)
        # ME
        self.html.clickDropdown('ME', 'liter')
        # Warehause
        self.html.clickDropdown('Raktár', 'Pult')

        # Save
        self.html.clickElement('Rögzít')
        # switch back to the browser
        self.html.switchFrame()
        self.driver.refresh()
        sleep(2)

        # self.assertTrue(self.driver.find_element_by_xpath('//td[contains(., '' + testName + '')]').is_displayed())
        self.assertTrue(self.html.getElement(testName, 'td').is_displayed())
        # second try to check if we can create duplicate raw materials
        self.html.clickElement('Új nyersanyag felvitele', 'a')
        # Create a new raw material without opening stock
        # switch to iframe and fill upp data
        self.driver.implicitly_wait(3)
        self.html.switchFrame('iframe')
        # # name
        self.html.fillInput('Nyersanyag neve', testName)
        # ME
        self.html.clickDropdown('ME', 'liter')
        # Warehause
        self.html.clickDropdown('Raktár', 'Pult')

        # Save
        self.html.clickElement('Rögzít')
        # we check if the iframe is still present, because if it is the system didn't let us create duplicate items
        self.assertTrue(self.html.getElement('ui-tabs', 'div', options={'htmlAttribute': 'class'}).is_displayed())
        # after that we close it with cancel button
        self.html.clickElement('Mégse')
        self.html.clickElement('Igen')
        self.html.switchFrame()
        sleep(2)
        self.deleteRawMaterial(testName)

    def testWastingRawMaterial(self):
        testName = 'Abszint'
        self.createRawMaterial(testName)
        self.html.clickElement(testName, 'td', options={'following':'a'})
        #self.html.getElementByClassName('edit').click()
        self.html.getElement('edit', 'a', options={'htmlAttribute': 'class'}).click()
        self.html.switchFrame('iframe')
        self.html.fillInput('Nyitó mennyiség', '10')
        self.html.clickDropdown('Raktár', 'Pult')
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        sleep(2)
        self.html.clickElement(testName, 'td', options={'following':'a'})
        #self.html.getElementByClassName('waste').click()
        self.html.getElement('waste', 'a', options={'htmlAttribute': 'class'}).click()
        self.html.switchFrame('iframe')
        self.html.clickDropdown('Raktár', 'Pult')
        sleep(1)
        self.html.fillInput('Mennyiség', '5')
        self.html.clickElement('Üveg összetört')
        sleep(2)
        self.html.switchFrame()
        self.driver.refresh()
        sleep(2)
        qty = self.html.getTxtFromTable(1, 3)
        self.assertEqual(qty, '5.00')
        self.deleteRawMaterial(testName)

    @classmethod
    def tearDownClass(self):
        #pass
        self.driver.quit()
