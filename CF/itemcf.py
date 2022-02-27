#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date: 2022/02/27 13:26:12
@Author: rojer
"""


import math
import operator
import sys
import read


def itemcf_get_contribute(type, user_click_count, click_time1=0, click_time2=0):

    # 用户点击惩罚贡献度，用户点击item越多，贡献度越小
    if type == 2:
        return 1 / math.log10(1 + user_click_count)

    # 用户点击的时间离现在越早，贡献度越小
    if type == 3:
        t = abs(click_time1 - click_time2) / (24 * 60 * 60)
        return 1 / (1 + t)

    # 基础贡献度，每一个增加1
    return 1


def itemcf(user_click, type):

    """
    @Description: itemcf
    @Args:
        user_click: 用户点击数据
        type: 贡献度计算方式，1-基础 2-按用户点击数量进行惩罚
    @Returns:
    """

    record = {}
    click_times = {}
    topk = 10
    for user, items in user_click.items():
        for i in range(len(items)):
            item_id_i = items[i][0]
            click_times.setdefault(item_id_i, 0)
            click_times[item_id_i] += 1
            for j in range(i + 1, len(items)):
                item_id_j = items[j][0]
                click_time1 = items[i][1]
                click_time2 = items[j][1]
                record.setdefault(item_id_i, {})
                record[item_id_i].setdefault(item_id_j, 0)
                record[item_id_i][item_id_j] += itemcf_get_contribute(
                    type, len(items), click_time1, click_time2
                )

                record.setdefault(item_id_j, {})
                record[item_id_j].setdefault(item_id_i, 0)
                record[item_id_j][item_id_i] += itemcf_get_contribute(
                    type, len(items), click_time1, click_time2
                )

    item_sim_score = {}
    for i in record.keys():
        for j in record[i].keys():
            item_sim_score.setdefault(i, {})
            # similar_score = contribute / sqrt(click_count(item_i) * click_count(item_j))
            item_sim_score[i][j] = record[i][j] / math.sqrt(
                click_times[i] * click_times[j]
            )

    for item_id, list in item_sim_score.items():
        item_sim_score[item_id] = sorted(
            list.items(), key=operator.itemgetter(1), reverse=True
        )[:topk]

    return item_sim_score


def recommend_itemcf(item_sim_score, user_click):
    record = {}
    topk = 5
    click_usecount = 3
    for user_id, items in user_click.items():
        for item_id, t in items[:click_usecount]:
            if item_id not in item_sim_score:
                continue
            record.setdefault(user_id, [])
            record[user_id] += item_sim_score[item_id][:topk]

    return record


def debug_recommend(fix_item_id, item_sim_score, infos):
    if fix_item_id in infos:
        print(infos[fix_item_id])

    print("sim items:")
    if fix_item_id in item_sim_score:
        sim_list = item_sim_score[fix_item_id][:5]
        for (item_id, score) in sim_list:
            if item_id in infos:
                print(infos[item_id], score)


if __name__ == "__main__":
    infos = read.get_item_info("./data/movies.txt")
    user_click = read.get_user_click("./data/ratings.txt")

    contribute_type = 3
    item_sim_score = itemcf(user_click, contribute_type)

    fix_item_id = "1"

    print("---------------------")
    print("-  debug_recommend  -")
    debug_recommend(fix_item_id, item_sim_score, infos)

    user_recommends = recommend_itemcf(item_sim_score, user_click)
    print("---------------------")
    print("-  user_recommend   -")

    fix_user_id = "1"
    if fix_user_id not in user_recommends:
        print("recommend not exist")
        sys.exit()
    user_recommend = user_recommends[fix_user_id]

    for (item_id, score) in user_recommend[:10]:
        if item_id in infos:
            print(infos[item_id], score)
