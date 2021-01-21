from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options
from receiving.ReceivingAssert import ReceivingAssert
from shared.TestData import TestData as td


class RestaurantSeed():

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.receivingAssert = ReceivingAssert(self.html, self.driver)

    def createTable(self, tableName, tableShape='Kör', tableType='Normál', module=False):
        if module:
            self.menu.openTableMapEditor()

        self.html.clickElement( tableShape + ' asztal hozzáadása', 'a', Options(htmlAttribute='title'))
        self.html.refresh()

        self.html.clickElement('Étterem', 'i')


        self.html.fillInput('Asztal neve', tableName)

        if not tableType == 'Normál':
            self.html.clickDropdown('Asztal típusa', tableType)

        self.html.clickElement('Rögzít', 'span')  # Span-t kell használni mert valamiért 'Rögzít' buttonból van egy amit előbb megtalál és az nem interactable

    def deleteTable(self, tableName, module=False):
        if module:
            self.menu.openTableMapEditor()

        self.html.clickElement(tableName, 'i')

        self.html.clickElement('Törlés', 'span') # ugyan az az állás mint a fenti kommentnél
        self.html.clickElement('Igen')

