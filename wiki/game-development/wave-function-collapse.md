---
tags: [procedural-generation, wfc, constraint-solving, tileset, game-development]
date: 2026-04-27
sources: 11
---

# Wave Function Collapse（WFC）

Wave Function Collapse 是 Maxim Gumin 于 2016 年发布的一种程序化生成算法，其本质是**约束编程（Constraint Programming）在瓦片生成场景下的特化应用**。名字借用量子力学术语，但与量子物理无关。

## 核心机制

WFC 将地图生成问题建模为约束满足问题（CSP）：网格的每个格子是一个**变量**，该格子可放置的瓦片集合是**域**，相邻格子之间的可连接规则是**约束**。求解流程分两步循环：

1. **约束传播**：当某格子的域缩减，沿约束边向邻居传播，消除不再合法的候选。用支持计数（support count）高效维护：某方向某瓦片的计数降为 0 时立即从域中删除。
2. **随机猜测（Observation）**：当传播无法进一步压缩域时，用**最小熵启发（Least Entropy）**选一个候选最少的格子，再按权重随机选一个瓦片"坍缩"该格子，然后继续传播。出现矛盾则回溯。

与传统 CSP 求解器不同，WFC 的目标是在海量合法解中随机采样，而非找唯一解，因此保留随机猜测正是其生成器身份的关键。

## 两种变体

**Adjacent WFC**（邻接模式）：约束只关心相邻两格之间的瓦片兼容性，美术师直接配置哪两种瓦片可以相邻。直觉明确，速度快，但无法捕捉距离大于 1 格的相关性。

**Overlapped WFC**（重叠模式）：约束是"输出中每个 NxN 窗口必须在样本图中出现过"。约束更强，能复现样本的中距离结构和纹理细节，但计算更慢，且容易过度拟合样本。

## 实践弱点与补救

WFC 本质上是**局部约束**求解器，不能保证大尺度结构。生成大型关卡时常出现孤立区域、单调重复等问题，典型补救手段有：

- **路径约束**（Path Constraint）：全局强制一组瓦片构成连通图，Boris 的 DeBroglie 库首先实现了这一扩展。
- **固定瓦片**（Fixed Tiles）：预先锁定入口/出口或手工内容片段。
- **分区运行**：将地图划分为 Biome 子区域，每个子区域用不同的瓦片集或样本跑独立的 WFC（Caves of Qud 方案）。
- **瓦片集设计**：用 [[autotile-tileset-layouts]] 中的 Marching Cubes 思路设计瓦片，让"接不上"的情况从物理上消失，大幅减少回溯。
- **分块修改（[[modifying-in-blocks]]）**：将生成区域划分为互相重叠的小块，每块独立求解，矛盾时只重启该块。配合分层依赖树可实现无限大地图的确定性惰性生成。

## Editable WFC

将 WFC 用作交互式地图编辑工具的变体。用户单击放置一块瓦片，算法以**脏格启发式**只重解受影响的最小区域，并用**相似度权重**优先保留现有地图内容。Townscaper 用确定性选择+隐藏驱动层实现了类似效果，Boris 的方案则更通用，直接在瓦片层编辑。

## Sources

- [[sources/boris-wfc-explained]]
- [[sources/boris-wfc-tips]]
- [[sources/boris-editable-wfc]]
- [[sources/boris-driven-wfc]]
- [[sources/boris-arc-consistency]]
- [[sources/boris-tessera-practical-system]]
- [[sources/boris-constraint-based-tile-generators]]
- [[sources/boris-quantum-wfc]]
- [[sources/boris-model-synthesis-modifying-blocks]]
- [[sources/boris-infinite-modifying-blocks]]
