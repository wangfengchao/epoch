import urllib

import time

from scrapy import crawler

from epoch.thread.detect_manager import Detect_Manager


def detect(*args):
    verify_url = "http://ip.chinaz.com/getip.aspx"
    proxy_host = "http://" + args[0] + ":" + args[1]
    response = urllib.urlopen(verify_url, proxies={"http": "http://210.83.223.26:80"})
    if response.getcode() == 200:
        return True
    else:
        return False

if __name__=="__main__":
    print crawler.settings.getlist('USER_AGENTS')

    # detecter = Detect_Manager(10)
    # detecter.start()
    # print detect("210.51.52.138", "8800")