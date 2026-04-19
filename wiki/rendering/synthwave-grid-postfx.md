---
tags: [rendering, post-processing, world-space, grid, stylized, synthwave]
date: 2026-04-19
sources: 1
---

# 世界空间网格后处理（Synthwave Grid Post-Process）

Synthwave 风格的招牌是一张无限延伸的发光网格。Snapshot Shaders Pro 的 Synthwave 效果把这种网格做成一个后处理层：在屏幕空间逐像素**反推世界坐标**，判断该点是否"靠近"三条正交平面（X=kG, Y=kG, Z=kG，G 为 Gap Width），靠近则画线色、远离则画背景色或保留原场景色。

## 反推世界坐标的两个前提

后处理阶段手里只有两件东西：当前像素的 NDC（由 SV_Position / `_ScreenParams` 换算得到）和 [[depth-texture-silhouette|`_CameraDepthTexture`]] 里的深度值。把两者塞进 `ClipToWorld` 反投影（`matrix(inverseViewProj) * float4(ndc, depth, 1)` 除以 w），就能拿到这个像素对应的**世界空间位置** `P`。

有了 `P`，网格判定只是简单的 `frac`：

```hlsl
float3 fp = frac(P / gap + offset);   // 周期化到 [0,1)
float3 d  = min(fp, 1 - fp) * gap;    // 到最近线面的距离（世界单位）
```

`d.x`、`d.y`、`d.z` 就是当前像素到三组无限平面（垂直于 X / Y / Z 轴）的距离。每一个分量再和 `lineWidth`、`lineWidth + falloff` 用 `smoothstep` 做一次软边，取 max 合并三轴就是 "当前像素离网格线有多近" 的强度。

## 参数与轴掩码

Pro 版暴露的参数几乎一一对应上面的公式：

- `Gap Width`（各轴独立）—— 上式里的 `gap`
- `Line Width` —— 实线硬边半宽
- `Line Falloff` —— 从硬边到背景的过渡宽度（smoothstep 第二参）
- `Offset` —— 把整个网格沿 `(0,0,0)` 方向平移
- `Axis Mask` —— 三个 bool，关掉某一轴就跳过那一组平面（只留 XZ 地面格、只留 Y 垂直墙等）
- `Line Colors 1 & 2` + `Line Color Mix` —— 两个 HDR 色按屏幕 y 做 gradient，典型的 synthwave 粉/青渐变
- `Background Color` / `Use Scene Color` —— 关掉 scene color 就是纯色背景的"数字虚空"，开起来就是叠加在实拍场景上的发光格子

## 和其它手段的差别

- **vs 在地面 mesh 上画 grid shader**：优点是**不用任何几何**、可以让网格穿过物体背后；缺点是每个像素都要反投影，开销随分辨率走
- **vs UV-space grid**：UV-space 不会随相机运动而"透视正确"，synthwave 要的就是无限延伸的世界格，必须在世界空间判定
- **HDR 线色 + bloom**：Line Colors 是 HDR-enabled 的设计暗示它期望下游接 [[bloom-threshold-blur-composite|Bloom]]——线色被 bloom 扩散才像霓虹灯

## 相关

- [[depth-texture-silhouette]] —— 反推世界位置前先拿线性深度
- [[coordinate-spaces]] —— clip / view / world 之间的反投影
- [[bloom-threshold-blur-composite]] —— 让线色"发光"的下游节点
- [[urp-volume-post-processing]]
- [[fwidth-derivative-antialiasing]] —— 另一种 grid line 抗锯齿思路（基于屏幕空间导数）

## Sources

- [[sources/danielilett-snapshot-pro-synthwave]]
