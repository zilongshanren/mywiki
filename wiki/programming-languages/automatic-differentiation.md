---
tags: [微分, 优化, 机器学习, 可微编程, 编译器]
date: 2026-04-14
sources: 1
---

# 自动微分：可微编程的底座

PyTorch、TensorFlow、JAX、可微渲染、可微物理——背后都是同一个算法：**自动微分**（autodiff）。它和数值微分（finite differences）、符号微分（Mathematica 那种代数变换）都不一样，**既不近似，也不会让表达式爆炸**。Max Slater 在 2022 年的长文里从导数的「向量到向量的高阶函数」视角出发，依次拆解了四种微分技术、两种 autodiff 模式、以及现代框架（JAX）的「把梯度看作图变换」的统一观点。

## 把导数看成「向量映射」

教科书定义 $f^\prime(x) = \lim_{h\to 0}\frac{f(x+h) - f(x)}{h}$，但更有用的几何视角是：**导数是一个把「输入处的向量」映射到「输出处的向量」的线性算子**。

- 1D → 1D：$f^\prime(x)$ 是一个标量，把 $\Delta x$ 缩放成 $\Delta y$。
- $\mathbb{R}^n \to \mathbb{R}$：梯度 $\nabla g$ 是一个 **行向量**，与 $\Delta\mathbf{x}$ 做点积得到 $\Delta g$。这正是「最陡上升方向」名字的由来——使方向导数最大化的 $\mathbf{v}$ 就是 $\nabla g$ 自身。
- $\mathbb{R}^n \to \mathbb{R}^m$：Jacobian $\mathbf{J}_h$ 是 $m \times n$ 矩阵。
- **链式法则就是矩阵乘法.** $h = g \circ f$，则 $\mathbf{J}_h = \mathbf{J}_g \cdot \mathbf{J}_f$。这一观察是后面所有 autodiff 的核心：链式法则是合成线性算子。

## 三种「对程序求导」的方法

**(1) 数值微分.** 直接套定义：$\frac{f(x+h) - f(x)}{h}$，挑个小 $h$。优点：不需要碰函数体。缺点：每个方向都要单独跑一次 $f$，高维下每个梯度分量都得跑——$n$ 维输入要 $n$ 次评估。还有舍入误差，永远是近似。

**(2) 符号微分.** 把 $f$ 写在一个 DSL 里，每个语法节点配一条求导规则：

```
d(Times(a, b)) → Add(Times(d(a), b), Times(a, d(b)))
```

这就是 Mathematica。麻烦在于 `Times` 求导后表达式 **至少翻倍**，每嵌套一次 `Times` 就再翻一倍——$f^\prime$ 的大小是 $f$ 的指数。Slater 给出了形式归纳证明。所以符号微分对深网络这种东西完全不可行。

**(3) Autodiff.** 既精确又不爆炸，是现代差分编程的真正算法。它有两种实现风格：forward mode 和 backward mode。

## Forward mode：dual number

定义新数 $a + b\epsilon$，约定 $\epsilon^2 = 0$。乘法、加法自然推广，结果总是「实部 + dual 系数」：

$$
(x + x'\epsilon)(y + y'\epsilon) = xy + (xy' + x'y)\epsilon
$$

dual 系数恰好就是乘积的导数。对任何光滑 $f$，都可以用 Maclaurin 级数证明：

