## AWN report to ReportPortal
_Simple module for publishing awn test results to ReportPortal TMS, 
based on report .json.
Parses json file exported from AWN, generates report for each TC step._
_______________________________________________________________________________
Installation requirements: Python 3.8 

Install [requests](https://2.python-requests.org/en/master/) library:

        pip install requests

_______________________________________________________________________________

script accepts one string parameter - report path, type is described in 
command line help:

        python run.py -h

Example of command line for running script:

        python run.py report.json

Other parameters should be set in settings.ini, default .ini would be created
during the first run.

Mandatory parameters:
 * rp_api_url = [YOUR RP SERVER IP]
 * rp_project_name = [YOUR RP PROJECT NAME]
 * rp_uuid = [from RP user settings]
 * rp_launch = [YOUR RP LAUNCH NAME]
 
