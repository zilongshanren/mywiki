---
tags: [渲染, 阴影, shader, 光照]
date: 2026-04-14
sources: 1
---

# 阴影贴图基础（Shadow Mapping）

**Shadow mapping** 是当前实时渲染里最主流的阴影算法（排除光线追踪）。核心思想一句话：**从光源方向渲染一次场景的深度，然后在正式渲染时用这张深度贴图判断每个像素「能否被光看到」**。它便宜、可扩展、和栅格化管线天然契合，是 3D 游戏必学的第一种阴影技术。本页整理 Xor 在 GM Shaders 的入门教程里覆盖的内容：depth map、hard shadows、bias、edge vignette、soft shadows，以及和 Phong 光照的配合。

## 第一步：深度贴图（Depth Map）

从光源的视角做一次渲染，把每个投射物体的 **投影空间深度 `gl_Position.z`** 写到一张单通道 float 表面（`R32F`）。GameMaker 里这是 `surface_r32float`。只要光源或投射者没动，这张贴图可以跨帧复用——不必每帧更新（参见 [[cached-shadowmaps]]）。

关键细节：

- **单通道浮点**比 RGBA8 + bit-packing 精度高很多，开启纹理插值后还能得到平滑的深度近似。
- 投影矩阵既可以是透视（点光源/聚光灯）也可以是正交（方向光）——算法不变。
- 绘制深度贴图时要**禁用 alpha blending**，否则透明度会污染深度值。

## 第二步：硬阴影（Hard Shadow）

正式渲染时，每个像素计算它在光源投影空间下的位置：

```
p = shadow_proj * shadow_view * world_pos;
uv = p.xy / p.w * vec2(0.5, -0.5) + 0.5;   // 注意 y 翻转
```

采样 shadow map 得到「光源能看到的最近深度」，和 `p.z` 比较。如果像素比它更远，就在阴影里。

### Bias 的必要性

深度精度不是无限的：shadow map 分辨率、float 量化、插值、斜面、投影矩阵……每个环节都在给深度引入误差。不加偏置直接比较，就是全场 [z-fighting]：表面自己把自己遮住，出现条纹状「阴影痤疮」（shadow acne）。典型处理：

```glsl
#define BIAS 0.001
float lit = float(texture2D(shadow_map, uv).r + BIAS > p.z);
```

Xor 推荐从 `0.001` 开始调：太大会让阴影「脱离投射者」（peter-panning），太小会出 acne。更好的做法是把 bias 做成**斜率相关**——表面越倾斜，需要的 bias 越大。这可以通过 `1 / max(-normal.z, 0.1)` 之类的方式估计。

另一个技巧是**把 hard cutoff 换成 soft fade**：

```glsl
float dif = (texture2D(shadow_map, uv).r - p.z) / p.w;
return clamp(dif * FADE + 2.0, 0.0, 1.0);
```

用 `FADE` 控制过渡锐度，单样本就能有一点「假柔边」的观感。

### 边界处理（Edge Vignette）

Shadow map 有限大小，像素可能落在其外（**超出光的视锥**）。纹理 repeat 会产生幽灵阴影。Xor 的干净做法是把「shadow map 里的可见度」做成一个 vignette：

```glsl
vec2 suv = proj.xy / proj.w;           // -1 ~ +1
vec2 edge = max(1.0 - suv*suv, 0.0);   // 边缘向 0 衰减
float shadow = edge.x * edge.y * float(proj.z > 0.0);
```

再加上 `proj.z > 0` 保证不去照亮光源背后的东西（像聚光灯一样）。只有当 `shadow > 一个小阈值`时，才去真正采样 shadow map。

## 第三步：软阴影（Soft Shadow）

硬阴影的边缘是 per-pixel 决策，锯齿和阶梯明显。软化的思路不是**去模糊 shadow map**，而是**对多个采样点分别做 hard 测试后再平均**——这是 PCF（Percentage-Closer Filtering）的基本形式。

### 2×2 双线性（便宜版）

