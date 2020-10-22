from shared.BaseTestCase import BaseTestCase


class Wasting(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openStocks()
        self.html.clickElement('Selejtezések', 'a')

    def testCheckWaste(self):
        self.html.searchWaste('Számláló neve, Raktár neve', 'asd', selector='placeholder')
        #self.html.searchWaste('asd')
        #self.html.search('searchinput simpleFilterTerm', 'asd') # ez meg nem mukodik, mert a html kodban a legelso elemet talalja meg es jelen esetben ez a 6. ilyen elem
        pass

    def tearDownClass(self):
        pass


