#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date: 2022/02/25 18:52:33
@Author: rojer
"""
import operator
import os
from re import I
import read


def get_user_profile(file_path, item_category, count=3):
    """
    @Description: 获取用户对分类的用户画像
    @Args:
        file_path: rating file
        item_category: item-category dict
    @Returns:
    """

    if not os.path.exists(file_path):
        return {}

    fp = open(file_path)

    linenum = 0

    record = {}

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

        if item_id not in item_category:
            continue

        if rating < 4.0:
            continue

        if user_id not in record:
            record[user_id] = {}

        categorys = item_category[item_id]

        for category in categorys:
            if category not in record[user_id]:
                record[user_id][category] = 0.0
            record[user_id][category] += (
                rating * get_time_score(timestamp) * (1 / len(categorys))
            )

    fp.close()

    for user_id in record:

        # 排序
        record[user_id] = [
            (category, score)
            for (category, score) in sorted(
                record[user_id].items(), key=operator.itemgetter(1), reverse=True
            )[:count]
        ]

        # 归一化
        total_score = 0.0
        for (category, score) in record[user_id]:
            total_score += score

        record[user_id] = [
            (category, round(score / total_score, 4))
            for (category, score) in record[user_id]
        ]

    return record


def get_time_score(timestamp):
    fix_time_stamp = 1476086345
    total_sec = 24 * 60 * 60
    delta = (fix_time_stamp - timestamp) / total_sec / 100
    return round(1 / (1 + delta), 3)


def get_recommend(user_profile, rank, user_id, count=10):

    if user_id not in user_profile:
        return []
    user_category = user_profile[user_id]
    result = []

    for (category, score) in user_category:
        c = int(score * count) + 1
        if category not in rank:
            continue
        result += rank[category][:c]

    return result


if __name__ == "__main__":
    user_id = "1"
    ave = read.get_ave_score("./data/ratings.txt")
    rank, item_cate = read.get_cate_rank(ave, "./data/movies.txt")
    user_profile = get_user_profile("./data/ratings.txt", item_cate)
    print("user_profile:", user_profile[user_id])
    result = get_recommend(user_profile, rank, user_id)
    infos = read.get_item_info("./data/movies.txt")
    for (item, score) in result:
        if item in infos:
            print(infos[item], score)
