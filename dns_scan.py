from urllib.parse import urlparse
from sys import argv
import requests
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
# !! This tool isn't applied OPSEC, careful to use !!.

----------------------------------------------------------
'''

# [0]: List Cloud Resource Links
# [1]: List Web Resource Links
# [2]: List Phone
# [3]: List Emails
obj_data = [[], [], [], []]


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
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
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


def get_all_link(link: str) -> (list, list, list):
    """
    Used to get all links in current web page
    :param link:
    :return: list_full_links, list_cloud_resource, list_web_resource
    """
    response = session.get(link).text
    src_link = re.findall(r'src="(.+?)"', response)
    href_link = re.findall(r'href="(.+?)"', response)
    list_crawled_link = src_link + href_link
    ret_list_links = []
    cloud_list_links = []
    web_list_links = []

    for src in list_crawled_link:
        if 'blob.core.windows.net' in src \
                or 'file.core.windows.net' in src:
            cloud_list_links.append(src)
        else:
            src = valid_link(link, src)
            web_list_links.append(src)
        ret_list_links.append(src)

    print('\n[*] Cloud Resources Scan:')
    if cloud_list_links:
        for link in cloud_list_links:
            print(f'   [+] Cloud Resource: {link}')
    else:
        print('   [-] Cloud resource not found!')
    print('\n[*] Web Resources Scan:')
    if web_list_links:
        for link in web_list_links:
            print(f'   [+] Web Resource: {link}')
    else:
        print('   [-] Web resource not found!')
    return ret_list_links, cloud_list_links, web_list_links


def get_contact(list_links: list) -> (list, list):
    """
    Used to find and get emails, phone number (###-###-####)
    :param list_links:
    :return: List_Phone_number, List_email
    """
    list_phone_number, list_email = [], []
    for link in list_links:
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

            list_email = re.findall(r'[\w_-]+@[\w._-]+\.\w+', html)
            if list_email:
                print(f'   [!] Emails Found:')
                for email in list_email:
                    print(f'      [+] Email: {email}')
            if not list_phone_number and not list_email:
                print('  [-] Not found any email or phone on this file')
    return list_phone_number, list_email


def option_panel():
    """
    Print option table for user to select option, after executed
    :return:
    """
    option = 0
    option_table = '''Option 1: Reconnaissance the targeted website
Option 2: DNS Scanning
Option 3: Exploit Cloud
Option 4: Extract data (PDF/HTML/XML)
Option 5: Exit
'''
    from time import sleep
    from os import system
    from sys import exit

    try:
        print(option_table)
        try:
            option = int(input('>> Enter your option: '))
        except ValueError:
            option = int(input('>> Enter your option: '))
        if option == 1:
            url = input('[*] Enter Url: ')
            list_url, obj_data[0], obj_data[1] = get_all_link(url)
            obj_data[2], obj_data[3] = get_contact(list_url)
            return option_panel()
        elif option == 2:
            return option_panel()
        elif option == 3:
            return option_panel()
        elif option == 4:
            if not obj_data[0]:
                print('[-] There is no data to print output')
                sleep(3)
                system('cls')
            else:  # Print data here, input function here
                pass
            return option_panel()
        elif option == 5:
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
