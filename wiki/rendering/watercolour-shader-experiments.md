---
tags: [shader, shadergraph, urp, 风格化, 后处理, 技术美术]
date: 2026-04-14
sources: 1
---

# 水彩 Shader 实验（Cyan 的三层组合）

Cyan 为 [[harry-alisavakis|Harry Alisavakis]] 主办的 `#TechnicallyAChallenge` 「水彩」主题做的一组 URP shader。它的有趣之处不是任何一个 shader 单独有多复杂，而是**三层 shader 协同工作**才能形成完整的水彩观感——每层负责一种水彩特征，组合起来就接近真实水彩的视觉语法。

## 三层结构

- **Object Shader（对象着色器）**：场景里所有 mesh 的材质。承担基础光照（自定义 Lambert + brighten）、Triplanar 噪声纹理（模拟纸纤维）、以及最关键的「**水彩阴影**」——把硬阴影边缘加深，模仿湿笔触在纸边缘聚集颜料的现象。
- **Image Effect Shader（全屏后处理）**：通过 [[blit-render-feature|Blit Render Feature]] 在整个画面上跑一遍。负责 Roberts cross 边缘检测（生成深色描边）、轻微的 UV 扭曲（模拟纸面起伏）、以及边缘的白色 vignette（模拟颜料淡出到空白纸面）。
- **Decal Shader（贴花着色器）**：散落在场景里的几个 cube，从 Scene Depth 重建世界坐标然后投影到表面上，画出绿色「苔藓水彩斑点」。这也是水彩最易识别的视觉签名——颜色是在不规则的斑块里生长的，而不是均匀填充。

三层加在一起还原了水彩的几个核心视觉要素：纤维感的纸面噪声、笔触在边缘聚集的暗边、湿润扩散的不规则形状、画面边缘的留白渐隐。

## Object Shader：水彩阴影的边缘加深

最值得拆解的是水彩阴影。常规 Lambert 阴影是「shadowed = 黑，lit = 白」的连续过渡；水彩观感要的是「lit 几乎全白、shadowed 边缘有一圈深色、shadowed 中心反而较浅」。Cyan 的实现是：

1. 对 `Shadow Attenuation` 取 `One Minus`（让 shadowed 区域变成 1）。
2. 把这个值压到 `0.5`（阴影最暗就是中灰，不要全黑）当 `Lerp.B`。
3. 用 `Step(Shadow Atten, 0.95)` 在 shadow 边缘附近产生一个硬切的 mask 当 `Lerp.T`。
4. `Lerp.A` 设为 `1`。

结果是：shadow 区域中心是中灰、shadow 边缘附近是接近白（被 step 选中），最后再把这个调制乘到漫反射上。视觉效果就是「阴影中间淡淡的灰、边缘有一道深色环」，正好对应湿笔在干纸上聚集的边缘。

阴影还要先经过**噪声扰动**让边缘不规则——把世界坐标的 Simple Noise 累加，喂进 shadow 采样位置的 offset。但单纯沿任意方向 offset 会把阴影**推进 mesh 自身**产生伪影，Cyan 的 trick 是用 C# 把主光的旋转矩阵作为 `_WorldToMainLightMatrix` 全局属性传给 shader，然后 offset 量乘以这个矩阵——只沿光源方向（局部 Z 轴）扰动，避免错误穿透。

噪声本身用 [[triplanar-mapping|Triplanar]] 节点采样以避免 UV 接缝；为了模拟「水彩颜料并非均匀分布」的颗粒感，对 triplanar 噪声做 `Multiply * strength → Subtract → Absolute`，得到带暗斑的 mask 再乘到 diffuse 上。

## Image Effect Shader：Roberts cross + Vignette

后处理层做了三件事，每件都很短：

- **Distortion**：Simple Noise（scale ≈ 200）减去 `0.5` 居中、乘 `0.01` 减弱，喂进 `Tiling and Offset` 的 offset 输入。整张画面看起来轻微「抖」，模拟纸面起伏。
- **Edge Detection（[Roberts Cross](https://en.wikipedia.org/wiki/Roberts_cross)）**：对 Scene Depth 在四个对角方向各采一次，两组对角差值的平方和开方就是边缘强度。比 Sobel 便宜（4 次采样 vs 9 次），但只对**斜边**敏感——对水彩描边正合适，因为水彩描边本来就要松散粗糙，没必要太精确。
- **White Vignette**：用扭曲后的坐标计算到 `(0.5, 0.5)` 的距离，`Smoothstep` 重映射后加到画面上、`Saturate` 截断——画面边缘自然变亮直到全白，模拟未被颜料覆盖的纸面。

最后用 `Lerp(image, black, edge_strength * 15)` 把边缘混成黑色描边线。

## Decal Shader：从 Scene Depth 重建世界位置

水彩斑点是「假 decal」：用一个 transparent cube 当贴花体，在 fragment 里**反推**屏幕背后真实物体的世界坐标，再变到 cube 的 object space 当作 UV。这是 [[scene-color-depth-nodes|Scene Color & Depth]] 文章里讲过的「从深度重建世界位置」技巧的应用：

```
fragmentDepth = Screen Position(Raw).w           // 当前 fragment 自己的 view-space 深度
ray = View Direction / fragmentDepth             // 归一化为「单位深度方向向量」（URP 下 View Direction 不归一化）
worldPos = Camera Position - ray * Scene Depth
```

然后 `Transform(worldPos, World → Object)` 拿到 object-space 坐标，`Multiply Object.Scale.x` 让噪声尺度跟世界尺寸一致而不是跟 cube 大小，再投影到 `xy` 平面采样噪声。最后用 `DDXY(distanceField)` / `fwidth` 抗锯齿一下边缘 alpha——这是从距离场拿到清晰像素边的标准技巧。

这种 decal 实现有几个限制：相机不能进入 cube（重建会失败），玩家走过会被穿透着色（如果 decal 体足够大），URP 下的 `View Direction` 必须非归一化（HDRP 默认归一化，要换成 `Camera Position - Absolute World Position`）。它不是工业 decal 系统，但作为美术效果非常够用。

## 这一篇的方法论价值

Cyan 这套水彩 shader 真正的教学价值在于**展示了一个完整美术效果如何拆成多个独立 shader 层叠加**。每层的概念都不复杂——光照 + 噪声 + 阴影 + 边缘检测 + 距离场 decal——但把它们组装成一个连贯的视觉语法需要清晰的分工：表面性质归 mesh shader、构图归后处理、点缀归 decal。这是技术美术做风格化效果的典型工作流。

## 相关

- [[blit-render-feature]]
- [[triplanar-mapping]]
- [[scene-color-depth-nodes]]
- [[diffuse-lighting-lambertian]]
- [[shaping-functions]]
- [[harry-alisavakis]]
- [[cyanilux]]

## Sources

- [[sources/cyan-watercolour-shader-experiments]]
