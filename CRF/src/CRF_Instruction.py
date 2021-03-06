# -*- coding: utf-8 -*-
# @Time    : 2019/10/27 19:28
# @Author  : Weiyang
# @File    : CRF_Instruction.py

#=======================================================================================================================
# 概率图模型：概率无向图(马尔可夫随机场) + 概率有向图(贝叶斯网络)
# 概念：结点表示一个随机变量，边表示随机变量之间的依赖关系。

# 条件随机场(conditional random field,CRF)：对P(Y|X)进行建模，属于判别模型；HMM是对P(X,Y)进行建模，属于生成模型
# 条件随机场模型实际上是定义在时序数据上的对数线性模型，学习方法包括极大似然估计和正则化的极大似然估计
# 概念：条件随机场是给定一组输入随机变量条件下，另一组输出随机变量的条件概率分布模型，其特点是假设输出随机变量构成
#       马尔可夫随机场(概率无向图模型),即给定随机变量X条件下，求随机变量Y的马尔可夫随机场。

# 概率无向图模型：是一个可以由无向图表示的联合概率分布，设有联合概率分布P(Y)，由无向图G=(V,E)表示，在图G中，结点表示随机变量
#                边表示随机变量之间的依赖关系。如果联合概率分布P(Y)满足成对、局部或全局马尔可夫性，就称此联合概率分布为概率
#                无向图模型，或马尔可夫随机场。

# 马尔可夫性假设：
# 这个假设直观理解就是无向图中的随机变量(组)，即无向图的结点(团)之间，如果不相邻，那么就是条件独立的；反之，相邻的无向图结点
# (团)之间是条件依赖的。
# 1. 成对马尔可夫性：给定 随机变量组Y_O 的条件下，随机变量Y_v 和 随机变量 Y_u 是条件独立的；这里u,v是图G中任意两个没有边连接的
#                   结点，其它所有结点用O表示；
# 2. 局部马尔可夫性：给定 随机变量组Y_W 的条件下，随机变量Y_v 和 随机变量组Y_O 是条件独立的；这里v是图G中任意一点，W是与v有边连接
#                   的所有结点，O是W和v以外的所有结点；
# 3. 全局马尔可夫性：给定 随机变量组Y_C 的条件下，随机变量组Y_A 和 随机变量组Y_B 是条件独立的；这里A和B是被结点集合C分开的任意
#                    两个结点集合；
# 成对的、局部的、全局的马尔可夫性定义是等价的。

# 概率无向图模型的因子分解：即如何求概率无向图表示的联合概率分布P(Y)
# 因子分解的含义：
# 1. 对给定的概率无向图模型，我们希望将整体的联合概率写成若干子联合概率的乘积的形式，也就是将联合概率进行因子分解，
#    这样便于模型的学习与计算。事实上，概率无向图模型的最大特点就是易于因子分解。
# 2. 将概率无向图模型的联合概率分布 表示为其最大团上的随机变量的函数的乘积形式的操作，称为概率无向图模型的因子分解；
# 3. 概率无向图模型的因子分解由 哈莫里斯-克利福德(Hammersley-Clifford) 定理来保证：
#                              P(Y) = 1/Z * ∏_C Ψ_C(Y_C)
#                              Z = ∑_Y ∏_C Ψ_C(Y_C)
#    C为图G上的最大团，Y_C表示C对应的随机变量，概率无向图模型的联合概率分布P(Y)可写作图中所有最大团C上的函数Ψ_C(Y_C)的乘积形式
#    Z是规范化因子，确保P(Y)构成一个概率分布，函数Ψ_C(Y_C)称为势函数，是严格正的，通常定义为指数函数：Ψ_C(Y_C) = exp(-E(Y_C))
# 4. 线性链条件随机场P(Y|X)的因子分解式的各因子是定义在相邻两个结点(最大团)上的势函数。

# 团与最大团：
# 1. 团：无向图G中任何两个结点均有边连接的结点子集称为团(clique)
# 2. 最大团：团中无法再加进任何一个结点使其成为一个更大的团，这个团就是最大团(max clique)
# 3. 团和最大团的数量不固定

