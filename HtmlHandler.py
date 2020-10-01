from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest


class HtmlHandler:

    def __init__(self, driver):
        self.driver = driver

    def clickElementByText(self, text='', tag='button'):
        #driver.find_element_by_xpath('//"' + type + '"[contains(., "' + text + '")]').click()
        self.driver.find_element_by_xpath('//' + tag + '[text() = "' + text + '"]').click()


    def fillInput(self, attribute='', message='', searchType='name'):
        if searchType == 'name':
            self.driver.find_element_by_name(attribute).clear()
            self.driver.find_element_by_name(attribute).send_keys(message)
        elif searchType == 'id':
            self.driver.find_element_by_id(attribute).clear()
            self.driver.find_element_by_id(attribute).send_keys(message)


    def fillInputByPlaceholder(self, placeholder='', message=''):
        self.driver.find_element_by_xpath('//input[@placeholder = "' + placeholder + '"]').send_keys(message)


    def fillInputFollowing(self, labelText='', message='', searchType='label', followNum=1, followType='input'):
        followString = ''
        for i in range(followNum):
            followString += '//following::' + followType

        self.driver.find_element_by_xpath('//' + searchType + '[text() = "' + labelText + '"]' + followString + '').send_keys(message)


    # Dropwdown select method
    def dropdownSelect(self, text, searchValue, method='text', tag='button'):
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




    def clear(self, text='', searchType='name'):
        pass
        #self.driver.find_element_by_name(text).send_keys(message)













