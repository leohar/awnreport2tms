## AWN report to Testlink
_Simple module for publishing awn test results to Testlink TMS, 
based on report .json.
Parses json file exported from AWN, checks if these Test cases are 
present in Testlink, creates if not, generates report for each TC step
and attaches TC logs._
_______________________________________________________________________________
Installation requirements: Python 3.8

Install [requests](https://2.python-requests.org/en/master/) library:

        pip install requests

Install [testlink](https://pypi.org/project/TestLink-API-Python-client/) library:

        pip install TestLink-API-Python-client
_______________________________________________________________________________
script accepts one string parameter - report path, type is described in 
command line help:

        python run.py -h

Example of command line for running script:

        python run.py report.json

Other parameters should be set in settings.ini, default .ini would be created
during the first run.

Mandatory parameters:
 * testlink_server_ip = [YOUR TL SERVER IP]
 * testlink_api_url = [TL Version <  1.9.7: Use [/testlink/lib/api/xmlrpc.php] 
                     TL Version >= 1.9.7: Use [/testlink/lib/api/xmlrpc/v1/xmlrpc.php]
 * dev_key = [from TL user settings]
 * testlink_user = [YOUR TL USER NAME]
 * testlink_project_name = [YOUR TL PROJECT NAME]
 * testlink_testsuite_id = [YOUR TL SUITE ID]
 * testlink_testplan_id = [YOUR TL TEST PLAN ID]
 * testlink_build_id = [YOUR TL BUILD ID]
 
