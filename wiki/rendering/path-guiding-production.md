---
tags: [渲染, 路径追踪, 重要性采样, 体积, openpgl, hyperion]
date: 2026-04-19
sources: 2
---

# 生产级 Path Guiding

**Path guiding** 用训练出的代理分布替代 BSDF 或相函数单独做下一步采样，目标是沿着真正把能量送回相机的方向多打样本。学术上自 PPG（Müller et al. 2017 *Practical Path Guiding*）后有一波发展；但把它真正铺进影片管线，要解决的问题和论文里不太一样。Yining Karl Li 等在 SIGGRAPH 2025 course *Path Guiding in Production and Recent Advancements* 的 Disney 章节（36 页）写了这段经验。

## 一代：从 PPG 到有限部署

- Hyperion 是最早实现 PPG 的生产渲染器之一（Müller 2019 course notes）。
- 从 *Frozen 2* 起上过有限的镜头，但因为几个原因一直没大规模铺开：只支持表面、工具链对艺术家不透明、默认 path tracing 上开关收益不稳定。

## 二代：Hyperion × OpenPGL × DisneyResearch|Studios

基于 Wayne Huang 的研究提案启动，Disney Research Studios（ETH Zürich 学术合作）、Disney Animation、Pixar、ILM 加 Intel 的 Sebastian Herholz 一起做。

目标是：

- **联合指导表面 + 体积**：Moana 2 风暴、Zootopia 2 的复杂体积几乎每个镜头都有体积，光一代的「只表面 PPG」远远不够。
- **Volume scattering probability guiding**（Xu et al. 2024）：体积里历史上缺的最后一块——对散射概率本身做指导，而不止散射方向。
- **Spatio-directional mixture models**（Dodik et al. 2022）：改进 PPG 对任意朝向 BSDF 的学习与 product sampling。
- **Neural path guiding**（Rath et al. 2025）：把 GPU 上的神经 path guiding 塞进 CPU wavefront 渲染器。

底座是 Intel 的 [OpenPGL](https://github.com/RenderKit/openpgl) 开源库。

## 工程挑战

- **Wavefront 不存路径历史**：在 [[wavefront-path-tracing]] 里，当前 bounce 之前的路径状态不保留，而 path guiding 需要全路径学习——需要专门的架构设计绕开。
- **与非物理特性共存**：生产渲染器为艺术指导保留了很多「违反物理」的开关（光组、可见性分离、lightpath 修改）。path guiding 的训练分布必须正确感知这些「开关」，否则学到的分布在最终 shot 上就是错的。
- **可视化与调试**：team 为验证正确性与理解产线行为写了大量 guiding 分布可视化工具，这在学术论文里不会讲。

## 产线首次广泛部署：Zootopia 2

- *Moana 2* 做了二代 path guiding 的原型，但没大规模上线。
- *Zootopia 2* 成为首部大规模铺开的片子——约 12% 镜头在 Hyperion 里用二代 path guiding 渲染，多个本来被视作「极难收敛」的镜头因此顺利过关。

## 相关

- [[hyperion-renderer]]
- [[wavefront-path-tracing]]
- [[yining-karl-li]]

## Sources

- [[sources/yiningkarlli-path-guiding-siggraph2025]]
- [[sources/yiningkarlli-zootopia-2]]
