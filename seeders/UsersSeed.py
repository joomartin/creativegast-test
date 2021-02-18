from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options
from users.Users import UserAssert


class StockSeed:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.usersAssert = UserAssert(self.html, self.driver)

    def deleteGroup(self, name):
        self.html.clickTableElement('groups', 'id', name, 'a', 'Törlés', 'Csoportok')
        self.html.clickElement('Igen', waitSeconds=1)
        self.html.search('', 'Számlálók')

























