from datetime import datetime, timedelta
import logging
import json
import csv
import sys

module_logger = logging.getLogger("json_to_rp.json_parse")


def json_read(read_path):
    """
    Parses json and returns base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.json_read")
    try:
        with open(read_path, "r") as in_file:
            data = in_file.read()
            # parse file
            obj = json.loads(data)
            # show values
            logger.info("Suite name: " + str(obj['info']))
            return obj
    except OSError as e:
        print(e)
        sys.exit("Error reading report file, check file path")


def format_list(json_obj):
    """
    Used to format list log objects
    """
    my_list = []
    logger = logging.getLogger("json_to_rp.json_parse.format_list")
    my_str = str(json_obj)
    result = my_str.replace('{', '').replace('}', '').replace('[', '').replace(']','').split(',')
    for i in result:
        my_list.append("{}\r\n".format(i))
    return my_list


def format_dict(json_obj):
    """
    Used to format dict log objects
    """
    logger = logging.getLogger("json_to_rp.json_parse.format_string")
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
    logger = logging.getLogger("json_to_rp.json_parse.read_suite_name")
    logger.debug("testSuiteName: " + str(obj['info']['name']))
    return obj['info']['name']


def read_suite_start_time(obj):
    """
    Returns suite start time from base dict object, converts to used timestamp
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_suite_start_time")
    logger.debug("Suite time to timestamp: " + str(obj['startTime']))
    test_start = obj['startTime']
    mlsec = repr(test_start).split('.')[1][:3]
    timestamp = datetime.strptime(test_start, '%d-%m-%Y %H:%M:%S.%f').strftime('%Y-%m-%dT%H:%M:%S.{}Z'.format(mlsec))
    logger.debug("Suite Start Time: " + timestamp)
    return timestamp


def read_suite_end_time(obj):
    """
    Returns suite end time from base dict object, calculates and formats
    to used timestamp
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_suite_end_time")
    test_start = obj['startTime']
    logger.debug("TestSuite StartTime to timestamp: " + str(test_start))
    execution_time = obj['executionTime']
    logger.debug("TestSuite ExecutionTime to timestamp: " + str(execution_time))
    test_end = datetime.strptime(test_start, '%d-%m-%Y %H:%M:%S.%f') + timedelta(milliseconds=execution_time)
    timestamp = test_end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    logger.debug("TestSuite EndTime to timestamp: " + timestamp)
    return timestamp


def read_suite_description(obj):
    """
    Returns suite description from base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_suite_description")
    logger.debug("testSuiteDescription: " + str(obj['suiteVariables'][1]['value']))
    return str(obj['suiteVariables'][0]['value'])


def read_suite_status(obj):
    """
    Returns modified suite status from base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_suite_status")
    suite_status_map = {'True': 'PASSED',
                        'False': 'FAILED'}
    suite_status = str(obj['status'])
    logger.debug("testSuiteStatus: " + str(obj['status']))
    suite_status_mod = suite_status_map.get(suite_status)
    logger.debug("testSuiteStatusMod: " + suite_status_mod)
    return suite_status_mod


def read_test_case_name(obj, test):
    """
    Returns test case name from base dict object
    """
    logger = logging.getLogger("json_to_rp.read_test_case_name")
    logger.debug("testCaseName: " + str(obj['testResults'][test]['info']['name']))
    return obj['testResults'][test]['info']['name']


def read_test_case_logs(obj, test):
    """
    Returns test case logs from base dict object
    """
    logger = logging.getLogger("json_to_rp.read_test_case_logs")
    logger.debug("testCaseLogs: " + str(obj['testResults'][test]['logs']))
    return obj['testResults'][test]['logs']


def read_test_case_variables(obj, test):
    """
    Returns test case variables from base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_case_variables")
    logger.debug("testCaseVariables: " + str(obj['testResults'][test]['testVariables']))
    return obj['testResults'][test]['testVariables']


def read_test_case_exec(obj, test):
    """
    Returns formated test case execution time from base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_case_exec")
    ms = obj['testResults'][test]['executionTime']
    time = float('{}.{}'.format(*divmod(ms, 60000)))
    logger.debug("testTime(s): " + str(ms))
    logger.debug("testTime(m): " + str(time))
    return time


def read_test_case_status(obj, test):
    """
    Returns modified test case status from base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_case_status")
    case_status_map = {'True': 'PASSED',
                       'False': 'FAILED'}
    case_status = str(obj['testResults'][test]['status'])
    logger.debug("testCaseStatus: " + str(obj['testResults'][test]['status']))
    case_status_mod = case_status_map.get(case_status)
    logger.debug("testCaseStatusMod: " + case_status_mod)
    return case_status_mod


