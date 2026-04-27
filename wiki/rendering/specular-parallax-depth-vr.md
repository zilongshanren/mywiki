---
tags: [vr, 立体渲染, 高光, 镜面反射, 视差, 深度感知]
date: 2026-04-27
sources: 1
---

# 高光的视差深度：镜面高光比表面更远

高光（specular highlight）所呈现的视差深度，与其所在表面的几何深度**并不相同**——高光看起来比表面更远。这是一个有光学理论依据的现象，在 VR 渲染中有重要意义。

## 物理直觉

想象一面镜子中自己的像：镜像看起来在镜面**后方**两倍距离处，而不是在镜面本身所在的位置。这是因为光线在镜面处发生了反射，视线的总光路长度加倍，双眼产生的视差也对应着这个更长的距离。

同样的道理适用于任何光泽表面（chrome、不锈钢、油腻的水龙头）上的高光：

- 高光是光源经过表面**反射**后映入眼睛的像
- 光路 = 光源 → 表面 → 眼睛，比"眼睛 → 表面"的单程距离更长
- 双目视差感知到的"深度"对应完整光路，而非几何距离

因此，高光在双眼视差意义上比它所在的表面**更远**，两者的视差偏移量不同。

## VR 渲染中的正确做法

[[ben-supnik|Supnik]] 在实现 X-Plane VR 时，对左右眼分别进行了独立的逐像素光照计算：每只眼使用各自的相机原点（camera origin）、变换矩阵和光照向量。最初他担心两眼之间的"不一致"会造成视觉错误，但实际上从未出现问题。

事后他意识到原因：**两眼之间的光照"不一致"本身就是正确的信息**——它编码了高光相对于表面的额外深度偏移，是大脑用来感知高光"更远"的深度线索。如果把两眼的高光位置强行对齐到相同的表面深度，反而会失去这个深度感知信号，看上去"假"。

## 实现要点

```
左眼 fragment shader:
    light_vec = normalize(light_pos - eye_left_origin)  // 用左眼原点
    specular = pow(dot(reflect(-light_vec, N), V_left), roughness)

右眼 fragment shader:
    light_vec = normalize(light_pos - eye_right_origin)  // 用右眼原点
    specular = pow(dot(reflect(-light_vec, N), V_right), roughness)
```

即使光源是方向光（directional light），也应该在逐像素层面使用各自眼睛的视点向量（V），确保高光位置在两眼之间产生合理的横向偏移。

## 与立体渲染的关系

这个现象揭示了立体渲染中一个常被忽视的细节：[[stereoscopic-3d-design|立体渲染]] 的正确性不只在于几何视差，**光照计算也必须是每眼独立的**才能还原正确的深度线索。依赖单眼渲染结果加视差偏移（reprojection 类方案）来生成另一眼画面，会在高光位置产生不正确的视差深度感。

## 相关

- [[stereoscopic-3d-design]] — 立体 3D 渲染通论
- [[stereo-reprojection-hole-fill]] — reprojection 方案及其局限
- [[physically-based-shading]] — 微面元 BRDF 与高光模型
- [[coordinate-spaces]] — 各眼独立变换矩阵的空间管理
- [[ben-supnik]]

## Sources

- [[sources/supnik-specular-depth-separation]]
