from selenium import webdriver

from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options
from stock.StockAssert import StockAssert

class DataSeed():

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.stockAssert = StockAssert(self.html, self.driver)


    def createRawMaterial(self, materialName, me, wareHouse):
        self.menu.openStocks()

        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', materialName)
        self.html.clickDropdown('ME', me)
        self.html.clickDropdown('Raktár', wareHouse)
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()
        self.stockAssert.assertMaterialExist(materialName, 'Raktárkészlet')

    def deleteRawMaterial(self, name):
        self.menu.openStocks()

        self.html.wait(2)
        self.html.search(name, 'Raktárkészlet')
        self.html.wait(2)
        self.html.clickTableDropdown(name, 'Törlés', 'Raktárkészlet')
        self.html.clickElement('Igen')
        self.html.wait(2)
        self.html.search('', 'Raktárkészlet')
        self.html.wait(2)

    def createWarehouse(self, warehouseName):
        self.menu.openStocks()
        self.html.clickElement('Raktárak', 'a')
        self.html.clickElement('Új raktár felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Raktár neve', warehouseName)
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

    def deleteWarehouse(self, warehouseName):
        self.menu.openStocks()
        self.html.clickElement('Raktárak', 'a')

        self.html.refresh()
        self.html.wait(2)
        self.html.search(warehouseName, 'Raktárak')
        self.html.wait(2)
        currWindow = self.html.getElement('tabs-3', 'div', options=Options(htmlAttribute='id'))
        # itt azert adjuk at a currWindow-t, hogy az adott oldalon keressen a td-k kozott
        self.html.clickElement(warehouseName, 'td', Options(following='a'), element = currWindow)
        self.html.wait(2)
        self.html.clickElement('Igen')
        self.html.wait(2)
        self.html.search('', 'Raktárak')
        self.html.wait(2)

    def createProductGroup(self, groupName):
        self.menu.openProducts()
        self.html.clickElement('Termékcsoportok', 'a')

        self.html.clickElement('Új termékcsoport felvitele', 'a')

        self.html.switchFrame('iframe')

        self.html.fillInput('Termékcsoport neve', groupName)
        self.html.clickDropdown('Kategória', 'Étel')
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.html.wait(2)

    def deleteProductGroup(self, groupName):
        self.menu.openProducts()
        self.html.clickElement('Termékcsoportok', 'a')

        self.html.clickTableElement('product_groups', 'id', groupName, 'span', 'Törlés', 'Termékcsoportok')
        self.html.wait(2)
        self.html.clickElement('Igen')

    def createMenu(self, menuName):
        self.menu.openProducts()
        self.html.clickElement('Menü', 'a')

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
        self.menu.openProducts()
        self.html.clickElement('Menü', 'a')

        self.html.clickTableElement('menu', 'id', menuName, 'span', 'Törlés', 'Menü')
        self.html.clickElement('Igen')

    def createPizza(self, pizzaName):
        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')

        self.html.clickElement('Új pizza (testreszabható)', 'a')

        self.html.switchFrame('iframe')
        self.html.clickDropdown('Nyomtatási részleg', 'Pizza')
        self.html.fillInput('Termék neve', pizzaName)
        self.html.fillInput('Kód', '1211')

        self.html.clickDropdown('Szósz', 'Paradicsomos alap')

        self.html.fillAutocomplete('baseComponentName', 'input', 'liszt', 'Liszt (teszt)', 'li', Options(htmlAttribute='id'))
        table = self.html.getElement('baseComponents', 'table', Options(htmlAttribute='id'))
        self.html.getElement('Hozzáad', 'button', element=table).click()


        self.html.fillAutocomplete('toppingComponentName', 'input', 'Sonka', 'Sonka Feltét', 'li', Options(htmlAttribute='id'))
        table = self.html.getElement('toppingComponents', 'table', Options(htmlAttribute='id'))
        self.html.getElement('Hozzáad', 'button', element=table).click()

        self.html.clickElement('Mennyiségek', 'a')
        self.html.wait(2)
        td = self.html.getElement('Eladási ár(ak)', 'td')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', Options(htmlAttribute='class'))

        self.html.fillInput('Nettó', '1000')
        self.html.clickElement('Rögzít', 'a')
        self.html.closeAllert()
        self.html.clickElement('Rögzít', 'a')
        self.html.wait(2)
        self.html.clickElement('Rögzít')


    def deletePizza(self, pizzaName):
        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')

        self.html.clickTableElement('customproduct-2', 'id', pizzaName, 'a', 'Törlés', 'Pizza (testreszabható)')
        self.html.clickElement('Igen')


    def createProduct(self, name, group, code, counter):
        self.menu.openProducts()

        self.html.clickElement('Új termék felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pult')
        self.html.switchFrame('iframe')

        self.html.clickElement(group, 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', name)
        self.html.fillInput('Kód', code)

        self.html.clickElement('p_counters', 'input', Options(htmlAttribute='id'), waitSeconds = 1)
        self.html.switchFrame('iframe')

        self.html.clickElement(counter, 'td')
        self.html.clickElement('Rögzít')
        self.html.switchFrame('iframe')

        '''
        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', element=places)
        self.html.fillInput('Nettó', 100)
        self.html.clickElement('Rögzít')
        self.html.wait(2)
        '''

        self.html.fillAutocomplete('componentName', 'input', 'Captain', 'Captain Morgan 0.7 l', 'li', Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', 2, 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

    def deleteProduct(self, name):
        self.menu.openProducts()

        self.html.refresh()

        self.html.clickTableElement('products', 'id', name, 'a', 'Törlés', 'Termékek')
        self.html.clickElement('Igen', waitSeconds=1)
        self.html.search('', 'Termékek')