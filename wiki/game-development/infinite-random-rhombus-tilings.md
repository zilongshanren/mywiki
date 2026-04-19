---
tags: [程序化生成, 铺砖, 无限网格, townscaper, sylves]
date: 2026-04-19
sources: 1
---

# 无限随机菱形铺砖

Townscaper 的招牌「有机六边形 + 菱形」网格让很多人想抄，但原算法有两个结构性毛病：(1) 随机配对三角形时偶尔落单，被迫做一次全局细分修补；(2) 每个六边形 chunk 的边界是**锁死**的——总是 8 条边，不管随机种子怎么变，chunk 边缘那条菱形链条都固定。[[boris-the-brave]] 在 Sylves 里给出一个替代方案：把 [[infinite-chunked-procedural-generation|相位化 chunk 算法]] 套在「菱形翻转」这个局部不变操作上，得到一个**无限、无全局细分、chunk 边界不可见**的随机铺砖。

## 三菱汇合点的翻转不变性

底层操作出奇地简单：平面上每 3 个菱形相交于一点时，可以把它们**原地旋转**——换一种摆法，周围所有其他菱形不受影响。如果一开始就摆好一整张正规菱形网（经典 3 方向等价图），那么对每个这样的三菱点独立投骰子翻或不翻，就是 Kenyon 风格的 **rhombus tiling 的 MCMC 洗牌**：翻得够多次，分布趋近一致随机铺砖。

在有限区域里，这个洗牌本身好做；问题在于要把它推到无限平面。

## 为什么直接分 chunk 洗不行

朴素做法：把无限平面切格子，每格独立洗牌。立刻踩坑——chunk 边界上的三菱点**跨越边界**，要么被两边同时洗导致冲突，要么永远不翻导致边缘可见。结果是每个 chunk 都带一条规整的边界。

## 三轮不同切法的无限覆盖

Boris 用了他在 [2021 年 Infinite Modifying In Blocks](https://www.boristhebrave.com/2021/11/08/infinite-modifying-in-blocks/) 里立过的套路，用**错位的三套 chunking** 依次洗：

- 第一轮：按切法 A 分块，每块独立洗
- 第二轮：按切法 B 分块（边界错开），独立洗
- 第三轮：按切法 C 分块（再次错开），独立洗

只要三套切法的并集覆盖整个平面，任一位置都至少被一轮「内部」翻过，不留整齐边界。关键性质：**给定 cell 的最终状态只依赖于有限多个邻近 chunk 的 seed**，因此整个过程仍是 `f(coord) -> tile` 的纯函数——lazy 求值、确定性、chunk 无关，和 [[infinite-chunked-procedural-generation]] 的方法论一脉相承。

Boris 提供了 [Sylves 实现](https://github.com/BorisTheBrave/sylves/blob/main/src/Sylves/Grid/Extras/RandomRhombusGrid.cs)；染色图里可以看到 hex chunk 边界被完全冲散——再也不是 Townscaper 那种「每边恰 8 tile」的标尺了。

## 对比 Townscaper

| 问题 | Townscaper | 无限随机菱形 |
|---|---|---|
| 未配对三角形 | 全局细分消除 | 根本没有三角形：起点就是整齐菱形网 |
| chunk 边界痕迹 | relaxation 后仍可见 | 三轮错位 chunking 覆盖，不可见 |
| 无限性 | 边界规则特殊处理 | 纯函数 `f(coord)`，无边界 |
| 可否关闭细分 | 不能（否则有三角形） | 天然就无三角形，分辨率可选 |

代价是失去 Townscaper 那种以六边形为主的自然聚集感——不同算法给出不同的「有机味道」。

## 可迁移性

同一翻转不变 + 三轮错位 chunk 的框架套在别的对偶操作上也能用。Boris 顺手演示了**随机矩形（herringbone 变体）**：两个并排矩形可以 90° 互换，同样是局部不变的对偶操作，同一套 chunk 洗法直接复用。这个模板等价于「找一个局部可逆的 tiling rewrite，用 phase 洗法无限化」，和 WFC 求解器无限化是同类问题的不同角落。

## 相关

- [[infinite-chunked-procedural-generation]] —— 同一个相位化 chunk 方法论的另一个实例
- [[poisson-rect-process]] —— 同系列无限程序化生成
- [[boris-the-brave]]

## Sources

- [[sources/boristhebrave-rhombus-tilings]]
