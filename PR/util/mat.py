#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date: 2022/02/23 15:29:23
@Author: rojer
"""

from scipy.sparse import coo_matrix
import numpy as np


def get_mat_from_graph(graph):
    """
    @Description: 将图转为M稀疏矩阵
    @Args:
        graph: 图
    @Returns:
        M: M稀疏矩阵
        index_dict: 所有点的下标字典
        vertex: 所有点
    """

    vertex = graph.keys()
    lenght = len(vertex)
    index_dict = {key: index for index, key in enumerate(vertex)}

    row = []
    col = []
    data = []
    for i in graph:
        weight = round(1 / len(graph[i]), 4)
        for j in graph[i]:
            row.append(index_dict[i])
            col.append(index_dict[j])
            data.append(weight)

    M = coo_matrix(
        (np.array(data), (np.array(row), np.array(col))), shape=(lenght, lenght)
    )
    return (M, index_dict, list(vertex))


def mat_all_point(M, alpha, vertex):
    """
    @Description: 计算 E - alpha * M‘
    @Args:
        M: M
        alpha: alpha
        vertex: id集
    @Returns:
    """

    lenght = len(vertex)
    row = []
    col = []
    data = []

    # 构建单位矩阵

    for i in range(lenght):
        row.append(i)
        col.append(i)
        data.append(1)

    E = coo_matrix(
        (np.array(data), (np.array(row), np.array(col))), shape=(lenght, lenght)
    )

    # PR矩阵公式=E-alpha*M(T)
    return E.tocsr() - alpha * M.tocsr().transpose()


# if __name__ == "__main__":
#     graph = read.get_train_data("../data/log.txt")
#     M, index_dict, vertex = get_mat_from_graph(graph)
#     result = mat_all_point(M, 0.7, vertex)
#     print(result)