对 4 个邻近 texel 分别测试，再按 fract 坐标做双线性或双三次插值。Xor 给的 `shadow_interp` 就是这种：

```
s00, s10, s01, s11 = shadow_hard(p + 4 个偏移)
return bicubic_blend(s00, s10, s01, s11, fract_uv)
```

比一个样本明显改善，但过渡仍有点「格子感」。

### Fibonacci 圆盘采样（漂亮版）

更好看的方案是在一个圆盘里按**黄金角**均匀撒点，每个点做一次 hard test，最后平均：

```glsl
// 从 blue noise 贴图取个随机起始方向
vec2 dir = normalize(texture2D(noise, gl_FragCoord.xy / 64.0).xy - 0.5);
// 黄金角旋转矩阵
const mat2 gold = mat2(-0.7373688, -0.6754904,
                        0.6754904, -0.7373688);
for (float i = 0.5/NUM; i < 1.0; i += 1.0/NUM) {
    dir *= gold;
    float radius = scale * sqrt(i);  // sqrt 让径向分布均匀
    sum += shadow_hard(p + radius * vec4(dir, BIAS*slope, 0));
}
return sum / NUM;
```

这里的两个关键细节：

- **blue noise 起始方向**：避免所有像素用同一个采样分布，把误差分散成高频噪声而不是低频条纹。
- **`sqrt(i)` 半径**：让样本按面积（不是半径）均匀分布，即真正的圆盘采样。参考 [[poisson-disk-sampling]]。

### 注意性能

大模糊半径的软阴影会**拖 GPU**——不是算术成本，而是 **texture cache**：GPU 为空间上紧邻的采样做了大量优化，大范围、分散的采样直接踩穿 cache。降低样本数、降低 shadow map 分辨率、或者在后处理阶段叠一个 [[depth-aware-upsampling|depth-aware blur]] 往往比堆样本数更划算。

## 和光照的配合：Phong

Xor 把整套算法和一个简化的 [Phong 光照模型](https://en.wikipedia.org/wiki/Phong_reflection_model) 配在一起。关键技巧是**把法线变换到 shadow space**——这样「朝向光」就等于「`-normal.z > 0`」，连点积都省了：

```glsl
v_normal = mat3(u_sha_view) * mat3(world_mat) * in_Normal;
```

- **Diffuse**：`0.5 - 0.5 * normal.z`（平滑的半兰伯特风格）。
- **Specular**：`pow(max(reflect(eye, normal).z, 0.0), EXP)`。
- **Shadow** 和 **diffuse** 相乘，再加 ambient 保底。
- 整个过程在 linear RGB 里做，最后 `pow(col, 1/gamma)` 回到 sRGB（见 [[color-space]]）。

## 进阶方向

这些是教程里提到但没展开的后续：

- **Cascaded Shadow Maps（CSM）**：把视锥按距离分成多个级联，每个级联单独一张 shadow map，解决「一张贴图覆盖大范围就没精度」的问题。和 [[cached-shadowmaps]] 自然组合：远级联本来就很少变。
- **Variance Shadow Maps / Moment Shadow Maps**：把「深度比较」换成「可过滤的概率统计」，让软阴影能用普通的 gaussian blur 解决。
- **Ray-traced shadows**：有硬件支持时的正确答案，但回退路径依然需要 shadow mapping。
- **Volumetric shadows**：Xor 这篇的本意就是为 volumetric 打底。

## 相关

- [[cached-shadowmaps]] — 把远级联结果跨帧缓存
- [[z-buffer]]
- [[reversed-z]]
- [[color-space]] — 光照/阴影必须在线性空间做
- [[poisson-disk-sampling]] — 软阴影采样内核的姊妹技术
- [[depth-aware-upsampling]] — 后处理软化
- [[coordinate-spaces]]
- [[xor-shader-artist]]
- [[sdf-ray-marched-shadows]] —— 2D SDF 场景里的 raymarch 软阴影路径（和 shadow map 无关的另一个谱系）

## Sources

- [[sources/xor-shadowmaps]]
