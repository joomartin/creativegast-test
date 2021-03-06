from datetime import datetime
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from core.Options import Options
from shared.TestData import TestData as data


class HtmlProxy:
    currWindow = None

    def __init__(self, driver):
        self.driver = driver

    def clickElement(self, target, tag='button', options=Options(), waitSeconds=0):
        self.getElement(target, tag, options).click()
        self.wait(waitSeconds)

    def getInput(self, target, selector, options=Options()):
        if selector != 'label':
            if self.getOption(options, 'htmlAttribute'):
                htmlAttribute = self.getOption(options, 'htmlAttribute')
                return self.getElement(target, selector, Options(htmlAttribute=htmlAttribute, element=self.getOption(options, 'element')))
            else:
                return self.getElement(target, 'input', Options(htmlAttribute=selector, element=self.getOption(options, 'element')))

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

        elem = self.getInput(target, selector, options)
        self.clearInput(target, selector, options)
        elem.send_keys(value)

    def clickDropdown(self, target, selectValue, selector='label', options=Options()):
        """
        Select value from dropdown button
        :param target: It's next to dropdown button
        :type target: String
        :param selectValue: This is what we want to select
        :type selectValue: String
        """
        if self.getOption(options, 'element') is not None:
            self.getElement(target, selector, Options(following='button', element=self.getOption(options, 'element'))).click()
            element = self.getElement(target, selector, Options(following='ul', element=self.getOption(options, 'element')))
            self.wait(1)
            element.find_element_by_xpath('.//label[contains(.,"' + selectValue + '")]').click()
        else:
            self.getElement(target, selector, Options(following='button')).click()
            element = self.getElement(target, selector, Options(following='ul', element=self.getOption(options, 'element')))
            self.wait(1)
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
        if self.getOption(options, 'element') is not None:
            element = self.getOption(options, 'element')
        else:
            element = self.driver
        if self.getOption(options, 'uniqueSelector'):
            return element.find_element_by_xpath(tag)

        htmlAttribute = self.getOption(options, 'htmlAttribute')
        exactMatch = self.getOption(options, 'exactMatch')

        if htmlAttribute and exactMatch:
            raise ValueError('exactMatch must be false while using htmlAttribute')

        if htmlAttribute:
            xpath = './/' + tag + '[@' + htmlAttribute + '="' + target + '"]'
            xpath = self.appendFollowing(xpath, options)

            return element.find_element_by_xpath(xpath)

        xpath = self.getXpathByExactMatch(tag, target, options)
        xpath = self.appendFollowing(xpath, options)

        #print(xpath)
        return element.find_element_by_xpath(xpath)

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

    def getElementInTable(self, searchText, id, tab):
        #search(searchText, tab)
        self.search(searchText, tab)
        return self.driver.find_element_by_xpath('//table[@id="' + id + '"]//td[text() = "' + searchText + '"]')

    def getElementTxtInTable(self, searchText, target, tab, attribute='id'):
        self.search(searchText, tab)
        return self.driver.find_element_by_xpath(
            '//table[@' + attribute + '="' + target + '"]//td[text() = "' + searchText + '"]').text

    def getTxtFromTable(self, row, col, tableId = '', options=Options()):
        """
        We can get a value from table that depends on params
        :param row: Table row number
        :type row: Int or string
        :param col: Table column number
        :type col: Int or String
        :return: Cell value
        :rtype: String
        """
        element = self.getOption(options, 'element')
        if element is None:
            if tableId == '':
                return self.driver.find_element_by_xpath('//table//tbody//tr[' + str(row) + ']/td[' + str(col) + ']').text
            else:
                return self.driver.find_element_by_xpath('//table[@id="' + tableId + '"]//tbody//tr[' + str(row) + ']/td[' + str(col) + ']').text
        else:
            if tableId == '':
                # asd = element.find_element_by_xpath('./table/tbody//tr[' + str(row) + ']/td[' + str(col) + ']').text

                return element.find_element_by_xpath('./table/tbody//tr[' + str(row) + ']/td[' + str(col) + ']').text
            else:
                return element.find_element_by_xpath('./table[@id="' + tableId + '"]/tbody/tr[' + str(row) + ']/td[' + str(col) + ']').text


    def getTxtFromListTable(self, row, col, tableId = '', options=Options()):
        """
        We can get a value from table that depends on params
        :param row: Table row number
        :type row: Int or string
        :param col: Table column number
        :type col: Int or String
        :return: Cell value
        :rtype: String
        """
        element = self.getOption(options, 'element')
        htmlAttribute = self.getOption(options, 'htmlAttribute')
        if element is None:
            if htmlAttribute is None:
                return self.driver.find_element_by_xpath('//table//tbody//tr[' + str(row) + ']/td/div[' + str(col) + ']')
            else:
                return self.driver.find_element_by_xpath('//table[@' + htmlAttribute + '="' + tableId + '"]//tbody//tr[' + str(row) + ']/td/div[' + str(col) + ']')
        else:
            if htmlAttribute == '':
                # #asd = element.find_element_by_xpath('./table/tbody//tr[' + str(row) + ']/td[' + str(col) + ']').text

                return element.find_element_by_xpath('./table/tbody//tr[' + str(row) + ']/td/div[' + str(col) + ']')
            else:
                return element.find_element_by_xpath('./table[@' + htmlAttribute + '="' + tableId + '"]/tbody/tr[' + str(row) + ']/td/div[' + str(col) + ']')

    # div version
    def getTxtFromListTable2(self, row, col, tableId = '', options=Options()):
        """
        We can get a value from table that depends on params
        :param row: Table row number
        :type row: Int or string
        :param col: Table column number
        :type col: Int or String
        :return: Cell value
        :rtype: String
        """
        element = self.getOption(options, 'element')
        if element is None:
            return self.driver.find_element_by_xpath('//tbody//tr[' + str(row) + ']/td/div[' + str(col) + ']')

        else:
            # #asd = element.find_element_by_xpath('./table/tbody//tr[' + str(row) + ']/td[' + str(col) + ']').text
            # print('asdasd')
            return element.find_element_by_xpath('//tbody//tr[' + str(row) + ']/td/div[' + str(col) + ']')

    def clearInput(self, target, selector='label', options=Options()):
        input  = self.getInput(target, selector, options)
        input.clear()

        if input.get_attribute('value'):
            input.send_keys(Keys.CONTROL + 'a')
            input.send_keys(Keys.DELETE)

    def pressKey(self, target, tag, key, options=Options()):
        self.getElement(target, tag, options).send_keys(key)

    def getOption(self, options, key):
        if not options:
            options = Options()

        return getattr(options, key)

    def wait(self, seconds = 2):
        sleep(seconds)

    def refresh(self):
        self.driver.refresh()
        self.wait(2)

    def fillAutocomplete(self, target, tag, value, selectValue, selectTag, options):
        self.getElement(target, tag, options).send_keys(value)
        self.wait(10) # ide is johetne explicit wait
        self.clickElement(selectValue, selectTag)

    def fillAutocompleteProduct(self, target, tag, value, selectValue, selectTag, options):
        self.getElement(target, tag, options).send_keys(value)
        self.wait(10) # ide is johetne explicit wait
        ulList = self.getElement('ui-id-1', 'ul', options=Options(htmlAttribute='id'))
        self.clickElement(selectValue, selectTag, options=Options(element=ulList))

    def clickTableElement(self, atrName, atrType, tdText, followingType, targetText, tab=None):
        if tab != None:
            self.search(tdText, tab)
        table = self.getElement(atrName, 'table', Options(htmlAttribute=atrType))
        #print('.//td[contains(., "' + tdText + '")]//following::' + followingType + '[contains(.,"' + targetText + '")]')
        table.find_element_by_xpath('.//td[contains(., "' + tdText + '")]//following::' + followingType +'[contains(.,"' + targetText +'")]').click()
        self.wait(3)

    def clickTableDropdown(self, materialName, target, tab):
        self.search(materialName, tab)
        element = self.getElement(materialName, 'td', Options(following='td[contains(.,"Menü")]'))
        element.find_element_by_xpath('./a').click()
        self.wait(1)
        element2 = element.find_element_by_xpath('./div')
        element2.find_element_by_xpath('./ul/li[contains(.,"' + target + '")]').click()
        self.wait(1)


    def clickTab(self, tab):
        tabList = self.getElement('ui-tabs-nav ui-state-default', 'ul', options=Options(htmlAttribute='class'))
        self.clickElement(tab, 'a', Options(element=tabList))

    def getTab(self, tab):
        # az osszes tabot tartalmazo ul lista // azert, mert mashol is elofprdulhat a tabnev
        tabList = self.getElement('ui-tabs-nav ui-state-default', 'ul', options=Options(htmlAttribute='class'))
        var = self.getElement(tab, 'a', Options(element=tabList))
        href = var.get_attribute('href')
        subResult = href.split('#')

        result = self.getElement(subResult[1], 'div', options=Options(htmlAttribute='id'))

        return result

    def search(self, value, tab):
        self.wait(2)
        try:
            currWindow = self.getTab(tab)
        except NoSuchElementException:
            return

        self.fillInput('searchinput simpleFilterTerm', value, selector='class', options=Options(element=currWindow))
        self.clickElement('Keresés', options=Options(element=currWindow))
        self.wait(2)

    def closeAllert(self):
        a = Alert(self.driver)
        a.accept()

    def getTablePairsExist(self, firstElement, SecondElelment):
        return self.driver.find_element_by_xpath('//tr[contains(., "' + firstElement + '") and contains(., "' + SecondElelment + '")]').is_displayed()

    def getElementPairsExist(self, firstElement, SecondElelment, tag='tr'):
        return self.driver.find_element_by_xpath('//' + tag + '[contains(., "' + firstElement + '") and contains(., "' + SecondElelment + '")]').is_displayed()

    def getRowExist(self, elements):
        xPath = ''
        for index, elem in enumerate(elements):
            if index != len(elements)-1:
                xPath += 'contains(., "' + elem + '") and '
            else:
                xPath += 'contains(., "' + elem + '")'

        return self.driver.find_element_by_xpath('//tr[' + xPath + ']').is_displayed()

    # currently it doesn't work
    def scrollToElement(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView;', element)

    # scroll down to end of the page
    def scroll(self):
        html = self.driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        self.wait(1)

    # it extendds decimals, may it belongs CGSpecific
    def extendedRound(self, number, decimals):
        return eval('"%.' + str(int(decimals)) + 'f" % ' + repr(number))

    def getElements(self, target, tag, options=Options()):
        if self.getOption(options, 'element') is not None:
            element = self.getOption(options, 'element')
        else:
            element = self.driver
        if self.getOption(options, 'uniqueSelector'):
                return element.find_elements_by_xpath(tag)

        htmlAttribute = self.getOption(options, 'htmlAttribute')
        exactMatch = self.getOption(options, 'exactMatch')

        if htmlAttribute and exactMatch:
            raise ValueError('exactMatch must be false while using htmlAttribute')

        if htmlAttribute:
            xpath = './/' + tag + '[@' + htmlAttribute + '="' + target + '"]'
            xpath = self.appendFollowing(xpath, options)

            return element.find_elements_by_xpath(xpath)

        xpath = self.getXpathByExactMatch(tag, target, options)
        xpath = self.appendFollowing(xpath, options)

        return element.find_elements_by_xpath(xpath)

    def screenshot(self, name):
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.driver.get_screenshot_as_file(
            './/screenShots//' + data.Screenshot['Name'] + '//' + name + '-%s.png' % now)

    def explicitWaitXpath(self, xpath, time=60, mode='clickable'):
        wait = WebDriverWait(self.driver, time)
        if mode == 'clickable':
            wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
        elif mode == 'visible':
            wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))