# 条件随机场
# 概念：设 X与Y 是随机变量，P(Y|X)是在给定X的条件下，Y的条件概率分布。若随机变量Y构成一个由无向图G=(V,E)表示的马尔可夫随机场
#       即 P(Y_v|X,Y_w,w≠v) = P(Y_v|X,Y_w,w～v) ，对任意结点v成立，则称条件概率分布P(Y|X)为条件随机场。式中，w～v表示在图G
#       中与结点v有边连接的所有结点w，w≠v 表示结点v以外的所有结点，Y_v，Y_u，Y_w为结点v,u,w对应的随机变量。
#       上述定义的含义，其实是结点v对应的随机变量只与X，以及与其结点有边连接的结点的随机变量有关。
# 在定义中并没有要来X与Y具有相同的结构，现实中，一般假设X和Y有相同的图结构。

# 线性链条件随机场：定义在线性链上的随机场，此时最大团为相邻两个结点的集合。
# 设X=(X1,X2,...,Xn),Y=(Y1,Y2,...,Yn)均为线性链表示的随机变量序列，若在给定随机变量序列X的条件下，随机变量序列Y的条件概率分布
# P(Y|X)构成条件随机场，即满足马尔可夫性：
#                                P(Yi|X,Y1,...,Yi-1,Yi+1,...,Yn) = P(Yi|X,Yi-1,Yi+1) (即当前时刻只与X，以及前后时刻相关)
# 则称P(Y|X)为线性链条件随机场。在标注问题中，X表示输入观测序列，Y表示对应的输出标记序列或状态序列。

# 线性链条件随机场的参数化形式
# 1.转移特征函数：定义在边上的特征函数，它依赖于当前和前一个位置
# 2.状态特征函数：定义在结点上的特征函数，依赖于当前位置
# 3.转移特征函数和状态特征函数都依赖于位置，是局部特征函数
# 4.特征函数的取值：取值为1或0，当满足特征条件时取值为1，否则为0
# 5.线性链条件随机场完全由特征函数和其对应的权值确定
# 6.线性链条件随机场也是对数线性模型
# 7.具体形式：
#   设P(Y|X)为线性链条件随机场，则在随机变量X取值为x的条件下，随机变量Y取值为y的条件概率具有如下形式：
#      P(y|x) = 1/Z(x) * exp{ ∑_{i,k}λ_k * t_k(y_i-1,y_i,x,i) + ∑_{i,l} μ_l * s_l(y_i,x,i)}
#   其中，规范化因子Z(x) = ∑_y exp{ ∑_{i,k}λ_k * t_k(y_i-1,y_i,x,i) + ∑_{i,l} μ_l * s_l(y_i,x,i)}，表示在所有可能的
#   输出序列上求和，确保概率和为1；λ_k ，μ_l分别是转移特征函数t_k和状态特征函数s_l的权重；
#   y,x都是一个序列，y_i,x_i表示序列中的某一个值

