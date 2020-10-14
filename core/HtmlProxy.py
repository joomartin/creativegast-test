from selenium.webdriver.support.ui import Select


class HtmlProxy:

    def __init__(self, driver):
        self.driver = driver

    def clickElement(self, target, tag='button', options={}):
        # options : exactMatch: True/False, following:True/False, following: the tag next to the clickable item
        element = self.getElement(target, tag, options)
        element.click()

    def fillInput(self, target, value, selector='label', options={}):
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
        self.clearInput(target, selector, options)

        if selector != 'label':
            self.getElement(target, 'input', options={'htmlAttribute': selector}).send_keys(value)
            return

        self.getElement(target, selector, options={'following': 'input', 'exactMatch': options.get('exactMatch', False)}).send_keys(value)

    def clickDropdown(self, labelTxt, selectValue):
        """
        Select value from dropdown button
        :param labelTxt: It's next to dropdown button
        :type labelTxt: String
        :param selectValue: This is what we want to select
        :type selectValue: String
        """
        # TODO: Maybe we need exact match in the future
        self.getElement(labelTxt, 'label', options={'following': 'button'}).click()
        self.getElement(selectValue, 'label').click()

    def switchFrame(self, tagName=""):
        """
        Frame switch method
        :param tagName: If it's empty(default) we'll switch to default content, otherwise we'll switch to frame that its tag is tagName
        :type tagName: String
        """
        if not tagName:
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(self.driver.find_element_by_tag_name(tagName))

    def getElement(self, target, tag, options={}):

        if options.get('uniqueSelector', False):
           return self.driver.find_element_by_xpath(tag)

        if options.get('htmlAttribute', False) and options.get('exactMatch', False):
            raise ValueError('exactMatch must be false while using htmlAttribute')

        if options.get('htmlAttribute', False):
            xpath = '//' + tag + '[@' + options.get('htmlAttribute') + '="' + target + '"]'
            xpath = self.appendFollowing(xpath, options)

            return self.driver.find_element_by_xpath(xpath)

        xpath = self.getXpathByExactMatch(tag, target, options)
        xpath = self.appendFollowing(xpath, options)

        return self.driver.find_element_by_xpath(xpath)

    def appendFollowing(self, xpath, options={}):
        if options.get('following', False):
            xpath += '//following::' + options.get('following', 'a')

        return xpath

    def getXpathByExactMatch(self, selector, target, options={}):
        if options.get('exactMatch', False):
            return '//' + selector + '[text() = "' + target + '"]'
        else:
            return '//' + selector + '[contains(.,"' + target + '")]'


    def getElementInTable(self, searchText, byClass):
        # return self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']".format("1newWH"))
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

    def clearInput(self, target, selector='label', options={}):
        if selector != 'label':
            self.driver.find_element_by_xpath('//input[@' + selector + ' = "' + target + '"]').clear()
            return

        if options.get('exactMatch', False):
            self.driver.find_element_by_xpath('//label[text() = "' + target + '"]//following::input').clear()
        else:
            self.driver.find_element_by_xpath('//label[contains(.,"' + target + '")]//following::input').clear()

    def pressKey(self, target, tag, key, options={}):
        self.getElement(target, tag, options).send_keys(key)



