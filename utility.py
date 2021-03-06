import os
import requests
import json

def wise_mk_dir(path):
    if path == "":
        return
    if os.path.exists(path):
        return
    p, c = os.path.split(path)
    if not os.path.exists(p):
        wise_mk_dir(p)
    os.mkdir(path)

def wise_mk_dir_for_file(filepath):
    p = os.path.dirname(filepath)
    wise_mk_dir(p)

UA_LIST = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"
]


def random_ua():
    import random
    return random.choice(UA_LIST)

def get_ip_country(ip):
    api = "http://apis.baidu.com/apistore/iplookupservice/iplookup?ip=%s" % ip
    headers = {"apikey":"bebdaf5a1d4d124669b121a990c9fb44"}
    r = requests.get(api, headers=headers, timeout=5)
    if r.status_code != 200:
        return None
    try:
        t = json.loads(r.content)
        return t["retData"]["country"].encode("utf-8")
    except:
        return None

def proxy_request(url, proxy_url, user_agent=None, timeout=None):
    proxies = {
        "http": proxy_url
    }
    headers = {}
    if user_agent:
        headers["user-agent"] = user_agent
    if timeout:
        return requests.get(url, proxies=proxies, headers=headers, timeout=timeout)
    else:
        return requests.get(url, proxies=proxies, headers=headers)