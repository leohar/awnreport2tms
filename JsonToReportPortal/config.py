import configparser
import logging
import os


module_logger = logging.getLogger("json_to_report_portal.config")


def create_config(path):
    """
    Create a config file
    """
    logger = logging.getLogger("json_to_report_portal.create_config")
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "rp_api_url", "http://[YOUR RP SERVER IP]/api")
    config.set("Settings", "rp_project_name", "[YOUR RP PROJECT NAME]")
    config.set("Settings", "rp_uuid", "[from RP user settings]")
    config.set("Settings", "rp_launch", "[YOUR RP LAUNCH NAME]")
    config.set("Settings", "rp_info",
               "You are reporting to RP: %(rp_api_url)s "
               "to project: %(rp_project_name)s")

    with open(path, "w") as config_file:
        config.write(config_file)
    logger.info('Config created')


def get_config(path):
    """
    Returns the config object
    """
    logger = logging.getLogger("json_to_report_portal.config.get_config")
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
    logger = logging.getLogger("json_to_report_portal.config.get_setting")
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
    logger = logging.getLogger("json_to_report_portal.config.update_setting")
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)
    logger.info('Updated setting: ' + setting)


def delete_setting(path, section, setting):
    """
    Delete a setting
    """
    logger = logging.getLogger("json_to_report_portal.config.delete_setting")
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "w") as config_file:
        config.write(config_file)
    logger.info('Deleted setting: ' + setting)
