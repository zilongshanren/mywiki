---
tags: [math, rotation, quaternion, game-development, animation]
date: 2026-04-27
sources: 1
---

# 四元数在游戏开发中的实用指南

四元数是 3D 旋转的一种数学表示，使用 4 个浮点数（相比旋转矩阵的 9 个）。游戏开发者无需理解其代数理论，只需掌握一组具有清晰几何意义的 API 函数。这与[[rendering/3d-rotation-math|3D 旋转的多种数学形式]]中的理论视角互补——这里关注的是实际用法而非推导。

## 核心操作

四元数几乎所有有用的操作都可以归结为以下几类：

**旋转向量** `q * v`：将向量 v 按四元数 q 所表示的旋转变换。

**组合旋转** `q1 * q2`：先应用 q2，再应用 q1，等价于 `(q1 * q2) * v == q1 * (q2 * v)`。乘法不满足交换律，顺序决定语义：
- 左乘（`newRot * object.rotation`）——绕**世界坐标轴**旋转
- 右乘（`object.rotation * newRot`）——绕**物体局部轴**旋转

**逆旋转** `q.Inverse`：撤销 q 的旋转，`q * q.Inverse == identity`。

**插值** `Slerp(q1, q2, t)`：在两个旋转之间球面线性插值，用于动画平滑过渡，是欧拉角线性插值的正确替代方案。

## 常用构造函数

| 函数 | 含义 |
|---|---|
| `AngleAxis(angle, axis)` | 绕指定轴旋转指定角度 |
| `LookRotation(forward, up)` | 使 +Z 朝向 forward，+Y 尽量对齐 up |
| `FromToRotation(from, to)` | 从向量 from 旋转到 to 的最短路径 |
| `identity` | 无旋转 |

## 常见陷阱

直接修改 `eulerAngles.x` 是典型的错误用法：欧拉角在内部有轴顺序，单独改一轴会引入其他轴的隐式变化，导致行为不符合预期。正确做法是用 AngleAxis + 乘法明确语义：

```csharp
// 绕全局 X 轴旋转：
object.rotation = Quaternion.AngleAxis(myAngle, Vector3.right) * object.rotation;
// 绕局部 X 轴旋转：
object.rotation = object.rotation * Quaternion.AngleAxis(myAngle, Vector3.right);
```

不要直接读写四元数的 x、y、z、w 分量——这些数值没有直观的几何意义，手动修改几乎必然产生非单位四元数（旋转表示失效）。

## 与旋转矩阵的关系

四元数与 3×3 旋转矩阵在表示能力上等价，可以互相转换。矩阵在批量变换顶点时更高效（GPU 天然支持），而四元数在存储、插值和组合上更紧凑。实际引擎通常内部用四元数做存储与插值，在需要变换顶点时转成矩阵。无 [[rendering/gimbal-lock-euler-interpolation|Gimbal Lock]] 是四元数相对欧拉角的决定性优势。

## Sources

- [[sources/boris-quaternions-game-dev]]
