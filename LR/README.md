# 逻辑斯蒂回归模型：分类模型

此处实现的是二项逻辑斯蒂回归模型，是二分类模型

值得注意的是，LR模型在用梯度下降法求解时，目的在于求解对数似然函数的**极大值**，因此，在更新参数W时，应该 **加上** 梯度 乘以 学习率，使得参数往**函数值增大的方向**变动。

运行`src/LogisticRegression.py`，如图：

![](./image/lr.png)