$$
f(x + x'\epsilon) = f(x) + f'(x)\,x'\epsilon
$$

所以实现非常便宜：把 `Float` 替换为 `(value, dual)` 二元组，重载所有算术操作，运行原函数即可——dual 部分就是 $f^\prime(x)$ 沿你输入的那个方向 $x'$ 的方向导数。

```js
function Const(n) { return [n, 0]; }
function Add(x, y) { return [x[0]+y[0], x[1]+y[1]]; }
function Times(x, y) { return [x[0]*y[0], x[1]*y[0] + x[0]*y[1]]; }
// 求 f'(x): 调 f([x, 1])，dual 部分就是 f'(x)
```

**局限**：每次评估只算 **一列** Jacobian——一个方向的方向导数。如果输入是 $n$ 维，要跑 $n$ 次。所以 forward mode 适合 **少输入、多输出** 的函数。

## Backward mode：反向传播

机器学习里通常是反过来：**几百万个输入，一个标量损失输出**。这种情况要的是 Jacobian 的 **一行**——backward mode 只跑一次正向 + 一次反向就给出整个 $\nabla f$。

实现思路：评估 $f$ 时不仅算结果，还把每个操作记录成图节点，构成一张 **DAG**——通常叫 tape 或 computational graph。这一步是 **forward pass**，记录每个节点的 **primal**（数值）。

然后 **backward pass**：从输出节点起步，初始化 $\frac{\partial f}{\partial \text{out}} = 1$，按 **逆拓扑序** 遍历。每个节点把自己的 grad 按操作的局部偏导推回输入边。比如加法节点 $+$ 把 grad 不变地推给两个输入；乘法节点 $\times$ 要把对方的 primal 乘进 grad（因为 $\frac{\partial(xy)}{\partial x} = y$）。同一个节点可能被多个下游使用——它的 grad 是所有下游推回来的总和。

```js
function backward(out_node) {
  const order = topological_sort(out_node).reverse();
  for (const node of order) {
    if (node.op === 'add') {
      node.in[0].grad += node.grad;
      node.in[1].grad += node.grad;
    } else if (node.op === 'times') {
      node.in[0].grad += node.in[1].out * node.grad;
      node.in[1].grad += node.in[0].out * node.grad;
    }
  }
}
```

**这就是反向传播**——本质是「链式法则 + 动态规划」：每个节点的局部偏导只算一次，被所有路径复用，所以总时间复杂度和正向 $f$ 相同。

**代价**：必须存所有中间值。深网训练时 activation 占的显存往往比模型本身还多。两条优化路径：

- **Checkpointing**：选择性地不存某些节点，反向时按需重算——经典时间换空间。
- **图分割 + 多机**：把 DAG 切到多机上，最小化 cut edge 上的通信成本。

## 第三种视角：把梯度看作图变换

PyTorch / TensorFlow 把图当作「forward 算 primal、backward 算 dual」的临时数据结构。但 **也可以把 $\nabla f$ 自身建成另一张图**——只要在 $f$ 的图上对每个原始节点添加 $O(1)$ 个 grad 节点。结果：

- $\nabla f$ 的图大小是 $f$ 的常数倍，**评估它的运算量等于 forward+backward**。
- 因为 $\nabla f$ 也是图，可以再对它做图变换得到 $\nabla(\nabla f)$ ——**高阶导数自然支持**。
- 单一图统一了 forward 和 backward，反向 pass 不再是单独算法，**更容易并行化、JIT 编译、跨机分布**。

JAX 就是这条路线（`grad` 是一个把函数变换为另一个函数的高阶变换），functorch 给 PyTorch 移植了类似的 API。

## 应用：图像反模糊

Slater 用自己写的 30 行 autodiff 框架解了一个真问题——**给定 3×3 box-blur 后的观察图像，恢复原图**。把「猜测图像」当作可微参数，定义损失为「猜测图像 blur 后与观察图像的逐像素平方差」，对猜测图像跑梯度下降。每一步：

1. 重置图。
2. forward(loss) 算当前猜测的 blur 与 loss。
3. loss.grad = 1，backward(loss) 把 grad 推到每个像素参数。
4. 像素参数沿负梯度走一小步。

迭代几百轮，猜测图像收敛到接近原图（box blur 是欠定的，所以无法精确恢复，但在感知上几乎一致）。整个过程没用任何 ML 框架——**是最纯粹的「用 autodiff 解优化问题」**。

## 相关

- [[functions-as-vectors]] — 把函数视为无限维向量，是 autodiff 的「无限维 Jacobian」自然起点
- [[higher-order-functions]] — 「梯度是高阶函数」的视角是理解链式法则的关键
- [[probabilistic-algorithms]] — 同样属于「数学结构推动算法」的程序设计范式
- [[spherical-harmonics]] — Slater 的可微图形系列里 SH 系数也常作可微参数
- [[max-slater]]

## Sources

- [[sources/slater-autodiff]]
