import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select


class RawMaterial(unittest.TestCase):

    def txtFromTable(self, row, col):
        return self.driver.find_element_by_xpath("//table//tbody//tr[" + str(row) + "]/td[" + str(col) + "]").text

    def CreateRawMaterial(self, materialName):
        # new raw material button
        self.driver.find_element_by_xpath("//a[contains(.,'Új nyersanyag felvitele')]").click()
        # create a raw material without an opening stock
        # switch to iframe
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # name
        self.driver.find_element_by_xpath("//label[contains(.,'Nyersanyag neve')]//following::input").send_keys(
            materialName)
        # ME
        self.driver.find_element_by_xpath("//label[contains(.,'ME')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'liter')]").click()
        # Warehause
        self.driver.find_element_by_xpath("//label[contains(.,'Raktár')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()

        # Save
        self.driver.find_element_by_xpath("//button[contains(.,'Rögzít')]").click()
        # switch back to the browser
        self.driver.switch_to.default_content()
        self.driver.refresh()
        sleep(2)

        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., '" + materialName + "')]").is_displayed())

    def DeleteRawMaterial(self, name):
        self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]//following::a").click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(.,'Törlés')]").click()
        self.driver.find_element_by_xpath("//button[contains(.,'Igen')]").click()

    def updateRawMaterial(self, name, purchase_price):
        self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]//following::a").click()
        self.driver.find_element_by_class_name("edit").click()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath("//*[@id='c_purchase_price']").send_keys(purchase_price)
        self.driver.find_element_by_xpath("//*[@id='save']").click()
        self.driver.switch_to.default_content()
        self.driver.refresh()
        sleep(2)
        new = self.driver.find_element_by_xpath("//*[@id='components']/tbody//tr[1]/td[6]").text
        self.assertEqual(purchase_price, new)

    def createRawMaterialWithOpening(self, name):
        self.driver.find_element_by_xpath("//a[contains(.,'Új nyersanyag felvitele')]").click()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # név
        self.driver.find_element_by_xpath("//label[contains(.,'Nyersanyag neve')]//following::input").send_keys(name)
        # gross purchase price
        self.driver.find_element_by_xpath(
            "//label[contains(.,'Bruttó beszerzési egységár')]//following::input").send_keys("1000")
        # ME
        self.driver.find_element_by_xpath("//label[contains(.,'ME')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'liter')]").click()
        # setting opening stock
        self.driver.find_element_by_xpath("//label[contains(.,'Nyitó mennyiség')]//following::input").send_keys("10")
        # Warehouse
        self.driver.find_element_by_xpath("//label[contains(.,'Raktár')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()
        # Save
        self.driver.find_element_by_xpath("//button[contains(.,'Rögzít')]").click()
        # switch back to browser
        self.driver.switch_to.default_content()
        self.driver.refresh()
        # checking the counted fields
        sleep(2)
        quantity = self.txtFromTable(1, 3)
        self.assertEqual("10.00", quantity)
        netprice = self.txtFromTable(1, 5)
        self.assertEqual(netprice, "787.40")
        nettvalue = self.txtFromTable(1, 7)
        self.assertEqual(nettvalue, "7 874.02")
        # checking the warehouses

        self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]//following::a").click()
        self.driver.find_element_by_class_name("storages").click()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        whause = self.txtFromTable(2, 2)
        self.assertEqual(whause, "Pult")
        grossPrice = self.txtFromTable(2, 3)
        self.assertEqual(grossPrice, "1000")
        qty = self.txtFromTable(2, 4)
        self.assertEqual(qty, "10")
        whValue = self.txtFromTable(2, 5)
        self.assertEqual(whValue, "10000")
        self.driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("/html/body/section/div/a[3]/span").click()
        sleep(2)

    def duplicateCreateRawMaterial(self, name):
        # new raw material button
        self.driver.find_element_by_xpath("//a[contains(.,'Új nyersanyag felvitele')]").click()
        # Create a new raw material without opening stock
        # switch to iframe and fill upp data
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # name
        self.driver.find_element_by_xpath("//label[contains(.,'Nyersanyag neve')]//following::input").send_keys(name)
        # ME
        self.driver.find_element_by_xpath("//label[contains(.,'ME')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'liter')]").click()
        # Warehouse
        self.driver.find_element_by_xpath("//label[contains(.,'Raktár')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()
        # Save
        self.driver.find_element_by_xpath("//button[contains(.,'Rögzít')]").click()
        # switch back to browser
        self.driver.switch_to.default_content()
        self.driver.refresh()
        sleep(2)

        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]").is_displayed())
        # second try to check if we can create duplicate raw materials
        self.driver.find_element_by_xpath("//a[contains(.,'Új nyersanyag felvitele')]").click()
        # Create a new raw material without opening stock
        # switch to iframe and fill upp data
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # Name
        self.driver.find_element_by_xpath("//label[contains(.,'Nyersanyag neve')]//following::input").send_keys(name)
        # ME
        self.driver.find_element_by_xpath("//label[contains(.,'ME')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'liter')]").click()
        # Warehouse
        self.driver.find_element_by_xpath("//label[contains(.,'Raktár')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()
        # Save
        self.driver.find_element_by_xpath("//button[contains(.,'Rögzít')]").click()
        # we check if the iframe is still present, because if it is the system didn't let us create duplicate items
        self.assertTrue(self.driver.find_element_by_class_name("ui-tabs"))
        # after that we close it with cancel button
        self.driver.find_element_by_xpath("//button[contains(.,'Mégsem')]").click()
        self.driver.find_element_by_xpath("//button[contains(.,'Igen')]").click()

    @classmethod
    def setUpClass(self):
        # On the virtual machines we have to add chromedriver.exe to the Path environmental variable
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.maximize_window()

        # waiting to server response
        self.driver.implicitly_wait(10)
        # destination URL
        self.driver.get("https://ricsi.creativegast.hu/login")

        self.driver.find_element_by_name("username").send_keys("admin")
        # password textfield and type 'admin'
        self.driver.find_element_by_name("pass").send_keys("admin")

        # click 'Belépés' button
        self.driver.find_element_by_xpath("//button[. = 'Belépés']").click()
        # self.assertEqual(self.driver.title, "Felhasználó váltás | CreativeGAST")

        self.driver.find_element_by_name("id_code").send_keys("admin")
        # Keys.ENTER
        self.driver.find_element_by_xpath("//button[. = 'Belépés']").click()
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
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath("//label[contains(.,'Nyitó mennyiség')]//following::input").send_keys("10")
        self.driver.find_element_by_xpath("//label[contains(.,'Raktár')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()
        self.driver.find_element_by_xpath("//button[contains(., 'Rögzít')]").click()
        self.driver.switch_to.default_content()
        sleep(2)
        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("waste").click()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath("//button[contains(.,'Válassz...')]").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//label[contains(.,'Mennyiség')]//following::input").send_keys("5")
        self.driver.find_element_by_xpath("//button[contains(.,'Üveg összetört')]").click()
        self.driver.find_element_by_xpath("//button[contains(.,'Selejtez')]").click()
        sleep(2)
        self.driver.switch_to.default_content()
        self.driver.refresh()
        sleep(2)
        qty = self.txtFromTable(1, 3)
        self.assertEqual(qty, "5.00")
        self.DeleteRawMaterial(testName)

    @classmethod
    def tearDownClass(self):
        # pass
        self.driver.quit()
