"""
- To use ZAP you should run these command:
    $ cd /usr/share/zaproxy/
    $ ./zap.sh -daemon -config api.key="<YOUR_API_KEY>" -port <YOUR-PORT | Default:8090> -config
        api.addrs.addr.name=.* -config api.addrs.addr.regex=true
"""

import json
import argparse
from core import ZAP_SCAN


def logo():
    my_log = """
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   
    ▒███████▒ ▄▄▄       ██▓███    ██████  ▄████▄   ▄▄▄       ███▄    █ 
    ▒ ▒ ▒ ▄▀░▒████▄    ▓██░  ██▒▒██    ▒ ▒██▀ ▀█  ▒████▄     ██ ▀█   █ 
    ░ ▒ ▄▀▒░ ▒██  ▀█▄  ▓██░ ██▓▒░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██  ▀█ ██▒
      ▄▀▒   ░░██▄▄▄▄██ ▒██▄█▓▒ ▒  ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▓██▒  ▐▌██▒
    ▒███████▒ ▓█   ▓██▒▒██▒ ░  ░▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒▒██░   ▓██░
    ░▒▒ ▓░▒░▒ ▒▒   ▓▒█░▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ 
    ░░▒ ▒ ░ ▒  ▒   ▒▒ ░░▒ ░     ░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░░ ░░   ░ ▒░
    ░ ░ ░ ░ ░  ░   ▒   ░░       ░  ░  ░  ░          ░   ▒      ░   ░ ░ 
      ░ ░          ░  ░               ░  ░ ░            ░  ░         ░ 
    ░                                    ░                               
                                                                 
                    owner: Majid Iranpour
                     twitter: @_majidmc2
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""
    print('\033[92m', my_log, '\033[0m')


def save_to_json(data, file):
    try:
        with open(file, 'w') as outfile:
            json.dump(data, outfile)
    except Exception as e:
        print('\033[93m', e, '\033[0m')


def main():
    parser = argparse.ArgumentParser(prog="zap_scan",
                                     usage=logo(),
                                     description="This script spider and scan your target whit OWASP-Zap API")
    parser.add_argument('-u', action='store', help='A target URI', required=True, dest='url')
    parser.add_argument('-o', action='store', help='Save output as JSON in a file', dest='output')
    parser.add_argument('--scan', action='store_true', default=False, help='Scan a target', dest='scan')
    parser.add_argument('--spider', action='store_true', default=False, help='Spider a target', dest='spider')
    parser.add_argument('--api-key', action='store', type=str, help='ZAP API-Key', required=True, dest='api_key')
    parser.add_argument('--http_proxy', action='store', type=str, help='ZAP HTTP-Proxy [Default "127.0.0.1:8090"]',
                        dest='http_proxy', default='127.0.0.1:8090')
    parser.add_argument('--https_proxy', action='store', type=str, help='ZAP HTTPS-Proxy [Default "27.0.0.1:8090"]',
                        dest='https_proxy', default='127.0.0.1:8090')
    args = parser.parse_args()

    if not args.scan and not args.spider:
        print('\033[93m', "[Error] Select '--scan' or '--spider'", '\033[0m')

    elif args.scan:
        zap_class = ZAP_SCAN(args.api_key, args.http_proxy, args.https_proxy)
        result = zap_class.start_spider_and_scan(args.url)
        if args.output:
            save_to_json(result, args.output)
        else:
            print(json.dumps(result, indent=4))

    elif args.spider:
        zap_class = ZAP_SCAN(args.api_key, args.http_proxy, args.https_proxy)
        result = zap_class.start_spider(args.url)
        if args.output:
            save_to_json(result, args.output)
        else:
            print(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
