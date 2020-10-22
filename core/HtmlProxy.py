from time import sleep

from selenium.webdriver.common.keys import Keys

from core.Options import Options


class HtmlProxy:
    def __init__(self, driver):
        self.driver = driver

    def clickElement(self, target, tag='button', options=Options(), waitSeconds=0):
        self.getElement(target, tag, options).click()
        self.wait(waitSeconds)

    def getInput(self, target, selector, options=Options()):
        if selector != 'label':
            return self.getElement(target, 'input', Options(htmlAttribute=selector))

        options.following = 'input'
        return self.getElement(target, selector, options)

    def fillInput(self, target, value, selector='label', options=Options()):
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
        element = self.getInput(target,selector,options)
        self.clearInput(target,selector,options)
        element.send_keys(value)

    def clickDropdown(self, target, selectValue):
        """
        Select value from dropdown button
        :param target: It's next to dropdown button
        :type target: String
        :param selectValue: This is what we want to select
        :type selectValue: String
        """
        self.getElement(target, 'label', Options(following='button')).click()
        element = self.getElement(target, 'label', Options(following='ul'))
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

    def getElement(self, target, tag, options=Options()):
        if self.getOption(options,'uniqueSelector'):
            return self.driver.find_element_by_xpath(tag)

        htmlAttribute = self.getOption(options,'htmlAttribute')

        exactMatch = self.getOption(options,'exactMatch')

        if htmlAttribute and exactMatch:
            raise ValueError('exactMatch must be false while using htmlAttribute')

        if htmlAttribute:
            xpath = '//' + tag + '[@' + htmlAttribute + '="' + target + '"]'
            xpath = self.appendFollowing(xpath, options)

            return self.driver.find_element_by_xpath(xpath)

        xpath = self.getXpathByExactMatch(tag, target, options)
        xpath = self.appendFollowing(xpath, options)

        return self.driver.find_element_by_xpath(xpath)

    def appendFollowing(self, xpath, options=Options()):
        following = self.getOption(options, 'following')
        if following:
            xpath += '//following::' + following

        return xpath

    def getXpathByExactMatch(self, tag, target, options=Options()):
        exactMatch = self.getOption(options, 'exactMatch')
        if exactMatch:
            return '//' + tag + '[text() = "' + target + '"]'
        else:
            return '//' + tag + '[contains(.,"' + target + '")]'

    def getElementInTable(self, searchText, byClass):
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

    def clearInput(self, target, selector='label', options=Options()):
        input  = self.getInput(target, selector, options)
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
