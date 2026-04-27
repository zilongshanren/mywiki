---
tags: [rendering, culling, visibility, portal, occlusion-culling]
date: 2026-04-27
sources: 1
---

# Portal/Cell 可见性与谓词化渲染

Portal/Cell 系统是实时渲染中针对高度遮挡场景（室内建筑、走廊、地牢）效率最高的可见性方案之一。其核心思想是将场景划分为若干**单元（Cell）**，单元之间通过**传送门（Portal）**相连；渲染时从摄像机所在单元出发，递归测试每个传送门是否可见，若可见则将视锥裁剪至该传送门范围，再继续测试下一个单元的内容。

## 历史脉络

Portal 技术的起点可以追溯到 Quake：BSP 把世界划分成凸区域（Cell），Portal 是区域之间的"边界"，编译期预计算的 PVS（Potentially Visible Set）记录了哪些单元两两可见。运行时，软件渲染用 BSP 做前后排序并以 span buffer 避免 overdraw；一旦有 GPU（GLQuake），z-buffer 直接接管。

Doom 3 进一步把这套流程推到**运行时**：从摄像机当前 Cell 出发，对每个 Portal 与视锥做相交测试，若可见则以 Portal 平面裁剪视锥，递归进入邻接 Cell。这是大多数人今天所理解的"Portal 剔除"。

Source 引擎的 Hammer 编辑器使 Portal 工作流广为人知：美术手动在地图中标记 Portal 刷子，编译器处理 CSG 布尔运算后生成 Cell 结构。

## Portal 即谓词化渲染

[[angelo-pesce]] 提出了一个更本质的解读：**Portal 是谓词化渲染（Predicated Rendering）的一种形式**——"如果该 Portal 可见，则渲染与之关联的那批几何体"。这个解读把 Portal 从特定关卡编辑工作流中解放出来：

- Portal 不必严格对应几何开口，可以比实际开口更大（保守估计），只影响剔除效率，不影响正确性。
- Cell 的定义也可以放宽：任何"一组应当被同一可见性条件控制的对象集合"就是一个 Cell，不需要它是凸区域或封闭体积。
- Portal 可以运动：例如汽车车窗就是一个 Portal，若所有车窗均不可见，车内所有几何体都不需要渲染。

这一抽象使 Portal 系统非常适合 GPU 驱动的实现——只需将 Portal 栅格化进遮挡缓冲区，即可用硬件测试其可见性，随后把相关 Cell 的对象加入渲染队列。

## Antiportal 与遮挡体

传统 Portal 系统描述的是**"如果入口可见，里面的东西才可见"**（Disocclusion 测试），但当场景较为开阔时，此逻辑效率低下。为此，许多引擎引入了 **Antiportal**：标记大型遮挡物，把它们从摄像机处投影成视锥，剔除被完全遮挡的对象。

Antiportal 与 Portal 是对偶概念：

| | Portal | Antiportal |
|---|---|---|
| 测试方向 | Disocclusion（入口可见→内容可见） | Occlusion（遮挡物覆盖→内容不可见） |
| 保守方向 | Portal 应**包围**真实开口 | Occluder 应**内切**真实遮挡几何 |
| 融合性 | 易于递归融合 | 多个 Antiportal 融合需要 beam tree，代价高 |

软件光栅化遮挡剔除（参见 [[occlusion-culling]]）的兴起部分原因正是 Antiportal 融合困难：光栅化天然处理多个遮挡体的合并遮挡关系。而在光栅化遮挡系统中，Portal 测试极为廉价——先光栅化 Portal 多边形测试是否可见，若可见再光栅化其 Cell 的遮挡体，并将该 Cell 的内容列入候选渲染列表，递归继续。

## 与现代引擎的关联

Portal/Cell 系统在开放世界游戏流行后逐渐被视为"室内专用技术"，实则可以普遍化：建筑物外壳本身就是 Portal（若建筑完全不可见，内部什么都不用渲染），[[gpu-based-occlusion-culling]] 与 Portal 思想可以同时存在于一套系统中。关键在于工具链支持——让美术可以便捷地标记 Portal 和 Cell，而不依赖特定的 BSP 关卡编辑器。

## Sources

- [[sources/c0de517e-portals-predicated-rendering]]
