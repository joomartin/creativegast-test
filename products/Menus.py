from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class Menus(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openProducts()
        self.html.clickElement('Menü', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def createMenu(self, menuName):
        self.html.clickElement('Új menü felvitele', 'a')

        self.html.switchFrame('iframe')
        self.html.clickDropdown('Nyomtatási részleg', 'Konyha')
        self.html.fillInput('Termék neve', menuName)
        self.html.getElement('Termékcsoport', 'label', Options(following='input//following::input')).click()
        self.html.wait(2)

        self.html.switchFrame('iframe')
        self.html.clickElement('Ételek', 'a')
        self.html.clickElement('Rögzít')
        self.html.switchFrame('iframe')

        self.html.fillInput('Kód', '1212')
        self.html.getElement('27%', 'td', Options(following='td//input')).send_keys('100')

        self.html.fillInput('Fogás neve', 'Előétel')
        self.html.clickDropdown('Termékcsoport:', 'Étel')
        self.html.clickElement('Ételek')
        self.html.fillInput('Mennyiség', '1')
        self.html.getInput('Mennyiség','label').click()
        self.html.clickElement('Hozzáad')
        self.html.wait(2)
        self.html.clickElement('Teszt kaja', 'span')

        self.html.clickElement('icon-hozzaadas addNewComponent', 'i', Options(htmlAttribute='class'))
        self.html.wait(3)

        tab = self.html.getElement('tabs-2', 'div', Options(htmlAttribute ='id'))
        self.html.fillInput('Fogás neve', 'Főétel', element=tab)
        self.html.clickDropdown('Termékcsoport:', 'Étel', element=tab)
        self.html.clickElement('Ételek',element=tab)
        self.html.fillInput('Mennyiség', '1', element=tab)
        self.html.getInput('Mennyiség', 'label', element=tab).click()
        self.html.clickElement('Hozzáad', element=tab)
        self.html.wait(3)
        self.html.clickElement('Kecskepuding', 'span', element=tab)

        self.html.clickElement('Rögzít')
        self.html.switchFrame()


    def deleteMenu(self, menuName):
        self.html.clickTableElement('menu', 'id', menuName, 'span', 'Törlés', 'Menü')
        self.html.clickElement('Igen')

    def testCreate(self):
        testName = 'Test menu'
        self.createMenu(testName)
        self.productAssert.assertMenuExists(testName, '127.00')
        self.deleteMenu(testName)

    def testUpdateMenu(self):
        testName = 'Test menu'
        modName = 'Modified menu'
        modPrice= 300
        self.createMenu(testName)

        self.html.clickTableElement('menu', 'id', testName, 'span', 'Szerkeszt', 'Menü')
        self.html.switchFrame('iframe')

        self.html.fillInput('Termék neve',modName)
        self.html.getElement('27%', 'td', Options(following='td//input')).clear()
        self.html.getElement('27%', 'td', Options(following='td//input')).send_keys(modPrice)
        self.html.clickElement('Rögzít')
        self.html.wait(2)
        try:
            self.html.getElement('iframe hasTwoRow', 'body', Options(htmlAttribute='class'))
        except NoSuchElementException:
            self.html.switchFrame()
        else:
            self.html.clickElement('Rögzít')
            self.html.switchFrame()

        self.html.refresh()
        self.html.search(modName, 'Menü')
        self.html.wait(3)
        self.productAssert.assertMenuExists(modName, '381.00')

        self.deleteMenu(modName)