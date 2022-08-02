
#!/usr/bin/env python
from __future__ import print_function
from getpass import getpass
import argparse
from modules import logger
import os
import rm
import subprocess


def main():
    """ main function """
    parser = argparse.ArgumentParser(description='this is to get IP address for lynis audit only')
    parser.add_argument('-env', '--environment', required=True, help='The cloud on which the test-suite is to be run',
                        choices=['azure'])
    parser.add_argument('-az_u', '--azure_user', required=False, help='username of azure account, optionally used if you want to run the azure audit with no user interaction.')
    parser.add_argument('-az_p', '--azure_pass', required=False, help='username of azure password, optionally used if you want to run the azure audit with no user interaction.')
    parser.add_argument('-o', '--output', required=False, default="cs-audit.log", help='writes a log in JSON of an audit, ideal for consumptions into SIEMS like ELK and Splunk. Defaults to cs-audit.log')
    parser.add_argument("-w", "--wipe", required=False, default=False, action='store_true',
                        help="rm -rf reports/ folder before executing an audit")
    parser.add_argument('-n', '--number', required=False, help='Retain number of report to store for a particular environment and user/project.')

    args = parser.parse_args()

    
    # set up logging
    log = logger.setup_logging(args.output, "INFO")

    log.info("starting cloud security suite v1.0")

    if args.number and args.wipe == True:
        print("Warning you can't use -w or -n flag at same time")
        exit(1)
    elif args.number:
        try:  
           int(args.number)
        except Exception as _:
            print("Please provide a number for -n option only. ")
            print("EXITTING!!")
            exit(1)

    if args.wipe:
        log.info("wiping reports/ folder before running")
        rm.rm("reports/")

    if args.environment == 'azure':
        if args.azure_user and args.azure_pass:
            print("using azure credentials passed via cli")
            subprocess.call(['az', 'login', '-u', args.azure_user, '-p', args.azure_pass])
        else:
            print("azure authentication required")
            subprocess.call(['az', 'login'])
        log.info("running azure audit")
        from modules import azureaudit
        azureaudit.azure_audit()
        log.info("completed azure audit")

if __name__ == '__main__':
    main()
 
