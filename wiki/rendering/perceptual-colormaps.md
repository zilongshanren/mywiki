---
tags: [渲染, 颜色, color-lut, 可视化, matplotlib]
date: 2026-04-14
sources: 1
---

# 感知均匀 colormap 与热成像着色

**Colormap**（色彩映射）是一种**一维查找表**：把一个标量（温度、高程、速度、密度……）映射到一个 RGB 颜色。热成像相机几乎都是单通道灰度传感器，呈现给用户看的那张彩色画面其实是 **「灰度 → palette」** 的一次 1D 查找。这正是 [[color-lut|1D LUT]] 最经典的场景，也是 matplotlib 整个 colormap 系统要解决的问题。

## 为什么要「感知均匀」

一个合格的科学可视化 colormap 必须满足：**标量上均匀间隔的值，在人眼看来也是均匀间隔的**。失败案例是老派的 `jet`（MATLAB 的 rainbow）——它在绿色附近聚集大量感知对比，在青色附近几乎是平台，结果「温度差 10 度」在不同区段看起来变化完全不一样，会在数据上制造**虚假边界**和**隐藏真实边界**。matplotlib 2.0 以 `viridis` 为默认就是为了解决这个问题：

- **viridis / inferno / plasma / magma**——感知均匀、对色盲友好、在灰度打印上仍然单调；
- **cividis**——专门为色盲校准的黄蓝序列；
- `jet` / `rainbow` / `hsv`——保留给怀旧，但 matplotlib 文档明确不推荐用于数据。

Frost 建议在 DaVinci Resolve 里做热成像调色时，**除非有明确艺术目的或特殊数据布局，否则永远用感知均匀的那一组**——和实时图形里 [[color-banding|去色带]] 的动机一致：让台阶之间的视觉变化和量化步长同步，不要给肉眼制造假结构。

## 把 matplotlib colormap 烘进 `.cube`

DaVinci Resolve 用 **Iridas/Adobe `.cube` 格式**存 LUT——这个格式**支持 1D LUT**，恰好就是一维 colormap 的最小载体。Frost 写了一段 Python 用 `colour-science` 包把 matplotlib 的所有 colormap 一次性烘成 `.cube` 1D LUT：

```python
grayscale_values = np.linspace(0, 1, lut_size)
colors = plt.get_cmap(colormap_name)(grayscale_values)[:, :3]
lut = LUT3x1D(table=colors, name=f"Colormap {colormap_name}")
write_LUT_IridasCube(lut, file_name)
```

思路极为简洁：在 `[0, 1]` 上均匀采样灰度，查 matplotlib 的 cmap 得到每个采样点的 RGB，塞进 `LUT3x1D` 表，写回 `.cube`。默认 `lut_size = 256`——对 8-bit 输入完全够用，也和任何像素格式对齐。

导入 DaVinci Resolve 的流程是「Preferences → 加 LUT 目录 → Color 页选中 LUT」——一旦 LUT 就位，任何 grayscale footage（真热成像、红外、热泵工业镜头，甚至普通 B&W 视频）都能一键着色，而且比成品「thermal look」贴图滤镜灵活得多：把对比度、曝光、色调偏移都留在 Resolve 的节点图里单独调。

## 和其他 LUT 用法的区别

Frost 自己的另一篇 [[color-lut]] 长文讲的是**游戏里**的 LUT——3D LUT 做 color grading，1D LUT 做 tinting。本文则是**视频后期**里的对称用法：同样是 1D LUT，但输入是灰度而不是 RGB，目的是着色（coloring）而不是调色（grading）。两者共享同一份工具链（`.cube` 格式、shader 里的 texture tap、DaVinci 的节点系统），只是输入维度不同。

从引擎角度看，这也是一个提醒：**1D LUT 是非常便宜的通用基元**——任何可以表示为「标量 → 颜色」的可视化（ragdoll velocity heatmap、mipmap level debug overlay、light complexity view、lightmap density、GPU 时间花销按 tile 着色）都可以复用同一套 1D LUT 资产，而不需要在每个 debug pass 里写一个独立的插值算式。只是要选感知均匀的 colormap——让 debug 视图告诉你的和你看到的是同一件事。

## 相关

- [[color-lut]] — 1D/3D LUT 的游戏 fragment shader 用途
- [[color-banding]] — 同样关心「视觉线性度」的另一面
- [[frost-kiwi]]

## Sources

- [[sources/frost-kiwi-thermal-colormaps]]
