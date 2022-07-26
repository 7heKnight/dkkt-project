import subprocess
from urllib.parse import urlparse
from sys import argv, exit
import requests
import os
import re

# Global variable
session = requests.session()
session.headers[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
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

# [0]: List Cloud Resource Links
# [1]: List Phone
# [2]: List Emails
list_urls = []
list_phones = []
list_emails = []


def valid_link(core_url: str, crawled_link: str) -> str:
    """
    This Function used to check and valid that is a link format
    :param core_url:
    :param crawled_link:
    :return:
    """
    base_url = urlparse(core_url)
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z\d](?:[A-Z\d-]{0,61}[A-Z\d])?\.)+(?:[A-Z]{2,6}\.?|[A-Z\d-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, crawled_link) is None:
        if crawled_link[0] == '/':
            base_url = f"{base_url.scheme}://{base_url.netloc}{crawled_link}"
        else:
            base_url = f"{base_url.scheme}://{base_url.netloc}/{crawled_link}"
    return base_url


def valid_cloud_resource():
    cloud_key = {}
    if not os.path.isfile('wordlist/service.txt'):
        print('[-] File "wordlist/service.txt" not found!')
        exit(1)
    read_cloud_svc = open('wordlist/service.txt', 'r').read()
    print(read_cloud_svc)
    cloud_svc_chk = re.findall(r'(.+?)\|', read_cloud_svc)
    cloud_svcname_chk = re.findall(r'.+?\|(.+?)\n', read_cloud_svc)
    for i in range(len(cloud_svc_chk)):
        cloud_key.update({cloud_svc_chk[i]: cloud_svcname_chk[i]})
    print(cloud_key)


def get_all_link(link: str):
    """
    Used to get all links in current web page
    :param link:
    :return: list_full_links, list_cloud_resource, list_web_resource
    """
    response = session.get(link).text
    src_link = re.findall(r'src="(.+?)"', response)
    href_link = re.findall(r'href="(.+?)"', response)
    href_link.append('https://github.com/dkktdev')
    list_crawled_link = src_link + href_link

    print('\n[*] Web Resources:')
    for src in list_crawled_link:
        if 'blob.core.windows.net' in src \
                or 'file.core.windows.net' in src:
            print(f'   [-] Web resource: {src}')
            list_urls.append(src)
        else:
            src = valid_link(link, src)
            print(f'   [-] Web resource: {src}')
            list_urls.append(src)
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
        except:
            pass

def option_panel():
    """
    Print option table for user to select option, after executed
    :return:
    """
    option_table = '''
Option 1: Reconnaissance the targeted website
Option 2: DNS Scanning
Option 3: Extract data (PDF/HTML/XML)
Option 4: Exit
'''
    from time import sleep
    from os import system

    try:
        print(option_table)
        try:
            option = int(input('>> Enter your option: '))
        except ValueError:
            option = int(input('>> Enter your option: '))
        if option == 1:
            url = input('[*] Enter Url: ')
            get_all_link(url)
            get_contact(list_urls)
            return option_panel()
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

            open('1.txt', 'w')
            os.system(f'python tools/cloud_enum.py -k {input_keyword} -b {input_brute} -m {input_mutation} -l 1.txt -t 10')

            return option_panel()
        elif option == 3:
            if not list_urls[0]:
                print('[-] There is no data to print output')
                sleep(3)
                system('cls')
            else:  # Print data here, input function here
                pass
            return option_panel()
        elif option == 4:
            print('-----------------------------\n[-] Exit the program!')
            exit(0x0)
        else:
            print('[-] Wrong option!')
            sleep(3)
            system('cls')
            return option_panel()
    except KeyboardInterrupt:
        print('\n-----------------------------\n[!] Keyboard Interruption.')
        exit(0x1)


if __name__ == '__main__':
    if '-q' not in argv:
        print(banner)
    option_panel()
