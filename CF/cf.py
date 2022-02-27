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
    """
    @Description: 计算item与item的贡献度
    @Args:
        type: 贡献度计算类型（1-基础|2-根据用户点击计算|3-根据item之间点击时间计算）
    @Returns:
        number: 贡献度
    """

    # 用户点击的item越多，贡献度越小
    if type == 2:
        return 1 / math.log10(1 + user_click_count)

    # 两个item点击时间间隔越长，贡献度越小
    if type == 3:
        t = abs(click_time1 - click_time2) / (24 * 60 * 60)
        return 1 / (1 + t)

    # 基础贡献度，每一个增加1
    return 1


def cf(click_data, type):

    """
    @Description: 计算贡献度矩阵
    @Args:
        click_data: 点击数据
        type: 贡献度计算方式，1-基础 2-按用户点击数量进行惩罚
    @Returns:
        sim_score: {item: [(item, sim_score)]}
    """

    record = {}
    click_count = {}
    topk = 10
    for key, items in click_data.items():
        for i in range(len(items)):
            item_id_i = items[i][0]
            click_count.setdefault(item_id_i, 0)
            click_count[item_id_i] += 1
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

    sim_score = {}
    for i in record.keys():
        for j in record[i].keys():
            sim_score.setdefault(i, {})
            # similar_score = contribute / sqrt(click_count(item_i) * click_count(item_j))
            sim_score[i][j] = record[i][j] / math.sqrt(click_count[i] * click_count[j])

    for item_id, list in sim_score.items():
        sim_score[item_id] = sorted(
            list.items(), key=operator.itemgetter(1), reverse=True
        )[:topk]

    return sim_score


def recommend_itemcf(item_sim_score, user_click):
    """
    @Description: 根据item2item贡献度矩阵与用户点击item，生成用户的推荐item集合
    @Args:
        item_sim_score: item2item贡献度矩阵
        user_click: 用户点击
    @Returns:
        dict: {user: [(item_id, score)]}
    """

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


def debug_itemcf_recommend(fix_item_id, item_sim_score, infos):
    """
    @Description: debug item的相识item信息详情
    @Args:
        fix_item_id: 解决的item id
        item_sim_score: item2item相似度矩阵
        infos: item信息字典
    """

    if fix_item_id in infos:
        print(infos[fix_item_id])

    print("sim items:")
    if fix_item_id in item_sim_score:
        sim_list = item_sim_score[fix_item_id][:5]
        for (item_id, score) in sim_list:
            if item_id in infos:
                print(infos[item_id], score)


def itemcf():
    infos = read.get_item_info("./data/movies.txt")
    user_click = read.get_user_click("./data/ratings.txt")

    contribute_type = 3
    item_sim_score = cf(user_click, contribute_type)

    fix_item_id = "1"

    print("---------------------")
    print("-  debug_recommend  -")
    debug_itemcf_recommend(fix_item_id, item_sim_score, infos)

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


def transfer_item_2_user(userclick):
    item_click = {}
    for user_id, items in userclick.items():
        for (item_id, timestamp) in items:
            item_click.setdefault(item_id, [])
            item_click[item_id].append((user_id, timestamp))
    return item_click


def recommend_usercf(user_sim_score, user_click):
    """
    @Description: 根据user2user贡献度矩阵与用户点击item，生成用户的推荐item集合
    @Args:
        user_sim_score: user2user贡献度矩阵
        user_click: 用户点击
    @Returns:
        dict: {user: [(item_id, score)]}
    """

    record = {}
    topk = 5
    click_usecount = 3
    for user_id in user_click.keys():
        if user_id not in user_sim_score:
            continue
        record.setdefault(user_id, [])
        for (user_id_j, score) in user_sim_score[user_id][:click_usecount]:
            if user_id_j not in user_click:
                continue
            for (item_id, t) in user_click[user_id_j][:topk]:
                record[user_id].append((item_id, score))

    return record


def usercf():
    infos = read.get_item_info("./data/movies.txt")
    user_click = read.get_user_click("./data/ratings.txt")

    contribute_type = 3
    item_click = transfer_item_2_user(user_click)
    user_sim_score = cf(item_click, contribute_type)
    fix_user_id = "1"

    user_recommends = recommend_usercf(user_sim_score, user_click)
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


if __name__ == "__main__":
    itemcf()
    usercf()
