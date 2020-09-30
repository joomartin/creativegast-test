import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

class RawMaterial(unittest.TestCase):

    def CreateRawMaterial(self, materialName):
        # Uj nyersanyag gomb
        self.driver.find_element_by_xpath("//a[contains(.,'Új nyersanyag felvitele')]").click()
        # Termék létrehozása nyitókészlet megadása nélkül
        # nyersanyag adatok kitoltese + váltás iframe-re a böngészőben
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # név
        self.driver.find_element_by_xpath("//label[contains(.,'Nyersanyag neve')]//following::input").send_keys(materialName)
        # ME
        self.driver.find_element_by_xpath("//label[contains(.,'ME')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'liter')]").click()
        # Raktar
        self.driver.find_element_by_xpath("//label[contains(.,'Raktár')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()

        # Mentes
        self.driver.find_element_by_xpath("//button[contains(.,'Rögzít')]").click()
        # visszaváltunk a böngészőre az iframe-ről
        self.driver.switch_to.default_content()
        self.driver.refresh()
        sleep(2)

        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., '"+materialName+"')]").is_displayed())

    def DeleteRawMaterial(self, name):
        self.driver.find_element_by_xpath("//td[contains(., '"+name+"')]//following::a").click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(.,'Törlés')]").click()
        self.driver.find_element_by_xpath("//button[contains(.,'Igen')]").click()

    def updateRawMaterial(self,name,purchase_price):
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

    def createRawMaterialWithOpening(self,name):
        self.driver.find_element_by_xpath("//a[contains(.,'Új nyersanyag felvitele')]").click()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # név
        self.driver.find_element_by_xpath("//label[contains(.,'Nyersanyag neve')]//following::input").send_keys(name)
        # Brutto beszerzesi egysegar megadasa
        self.driver.find_element_by_xpath("//label[contains(.,'Bruttó beszerzési egységár')]//following::input").send_keys("1000")
        # ME
        self.driver.find_element_by_xpath("//label[contains(.,'ME')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'liter')]").click()
        # Nyitomennyiseg megadasa
        self.driver.find_element_by_xpath("//label[contains(.,'Nyitó mennyiség')]//following::input").send_keys("10")
        # Raktar
        self.driver.find_element_by_xpath("//label[contains(.,'Raktár')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()
        # Mentes
        self.driver.find_element_by_xpath("//button[contains(.,'Rögzít')]").click()
        # visszaváltunk a böngészőre az iframe-ről
        self.driver.switch_to.default_content()
        self.driver.refresh()
        # számított mezők értékeinek ellenőrzése
        sleep(2)
        quantity = self.driver.find_element_by_xpath("//*[@id='components']/tbody//tr[1]/td[3]").text
        self.assertEqual("10.00", quantity)
        netprice = self.driver.find_element_by_xpath("//*[@id='components']/tbody//tr[1]/td[5]").text
        self.assertEqual(netprice, "787.40")
        nettvalue = self.driver.find_element_by_xpath("//*[@id='components']/tbody//tr[1]/td[7]").text
        self.assertEqual(nettvalue, "7 874.02")
        # raktarak ellenörés

        self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]//following::a").click()
        self.driver.find_element_by_class_name("storages").click()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        whause = self.driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr[2]/td[2]").text
        self.assertEqual(whause, "Pult")
        grossPrice = self.driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr[2]/td[3]").text
        self.assertEqual(grossPrice, "1000")
        qty = self.driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr[2]/td[4]").text
        self.assertEqual(qty, "10")
        whValue = self.driver.find_element_by_xpath("//html/body/div[2]/table/tbody/tr[2]/td[5]").text
        self.assertEqual(whValue, "10000")
        self.driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("/html/body/section/div/a[3]/span").click()
        sleep(2)

    def duplicateCreateRawMaterial(self,name):
        # Uj nyersanyag gomb
        self.driver.find_element_by_xpath("//a[contains(.,'Új nyersanyag felvitele')]").click()
        # Termék létrehozása nyitókészlet megadása nélkül
        # nyersanyag adatok kitoltese + váltás iframe-re a böngészőben
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # név
        self.driver.find_element_by_xpath("//label[contains(.,'Nyersanyag neve')]//following::input").send_keys(name)
        # ME
        self.driver.find_element_by_xpath("//label[contains(.,'ME')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'liter')]").click()
        # Raktar
        self.driver.find_element_by_xpath("//label[contains(.,'Raktár')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()
        # Mentes
        self.driver.find_element_by_xpath("//button[contains(.,'Rögzít')]").click()
        # visszaváltunk a böngészőre az iframe-ről
        self.driver.switch_to.default_content()
        self.driver.refresh()
        sleep(2)

        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., '" + name + "')]").is_displayed())

        self.driver.find_element_by_xpath("//a[contains(.,'Új nyersanyag felvitele')]").click()
        # Termék létrehozása nyitókészlet megadása nélkül
        # nyersanyag adatok kitoltese + váltás iframe-re a böngészőben
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # név
        self.driver.find_element_by_xpath("//label[contains(.,'Nyersanyag neve')]//following::input").send_keys(name)
        # ME
        self.driver.find_element_by_xpath("//label[contains(.,'ME')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'liter')]").click()
        # Raktar
        self.driver.find_element_by_xpath("//label[contains(.,'Raktár')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'Pult')]").click()
        # Mentes
        self.driver.find_element_by_xpath("//button[contains(.,'Rögzít')]").click()

        self.assertTrue(self.driver.find_element_by_class_name("ui-tabs"))
        # ezután bezárjuk a mégsem gombbal
        self.driver.find_element_by_xpath("//button[contains(.,'Mégsem')]").click()
        self.driver.find_element_by_xpath("//button[contains(.,'Igen')]").click()



    @classmethod
    def setUpClass(self):
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
        testName = "Abszint"
        self.CreateRawMaterial(testName)
        self.DeleteRawMaterial(testName)


    def test_Update(self):
        testName = "Abszint"
        self.CreateRawMaterial(testName)
        self.updateRawMaterial(testName,'1 010.00')
        self.DeleteRawMaterial(testName)
    def test_Opening(self):
        testName = "Abszint"
        self.createRawMaterialWithOpening(testName)
        self.DeleteRawMaterial(testName)

    def test_Duplicate(self):
        testName = "Abszint"
        self.duplicateCreateRawMaterial(testName)
        sleep(2)
        self.DeleteRawMaterial(testName)


    @classmethod
    def tearDownClass(self):
        #pass
        self.driver.quit()