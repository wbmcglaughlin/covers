import os
import appdirs
import pathlib
import configparser
from constant import app_author, app_name


def get_persistent_data_path():
    path = pathlib.Path(appdirs.user_data_dir(appauthor=app_author, appname=app_name))
    if not os.path.exists(path):
        os.mkdir(path)

    return path

def make_configurations_folder():
    config_folder_path = get_configurations_folder()
    if not os.path.exists(config_folder_path):
        os.mkdir(config_folder_path)

def get_configurations_folder():
    return get_persistent_data_path() / 'configurations'


def get_configurations_file():
    return get_configurations_folder() / 'user_configurations.ini'


def make_configurations_file():
    config_file = get_configurations_file()
    if not os.path.exists(config_file):
        open(config_file, 'w+')


def prepare_configurations():
    make_configurations_folder()
    make_configurations_file()


def init_configurations():
    make_configurations_folder()
    make_configurations_file()

    config = configparser.ConfigParser()

    config.read(get_configurations_file())

    if 'UserConfigurations' not in config:
        config['UserConfigurations'] = {}

    with open(get_configurations_file(), 'w') as configfile:
        config.write(configfile)
