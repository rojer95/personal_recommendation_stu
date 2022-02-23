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


def get_train_data(file_path):
    """
    @Description: 获取训练集
    @Args:
        file_path: 文件路径
    @Returns:
        [(user_id, item_id, label)]
    """

    if not os.path.exists(file_path):
        return []
    ave_score_dict = get_ave_score(file_path=file_path)

    fp = open(file_path)

    linenum = 0
    score_split = 4.0
    positive_dict = {}
    negative_dict = {}
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) != 4:
            continue
        user_id, item_id, ranting = item[0], item[1], float(item[2])
        if user_id not in positive_dict:
            positive_dict[user_id] = []
        if user_id not in negative_dict:
            negative_dict[user_id] = []
        if ranting >= score_split:
            positive_dict[user_id].append((item_id, 1))
        else:
            ave_score = ave_score_dict.get(item_id, 0)
            negative_dict[user_id].append((item_id, ave_score))

    fp.close()

    train_data = []
    for user_id in positive_dict:
        data_len = min(len(positive_dict[user_id]), len(negative_dict.get(user_id, [])))

        if data_len > 0:
            train_data += [
                (user_id, zhuhe[0], zhuhe[1]) for zhuhe in positive_dict[user_id]
            ][:data_len]
        else:
            continue
        sorted_negative_list = sorted(
            negative_dict.get(user_id, []), key=lambda element: element[1], reverse=True
        )[:data_len]
        train_data += [(user_id, zhuhe[0], 0) for zhuhe in sorted_negative_list]

    return train_data


# if __name__ == '__main__':
# item_dict = get_item_info('../data/movies.txt')
# print(len(item_dict))
# print(item_dict['1'])
# print(item_dict['11'])

# score_dict = get_ave_score('../data/ratings.txt')
# print(len(score_dict))
# print(score_dict['31'])

# train_data = get_train_data('../data/ratings.txt')
# print(len(train_data))
# print(train_data[:20])
