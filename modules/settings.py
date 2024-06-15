import configparser

def load_settings_from_ini():
    config = configparser.ConfigParser()
    config.read('config.ini')

    for section in config.sections():
        for key, value in config.items(section):
            if key.startswith('l_'):
                value = [item.strip() for item in value.split(',')]
            globals()[key.upper()] = value