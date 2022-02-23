#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date: 2022/02/22 14:41:17
@Author: rojer
"""

import numpy as np

from util import read


def fml_train(train_data, F, alpha, beta, step):
    """
    @Description: fml训练
    @Args:
        train_data: 训练数据
        F: 特征数
        alpha: 正则化参数
        beta: 学习率
        step: 重复次数
    @Returns:
        user_vec: 用户向量
        item_vec: 项目向量
    """

    user_vec = {}
    item_vec = {}
    for step_index in range(step):
        print("step_index=%d" % (step_index))
        for train_instance in train_data:
            user_id, item_id, label = train_instance
            # 初始化向量
            if user_id not in user_vec:
                user_vec[user_id] = init_model(F)
            if item_id not in item_vec:
                item_vec[item_id] = init_model(F)

            # loss
            delta = label - model_predict(user_vec[user_id], item_vec[item_id])

            for index in range(F):
                # 迭代每一个向量值
                user_vec[user_id][index] += beta * (
                    delta * item_vec[item_id][index] - alpha * user_vec[user_id][index]
                )
                item_vec[item_id][index] += beta * (
                    delta * user_vec[user_id][index] - alpha * item_vec[item_id][index]
                )

            # 迭代后对学习率进行收缩
            beta *= 0.9

    return user_vec, item_vec


def init_model(F):
    """
    @Description: 初始化向量
    @Args:
        F: 特征数
    @Returns:
        a vector
    """
    return np.random.randn(F)


def model_predict(user_vec, item_vec):
    """
    @Description: 用cos距离公式取预测值
    @Args:
        user_vec: 用户向量
        item_vec: 项目向量
    @Returns:
        number: 预测值
    """

    return np.dot(user_vec, item_vec) / (
        np.linalg.norm(user_vec) * np.linalg.norm(item_vec)
    )


def give_recommend_result(user_vec, item_vec, user_id, count):
    """
    @Description: 生成推荐结果
    @Args:
        user_vec: 用户向量
        item_vec: 项目向量
        user_id: 用户id
        count: 推荐数量
    @Returns:
        [(item_id, score),...]
    """

    if user_id not in user_vec:
        return []

    result = []

    for item_id in item_vec:
        label = model_predict(user_vec=user_vec[user_id], item_vec=item_vec[item_id])
        result.append((item_id, label))

    list = []
    for (item_id, score) in sorted(
        result, key=lambda element: element[1], reverse=True
    )[:count]:
        list.append((item_id, round(score, 3)))

    return list


def ana_recommend_result(train_data, user_id, recommend_list):
    """
    @Description: 展示推荐结果与验证
    @Args:
        train_data: 训练数据
        user_id: 用户id
        recommend_list: 推荐结果
    """

    infos = read.get_item_info("./data/movies.txt")
    for train_instance in train_data:
        user_id_temp, item_id, label = train_instance
        if user_id == user_id_temp and label == 1:
            print(infos[item_id])
    print("recommend result:")
    for recommend in recommend_list:
        item_id, score = recommend
        print(infos[item_id], score)


def model_train_processer():
    train_data = read.get_train_data("./data/ratings.txt")
    user_vec, item_vec = fml_train(
        train_data=train_data, F=50, alpha=0.01, beta=0.1, step=50
    )

    user_id = "24"
    recommend_result = give_recommend_result(
        user_vec=user_vec, item_vec=item_vec, user_id=user_id, count=10
    )

    ana_recommend_result(
        train_data=train_data, user_id=user_id, recommend_list=recommend_result
    )


if __name__ == "__main__":
    model_train_processer()
