import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


class Test2(unittest.TestCase):
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
        #Brutto beszerzesi egysegar megadasa
        self.driver.find_element_by_xpath("//*[@id='c_purchase_price']").send_keys("1000")
        # ME
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/button").click()
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/div/ul/li[2]").click()
        #Nyitomennyiseg megadasa
        self.driver.find_element_by_xpath("//*[@id='c_open_qty']").send_keys("10")
        # Raktar
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/button").click()
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/div/ul/li[2]/label").click()
        # Mentes
        self.driver.find_element_by_xpath("//*[@id='save']").click()
        # visszaváltunk a böngészőre az iframe-ről
        self.driver.switch_to.default_content()
        self.driver.refresh()
        # számított mezők értékeinek ellenőrzése
        sleep(2)
        mennyiseg = self.driver.find_element_by_xpath("//*[@id='components']/tbody//tr[1]/td[3]").text
        self.assertEqual("10.00",mennyiseg)
        nettoar = self.driver.find_element_by_xpath("//*[@id='components']/tbody//tr[1]/td[5]").text
        self.assertEqual(nettoar,"787.40")
        nettoertek=self.driver.find_element_by_xpath("//*[@id='components']/tbody//tr[1]/td[7]").text
        self.assertEqual(nettoertek,"7 874.02")
        #raktarak ellenörés

        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("storages").click()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        raktar = self.driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr[2]/td[2]").text
        self.assertEqual(raktar,"Pult")
        brutBesz = self.driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr[2]/td[3]").text
        self.assertEqual(brutBesz,"1000")
        menny =self.driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr[2]/td[4]").text
        self.assertEqual(menny,"10")
        raktErtek = self.driver.find_element_by_xpath("//html/body/div[2]/table/tbody/tr[2]/td[5]").text
        self.assertEqual(raktErtek,"10000")
        self.driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath("/html/body/section/div/a[3]/span").click()

        #törlés
        sleep(2)
        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("del").click()

        self.driver.find_element_by_xpath("//button[contains(.,'Igen')]").click()
        self.driver.implicitly_wait(2)

        self.driver.refresh()

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]")


        self.driver.close()