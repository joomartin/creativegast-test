from configparser import ConfigParser
import os


def read_section(section='default', filename='config.ini'):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    path = ROOT_DIR + '/' + filename

    parser = ConfigParser()
    parser.read(path)

    config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            config[item[0]] = item[1]
    else:
        raise Exception('{0} not found in {1} file'.format(section, filename))

    return config