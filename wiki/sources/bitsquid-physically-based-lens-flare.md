---
tags: [source, rendering, lens-flare, optics, stingray, post-processing]
date: 2026-04-19
sources: 1
---

# Physically Based Lens Flare（Jp, Stingray）

Bitsquid / Stingray 博客 2017-07-03，作者 **Jp（Jean-Philippe Guertin）**。把 Hullin 等人 *Physically-Based Real-Time Lens Flare Rendering* (SIGGRAPH 2011) 的论文实现进 Stingray，覆盖 ghost、光圈衍射星芒、AR 镀膜四个子效果。代码开源在 `github.com/greje656/PhysicallyBasedLensFlare`。

## 摘要

Horizon Zero Dawn 里漂亮的 lens flare 让 Jp 决定在 Stingray 里也做一套。他把 lens flare 拆成四类：anamorphic 拉丝、光圈衍射的 starburst、太阳月亮产生的高质量 ghost、以及所有其他光源产生的屏幕空间低质量 ghost。文章集中讲 **高质量 ghost**：输入一个真实镜头的专利处方（如 Nikon 28-75mm 有 27 片镜片），枚举所有 "两次反射" 组合——27 片能生成 `C(27, 2) = 352` 个 ghost——每个 ghost 在 camera 入光口细分一张 patch（352×32×32 条光线），compute shader 逐条 raytrace 到传感器。

关键工程点：(1) 光线未命中透镜时不立即终止，而是"飞到传感器为止"以保持 patch 插值连续性，只在超出透镜整体球壳时才切断；(2) ray bundle 携带固定能量，所以要按 bundle 面积的收缩膨胀调节辐照度——这是 caustic 形成的物理来源；(3) pixel shader 依次 discard：出了透镜系统的、原本在太阳盘外的、被光圈挡住的，剩下的按 `original_area / new_area` 修正强度。光圈用 SDF 程序化生成；starburst 用 Intel 的 FFT compute 实现把光圈图变到 Fourier 域，再按波长缩放 Power Spectrum 累加得到白光衍射。**AR 镀膜** 给每片镜片指定目标波长，按 `n1 = sqrt(n0·n2), d = λ/(4·n1)` 算出理想厚度与折射率，用户还能手动调厚以增强反射。Nikon 28-75mm 全套 12ms（3ms raymarch + 9ms rasterize 352 patches）——成本太高，作者承认大概只适合电影预览，而非实时游戏。

## 关键要点

- **论文里模糊的"transform feedback 算邻居四边形"**，作者直接用 compute + UAV 替代，对四个相邻 quad 按 parallelogram 估计底高——更简单但近似。
- **性能瓶颈在光栅化**：太阳盘大、ghost 多，overshading 严重。Compute/DrawIndirect 做 coarse culling 丢弃低强度 ghost 是未来方向。
- **诚实披露**：作者提醒原论文作者已就算法申请专利，商用需小心。
- **starburst** 用 Fraunhofer 近似：同一份光圈 Fourier 信号按波长缩放采样坐标即可合成白光衍射——之后再叠一轮螺旋+小旋转的滤波消除径向 ringing。
- **AR 镀膜的物理**：quarter-wavelength 膜对目标波长反射率最低，厚度偏离理想时反射率上升——作者提供了一个"调厚旋钮"让美术刻意制造镀膜退化。

## 链接到的概念

- [[physically-based-lens-flare]]
- [[physical-camera-model]]
- [[physically-based-shading]]

## 原文

- 链接：https://bitsquid.blogspot.com/2017/07/physically-based-lens-flare.html
- 本地：`raw/articles/bitsquid.blogspot.com/2017-07-03_physically-based-lens-flare.md`
