---
tags: [渲染, 骨骼动画, 模型格式, md5, doom3]
date: 2026-04-14
sources: 2
---

# MD5 模型格式

MD5 是 id Software 为 *Doom 3* 开发的骨骼动画模型格式，**纯文本**、易读、好上手，是早期游戏程序员学习蒙皮动画时事实上的标准教学素材。一个完整的 MD5 资产由两类文件组成：`.md5mesh` 描述几何与骨架绑定，`.md5anim` 描述一段动画。两个文件的关节数量与名字必须一致才算合法配对。

## .md5mesh：几何 + 绑定骨架

`.md5mesh` 文件包含三部分：

- **header**：`MD5Version`（教程里始终是 10）、`commandline`、`numJoints`、`numMeshes`。
- **joints 段**：定义骨架的 *bind pose*。每个关节一行，含名字、父关节索引（根关节为 -1）、对象局部空间中的位置 `(x y z)`，以及一个**只存了 xyz 三分量**的方向四元数。`w` 分量在加载时由 `w = -sqrt(1 - x² - y² - z²)` 现算补回，是 MD5 的标志性细节。
- **mesh 段**（每个子网格一段）：`shader` 给出贴图路径；然后是 `verts`、`tris`、`weights` 三个数组。

MD5 的 vertex 不直接存位置，而是存 `(uv, startWeight, weightCount)`——位置由若干 *weight* 累加得到。每个 *weight* 写明：`jointID`、`bias`（权重）、以及在**该关节局部空间中的位移**。最终顶点位置的公式是：

```
finalPos = Σ joint.pos + (joint.orient · weight.pos) × weight.bias
```

也就是把每个 weight 从关节本地空间用关节的旋转/位移搬到对象空间，再按 bias 加权求和。这也意味着 MD5 的"权重"和别的格式的"骨权重"语义略有不同——它绑定的是一个**位置**而不是一个**绑定姿态下的顶点**。

## .md5anim：每帧的姿态曲线

动画文件由 `header`、`hierarchy`、`bounds`、`baseframe`、若干 `frame` 组成：

- **hierarchy**：列出骨架中的关节及一个 `flags` 位掩码，flags 决定该关节的 6 个自由度（3 位置 + 3 旋转）中哪些会被这帧动画覆盖，未覆盖的从 `baseframe` 取。`startIndex` 指向该帧 frame data 数组里属于本关节的首个 float。
- **bounds**：每帧的对象空间 AABB。
- **baseframe**：每个关节的"默认相对父关节"位置/方向，作为 frame data 中缺失分量的回退值。
- **frame N { float… }**：该帧所有"被动画驱动的分量"展平后的浮点数组，长度为 `numAnimatedComponents`。

加载器解释一帧时，对每个关节按 `flags` 从 baseframe 拷贝 6 个分量，再按 flags 从 frame data 覆盖被驱动的分量，重算四元数 `w`，最后**乘上父关节的变换**得到对象空间中的最终骨架。

## 为什么仍然值得讲

MD5 在工业界早被 glTF / FBX 取代，但作为**教学格式**它有几个不可替代的优点：纯文本可以肉眼 diff；显式区分 bind pose / animation；权重—关节—位置的关系直白到可以手算；并且配合 *Doom 3* 当年开源的资源，永远能跑起一个会动的模型。后续讨论 [[gpu-skinning-matrix-palette|GPU skinning]] 时几乎所有教程都默认用 MD5 演示。

## 相关

- [[gpu-skinning-matrix-palette]] —— 把 MD5 的骨骼变换搬到 vertex shader
- [[3d-rotation-math]] —— 四元数为何能省一个分量
- [[mvp-transform]]
- [[jeremiah-van-oosten]]

## Sources

- [[sources/3dgep-md5-loading-animating]]
- [[sources/3dgep-md5-gpu-skinning]]
