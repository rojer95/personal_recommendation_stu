#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date: 2022/02/27 13:18:02
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


def get_user_click(filepath):

    """
    @Description: 获取用户点击数据
    @Args:
        filepath: 用户评分数据文件
    @Returns:
        dict: {user_id: [(item_id, timestamp), ... ]}
    """

    if not os.path.exists(filepath):
        return {}

    record = {}
    linenum = 0
    fp = open(filepath)

    # 3分以上算用户点击
    click_score = 3.0

    for line in fp:
        if linenum == 0:
            linenum += 1
            continue

        item = line.strip().split(",")
        if len(item) < 4:
            continue
        user_id, item_id, rating, timestamp = (
            item[0],
            item[1],
            float(item[2]),
            int(item[3]),
        )

        if rating < click_score:
            continue

        record.setdefault(user_id, [])
        record[user_id].append((item_id, timestamp))

    fp.close()
    return record


if __name__ == "__main__":
    print(get_user_click("./data/ratings.txt")["1"])
