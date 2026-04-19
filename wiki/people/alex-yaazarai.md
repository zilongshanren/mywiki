---
tags: [人物, 作者, shader, 渲染, 全局光照, gamemaker]
date: 2026-04-19
sources: 2
---

# Alex（Yaazarai）

**Yaazarai**（真名 Alex）是 GameMaker 社区的 shader 开发者，以在 GM 上移植和教学**最新的 2D 全局光照算法**著称。在 GM Shaders 的客座系列里写过 **Radiance Cascades 两部分教程**（2024-04 Part 1 几何直觉、2024-07 Part 2 优化与代码深剖），是中文世界可查到的最早一批把 Alexander Sannikov 的论文翻译成可跑代码的人之一。

## 代表作

- **Radiance Cascades Part 1**（2024-04）：介绍 [[penumbra-hypothesis|半影假设]]、cascade 层级结构、merge 几何——以可视化 demo 为主，代码只给了示意。见 [[sources/yaazarai-radiance-cascades]]。
- **Radiance Cascades Part 2**（2024-07）：重写了 Part 1 的实现，引入 **pre-averaging**（75% 内存节省）和 **direction-first 内存布局**（硬件双线性插值把 merge 降到 1 次采样）。这是 GitHub 上流传最广的 GM 版 RC 实现之一。见 [[sources/yaazarai-radiance-cascades-2]]。

他之前还写过一篇基于随机射线采样的**naive radiosity GI** 教程（Part 1 的前作，本批次未覆盖），是对比 RC 的基准。

## 风格

- **重可视化**：每一个算法步骤都配动图/demo，把抽象的级联几何变成可交互的东西。
- **坦诚承认错误**：Part 2 开篇直接列出 Part 1 实现的四类问题（过于复杂、不支持非方形分辨率、性能差、内存浪费），给出修复。2024-07 的 update note 里又纠正了"direction-first 更快"的说法——事实是 GM 当时一个 bug 让表面上变慢的那组数据反向了。这种"覆水收回"的礼仪在开源教程里少见。
- **社区嵌入**：实现依赖 Graphics Programming Discord 的 RC 社区，借鉴 Mytino、Fad 等人的工作。

## 相关

- [[radiance-cascades]]
- [[penumbra-hypothesis]]
- [[alexander-sannikov]] —— RC 算法发明者
- [[xor-shader-artist]] —— GM Shaders 博主
- [[jump-flooding-algorithm]] —— 2D RC 需要 SDF 作为 raymarch 加速结构

## Sources

- [[sources/yaazarai-radiance-cascades]]
- [[sources/yaazarai-radiance-cascades-2]]
