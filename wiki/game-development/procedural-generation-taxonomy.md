---
tags: [procedural-generation, overview, taxonomy, game-development]
date: 2026-04-27
sources: 1
---

# 程序化生成分类概述

程序化生成（Procedural Generation，PCG）是利用计算机算法自动产生创意内容的技术总称，涵盖游戏关卡、美术资产、音乐、叙事等多个领域。从技术机制来看，可以归为四个大类。

## 四大技术类别

**算法型（Algorithmic）**：以经典编程思路实现，给定一组确定性指令，计算机按步骤执行。典型代表是 Prim 算法生成迷宫、BSP 树分割房间。优势是结果可预期、可调试；缺点是难以产生"意外的惊喜"。

**函数型（Functional）**：指定数学公式，对坐标或参数求值即得结果。最具代表性的是 Perlin 噪声——输入坐标，输出连续的伪随机值，广泛用于地形高度图、云层纹理等。[[rendering/classic-shader-noise|噪声函数]]在渲染和 PCG 领域均有重要地位。函数型方法高度并行、易于 GPU 加速，但表达力受限于函数形状。

**模拟型（Simulation）**：设定初始状态与演化规则，让系统自行运转。物理模拟是最广为人知的形式；元胞自动机生成洞穴、侵蚀算法雕刻地形、群体动力学驱动 NPC 行为，都属此类。[[game-development/graph-rewriting-proc-gen|图改写]]中的 Cellular 迭代模式本质上也是一种模拟。

**生成式 AI（Generative AI）**：2020 年代兴起的新范式，以深度学习模型直接生成内容。控制性、确定性、版权归属等问题仍处于探索阶段，与传统 PCG 技术的边界和互补方式也在持续重新定义中。

## 应用场景的主要群体

PCG 技术的使用者分布在多个行业，各有侧重：

- **游戏开发者**：Roguelike/roguelite 游戏依赖 PCG 驱动重玩性；AAA 游戏借助 PCG 管理海量内容（如 Houdini 生成地形和植被）。技术美术（Technical Artist）是连接美术创作与生成算法的桥梁。
- **艺术家**：demoscene 场景、生成艺术（Generative Art）、NFT、互动装置展览。
- **影视 VFX**：物理模拟填充场景细节，程序化动画辅助群体运动。
- **学术研究者**：PCG 横跨计算机图形学、AI 与创意计算，有专属会议（如 Everything Procedural）。

## 与相关概念的关系

Boris 的博客系列覆盖了 PCG 的多个细分方向：[[game-development/wave-function-collapse|WFC]] 和[[game-development/constraint-based-tile-generators|约束瓦片生成]]属于算法型/约束型；[[game-development/dungeon-generation-algorithm|地牢生成]]常综合多种方法；[[game-development/graph-rewriting-proc-gen|图改写]]提供了宏观结构的生成语言；噪声函数、侵蚀等属于函数型和模拟型的典型。

## Sources

- [[sources/boris-what-is-proc-gen]]
