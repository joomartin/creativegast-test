from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from core.Options import Options
from receiving.ReceivingAssert import ReceivingAssert
from shared.TestData import TestData as td


class ReceivingSeed():

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.receivingAssert = ReceivingAssert(self.html, self.driver)

    def createPartner(self, name, id,  module=False, tab = False):
        if module:
            self.menu.openReceiving()
            self.html.clickElement('Beszállítók', 'a')
        if tab:
            self.html.clickElement('Beszállítók', 'a')


        self.html.clickElement('Új beszállító', 'a')

        self.html.switchFrame('iframe')

        self.html.fillInput('Beszállító neve', name)
        self.html.fillInput('Belső azonosító', id)

        self.html.clickElement('Rögzít')

        self.html.switchFrame()

        self.receivingAssert.assertPartnerExist(name, 'Beszállítók')

    def deleteParter(self, partnerName,  module=False, tab = False):
        if module:
            self.menu.openReceiving()
            self.html.clickElement('Beszállítók', 'a')
        if tab:
            self.html.clickElement('Beszállítók', 'a')

        self.html.search(partnerName, 'Beszállítók')

        self.html.clickElement(None,
                               '//table[@id="partners"]//tr[contains(.,"' + partnerName +'")]//label',
                               Options(uniqueSelector=True))
        self.html.clickElement('deletePartners', options=Options(htmlAttribute='id'))
        self.html.clickElement('Igen')
        self.html.refresh()

        self.receivingAssert.assertPartnerNotExist(partnerName,'Beszállítók')