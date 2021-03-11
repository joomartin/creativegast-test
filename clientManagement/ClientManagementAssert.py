import unittest

from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy


class ClientManagementAssert(unittest.TestCase):

    def __init__(self, htmlProxy, driver):
        super().__init__()
        self.html = htmlProxy
        self.menu = MainMenuProxy(driver)

    def assertRegularExist(self, name, address, phone, discount, code):
        self.html.search(name, 'Törzsvendégek')
        self.html.clickTableElement('frequenters', 'id', name, 'a', 'Részletek')
        self.html.switchFrame('iframe')
        #name = self.html.getElement('cl_name', 'input', options=Options(htmlAttribute='id'))
        self.assertTrue(self.html.getTablePairsExist('Név', name))
        self.assertTrue(self.html.getTablePairsExist('Cím', address))
        self.assertTrue(self.html.getTablePairsExist('Telefon', phone))
        self.assertTrue(self.html.getTablePairsExist('Kedv.', discount))
        self.assertTrue(self.html.getTablePairsExist('Kód', code))

        self.html.switchFrame()
        self.html.clickElement('fancybox-item fancybox-close', 'a', options=Options(htmlAttribute='class'))

    def assertClientExist(self, name, address, phone, discount, code):
        self.html.search(name, 'Házhozszállítási cím')
        self.html.clickTableElement('clients', 'id', name, 'a', 'Részletek')
        self.html.switchFrame('iframe')
        #name = self.html.getElement('cl_name', 'input', options=Options(htmlAttribute='id'))
        self.assertTrue(self.html.getTablePairsExist('Név', name))
        self.assertTrue(self.html.getTablePairsExist('Cím', address))
        self.assertTrue(self.html.getTablePairsExist('Telefon', phone))
        self.assertTrue(self.html.getTablePairsExist('Kedv.', discount))
        self.assertTrue(self.html.getTablePairsExist('Kód', code))

        self.html.switchFrame()
        self.html.clickElement('fancybox-item fancybox-close', 'a', options=Options(htmlAttribute='class'))

    def assertDiscountCardExist(self, name, code, discount, category='', group = '', products = 'Válassz...'):
        days = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']

        self.html.search(name, 'Kedvezménykártyák')
        self.html.clickTableElement('discount_cards', 'id', name, 'a', 'Részletek')
        self.html.switchFrame('iframe')

        self.assertTrue(self.html.getTablePairsExist('Megnevezés', name))
        self.assertTrue(self.html.getTablePairsExist('Kód', code))

        for day in days:
            self.assertTrue(self.html.getTablePairsExist(day, discount))

        self.html.switchFrame()
        self.html.clickElement('fancybox-item fancybox-close', 'a', options=Options(htmlAttribute='class'))

        self.html.clickTableElement('discount_cards', 'id', name, 'a', 'Szerkeszt')
        self.html.switchFrame('iframe')
        '''
        lista = self.html.getElement('selectContainer', 'div', options=Options(htmlAttribute='class'))
        getCategory = []
        getCategory.append(self.html.getElement('item selected', 'li', options=Options(htmlAttribute='class', element=lista)))
        print(type(lista))
        print(type(getCategory[0]))
        for i in range(len(getCategory)):
            print('print')
            print(type(getCategory[i]))
            asd = self.html.getElements(category[i], 'label')
            self.assertTrue(self.html.getElement(category[i], 'label', options=Options(element=getCategory[i])).is_displayed())
        '''

        if category == 'all':
            selectList = self.html.getElement('selectContainer', 'div', options=Options(htmlAttribute='class'))
            allElements = self.html.getElements('', 'li', options=Options(element=selectList))
            selectedElements = self.html.getElements('item selected', 'li',
                                                     options=Options(htmlAttribute='class', element=selectList))
            # osszes elem kilett e valasztva
            self.assertEqual(len(allElements), len(selectedElements))
        else:
            self.assertTrue(self.html.getElement(category, 'button').is_displayed())

        self.assertTrue(self.html.getElement(products, 'button').is_displayed())

        if group != '':
            self.html.clickElement('Termékcsoportok', 'label', options=Options(following='input'))
            self.html.switchFrame('iframe')
            selectedGroup = self.html.getElement('dynatree-node dynatree-exp-c dynatree-ico-c dynatree-selected', 'span', options=Options(htmlAttribute='class'))
            group = self.html.getElement('Üdítők', 'a', options=Options(element=selectedGroup)).is_displayed()
            self.assertTrue(group)

        self.html.switchFrame()
        self.html.clickElement('fancybox-item fancybox-close', 'a', options=Options(htmlAttribute='class'))




















