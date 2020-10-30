from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class Wasting(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openStocks()
        self.html.clickElement('Selejtezések', 'a')
        self.html.currWindow = self.html.getElement('tabs-6', 'div', options=Options(htmlAttribute='id'))

    def testCheckWaste(self):
        self.html.search('asd')

        #self.html.search('Számláló neve, Raktár neve', 'asd', selector='placeholder')
        #self.html.search('searchinput simpleFilterTerm', 'asd') # ez meg nem mukodik, mert a html kodban a legelso elemet talalja meg es jelen esetben ez a 6. ilyen elem

    def tearDownClass(self):
        pass


