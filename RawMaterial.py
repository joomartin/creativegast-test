import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from HtmlHandler import HtmlHandler

class RawMaterial(unittest.TestCase):
    #html = None


    def CreateRawMaterial(self, materialName):
        # new raw material button
        self.html.clickElement("Új nyersanyag felvitele", tag="a")
        # create a raw material without an opening stock
        # switch to iframe
        sleep(1)
        self.html.switchFrame("iframe")
        # name
        self.html.fillInputByLabel("Nyersanyag neve", materialName)
        # ME
        self.html.clickDropdown("ME", "liter")
        # Warehause
        self.html.clickDropdown("Raktár", "Pult")

        # Save
        self.html.clickElement("Rögzít")
        # switch back to the browser
        self.html.switchFrame()
        self.driver.refresh()
        sleep(2)

        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., '" + materialName + "')]").is_displayed())

    def DeleteRawMaterial(self, name):
        self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]//following::a").click()
        sleep(2)
        self.html.clickElement("Törlés", tag='a')
        self.html.clickElement("Igen")

    def updateRawMaterial(self, name, purchase_price):
        self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]//following::a").click()
        self.driver.find_element_by_class_name("edit").click()
        self.html.switchFrame("iframe")
        self.html.fillInputByLabel("Bruttó beszerzési egységár",purchase_price)
        self.html.clickElement("Rögzít")
        self.html.switchFrame()
        self.driver.refresh()
        sleep(2)
        new = self.html.getTxtFromTable("1", "6")
        self.assertEqual(purchase_price, new)

    def createRawMaterialWithOpening(self, name):
        self.html.clickElement("Új nyersanyag felvitele", tag="a")
        self.html.switchFrame("iframe")
        # név
        self.html.fillInputByLabel("Nyersanyag neve", name)
        # gross purchase price
        self.html.fillInputByLabel("Bruttó beszerzési egységár", "1000")
        # ME
        self.html.clickDropdown("ME", "liter")
        # setting opening stock
        self.html.fillInputByLabel("Nyitó mennyiség", "10")
        # Warehouse
        self.html.clickDropdown("Raktár", "Pult")
        # Save
        self.html.clickElement("Rögzít")
        # switch back to browser
        self.html.switchFrame()
        self.driver.refresh()
        # checking the counted fields
        sleep(2)
        quantity = self.html.getTxtFromTable(1, 3)
        self.assertEqual("10.00", quantity)
        netprice = self.html.getTxtFromTable(1, 5)
        self.assertEqual(netprice, "787.40")
        nettvalue = self.html.getTxtFromTable(1, 7)
        self.assertEqual(nettvalue, "7 874.02")
        # checking the warehouses

        self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]//following::a").click()
        #self.driver.find_elements_by_xpath("//a[contains(., 'Raktárak')]")[1].click()
        self.driver.find_element_by_class_name("storages").click()
        self.html.switchFrame("iframe")
        whause = self.html.getTxtFromTable(2, 2)
        self.assertEqual(whause, "Pult")
        grossPrice = self.html.getTxtFromTable(2, 3)
        self.assertEqual(grossPrice, "1000")
        qty = self.html.getTxtFromTable(2, 4)
        self.assertEqual(qty, "10")
        whValue = self.html.getTxtFromTable(2, 5)
        self.assertEqual(whValue, "10000")
        self.driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
        self.html.switchFrame()
        self.driver.find_element_by_xpath("/html/body/section/div/a[3]/span").click()
        sleep(2)

    def duplicateCreateRawMaterial(self, name):
        self.html.clickElement("Új nyersanyag felvitele", tag="a")
        # create a raw material without an opening stock
        # switch to iframe
        sleep(1)
        self.html.switchFrame("iframe")
        # name
        self.html.fillInputByLabel("Nyersanyag neve", name)
        # ME
        self.html.clickDropdown("ME", "liter")
        # Warehause
        self.html.clickDropdown("Raktár", "Pult")

        # Save
        self.html.clickElement("Rögzít")
        # switch back to the browser
        self.html.switchFrame()
        self.driver.refresh()
        sleep(2)

        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]").is_displayed())
        # second try to check if we can create duplicate raw materials
        self.html.clickElement("Új nyersanyag felvitele", tag="a")
        # Create a new raw material without opening stock
        # switch to iframe and fill upp data
        self.driver.implicitly_wait(3)
        self.html.switchFrame("iframe")
        # # name
        self.html.fillInputByLabel("Nyersanyag neve", name)
        # ME
        self.html.clickDropdown("ME", "liter")
        # Warehause
        self.html.clickDropdown("Raktár", "Pult")

        # Save
        self.html.clickElement("Rögzít")
        # we check if the iframe is still present, because if it is the system didn't let us create duplicate items
        self.assertTrue(self.driver.find_element_by_class_name("ui-tabs"))
        # after that we close it with cancel button
        self.html.clickElement("Mégse")
        self.html.clickElement("Igen")

    @classmethod
    def setUpClass(self):
        # On the virtual machines we have to add chromedriver.exe to the Path environmental variable
        test = RawMaterial()
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.maximize_window()

        # waiting to server response
        self.driver.implicitly_wait(10)
        # destination URL
        self.driver.get("https://ricsi.creativegast.hu/login")

        self.html = HtmlHandler(self.driver)

        self.driver.find_element_by_name("username").send_keys("admin")
        # password textfield and type 'admin'
        self.driver.find_element_by_name("pass").send_keys("admin")

        # click 'Belépés' button
        #self.driver.find_element_by_xpath("//button[. = 'Belépés']").click()
        self.html.clickElement("Belépés")
        # self.assertEqual(self.driver.title, "Felhasználó váltás | CreativeGAST")

        self.driver.find_element_by_name("id_code").send_keys("admin")
        # Keys.ENTER
        test.html.clickElement("Belépés")
        self.driver.implicitly_wait(10)
        # self.assertEqual(self.driver.title, "Főoldal | CreativeGAST")

        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('/html/body/section/div/a[3]').click()

    def test_Create(self):
        # This case we simply test the process of creation
        testName = "Abszint"
        self.CreateRawMaterial(testName)
        self.DeleteRawMaterial(testName)

    def test_Update(self):
        # here we test the update of a raw material
        testName = "Abszint"
        self.CreateRawMaterial(testName)
        self.updateRawMaterial(testName, '1 010.00')
        self.DeleteRawMaterial(testName)

    def test_Opening(self):
        # Here we test the creation of raw material with opening stock and assert the values
        testName = "Abszint"
        self.createRawMaterialWithOpening(testName)
        self.DeleteRawMaterial(testName)

    def test_Duplicate(self):
        # Here we check if the system lets us create two raw materials with the same name
        testName = "Abszint"
        self.duplicateCreateRawMaterial(testName)
        sleep(2)
        self.DeleteRawMaterial(testName)

    def test_WastingRawMaterial(self):
        testName = "Abszint"
        self.CreateRawMaterial(testName)
        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("edit").click()
        self.html.switchFrame("iframe")
        self.html.fillInputByLabel("Nyitó mennyiség", "10")
        self.html.clickDropdown("Raktár", "Pult")
        self.html.clickElement("Rögzít")
        self.html.switchFrame()
        sleep(2)
        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("waste").click()
        self.html.switchFrame("iframe")
        self.html.clickDropdown("Raktár", "Pult")
        sleep(1)
        self.html.fillInputByLabel("Mennyiség", "5")
        self.html.clickElement("Üveg összetört")
        sleep(2)
        self.html.switchFrame()
        self.driver.refresh()
        sleep(2)
        qty = self.html.getTxtFromTable(1, 3)
        self.assertEqual(qty, "5.00")
        self.DeleteRawMaterial(testName)

    @classmethod
    def tearDownClass(self):
        # pass
        self.driver.quit()
