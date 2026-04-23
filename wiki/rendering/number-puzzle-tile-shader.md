---
tags: [渲染, shader, 纹理, 去重复]
date: 2026-04-19
sources: 1
---

# Number Puzzle 瓦片随机化 shader

[[ben-supnik]] 2010 年在 X-Plane 场景渲染里玩的一种 shader 级纹理去重复技巧：把一张重复纹理划分为若干子瓦片（sub-tile），shader 里**根据位置随机置换瓦片**，把规则的 tiling 变成视觉上不规则的拼贴——就像把数字华容道打乱。

## 基本机制

输入是一张被划分成 N×N 小格的纹理（就是游戏里的「数字华容道」格局）。shader 做法：

1. 把 UV 坐标拆成「瓦片选择位」（高位 bits）和「瓦片内部 UV」（低位 bits）。
2. 用高位作为索引去一张噪声图里采样，得到一个随机瓦片编号。
3. 按随机编号重组 UV：高位=随机瓦片，低位=原本瓦片内部坐标。
4. 用新 UV 采样基础纹理。

结果：同一张小纹理平铺，但每个瓦片看起来都用了不同的内容——大面积重复感消失，GPU 开销几乎零（一次噪声采样 + 位运算）。

**一个隐性优点**：关闭 shader（走 fixed function）时，UV 不被改写，你得到的是原本的重复 tiling，视觉丑但**仍然是合法输出**。不需要为 fixed function 路径做分支，特性可以优雅降级。

## 和 atlas 的结合

Supnik 在这篇博客里当场想到的扩展：把「随机瓦片的选择范围」约束到 UV 某段上位区间，**从一张更大的 atlas 内挑瓦片**——原来一张图只能提供 N×N 种排列，atlas 里可以放多组瓦片集，一次 batch 绘制多种地表。

代价是：atlas + 随机 tiling 与 fixed function pipeline 的 [[sampler-filter-wrap-modes|UV wrap 模式]] 根本性不兼容。wrap 要求采样超出 [0,1] 时自动 mod 回来，而 atlas 要求采样不能越过子图边界。shader on 路径可以靠代码手工 mod，shader off 路径只有 hardware wrap 可用——退化后你得到花屏，不再是「丑但合法」。

这是 2010 年 Supnik 明确说「可能是 deal-breaker，只要 fixed function 还是必须的」的地方。

## 与相关技术的位置

这个技巧和 [[stochastic-texture-sampling]]（Heitz 那套把 gaussian 样本加权混合消除 tiling 的方法）是**同类问题的不同解**：

- number puzzle 用的是**离散重组**：瓦片整块整块挪位置，接缝处可能被察觉，但成本最低、和 mipmap 兼容。
- stochastic sampling 用的是**连续混合**：多次采样加权平均，数学上严格去相关，但每像素 3-5 次采样、且要存 histogram 预处理。

Number puzzle 更适合 X-Plane 这种**需要在老硬件上跑、且有自然离散感的地表**（农田、街区）；stochastic 更适合沙、草、石这类应**完全无缝**的 micro-detail。

## 为什么 Supnik 还要讨论 fixed function

文章第二半是「2010 年还要支持 fixed function 吗」的工程权衡。他的回答不是硬件占比（虽然他追踪 Steam hardware survey），而是**客户支持价值**：能让用户一键关掉 advanced path，是「等一个月新驱动 vs 退货」的分水岭。这条逻辑在 X-Plane 这种长寿命模拟软件里格外重。今天的类比是各引擎的 `--safe-mode` / compatibility renderer。

## 相关

- [[stochastic-texture-sampling]]
- [[sampler-filter-wrap-modes]]
- [[texture-swizzle-nested-tiling]]

## Sources

- [[sources/supnik-tile-too-far]]
