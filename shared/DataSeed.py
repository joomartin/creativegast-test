from selenium import webdriver

from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options

class DataSeed():

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe')

        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)

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