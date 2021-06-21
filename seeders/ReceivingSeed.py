from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options
from receiving.ReceivingAssert import ReceivingAssert
from shared.TestData import TestData as data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class ReceivingSeed:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.receivingAssert = ReceivingAssert(self.html, self.driver)

    def createPartner(self, name, id,  module=False, tab = False):
        if module:
            self.menu.openReceiving()
            self.html.clickElement('Beszállítók', 'a')
        if tab:
            self.html.clickElement('Beszállítók', 'a')


        self.html.clickElement('Új beszállító', 'a')

        self.html.switchFrame('iframe')

        self.html.fillInput('Beszállító neve', name)
        self.html.fillInput('Belső azonosító', id)

        self.html.clickElement('Rögzít')

        self.html.switchFrame()

        #self.receivingAssert.assertPartnerExist(name, 'Beszállítók')
        self.receivingAssert.assertPartnerExist('asdasd', 'Beszállítók')

    def deleteParter(self, partnerName,  module=False, tab=False):
        if module:
            self.menu.openReceiving()
            self.html.clickElement('Beszállítók', 'a')
        if tab:
            self.html.clickElement('Beszállítók', 'a')

        self.html.search(partnerName, 'Beszállítók')

        self.html.clickElement(None,
                               '//table[@id="partners"]//tr[contains(.,"' + partnerName +'")]//label',
                               Options(uniqueSelector=True))
        self.html.clickElement('deletePartners', options=Options(htmlAttribute='id'))
        self.html.clickElement('Igen')
        self.html.refresh()

        self.receivingAssert.assertPartnerNotExist(partnerName, 'Beszállítók')

    def createReceiving(self):
        self.menu.openReceiving()
        self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
        try:
            self.html.clickElement('Új')
        except Exception:
            pass
        self.html.switchFrame('iframe')

        self.html.fillInput('Számla azonosító', 'KomplexTest')
        self.html.clickDropdown('Fizetési mód', 'Készpénz')
        self.html.clickDropdown('Beszállító', data.Partner['Szallito']['Name'])

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Csirkemell']['Name'],
                                   data.RawMaterial['Csirkemell']['Name'], 'li', Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '1000', 'data-title')
        self.html.clickElement('Válassz...')
        firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
        warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
        #self.html.wait(2)
        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
        self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                            options=Options(htmlAttribute='placeholder', element=warehouse[2]))
        self.html.wait(2)

        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.wait(2)
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Finomliszt']['Name'],
                                   data.RawMaterial['Finomliszt']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '150', 'data-title')
        self.html.clickElement('Válassz...')
        firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
        warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
        #self.html.wait(2)
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
        self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                            options=Options(htmlAttribute='placeholder', element=warehouse[2]))
        self.html.wait(2)
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Almalé']['Name'],
                                   data.RawMaterial['Almalé']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '300', 'data-title')
        self.html.clickElement('Válassz...')
        firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
        warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
        #self.html.wait(2)
        wait.until(ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
        self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                            options=Options(htmlAttribute='placeholder', element=warehouse[2]))
        self.html.wait(2)
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Hasábburgonya']['Name'],
                                   data.RawMaterial['Hasábburgonya']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '200', 'data-title')
        self.html.clickElement('Válassz...')
        firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
        warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
        #self.html.wait(2)
        wait.until(ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
        self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                            options=Options(htmlAttribute='placeholder', element=warehouse[2]))
        self.html.wait(2)
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Sonka']['Name'],
                                   data.RawMaterial['Sonka']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '1800', 'data-title')
        self.html.clickElement('Válassz...')
        firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
        warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
        #self.html.wait(2)
        wait.until(ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
        self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                            options=Options(htmlAttribute='placeholder', element=warehouse[2]))
        self.html.wait(2)
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Paradicsomszósz']['Name'],
                                   data.RawMaterial['Paradicsomszósz']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '2000', 'data-title')
        self.html.clickElement('Válassz...')
        firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
        warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
        #self.html.wait(2)
        wait.until(ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
        self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                            options=Options(htmlAttribute='placeholder', element=warehouse[2]))
        self.html.wait(2)
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', 'Kóla', 'Kóla', 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '200', 'data-title')
        self.html.clickElement('Válassz...')
        firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
        warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
        #self.html.wait(2)
        wait.until(ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
        self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                            options=Options(htmlAttribute='placeholder', element=warehouse[2]))
        self.html.wait(2)
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.clickElement('Rögzít')

        self.html.switchFrame()

