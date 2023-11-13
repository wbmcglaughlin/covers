import os
import pathlib
import configparser
import appdirs

from src.constant import app_author, app_name


def get_persistent_data_path():
    """Get persistent data path using app author and app name.

    :return pathlib.Path: persistent data path.
    """
    path = pathlib.Path(appdirs.user_data_dir(appauthor=app_author, appname=app_name))
    path.mkdir(exist_ok=True)

    return path


def get_configurations_folder():
    """Get configurations folder.

    :return _type_: _description_
    """
    config_folder = get_persistent_data_path() / 'configurations'
    config_folder.mkdir(exist_ok=True)

    return config_folder


def get_configurations_file():
    """Get file containing configurations.

    :return pathlib.Path: config file path.
    """
    config_file = get_configurations_folder() / 'user_configurations.ini'
    if not os.path.exists(config_file):
        open(config_file, 'w+', encoding='utf-8')

    return config_file


def init_configurations():
    """Init configurations.
    """
    config_file = get_configurations_file()

    config = configparser.ConfigParser()

    config.read(config_file)

    if 'UserConfigurations' not in config:
        config['UserConfigurations'] = {}

        with open(config_file, 'w', encoding="UTF-8") as configfile:
            config.write(configfile)

    return config
