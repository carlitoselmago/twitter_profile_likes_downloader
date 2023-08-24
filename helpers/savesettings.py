import configparser
import os

def create_config(config_file_path, user, pwd):
    config = configparser.ConfigParser()
    config.add_section('Credentials')
    config.set('Credentials', 'user', user)
    config.set('Credentials', 'pwd', pwd)
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)


config_file_path = 'settings.ini'
config = configparser.ConfigParser()
if os.path.isfile(config_file_path):
    config.read(config_file_path)
    user = config.get('Credentials', 'user')
    pwd = config.get('Credentials', 'pwd')
    print('Settings loaded: User - {}, Password - {}'.format(user, pwd))
else:
    print("settings.ini doesn't exist, introduce your Twitter user and password and the data will be stored for next time")
    user = input('Enter user: ')
    pwd = input('Enter password: ')
    create_config(config_file_path, user, pwd)
    print('Settings saved in settings.ini file.')

