import sys
import random
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import os

os.environ['MOZ_FORCE_DISABLE_E10S'] = '1'

def parse_args():
    """ Script arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', help='Enter the domain', required=True)
    return parser.parse_args()

def get_ua():
    """ Get a random user agent from this list for each request """
    ua_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0']
    ua = random.choice(ua_list)
    return ua

def start_browser():
    """ Start the browser with a random User-Agent """
    options = Options()
    user_agent = get_ua()
    options.add_argument(f"user-agent={user_agent}")
    br = webdriver.Firefox(options=options)
    br.implicitly_wait(10)
    return br

def interact_with_dnstwister(br, domain):
    br.get('https://dnstwister.report/')
    time.sleep(3)  # Wait for the page to load
    
    try:
        search_box = br.find_element(By.NAME, "domains")
        search_box.click()
        search_box.send_keys(domain)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)  # Wait for the results to load
    except Exception as e:
        print(f"An error occurred while interacting with dnstwister: {e}")

def open_page(br, domain):
    """ Open URLs each in its own tab """
    g_search_base = 'https://www.google.com/search?q='
    google_queries = (
        '',
        '+intitle:index.of',  # Dir indexing
        '+ext:xml+|+ext:conf+|+ext:cnf+|+ext:reg+|+ext:inf+|+ext:rdp+|+ext:cfg+|+ext:txt+|+ext:ora+|+ext:ini',  # Config files
        '+ext:sql+|+ext:dbf+|+ext:mdb',  # Database files
        '+ext:log',  # Logs
        '+ext:bkf+|+ext:bkp+|+ext:bak+|+ext:old+|+ext:backup',  # Backups
        '+intext:"sql syntax near"+|+intext:"syntax error has occurred"+|+intext:"incorrect syntax near"+|+intext:"unexpected end of SQL command"+|+intext:"Warning: mysql_connect()"+|+intext:"Warning: mysql_query()"+|+intext:"Warning: pg_connect()"',  # SQL errors
        '+filetype:asmx+|+inurl:jws?wsdl+|+filetype:jws+|+inurl:asmx?wsdl',  # WSDLs
        '+ext:doc+|+ext:docx+|+ext:odt+|+ext:pdf+|+ext:rtf+|+ext:sxw+|+ext:psw+|+ext:ppt+|+ext:pptx+|+ext:pps+|+ext:csv',  # Docs
    )

    urls = [f'{g_search_base}site:{domain}{q}' for q in google_queries]
    urls.append(f'{g_search_base}site:pastebin.com+{domain}')
    urls.append(f'{g_search_base}site:pastebin.com+"{domain}"')

    additional_urls = [
        f'https://viewdns.info/reverseip/?host={domain}&t=1',
        f'https://viewdns.info/iphistory/?domain={domain}',
        f'https://viewdns.info/httpheaders/?domain={domain}',
        f'https://web.archive.org/cdx/search/cdx?url=*.{domain}&output=xml&fl=original&collapse=urlkey',
        f'https://web.archive.org/web/20230000000000*/{domain}',
        f'https://viewdns.info/dnsrecord/?domain={domain}',
        f'https://viewdns.info/portscan/?host={domain}',
        f'https://crt.sh/?q={domain}',
        f'https://who.is/whois/{domain}',
        f'https://securitytrails.com/list/apex_domain/{domain}',
        f'https://urlscan.io/search/#{domain}',
        f'https://www.shodan.io/search?query={domain}',
        f'https://search.censys.io/search?resource=hosts&sort=RELEVANCE&per_page=25&virtual_hosts=EXCLUDE&q={domain}',
        f'https://dnshistory.org/dns-records/{domain}',
        f'https://www.wappalyzer.com/lookup/{domain}/',
        f'https://builtwith.com/{domain}',
        f'https://sitereport.netcraft.com/?url=http://{domain}',
        f'https://www.statscrop.com/www/{domain}',
        f'https://spyonweb.com/{domain}',
        f'https://securityheaders.com/?q={domain}&followRedirects=on',
        f'https://github.com/search?q={domain}&type=code',
        f'https://grep.app/search?q={domain}',
        f'https://trends.google.com/trends/explore?q={domain}',
        f'https://dnssec-debugger.verisignlabs.com/{domain}',
        f'https://dnsviz.net/d/{domain}/analyze/',
        f'https://buckets.grayhatwarfare.com/files?keywords={domain}',
    ]

    urls.extend(additional_urls)

    original_window = br.current_window_handle

    # Interact with dnstwister
    interact_with_dnstwister(br, domain)

    for index, u in enumerate(urls):
        time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
        br.execute_script("window.open();")
        br.switch_to.window(br.window_handles[-1])
        br.get(u)
        page_source = br.page_source
        if "did not match any documents" not in page_source:
            print(f"Results found for query: {u}")
        else:
            print(f"No results found for query: {u}")

    br.switch_to.window(original_window)
        
def main():
    args = parse_args()
    if args.domain.startswith('http'):
        sys.exit('[*] Do: -d example.com  Do not: -d http://example.com')
    
    br = start_browser()
    domain = args.domain
    open_page(br, domain)

if __name__ == "__main__":
    main()
