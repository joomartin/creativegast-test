from selenium.webdriver.common.keys import Keys

from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class Users(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    def setUp(self):
        self.menu.openUsers()

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def tearDown(self):
        pass

    def testCreateUser(self):
        surname = data.User['Géza']['Surname']
        firstName = data.User['Géza']['FirstName']
        userName = data.User['Géza']['UserName']
        position = data.User['Géza']['Position']
        password = data.User['Géza']['Password']
        group = data.User['Géza']['Group']
        rights = data.Group['Felszolgáló2']['Rights'].values()

        self.usersSeed.createUser(surname, firstName, userName, password, position, group)
        self.usersAssert.assertUserExist(surname, firstName, position, rights, group=group)

        self.html.clickElement('Kilépés a rendszerből', 'a')
        self.html.fillInput('Felhasználónév', userName, selector='placeholder')
        self.html.fillInput('Jelszó', password, selector='placeholder')
        self.html.clickElement('Belépés')
        self.html.fillInput('Belépési kód', password, selector='placeholder')
        self.html.clickElement('Belépés')
        self.setUp()

        self.html.clickElement('Kilépés a rendszerből', 'a')
        self.setUpClass()
        self.setUp()

        self.usersSeed.deleteUser(surname)
























































