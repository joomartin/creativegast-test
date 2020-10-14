from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest
from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy




class Test(unittest.TestCase):

    def createWarehouse(self, warehouseName):
        self.driver.implicitly_wait(10)
        self.html.clickElement('Új raktár felvitele', 'a')
        self.driver.implicitly_wait(10)
        self.html.switchFrame("iframe")

        # textinput kitoltese
        self.html.fillInput('Raktár neve', warehouseName)
        self.html.clickElement("Rögzít")
        self.driver.implicitly_wait(10)
        self.html.switchFrame()
        self.driver.refresh()
        self.driver.implicitly_wait(10)

        sleep(2)


    def deleteWarehouse(self, warehouseName):
        sleep(1)
        #self.html.clickElementFollowing(tagText = warehouseName, tag = 'td', byClass = 'sorting_1')
        self.html.clickElement(warehouseName,'td[@class="sorting_1"]',options={'following':'a'})
        sleep(1)
        self.html.clickElement('Igen')
        sleep(1)



    @classmethod
    def setUpClass(self):
        # webdriver(chrome)
        options = webdriver.ChromeOptions()
        options.add_argument('--auto-open-devtools-for-tabs')
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(executable_path='C:\Webdrivers/chromedriver.exe')
        # maximize window
        self.driver.maximize_window()

        # waiting to server response
        self.driver.implicitly_wait(10)
        # destination URL
        self.driver.get("https://adrian.creativegast.hu/login")

        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)

        self.html.fillInput('Felhasználónév', 'admin', selector='placeholder')
        self.html.fillInput('Jelszó', 'admin', selector='placeholder')


        # click 'Belépés' button
        self.html.clickElement('Belépés')
        #self.assertEqual(self.driver.title, "Felhasználó váltás | CreativeGAST")

        self.html.fillInput('Belépési kód', 'admin', selector='placeholder')
        self.html.clickElement('Belépés')

        #self.assertEqual(self.driver.title, "Főoldal | CreativeGAST")

        self.driver.implicitly_wait(10)
        #self.driver.find_element_by_xpath('/html/body/section/div/a[3]').click()
        self.menu.openStocks()

        sleep(1)
        self.html.clickElement('Raktárak', 'a')


    # create warehouse
    def testCreateWarehouse(self):
        self.createWarehouse("1newWH")

        # check it's displayed
        #self.assertTrue(self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']".format("1newWH")).is_displayed())
        self.assertTrue(self.html.getElementInTable("1newWH", "sorting_1").is_displayed())

        self.deleteWarehouse("1newWH")


    # megegy azonos nevu raktar nem johet letre
    def testCantCreate(self):

        self.createWarehouse("2newWH")

        self.driver.implicitly_wait(10)
        self.html.clickElement('Új raktár felvitele', 'a')
        self.driver.implicitly_wait(10)
        self.html.switchFrame("iframe")

        self.html.fillInput('Raktár neve', '2newWH',)
        self.html.clickElement("Rögzít")
        self.driver.implicitly_wait(10)

        sleep(2)
        #self.assertTrue(self.driver.find_element_by_class_name("iframe").is_displayed())
        #self.assertTrue(self.html.getElementByClassName("iframe").is_displayed())
        self.assertTrue(self.html.getElement('iframe', 'body', options={'htmlAttribute': 'class'}).is_displayed())


        #self.driver.find_element_by_xpath('//label[contains(., "Raktár neve")]//following::input').clear()
        self.html.clearInput('Raktár neve')
        self.html.clickElement("Mégsem")

        self.deleteWarehouse("2newWH")

    # szerkeszt
    def testEdit(self):
        self.createWarehouse("3newWH")

        sleep(2)
        #self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']//following::a//following::a".format("3newWH")).click()
        #self.html.clickElement(t"3newWH", tag = 'td', followNum=2, byClass = 'sorting_1')
        self.html.clickElement(None,"//tr[contains(., '3newWH')]//a[contains(@class, 'edit') and contains(@class, 'actionButton')]", options = {'uniqueSelector':True})
        self.driver.implicitly_wait(10)
        self.html.switchFrame("iframe")
        #self.html.clearInput('Raktár neve')
        self.html.fillInput('Raktár neve', '33newWH')
        self.html.clickElement('Rögzít')

        self.driver.implicitly_wait(10)
        self.html.switchFrame()
        self.driver.refresh()

        sleep(2)
        #self.assertTrue(self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']".format("33newWH")).is_displayed())
        self.assertTrue(self.html.getElementInTable('33newWH', 'sorting_1').is_displayed())

        self.deleteWarehouse("33newWH")

    # törlés
    def testDelete(self):

        self.createWarehouse("4newWH")

        sleep(1)
        self.html.clickElement('4newWH','td[@class="sorting_1"]',options={'following':'a'})
        sleep(1)
        self.html.clickElement("Igen")
        sleep(1)

        sleep(2)
        with self.assertRaises(NoSuchElementException):
            #self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '4newWH']")
            self.html.getElementInTable("4newWH", "sorting_1")




    @classmethod
    def tearDownClass(self):
        #pass
        self.driver.quit()





if __name__ == "__main__":
    unittest.main()






















'''
whList = []
table_id = self.driver.find_element_by_xpath('//*[@id="storages"]')
rows = table_id.find_elements_by_tag_name("tr")
for row in rows:
    if len(row.find_elements_by_tag_name("td")) != 0:
        col = row.find_elements_by_tag_name("td")[0] # note: index start from 0, 1 is col 2
        print(col.text)
        whList.append((col.text))

print(whList)
self.assertIn("0newWH", whList)
'''

'''
#bodyText = self.driver.find_element_by_tag_name('table').text
#self.assertTrue("0newWH" in bodyText)
#self.assertTrue(self.driver.find_element_by_xpath("//td[contains(., '0newWH')]").is_displayed())
'''
