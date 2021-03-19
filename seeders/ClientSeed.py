
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

    def createClient(self, name, code, phone, discount, taxnumber, country, postalCode, city, street, houseNumber, tab=False):
        if tab:
            self.html.clickElement('Házhozszállítási cím', 'a')

        self.html.clickElement('Új házhozszállítási cím', 'a', waitSeconds=2)

        self.html.switchFrame('iframe')
        self.html.fillInput('Név / azonosító', name)
        self.html.fillInput('Ügyfélazonosító', code)
        self.html.fillInput('Telefon', phone)
        self.html.fillInput('Kedv. (%)', discount)
        self.html.fillInput('Adószám', taxnumber)

        self.html.fillInput('ca_country_helper', country, 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_zip_helper', postalCode, 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_city_helper', city, 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_street_helper', street, 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_housenumber_helper', houseNumber, 'input',
                            options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít', waitSeconds=2)
        self.html.switchFrame()
        address = country + ', ' + postalCode + ' ' + city + ' ' + street + ' ' + houseNumber

        return address

    def createRegular(self, name, code, phone, discount, taxnumber, country, postalCode, city, street, houseNumber, module=False, tab=False):
        if module:
            self.menu.openClientManagement()
            self.html.clickElement('Törzsvendégek', 'a')
        if tab:
            self.html.clickElement('Törzsvendégek', 'a')

        self.html.clickElement('Új törzsvendég', 'a', waitSeconds=2)

        self.html.switchFrame('iframe')
        self.html.fillInput('Név / azonosító', name)
        self.html.fillInput('Ügyfélazonosító', code)
        self.html.fillInput('Telefon', phone)
        self.html.fillInput('Kedv. (%)', discount)
        self.html.fillInput('Adószám', taxnumber)

        self.html.fillInput('ca_country_helper', country, 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_zip_helper', postalCode, 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_city_helper', city, 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_street_helper', street, 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_housenumber_helper', houseNumber, 'input',
                            options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít', waitSeconds=2)
        self.html.switchFrame()
        address = country + ', ' + postalCode + ' ' + city + ' ' + street + ' ' + houseNumber

        return address

    def deleteRegular(self, name, module=False, tab=False):
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

    def deleteCard(self, name, module=False, tab=False):
        if module:
            self.menu.openClientManagement()
            self.html.clickElement('Kedvezménykártyák', 'a')
        elif tab:
            self.html.clickElement('Kedvezménykártyák', 'a')

        self.html.wait(2)
        self.html.search(name, 'Kedvezménykártyák')
        self.html.wait(2)
        self.html.clickTableElement('discount_cards', 'id', name, 'a', 'Törlés')
        self.html.wait(2)
        self.html.clickElement('Igen')
        self.html.wait(2)
        self.html.search('', 'Kedvezménykártyák')
        self.html.wait(2)

    def deleteClient(self, name, module=False, tab=False):
        if module:
            self.menu.openClientManagement()
            self.html.clickElement('Házhozszállítási cím', 'a')
        elif tab:
            self.html.clickElement('Házhozszállítási cím', 'a')

        self.html.wait(2)
        self.html.search(name, 'Házhozszállítási cím')
        self.html.wait(2)
        self.html.clickTableElement('frequenters', 'id', name, 'a', 'Törlés')
        self.html.wait(2)
        self.html.clickElement('Igen')
        self.html.wait(2)
        self.html.search('', 'Törzsvendégek')
        self.html.wait(2)