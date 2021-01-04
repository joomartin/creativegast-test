from selenium.common.exceptions import NoSuchElementException

from core.HtmlProxy import HtmlProxy
from selenium import webdriver

class CGSpecific:

    html = HtmlProxy(webdriver)

    def search(self, value, tab):
        self.html.wait(2)
        try:
            currWindow = self.html.getTab(tab)
        except NoSuchElementException:
            return

        self.html.fillInput('searchinput simpleFilterTerm', value, selector='class', element=currWindow)
        self.html.clickElement('Keresés', element=currWindow)
        self.html.wait(2)


