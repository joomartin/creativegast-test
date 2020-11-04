from time import sleep

from selenium.webdriver.common.keys import Keys
from core.Options import Options


class HtmlProxy:
    currWindow = None

    def __init__(self, driver):
        self.driver = driver

    def clickElement(self, target, tag='button', options=Options(), waitSeconds=0, element = None):
        self.getElement(target, tag, options, element).click()
        self.wait(waitSeconds)

    def getInput(self, target, selector, options=Options(), element=None):
        if selector != 'label':
            return self.getElement(target, 'input', Options(htmlAttribute=selector), element)

        options.following = 'input'
        return self.getElement(target, selector, options, element)

    def fillInput(self, target, value, selector='label', options=Options(), element = None):
        '''
        :param target: The value that we are looking for
        :type target: String
        :param value:
        :type value:
        :param selector:
        :type selector:
        :param options:
        :type options:
        :return:
        :rtype:
        '''

        elem = self.getInput(target,selector,options, element)
        self.clearInput(target,selector,options, element)
        elem.send_keys(value)

    def clickDropdown(self, target, selectValue, selector='label'):
        """
        Select value from dropdown button
        :param target: It's next to dropdown button
        :type target: String
        :param selectValue: This is what we want to select
        :type selectValue: String
        """
        self.getElement(target, selector, Options(following='button')).click()
        element = self.getElement(target, selector, Options(following='ul'))
        element.find_element_by_xpath('.//label[contains(.,"' + selectValue + '")]').click()

    def switchFrame(self, tagName=None):
        """
        Frame switch method
        :param tagName: If it's empty(default) we'll switch to default content, otherwise we'll switch to frame that its tag is tagName
        :type tagName: String
        """
        if not tagName:
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(self.driver.find_element_by_tag_name(tagName))

        self.wait(2)

    def getElement(self, target, tag, options=Options(), element = None):
        if self.getOption(options,'uniqueSelector'):
            if element:
                return element.find_element_by_xpath(tag)
            else:
                return self.driver.find_element_by_xpath(tag)

        htmlAttribute = self.getOption(options,'htmlAttribute')
        exactMatch = self.getOption(options,'exactMatch')

        if htmlAttribute and exactMatch:
            raise ValueError('exactMatch must be false while using htmlAttribute')

        if htmlAttribute:
            xpath = './/' + tag + '[@' + htmlAttribute + '="' + target + '"]'
            xpath = self.appendFollowing(xpath, options)

            if element:
                return element.find_element_by_xpath(xpath)
            else:
                return self.driver.find_element_by_xpath(xpath)

        xpath = self.getXpathByExactMatch(tag, target, options)
        xpath = self.appendFollowing(xpath, options)

        if element:
            return element.find_element_by_xpath(xpath)
        else:
            return self.driver.find_element_by_xpath(xpath)

    def appendFollowing(self, xpath, options=Options()):
        following = self.getOption(options, 'following')
        if following:
            xpath += '//following::' + following

        return xpath

    def getXpathByExactMatch(self, tag, target, options=Options()):
        exactMatch = self.getOption(options, 'exactMatch')
        if exactMatch:
            return './/' + tag + '[text() = "' + target + '"]'
        else:
            return './/' + tag + '[contains(.,"' + target + '")]'

    def getElementInTable(self, searchText, byClass, tab):
        self.search(searchText, tab)
        return self.driver.find_element_by_xpath('//td[@class="' + byClass + '"][text() = "' + searchText + '"]')

    def getTxtFromTable(self, row, col):
        """
        We can get a value from table that depends on params
        :param row: Table row number
        :type row: Int or string
        :param col: Table column number
        :type col: Int or String
        :return: Cell value
        :rtype: String
        """
        return self.driver.find_element_by_xpath("//table//tbody//tr[" + str(row) + "]/td[" + str(col) + "]").text

    def clearInput(self, target, selector='label', options=Options(), element = None):
        input  = self.getInput(target, selector, options, element)
        input.clear()

        if input.get_attribute('value'):
            input.send_keys(Keys.CONTROL + 'a')
            input.send_keys(Keys.DELETE)

    def pressKey(self, target, tag, key, options=Options()):
        self.getElement(target, tag, options).send_keys(key)

    def getOption(self, options, key):
        if not options :
            options = Options()

        return getattr(options, key)

    def wait(self, seconds = 2):
        sleep(seconds)

    def refresh(self):
        self.driver.refresh()
        self.wait(2)

    def fillAutocomplete(self, target, tag, value, selectValue, selectTag, options):
        self.getElement(target, tag, options).send_keys(value)
        self.wait(3)
        self.clickElement(selectValue, selectTag)

    def clickTableElement(self, atrName, atrType, tdText, followingType, targetText, tab):
        self.search(tdText, tab)
        table = self.getElement(atrName, 'table', Options(htmlAttribute=atrType))
        table.find_element_by_xpath('.//td[contains(., "' + tdText + '")]//following::' + followingType +'[contains(.,"' + targetText +'")]').click()
        '''
        table = self.html.getElement('barchecking', 'table', Options(htmlAttribute='id'))
        table.find_element_by_xpath('.//td[contains(., "Admin Admin")]//following::a[contains(.,"Megtekintés")]').click()
        '''

    def clickTableDropdown(self, materialName, target, tab):
        self.search(materialName, tab)
        element = self.getElement(materialName, 'td', Options(following='td[contains(.,"Menü")]'))
        element.find_element_by_xpath('./a').click()
        self.wait(1)
        element2 = element.find_element_by_xpath('./div')
        element2.find_element_by_xpath('./ul/li[contains(.,"' + target + '")]').click()
        self.wait(1)

    def getTab(self, tab):
        # az osszes tabot tartalmazo ul lista // azert, mert mashol is elofprdulhat a tabnev
        tabList = self.getElement('ui-tabs-nav ui-state-default', 'ul', options=Options(htmlAttribute='class'))
        var = self.getElement(tab, 'a', element = tabList)
        href = var.get_attribute('href')
        subResult = href.split('#')

        result = self.getElement(subResult[1], 'div', options=Options(htmlAttribute='id'))

        return result

    def search(self, value, tab):
        currWindow = self.getTab(tab)

        self.fillInput('searchinput simpleFilterTerm', value, selector = 'class', element = currWindow)
        self.clickElement('Keresés', element = currWindow)
        self.wait(2)

