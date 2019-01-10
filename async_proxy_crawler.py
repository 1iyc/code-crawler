#! /usr/bin/env python
# coding: utf-8

import argparse
import asyncio
import aiohttp
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from random import randint
import traceback

parser = argparse.ArgumentParser(description="Crawling Item Name and Code via Multiple Proxy Server with Async")

parser.add_argument('--uri', dest="uri", type=str, default=None,
                    help="URI, If You Want to Use Dictionary, Use '???' at Parameter Place"
                         "and If URI Page Number Has Page Number, Use '@@@' at Page Number Place")
parser.add_argument('--proxy_uri', dest="proxy_uri", type=str, default=None,
                    help="Proxy Site URI")

parser.add_argument('--dict_file', dest="dict_file", type=str, default=None,
                    help="Dictionary File Path Used on Search")
parser.add_argument('--output_file', dest="output_file", type=str, default="./data/data.txt",
                    help="Output Data File Path")
parser.add_argument('--output_dir', dest="output_dir", type=str, default="./data/output",
                    help="Output Data Directory Path")
parser.add_argument('--finished_file', dest="finished_file", type=str, default="./data/finished_data.txt",
                    help="Finished Data File Path")

args = parser.parse_args()


async def get_proxy(word):
    try:
        async with aiohttp.request("GET", args.proxy_uri, headers={'User-Agent:': UserAgent().random},
                                   allow_redirects=False) as res:
            row = BeautifulSoup(await res.text(), "html.parser")\
                .select("table > tbody > tr")[randint(0, 20)].select("td")
            proxy_ip = "http://" + row[0].text + ":" + row[1].text
            print("[{}] GET PROXY IP: {}".format(word, proxy_ip))
            return proxy_ip
    except Exception as e:
        print("!!! [{}] ERROR (GET PROXY) err: {}".format(word, e))
        return await get_proxy(word)


async def re_request(uri, word):
    print("[{}] RE REQUESTED".format(word))
    try:
        async with aiohttp.request("GET", uri, headers={'User-Agent:': UserAgent().random},
                                   proxy=await get_proxy(word), allow_redirects=False) as res:
            return BeautifulSoup(await res.text(), "html.parser")
    except (aiohttp.client_exceptions.ClientProxyConnectionError, aiohttp.client_exceptions.ClientOSError):
        # print("!!! [{}] RE REQUEST ERROR (CANNOT CONNECT to PROXY HOST)".format(word))
        return await re_request(uri, word)
    except Exception as e:
        print("!!! [{}] UNEXPECTED ERROR (RE REQUEST) err: {}".format(word, e))
        print(traceback.format_exc())
        return await re_request(uri, word)


async def get_last_page(soup, word):
    try:
        text = soup.select("div#pages > div#pages > a")[-2].text
        if text == "Prev":
            return 1
        else:
            return int(text) if int(text) < 21 else 20
    except (AttributeError, IndexError):
        # print("[{}] NOTHING SEARCHED".format(word))
        return 0
    except Exception as e:
        print("!!! [{}] UNEXPECTED ERROR (GET PAGE NUM) err: {}".format(word, e))
        print(traceback.format_exc())


async def write_items(soup):
    codes = soup.select("div.display_table > div.display_row1 > p > span")
    with open(args.output_file, "a", encoding="utf-8") as f:
        for code in codes:
            items = soup.select("div.display_table > div.display_row2 > p#" + code.text + " > span > a")
            for item in items:
                f.write(item.text + "\t" + code.text + "\n")


async def request_soup(uri, word):
    try:
        async with aiohttp.request("GET", uri, headers={'User-Agent:': UserAgent().random},
                                   proxy=await get_proxy(word), allow_redirects=False) as res:
            return BeautifulSoup(await res.text(), "html.parser")
    except (aiohttp.client_exceptions.ClientProxyConnectionError, aiohttp.client_exceptions.ClientOSError,
            aiohttp.client_exceptions.ServerDisconnectedError):
        # print("!!! [{}] ERROR (CANNOT CONNECT to PROXY HOST)".format(word))
        return await re_request(uri, word)
    except Exception as e:
        print("!!! [{}] UNEXPECTED ERROR (GET REQUEST VIA PROXY) err: {}".format(word, e))
        print(traceback.format_exc())
        return await re_request(uri, word)


async def page_crawling(uri, word, last_page):
    if last_page > 1:
        print("[{} - {}] STARTED".format(word, last_page))
        uri_page = uri.replace("@@@", str(last_page))

        soup = await request_soup(uri_page, word)
        await write_items(soup)
        await page_crawling(uri, word, last_page-1)
    else:
        return 0


async def multi_crawling(semaphore, word):
    await semaphore.acquire()
    print("[{}] STARTED".format(word))
    uri_word = args.uri.replace("???", word)
    uri_page = uri_word.replace("@@@", '1')

    soup = await request_soup(uri_page, word)

    last_page = await get_last_page(soup, word)
    print("[{}] TOTAL PAGE NUM: {}".format(word, last_page))

    if last_page > 0:
        await write_items(soup)
        await page_crawling(uri_word, word, last_page)

    with open(args.finished_file, "a", encoding="utf-8") as f:
        f.write(word + "\n")

    await asyncio.sleep(0.05)
    print("[{}] RELEASED".format(word))
    semaphore.release()


async def main(loop):
    word_list = list(open(args.dict_file, 'r', encoding="utf-8").readlines())
    crawler_semaphore = asyncio.Semaphore(value=20)
    await asyncio.wait([multi_crawling(crawler_semaphore, word.strip()) for word in word_list])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print("[!!! FINISHED !!!]")
    loop.close()
