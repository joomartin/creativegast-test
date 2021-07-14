from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options
from receiving.ReceivingAssert import ReceivingAssert
from shared.TestData import TestData as td


class RestaurantSeed:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.receivingAssert = ReceivingAssert(self.html, self.driver)

    def createTable(self, tableName, tableShape='Kör', tableType='Normál', discount='0', module=False):
        if module:
            self.menu.openTableMapEditor()

        self.html.clickElement(tableShape + ' asztal hozzáadása', 'a', Options(htmlAttribute='title'))
        self.html.refresh()
        self.html.wait(15)

        self.html.clickElement('Étterem', 'i')
        self.html.fillInput('Asztal neve', tableName)

        if not tableType == 'Normál':
            self.html.clickDropdown('Asztal típusa', tableType)
            if tableType == 'Főnöki' or tableType == 'Személyzeti':
                self.html.fillInput('Kedv.', discount)

        self.html.clickElement('Rögzít', 'span')  # Span-t kell használni mert valamiért 'Rögzít' buttonból van egy amit előbb megtalál és az nem interactable

    def deleteTable(self, tableName, module=False):
        if module:
            self.menu.openTableMapEditor()

        self.html.clickElement(tableName, 'i')

        self.html.clickElement('Törlés', 'span') # ugyan az az állás mint a fenti kommentnél
        self.html.clickElement('Igen')

    def createDynamicCourierTable(self, name):
        self.html.clickElement('+', waitSeconds=1)
        self.html.fillAutocomplete('cl_name', 'input', name, name, 'li', options=Options(htmlAttribute='id'))
        self.html.clickElement('Rögzít', 'span')

    def createDynCTableForNew(self, name, city, street, houseNum, phone):
        self.html.clickElement('+', waitSeconds=1)
        self.html.fillInput('Vendég neve', name)
        self.html.fillAutocomplete('sh_city', 'input', city, city, 'li', options=Options(htmlAttribute='id'))
        self.html.fillInput('Utca', street)
        self.html.fillInput('Házszám', houseNum)
        self.html.wait(2)
        self.html.fillInput('Telefon', phone, options=Options(exactMatch=True))
        self.html.clickElement('Rögzít', 'span')





