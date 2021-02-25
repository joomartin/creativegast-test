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
        # super().tearDownClass()
        pass

    def tearDown(self):
        pass

    def testCreateUser(self):
        surname = data.User['Géza']['Surname']
        firstName = data.User['Géza']['FirstName']
        userName = data.User['Géza']['UserName']
        position = data.User['Géza']['Position']
        password = data.User['Géza']['Password']
        group = data.User['Géza']['Group']

        self.usersSeed.createUser(surname, firstName, userName, password, position, group)
        self.usersAssert.assertUserExist(surname, firstName, position, group=group)
        #self.usersSeed.deleteGroup(name)

    def testUpdate(self):
        name = data.Group['Felszolgáló2']['Name']
        enter = data.Group['Felszolgáló2']['Rights']['Enter']
        enter2 = data.Group['Felszolgáló2']['Rights']['Enter2']
        restaurant = data.Group['Felszolgáló2']['Rights']['Restaurant']
        openDay = data.Group['Felszolgáló2']['Rights']['OpenDay']
        closeDay = data.Group['Felszolgáló2']['Rights']['CloseDay']
        printCloseDay = data.Group['Felszolgáló2']['Rights']['PrintCloseDay']

        self.usersSeed.createGroup(name)

        self.html.clickTableElement('groups', 'id', name, 'a', 'Szerkeszt', 'Csoportok')
        self.html.clickElement('Jogok', 'a')
        self.html.switchFrame('iframe')
        self.html.clickElement('inside scrollableContent', 'div', options=Options(htmlAttribute='class'))
        html = self.driver.find_element_by_tag_name('html')
        appeared = False
        self.html.scroll()
        #self.driver.find_element_by_xpath('.//a[contains(.,"Gyártás")]').submit()
        print(self.html.getElement('Gyártás', 'a').is_displayed())
        '''
        while appeared is False:
            html.send_keys(Keys.DOWN)
            appeared = self.html.getElement('Gyártás', 'a').is_displayed()
            try:
                self.html.clickElement('Gyártás', 'a')
            except Exception as ex:
                print(ex)
            print(self.html.getElement('Gyártás', 'a').is_displayed())
            self.html.wait(0.5)
        '''

        '''
        self.html.clickElement('inside scrollableContent', 'div', options=Options(htmlAttribute='class'))
        element = self.html.getElement('Gyártás', 'a')
        html = self.driver.find_element_by_tag_name('html')
        html.send_keys(Keys.DOWN)
        self.html.wait(2)
        '''
        '''
        self.html.clickElement(enter, 'a')
        self.html.clickElement(enter2, 'a')
        self.html.clickElement(restaurant, 'a')
        self.html.clickElement(openDay, 'a')
        self.html.clickElement(closeDay, 'a')
        self.html.clickElement(printCloseDay, 'a')
        '''

    def testCreateGroupWithRights(self):
        pass

































































