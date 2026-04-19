---
tags: [rendering, blur, post-processing, bloom]
date: 2026-04-19
sources: 1
---

# Dual Kawase Blur

**Dual Kawase Blur** 是目前游戏引擎与桌面合成器（KDE、macOS 风格的毛玻璃）里最流行的大半径模糊算法之一，由 Marius Bjørge / ARM 在 SIGGRAPH 2015 的《Bandwidth-Efficient Rendering》报告中正式提出，本质上是 [[kawase-blur]] 的"多级金字塔"版本。核心思想是：把 Kawase 原本单级的四角采样和 mipmap 式的**下采样 + 上采样**结合——先一路把 framebuffer 降到 1/4、1/16、1/64 分辨率，每一步都用一个便宜的 Kawase 风格 tap 结构读取，再沿相同台阶一路上采样、把低频结果加回高频层。由于每一级的输入像素数呈 4 倍收缩，整条 pipeline 的 texture taps 数近似于线性而非正方形增长，大半径模糊依然保持实时预算内。

视觉上，Dual Kawase 的输出与 [[separable-gaussian-blur]] 几乎无差别——它同样是"低通滤波"，只是把滤波行为从两次 1D pass 迁移到了多级金字塔上。关键的工程收益来自两点：一是**双线性采样**（见 Frost Kiwi 对 `samplePosMultiplier` 与 bilinear tap 的解读）——把 tap 位置放在像素格子正中间时，一次硬件 texture 读取就等价于 4 个像素的平均；二是**分辨率压缩**——下采样本身就是一种低通，只要避免明显走样，就可以用非常少的 tap 数实现接近大 kernel 高斯的外观。

在 Bloom 场景里，Dual Kawase 往往替代了更老的"Threshold + Separable Gaussian"组合，因为它可以在多级金字塔里同时完成 [[bloom-threshold-blur-composite]] 里的模糊分层，和 Unreal/Frostbite 那种"多级权重相加"的 lens flare 外观兼容良好。它也被 KDE 与各路 Wayland 合成器用于实时的毛玻璃背景（"frosted panel"），因为手机 / 集成显卡的带宽预算下，这是唯一能做到 4K 全屏实时大半径模糊的选项。

Frost Kiwi 的这篇交互式长文是目前对 Dual Kawase 最完整的博客级教材，把 [[convolution-separability-blur]]、bilinear 采样、downsampling 几个点串进同一条"graphics programming time travel"里讲清楚。

## Sources

- [[sources/frost-kiwi-video-game-blurs]]
