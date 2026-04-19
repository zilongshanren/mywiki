---
tags: [渲染, 体积云, raymarching, 时间重投影, upsampling, jitter, unity]
date: 2026-04-19
sources: 1
---

# 体积云：1/4 分辨率 + jitter + 时间 reproject 升采样

Horizon Zero Dawn 的体积云 presentation 里有一句广为流传的说法——"每帧只更新 1/16 的像素"。很多人（包括 Steven Sell）第一次读的时候误解了这句话：以为是在 full-res buffer 里 **跳过 15/16 像素**。按这个字面意思写下来性能根本没提升——因为 GPU 的 wave/warp 宽度是 16/32/64，一组里只要有一个 fragment 要执行，其它 15 个在分支处等它结束，"跳过"不省 wave 时间。

正确的读法来自《Optimizations for Real-Time Volumetric Cloudscapes》论文：**在一张 1/4 宽、1/4 高的 offscreen buffer（即 1/16 像素）里 raymarch**，然后用时间 reprojection + jitter 把结果填回 full-res。两层优化相互支撑。

## 三张 buffer 的舞蹈

- `Quarter`：本帧 raymarch 的低分辨率输出。
- `FullPrev` / `FullCurr`：双缓冲的全分辨率累积结果。

每帧的流程：
1. 在 `Quarter` 上 raymarch 云（并施加 **jitter**）。
2. 从 `FullPrev` 采样历史 + 从 `Quarter` 采样当前，按"这个 full-res 像素是不是本帧 jitter 选中的那个"决定混合权重，写到 `FullCurr`。
3. Swap Front/Back。

## Jitter：让每个像素都被轮询到

单纯把 1/16 像素用 bilinear 放大到 full-res 肉眼就能看出来是"糊开的小图"。**Jitter** 的作用是让每一帧 raymarch 的那 1/16 像素**位置不同**——16 帧下来正好覆盖每个 4×4 block 里的 16 个位置，等价于完整采样，代价是每个像素的刷新率是 1/16 而不是 1。

实现上用一个预计算的打散顺序（不是按顺序扫，否则屏幕上会看到"扫描线"）：

```cpp
Vector2[16] FrameJitters = { (0,2),(0,1),(3,1),(1,2),
                              (0,3),(1,0),(1,3),(1,1),
                              (2,0),(2,1),(3,2),(0,0),
                              (2,3),(3,0),(2,2),(3,3) };
```

Jitter 作用在 raymarch 的 ray direction UV 上：`uv + jitter / fullRes`。注意除以**全分辨率**而不是 quarter——jitter 的幅度对应 full-res 像素，否则相邻帧采样会跳 4 格，相当于白给了 15/16 的工作。

## Upsample 的 jitter correction

naive bilinear upsample + 历史混合会让云"抖动"。解法是写一个 **JitterCorrection(uv)** 返回 0/1：本帧 4×4 block 里那个被 jitter 选中的位置返回 0（用当前帧），其它 15 个位置返回 1（沿用历史）：

```hlsl
float2 localIndex = floor(fmod(uv * fullRes, 4.0));
localIndex = abs(localIndex - jitter);
return saturate(localIndex.x + localIndex.y);
```

再做 `lerp(curr, prev, correction)` 就能把"本帧新渲的那一格"正确地写进历史，其它位置保持。

## Convergence speed 控制

顶点（天顶）方向的云距离相机近，对视觉敏感，希望更新更快；地平线远，可以慢。给 lerp 一个额外权重：

```
d = saturate(length((uv-0.5)*2));
speed = lerp(0.75, 0.5, d);
```

或者直接用 raymarch 出来的深度做权重，让近距离的云优先 converge。

## 为什么"跳过像素"方案会失败

- **Wave 粒度**：GPU 的 wave 要等所有 lane 结束才能退役，少数工作的 lane 不会节省 wave 的时间。
- **缓存粒度**：fragment shader 按 2×2 quad 调度（ddx/ddy 依赖），稀疏 active 破坏这个假设。
- **bandwidth 不变**：color/depth attach 的写回粒度是固定的，写少数像素不省带宽。

1/4 分辨率 raymarch 直接把 fragment 数量砍到 1/16，这些问题全部消失——wave/quad/bandwidth 都按 quarter buffer 的真实大小工作。Jitter + temporal 只是把剩下的"分辨率缺口"在时间维度上补齐。

## 和其它 temporal 工程的家族性

这条路子和 [[temporal-antialiasing]] / [[temporal-supersampling]] 本质同构——都是**把昂贵采样分散到多帧**，然后用 history buffer 累积。体积云的特殊点在于 raymarch 本身就是 per-pixel 独立的（没有几何 motion vectors），history invalidation 更温和，主要靠 depth-weighted convergence 而不是 rectification box。

## 相关

- [[temporal-antialiasing]]
- [[temporal-supersampling]]
- [[volumetric-raymarching-intro]]
- [[depth-aware-upsampling]]
- [[horizon-zero-dawn-clouds]]
- [[steven-sell]]

## Sources

- [[sources/vertexfragment-cloud-upsample]]
