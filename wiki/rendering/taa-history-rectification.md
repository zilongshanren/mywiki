---
tags: [渲染, temporal, taa, ghosting]
date: 2026-04-14
sources: 1
---

# TAA History Rectification（历史修正）

**解决 [[temporal-antialiasing|TAA]] 里 ghosting 与 flicker 的一整套启发式技术**。核心问题是：reprojection 之后，历史 buffer 里采到的那个颜色是否真的属于「当前这个表面」？如果不是，直接混进去会出现拖影。Rectification 不是一招鲜，而是一个「组合拳」：color clamping 兜底，更精准的 rejection 叠加其上。

## Color Clamping

最基本也最通用的手段。假设：**当前像素的 3×3 邻域颜色范围足以代表这一位置「合理的」颜色**；超出这个范围的历史颜色就算是失效的，但不要直接丢掉（否则 accumulation 会被反复 reset），而是把它 clamp 进这个 bounding box。

```hlsl
float3 minColor = 1e9, maxColor = -1e9;
for (int y = -1; y <= 1; ++y)
for (int x = -1; x <= 1; ++x) {
    float3 c = CurrentTexture.Sample(uv + offset);
    minColor = min(minColor, c);
    maxColor = max(maxColor, c);
}
float3 previousColorClamped = clamp(previousColor, minColor, maxColor);
```

变体包括 `clamp`、`clip`、**variance clipping**（用均值+方差构建更紧的椭球）。Playdead 的 INSIDE、UE4 的 High Quality Temporal Supersampling 都公开了各自实现。Color clamping 是 TAA 的保底——没有它其他方法都靠不住。

## Depth / Stencil / Velocity Rejection

邻域假设不总是成立——高 contrast 区域邻域很大，clamp 的 bounding box 也很大，拖影还是会漏过来。这时用其他信号精化判断：

- **Depth rejection**：上一帧和当前帧的深度差太大就拒绝。对 FPS 的手+场景分离很有效，对 foliage 之类深度复杂的内容会误判。
- **Stencil rejection**：给重要物体（主角、车辆）打 stencil ID，不同 ID 之间不接受 history。要处理边缘硬切。类似做法也可以用 ID buffer。
- **Velocity rejection**：从定义上讲 disocclusion 就是「相对运动差异」。读当前 velocity 和上一帧同位置的 velocity，比较二者。作者推荐用**差向量的长度**（其实就是帧间加速度）——既不会被反向等长向量欺骗（那是 magnitude 差的问题），也不会在 0 向量处炸（那是 dot product 的问题）。可以 lerp 到一个轻度模糊的版本过渡，避免硬切。

这些方法互不排斥，可以叠加。作者明确说：velocity 不行的时候 color clamping 顶上。

## Flicker：tonemap weighing

clamping 有个副作用——当邻域里出现高亮度 outlier（镜面高光、fireflies），它们会被 clamp 放行，下一帧又消失，造成**闪烁**。修复手段是在 resolve 前给颜色做非线性加权，把亮点压下来：

- **Luminance weighing**：`weight = 1 / (1 + luminance)`
- **Log weighing**：在 log 空间做线性操作

Luminance 加权收敛到常数，log 加权则继续缓慢增长——看场景选。作者两种都实现过，luminance 是 UE4 / Call of Duty 广泛使用的版本。

## Blend Factor Attenuation

UE4 会在即将触发 clamp 事件时**降低 blend factor**——让当前帧权重暂时减小，历史权重增加，避免 clamp 把本该保留的 outlier 直接替换掉。副作用是会让 jitter 重新可见，要小心平衡。

## 相关

- [[temporal-antialiasing]]
- [[motion-vectors]]
- [[aliasing]]
- [[emilio-lopez-ros]]

## Sources

- [[sources/elopezr-taa-holy-trail]]
- [[sources/adrian-doom-2016-graphics]]
