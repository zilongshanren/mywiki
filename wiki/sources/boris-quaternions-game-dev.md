---
tags: [source, game-development, math, quaternion, rotation]
date: 2026-04-27
sources: 1
---

# Everything You Need to Know About Quaternions for Game Development（Boris The Brave）

[[people/boris-the-brave]] 发表于 2022 年 12 月的短文，论点极简：四元数本质是 3D 旋转的表示，游戏开发者不需要理解其数学本质，只需掌握五到十个有几何意义的 API 函数即可。

## 摘要

文章用一个尖锐的前提开篇——「四元数就是旋转，这就是全文」——然后展示游戏实践中真正需要的操作：乘法（组合旋转或变换向量）、逆（求反向旋转）、Slerp（插值，用于动画）、LookRotation、AngleAxis 等。作者以 Unity API 举例，但指出这些函数在主流引擎/语言中普遍存在。核心建议是：把四元数当黑盒，按几何语义操作；避免直接操作 xyzw 分量；用 AngleAxis + 乘法代替修改 eulerAngles.x 这类陷阱写法。

## 关键要点

- 四元数比 3×3 旋转矩阵更高效（4 个数 vs 9 个数），行为等价
- `q1 * q2`：先应用 q2 再应用 q1；左乘 = 世界轴旋转，右乘 = 局部轴旋转
- 直接修改 `eulerAngles.x` 会引入轴顺序歧义；AngleAxis + 乘法语义清晰
- Slerp 是平滑姿态过渡的标准工具，配合 LookRotation 可实现追踪摄像机
- 不需要了解四元数的代数理论，库函数已封装所有数学

## 链接到的概念

- [[game-development/quaternion-for-games]]
- [[rendering/3d-rotation-math]]
- [[rendering/gimbal-lock-euler-interpolation]]

## 原文

- 链接：https://www.boristhebrave.com/2022/12/12/everything-you-need-to-know-about-quaternions-for-game-development/
- 本地：`raw/articles/boristhebrave.com/2022-12-12_everything-you-need-to-know-about-quaternions-for-game-devel.md`
