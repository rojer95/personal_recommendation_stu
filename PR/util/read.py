#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date: 2022/02/22 13:40:18
@Author: rojer
"""

import os


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


def get_graph(file_path):
    """
    @Description: 获取训练集
    @Args:
        file_path: 文件路径
    @Returns:
        {item_id: {user_id:1, ...}, ..., {user_id: {item_id: 1, ...}}}
    """

    if not os.path.exists(file_path):
        return []

    linenum = 0
    rank_min = 4.0
    fp = open(file_path)

    train_data = {}

    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        items = line.strip().split(",")

        if len(items) >= 3:
            user_id, item_id, rank = items[0], "item_" + items[1], float(items[2])
            if rank < rank_min:
                continue
            if user_id not in train_data:
                train_data[user_id] = {}
            if item_id not in train_data:
                train_data[item_id] = {}
            train_data[user_id][item_id] = 1
            train_data[item_id][user_id] = 1

    fp.close()
    return train_data


if __name__ == "__main__":
    # item_dict = get_item_info('../data/movies.txt')
    # print(len(item_dict))
    # print(item_dict['1'])
    # print(item_dict['11'])

    train_data = get_train_data("../data/log.txt")
    print(train_data)
