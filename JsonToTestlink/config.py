import configparser
import logging
import os


module_logger = logging.getLogger("json_to_testlink.config")


def create_config(path):
    """
    Create a config file
    """
    logger = logging.getLogger("json_to_testlink.config.create_config")
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "testlink_server_ip", "[YOUR TL SERVER IP]")
    config.set("Settings", "testlink_server_port", "")
    config.set("Settings", "testlink_api_url", "[YOUR TL API URL]]")
    config.set("Settings", "dev_key", "[from TL user settings]")
    config.set("Settings", "testlink_user", "[TL USER NAME]")
    config.set("Settings", "testlink_password", "admin")
    config.set("Settings", "testlink_project_name", "[YOUR TL PROJECT NAME]")
    config.set("Settings", "testlink_test_project_prefix", "awn")
    config.set("Settings", "testlink_testsuite_id", "[YOUR TL SUITE ID]")
    config.set("Settings", "testlink_testplan_id", "[YOUR TL TEST PLAN ID]")
    config.set("Settings", "testlink_build_id", "[YOUR TL BUILD ID]")
    config.set("Settings", "testlink_info",
               "You are reporting to testlink: %(testlink_server_ip)s "
               "at port: %(testlink_server_port)s "
               "and full api url: %(testlink_api_url)s ")

    with open(path, "w") as config_file:
        config.write(config_file)
    logger.info('Config created')


def get_config(path):
    """
    Returns the config object
    """
    logger = logging.getLogger("json_to_testlink.config.get_config")
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    logger.debug('Config read done')
    return config


def get_setting(path, section, setting, msg=0):
    """
    Print out a setting
    """
    logger = logging.getLogger("json_to_testlink.config.get_setting")
    config = get_config(path)
    value = config.get(section, setting)
    if msg:
        msg = "{section} {setting} is {value}".format(
            section=section, setting=setting, value=value
        )
    logger.info('Get setting: ' + setting)
    return value


def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    logger = logging.getLogger("json_to_testlink.config.update_setting")
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)
    logger.info('Updated setting: ' + setting)


def delete_setting(path, section, setting):
    """
    Delete a setting
    """
    logger = logging.getLogger("json_to_testlink..config.delete_setting")
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "w") as config_file:
        config.write(config_file)
    logger.info('Deleted setting: ' + setting)
