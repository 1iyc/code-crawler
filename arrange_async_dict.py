#! /usr/bin/env python
# coding: utf-8

import argparse
import os

parser = argparse.ArgumentParser(description="Arrange Dictionary File for Async Crawler")

parser.add_argument('--dict_file', dest="dict_file", type=str, default=None,
                    help="Dictionary File Path Used on Search")
parser.add_argument('--finished_file', dest="finished_file", type=str, default="./data/finished_data.txt",
                    help="Output Data File Path")

args = parser.parse_args()


def arrange_dict(dict_file, finished_file):
    dict_list = list(open(dict_file, 'r', encoding="utf-8").readlines())
    finished_list = list(open(finished_file, 'r', encoding="utf-8").readlines())

    arrange_list = [line for line in dict_list if line not in finished_list]

    os.rename(dict_file, dict_file.replace(".txt", "_before.txt"))

    with open(dict_file, "w", encoding="utf-8") as f:
        for data in arrange_list:
            f.write(data)


def main():
    arrange_dict(args.dict_file, args.finished_file)


if __name__ == '__main__':
    main()