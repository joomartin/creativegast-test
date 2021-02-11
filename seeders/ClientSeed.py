
from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options
from clientManagement.ClientManagementAssert import ClientManagementAssert


class ClientSeed:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.clientAssert = ClientManagementAssert(self.html, self.driver)

    def deleteClient(self, name, module=False, tab=False):
        if module:
            self.menu.openClientManagement()
            self.html.clickElement('Törzsvendégek', 'a')
        elif tab:
            self.html.clickElement('Törzsvendégek', 'a')

        self.html.wait(2)
        self.html.search(name, 'Törzsvendégek')
        self.html.wait(2)
        self.html.clickTableElement('frequenters', 'id', name, 'a', 'Törlés')
        self.html.wait(2)
        self.html.clickElement('Igen')
        self.html.wait(2)
        self.html.search('', 'Törzsvendégek')
        self.html.wait(2)




