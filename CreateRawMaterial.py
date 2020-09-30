import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def CreateRawMaterial(webDriver):
    driver = webDriver
    print(hex(id(driver)), " metodus")
    # Raktarkészlet menüpont megnyitasa
    driver.find_element_by_xpath("/html/body/section/div/a[3]/span").click()
    # Uj nyersanyag gomb
    driver.find_element_by_xpath("//*[@id='newComponent']").click()
    # Termék létrehozása nyitókészlet megadása nélkül
    # nyersanyag adatok kitoltese + váltás iframe-re a böngészőben
    driver.implicitly_wait(3)
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    # név
    driver.find_element_by_xpath("//*[@id='c_name']").click()
    driver.find_element_by_xpath("//*[@id='c_name']").send_keys("Abszint")
    # ME
    driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/button").click()
    driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/div/ul/li[2]").click()
    # Raktar
    driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/button").click()
    driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/div/ul/li[2]/label").click()
    # Mentes
    driver.find_element_by_xpath("//*[@id='save']").click()
    # visszaváltunk a böngészőre az iframe-ről
    driver.switch_to.default_content()



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

        '''#Raktarkészlet menüpont megnyitasa
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
        '''

        CreateRawMaterial(self.driver)
        self.driver.refresh()
        sleep(2)

        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]").is_displayed())

        # Törlés
        sleep(2)
        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("del").click()

        self.driver.find_element_by_xpath("//button[contains(.,'Igen')]").click()
        self.driver.implicitly_wait(2)

        self.driver.refresh()
        sleep(3)
        '''
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]")
        '''
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Megpróbáljuk most a terméket kétszer lérehozni, hogy lássuk, hogy már létező terméket nem tudunk ujra létrehozni
        # Uj nyersanyag gomb
        self.driver.find_element_by_xpath("//*[@id='newComponent']").click()

        # nyersanyag adatok kitoltese + váltás iframe-re a böngészőben
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # név
        self.driver.find_element_by_xpath("//*[@id='c_name']").click()
        self.driver.find_element_by_xpath("//*[@id='c_name']").send_keys("Abszint")
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
        # Ellenorizzuk a megjelenest
        self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]").is_displayed())
        # Most ujra létezik a termék szóval megpróbáljuk újra létrehozni

        # Uj nyersanyag gomb
        self.driver.find_element_by_xpath("//*[@id='newComponent']").click()

        # nyersanyag adatok kitoltese + váltás iframe-re a böngészőben
        self.driver.implicitly_wait(3)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # név
        self.driver.find_element_by_xpath("//*[@id='c_name']").click()
        self.driver.find_element_by_xpath("//*[@id='c_name']").send_keys("Abszint")
        # ME
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/button").click()
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[1]/div/div/div/ul/li[2]").click()
        # Raktar
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/button").click()
        self.driver.find_element_by_xpath("//*[@id='tabs-base']/div[4]/div/div/ul/li[2]/label").click()
        # Mentes
        self.driver.find_element_by_xpath("//*[@id='save']").click()
        # Itt azt ellenőrizzük, hogy az Iframe nem tűnik el ezzel látva, hogy a rendszer nem engedte újbol létrehozni a terméket
        self.assertTrue(self.driver.find_element_by_class_name("ui-tabs"))
        # ezután bezárjuk a mégsem gombbal
        self.driver.find_element_by_xpath("//*[@id='cancel']").click()
        self.driver.find_element_by_xpath("//button[contains(.,'Igen')]").click()

        # Törlés
        sleep(2)
        self.driver.find_element_by_xpath("//td[contains(., 'Abszint')]//following::a").click()
        self.driver.find_element_by_class_name("del").click()
        self.driver.find_element_by_xpath("//button[contains(.,'Igen')]").click()
        self.driver.implicitly_wait(2)

        self.driver.close()
