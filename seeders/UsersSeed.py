from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options
from users.UsersAssert import UserAssert


class UsersSeed:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.usersAssert = UserAssert(self.html, self.driver)

    def createGroup(self, name):
        page = self.html.getElement('tabs-groups', 'div', options=Options(htmlAttribute='id'))
        self.html.fillInput('Név', name)
        self.html.clickElement('Rögzít', options=Options(element=page))

    def deleteGroup(self, name):
        self.html.clickTableElement('groups', 'id', name, 'a', 'Törlés', 'Csoportok')
        self.html.clickElement('Igen', waitSeconds=1)
        self.html.search('', 'Csoportok')

    def createUser(self, surname, firstName, userName, password, position, group):
        self.html.fillInput('Vezetéknév', surname)
        #self.html.fillInput('Vezetéknévasdasd', surname)
        self.html.fillInput('Keresztnév', firstName)
        self.html.fillInput('Felhasználónév', userName)
        self.html.fillInput('Jelszó', password)
        self.html.fillInput('Jelszó ismét', password)
        self.html.fillInput('Belépő kód', password)
        self.html.clickDropdown('Beosztás', position)
        self.html.clickDropdown('Csoportok', group)

        self.html.clickElement('Rögzít')

    def deleteUser(self, surname):
        self.html.search(surname, 'Személyzet')
        self.html.clickTableElement('users', 'id', surname, 'a', 'Törlés', 'Személyzet')
        self.html.clickElement('Igen', waitSeconds=1)
        self.html.search('', 'Személyzet')






















