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
