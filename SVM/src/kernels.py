# -*- coding: utf-8 -*-
# @Time    : 2019/9/22 21:31
# @Author  : Weiyang
# @File    : kernels.py

#===================================================================================================================
# 核函数(Kernel Function)
# 1. 概念：设X是输入空间，H为特征空间，如果存在一个从 X 到 H 的映射:
#                             φ(x) : X --> H
#    使得对所有 x,z ∈ X ,函数K(x,z)满足条件:
#                              K(x,z) = φ(x)·φ(z)
#    则称K(x,z) 为核函数，φ(x)为映射函数，式中 φ(x)·φ(z) 为 φ(x)和φ(z) 的内积。
# 2. 显然核函数计算的是两个向量经过高维映射(φ(x))后的点的内积，核函数在非线性支持向量机的作用便是
#    用原数据点在高维空间的内积(这个结果通过核函数可以计算出)，替换原数据点之间的内积。
# 3. 正定核：通常所说的核函数就是正定核，K(x,z)是正定核的充要条件 K(x,z)对应的格拉姆矩阵Gram是半正定矩阵。
# 4. 正定矩阵：设 M 是 n 阶方阵，如果对任何非零向量 Z，都有Z_T*M*Z > 0 ,Z_T是Z的转置，就称M为正定矩阵
# 5. 半正定矩阵：设 M 是 n 阶方阵，如果对任何非零向量 Z，都有Z_T*M*Z >= 0 ,Z_T是Z的转置，就称M为半正定矩阵

# 核技巧(Kernel Trick)
# 1. 思想: 通过一个非线性变换将输入空间对应于一个特征空间，使得在输入空间的超曲面模型(因为线性不可分，故而要分开只能是曲面，而不是平面)
#          对应于特征空间的超平面模型(支持向量机)。这样，分类问题的学习任务通过在特征空间中求解支持向量机就可以完成。
# 2. 具体操作：在学习与预测中，只定义核函数K(x,z)，而不显式地定义映射函数φ。通常，直接计算K(x,z)比较容易，通过φ(x)和φ(z)
#              计算K(x,z)并不容易。φ是输入空间到特征空间的映射，而特征空间一般是高维的，甚至是无穷维的，比如高斯核。
# 3. 核技巧在支持向量机中的作用：在支持向量机的对偶问题中，无论是目标函数还是决策函数(分离超平面)都只涉及
#                               输入实例与输入实例之间的内积。在对偶问题的目标函数中的内积x_i·x_j 可以用核函数
#                                          K(x_i,x_j) = φ(x_i)·φ(x_j) 来代替。
#                               这等价于经过映射函数φ，将原来的输入空间变换到一个新的特征空间，将输入空间中的内积x_i·x_j
#                               变换为特征空间中的内积φ(x_i)·φ(x_j)，在新的特征空间里从训练样本中学习线性支持向量机。
#                               因此，在核函数K(x,z)给定的条件下，可以利用解线性分类问题的方法求解非线性分类问题的支持向量机。
#                               学习是隐式地在特征空间进行的，不需要显式地定义特征空间和映射函数。

# 常用核函数
# 1. 线性核函数: 当多项式核函数的阶为1时，被称为线性核函数
# 2. 多项式核函数
# 3. 高斯核函数(RBF kernel，也叫径向基核函数)
#====================================================================================================================

import numpy as np
import scipy.spatial.distance as dist

class LinearKernel(object):
    '''线性核'''
    def __call__(self,X,Y): # __call__() 表明该类型是可调用的
        '''
        X = np.array([[value,...],...]),Y = np.array([value,...])
        求数据Y 与 数据集X 中每条数据的核函数值，即 高维特征空间的内积
        '''
        return np.dot(X,Y.T) # 一个标量

class PolyKernel(object):
    '''多项式核'''
    def __init__(self,degree=2):
        self.degree = degree # 表明是几阶多项式核

    def __call__(self,X,Y):
        '''
        X = np.array([[value,...],...]),Y= np.array([value,...])
        求数据Y 与 数据集X 中每条数据的核函数值，即 高维特征空间的内积
        '''
        return np.power(np.dot(X,Y.T),self.degree)

class RBF(object):
    '''RBF核，高斯核'''
    def __init__(self,gamma=0.1):
        self.gamma = gamma # RBF核参数，相当于1/(2sigma**2)

    def __call__(self,X,Y):
        '''
        X = np.array([[value,...],...]),Y = np.array([value,...])
        求数据Y 与 数据集X 中每条数据的核函数值，即 高维特征空间的内积
        '''
        X = np.atleast_2d(X)
        Y = np.atleast_2d(Y)
        # dist.cdist(X,Y) 计算欧式距离
        return np.exp(-self.gamma * dist.cdist(X,Y) ** 2).flatten()