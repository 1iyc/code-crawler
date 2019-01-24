#! /usr/bin/env python
# coding: utf-8

import argparse
import os

parser = argparse.ArgumentParser(description="Merge Separated Data")

parser.add_argument('--main_file', dest="main_file", type=str, default="./data/data.txt",
                    help="Main Data File. Merge to Main Data")
parser.add_argument('--sub_file', dest="sub_file", type=str, default="./data/data_sub.txt",
                    help="Sub Data File. Data File Merged to Main Data")

args = parser.parse_args()


def merge_data(main_file, sub_file):
    mf = open(main_file, 'a', encoding="utf-8")

    with open(sub_file, 'r', encoding="utf-8") as f:
        for line in f:
            mf.write(line)


def main():
    merge_data(args.main_file, args.sub_file)


if __name__ == '__main__':
    main()