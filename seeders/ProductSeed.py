from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options
from stock.StockAssert import StockAssert
from shared.TestData import TestData as data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class ProductSeed:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.stockAssert = StockAssert(self.html, self.driver)

    def createProductGroup(self, groupName, module=False, tab=False):

        if module:
            self.menu.openProducts()
            self.html.clickElement('Termékcsoportok', 'a')
        if tab:
            self.html.clickElement('Termékcsoportok', 'a')

        self.html.clickElement('Új termékcsoport felvitele', 'a')

        self.html.switchFrame('iframe')

        self.html.fillInput('Termékcsoport neve', groupName)
        self.html.clickDropdown('Kategória', 'Étel')
        self.html.clickElement('Rögzít')
        #// *[ @ id = "tabs-productgroups"] / div[1] / div / button
        wait = WebDriverWait(self.driver, 10000)

        asd = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="tabs-productgroups"]/div[1]/div/button')))
        self.html.switchFrame()
        #self.html.wait(120)
        #self.html.switchFrame()
        #self.html.wait(10)

    def deleteProductGroup(self, groupName, module=False, tab=False):
        if module:
            self.menu.openProducts()
            self.html.clickElement('Termékcsoportok', 'a')
        elif tab:
            self.html.clickElement('Termékcsoportok', 'a')

        self.html.clickTableElement('product_groups', 'id', groupName, 'span', 'Törlés', 'Termékcsoportok')
        self.html.wait(2)
        self.html.clickElement('Igen')

    def createMenu(self, menuName, firstMeal, secondMeal, module=False, tab=False):
        if module:
            self.menu.openProducts()
            self.html.clickElement('Menü', 'a')
        elif tab:
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
        self.html.clickDropdown('Termékcsoport:', data.ProductGroup['Egyeb']['Name'])
        self.html.clickElement(data.ProductGroup['Egyeb']['Name'])
        self.html.fillInput('Mennyiség', '1')
        self.html.getInput('Mennyiség', 'label').click()
        self.html.clickElement('Hozzáad')
        self.html.wait(3)
        self.html.clickElement(firstMeal, 'span')

        self.html.clickElement('icon-hozzaadas addNewComponent', 'i', Options(htmlAttribute='class'))
        self.html.wait(3)

        tab = self.html.getElement('tabs-2', 'div', Options(htmlAttribute='id'))
        self.html.fillInput('Fogás neve', 'Főétel', options=Options(element=tab))
        self.html.clickDropdown('Termékcsoport:', data.ProductGroup['Egyeb']['Name'], options=Options(element=tab))
        self.html.clickElement(data.ProductGroup['Egyeb']['Name'], options=Options(element=tab))
        self.html.fillInput('Mennyiség', '1', options=Options(element=tab))
        self.html.getInput('Mennyiség', 'label', options=Options(element=tab)).click()
        self.html.clickElement('Hozzáad', options=Options(element=tab))
        self.html.wait(3)
        self.html.clickElement(secondMeal, 'span', options=Options(element=tab))

        self.html.clickElement('Rögzít')
        self.html.switchFrame()

    def deleteMenu(self, menuName, module=False, tab=False):
        if module:
            self.menu.openProducts()
            self.html.clickElement('Menü', 'a')
        elif tab:
            self.html.clickElement('Menü', 'a')

        self.html.clickTableElement('menu', 'id', menuName, 'span', 'Törlés', 'Menü')
        self.html.clickElement('Igen')

    def createPizza(self, pizzaName, baseComponent, topping, module=False, tab=False):
        if module:
            self.menu.openProducts()
            self.html.clickElement('Pizza (testreszabható)', 'a')
        elif tab:
            self.html.clickElement('Pizza (testreszabható)', 'a')

        self.html.clickElement('Új pizza (testreszabható)', 'a')

        self.html.switchFrame('iframe')
        self.html.clickDropdown('Nyomtatási részleg', 'Pizza')
        self.html.fillInput('Termék neve', pizzaName)
        self.html.fillInput('Kód', '1211')

        self.html.clickDropdown('Szósz', 'Paradicsomos alap')

        self.html.fillAutocomplete('baseComponentName', 'input', baseComponent, baseComponent, 'li',
                                   Options(htmlAttribute='id'))
        table = self.html.getElement('baseComponents', 'table', Options(htmlAttribute='id'))
        self.html.getElement('Hozzáad', 'button', Options(element=table)).click()

        # self.html.fillAutocomplete('toppingComponentName', 'input', topping, topping, 'li', Options(htmlAttribute='id'))
        # table = self.html.getElement('toppingComponents', 'table', Options(htmlAttribute='id'))
        # self.html.getElement('Hozzáad', 'button', element=table).click()

        self.html.clickElement('Mennyiségek', 'a')
        self.html.wait(2)
        td = self.html.getElement('Eladási ár(ak)', 'td')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', Options(htmlAttribute='class'))

        self.html.fillInput('Nettó', '1000')
        self.html.wait(2)
        self.html.clickElement('Rögzít', 'a', waitSeconds=2)
        #self.html.closeAllert()
        #self.html.clickElement('Rögzít', 'a')
        self.html.clickElement('Rögzít')

    def deletePizza(self, pizzaName, module=False, tab=False):
        if module:
            self.menu.openProducts()
            self.html.clickElement('Pizza (testreszabható)', 'a')
        elif tab:
            self.html.clickElement('Pizza (testreszabható)', 'a')

        self.html.clickTableElement('customproduct-2', 'id', pizzaName, 'a', 'Törlés', 'Pizza (testreszabható)')
        self.html.clickElement('Igen')

    def createProduct(self, name, group, code, counter, component, compQty=2, netPrice=100, module=False):
        if module:
            self.menu.openProducts()

        self.html.clickElement('Új termék felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pult')
        self.html.switchFrame('iframe')

        self.html.clickElement(group, 'a')
        self.html.wait(2)
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', name)
        self.html.fillInput('Kód', code)

        self.html.clickElement('p_counters', 'input', Options(htmlAttribute='id'), waitSeconds=1)
        self.html.switchFrame('iframe')

        wait = WebDriverWait(self.driver, 10000)
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id = "fix"]')))
        self.html.clickElement(counter, 'td')
        self.html.clickElement('Rögzít')
        self.html.switchFrame('iframe')

        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', options=Options(element=places))
        self.html.fillInput('Nettó', netPrice)
        self.html.wait(1)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(2)

        self.html.fillAutocomplete('componentName', 'input', component, component, 'li', Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', compQty, 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

    def createProductConveniencies(self, name, group, code, counter, component, compQty=2, module=False):
        if module:
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

        self.html.clickElement('p_counters', 'input', Options(htmlAttribute='id'), waitSeconds=1)
        self.html.switchFrame('iframe')

        self.html.clickElement(counter, 'td')
        self.html.clickElement('Rögzít')
        self.html.switchFrame('iframe')

        self.html.clickElement(None, './/label[contains(.,"Gyártás termék") and @class="radio formStyle"]', options=Options(uniqueSelector=True))
        self.html.fillInput('Recept adag', '1')

        self.html.fillAutocomplete('componentName', 'input', component, component, 'li', Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', compQty, 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

    def deleteProduct(self, name, module=False):
        if module:
            self.menu.openProducts()

        self.html.refresh()

        self.html.clickTableElement('products', 'id', name, 'a', 'Törlés', 'Termékek')
        self.html.clickElement('Igen', waitSeconds=2)
        self.html.search('', 'Termékek')

    def createCounter(self, name, position, module=False, tab=False):
        if module:
            self.menu.openProducts()
            self.html.clickElement('Számlálók', 'a')
        if tab:
            self.html.clickElement('Számlálók', 'a')

        self.html.clickElement('Új számláló felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Számláló neve', name)
        self.html.fillInput('Számláló állás', position)
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

    def deleteCounter(self, name, module=False, tab=False):
        if module:
            self.menu.openProducts()
            self.html.clickElement('Számlálók', 'a')
        if tab:
            self.html.clickElement('Számlálók', 'a')
        self.html.refresh()

        self.html.clickTableElement('counters', 'id', name, 'a', 'Törlés', 'Számlálók')
        self.html.clickElement('Igen', waitSeconds=1)
        self.html.search('', 'Számlálók')

    # kola
    def createProductAsRawMaterial(self, module=False):
        if module:
            self.menu.openProducts()

        self.html.clickElement('Új termék felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pult')
        self.html.switchFrame('iframe')

        self.html.clickElement('Üdítők', 'a')
        self.html.clickElement('Rögzít')
        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', 'Kóla')
        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', options=Options(element=places))
        self.html.fillInput('Nettó', '300')
        self.html.wait(1)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(2)

        self.html.clickElement('Felvétel nyersanyagként', 'label', Options(following='i'))
        #self.html.fillInput('Termék mennyiségi tartalma', '100')
        self.html.clickElement('Rögzít')

    # termek valaszthato korettel
    def createProductChose(self, name):
        self.html.clickElement('Új termék felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pult')
        self.html.switchFrame('iframe')

        self.html.clickElement('Ételek', 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', name)

        self.html.clickElement('Ez a termék tartalmaz köretet', 'label', Options(following='i'))

        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', options=Options(element=places))
        self.html.fillInput('Nettó', '1800')
        self.html.wait(1)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(2)

        self.html.fillAutocomplete('componentName', 'input', 'Csirkemell', 'Csirkemell', 'li', Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', '0.20', 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

    def createProductFix(self, name, sideDish, module=False):
        if module:
            self.menu.openProducts()

        self.html.clickElement('Új termék felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pult')
        self.html.switchFrame('iframe')

        self.html.clickElement('Ételek', 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', name)

        self.html.clickElement('Ez a termék tartalmaz köretet', 'label', Options(following='i'))

        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', options=Options(element=places))
        self.html.fillInput('Nettó', '2200')
        self.html.wait(1)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(2)

        self.html.clickElement('Válasszon köretet')
        self.html.clickElement(data.Product[sideDish]['Name'], 'label')

        self.html.fillAutocomplete('componentName', 'input', 'Csirkemell', 'Csirkemell', 'li',
                                   Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', '0.20', 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

    def createSpecialPizza(self, pizzaName, baseComponent, topping, module=False, tab=False):
        if module:
            self.menu.openProducts()
            self.html.clickElement('Pizza (testreszabható)', 'a')
        elif tab:
            self.html.clickElement('Pizza (testreszabható)', 'a')

        self.html.clickElement('Új pizza (testreszabható)', 'a')

        self.html.switchFrame('iframe')
        self.html.clickDropdown('Nyomtatási részleg', 'Pizza')
        self.html.fillInput('Termék neve', pizzaName)
        self.html.fillInput('Kód', '1333')

        self.html.clickDropdown('Szósz', 'Paradicsomszósz')

        self.html.fillAutocomplete('baseComponentName', 'input', baseComponent, baseComponent, 'li',
                                   Options(htmlAttribute='id'))
        table = self.html.getElement('baseComponents', 'table', Options(htmlAttribute='id'))
        self.html.getElement('Hozzáad', 'button', Options(element=table)).click()

        self.html.fillAutocomplete('toppingComponentName', 'input', topping, topping, 'li',
                                   Options(htmlAttribute='id'))
        table = self.html.getElement('toppingComponents', 'table', Options(htmlAttribute='id'))
        self.html.getElement('Hozzáad', 'button', options=Options(element=table)).click()

        self.html.clickElement('Mennyiségek', 'a')
        self.html.wait(2)

        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', Options(htmlAttribute='class'))
        self.html.fillInput('grossPrice-2-1', '1400', 'input', options=Options(htmlAttribute='name'))
        self.html.fillInput('grossPrice-5-1', '2000', 'input', options=Options(htmlAttribute='name'))
        self.html.wait(2)
        self.html.clickElement('Rögzít', 'a', waitSeconds=2)
        self.html.clickElement('Rögzít')

        self.html.clickTableElement('customproduct-2', 'id', 'Sonkás pizza', 'a', 'Szerkeszt',
                                    'Pizza (testreszabható)')
        self.html.switchFrame('iframe')
        self.html.clickElement('Mennyiségek', 'a')
        self.html.wait(2)
        inputFields = self.html.getElements('inputmask-numeric qtys', 'input',
                                            options=Options(htmlAttribute='class'))

        inputFields[0].send_keys('0,18')
        inputFields[1].send_keys('0,18')
        # self.html.fillInput('inputmask-numeric qtys', '0,18', 'input', options=Options(htmlAttribute='class', element=inputFields[0]))
        # self.html.fillInput('inputmask-numeric qtys', '0,18', 'input', options=Options(htmlAttribute='class', element=inputFields[1]))
        self.html.clickElement('Rögzít')

    def createAppleJuice(self):
        self.productseed.createProduct('Almalé', 'Kiszereléses',
                                       '99', data.Counter['TestCounter']['Name'], data.RawMaterial['Almalé']['Name'],
                                       '1', '1800',
                                       module=True)
