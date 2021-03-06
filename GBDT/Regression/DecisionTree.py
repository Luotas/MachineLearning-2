# -*- coding: utf-8 -*-
# @Time    : 2019/9/13 14:56
# @Author  : Weiyang
# @File    : DecisionTree.py

############################################################################
# 决策树模型
# 决策树模型是一种分类与回归方法，可以视为if-then规则的集合，也可以认为是定义在
#             特征空间与类空间上的条件概率分布。

# 决策树学习包含三个部分：特征选择，决策树生成和决策树剪枝
# 特征选择的指标：信息增益最大，信息增益比最大，平方误差最小和基尼指数最小
# 决策树生成算法：ID3算法，C4.5算法和CART算法
# 决策树剪枝：防止过拟合，目标是使决策树损失函数最小
############################################################################

import numpy as np
from TreeNode import TreeNode

class DecisionTree:
    '''回归树模型,该类是CART回归决策树的父类'''
    def __init__(self,min_samples_split=2,min_impurity=1e-7,max_depth=float("inf"),loss=None):
        self.root = None # 决策树的根节点
        self.min_samples_split = min_samples_split # 拆分节点时所需要的最小样本数
        self.min_impurity = min_impurity # 拆分节点时所需要的最小impurity，该值可以是信息增益，信息增益比，基尼指数，平方误差损失
        self.max_depth = max_depth # 决策树的最大深度
        self.impurity_calculation = None # 计算信息增益，信息增益比，基尼指数等
        self.leaf_value_calculation = None # 叶节点输出值的方法，分类树：选取出现次数最多的类标签；回归树：取所有值的均值
        # 判断y是一维的还是多维的，一维的，如[label,label,...];多维的，如[[0,1,0],[1,0,0],...]
        self.one_dim = None
        self.loss = loss # 用于梯度提升(Gradient Boost)

    def _labelCounts(self,Y):
        '''统计各个类别的取值个数,Y=[label1,label2,...]'''
        results = {}
        for label in Y:
            # 判断label是否在results
            if label not in results:
                results[label] = 0
            results[label] += 1 # 计数加1
        return results

    def _entropy(self,Y):
        '''计算数据集的熵，Y=[label1,label2,...]'''
        from math import log
        # 各个类别的数据量
        results = self._labelCounts(Y)
        # 计算熵值
        ent = 0.0
        # 遍历每个类别
        for label in results.keys():
            # 当前类别的概率
            p = float(results[label]) / len(Y)
            ent = ent - p * log(p,2)
        return ent

    def _divideOnFeature(self,X,feature_index,threshold):
        '''基于某个特征来切分数据集X，特征值大于threshold，为一类；小于threshold，为另一类'''
        split_func = None # 切分函数
        # 连续特征
        if isinstance(threshold,int) or isinstance(threshold,float):
            split_func = lambda sample:sample[feature_index] >= threshold
        else:
            # 离散型特征
            split_func = lambda sample:sample[feature_index] == threshold

        X_1 = np.array([sample for sample in X if split_func(sample)])
        X_2 = np.array([sample for sample in X if not split_func(sample)])
        return X_1,X_2

    def _buildTree(self,X,Y,current_depth=0):
        '''
        递归生成决策树：根据X的特征，以信息增益或信息增益比或基尼指数为分割依据，分裂X，从而生成决策树
        X = np.array([[value,value,...],...]),Y = [label1,label2,...]
        features = [0,1,2,...] 用于切分节点的特征索引集合
        '''
        max_impurity = 0 # 存储信息增益，信息增益比或基尼指数的最大值，便于确定以哪个特征作为结点的特征
        best_criteria = None # 分裂节点的最佳判别标准,事实上存储的是 特征的索引和阈值threshold
        best_sets = None #

        # 样本数，特征数
        n_samples,n_features = np.shape(X)
        # 将特征和类别合并在一起
        Y = np.array(Y)
        # 确保Y的维度长度至少为2，否则不能拼接
        if len(Y.shape) == 1:
            Y = np.expand_dims(Y,axis=1) # Y = np.array([[label],[label],..])
        data = np.concatenate((X,Y),axis=1)
        # 生成树
        # 如果样本数大于最小分割样本数，且当前深度小于最大深度
        if n_samples >= self.min_samples_split and current_depth <= self.max_depth:
            # 计算待选的特征序列中的每个特征的impurity(信息增益，信息增益比或基尼指数)
            for feature_index in range(n_features):
                # 取出训练数据X的当前特征的数据列
                feature_values = np.expand_dims(X[:,feature_index],axis=1)
                # 获取当前特征的所有可能取值
                unique_values = np.unique(feature_values)

                # 遍历当前特征的所有可能取值，以取值为特征的切分点，计算impurity
                for threshold in unique_values:
                    # 以当前特征的取值分割训练集data为两个子集
                    data1,data2 = self._divideOnFeature(data,feature_index,threshold)

                    # 如果data1和data2不空，则计算
                    if len(data1) > 0 and len(data2) > 0:
                        # 获取两个数据集的类别系列
                        label1 = data1[:,n_features:]# 去除多余的维度
                        label1 = [label[0] for label in label1 ]
                        label2 = data2[:,n_features:]
                        label2 = [label[0] for label in label2]
                        # 获取impurity
                        impurity = self.impurity_calculation(Y,label1,label2)

                        # 如果当前阈值threshold能够获得更大的impurity,那么记录该impurity到
                        # max_impurity和相应的特征
                        if impurity > max_impurity:
                            max_impurity = impurity
                            # 存储最佳的分割结点的特征以及以特征相应的分割阈值
                            best_criteria = {"feature_index":feature_index,"threshold":threshold}
                            # 最佳分割的数据集
                            best_sets = {
                                "leftX":data1[:,:n_features], # 位于左子节点的样本
                                "leftY":data1[:,n_features:], # 位于左子节点的样本标签
                                "rightX":data2[:,:n_features],# 位于右子节点的样本
                                "rightY":data2[:,n_features:] # 位于右子节点的样本标签
                            }
        # 经过当前最佳特征的特征值最佳分割点分割后的数据，继续递归构建左右子树
        # 如果当前数据集D，在当前特征的条件下，平方误差损失仍大于指定的阈值，则继续拆分节点
        if max_impurity > self.min_impurity and best_criteria != None:
            # 由此可看出，虽然特征会重复作为拆分节点的条件，但是每次拆分的threshold是不一样的
            #print(current_depth,best_criteria["feature_index"],best_criteria['threshold'])
            # 构建当前节点的左子树,节点深度加1
            true_branch = self._buildTree(best_sets["leftX"],best_sets["leftY"],current_depth+1)
            # 构建当前节点的右子树，节点深度加1
            false_branch = self._buildTree(best_sets["rightX"],best_sets["rightY"],current_depth+1)
            # 返回当前节点
            return TreeNode(feature_index=best_criteria["feature_index"],threshold=best_criteria["threshold"],
                            true_branch=true_branch,false_branch=false_branch)

        # 叶节点的输出值：分类时为类别，回归时为叶节点内样本的均值
        leaf_value = self.leaf_value_calculation(Y) #
        return TreeNode(value=leaf_value)

    def fit(self,X,Y,loss=None):
        '''
        决策树生成
        X = np.array([[value,value,...],...]),Y 一维编码= [label1,label2,...]；Y多维编码[[1,0,0],...]
        '''
        self.one_dim = len(np.shape(Y)) == 1 # 判断Y是一维编码还是多维编码
        self.root = self._buildTree(X,Y)
        self.loss = loss

    def predict_value(self,x,tree=None):
        '''
        对单个样本进行预测
        对树进行递归搜索，并根据我们最终到达的叶节点的值对数据样本进行预测
        x是单个样本,x = [value1,...]
        '''
        # tree开始时是根节点，递归后是内部节点
        if tree is None:
            tree = self.root
        # 当前节点是叶节点
        if tree.value is not None:
            return tree.value

        # 依据根节点的特征，获取用于决策的特征列
        feature_value = x[tree.feature_index]

        # 依据根节点的特征，判断是向左子树走还是右子树走
        branch = tree.false_branch
        if isinstance(feature_value,int) or isinstance(feature_value,float):
            # 如果是连续型特征
            if feature_value >= tree.threshold:
                branch = tree.true_branch
        # 离散型特征
        elif feature_value == tree.threshold:
            branch = tree.true_branch

        # 继续递归测试子树
        return self.predict_value(x,branch)

    def predict(self,X):
        '''对样本集X 进行预测'''
        y_pred = [] # 预测的标签
        for x in X:
            y_pred.append(self.predict_value(x))
        return y_pred

    def print_tree(self,tree=None,indent=" "):
        '''递归打印决策树'''
        if not tree:
            tree = self.root
        # 如果是叶子节点，则输出标签
        if tree.value is not None:
            print(tree.value)
        else:
            # 继续遍历
            # 输出节点的特征，节点判别的阈值
            print("%s:%s? " % (tree.feature_index,tree.threshold))
            # 输出左子树
            print("%sT->" % (indent),end="") # indent 用于缩进左右子树
            self.print_tree(tree.true_branch,indent + indent)
            # 输出右子树
            print("%sF->" % (indent),end="")
            self.print_tree(tree.false_branch,indent + indent)