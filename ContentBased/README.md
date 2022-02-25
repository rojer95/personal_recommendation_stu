# ContentBased

基于 用户内容 推荐

## 步骤

1. 对item取平均分
2. 对item根据category进行划分并排序，排序按item平均分进行降序。即：得到category排行榜
3. 计算user对每种category的rating归一化值并降序排列
4. 通过步骤3得到的user-category-rating表与category排行榜结合计算推荐item

