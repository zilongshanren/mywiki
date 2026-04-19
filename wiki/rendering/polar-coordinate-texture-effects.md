---
tags: [渲染, shader, 纹理效果, 极坐标, unity]
date: 2026-04-19
sources: 1
---

# 极坐标纹理效果

2D 纹理效果里，**把 UV 从笛卡尔坐标换到极坐标**是一个便宜又好用的把戏。Steven Sell 在复刻《荒野之息》脚下水圈时走了一条弯路——先用 [[sdf-2d-primitives|SDF 环形]]+ sin/cos 做涟漪，结果 fade 均匀、看起来像心电图而不是水花——再绕回极坐标才把效果做对。

## 核心变换

以 UV 中心 `(0.5, 0.5)` 为原点，二维 UV 可以映射到 `(r, θ)`，其中 `r` 是到中心的距离、`θ` 在 `[-π, π]` 范围内。HLSL 实现极其朴素：

```hlsl
float2 CartesianToPolar(float2 cartesian, float2 origin) {
    float2 p = cartesian - origin;
    return float2(length(p), atan2(p.y, p.x));
}
```

反向用 `(cos θ, sin θ) * r` 加回原点即可。约定上要注意——Sell 早期代码把 `(θ, r)` 和 `(r, θ)` 搞反，得到了"好看的错误"，提醒"方向不重要，一致性重要"。`atan2` 和 `sqrt` 的 round-trip 会引入可见的浮点误差，ShaderToy 上常用的误差可视化是 `abs(polarToUV(uvToPolar(uv)) - uv) * k`。

## 为什么极坐标适合"从中心扩散"

在 UV 空间用 `polar.yx` 采样一张 tileable 噪声，结果就是**以中心为原点、沿角度方向平铺的噪声带**。对 `polar.y`（角度维）做 `+= _Time * speed` 会让图案旋转；对 `polar.x`（半径维）做 `-= _Time * speed` 会让噪声**从中心向外扩散**——不用改贴图、不用改几何、不用改 UV 布局，一行代码就出涡旋 + 扩散效果。

`θ = 0` 这条缝必然有 discontinuity（角度回卷），Sell 的做法是把 `[-π, π]` 映射到 `[0, 1]` 并让旋转运动把这条缝不断扫过不同方位，加上纹理本身的 tileable 性质让肉眼很难看到接缝。

## 与 SDF 环形组合

极坐标采样给出了"swirl noise"，SDF 给出了"环的形状"——两者相乘就是"环内纹理扩散"。Sell 的水圈最终公式是：

```
final = saturate((polarNoise * sdfRing - fade01) * strength)
```

`fade01` 的减法做 **time-based dissolve**：随时间推进只保留噪声最亮的顶部，整个环逐渐崩解成碎片，避免了均匀 fade 带来的"心电图感"。

## 超出水圈：投影与 demo art

极坐标还有一个在体积云里常见的用途——把 raymarch 结果渲到一张**极坐标参数化**的 offscreen texture，然后贴到一个半球 mesh 上，天空盖的 UV 就是极坐标，球心在正上方。ShaderToy 上很多 "swirling galaxy / tunnel / portal" 类的作品其实都是这同一个把戏——UV 变换到极坐标，然后在极坐标空间做常规的纹理 + 噪声 + 时间偏移。

## 相关

- [[uv-manipulation-nodes]]
- [[coordinate-spaces]]
- [[sdf-2d-primitives]] — 环、距离场，和极坐标组合
- [[classic-shader-noise]] — 被极坐标采样的那张 tileable 噪声
- [[steven-sell]]

## Sources

- [[sources/vertexfragment-polar-coordinates]]
