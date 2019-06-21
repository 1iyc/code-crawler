#! /usr/bin/env python
# coding: utf-8

import argparse
from datetime import datetime
import asyncio
import requests
from fake_useragent import UserAgent
from random import randint
from random import uniform
from time import sleep
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Crawling Item Name and Code via Multiple Proxy Server")

parser.add_argument('--uri', dest="uri", type=str, default=None,
                    help="URI, If You Want to Use Dictionary, Use '???' at Parameter Place"
                         "and If URI Page Number Has Page Number, Use '@@@' at Page Number Place")
parser.add_argument('--proxy_uri', dest="proxy_uri", type=str, default=None,
                    help="Proxy Site URI")

parser.add_argument('--dict_file', dest="dict_file", type=str, default=None,
                    help="Dictionary File Path Used on Search")
parser.add_argument('--output_file', dest="output_file", type=str, default="./data/data.txt",
                    help="Output Data File Path")
parser.add_argument('--finished_file', dest="finished_file", type=str, default="./data/finished_data.txt",
                    help="Finished Data File Path")

args = parser.parse_args()

count = 0


def get_proxy(proxy_uri):
    proxies_req = requests.get(proxy_uri, headers={'User-Agent': UserAgent().random})
    proxies_dom = BeautifulSoup(proxies_req.content, "html.parser")
    proxies_tr = proxies_dom.select("table > tbody > tr")

    try:
        random_int = randint(0, len(proxies_tr) - 1)
    except Exception as e:
        print(e)
        return get_proxy(proxy_uri)

    proxy = {
        "http": proxies_tr[random_int].select("td")[0].text+":" + proxies_tr[random_int].select("td")[1].text,
        "https": proxies_tr[random_int].select("td")[0].text+":" + proxies_tr[random_int].select("td")[1].text,
    }
    return proxy


async def crawling_items(semaphore, uri, proxy_uri, word, total_count, output_file, finished_file,
                         start_page=1, last_page=0):
    await semaphore.acquire()
    print("[ {} ]  STARTED!!!!! {}".format(word.strip(), datetime.now().strftime("%H:%M:%S %f")))
    if type(proxy_uri) == str:
        proxy = get_proxy(proxy_uri)
    else:
        proxy = proxy_uri

    uri_page = uri.replace("???", word)
    uri_page = uri_page.replace("@@@", str(start_page))

    try:
        req = requests.get(uri_page, proxies=proxy, timeout=5)
    except requests.exceptions.ProxyError:
        print("[ {} ]  PROXY ERROR!!!".format(word))
        crawling_items(uri, args.proxy_uri, word, output_file, start_page, last_page)
        return 0
    except requests.exceptions.Timeout:
        print("[ {} ]  TIMEOUT ERROR!!!".format(word))
        crawling_items(uri, args.proxy_uri, word, output_file, start_page, last_page)
        return 0
    except (ConnectionRefusedError, requests.exceptions.ConnectionError):
        print("[ {} ]  CONNECTION ERROR!!!".format(word))
        crawling_items(uri, args.proxy_uri, word, output_file, start_page, last_page)
        return 0
    except Exception as e:
        print("[ {} ]  UNEXPECTED ERROR!!! {}".format(word, e))
        crawling_items(uri, args.proxy_uri, word, output_file, start_page, last_page)
        return 0

    dom = BeautifulSoup(req.content, "html.parser")

    codes = dom.select("div.display_table > div.display_row1 > p > span")

    if not last_page:
        pages = dom.select("div#pages > div#pages > a")
        try:
            last_page = int(pages[-2].text)
            print("[ {} ]  TOTAL PAGE\t{}".format(word, last_page-1))
            if last_page > 21:
                last_page = 21
        except IndexError:
            print("[ {} ]  NOT EXISTED".format(word))
            return 1
        except ValueError:
            last_page = 2
            print("[ {} ]  TOTAL PAGE\t{}".format(word, last_page-1))

    f = open(output_file, 'a', encoding="utf-8")

    for code in codes:
        # f.write(data.text + "\n")
        items = dom.select("div.display_table > div.display_row2 > p#" + code.text + " > span > a")
        for item in items:
            f.write(item.text + "\t" + code.text + "\n")

    f.close()

    print("[ {} ]  {}/{}".format(word, start_page, last_page-1))

    start_page += 1

    if start_page < last_page and start_page < 21:
        sleep(uniform(0.01, 0.05))
        crawling_items(uri, proxy, word, output_file, start_page, last_page)

    sleep(uniform(0.05, 0.1))


async def main(loop):
    word_list = list(open(args.dict_file, 'r', encoding="utf-8").readlines())
    output_file = open(args.output_file, 'a', encoding="utf-8")
    finished_file = open(args.finished_file, 'a', encoding="utf-8")

    total_count = len(word_list)

    crawler_semaphore = asyncio.Semaphore(value=10)
    await asyncio.wait([crawling_items(crawler_semaphore, args.uri, args.proxy_uri, word.strip(),
                                       total_count, output_file, finished_file) for word in word_list])

    # print("[ {} ]  ENDED!!!!! {}".format(word.strip(), datetime.now().strftime("%H:%M:%S %f")))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print("[!!! FINISHED !!!]")
    loop.close()