# 条件随机场的简化形式
# 1.局部特征函数：由于转移特征函数和状态特征函数都依赖于当前位置，因此是局部特征函数
# 2.全局特征函数：由于同一个特征函数在各个位置都有定义，可以对同一特征函数在各个位置求和，将局部特征函数转化为一个全局特征函数
# 3.利用全局特征函数和各个特征的权值，可以将条件随机场表示为 权值向量 和 特征向量的 内积形式，即条件随机场的简化形式：
#   1. 将转移特征和状态特征及其权值用统一的符号表示，设有K1个转移特征，K2个状态特征，K=K1+K2，记：
#                                               t_k(y_i-1,y_i,x,i)  ,k=1,..,K1
#                         f_k(y_i-1,y_i,x,i) =
#                                               s_l(y_i,x,i)        ,k=K1+l,l=1,2,..,K2
#   2. 对某个转移特征或状态特征在各个位置i求和，记作：
#                         f_k(y,x) = ∑_{i～n} f_k(y_i-1,y_i,x,i)，y,x，表示序列，y_i,x_i表示序列中的某一个值
#   3. 用w_k表示特征f_k(y,x)的权值，即
#                                   λ_k  ,k = 1,..,K1
#                         w_k =
#                                   μ_l  ,k=K1+l;l=1,2,..,K2
#   4. 线性链条件随机场可表示为
#                         P(y|x) = 1/Z(x) * exp{ ∑_{1,..,K}w_k * f_k(y,x)}
#                         Z(x) = ∑_y exp{ ∑_{1,..,K}w_k * f_k(y,x) }
#   5. 若以w表示权值向量，即 w = (w1,w2,...,wK)^T
#      以F(y,x)表示全局特征向量，即 F(y,x) = (f1(y,x),f2(y,x),...,fK(y,x))^T
#      则条件随机场写成向量w和F(y,x)的内积形式为：
#                         P_w(y|x) = exp( w * F(y,x)) / Z_w(x)
#                         Z_w(x) = ∑_y exp( w * F(y,x))

# 条件随机场的矩阵形式
# 假设P_w(y|x)是线性链条件随机场，表示对给定观测序列x，相应的标记序列y的条件概率。对每个标记序列引进特殊的起点和终点状态标记
# y_o = start 和 y_n+1 = stop，这时标注序列的概率P_w(y|x)可以通过矩阵形式表示并有效计算。对观测序列x的每一个位置i=1,..,n+1
# 由于y_i-1和y_i在m个标记中取值，可以定义一个m阶矩阵随机变量：
#                         M_i(x) = [ M_i(y_i-1,y_i|x) ]
# 矩阵随机变量的元素为：
#                         M_i(y_i-1,y_i|x) = exp { W_i(y_i-1,y_i|x)}
#                         W_i(y_i-1,y_i|x) = ∑_{1～K} w_k * f_k(y_i-1,y_i,x,i) (表示某个位置所有特征函数与其权值乘积的和)
# y_i-1,y_i是标记随机变量Y_i-1,Y_i的取值
# 给定观测序列x，相应标记序列y的非规范概率(即没有除Z(x))可以通过该序列n+1个矩阵的适当元素的乘积∏_{1～n+1}M_i(y_i-1,y_i|x)表示，
# 于是，条件概率P_w(y|x)：
#                         P_w(y|x) = 1/Z_w(x) * ∏_{1～n+1}M_i(y_i-1,y_i|x)
# Z_w(x)为规范化因子，是n+1个矩阵的乘积的(start,stop)元素
#                         Z_w(x) = [ M_1(x)M_2(x)...M_n+1(x) ]_start,stop
# 注意,y_o = start 与 y_n+1 = stop 表示开始状态与终止状态，规范化因子Z_w(x) 是以start为起点，stop为终点通过状态的所有路径
# y1y2...yn 的非规范化概率∏_{1～n+1}M_i(y_i-1,y_i|x)之和

