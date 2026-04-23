---
tags: [渲染, 交互, 拾取, mouse-picking, 坐标空间, 裁剪]
date: 2026-04-19
sources: 1
---

# 鼠标拾取的三种坐标空间与近裁剪面陷阱

[[ben-supnik|Supnik]] 2013-10 *3-d Mouse Testing* 是他修完 BrickSmith 剔除代码一个长期 bug 后写的**三种 hit-test 坐标空间的对照**——一条很实用的笔记，因为 3D 编辑器 / 关卡编辑器的 pick 通常是新手 3D 程序员落地自己写 raycast 的第一次，每种空间都会踩到一套特定的坑。

## 方案 A：Modelview Space

最朴素：把鼠标点当作 NDC 里一条 Z=-1 到 Z=1 的射线，用 `(MV × P)⁻¹` 把射线变回 modelview 空间；每个被测试三角形**正向**变换到 modelview 空间；然后跑 [Möller-Trumbore](https://en.wikipedia.org/wiki/Möller–Trumbore_intersection_algorithm) 射线-三角形相交。

优点：

- 深度值从算法副产出，**hit sorting** 免费。
- 正向变换三角形，不需要**求逆**——LDraw 的 sub-transform 是任意 4×3 矩阵，避免真逆是一笔节省。
- 编辑器可以持续修改模型，不需要缓存任何"帮手数据"。

缺点：**没有剔除、没有 early-out，一次 hit test 扫全模型**，慢。

## 方案 B：Screen Space

Supnik 改写 BrickSmith 时走的路，目的是让 marquee 选择便宜、让**层级 AABB 剔除**能起作用：

- Point query / AABB query 都在 NDC 里表达，返回的 depth 也是 NDC [-1, 1]。
- 三角形**正向变换到 clip 空间 + 透视除法**后，得到的是 2D 图元。
- 2D AABB test 便宜到像白给。

更重要的是：**把模型的层级 bounds 也变换到屏幕空间后，对 sub-model 容器做 AABB cull 几乎不要钱**。一个 MPD 模型里大多数 sub-model 落屏外直接拒——即便整张大模型在屏幕上，一次鼠标点也能把**周围一大片**的三角形在第一层剔掉。对于大模型**单 pick** 比方案 A 快 10–50 倍。

## 方案 B 的坑：近裁剪面

到这里 Supnik 很得意。直到他给 BrickSmith 加了**"walk-through" camera**——让用户走进自己造的模块化建筑里转——帧率掉了，而且**模型局部会随机消失**。

他说：数学你怎么算都对，问题是**缺了 clip**。

GPU 渲染时，GPU 自己会在近裁剪面前面把几何裁掉；**他的 CPU 侧 hit-test 代码没做这一步**。标准 `glFrustum` 之后，在齐次 clip 空间里，-Z 变成 W，成为最终 NDC 坐标的除数；X、Y 已经乘过 near：

- **在近裁剪面上**：几何不变尺寸——一个整齐的 2D 坐标系。
- **在近裁剪面后**：越远越小（正常）。
- **在近裁剪面前**：尺寸**迅速暴涨**，因为在除一个分数 Z。
- **Z = 0**：除零，场面很激动。
- **在摄像机后方**：W 被提前取负以让后半渲染正常运转，所以分母变负 ⇒ X、Y 整个**左右镜像**。

**消失 bug 的机制**：一个 AABB 在 view-space 里跨 Z=0——比如前半在屏幕左边前方、后半在屏幕右边后方（45° 穿心角），投影后"摄像机后方的那一半"被镜像到屏幕左边，结果整个 AABB 看起来**全在屏幕左侧**，屏幕 AABB cull 直接把它丢了。

长而细的模型 + 沿长轴 45° 穿行，这种 AABB 翻转**每次 pan 相机都会发生**。

## 修复：clip-space 裁剪后再做透视除法

Supnik 的修：在透视除法**之前**，先把 triangles / AABB 用 clip-space 的近裁剪面做标准裁剪。

- AABB 当成立方体 + 12 条边 → clip 后重新包 AABB（点集可能多于 8 个不要紧）。
- 三角形 clip 后变 0 / 1 / 2 个新三角形。

"蠢但有效"是他的原话。

## 方案 C：Eye Space 或 Homogeneous

他列了两个没时间写的备选：

- **Eye space + 平面侧性测试**：X-Plane 的 culling 就是这么做的，点对平面的判别廉价且不需要裁剪；ray-triangle 可以在模型自身坐标系做（X-Plane 的 sub-transform 都是简单旋转 / 平移，求逆便宜，所以反过来把 ray 变到 model 空间反而最省）。
- **齐次坐标里直接做 ray-triangle**：理论上可以不先透视除法、在 clip 空间直接解交点，再把交点的 Z/W 检查是否在近面后——把"清洗几何"这一步压缩成交点一次性判别。Supnik 自己说不确定这条是否数学上成立。

## 一条可带走的启发

**"在哪个空间做 pick"没有普适答案**：编辑器是否会让用户进入模型内部、模型的层级 bounds 是否密集、sub-transform 是否容易求逆、是否需要 hit depth 排序，每一条都会把答案从 A 推到 B 推到 C。Supnik 的 bug 不是算错了数学，而是**在 walk-through 相机开启之前，屏幕空间方案所需的"模型永远在近面之后"前提悄悄失效了**——这种"抽象的泄漏"是坐标空间选型最容易忽略的成本项。

## 相关

- [[coordinate-spaces]]
- [[ray-casting]]
- [[culling]]
- [[occlusion-culling]]
- [[screen-space-curve-tessellation-cutoff]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-3d-mouse-testing]]
