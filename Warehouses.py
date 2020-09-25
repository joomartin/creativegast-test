from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import unittest
#unittest.TestLoader.sortTestMethodsUsing = lambda self, a, b: (a < b) - (a > b)
import HTMLTestRunner
import os




class Test(unittest.TestCase):

    name = "0newWH"

    def createWarehouse(self, warehouseName):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('//*[@id="newStorage"]').click()
        self.driver.implicitly_wait(10)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath('//*[@id="st_name"]').send_keys(warehouseName)
        self.driver.find_element_by_xpath('//*[@id="save"]').click()
        self.driver.implicitly_wait(10)
        self.driver.switch_to.default_content()
        self.driver.refresh()
        self.driver.implicitly_wait(10)

        sleep(2)

    def deleteWarehouse(self, warehouseName):
        sleep(2)
        self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '" + warehouseName + "']//following::a").click()
        sleep(2)
        self.driver.find_element_by_xpath('//button[contains(., "Igen")]').click()
        sleep(2)



    @classmethod
    def setUpClass(self):
        # webdriver(chrome)
        options = webdriver.ChromeOptions()
        options.add_argument('--auto-open-devtools-for-tabs')
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # maximize window
        self.driver.maximize_window()

        # waiting to server response
        self.driver.implicitly_wait(10)
        # destination URL
        self.driver.get("https://adrian.creativegast.hu/login")

        self.driver.find_element_by_name("username").send_keys("admin")
        # password textfield and type 'admin'
        self.driver.find_element_by_name("pass").send_keys("admin")

        # click 'Belépés' button
        self.driver.find_element_by_xpath("//button[. = 'Belépés']").click()
        #self.assertEqual(self.driver.title, "Felhasználó váltás | CreativeGAST")

        self.driver.find_element_by_name("id_code").send_keys("admin")
        # Keys.ENTER
        self.driver.find_element_by_xpath("//button[. = 'Belépés']").click()
        self.driver.implicitly_wait(10)
        #self.assertEqual(self.driver.title, "Főoldal | CreativeGAST")

        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('/html/body/section/div/a[3]').click()

        sleep(1)
        self.driver.find_element_by_xpath('//a[contains(., "Raktárak")]').click()




    def test001_create_warehouse(self):

        self.createWarehouse("1newWH")

        self.assertTrue(self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']".format("1newWH")).is_displayed())

        self.deleteWarehouse("1newWH")

        #self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '0newWH']//following::a").click()

    # megegy azonos nevu raktar nem johet letre
    #@unittest.skip("ez most skip")
    def test002_cant_create(self):

        self.createWarehouse("2newWH")

        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('//*[@id="newStorage"]').click()
        self.driver.implicitly_wait(10)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath('//*[@id="st_name"]').send_keys("2newWH")
        self.driver.find_element_by_xpath('//*[@id="save"]').click()
        self.driver.implicitly_wait(10)

        sleep(2)
        self.assertTrue(self.driver.find_element_by_class_name("iframe").is_displayed())

        self.driver.find_element_by_xpath('//*[@id="st_name"]').clear()
        self.driver.find_element_by_xpath('//*[@id="cancel"]').click()

        self.deleteWarehouse("2newWH")

    # szerkeszt
    def test003_edit(self):
        self.createWarehouse("3newWH")

        newName = "11newWH"
        sleep(2)
        self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']//following::a//following::a".format("3newWH")).click()
        self.driver.implicitly_wait(10)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_element_by_xpath('//*[@id="st_name"]').clear()
        self.driver.find_element_by_xpath('//*[@id="st_name"]').send_keys("33newWH")
        self.name = newName
        print(hex(id(self.name)))
        print(self.name)
        self.driver.find_element_by_xpath('//*[@id="save"]').click()

        self.driver.implicitly_wait(10)
        self.driver.switch_to.default_content()
        self.driver.refresh()

        sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']".format("33newWH")).is_displayed())

        self.deleteWarehouse("33newWH")

    # törlés
    def test004_delete(self):

        self.createWarehouse("4newWH")

        print(hex(id(self.name)))
        print(self.name)
        sleep(2)
        self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '4newWH']//following::a").click()
        sleep(2)
        self.driver.find_element_by_xpath('//button[contains(., "Igen")]').click()
        sleep(2)

        sleep(2)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '4newWH']//following::a")



    @classmethod
    def tearDownClass(self):
        pass
        #self.driver.quit()





if __name__ == "__main__":
    #suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()








'''
var = self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '0newWH']")
print(var.text)
var = self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '0newWH']")
print(var.text)
'''


















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
