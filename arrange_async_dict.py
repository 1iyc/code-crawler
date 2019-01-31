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

    dict_length = len(dict_list)
    print("Dict List Size: {}".format(dict_length))
    print("Finished List Size: {}".format(len(finished_list)))

    arrange_list = []
    for i, line in enumerate(dict_list):
        if (i+1) % 10000 == 0:
            print(str(i+1) + "/" + str(dict_length))
        if line not in finished_list:
            arrange_list.append(line)

    os.rename(dict_file, dict_file.replace(".txt", "_before.txt"))

    with open(dict_file, "w", encoding="utf-8") as f:
        for data in arrange_list:
            f.write(data)


def main():
    arrange_dict(args.dict_file, args.finished_file)


if __name__ == '__main__':
    main()