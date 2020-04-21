import time
import progressbar
from zapv2 import ZAPv2


class ZAP_SCAN:
    def __init__(self, zap_api_key, zap_http_proxy, zap_https_proxy):
        self.zap = ZAPv2(apikey=zap_api_key, proxies={'http': zap_http_proxy, 'https': zap_https_proxy})

    def __zap_spider(self, target):
        scan_id = self.zap.spider.scan(target)

        bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        print('\033[1m', "[*] Start spider module ...", '\033[0m')
        bar.start()
        while int(self.zap.spider.status(scan_id)) < 100:
            time.sleep(1)
            bar.update(int(self.zap.spider.status(scan_id)))
        bar.finish()

        urls = self.zap.spider.results()

        for i in range(0, len(urls)):
            url = str(urls[i])
            if 'ZAP' in url:
                url = url.replace('ZAP', 'ZAP_SCAN')
            urls[i] = url

        return urls

    def __zap_scanner(self, target):
        scan_id = self.zap.ascan.scan(target)

        bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'),
                                                           ' ', progressbar.Percentage()])
        print('\033[1m', "[*] Start scan module ...", '\033[0m')
        bar.start()
        while int(self.zap.ascan.status(scan_id)) < 100:
            time.sleep(3)
            bar.update(int(self.zap.ascan.status(scan_id)))
        bar.finish()

        alerts = list()
        for i in self.zap.core.alerts():
            if 'alert' in i and 'url' in i:
                alert = str(i['alert'])
                url = str(i['url'])

                if 'ZAP' in url:
                    url = url.replace('ZAP', 'ZAP_SCAN')

                alerts.append(
                    {
                        'alert': alert,
                        'url': url,
                        'attack': str(i['attack']),
                        'confidence': str(i['confidence']),
                        'cweid': str(i['cweid']),
                        'description': str(i['description']),
                        'evidence': str(i['evidence']),
                        'method': str(i['method']),
                        'name': str(i['name']),
                        'other': str(i['other']),
                        'param': str(i['param']),
                        'risk': str(i['risk']),
                        'solution': str(i['solution']),
                        'wascid': str(i['wascid'])
                    }
                )

        results = {
            'hosts: ': ', '.join(self.zap.core.hosts),
            'number_of_vulnerability': str(len(self.zap.core.alerts())),
            'results': alerts
        }

        return results

    def start_spider_and_scan(self, target):
        # print(self.zap_api_key, self.zap_http_proxy, self.zap_https_proxy)

        if "ZAP Error [java.net.NoRouteToHostException]: No route to host (Host unreachable)" in self.zap.urlopen(
                target):
            return {"error": "Host unreachable"}

        urls = self.__zap_spider(target)
        results = self.__zap_scanner(target)
        results['urls'] = urls

        return results

    def start_spider(self, target):
        # print(self.zap_api_key, self.zap_http_proxy, self.zap_https_proxy)

        if "ZAP Error [java.net.NoRouteToHostException]: No route to host (Host unreachable)" in self.zap.urlopen(
                target):
            return {"error": "Host unreachable"}

        return {"urls": self.__zap_spider(target)}
