---
tags: [人物, 作者, 渲染, 图像处理]
date: 2026-04-14
sources: 7
---

# Bart Wronski（Bartosz Wroński）

**Bart Wronski** 是波兰图形学/图像处理工程师，长期博客 [bartwronski.com](https://bartwronski.com) 是渲染、信号处理、计算摄影方向最值得追的个人技术站之一。他先后在 **Sony Santa Monica（God of War）** 担任图形程序员，后来加入 **Google**，参与 Pixel 手机的 **HDR+** 与 **Night Sight** 等计算摄影流水线。

## 风格

- **从渲染工程到信号处理**：把音频/通信领域的 IIR、Z 变换、Wiener 反卷积等工具引入到实时图形领域，并交叉应用到 TAA、模糊、反卷积等问题上。
- **偏好数据驱动**：相比手工推导滤波器系数，他更倾向把问题写成可微目标 + 梯度下降，让 Jax 帮忙搜索系数。
- **诚实地讲缺点**：每篇文章后面都会专门列「为什么这个方法不一定适合你」——稳定性、数值精度、缓存带宽、并行度。
- **配 demo / 代码**：很多文章带 Colab、Jax notebook 或 WebGL 在线 demo，可以直接玩。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| Exposure Fusion – local tonemapping for real-time rendering | [[local-tonemapping]]、[[exposure-fusion]]、[[laplacian-pyramid]] |
| Gradient-descent optimized recursive filters for deconvolution | [[iir-filter-deconvolution]] |
| Poisson disk/square sampling generator for rendering | [[poisson-disk-sampling]] |
| New debugging options in CSharpRenderer | [[gpu-printf-debugging]]、[[debug-visualization]] |
| Bokeh depth of field – going insane! part 1 | [[scatter-bokeh-dof]] |
| Temporal supersampling pt. 2 – SSAO demonstration | [[temporal-supersampling]] 的 AC4 实测补充 |
| Runtime editor-console connection in The Witcher 2 | [[runtime-editor-console-connection]] |

## 相关

- [[local-tonemapping]]
- [[exposure-fusion]]
- [[laplacian-pyramid]]
- [[iir-filter-deconvolution]]
- [[poisson-disk-sampling]]
- [[gpu-printf-debugging]]
- [[screenspace-reflections]]
- [[temporal-supersampling]]
- [[temporal-antialiasing]]
- [[gcn-wave-occupancy]]
- [[gpu-latency-hiding]]
- [[scatter-bokeh-dof]]
- [[runtime-editor-console-connection]]
- [[chromatic-aberration-post]]
- [[thin-lens-model]]

## Sources

- [[sources/bartwronski-exposure-fusion]]
- [[sources/bartwronski-iir-deconvolution]]
- [[sources/bartwronski-poisson-sampling]]
- [[sources/bartwronski-csharprenderer-debug]]
- [[sources/bartwronski-future-of-ssr]]
- [[sources/bartwronski-temporal-supersampling]]
- [[sources/bartwronski-gcn-latency-hiding]]
- [[sources/bartwronski-bokeh-insane-pt1]]
- [[sources/bartwronski-temporal-ssao]]
- [[sources/bartwronski-editor-console-connection]]
