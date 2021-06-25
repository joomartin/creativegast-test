from selenium.webdriver.common.keys import Keys

from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class Groups(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    def setUp(self):
        self.menu.openUsers()
        self.html.clickElement('Csoportok', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def tearDown(self):
        pass

    def testCreateGroup(self):
        def wrapper():
            name = data.Group['Felszolgáló2']['Name']

            self.usersSeed.createGroup(name)
            self.assertTrue(self.html.getElementInTable(name, 'groups', 'Csoportok').is_displayed())
            self.usersSeed.deleteGroup(name)

        super(Groups, self).runTest(wrapper, 'groups-testCreateGroup')

    def testUpdateUserGroup(self):
        def wrapper():
            name = data.Group['Felszolgáló2']['Name']
            rights = data.Group['Felszolgáló2']['Rights'].values()
            self.usersSeed.createGroup(name)

            self.html.clickTableElement('groups', 'id', name, 'a', 'Szerkeszt', 'Csoportok')
            self.html.clickElement('Jogok', 'a')
            self.html.switchFrame('iframe')
            self.html.clickElement('inside scrollableContent', 'div', options=Options(htmlAttribute='class'))
            html = self.driver.find_element_by_tag_name('html')


            # oke, egyelore jo lesz igy
            # NASA code
            # a megjeleno iframe-ben gorgetunk lefele es bepipaljuk a szukseges elemeket
            selected = 0
            while selected != len(rights):
                for i in rights:
                    try:
                        self.html.getElement(None, '//span[contains(., "' + i + '") and @class="dynatree-node dynatree-exp-c dynatree-ico-c"]', options=Options(uniqueSelector=True)).click()
                        selected += 1
                    except Exception as ex:
                        pass
                html.send_keys(Keys.DOWN)
                self.html.wait(0.5)

            self.html.clickElement('Rögzít', waitSeconds=2)
            self.usersAssert.assertGroupExist(name, rights)

            self.usersSeed.deleteGroup(name)

        super(Groups, self).runTest(wrapper, 'groups-testUpdateUserGroup')

    '''
    def testCreateGroupWithRights(self):
        pass
    '''


































