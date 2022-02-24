#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date: 2022/02/24 13:07:49
@Author: rojer
"""

import os
import sys


def produce_train_data(input_file, out_file):
    """
    @Description: 生成训练文件
    @Args:
        input_file: 输入文件
        out_file: 输出文件
    """

    if not os.path.exists(input_file):
        return

    linenum = 0
    rating_spt = 4.0
    fp = open(input_file)

    record = {}
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        items = line.strip().split(",")
        if len(items) < 4:
            continue
        user_id, item_id, rating = items[0], items[1], float(items[2])

        if rating < rating_spt:
            continue
        if user_id not in record:
            record[user_id] = []
        record[user_id].append(item_id)

    fp.close()

    fw = open(out_file, "w+")

    for user_id in record:
        fw.write(" ".join(record[user_id]) + "\n")

    fw.close()


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("please input the train data file")
        sys.exit()
    produce_train_data(sys.argv[1], "../data/train_data.txt")
