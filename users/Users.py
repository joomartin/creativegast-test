from selenium.webdriver.common.keys import Keys

from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class Users(BaseTestCase):
    surname = data.User['Géza']['Surname']
    firstName = data.User['Géza']['FirstName']
    userName = data.User['Géza']['UserName']
    position = data.User['Géza']['Position']
    password = data.User['Géza']['Password']
    group = data.User['Géza']['Group']
    rights = data.Group['Felszolgáló2']['Rights'].values()

    @classmethod
    def setUpClass(self):
        def wrapper():
            super().setUpClass()
            super().login(self)

        super(Users, self).runTest(wrapper, 'users-setUpClass')

    def setUp(self):
        def wrapper():
            self.menu.openUsers()

        super(Users, self).runTest(wrapper, 'users-setUp')

    @classmethod
    def tearDownClass(self):
        def wrapper():
            super().tearDownClass()

        super(Users, self).runTest(wrapper, 'users-tearDownClass')

    def tearDown(self):
        try:
            self.usersSeed.deleteUser(self.surname)
        except Exception:
            pass

    def testCreateUser(self):
        def wrapper():
            self.usersSeed.createUser(self.surname, self.firstName, self.userName, self.password, self.position, self.group)
            self.usersAssert.assertUserExist(self.surname, self.firstName, self.position, self.rights, group=self.group)

            self.html.clickElement('Kilépés a rendszerből', 'a')
            self.html.fillInput('Felhasználónév', self.userName, selector='placeholder')
            self.html.fillInput('Jelszó', self.password, selector='placeholder')
            self.html.clickElement('Belépés')
            self.html.fillInput('Belépési kód', self.password, selector='placeholder')
            self.html.clickElement('Belépés')
            self.setUp()

            self.html.clickElement('Kilépés a rendszerből', 'a')
            self.tearDownClass()
            self.setUpClass()
            self.setUp()

        super(Users, self).runTest(wrapper, 'users-testCreateUser')













