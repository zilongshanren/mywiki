---
tags: [source, rendering, physical-camera, exposure, stingray, entity-system]
date: 2026-04-19
sources: 1
---

# Physical Cameras in Stingray（Jp & Olivier Dionne）

Bitsquid / Stingray 博客 2017-09-28，作者 **Jp（Jean-Philippe Guertin）与 Olivier Dionne**。这是 Jp 在 Stingray 博客的最后一篇——Stingray 在 2018 年被 Autodesk 停更。物理相机是 Stingray PBR 三阶段（material → light → camera）的收尾之作。

## 摘要

"物理相机"即一个用真实相机参数（sensor size、ISO、shutter speed、focal length、focus range、aperture range）驱动的 entity——Stingray 继续用数据导向 entity-component 架构把它表达成一堆 component：**Camera Body**（sensor + ISO + 快门档位）、**Camera Lens**（焦距 + 对焦距离 + 光圈档位）、transform + camera（view projection matrix）、以及一堆 shading environment component（DOF、motion blur、vignette、bloom、色差等每个 post effect 都挂一个）。一个叫 *Physical Camera Properties Mapper* 的 Lua 脚本 component 在任何参数改动时重算映射。美术如果不爽物理正确的 DOF，就把 Depth Of Field component 从 entity 删掉，就回到纯艺术 DOF。

两个核心映射。**Exposure**：按 Frostbite PBR 那套公式 `EV100 = log2(aperture² · 100 / (shutter · ISO))`，再得 `max_luminance = 1.2 · 2^EV100`，场景乘以 `1/max_luminance`。**FOV**：标准 `2·atan(h/2f)` 只在对焦无穷远时正确，Fox Engine (MGS5) 提醒过 focus 距离会改变有效焦距——Jp 加了个简单的线性映射 `focal_length_offset = lerp(0, 1, normalized_focus)`，zoom 镜头到 24mm 对齐了，到 70mm 又不对，这一块留作未来工作。

验证用了一个自建的"小型控制光室"对照真实照片——结果第一次对出来 Stingray 太暗。查出来是光强度单位用错：Stingray 让用户以流明（lumen）填写强度，但 material shader 需要的是 luminous intensity（流明每立体角），转换公式 `candela = lumens / (2π · (1 - cos(½α)))`。改对后 point / spot 能对上，directional light 后续改用 lux + disk 角径描述。

## 关键要点

- **相机作为 entity**：sensor、lens、所有 post-effect 都是可插拔 component——美术可以直接 "扔掉" 某个 component 关掉其物理映射，保留其他 effect。ECS 的表达力在复杂对象上体现得很充分。
- **exposure pipeline** 完全复用了 Frostbite 的 EV100 公式，没有重新发明。
- **focus 影响 FOV** 是老生常谈但工程界少认真处理——Jp 的线性 offset 是实用但不完全正确的第一步。
- **单位陷阱**：lumens（全角度总光通量）vs luminous intensity（每立体角）——这是早期 PBR 管线反复踩的坑，光圈角越小影响越大。
- **控制光室对照法** 是最后一块拼图：离线渲染器验过算法，真光室验单位和管线一致性。

## 链接到的概念

- [[physical-camera-model]]
- [[material-light-validation]]
- [[ecs]]

## 原文

- 链接：https://bitsquid.blogspot.com/2017/09/physical-cameras-in-stingray.html
- 本地：`raw/articles/bitsquid.blogspot.com/2017-09-28_physical-cameras-in-stingray.md`
