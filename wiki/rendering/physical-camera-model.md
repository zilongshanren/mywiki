---
tags: [physical-camera, exposure, post-processing, stingray, ecs]
date: 2026-04-19
sources: 1
---

# 物理相机模型（Stingray）

物理相机指"用真实相机参数驱动渲染器"的相机实体：不是给美术一个 FOV 旋钮，而是暴露 **sensor size、ISO、shutter speed、focal length、focus range、aperture diameter** 这些摄影师熟悉的旋钮，让曝光、景深、FOV 的变化完全服从光学。这是 PBR 管线的收尾——在 [[physically-based-shading|material]] 与物理光（见 [[material-light-validation|material-light-validation]]）都对齐以后，如果相机还是老的 "非物理曝光 + 手调后处理"，整套链路就断在最后一环。

Stingray 在 2017 年把物理相机做成一个 **entity**，挂一堆 component：
- **Camera Body**：sensor 尺寸、ISO 档、快门档位
- **Camera Lens**：焦距、对焦距离、光圈档位
- Transform + Camera：常规 view-projection
- 一排 shading environment component：DOF、motion blur、bloom、vignette、film grain、色差——每个 post-effect 都用一个 component 表达其物理参数

一段 Lua 脚本 component *Physical Camera Properties Mapper* 监听所有参数变化，把物理值实时映射到各 post-effect 的实现参数。美术如果嫌物理 DOF 太受限，直接**删掉** DOF component 就回退到纯艺术 DOF——这是 [[ecs|ECS]] 表达力的漂亮用法。

两个核心映射：

**曝光**（沿用 Frostbite 那套）：
```
EV100 = log2(aperture² · 100 / (shutter · ISO))
max_luminance = 1.2 · 2^EV100
scene *= 1 / max_luminance
```

**FOV 受对焦距离影响**：标准 `2 · atan(h / 2f)` 只在对焦无穷远时对，真实镜头对焦时内部镜组移动改变有效焦距。Jp 用了个简单线性 offset——zoom 在 24mm 端对上了但 70mm 又不对，这一块他标为"未来工作"，本质上需要更严肃的 thick lens / 镜组光学模型。

**光强度单位踩的坑**：Stingray 最初让用户以流明（lumen，全角度总光通量）填写光强度，但 material shader 需要的是 **luminous intensity**（流明每立体角）。修复：`I = lumens / (2π · (1 - cos(½α)))`，其中 α 是光的张角。这对 spot light 的锥角越小影响越大。这种"单位看起来只差一个因子，结果差一个数量级"的陷阱是 PBR 管线反复翻车的点。

验证用了一个小型 **controlled light room**（思路来自 MGS5 / Fox Engine 的 conference room setup），在 Stingray 里复刻几何、白平衡到纯白，跟照片在线性空间做比较。初次对照 Stingray 偏暗就是靠这个排查出 lumen/cd 单位 bug。

## Sources

- [[sources/bitsquid-physical-cameras-stingray]]
