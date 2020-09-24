import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

class Test(unittest.TestCase):
    options = webdriver.ChromeOptions()
    options.add_argument("--auto-open-devtools-for-tabs")
    driver = webdriver.Chrome()

    def test_firstTest(self):
        login = "admin"
        # Felhasznalonev és jelszo megadasa

        self.driver.get("https://ricsi.creativegast.hu/login")
        self.driver.maximize_window()
        self.element = self.driver.find_element_by_xpath("//*[@id='req']")
        self.element.send_keys(login)
        self.element = self.driver.find_element_by_xpath("//*[@id='pass']")
        self.element.send_keys(login)
        self.element.send_keys(Keys.ENTER)

        # Belepesi kod megadas
        element = self.driver.find_element_by_xpath("//*[@id='pass']")
        element.send_keys(login)
        element = self.driver.find_element_by_xpath('//*[@id="login"]/button').click()

        # Raktarkészlet menüpont megnyitasa
        self.driver.find_element_by_xpath("/html/body/section/div/a[3]/span").click()
        # Uj nyersanyag gomb
        self.driver.find_element_by_xpath("//*[@id='newComponent']").click()
        # Termék létrehozása nyitókészlettel
        # nyersanyag adatok kitoltese + váltás iframe-re a böngészőben
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # név
        self.driver.find_element_by_xpath("//*[@id='c_name']").click()
        self.driver.find_element_by_xpath("//*[@id='c_name']").send_keys("Abszint")
        # Brutto beszerzesi egysegar megadasa
        self.driver.find_element_by_xpath("//*[@id='c_purchase_price']").send_keys("1000")
        # ME
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/button").click()
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/div/ul/li[2]").click()
        # Nyitomennyiseg megadasa
        self.driver.find_element_by_xpath("//*[@id='c_open_qty']").send_keys("10")
        # Raktar
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/button").click()
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/div/ul/li[2]/label").click()
        # Mente
        self.driver.find_element_by_xpath("//*[@id='save']").click()
        self.driver.switch_to.default_content()
        self.driver.refresh()
        sleep(2)
        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("waste").click()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        #selejtraktar
        self.driver.find_element_by_xpath("//*[@id='componentsWaste-Form']/div[1]/button").click()
        self.driver.find_element_by_xpath("//*[@id='componentsWaste-Form']/div[1]/div/ul/li[2]/label").click()
        self.driver.find_element_by_xpath("//*[@id='cw_quantity']").send_keys("5")
        self.driver.find_element_by_xpath("//*[@id='cw_other_reason']").send_keys("teszt")
        self.driver.find_element_by_xpath("//*[@id='doWaste']").click()
        self.driver.switch_to.default_content()
        self.driver.refresh()
        sleep(2)
        new = self.driver.find_element_by_xpath("//*[@id='components']/tbody//tr[1]/td[3]").text
        self.assertEqual(new, "5.00")

        self.driver.close()