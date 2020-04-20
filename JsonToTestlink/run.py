import os
import sys
import config
import logging
import argparse
import testlink
from testlink.testlinkerrors import TLResponseError
import json_parse


def main():

    # create logging file handler
    logger = logging.getLogger("json_to_testlink")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("json_to_testlink.log")
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    logger.info("Test reporter started!")

    settings_path = 'json_to_testlink_settings.ini'

    # creating settings.ini if not exists, reading all settings
    if os.path.exists(settings_path):
        testlink_server_ip = config.get_setting(settings_path, 'Settings', 'testlink_server_ip')
        testlink_server_port = config.get_setting(settings_path, 'Settings', 'testlink_server_port')
        testlink_api_url = config.get_setting(settings_path, 'Settings', 'testlink_api_url')
        dev_key = config.get_setting(settings_path, 'Settings', 'dev_key')
        testlink_user = config.get_setting(settings_path, 'Settings', 'testlink_user')
        testlink_password = config.get_setting(settings_path, 'Settings', 'testlink_password')
        testlink_project_name = config.get_setting(settings_path, 'Settings', 'testlink_project_name')
        testlink_test_project_prefix = config.get_setting(settings_path, 'Settings', 'testlink_test_project_prefix')
        testlink_testsuite_id = config.get_setting(settings_path, 'Settings', 'testlink_testsuite_id')
        testlink_testplan_id = config.get_setting(settings_path, 'Settings', 'testlink_testplan_id')
        testlink_build_id = config.get_setting(settings_path, 'Settings', 'testlink_build_id')
        testlink_info = config.get_setting(settings_path, 'Settings', 'testlink_info')
        logger.info(testlink_info)
    else:
        config.create_config(settings_path)
        testlink_server_ip = config.get_setting(settings_path, 'Settings', 'testlink_server_ip')
        testlink_server_port = config.get_setting(settings_path, 'Settings', 'testlink_server_port')
        testlink_api_url = config.get_setting(settings_path, 'Settings', 'testlink_api_url')
        dev_key = config.get_setting(settings_path, 'Settings', 'dev_key')
        testlink_user = config.get_setting(settings_path, 'Settings', 'testlink_user')
        testlink_password = config.get_setting(settings_path, 'Settings', 'testlink_password')
        testlink_project_name = config.get_setting(settings_path, 'Settings', 'testlink_project_name')
        testlink_test_project_prefix = config.get_setting(settings_path, 'Settings', 'testlink_test_project_prefix')
        testlink_testsuite_id = config.get_setting(settings_path, 'Settings', 'testlink_testsuite_id')
        testlink_testplan_id = config.get_setting(settings_path, 'Settings', 'testlink_testplan_id')
        testlink_build_id = config.get_setting(settings_path, 'Settings', 'testlink_build_id')
        testlink_info = config.get_setting(settings_path, 'Settings', 'testlink_info')
        logger.info(testlink_info)

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

    testlink_connection_url = "http://{}{}{}".format(testlink_server_ip, testlink_server_port, testlink_api_url)
    logger.debug("Testlink_connection_string = " + testlink_connection_url)

    tls = testlink.TestlinkAPIClient(testlink_connection_url, dev_key)
    logger.debug("Check api connection: ")
    logger.debug(print(tls.about()))

    logger.info("Start json parsing")
    json_test_data = json_parse.json_read(json_report_path)

    # internal variables
    awn_test_suite = json_test_data['testResults']
    step_info = []
    report_step_info = []
    test_case_names = []
    execution_type = 2  # for manual set 1, for automated set 2
    test_case_version = 1
    # test_case_status = 'b'
    this_file_dirname = os.path.dirname(__file__)
    logger.debug(this_file_dirname)
    log_path = os.path.join(this_file_dirname, 'report_log.csv')
    logger.debug(log_path)

    testlink_testproject_id = tls.getProjectIDByName(testlink_project_name)
    logger.debug("Test_project_id: " + str(testlink_testproject_id))
    logger.debug("Get_Project_TCases")
    response = tls.getTestCasesForTestSuite(testsuiteid=testlink_testsuite_id)
    for tc in range(len(response)):
        test_case_names.append(response[tc]['name'])
    logger.debug("Project TCases: " + str(test_case_names))

    for test in range(len(awn_test_suite)):
        test_case = json_test_data['testResults'][test]['stepResults']
        logger.debug(json_parse.read_test_case_name(json_test_data, test))
        for step in range(len(test_case)):
            # print("Test step: ")
            logger.debug(json_parse.read_test_case_step_actions(json_test_data, test, step))
            step_info.append({'step_number': step + 1,
                              'actions': json_parse.read_test_case_step_actions(json_test_data, test, step),
                              'expected_results': json_parse.read_test_case_step_expected_results(json_test_data, test,
                                                                                                  step),
                              'execution_type': execution_type})
            report_step_info.append({'step_number': step + 1,
                                     'result': json_parse.read_test_case_step_status(json_test_data, test, step),
                                     'notes': json_parse.read_test_case_step_execution_notes(json_test_data, test, step)})

            logger.debug(step_info)
            logger.debug(report_step_info)

        if json_parse.read_test_case_name(json_test_data, test) in test_case_names:
            test_case_id = tls.getTestCaseIDByName(json_parse.read_test_case_name(json_test_data, test))[0][
                'id']
            new_result = tls.reportTCResult(testcaseid=test_case_id,
                                            testplanid=testlink_testplan_id,
                                            buildid=testlink_build_id,
                                            status=json_parse.read_test_case_status(json_test_data, test),
                                            execduration=json_parse.read_test_case_exec(json_test_data, test),
                                            timestamp=json_parse.read_test_case_start_time(json_test_data, test),
                                            steps=report_step_info)
            logger.info("Test case report created: " + str(response))

            log_info = json_parse.read_test_case_logs(json_test_data, test)
            logger.debug(log_info)
            json_parse.csv_write(log_info, log_path)

            new_result_id = new_result[0]['id']
            try:
                new_attachment = tls.uploadExecutionAttachment(log_path,
                                                               new_result_id,
                                                               "logfile",
                                                               'Test case logfile for a AWN Execution run')
                logger.info("Test case attachment upload done :" + str(new_attachment))
            except TLResponseError:
                pass

            report_step_info.clear()
        else:
            response = tls.createTestCase(testcasename=json_parse.read_test_case_name(json_test_data, test),
                                          testsuiteid=testlink_testsuite_id,
                                          testprojectid=testlink_testproject_id,
                                          authorlogin=testlink_user,
                                          summary='',
                                          steps=step_info)
            test_case_id = response[0]['id']
            tc_aa_full_ext_id = tls.getTestCase(test_case_id)[0]['full_tc_external_id']
            logger.info("Test case created: " + str(response))
            logger.debug("Test case id: " + str(test_case_id))
            logger.debug("Test case_ext_id: " + str(tc_aa_full_ext_id))

            response = tls.addTestCaseToTestPlan(testlink_testproject_id,
                                                 testlink_testplan_id,
                                                 tc_aa_full_ext_id,
                                                 test_case_version)
            logger.info("Test case added to TP: " + str(response))

            new_result = tls.reportTCResult(testcaseid=test_case_id,
                                            testplanid=testlink_testplan_id,
                                            buildid=testlink_build_id,
                                            status=json_parse.read_test_case_status(json_test_data, test),
                                            execduration=json_parse.read_test_case_exec(json_test_data, test),
                                            timestamp=json_parse.read_test_case_start_time(json_test_data, test),
                                            steps=report_step_info)
            logger.info("Test case report created: " + str(response))

            log_info = json_parse.read_test_case_logs(json_test_data, test)
            logger.debug(log_info)
            json_parse.csv_write(log_info, log_path)

            new_result_id = new_result[0]['id']
            try:
                new_attachment = tls.uploadExecutionAttachment(log_path,
                                                               new_result_id,
                                                               "logfile",
                                                               'Test case logfile for a AWN Execution run')
                logger.info("Test case attachment upload done :" + str(new_attachment))
            except TLResponseError:
                pass

            report_step_info.clear()
        step_info.clear()

    logger.info("Report logs upload done")

    logger.info("Test reporting completed!")


if __name__ == "__main__":
    main()
