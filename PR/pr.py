#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Date: 2022/02/23 14:15:36
@Author: rojer
"""


from util import read
from util import mat
import operator
from scipy.sparse.linalg import gmres


def personal_rank(graph, alpha, step, root, return_num=10):
    """
    @Description: pr算法
    @Args:
        graph: 图
        alpha: 走往下一个节点的概率，1-alpha则表示会到自身的概率
        step: 循环次数
        root: 起始节点
        return_num: 返回数量
    @Returns:
        dict
    """

    rank = {}
    rank = {key: 0 for key in graph}
    rank[root] = 1

    for step_index in range(step):
        temp_rank = {}
        temp_rank = {key: 0 for key in graph}
        for out_key, out_value in graph.items():
            for iner_key, iner_value in out_value.items():
                # PR(a) = alpla * ( PR(A)/out(A) + PR(B)/out(B) ) 当 root != A 时候
                temp_rank[iner_key] += alpha * rank[out_key] / len(out_value)
                if iner_key == root:
                    # 当root == A 时，PR(A) = (1-aplha) + alpha * (1/PR(a) + 1/PR(b) + 1/PR(d))
                    temp_rank[iner_key] += 1 - alpha

        if temp_rank == rank:
            print("finished step id %d" % (step_index))
            break

        rank = temp_rank

    cc = 0
    result = {}
    for zhuhe in sorted(rank.items(), key=operator.itemgetter(1), reverse=True):
        key, ranking = str(zhuhe[0]), zhuhe[1]
        # 过滤用户
        if len(key.split("_")) < 2:
            continue

        # 过滤已经存在的图
        if key in graph[root]:
            continue

        result[key] = round(ranking, 4)
        cc += 1
        if cc > return_num:
            break

    return result


def personal_rank_mat(graph, root, alpha, return_num=10):
    """
    @Description: PR矩阵算法
    @Args:
        graph: 二分图
        root: 要生成的用户id
        alpha: 走往下一个节点的概率，1-alpha则表示会到自身的概率
        return_num: 返回预测数量
    @Returns:
    """

    # 将图转换为M
    M, index_dict, vertex = mat.get_mat_from_graph(graph)

    # 计算(E - (alpha * M'))的值，记作 mat_all
    mat_all = mat.mat_all_point(M, alpha, vertex)
    if root not in vertex:
        return {}

    # 构建r0矩阵
    r0 = [[1] for i in range(len(vertex))]
    r0[index_dict[root]] = [1]

    """
        求解pr值
        对于PR的矩阵方程：
               r = (1-alpha) * r0 + (alpha * M' * r)
            => r - (alpha * M' * r) = (1-alpha) * r0
            => r * (E - (alpha * M')) = (1-alpha) * r0
            (1-alpha) 作为常熟，直接略掉
            => r * (E - (alpha * M')) =  r0  
            =>  (E - (alpha * M')) * r =  r0 
            求解 r 
            令：
                A = (E - (alpha * M')) 
                b = r0
                x = r
            对于方程组Ax=b，直接使用gmres，求解得出（其中A已经在mat_all_point中求解）
    """

    r = gmres(mat_all, r0, tol=1e-8)[0]

    r_dict = {}
    for index, pr in enumerate(r):
        """
        过滤用户id
        过滤已经连通过的点
        """
        point = vertex[index]
        if len(point.strip().split("_")) < 2:
            continue
        if point in graph[root]:
            continue
        r_dict[point] = pr

    return_dict = {}
    # 按pr值排序，并返回
    for zhuhe in sorted(r_dict.items(), key=operator.itemgetter(1), reverse=True)[
        :return_num
    ]:
        point, pr = zhuhe[0], zhuhe[1]
        return_dict[point] = pr

    return return_dict


def personal_rank_process():
    """
    @Description: 普通PR算法
    """

    user_id = "2"
    graph = read.get_graph("./data/ratings.txt")
    rank_result = personal_rank(graph, 0.7, 100, user_id)
    infos = read.get_item_info("./data/movies.txt")

    for item_id, v in graph[user_id].items():
        id = str(item_id).split("_")[1]
        print(infos[id])

    print("pr result:")

    for item_id, rank in rank_result.items():
        id = str(item_id).split("_")[1]
        print(infos[id], rank)


def personal_rank_mat_process():
    """
    @Description: PR矩阵算法
    @Args:
    @Returns:
    """

    user_id = "A"
    graph = read.get_graph("./data/log.txt")
    print(personal_rank_mat(graph, user_id, 0.7))


def personal_rank_comp():
    """
    @Description: 对比普通PR算法与矩阵PR预测出的item重复数量
    """

    user_id = "1"
    graph = read.get_graph("./data/ratings.txt")
    alpha = 0.8
    count = 100

    normal_result = personal_rank(graph, alpha, 100, user_id, count)
    mat_result = personal_rank_mat(graph, user_id, alpha, count)

    count = 0
    for point in normal_result:
        if point in mat_result:
            count += 1

    print("same item count: %d" % (count))


if __name__ == "__main__":
    personal_rank_comp()
