#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date: 2022/02/25 18:36:17
@Author: rojer
"""


import operator
import os
from unittest import result


def get_item_info(file_path):
    """
    @Description: 获取item信息
    @Args:
        file_path: 文件路径
    @Returns:
        {item_id: [title, genres]}
    """

    if not os.path.exists(file_path):
        print("not exist file: " + file_path)
        return {}

    linenum = 0
    infos = {}
    fp = open(file_path)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue

        items = line.strip().split(",")
        if len(items) < 3:
            continue
        elif len(items) == 3:
            item_id, title, genres = items[0], items[1], items[2]
        elif len(items) > 3:
            item_id, genres = items[0], items[-1]
            title = ",".join(items[1:-1])
        infos[item_id] = [title, genres]

    fp.close()
    return infos


def get_ave_score(file_path):
    """
    @Description: 获取平均分
    @Args:
        file_path: 文件路径
    @Returns:
        {item_id: average score }
    """

    if not os.path.exists(file_path):
        print("file not exist:" + file_path)
        return {}

    fp = open(file_path)
    linenum = 0
    aves = {}
    records = {}

    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        items = line.strip().split(",")
        if len(items) == 4:
            item_id, rating = items[1], float(items[2])
            if item_id not in records:
                records[item_id] = [0, 0]
            records[item_id][0] += 1
            records[item_id][1] += rating
    for item_id in records:
        aves[item_id] = round(records[item_id][1] / records[item_id][0], 3)

    return aves


def get_cate_rank(ave, file_path):
    """
    @Description: 根据分类对item做排行榜
    @Args:
        age: 平均分
        file_path: infos文件
    @Returns:
        ranks: {category: [(item, ranting), ....]}
        item_cate: {item: [category1, ...]}
    """

    if not os.path.exists(file_path):
        return {}
    linenum = 0

    fp = open(file_path)

    record = {}
    item_cate = {}
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue

        item = line.strip().split(",")
        if len(item) < 3:
            continue
        item_id, category_str = item[0], item[-1]
        catgeorys = category_str.strip().split("|")

        item_cate[item_id] = catgeorys

        for category in catgeorys:
            if category not in record:
                record[category] = []
            record[category].append((item_id, ave.get(item_id, 0)))
    fp.close()
    result = {}
    for category in record:
        result[category] = [
            (item_id, score)
            for (item_id, score) in sorted(
                record[category], key=operator.itemgetter(1), reverse=True
            )
        ]

    return result, item_cate


if __name__ == "__main__":
    ave = get_ave_score("./data/ratings.txt")
    rank = get_cate_rank(ave, "./data/movies.txt")
    print(rank["Animation"])
