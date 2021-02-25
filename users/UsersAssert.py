import unittest

from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy


class UserAssert(unittest.TestCase):

    def __init__(self, htmlProxy, driver):
        super().__init__()
        self.html = htmlProxy
        self.menu = MainMenuProxy(driver)

    def assertUserExist(self, surname, firstName, position, group):

        self.html.search(surname, 'Személyzet')
        getSurname = self.html.getTxtFromTable(1, 1, tableId='users', options=Options(htmlAttribute='id'))
        getFirstName = self.html.getTxtFromTable(1, 2, tableId='users', options=Options(htmlAttribute='id'))
        getPosition = self.html.getTxtFromTable(1, 3, tableId='users', options=Options(htmlAttribute='id'))

        self.assertEqual(surname, getSurname)
        self.assertEqual(firstName, getFirstName)
        self.assertEqual(position, getPosition)

        self.html.clickTableElement('users', 'id', surname, 'a', 'Szerkeszt')

        self.assertEqual(position, self.html.getElement('position', 'select', options=Options(htmlAttribute='id', following='button')).text)
        self.assertEqual(group, self.html.getElement('user_groups', 'select', options=Options(htmlAttribute='id', following='button')).text)















