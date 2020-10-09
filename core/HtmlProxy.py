from selenium.webdriver.support.ui import Select


class HtmlProxy:

    def __init__(self, driver):
        self.driver = driver


    def clickElement(self, target, selector = 'button', options = {}):
        #options : exactMatch: True/False, following:True/False, following: the tag next to the clickable item
        if options.get('uniqueSelector',False):
            self.driver.find_element_by_xpath(selector).click()
            return

        if options.get('following',False):
            if options.get('exactMatch', False):
                self.driver.find_element_by_xpath('//' + selector + '[text() = "' + target + '"]//following::'+options.get('following','a')).click()
            else:
                self.driver.find_element_by_xpath('//' + selector + '[contains(.,"' + target + '")]//following::'+options.get('following','a')).click()
        else:
            if options.get('exactMatch', False):
                self.driver.find_element_by_xpath('//' + selector + '[text() = "' + target + '"]').click()
            else:
                self.driver.find_element_by_xpath('//' + selector + '[contains(.,"' + target + '")]').click()




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
            self.clearInput(target, selector)
            self.driver.find_element_by_xpath('//input[@' + selector + ' = "' + target + '"]').send_keys(value)
            return

        self.clearInput(target, selector, options)
        if options.get('exactMatch', False):
            self.driver.find_element_by_xpath('//label[text() = "' + target + '"]//following::input').send_keys(value)
        else:
            self.driver.find_element_by_xpath('//label[contains(.,"' + target + '")]//following::input').send_keys(value)



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


    def clearInput(self, target, selector = 'label', options = {}):
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


