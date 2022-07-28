import datetime
import os
import re


def get_name() -> str:
    now = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
    return f'dkkt-report_{now}'


def get_html_report(lu, lp, le, oo):
    if not os.path.isfile('form/form.html'):
        print('[!] Missing html form to export.')
        return ''
    final_output = open('form/form.html', encoding='utf8').read()

    # Replace Urls
    output_urls = '- ' + '<br>- '.join(u for u in lu)
    # print(output_urls)

    # Replace Phones
    output_phones = '- ' + '<br>- '.join(u for u in lp)
    # print(output_phones)

    # Replace Emails
    output_emails = '- ' + '<br>- '.join(u for u in le)
    # print(output_emails)

    # Replace Others
    output_others = oo.replace('\n\n', '- ')
    output_others = re.sub(r'#+.+?#+\n', '', output_others, re.S)
    output_others = re.sub(r'\n', '<br>- ', output_others, re.S)
    output_others = output_others.replace('- -', '-')
    output_others = output_others.replace('- <br>', '')
    output_others = re.sub(r'<br>- $', '', output_others)

    # Replace
    final_output = final_output.replace('ReplaceTimeHere', datetime.datetime.now().strftime("%d/%m/%Y (%H:%M:%S)"))
    if output_urls == '- ':
        output_urls += 'None'
    final_output = final_output.replace('ReplaceLinksHere', output_urls)
    if output_phones == '- ':
        output_phones += 'None'
    final_output = final_output.replace('ReplacePhonesHere', output_phones)
    if output_emails == '- ':
        output_emails += 'None'
    final_output = final_output.replace('ReplaceEmailsHere', output_emails)
    if output_others == '- ' or output_others == '':
        output_others += '- None'
    final_output = final_output.replace('ReplaceOthersHere', output_others)
    return final_output


def get_txt_report(lu, lp, le, oo):
    if not os.path.isfile('form/form.txt'):
        print('[!] Missing html form to export.')
        return ''
    final_output = open('form/form.txt', encoding='utf8').read()

    # Replace Urls
    output_urls = '- ' + '\n- '.join(u for u in lu)
    # print(output_urls)

    # Replace Phones
    output_phones = '- ' + '\n- '.join(u for u in lp)
    # print(output_phones)

    # Replace Emails
    output_emails = '- ' + '\n- '.join(u for u in le)
    # print(output_emails)

    # Replace Others
    output_others = oo.replace('\n\n', '- ')
    output_others = re.sub(r'#+.+?#+\n', '', output_others, re.S)
    output_others = re.sub(r'\n', '\n- ', output_others, re.S)
    output_others = output_others.replace('- -', '-')
    output_others = output_others.replace('- \n', '')
    output_others = re.sub(r'\n- $', '', output_others)

    # Replace
    final_output = final_output.replace('ReplaceTimeHere', datetime.datetime.now().strftime("%d/%m/%Y (%H:%M:%S)"))
    if output_urls == '- ':
        output_urls += 'None'
    final_output = final_output.replace('ReplaceLinksHere', output_urls)
    if output_phones == '- ':
        output_phones += 'None'
    final_output = final_output.replace('ReplacePhonesHere', output_phones)
    if output_emails == '- ':
        output_emails += 'None'
    final_output = final_output.replace('ReplaceEmailsHere', output_emails)
    if output_others == '- ' or output_others == '':
        output_others += '- None'
    final_output = final_output.replace('ReplaceOthersHere', output_others)
    return final_output


def main(lu, lp, le, oo):
    if not os.path.isdir('export'):
        os.mkdir('export')
    final_output = ''
    while True:
        export_type = input('[*] Enter export format (HTML/TXT): ').lower()
        export_type = '.' + export_type
        if export_type == '.html':
            final_output = get_html_report(lu, lp, le, oo)
            break
        elif export_type == '.txt':
            final_output = get_txt_report(lu, lp, le, oo)
            break
        else:
            print('   [-] Sorry, your expected type currently is not supported')
    if final_output == '':
        print('Nothing to Export')
        return
    write_output = open('export/' + get_name() + export_type, 'w', encoding='UTF8')
    write_output.write(final_output)
    print('[+] Your report successfully saved to:\n'
          f'\t{os.getcwd()}/export/{get_name() + export_type}')
