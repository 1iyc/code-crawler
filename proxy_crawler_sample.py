#! /usr/bin/env python
# coding: utf-8

import argparse
import requests
from fake_useragent import UserAgent
from random import randint
from random import uniform
from time import sleep
from bs4 import BeautifulSoup


def proxy_crawl(uri, proxy_uri):
    if type(proxy_uri) == str:
        proxies_req = requests.get(proxy_uri, headers={'User-Agent': UserAgent().random})
        proxies_dom = BeautifulSoup(proxies_req.content, "html.parser")
        proxies_tr = proxies_dom.select("table > tbody > tr")

        proxies = []
        for row in proxies_tr[:5]:
            proxies.append({
                "http": row.select("td")[0].text+":" + row.select("td")[1].text,
                "https": row.select("td")[0].text+":" + row.select("td")[1].text,
            })
            print(proxies)
            print(len(proxies))

        try:
            proxy = proxies[randint(0, len(proxies) - 1)]
        except Exception as e:
            print(proxy)
            print(len(proxy))
            print(e)
            proxy_crawl(uri, proxy_uri)
        print("PROXY IP\t{}".format(proxy['http']))
    else:
        proxy = proxy_uri

    try:
        # Plz modify this for customize
        req = requests.get(uri, proxies=proxy, timeout=5)
    except requests.exceptions.ProxyError:
        print("PROXY ERROR!!!")
        proxy_crawl(uri, proxy_uri)
        return 0
    except requests.exceptions.Timeout:
        print("TIMEOUT ERROR!!!")
        proxy_crawl(uri, proxy_uri)
        return 0
    except (ConnectionRefusedError, requests.exceptions.ConnectionError):
        print("CONNECTION ERROR!!!")
        proxy_crawl(uri, proxy_uri)
        return 0
    except Exception as e:
        print("UNEXPECTED ERROR!!! {}")
        proxy_crawl(uri, proxy_uri)
        return 0

    sleep(uniform(0.05, 0.1))


def main():
    parser = argparse.ArgumentParser(description="Crawling Item Name and Code via Multiple Proxy Server")

    parser.add_argument('--uri', dest="uri", type=str, default=None,
                        help="URI, If You Want to Use Dictionary, Use '???' at Parameter Place"
                             "and If URI Page Number Has Page Number, Use '@@@' at Page Number Place")
    parser.add_argument('--proxy_uri', dest="proxy_uri", type=str, default="https://free-proxy-list.net/",
                        help="Proxy Site URI")

    args = parser.parse_args()

    proxy_crawl(args.uri, args.proxy_uri)


if __name__ == '__main__':
    main()