# 条件随机场的概率计算问题：
# 1. 概念：给定条件随机场P(Y|X)，输入序列x和输出序列y，计算条件概率P(Y_i = y_i|x),P(Y_i-1=y_i-1,Y_i=y_i|x)以及相应的数学期望的问题。
# 2. 前向算法：
#    对每个指标i=0,1,...,n+1，定义前向向量alpha_i(x):
#                                              1 ,y = start
#                             alpha_o(y|x) =
#                                              0 ,否则
#    递推公式为：
#                             (alpha_i(y_i|x))^T = (alpha_i-1(y_i-1|x))^T * [M_i(y_i-1,y_i|x)] ,i=1,..,n+1
#    又可表示为：
#                             (alpha_i(x))^T = (alpha_i(x))^T * M_i(x) ,(alpha_i(x))^T是一个行向量
#    alpha_i(x)表示在位置i的标记是 y_i 并且从1到i的前部分标记序列的非规范化概率，y_i可取的值有m个，所以alpha_i(x)是m维列向量
# 3. 后向算法
#    对每个指标i=0,1,...,n+1，定义后向向量beta_i(x):
#                                                  1 ，y_n+1 = stop
#                             beta_n+1(y_n+1|x) =
#                                                  0 ,否则
#    递推公式为：
#                             beta_i(y_i|x) = [ M_i+1(y_i,y_i+1|x) ] * beta_i+1(y_i+1|x)
#    又可表示为：
#                             beta_i(x) = M_i+1(x) * beta_i+1(x)
#    beta_i(y_i|x)表示在位置i的标记为y_i并且从i+1到n的后部分标记序列的非规范化概率，是一个m维的列向量
# 4. 概率计算
#    1. 标记序列在位置i是标记y_i的条件概率：
#                              P(Y_i=y_i|x) = (alpha_i(y_i|x))^T * beta_i(y_i|x)/ Z(x)
#    2. 标记序列在位置i-1和i是标记y_i-1和y_i的条件概率：
#                              P(Y_i-1=y_i-1,Y_i=y_i|x) = (alpha_i-1(y_i-1|x))^T * M_i(y_i-1,y_i|x) * beta_i(y_i|x)/Z(x)
#       Z(x) = (alpha_n(x))^T * 1 = 1 * beta_1(x) ，其中 1 是元素均为1的m维列向量，m表示标记的种类数，或隐状态的种类数

# 期望值的计算
# 利用前向-后向向量，可以计算特征函数关于联合分布P(X,Y)和条件分布P(Y|X)的数学期望，用于IIS算法
# 1. 特征函数f_k关于条件分布P(Y|X)的数学期望
#    E_P(Y|X)[f_k] = ∑_y P(y|x) * f_k(y,x)
#      = ∑_{i=1～n+1}∑_{y_i-1,y_i} f_k(y_i-1,y_i,x,i) * (alpha_i-1(y_i-1|x))^T * M_i(y_i-1,y_i|x) * beta_i(y_i|x)/Z(x)
# 2. 假设经验分布为P'(X)，特征函数f_k关于联合分布P(X,Y)的数学期望
#    E_P(X,Y)[f_k] = ∑_{x,y}P(x,y)∑_{i=1～n+1}f_k(y_i-1,y_i,x,i)
#   = ∑_x P'(x)∑_y P(y|x)∑_{i=1～n+1}f_k(y_i-1,y_i,x,i)
#   = ∑_x P'(x)∑_{i=1～n+1}∑_{y_i-1,y_i}f_k(y_i-1,y_i,x,i)*(alpha_i-1(y_i-1|x))^T * M_i(y_i-1,y_i|x) * beta_i(y_i|x)/Z(x)
# 3. 对于给定的观测序列x与标记序列y，可以通过一次前向扫描计算alpha_i及Z(x)，通过一次后向扫描计算beta_i，从而计算所有的概率
#    和特征的期望。

# 条件随机场的学习算法：
# 1. 极大似然估计法
# 2. 正则化的极大似然估计法

# 条件随机场的学习算法的优化实现：
# 1. 梯度下降法
# 2. 拟牛顿法
# 3. 改进的迭代尺度算法IIS：S算法 + T算法
#    改进的迭代尺度算法通过迭代的方法不断优化对数似然函数改变量的下界，达到极大化对数似然函数的目的，待求的参数就是各个特征函数的
#    权重。

# 条件随机场的预测算法：维特比算法
# 条件随机场的预测问题是给定条件随机场P(Y|X)和输入序列(观测序列)x，求条件概率最大的输出序列(标记序列)y，即对观测序列进行标注。

# 线性链条件随机场用于序列标注
# 线性链条件随机场可以用于标注等问题。这时，在条件概率模型P(Y|X)中，Y是输出变量，表示标记序列，X是输入变量，表示需要标注的观测序列
# 也把标记序列称为状态序列。学习时，利用训练数据集通过极大似然估计或正则化的极大似然估计得到条件概率模型P(Y|X)；预测时，对于
# 给定的输入序列x，求出条件概率P(y|x)最大的输出序列y。
#=======================================================================================================================