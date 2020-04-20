import os
import sys
import json
import config
import logging
import requests
import argparse
import json_parse
from pprint import pprint


def main():

    # create logging file handler
    logger = logging.getLogger("json_to_rp")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("json_to_rp.log")
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    logger.info("Test reporter started!")

    settings_path = 'json_to_rp_settings.ini'

    # creating settings.ini if not exists, reading all settings
    if os.path.exists(settings_path):
        rp_api_url = config.get_setting(settings_path, 'Settings', 'rp_api_url')
        rp_project_name = config.get_setting(settings_path, 'Settings', 'rp_project_name')
        rp_uuid = config.get_setting(settings_path, 'Settings', 'rp_uuid')
        rp_launch = config.get_setting(settings_path, 'Settings', 'rp_launch')
        rp_info = config.get_setting(settings_path, 'Settings', 'rp_info')
        logger.info(rp_info)
    else:
        config.create_config(settings_path)
        rp_api_url = config.get_setting(settings_path, 'Settings', 'rp_api_url')
        rp_project_name = config.get_setting(settings_path, 'Settings', 'rp_project_name')
        rp_uuid = config.get_setting(settings_path, 'Settings', 'rp_uuid')
        rp_launch = config.get_setting(settings_path, 'Settings', 'rp_launch')
        rp_info = config.get_setting(settings_path, 'Settings', 'rp_info')
        logger.info(rp_info)

    # command line arguments parser settings
    parser = argparse.ArgumentParser(description='Report builder requires relative json report path for '
                                                 'report generation.')
    parser.add_argument(
                        "json_report_path",
                        metavar='1',
                        type=str,
                        help='json report file name or file path')
    args = parser.parse_args()
    logger.debug(str(parser.parse_args()))
    json_report_path = parser.parse_args().json_report_path

    rp_headers = {"accept": "*/*",
                  "content-type": "application/json",
                  "Authorization": "bearer {}".format(rp_uuid)}
    logger.debug("RP_headers" + str(rp_headers))

    logger.info("Check api connection: ")
    rp_endpoint = "{}/v1/{}/launch".format(rp_api_url, rp_project_name)
    logger.debug("RP_connection_string = " + rp_endpoint)
    check = requests.get(rp_endpoint,
                         headers=rp_headers)
    check.raise_for_status()
    logger.info("Connection: OK")
    logger.debug(check.status_code)

    logger.info("Start json parsing")
    json_test_data = json_parse.json_read(json_report_path)

    # internal variables
    awn_test_suite = json_test_data['testResults']

    logger.info("Start launch")
    rp_endpoint = "{}/v1/{}/launch".format(rp_api_url, rp_project_name)
    logger.debug("RP_connection_string = " + rp_endpoint)
    rp_data = {"description": rp_project_name,
               "mode": "DEFAULT",
               "name": rp_launch,
               "startTime": json_parse.read_suite_start_time(json_test_data)
               }
    logger.debug("Request: ")
    pprint(rp_data)
    launch = requests.post(rp_endpoint,
                           headers=rp_headers,
                           data=json.dumps(rp_data))
    launch.raise_for_status()
    launch_id = launch.json()['id']
    logger.debug("Response Launch_id: " + str(launch.text))

    logger.info("Start suite")
    rp_endpoint = "{}/v1/{}/item".format(rp_api_url, rp_project_name)
    logger.debug("RP_connection_string = " + rp_endpoint)
    rp_data = {"description": "awn",
               "launchUuid": launch_id,
               "name": json_parse.read_suite_name(json_test_data),
               "startTime": json_parse.read_suite_start_time(json_test_data),
               "type": "suite"
               }
    logger.debug("Request: ")
    pprint(rp_data)
    test_suite = requests.post(rp_endpoint,
                               headers=rp_headers,
                               data=json.dumps(rp_data))
    test_suite.raise_for_status()
    suite_id = test_suite.json()['id']
    logger.debug("Response Suite_id: " + str(test_suite.text))
  
    for test in range(len(awn_test_suite)):
        awn_step_results = json_test_data['testResults'][test]['stepResults']
        logger.debug(json_parse.read_test_case_name(json_test_data, test))

        logger.info("Start_test")
        rp_endpoint = "{}/v1/{}/item/{}".format(rp_api_url, rp_project_name, suite_id)
        logger.debug("RP_connection_string = " + rp_endpoint)
        rp_data = {"name": json_parse.read_test_case_name(json_test_data, test),
                   "startTime": json_parse.read_test_case_start_time(json_test_data, test),
                   "launchUuid": launch_id,
                   "type": "test"
                   }
        logger.debug("Request: ")
        pprint(rp_data)
        test_case = requests.post(rp_endpoint,
                                  headers=rp_headers,
                                  data=json.dumps(rp_data))
        test_case.raise_for_status()
        test_case_id = test_case.json()['id']
        logger.debug("Response Test_id: " + str(test_case.text))

        for step in range(len(awn_step_results)):
            logger.info("Start_test_step")
            rp_endpoint = "{}/v1/{}/item/{}".format(rp_api_url, rp_project_name, test_case_id)
            logger.debug("RP_connection_string = " + rp_endpoint)
            rp_data = {"name": json_parse.read_test_step_name(json_test_data, test, step),
                       "description": json_parse.read_test_step_description(json_test_data, test, step),
                       "startTime": json_parse.read_test_step_start_time(json_test_data, test, step),
                       "launchUuid": launch_id,
                       "type": "step"
                       }
            logger.debug("Request: ")
            pprint(rp_data)
            test_step = requests.post(rp_endpoint,
                                      headers=rp_headers,
                                      data=json.dumps(rp_data))
            test_step.raise_for_status()
            test_step_id = test_step.json()['id']
            logger.debug("Test_step_started: " + str(test_step_id))

            logger.info("Finish_test_step")
            rp_endpoint = "{}/v1/{}/item/{}".format(rp_api_url, rp_project_name, test_step_id)
            logger.debug("RP_connection_string = " + rp_endpoint)
            rp_data = {"endTime": json_parse.read_test_step_end_time(json_test_data, test, step),
                       "status": json_parse.read_test_step_status(json_test_data, test, step),
                       "launchUuid": launch_id,
                       }
            logger.debug("Request: ")
            pprint(rp_data)
            finish_step = requests.put(rp_endpoint,
                                       headers=rp_headers,
                                       data=json.dumps(rp_data))
            finish_step.raise_for_status()
            finish_step_message = finish_step.json()['message']
            logger.debug("Test_step_finished: " + str(finish_step_message))

        logger.info("Finish_test")
        rp_endpoint = "{}/v1/{}/item/{}".format(rp_api_url, rp_project_name, test_case_id)
        logger.debug("RP_connection_string = " + rp_endpoint)
        rp_data = {"endTime": json_parse.read_test_case_end_time(json_test_data, 0),
                   "status": json_parse.read_test_case_status(json_test_data, 0),
                   "launchUuid": launch_id,
                   }
        logger.debug("Request: ")
        pprint(rp_data)
        finish_case = requests.put(rp_endpoint,
                                   headers=rp_headers,
                                   data=json.dumps(rp_data))
        finish_case.raise_for_status()
        finish_case_message = finish_case.json()['message']
        logger.debug("Test_finished: " + str(finish_case_message))

    logger.info("Report logs upload done")

    logger.info("Finish_suite")
    rp_endpoint = "{}/v1/{}/item/{}".format(rp_api_url, rp_project_name, suite_id)
    logger.debug("RP_connection_string = " + rp_endpoint)
    rp_data = {"endTime": json_parse.read_suite_end_time(json_test_data),
               "status": json_parse.read_suite_status(json_test_data),
               "launchUuid": launch_id,
               }
    logger.debug("Request: ")
    pprint(rp_data)
    finish_suite = requests.put(rp_endpoint,
                                headers=rp_headers,
                                data=json.dumps(rp_data))
    finish_suite.raise_for_status()
    finish_suite_message = finish_suite.json()['message']
    logger.debug("Suite_finished: " + str(finish_suite_message))

    logger.info("Finish_launch")
    rp_endpoint = "{}/v1/{}/launch/{}/finish".format(rp_api_url, rp_project_name, launch_id)
    logger.debug("RP_connection_string = " + rp_endpoint)
    rp_data = {"endTime": json_parse.read_suite_end_time(json_test_data),
               }
    logger.debug("Request: ")
    pprint(rp_data)
    finish_launch = requests.put(rp_endpoint,
                                 headers=rp_headers,
                                 data=json.dumps(rp_data))
    finish_launch.raise_for_status()
    finish_launch_message = finish_launch.json()['id']
    logger.debug("Launch_finished: " + str(finish_launch_message))

    logger.info("Test reporting completed!")


if __name__ == "__main__":
    main()
