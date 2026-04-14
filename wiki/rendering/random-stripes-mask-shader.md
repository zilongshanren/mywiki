---
tags: [渲染, unity, shader, mask, 随机, 后处理, 程序化]
date: 2026-04-14
sources: 1
---

# 随机条纹 Mask Shader（Random Stripes Mask）

**随机条纹 mask** 是一支只做一件事的极小全屏 shader：把屏幕按 Y 方向切成等高的水平条，每条随机填黑或白，生成一张带噪点的横线遮罩。它的价值不在「画面好看」而在**积木性**——后续 [[glitch-image-effect|glitch 后处理]]、CRT 抖动、"坏信号"演出、以及对 [[uv-displacement-image-effect|UV 位移]] 的每行扰动，都把它当作一个**逐行的二值噪声源**来驱动别的效果。[[harry-alisavakis|Harry Alisavakis]] 在 *My take on shaders* 里拿它当作把 [thebookofshaders](http://thebookofshaders.com) 的一维 hash 思路迁移到 Unity 的最小范例。

## 核心公式：floor + hash + step

fragment shader 的关键只有一行：

```hlsl
float random(float2 input) {
    return frac(sin(dot(input, float2(12.9898, 78.233))) * 43758.5453123);
}

float stripes = 1 - step(_Fill, random(floor(i.uv.y * _Frequency)));
return float4(stripes.xxx, 1);
```

三步走：

1. **`floor(uv.y * _Frequency)`**——把 `[0,1]` 的屏幕 Y 坐标乘以「每屏几条」的频率，再向下取整，等价于把屏幕切成 `_Frequency` 条等宽水平带，同一条内所有像素拿到同一个整数 ID。
2. **`random(id)`**——经典的 `frac(sin(dot(x, k)) * big)` 伪随机 hash。数学上它不可解释，工程上它便宜且几乎处处不相关，Book of Shaders 把它当作 "one-liner 伪随机" 的事实标准。[[shader-color-interpolation|shader 里的值噪声]] 几乎都以它为起点。同一条带里所有像素 hash 到同一个 ID，就得到同一个随机值——**相邻像素有相关性、条带之间独立**，这正是条纹 mask 想要的结构。
3. **`step(_Fill, r)`**——把 `[0,1]` 的随机数二值化：超过 `_Fill` 得 1、否则 0，再反一下得到「白条占比 = 1 - _Fill」的黑白带图案。`_Fill` 这个名字其实反了直觉（fill 大反而空洞大），但一旦理解它是 "step 的阈值" 就不再困惑。

## 为什么是「逐行二值噪声」而不是图像

直接用这张 mask 本身没什么看头——它只是一堆黑白横条。它真正的用法是**把 `stripes` 当权重**去驱动另一个效果：

- 在 glitch shader 里，`stripes * _DisplacementAmount` 就是「这一行是否参与水平位移」的开关，得到经典的 VHS 横向撕裂。
- 做两套（`_RightStripesFill` / `_LeftStripesFill`），一套向右位移、一套向左位移再相减，画面一半行向左跳、一半向右跳，像信号严重失真的电视机。
- 把白条换成「这行要加色噪」或「这行要采样偏移 color ramp」，就变成 CRT scanline / 荧光屏闪烁。

关键观察：条纹 mask 不关心**横向**分布，只靠 `uv.y` 做 hash，**同一条带里的每一个像素都是同一个随机值**。这让它天然适合描述「一整行一整行出问题」这种硬件故障的语义——真实 CRT 的扫描线、VHS 的磁迹头跳针、LCD 信号丢线，都是以行为单位出错的。

## 性能与退化

- **每像素只有一次 `sin` 一次 `dot` 一次 `frac`**。即便 1080p 全屏也几乎察觉不到开销，这是 "hash-based procedural mask" 相对采样贴图的最大卖点：完全零带宽占用。
- **分辨率无关**：频率参数是屏幕空间的，不依赖像素尺寸。
- **依赖 `sin` 精度的陷阱**——在某些移动 GPU 上 `sin(巨大数)` 会出现周期性伪影，因为低精度浮点丢失了高位。工程上的对策是换成 [[pcg3d-hash|PCG / Wang hash]] 类整数混合函数，以牺牲几行代码换可预测性。
- **帧间静止**：没有时间项的话这张 mask 每帧一样，看起来是死的。要让它"闪"起来，在 hash 输入里混一个 `_Time.y` 或一个帧计数即可。

## 相关

- [[glitch-image-effect]] —— 主要消费者，两套条纹 mask + 波浪位移 + 色差
- [[custom-mask-shaders]] —— 同系列里「坐标函数算 mask」的另一种路线（圆盘 / 圆环 / SDF）
- [[image-effect-mask-blend]] —— 前驱，用贴图做 mask
- [[uv-displacement-image-effect]] —— 常见的下游效果
- [[shader-color-interpolation]] —— `frac(sin(...))` 在着色器里的来源
- [[pcg3d-hash]] —— 更鲁棒的替代 hash
- [[unity-image-effect-basics]]
- [[shaping-functions]] —— `step` 作为二值化 shaper
- [[harry-alisavakis]]

## Sources

- [[sources/halisavakis-random-stripes-mask]]
