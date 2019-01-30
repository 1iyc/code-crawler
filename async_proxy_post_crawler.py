#! /usr/bin/env python
# coding: utf-8

import argparse
import asyncio
import ast
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


parser.add_argument('--post_data', dest="post_data", type=str, default=None,
                    help="Post Data File")
parser.add_argument('--item_prop', dest="item_prop", type=str, default=None,
                    help="Post Data File")
parser.add_argument('--page_prop', dest="page_prop", type=str, default=None,
                    help="Post Data File")


parser.add_argument('--dict_file', dest="dict_file", type=str, default=None,
                    help="Dictionary File Path Used on Search")
parser.add_argument('--output_file', dest="output_file", type=str, default="./data/data.txt",
                    help="Output Data File Path")
parser.add_argument('--output_dir', dest="output_dir", type=str, default="./data/output",
                    help="Output Data Directory Path")
parser.add_argument('--finished_file', dest="finished_file", type=str, default="./data/finished_data.txt",
                    help="Finished Data File Path")

args = parser.parse_args()


async def get_proxy(word, count=11):
    count = count - 1
    if not count:
        raise RecursionError

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
        return await get_proxy(word, count)


async def re_request(uri, word, post_data, count=11):
    print("[{}] RE REQUESTED".format(word))
    count = count - 1
    if not count:
        raise RecursionError

    try:
        async with aiohttp.request("POST", uri, headers={'User-Agent:': UserAgent().random}, data=post_data,
                                   proxy=await get_proxy(word), allow_redirects=False) as res:
            print(await res.json(content_type="text/html"))
            return await res.json(content_type="text/html")
    except (aiohttp.client_exceptions.ClientProxyConnectionError, aiohttp.client_exceptions.ClientOSError):
        # print("!!! [{}] RE REQUEST ERROR (CANNOT CONNECT to PROXY HOST)".format(word))
        return await re_request(uri, word, post_data, count)
    except RecursionError:
        print("!!! [{}] RECURSION ERROR (RE REQUEST)".format(word))
    except Exception as e:
        print("!!! [{}] UNEXPECTED ERROR (RE REQUEST) err: {}".format(word, e))
        print(traceback.format_exc())
        return await re_request(uri, word, post_data, count)


async def write_items(post_data):
    with open(args.output_file, "a", encoding="utf-8") as f:
        for data in post_data['uls_dmst']['itemList']:
            f.write(data['CMDT_NM_TIT'] + "\t" + data['DTRM_HS_SGN'] + "\n")


async def request_post(uri, word, post_data):
    try:
        async with aiohttp.request("POST", uri, headers={'User-Agent:': UserAgent().random},
                                   proxy=await get_proxy(word), data=post_data,
                                   allow_redirects=False) as res:
            print(await res.json(content_type="text/html"))
            return await res.json(content_type="text/html")
    except (aiohttp.client_exceptions.ClientProxyConnectionError, aiohttp.client_exceptions.ClientOSError,
            aiohttp.client_exceptions.ServerDisconnectedError):
        # print("!!! [{}] ERROR (CANNOT CONNECT to PROXY HOST)".format(word))
        return await re_request(uri, word, post_data)
    except Exception as e:
        print("!!! [{}] UNEXPECTED ERROR (GET REQUEST VIA PROXY) err: {}".format(word, e))
        print(traceback.format_exc())
        return await re_request(uri, word, post_data)


async def page_crawling(uri, word, post_data, last_page):
    if last_page > 1:
        print("[{} - {}] STARTED".format(word, last_page))
        post_data[args.page_prop] = last_page

        res_data = await request_post(args.uri, word, post_data)
        await write_items(res_data)
        await page_crawling(uri, word, last_page-1)
    else:
        return 0


async def multi_crawling(semaphore, word, post_data):
    await semaphore.acquire()
    print("[{}] STARTING".format(word))

    for word_prop in [x.strip() for x in args.item_prop.split(',')]:
        post_data[word_prop] = word
    post_data[args.page_prop] = 1

    try:
        res_data = await request_post(args.uri, word, post_data)

        last_page = res_data["paginationInfo"]["lastPageNo"]
        print("[{}] TOTAL PAGE NUM: {}".format(word, last_page))

        if last_page > 0:
            await write_items(res_data)
            await page_crawling(args.uri, word, post_data, last_page)

        with open(args.finished_file, "a", encoding="utf-8") as f:
            f.write(word + "\n")

        await asyncio.sleep(0.05)
        print("[{}] RELEASED".format(word))
        semaphore.release()
    except RecursionError:
        print("[{}] RECURSION ERROR (MULTI CRAWLING)".format(word))
        await asyncio.sleep(0.05)
        semaphore.release()


async def main(loop):
    word_list = list(open(args.dict_file, 'r', encoding="utf-8").readlines())
    post_data = ast.literal_eval(open(args.post_data, 'r', encoding="utf-8").readline().strip())
    crawler_semaphore = asyncio.Semaphore(value=1)
    await asyncio.wait([multi_crawling(crawler_semaphore, word.strip(), post_data) for word in word_list])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print("[!!! FINISHED !!!]")
    loop.close()
