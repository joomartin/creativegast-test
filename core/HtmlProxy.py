from selenium.webdriver.support.ui import Select


class HtmlProxy:

    def __init__(self, driver):
        self.driver = driver


    def clickElement(self, text, tag='button', exactMatch=False):
        """

        :param text: Text what we want to find
        :type text: String
        :param tag: Type of tag
        :type tag: String
        :param exactMatch: If True we want to find the text in this tag otherwise in altag
        :type exactMatch: Boolean
        """
        if not exactMatch:
            self.driver.find_element_by_xpath('//' + tag + '[contains(., "' + text + '")]').click()
        else:
            self.driver.find_element_by_xpath('//' + tag + '[text() = "' + text + '"]').click()


    def click(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()



    def clickElementFollowing(self, tagText, tag='label', followNum=1, followType='a', byClass=''):
        """

        :param labelText: Next to target
        :type labelText:  String
        :param tag: Type of tag
        :type tag: String
        :param followNum: How many following
        :type followNum: Int
        :param followType: Type of followed tag
        :type followType: String
        :param byClass: A switch. If it's not empty then method use class tag too.
        :type byClass: String
        """
        followString = ''
        for i in range(followNum):
            followString += '//following::' + followType

        if byClass == '':
            self.driver.find_element_by_xpath('//' + tag + '[text() = "' + tagText + '"]' + followString + '').click()
        else:
            self.driver.find_element_by_xpath('//' + tag + '[@class="' + byClass + '"][text() = "' + tagText + '"]' + followString + '').click()



    def fillInput(self, target, value, selector = 'label', options = {}):
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
        if selector != 'label':
            self.driver.find_element_by_xpath('//input[@' + selector + ' = "' + target + '"]').send_keys(value)
            return

        if options.get('exactMatch', False):
            self.driver.find_element_by_xpath('//label[text() = "' + target + '"]//following::input').send_keys(value)
        else:
            self.driver.find_element_by_xpath('//label[contains(.,"' + target + '")]//following::input').send_keys(value)


    def fillInputByPlaceholder(self, placeholder, message):
        """
        Fill input field with a text
        :param placeholder: Placeholder
        :type placeholder: String
        :param message: With which we want to fill input field
        :type message: String
        """
        self.fillInput(placeholder, message, selector='placeholder')



    def fillInputByLabel(self, labelText, message, followNum=1, exactMatch=False):
        """
        Fill input field
        :param labelText: It's next to target input
        :type labelText: String
        :param message: What we want to put to input field
        :type message: String
        :param followNum: How many follow
        :type followNum: Int
        :param exactMatch: If True we want to find the exact labelText
        :type exactMatch: Boolean
        """

        self.fillInput(labelText, message, options={exactMatch: exactMatch})


    # Dropwdown select method
    def clickBasicDropdown(self, text, searchValue, method='text', tag='button'):
        """
        :param method: initially it's text, other opportunities: index, value
        :param text: visiable name of the dropdown element, usually element is button
        :param searchValue: this is what we want to find/select in any method case
        :param tag: type of tag that includes the text
        """

        element = self.driver.find_element_by_xpath('//' + tag + '[text() = "' + text + '"]')
        drp=Select(element)

        if method == 'text':
            drp.select_by_visible_text(searchValue)
        elif method == 'index':
            drp.select_by_index(int(searchValue))
        elif method == 'value':
            drp.select_by_value(searchValue)


    # Switch to alert message
    def treatAlertMessage(self, accept=True):
        """
        :param accept: If it's True, then we accept the alert
        :type accept: Boolean
        """
        if accept:
            self.driver.switch_to_alert().accept()
        else:
            self.driver.switch_to_alert().dismiss()


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

    def getElement(self, tag, searchText, exactMatch=False):
        '''
        :param tag: Type of tag that includes the text
        :type tag: String
        :param searchText: The text to find
        :type searchText: String
        :param exactMatch: Specifies if we need an exact match or not
        :type exactMatch: bool
        :return: returns the found element
        :rtype: webelement
        '''
        if not exactMatch:
            element = self.driver.find_element_by_xpath("//" + tag + "[contains(., '" + searchText + "')]")
            return element
        else:
            element = self.driver.find_element_by_xpath("//" + tag + "[text() = '" + searchText + "']")
            return element


    def getElementByClassName(self, className):
        return self.driver.find_element_by_class_name(className)

    def getElementByTag(self, tag):
        return self.driver.find_element_by_tag_name(tag)


    def getElementInTable(self, searchText, byClass):
        #return self.driver.find_element_by_xpath("//table[@id='storages']/tbody/tr[td = '{}']".format("1newWH"))
        return self.driver.find_element_by_xpath('//td[@class="' + byClass + '"][text() = "' + searchText + '"]')


    def clearInputByLabel(self, labelText, followNum=1, exactMatch=False):
        followString = ''
        for i in range(followNum):
            followString += '//following::input'

        if not exactMatch:
            self.driver.find_element_by_xpath("//label[contains(.,'" + labelText + "')]" + followString).clear()
        else:
            self.driver.find_element_by_xpath('//label[text() = "' + labelText + '"]' + followString).clear()

    def pressKey(self, className, key):
        self.getElementByClassName(className).send_keys(key)


    '''
    def fillInput(self, attribute='', message='', searchType='name'):
        if searchType == 'name':
            self.driver.find_element_by_name(attribute).clear()
            self.driver.find_element_by_name(attribute).send_keys(message)
        elif searchType == 'id':
            self.driver.find_element_by_id(attribute).clear()
            self.driver.find_element_by_id(attribute).send_keys(message)

    '''
    '''
    def fillInput(self, labelTxt, inputTxt):
        self.driver.find_element_by_xpath("//label[contains(.,'" + labelTxt + "')]//following::input").send_keys(
            inputTxt)
    '''


    '''
    def getElement(self, text, tag='button', exactMatch=False):

        returner = None

        if not exactMatch:
            self.driver.find_element_by_xpath('//' + tag + '[contains(., "' + text + '")]').click()
        else:
            self.driver.find_element_by_xpath('//' + tag + '[text() = "' + text + '"]').click()

        return returner
    '''


