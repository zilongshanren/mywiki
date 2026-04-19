---
tags: [rendering, shader, debugging, precision]
date: 2026-04-19
sources: 1
---

# Shader 常见陷阱速查

Xor 在 Common Shader Mistakes 汇总了他「写过上千小时 shader 后仍然踩」的坑，大体分五类：清晰度、颜色、纹理、坐标、精度。这页可以当 bug 清单反复来查。

## 清晰度

- 变量命名要一致。`c` 到底是 color 还是 coord？一旦混用，很快就找不回来。
- **uniform 名拼错不会报错**，只会静默给 0.0——屏幕全黑时第一个怀疑它。
- 消灭魔法数字：用 `const` / `#define` / uniform 命名，避免散落的 `0.5`、`32.0`。

## 颜色：主要是 NaN 传染

NaN 一旦出现，后续任何算术都把它传下去，对应像素永远黑。高发点：

- `sqrt(x)` / `log(x)` / `log2(x)` / `pow(x, y)` 在 `x<0` 时；对策 `max(x, 0.0)` 或 `abs(x)`。
- `acos(x)` / `asin(x)` 在 `|x|>1` 时；对策 `clamp(x, -1.0, 1.0)`。
- `0.0 / 0.0` —— 任何除法都要留神。
- 光照衰减选 **inverse square** 最物理正确；banding 用 [[floyd-steinberg-dithering|dither]] 掩盖。
- 颜色运算要先解 gamma 再编回 sRGB（见 [[gamma-correction-srgb]]）。

## 纹理

- 引擎（比如 GameMaker）把多个精灵打包进 **texture page**，所以 **texture coord 不一定是 [0,1]**。要用 `(coord - uv.xy)/uv.zw` 显式归一化（见 [[two-texture-sampling-tricks]]）。
- **硬件双线性插值只有 256 个中间步**（iq 的老发现），放大得太厉害会露步进。
- [[mipmap-generation-sampling|Mipmap]] 按 2×2 quad 判断 LOD，UV 在 quad 内出现**突变**（比如 `fract` 分支）就会选错级，出现 2×2 色块。处理办法：手动 `textureGrad` 或去掉 UV 不连续。
- 某些设备不支持 non-power-of-two，会偷偷 pad 纹理，假设全范围 `[0,1]` 的 shader 会在那类设备上失真。

## 坐标

不同分辨率 / 宽高比下稳定，是 shader 艺术最基础的「能跑到任何地方」门槛。常见坐标系（见 [[coordinate-spaces]]）：screen-space、texel、world-space、model-space；每一次转换都要显式、清楚单位。

## 精度

- 移动端默认 `mediump`，桌面可能是 `highp`；颜色 `lowp` 通常够，纹理坐标 `mediump`，**位置 / 程序化噪声必须 `highp`**。
- **时间 uniform 长时间累积后精度崩**：测试时把 `u_time` 乘 1000 模拟几个小时后的状态；常见解法是每 ~600 秒循环回 0。
- 锐利边缘没实现 AA 就是偷懒，详见 [[analytical-antialiasing]]、[[fwidth-derivative-antialiasing]]。

## 工具

调试推荐 **RenderDoc**（桌面端都用）和 **SHADERed**（离线编辑/profile）。

## Sources

- [[sources/xor-mini-common-mistakes]]
