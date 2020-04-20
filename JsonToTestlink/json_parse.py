from datetime import datetime
import logging
import json
import csv
import sys

module_logger = logging.getLogger("json_to_testlink.json_parse")


def json_read(read_path):
    """
    Parses json, return base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.json_read")
    try:
        with open(read_path, "r") as in_file:
            data = in_file.read()
            # parse file
            obj = json.loads(data)
            # show values
            logger.info("Info: " + str(obj['info']))
            return obj
    except OSError as e:
        print(e)
        sys.exit("Error reading report file, check file path")


def format_list(json_obj):
    """
    Used to format list data from base dict object
    """
    my_list = []
    logger = logging.getLogger("json_to_testlink.json_parse.format_list")
    my_str = str(json_obj)
    result = my_str.replace('{', '').replace('}', '').replace('[', '').replace(']','').split(',')
    for i in result:
        my_list.append("{}\r\n".format(i))
    return my_list


def format_dict(json_obj):
    """
    Used to format dict data from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.format_string")
    my_list = [] = json_obj.split(',')
    result = []
    for item in json_obj:
        print(item)
        result.append("{}\r\n".format(item.key, item.value))
    "".join(my_list)
    logger.debug("formatedString: " , my_list)
    return my_list


def read_suite_name(obj):
    """
    Returns suite name from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_suite_name")
    logger.debug("testSuiteName: " + str(obj['suiteVariables'][1]['name']))
    return str(obj['suiteVariables'][0]['name'])


def read_suite_description(obj):
    """
    Returns suite description from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_suite_description")
    logger.debug("testSuiteDescription: " + str(obj['suiteVariables'][1]['value']))
    return str(obj['suiteVariables'][0]['value'])


def read_test_case_name(obj, test):
    """
    Returns test case name from base dict object
    """
    logger = logging.getLogger("json_to_testlink.read_test_case_name")
    logger.debug("testCaseName: " + str(obj['testResults'][test]['info']['name']))
    return str(obj['testResults'][test]['info']['name'])


def read_test_case_logs(obj, test):
    """
    Returns test case logs from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_test_case_logs")
    logger.debug("testCaseLogs: " + str(obj['testResults'][test]['logs']))
    return obj['testResults'][test]['logs']


def read_test_case_variables(obj, test):
    """
    Returns test case variables from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_test_case_variables")
    logger.debug("testCaseVariables: " + str(obj['testResults'][test]['testVariables']))
    return obj['testResults'][test]['testVariables']


def read_test_case_exec(obj, test):
    """
    Returns test case formated execution time from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_test_case_exec")
    ms = obj['testResults'][test]['executionTime']
    time = float('{}.{}'.format(*divmod(ms, 60000)))
    logger.debug("testTime(s): " + str(ms))
    logger.debug("testTime(m): " + str(time))
    return time


def read_test_case_status(obj, test):
    """
    Returns test case modified status from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_test_case_status")
    case_status_map = {'True': 'p',
                       'False': 'f'}
    case_status = str(obj['testResults'][test]['status'])
    logger.debug("testCaseStatus: " + str(obj['testResults'][test]['status']))
    logger.debug(case_status_map.get(case_status))
    return case_status_map.get(case_status)


def read_test_case_start_time(obj, test):
    """
    Returns test case formated start time from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_test_case_start_time")
    test_start = obj['testResults'][test]['startTime']
    logger.debug("timeToTimestamp: " + test_start)
    timestamp = datetime.strptime(test_start, '%d-%m-%Y %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
    logger.debug("startTime: " + timestamp)
    return timestamp


def read_test_case_step_actions(obj, test, step):
    """
    Returns test step actions from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_test_case_step_actions")
    logger.debug("testCaseStepActions: " + str(obj['testResults'][test]['stepResults'][step]['info']))
    return obj['testResults'][test]['stepResults'][step]['info']['name']


def read_test_case_step_expected_results(obj, test, step):
    """
    Returns test step expected result from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_test_case_step_expected_results")
    logger.debug("testCaseStepExpectedResult: " + str(obj['testResults'][test]['stepResults'][step]['checks']))
    return obj['testResults'][test]['stepResults'][step]['info']['description']


def read_test_case_step_execution_notes(obj, test, step):
    """
    Returns test step execution notes from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_test_case_execution_notes")
    logger.debug("testCaseStepExecutionNotes: " + str(obj['testResults'][test]['stepResults'][step]['parameters']))
    return str(obj['testResults'][test]['stepResults'][step]['parameters'])


def read_test_case_step_logs(obj, test, step):
    """
    Returns test step logs from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_test_case_step_logs")
    logger.debug("testCaseStepLogs: " + str(obj['testResults'][test]['stepResults'][step]['logs']))
    return str(obj['testResults'][test]['stepResults'][step]['logs'])


def read_test_case_step_status(obj, test, step):
    """
    Returns test step modified status from base dict object
    """
    logger = logging.getLogger("json_to_testlink.json_parse.read_test_case_step_status")
    step_map = {'PASSED': 'p',
                'FAILED': 'f',
                'SKIPPED': 'b'}
    x = obj['testResults'][test]['stepResults'][step]['status']
    logger.debug("testCaseStepStatus: " + str(obj['testResults'][test]['stepResults'][step]['status']))
    return step_map.get(x)


def log_write(data, log_path):
    """
    Writes to log file
    """
    logger = logging.getLogger("json_to_testlink.json_parse.log_write")
    try:
        with open(log_path, "a") as out_file:
            log_file = out_file.writelines(data)
        logger.info('Write to log: ' + log_path)
    except OSError as e:
        print(e)


def csv_write(data, csv_path):
    """
    Writes to csv
    """
    logger = logging.getLogger("json_to_testlink.json_parse.csv_write")
    try:
        with open(write_path, "w", newline='') as out_file:
            writer = csv.writer(out_file, delimiter=' ')
            writer.writerow(data)
        logger.info('Csv log created: ' + write_path)
    except OSError as e:
        print(e)
