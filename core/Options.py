

class Options:

    def __init__(self, following='', exactMatch=False, uniqueSelector=False, htmlAttribute='', element=None):
        '''

        :param following:
        :type following: string
        :param exactMatch:
        :type exactMatch: bool
        :param uniqueSelector:
        :type uniqueSelector: string
        :param htmlAttribute:
        :type htmlAttribute: string
        '''
        self.following = following
        self.exactMatch = exactMatch
        self.uniqueSelector = uniqueSelector
        self.htmlAttribute = htmlAttribute
        self.element = element

