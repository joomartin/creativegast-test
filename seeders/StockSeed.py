
from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options
from stock.StockAssert import StockAssert


class StockSeed:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.stockAssert = StockAssert(self.html, self.driver)

    def createRawMaterial(self, materialName, me, wareHouse, module=False):
        if module:
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

    def createRawMaterialWithOpening(self, testName, grossPrice, openingQty, whName, me='liter', module=False):
        if module:
            self.menu.openStocks()
        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', testName)
        self.html.fillInput('Bruttó beszerzési egységár', grossPrice)
        self.html.clickDropdown('ME', me)
        self.html.fillInput('Nyitó mennyiség', openingQty)
        self.html.clickDropdown('Raktár', whName)
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

    def deleteRawMaterial(self, name, module=False):
        if module:
            self.menu.openStocks()

        self.html.wait(2)
        self.html.search(name, 'Raktárkészlet')
        self.html.wait(2)
        self.html.clickTableDropdown(name, 'Törlés', 'Raktárkészlet')
        self.html.wait(4)
        self.html.clickElement('Igen')
        self.html.wait(2)
        self.html.search('', 'Raktárkészlet')
        self.html.wait(4)

    def createWarehouse(self, warehouseName, module=False, tab = False):

        if module:
            self.menu.openStocks()
            self.html.clickElement('Raktárak', 'a')
        elif tab:
            self.html.clickElement('Raktárak', 'a')

        self.html.clickElement('Új raktár felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Raktár neve', warehouseName)
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

    def deleteWarehouse(self, warehouseName, module=False, tab = False):

        if module:
            self.menu.openStocks()
            self.html.clickElement('Raktárak', 'a')
        elif tab:
            self.html.clickElement('Raktárak', 'a')

        self.html.refresh()
        self.html.wait(2)
        self.html.search(warehouseName, 'Raktárak')
        self.html.wait(2)
        currWindow = self.html.getElement('tabs-3', 'div', options=Options(htmlAttribute='id'))
        # itt azert adjuk at a currWindow-t, hogy az adott oldalon keressen a td-k kozott
        self.html.clickElement(warehouseName, 'td', Options(following='a', element=currWindow))
        self.html.wait(3)
        self.html.clickElement('Igen')
        self.html.wait(2)
        self.html.search('', 'Raktárak')
        self.html.wait(2)
