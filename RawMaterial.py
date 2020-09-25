import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class RawMaterial(unittest.TestCase):

    def CreateRawMaterial(self, materialName):
        # Raktarkészlet menüpont megnyitasa
        self.driver.find_element_by_xpath("/html/body/section/div/a[3]/span").click()
        # Uj nyersanyag gomb
        self.driver.find_element_by_xpath("//*[@id='newComponent']").click()
        # Termék létrehozása nyitókészlet megadása nélkül
        # nyersanyag adatok kitoltese + váltás iframe-re a böngészőben
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # név
        self.driver.find_element_by_xpath("//*[@id='c_name']").click()
        self.driver.find_element_by_xpath("//*[@id='c_name']").send_keys(materialName)
        # ME
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/button").click()
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/div/ul/li[2]").click()
        # Raktar
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/button").click()
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/div/ul/li[2]/label").click()
        # Mentes
        self.driver.find_element_by_xpath("//*[@id='save']").click()
        # visszaváltunk a böngészőre az iframe-ről
        self.driver.switch_to.default_content()
        self.driver.refresh()
        sleep(2)

        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., '"+materialName+"')]").is_displayed())

    def DeleteRawMaterial(self, name):
        self.driver.find_element_by_xpath("//td[contains(., '"+name+"')]//following::a").click()
        self.driver.find_element_by_class_name("del").click()
        self.driver.find_element_by_xpath("//button[contains(.,'Igen')]").click()


    def setUpClass(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()


    def TestRawMaterial(self):
        testName = "Abszint"
        self.CreateRawMaterial(testName)
        self.DeleteRawMaterial(testName)