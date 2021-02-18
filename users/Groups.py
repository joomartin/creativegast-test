from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class DiscountCards(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    def setUp(self):
        self.menu.openUsers()
        self.html.clickElement('Csoportok', 'a')

    @classmethod
    def tearDownClass(self):
        # super().tearDownClass()
        pass

    def tearDown(self):
        pass

    def testCreateGroup(self):
        name = data.Group['Felszolgáló2']['Name']
        enter = data.Group['Felszolgáló2']['Rights']['Enter']
        enter2 = data.Group['Felszolgáló2']['Rights']['Enter2']
        restaurant = data.Group['Felszolgáló2']['Rights']['Restaurant']
        openDay = data.Group['Felszolgáló2']['Rights']['OpenDay']
        closeDay = data.Group['Felszolgáló2']['Rights']['CloseDay']
        printCloseDay = data.Group['Felszolgáló2']['Rights']['PrintCloseDay']

        page = self.html.getElement('tabs-groups', 'div', options=Options(htmlAttribute='id'))

        self.html.fillInput('Név', name)
        self.html.clickElement('Rögzít', options=Options(element=page))

        self.assertTrue(self.html.getElementInTable(name, 'groups', 'Csoportok').is_displayed())

    def testEdit(self):
        pass

    def testCreateGroupWithRights(self):
        pass



































