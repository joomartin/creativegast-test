from configparser import ConfigParser


def read_section(section, filename='config.ini'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            config[item[0]] = item[1]
    else:
        raise Exception('{0} not found in {1} file'.format(section, filename))

    return config