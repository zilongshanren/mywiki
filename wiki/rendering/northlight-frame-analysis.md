---
tags: [渲染, 帧分析, 光线追踪, 去噪, hybrid-rendering, dlss, remedy, northlight]
date: 2026-04-27
sources: 1
---

# Northlight 引擎帧分析 — Control

[[people/alain-galvan|Alain Galvan]] 2021 年对 Remedy Entertainment 的 Control（2019）进行了帧级别分析，揭示了基于 **Northlight 引擎**的混合光追渲染管线实现细节。这是 [[rendering/hybrid-raytracing-pipeline|混合光追管线]]在商业 AAA 游戏中的典型案例。

## 渲染管线顺序

### 1. 初始化与加速结构

每帧开头构建场景的**加速数据结构（BVH）**，同时为 UI 元素生成纹理图集，并为场景中的灯光构建包围体层次（[[rendering/bvh-traversal-hardware|BVH]]）。

### 2. 阴影深度通道

渲染到一张 `16384×2048` 的**纹理图集**，每个光源占据 `512×512` 或 `256×256` 的子区域。Control 同时使用光栅化阴影**和**光追阴影——光追阴影专用于处理接触阴影（Contact Shadows），而非替换全部阴影。

### 3. 预通道（Prepass）

- 第一附件：视空间法线（`b` 通道编码边缘软化/接触边缘信息）
- 第二附件：次表面散射数据（`r` 通道）+ 粗糙度（`g` 通道）
- 专门的第二预通道处理小物体及倒角边缘效果

### 4. 速度通道

独立写入 `R16G16_FLOAT` 纹理，采用 NDC 空间速度编码，供 [[rendering/rt-denoising|时空重投影]]使用。

### 5. 光照通道（DispatchRays）

三路光追通道通过 `DispatchRays` 并行提交：

- **弯曲法线（Bent Normals）**：先通过 Compute `Dispatch` 计算
- **光追反射**：全分辨率，基于 GGX 镜面 BRDF，对远处或低粗糙度表面使用近似减少成本（[[Sjöholm et al. 2021]]）
- **光追全局光照（GI）**：半分辨率（`960×560`），结合预计算体素 GI（离线路径追踪静态物体）与近场 BRDF 间接漫反射
- **接触阴影**：`r` 通道为聚光灯索引，`g` 通道为点光索引

所有光追通道均使用 [[rendering/svgf|SVGF]] 的变体降噪，加入了"萤火虫滤波（Firefly Filter）"和基于 4 像素邻域的空间滤波。

### 6. 技术特效通道

- **敌人特效**：护盾 Overlay + 发光模糊
- **流体烟雾（Fluid Smoke）**：Northlight 的技术亮点——用 Compute 维护流体速度、散度、压力缓冲区，通过帧间反馈循环扭曲当前帧产生类似气体流动的屏幕空间效果（[[McAloon 2019]]）

### 7. DLSS 超分

DLSS 将 `1080p` 输入超分至 `4K`，使 2070 Super 在 4K 下平均帧率超过 30 fps。这是 [[rendering/rt-denoising|DLSS]]去噪 + 超采样结合的早期商业案例。

### 8. UI 与呈现

UI 使用 Coherent Labs 的 HTML5 游戏界面渲染器 **Gameface** 渲染，CPU 侧执行 DOM 驱动的绘图调用。

## 要点

Control 的渲染策略体现了混合光追的务实取向：光追只用于"最值得"的效果（反射、GI、接触阴影），其余仍走光栅化路径；SVGF 去噪虽有时域伪影，但在美术风格下几乎不可察觉，甚至与游戏的超自然氛围相融合。

## Sources

- [[sources/alain-frame-analysis-control]]
