---
tags: [资源管线, blender, 欧拉角, 导出器, 坐标系, x-plane]
date: 2026-04-19
sources: 1
---

# Blender 的 "XYZ" 欧拉约定与 X-Plane OBJ 导出的顺序反转

Blender 在动画面板里把一个旋转标成 "XYZ Euler"——这三个字母的含义并不显而易见。[[ben-supnik|Supnik]] 在 2015 年给 X-Plane 的 Blender exporter 调试时留下一条极短的"备忘录式"帖子，把这套约定还原清楚，也顺便记下老 2.49 exporter 的历史 bug。

## "XYZ Euler" 的三条含义

1. **Z 轴是 up**（Y 轴指向远处以保持右手系）。这是 Blender 的世界坐标约定。
2. 每个角度**绕同名轴**旋转：X-rotation 绕 X 轴（对飞行员来说是 pitch up），Y-rotation 绕 Y 轴（roll），Z-rotation 绕 Z 轴（yaw）。
3. **三次旋转按 X → Y → Z 顺序、外旋（extrinsic）应用**——每一次都绕**全局**轴，不是前一次旋转后的局部轴。

外旋的关键推论：**最后施加的 Z 轴旋转不受前两次影响**（因为它绕全局 Z），而**先施加的 X 会被后面的 Y 和 Z 改变**。等价的理解是"先 X 再 Y 再 Z 的外旋"与"先 Z'' 再 Y' 再 X 的内旋"产生同一个最终姿态（顺序反转 + 内外旋对调）。

从飞行员习惯看，这相当于：先 yaw（global Z 不被后续改）、再 roll（被变换过的 Y'）、再 pitch（被变换过的 X''）——**pitch 放最后做**，和真实飞机操纵顺序完全不一样。所以 Supnik 说：想匹配 X-Plane 姿态语义，**Blender 里该选 YXZ**（让 roll 变成最低优先级、pitch 变成最先应用的），而不是 XYZ。这是给 Blender 2.75 用户的备忘。

## 导出到 X-Plane OBJ 的顺序问题

X-Plane 的动画模型只有 **局部变换**：OBJ 里一串 `ANIM_rotate` 按书写顺序应用，后一个作用于前一个的结果。因此 Blender 的全局 XYZ 必须**反向**写进 OBJ：

```
ANIM_rotate 0 0 1   # Z 先应用
ANIM_rotate 0 1 0   # 再 Y
ANIM_rotate 1 0 0   # 最后 X
```

Blender 的全局 X 因为"最先施加 + 最受后续影响"，在 X-Plane 的局部坐标里对应"最后施加 + 不被后续改变"——两种坐标语言把"先被施加但最易被扰动"与"最后施加且独立"这对偶关系换了个说法。

## Blender 2.49 Exporter 的历史 bug

Blender 2.49 强制使用 XYZ（没有 YXZ 选项）。当年 exporter 把旋转分解成 Eulers 的顺序**在 X-Plane 坐标系里执行**——即先算一个绕 X-Plane Z 的角度、再算 Y、再算 X。

这样的分解有一条恰好反过来的不变量：在 Blender 的 XYZ 里**yaw（Z）不变**；但老 exporter 的导出里，**roll（在 X-Plane 坐标下对应的那个轴）不变**。对动画师来说，这意味着"我在 Blender 里改了 yaw 曲线而导出后 roll 被保留了" 的诡异错位——改 Blender 数值、X-Plane 里看到的是被错误分配的分量。修复时必须把分解搬回原坐标系、让 Blender 的 XYZ 不变量与导出文件的轴序对齐。

## 教训

这条 bug 的通用启示：**Euler 分解只在"和它被施加时同一坐标系"里是无歧义的**。导出管线跨坐标系时——不管是 Y-up / Z-up、左右手、单位约定——要么先把旋转转成坐标无关的表达（矩阵或 [[3d-rotation-math|四元数]]），要么在同一坐标系里完成分解再做坐标系变换。在源坐标系里做 Euler 分解、直接把欧拉分量搬过去，几乎注定踩到 [[gimbal-lock-euler-interpolation|欧拉相关]] 的坑。

## 相关
- [[3d-rotation-math]]
- [[gimbal-lock-euler-interpolation]]
- [[exponential-map-rotations]]
- [[asset-exchange-format-strategy]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-blender-eulers-notepad]]