def read_test_case_start_time(obj, test):
    """
    Returns test case start time from base dict object, converts to used timestamp
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_case_start_time")
    test_start = obj['testResults'][test]['startTime']
    logger.debug("TestCase Start time to timestamp: " + str(test_start))
    timestamp = datetime.strptime(test_start, '%d-%m-%Y %H:%M:%S.%f').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    logger.debug("TestCase Start Time: " + timestamp)
    return timestamp


def read_test_case_end_time(obj, test):
    """
    Returns test case end time from base dict object, converts to used timestamp
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_case_end_time")
    test_start = obj['testResults'][test]['startTime']
    logger.debug("TestCase StartTime to timestamp: " + str(test_start))
    execution_time = obj['testResults'][test]['executionTime']
    logger.debug("TestCase ExecutionTime to timestamp: " + str(execution_time))
    test_end = datetime.strptime(test_start, '%d-%m-%Y %H:%M:%S.%f') + timedelta(milliseconds=execution_time)
    timestamp = test_end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    logger.debug("TestCase EndTime to timestamp: " + timestamp)
    return timestamp


def read_test_step_name(obj, test, step):
    """
    Returns test step name from base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_step_name")
    logger.debug("testStepName: " + str(obj['testResults'][test]['stepResults'][step]['info']['name']))
    return obj['testResults'][test]['stepResults'][step]['info']['name']


def read_test_step_description(obj, test, step):
    """
    Returns test step description from base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_step_description")
    logger.debug("testStepDescription: " + str(obj['testResults'][test]['stepResults'][step]['info']['description']))
    return obj['testResults'][test]['stepResults'][step]['info']['description']


def read_test_step_start_time(obj, test, step):
    """
    Returns test step start time from base dict object, converts to used timestamp
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_step_start_time")
    test_start = obj['testResults'][test]['stepResults'][step]['startTime']
    logger.debug("TestStep time to timestamp: " + str(test_start))
    timestamp = datetime.strptime(test_start, '%d-%m-%Y %H:%M:%S.%f').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    logger.debug("TestStep Start Time: " + timestamp)
    return timestamp


def read_test_step_end_time(obj, test, step):
    """
    Returns test step end time from base dict object, converts to used timestamp
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_step_end_time")
    test_start = obj['testResults'][test]['stepResults'][step]['startTime']
    logger.debug("TestStep StartTime to timestamp: " + str(test_start))
    execution_time = obj['testResults'][test]['stepResults'][step]['executionTime']
    logger.debug("TestStep ExecutionTime to timestamp: " + str(execution_time))
    test_end = datetime.strptime(test_start, '%d-%m-%Y %H:%M:%S.%f') + timedelta(milliseconds=execution_time)
    timestamp = test_end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    logger.debug("TestStep EndTime to timestamp: " + timestamp)
    return timestamp


def read_test_step_parameters(obj, test, step):
    """
    Returns test step parameters from base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_execution_notes")
    logger.debug("testCaseStepExecutionNotes: " + str(obj['testResults'][test]['stepResults'][step]['parameters']))
    return obj['testResults'][test]['stepResults'][step]['parameters']


def read_test_step_logs(obj, test, step):
    """
    Returns test step logs from base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_step_logs")
    logger.debug("testCaseStepLogs: " + str(obj['testResults'][test]['stepResults'][step]['logs']))
    return obj['testResults'][test]['stepResults'][step]['logs']


def read_test_step_status(obj, test, step):
    """
    Returns test step status from base dict object
    """
    logger = logging.getLogger("json_to_rp.json_parse.read_test_step_status")
    logger.debug("testCaseStepStatus: " + str(obj['testResults'][test]['stepResults'][step]['status']))
    return obj['testResults'][t]['stepResults'][s]['status']


def log_write(data, log_path):
    """
    Writes to log file
    """
    logger = logging.getLogger("json_to_rp.json_parse.log_write")
    try:
        with open(log_path, "a") as out_file:
            log_file = out_file.writelines(data)
        logger.info('Write to log: ' + log_path)
    except OSError as e:
        print(e)


def csv_write(data, csv_path):
    """
    Writes to CSV
    """
    logger = logging.getLogger("json_to_rp.json_parse.csv_write")
    try:
        with open(write_path, "w", newline='') as out_file:
            writer = csv.writer(out_file, delimiter=' ')
            writer.writerow(data)
        logger.info('Csv log created: ' + write_path)
    except OSError as e:
        print(e)
