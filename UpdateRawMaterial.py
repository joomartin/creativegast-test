import unittest
from time import sleep
import CreateRawMaterial as crm

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome()

    def test_firstTest(self):
        login = "admin"
        # Felhasznalonev és jelszo megadasa

        #self.driver.get("https://ricsi.creativegast.hu/login")
        self.driver.maximize_window()
        '''
        self.element = self.driver.find_element_by_xpath("//*[@id='req']")
        self.element.send_keys(login)
        self.element = self.driver.find_element_by_xpath("//*[@id='pass']")
        self.element.send_keys(login)
        self.element.send_keys(Keys.ENTER)

        # Belepesi kod megadas
        element = self.driver.find_element_by_xpath("//*[@id='pass']")
        element.send_keys(login)
        
        element = self.driver.find_element_by_xpath('//*[@id="login"]/button').click()
        
        #Raktarkészlet menüpont megnyitasa
        self.driver.find_element_by_xpath("/html/body/section/div/a[3]/span").click()
        #Uj nyersanyag gomb
        self.driver.find_element_by_xpath("//*[@id='newComponent']").click()
        # Termék létrehozása nyitókészlet megadása nélkül
        #nyersanyag adatok kitoltese + váltás iframe-re a böngészőben
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        #név
        self.driver.find_element_by_xpath("//*[@id='c_name']").click()
        self.driver.find_element_by_xpath("//*[@id='c_name']").send_keys("Abszint")
        #ME
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/button").click()
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/div/ul/li[2]").click()
        #Raktar
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/button").click()
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/div/ul/li[2]/label").click()
        #Mentes
        self.driver.find_element_by_xpath("//*[@id='save']").click()
        #visszaváltunk a böngészőre az iframe-ről
        self.driver.switch_to.default_content()
        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]").is_displayed())
        
        print(hex(id(self.driver)), "osztaly")
        crm.CreateRawMaterial(self.driver)

        #szerkesztés
        self.driver.refresh()
        sleep(2)
        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("edit").click()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath("//*[@id='c_purchase_price']").send_keys('1010')
        self.driver.find_element_by_xpath("//*[@id='save']").click()
        self.driver.switch_to.default_content()
        self.driver.refresh()
        sleep(2)
        new = self.driver.find_element_by_xpath("//*[@id='components']/tbody//tr[1]/td[6]").text
        self.assertEqual('1 010.00', new)

        #törlés
        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("del").click()

        self.driver.find_element_by_xpath("//button[contains(.,'Igen')]").click()

        self.driver.close()
        '''