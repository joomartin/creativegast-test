from selenium.webdriver.support.ui import Select


class HtmlProxy:

    def __init__(self, driver):
        self.driver = driver

    def clickElement(self, target, selector='button', options={}):
        # options : exactMatch: True/False, following:True/False, following: the tag next to the clickable item
        element = self.getElement(target, selector, options)
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
            self.driver.find_element_by_xpath('//input[@' + selector + ' = "' + target + '"]').send_keys(value)
            return

        if options.get('exactMatch', False):
            self.driver.find_element_by_xpath('//label[text() = "' + target + '"]//following::input').send_keys(value)
        else:
            self.driver.find_element_by_xpath('//label[contains(.,"' + target + '")]//following::input').send_keys(
                value)

    def clickDropdown(self, labelTxt, selectValue):
        """
        Select value from dropdown button
        :param labelTxt: It's next to dropdown button
        :type labelTxt: String
        :param selectValue: This is what we want to select
        :type selectValue: String
        """
        # TODO: Maybe we need exact match in the future
        self.driver.find_element_by_xpath("//label[contains(.,'" + labelTxt + "')]//following::button").click()
        self.driver.find_element_by_xpath("//label[contains(.,'" + selectValue + "')]").click()

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

    def getElement(self, target, selector, options={}):

        if options.get('uniqueSelector', False):
           return self.driver.find_element_by_xpath(selector)

        if options.get('htmlAttribute',False):
            xpath = '//' + selector + '[@'+options.get('htmlAttribute','id')+'="'+target+'"]'
            return self.driver.find_element_by_xpath(xpath)

        if options.get('exactMatch', False):
            xpath = '//' + selector + '[text() = "' + target + '"]'
        else:
            xpath = '//' + selector + '[contains(.,"' + target + '")]'

        if options.get('following', False):
            xpath += '//following::' + options.get('following', 'a')

        return self.driver.find_element_by_xpath(xpath)

    def getElementByClassName(self, className):
        return self.driver.find_element_by_class_name(className)

    def getElementByTag(self, tag):
        return self.driver.find_element_by_tag_name(tag)

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

    def pressKey(self, className, key):
        self.getElementByClassName(className).send_keys(key)

    def pressKeyWithTag(self, tag, key):
        self.getElementByTag(tag).send_keys(key)

