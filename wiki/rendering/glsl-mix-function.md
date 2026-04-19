---
tags: [渲染, shader, glsl, 插值, 颜色]
date: 2026-04-19
sources: 1
---

# GLSL mix 函数的进阶用法

`mix(x, y, a)` 在 GLSL 里就是线性插值：`x + (y-x) * a`，等价写法 `x*(1-a) + y*a`。看似平平无奇，[[xor-shader-artist|Xor]] 却在「Functions: Mix」里列了一串容易被忽略的用法。

## 颜色空间里的小工具

### 饱和度控制

灰度插值到彩色：

```glsl
float gray = dot(col.rgb, vec3(0.2126, 0.7152, 0.0722));  // luma
col = mix(vec3(gray), col, SATURATION);
```

- `SATURATION = 0` → 灰度
- `SATURATION = 1` → 原色
- `SATURATION > 1` → **过饱和**（超出 [0,1] 范围，但 mix 不限制 $a$，天然外推）
- `SATURATION < 0` → **色相取反**

### 亮度 + 对比

`col = mix(vec3(BRIGHTNESS), col, CONTRAST)`：

- `CONTRAST < 1` → 对比度降低、向 BRIGHTNESS 收敛
- `CONTRAST > 1` → 对比度提升，外推
- 把 `BRIGHTNESS` 改成 RGB 三元组就是**每通道独立增益**——做色温校正、lift/gamma/gain 的基础砖。

## 插值外推

由于 `mix` 不检查 $a \in [0, 1]$，它同时能做 extrapolation：

- `mix(a, b, 2.0)` 就是 `a + 2(b-a)`，即沿 $a \to b$ 方向再走一步。
- `mix(origin, target, -0.5)` 则反着外推。

这个性质让「mix + 负数 / 大于 1 的系数」可以伪装成很多其它操作。

## 坐标操作

### 两点间插值（动画 / 过渡）

`vec2 pos = mix(POS1, POS2, time_factor);` 基本不用说。

### 径向模糊 / 色散

把 UV 向一个焦点拉回：

```glsl
for (float i = 0; i < 1.0; i += 0.05) {
    vec2 tuv = mix(uv, vec2(0.5), i * 0.2);
    col += texture(iChannel0, tuv) * 0.05;
}
```

**可读性远好于**手写 `uv * 0.9 + vec2(0.5) * 0.1` ——一眼看出中心和强度。

### Texture atlas 坐标映射

```glsl
vec2 uv = mix(uvs.xy, uvs.zw, norm_uv);
```

把 `[0,1]` 标准化 UV 映射到 atlas 里某个子矩形——比手写两次 `pos = min + norm * (max - min)` 简洁。

## remap：mix 的反推版

`mix(a, b, x)` 把 `x ∈ [0,1]` 线性映到 `[a,b]`。常常需要反过来：把 `x ∈ [a,b]` 映到 `[c,d]`：

```glsl
float remap(float a, float b, float c, float d, float x) {
    return (x - a) / (b - a) * (d - c) + c;
}
```

处理 UV、纹理页、角度范围的救命工具。记为 `mix 2.0`。

## 感知正确的 Mix

RGB 空间下 `mix(red, green, 0.5)` 通常**不是视觉上的中间色**——中间会浑浊发暗。要视觉感知均匀，切到 [[oklab-color-space|OkLab]] 再 mix、再转回：

```glsl
vec3 mix_oklab(vec3 a, vec3 b, float t) {
    return oklab_to_rgb(mix(rgb_to_oklab(a), rgb_to_oklab(b), t));
}
```

代价不大、效果显著（尤其浓色相互混合时）。

## 建议

- **能用 `mix` 写的就用 `mix` 写**——比显式展开更易读、更容易被驱动优化。
- 始终意识到 `a` 可超出 [0,1]——这是 feature 不是 bug。
- 颜色混合先想想"需要感知均匀吗"。

## 相关

- [[xor-shader-artist]]
- [[oklab-color-space]]
- [[hyperbolic-tangent-shader]]
- [[shader-color-interpolation]]
- [[raymarching-intro]]

## Sources

- [[sources/xor-functions-mix]]
