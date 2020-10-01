import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select


class RawMaterial(unittest.TestCase):

    def txtFromTable(self, row, col):
        return self.driver.find_element_by_xpath("//table//tbody//tr[" + str(row) + "]/td[" + str(col) + "]").text

    def ClickElement(self, tag, text):
        self.driver.find_element_by_xpath("//" + str(tag) + "[contains(.,'" + text + "')]").click()

    def dropDownSelect(self, labelTxt, selectValue):
        self.driver.find_element_by_xpath("//label[contains(.,'" + labelTxt + "')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'" + selectValue + "')]").click()

    def fillInput(self, labelTxt, inputTxt):
        self.driver.find_element_by_xpath("//label[contains(.,'" + labelTxt + "')]//following::input").send_keys(inputTxt)
        
    def switchFrame(self, tagName=""):
        if not tagName:
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(self.driver.find_element_by_tag_name(tagName))


    def CreateRawMaterial(self, materialName):
        # new raw material button
        self.ClickElement("a","Új nyersanyag felvitele")
        # create a raw material without an opening stock
        # switch to iframe
        sleep(1)
        self.switchFrame("iframe")
        # name
        self.fillInput("Nyersanyag neve", materialName)
        # ME
        self.dropDownSelect("ME", "liter")
        # Warehause
        self.dropDownSelect("Raktár", "Pult")

        # Save
        self.ClickElement("button", "Rögzít")
        # switch back to the browser
        self.switchFrame()
        self.driver.refresh()
        sleep(2)

        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., '" + materialName + "')]").is_displayed())

    def DeleteRawMaterial(self, name):
        self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]//following::a").click()
        sleep(2)
        self.ClickElement("a", "Törlés")
        self.ClickElement("button", "Igen")

    def updateRawMaterial(self, name, purchase_price):
        self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]//following::a").click()
        self.driver.find_element_by_class_name("edit").click()
        self.switchFrame("iframe")
        self.driver.find_element_by_xpath("//*[@id='c_purchase_price']").send_keys(purchase_price)
        self.driver.find_element_by_xpath("//*[@id='save']").click()
        self.switchFrame()
        self.driver.refresh()
        sleep(2)
        new = self.driver.find_element_by_xpath("//*[@id='components']/tbody//tr[1]/td[6]").text
        self.assertEqual(purchase_price, new)

    def createRawMaterialWithOpening(self, name):
        self.ClickElement("a","Új nyersanyag felvitele")
        self.switchFrame("iframe")
        # név
        self.fillInput("Nyersanyag neve", name)
        # gross purchase price
        self.driver.find_element_by_xpath(
            "//label[contains(.,'Bruttó beszerzési egységár')]//following::input").send_keys("1000")
        # ME
        self.dropDownSelect("ME", "liter")
        # setting opening stock
        self.driver.find_element_by_xpath("//label[contains(.,'Nyitó mennyiség')]//following::input").send_keys("10")
        # Warehouse
        self.dropDownSelect("Raktár", "Pult")
        # Save
        self.driver.find_element_by_xpath("//button[contains(.,'Rögzít')]").click()
        # switch back to browser
        self.switchFrame()
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
        #self.driver.find_elements_by_xpath("//a[contains(., 'Raktárak')]")[1].click()
        self.driver.find_element_by_class_name("storages").click()
        self.switchFrame("iframe")
        whause = self.txtFromTable(2, 2)
        self.assertEqual(whause, "Pult")
        grossPrice = self.txtFromTable(2, 3)
        self.assertEqual(grossPrice, "1000")
        qty = self.txtFromTable(2, 4)
        self.assertEqual(qty, "10")
        whValue = self.txtFromTable(2, 5)
        self.assertEqual(whValue, "10000")
        self.driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
        self.switchFrame()
        self.driver.find_element_by_xpath("/html/body/section/div/a[3]/span").click()
        sleep(2)

    def duplicateCreateRawMaterial(self, name):
        self.ClickElement("a", "Új nyersanyag felvitele")
        # create a raw material without an opening stock
        # switch to iframe
        sleep(1)
        self.switchFrame("iframe")
        # name
        self.fillInput("Nyersanyag neve", name)
        # ME
        self.dropDownSelect("ME", "liter")
        # Warehause
        self.dropDownSelect("Raktár", "Pult")

        # Save
        self.ClickElement("button", "Rögzít")
        # switch back to the browser
        self.switchFrame()
        self.driver.refresh()
        sleep(2)

        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]").is_displayed())
        # second try to check if we can create duplicate raw materials
        self.ClickElement("a", "Új nyersanyag felvitele")
        # Create a new raw material without opening stock
        # switch to iframe and fill upp data
        self.driver.implicitly_wait(3)
        self.switchFrame("iframe")
        # # name
        self.fillInput("Nyersanyag neve", name)
        # ME
        self.dropDownSelect("ME", "liter")
        # Warehause
        self.dropDownSelect("Raktár", "Pult")

        # Save
        self.ClickElement("button", "Rögzít")
        # we check if the iframe is still present, because if it is the system didn't let us create duplicate items
        self.assertTrue(self.driver.find_element_by_class_name("ui-tabs"))
        # after that we close it with cancel button
        self.ClickElement("button", "Mégse")
        self.ClickElement("button", "Igen")

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

        self.driver.find_element_by_name("username").send_keys("admin")
        # password textfield and type 'admin'
        self.driver.find_element_by_name("pass").send_keys("admin")

        # click 'Belépés' button
        #self.driver.find_element_by_xpath("//button[. = 'Belépés']").click()
        test.ClickElement(tag="button", text="Belépés")
        # self.assertEqual(self.driver.title, "Felhasználó váltás | CreativeGAST")

        self.driver.find_element_by_name("id_code").send_keys("admin")
        # Keys.ENTER
        test.ClickElement(tag="button", text="Belépés")
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
        self.switchFrame("iframe")
        self.driver.find_element_by_xpath("//label[contains(.,'Nyitó mennyiség')]//following::input").send_keys("10")
        self.driver.find_element_by_xpath("//label[contains(.,'Raktár')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()
        self.driver.find_element_by_xpath("//button[contains(., 'Rögzít')]").click()
        self.switchFrame()
        sleep(2)
        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("waste").click()
        self.switchFrame("iframe")
        self.driver.find_element_by_xpath("//button[contains(.,'Válassz...')]").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//label[contains(.,'Mennyiség')]//following::input").send_keys("5")
        self.driver.find_element_by_xpath("//button[contains(.,'Üveg összetört')]").click()
        sleep(2)
        self.switchFrame()
        self.driver.refresh()
        sleep(2)
        qty = self.txtFromTable(1, 3)
        self.assertEqual(qty, "5.00")
        self.DeleteRawMaterial(testName)

    @classmethod
    def tearDownClass(self):
        # pass
        self.driver.quit()
