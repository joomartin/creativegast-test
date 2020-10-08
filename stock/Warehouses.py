from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest
#unittest.TestLoader.sortTestMethodsUsing = lambda self, a, b: (a < b) - (a > b)
from core.HtmlProxy import HtmlProxy




class Test(unittest.TestCase):
    #html = None
    name = "0newWH"

    def createWarehouse(self, warehouseName):
        self.driver.implicitly_wait(10)
        #self.driver.find_element_by_xpath('//a[contains(., "Új raktár felvitele")]').click()
        self.html.clickElement(text='Új raktár felvitele', tag='a')
        self.driver.implicitly_wait(10)
        self.html.switchFrame("iframe")
        #self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        #self.driver.find_element_by_xpath('//*[@id="st_name"]').send_keys(warehouseName)

        # textinput kitoltese
        self.html.fillInputByLabel(labelText='Raktár neve', message=warehouseName)
        #self.driver.find_element_by_xpath('//*[@id="save"]').click()
        self.html.clickElement("Rögzít")
        #self.driver.find_element_by_xpath('//button[contains(., "Rögzít")]').click()
        self.driver.implicitly_wait(10)
        self.html.switchFrame()
        #self.driver.switch_to.default_content()
        self.driver.refresh()
        self.driver.implicitly_wait(10)


        sleep(2)

    def deleteWarehouse(self, warehouseName):
        sleep(2)

        #self.driver.find_element_by_xpath("//td[@class='sorting_1'][contains(text(), '" + warehouseName + "')]//following::a").click()
        self.html.clickElementFollowing(tagText = warehouseName, tag = 'td', byClass = 'sorting_1')
        sleep(2)
        self.html.clickElement(text='Igen')
        #self.driver.find_element_by_xpath('//button[contains(., "Igen")]').click()
        sleep(2)



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

        #self.driver.find_element_by_name("username").send_keys("admin")
        self.html.fillInputByPlaceholder(placeholder='Felhasználónév', message='admin')
        # password textfield and type 'admin'
        #self.driver.find_element_by_name("pass").send_keys("admin")
        self.html.fillInputByPlaceholder(placeholder='Jelszó', message='admin')

        # click 'Belépés' button
        #self.driver.find_element_by_xpath("//button[. = 'Belépés']").click()
        self.html.clickElement(text='Belépés')
        #self.assertEqual(self.driver.title, "Felhasználó váltás | CreativeGAST")

        #self.driver.find_element_by_name("id_code").send_keys("admin")
        self.html.fillInputByPlaceholder(placeholder='Belépési kód', message='admin')
        #self.driver.find_element_by_xpath("//button[. = 'Belépés']").click()
        self.html.clickElement(text='Belépés')

        #self.assertEqual(self.driver.title, "Főoldal | CreativeGAST")

        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('/html/body/section/div/a[3]').click()
        #self.driver.find_element_by_xpath('//br[contains(., "Raktárkészlet")]').click()

        sleep(1)
        #self.driver.find_element_by_xpath('//a[contains(., "Raktárak")]').click()
        #self.driver.find_element_by_xpath('//a[. = "Raktárak"]').click()
        self.html.clickElement(text='Raktárak', tag='a')


    # create warehouse
    def testCreateWarehouse(self):
        self.createWarehouse("1newWH")

        # check it's displayed
        self.assertTrue(self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']".format("1newWH")).is_displayed())
        #self.assertTrue(self.html.("//table[@id='storages']/tbody/tr[td = '{}']".format("1newWH")).is_displayed())

        self.deleteWarehouse("1newWH")
        #self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '0newWH']//following::a").click()


    # megegy azonos nevu raktar nem johet letre
    def testCantCreate(self):

        self.createWarehouse("2newWH")

        self.driver.implicitly_wait(10)
        #self.driver.find_element_by_xpath('//*[@id="newStorage"]').click()
        #self.driver.find_element_by_xpath('//a[contains(., "Új raktár felvitele")]').click()
        self.html.clickElement(text='Új raktár felvitele', tag='a')
        self.driver.implicitly_wait(10)
        #self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.html.switchFrame("iframe")
        #self.driver.find_element_by_xpath('//*[@id="st_name"]').send_keys("2newWH")

        #self.driver.find_element_by_xpath('//label[contains(., "Raktár neve")]//following::input').send_keys("2newWH")
        self.html.fillInputByLabel(labelText='Raktár neve', message="2newWH")
        #self.driver.find_element_by_xpath('//*[@id="save"]').click()
        #self.driver.find_element_by_xpath('//button[contains(., "Rögzít")]').click()
        self.html.clickElement("Rögzít")

        self.driver.implicitly_wait(10)

        sleep(2)
        self.assertTrue(self.driver.find_element_by_class_name("iframe").is_displayed())

        #self.driver.find_element_by_xpath('//*[@id="st_name"]').clear()
        self.driver.find_element_by_xpath('//label[contains(., "Raktár neve")]//following::input').clear()
        self.html.clickElement("Mégsem")
        #self.driver.find_element_by_xpath('//button[contains(., "Mégsem")]').click()
        #self.driver.find_element_by_xpath('//*[@id="cancel"]').click()

        self.deleteWarehouse("2newWH")

    # szerkeszt
    def testEdit(self):
        self.createWarehouse("3newWH")

        #newName = "11newWH"
        sleep(2)
        #self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']//following::a//following::a".format("3newWH")).click()
        self.html.clickElementFollowing(tagText="3newWH", tag = 'td', followNum=2, byClass = 'sorting_1')
        self.driver.implicitly_wait(10)
        #self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.html.switchFrame("iframe")
        #self.driver.find_element_by_xpath('//*[@id="st_name"]').clear()
        self.driver.find_element_by_xpath('//label[contains(., "Raktár neve")]//following::input').clear()
        #self.driver.find_element_by_xpath('//*[@id="st_name"]').send_keys("33newWH")
        #self.driver.find_element_by_xpath('//label[contains(., "Raktár neve")]//following::input').send_keys("33newWH")
        self.html.fillInputByLabel("Raktár neve", message="33newWH")
        #self.name = newName
        #self.driver.find_element_by_xpath('//*[@id="save"]').click()
        #self.driver.find_element_by_xpath('//button[contains(., "Rögzít")]').click()
        self.html.clickElement("Rögzít")

        self.driver.implicitly_wait(10)
        #self.driver.switch_to.default_content()
        self.html.switchFrame()
        self.driver.refresh()

        sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']".format("33newWH")).is_displayed())

        self.deleteWarehouse("33newWH")

    # törlés
    def testDelete(self):

        self.createWarehouse("4newWH")

        sleep(2)
        #self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '4newWH']//following::a").click()
        self.html.clickElementFollowing(tagText="4newWH", tag='td', byClass='sorting_1')
        sleep(2)
        #self.driver.find_element_by_xpath('//button[contains(., "Igen")]').click()
        self.html.clickElement("Igen")
        sleep(2)

        sleep(2)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '4newWH']//following::a")



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
