---
tags: [渲染, 骨骼动画, vertex-shader, gpu, vbo, 矩阵调色板]
date: 2026-04-14
sources: 1
---

# GPU 蒙皮（矩阵调色板）

在可编程管线出现之前，骨骼动画的"蒙皮"——把网格顶点按骨骼变换重新放置——必须每帧在 CPU 上做完，再把整批顶点重新上传到 GPU。这意味着每帧都要传几千到几万个顶点。可编程 vertex shader 出现以后，蒙皮可以下沉到 GPU，**顶点数据只在加载时上传一次**，每帧只需要传一小束骨骼矩阵（"matrix palette"），整个模型就跟着动起来。这是早期 vertex shader 最经典的应用之一。

## 数据布局

顶点缓存里除了常规的位置、法线、UV，还要新增两条：

- `boneIndices : vec4` —— 影响该顶点的 4 根骨骼在 palette 里的下标。
- `boneWeights : vec4` —— 对应的 4 个权重，和为 1。

"4 根骨骼"是行业惯例：四个权重塞进一条 `vec4`，刚好填满一个 vertex attribute slot；绝大多数模型也用不到第五根。Jeremiah 在 MD5 demo 里直接 `assert(weightCount < 4)`。

## 矩阵调色板与 inverse bind pose

每帧要送上 GPU 的不是骨骼当前的世界变换，而是：

```
skinMatrix[i] = animatedBone[i] · inverseBindPose[i]
```

其中 `inverseBindPose[i]` 是这根骨骼在 [[md5-model-format|bind pose]] 下的全局变换的逆。

为什么乘逆？因为顶点存的是 **bind pose 下的位置**。先用 `inverseBindPose` 把它"撤回"到关节本地空间，再用 `animatedBone` 把它送到当前帧的位置。两步合一，既减少了 shader 里的乘法，也让动画数据可以在不同骨架尺寸的模型间复用——男角色、女角色绑同一套动画，只要骨架拓扑相同，各自的 inverse bind pose 会把动画"翻译"到自己的体型上。

如果一个动画只服务一个模型，可以离线把这两步预乘掉、按动画帧缓存，省掉运行时的乘法但要多花 `numBones × numFrames` 矩阵的内存。这是一个典型的 **算力 ↔ 内存** 折中。

## Vertex shader 里的混合

shader 端的核心一段大致是：

```cgfx
float4 skinPos =
    weights.x * mul(palette[indices.x], position) +
    weights.y * mul(palette[indices.y], position) +
    weights.z * mul(palette[indices.z], position) +
    weights.w * mul(palette[indices.w], position);
```

法线同样 mix（只取 3×3 子矩阵），然后做正常的 MVP 投影。Lighting 留到 fragment shader 做 per-pixel。

## 寄存器/Uniform 限制

老一代 vertex profile 限制非常严：vp30/arbvp1 只有 96 个 4-component constant，刚好 24 个 4×4 矩阵，远不够装下 58 块骨骼的 demo。Jeremiah 不得不切到 `vp40`/Cg 4.0 profile 才能塞进去。这也是为什么早期商业引擎要么压缩骨骼矩阵到 4×3，要么把 palette 拆成多个 draw call。今天的常见做法是把 palette 放进 **constant buffer / SSBO / texture buffer**，单次 draw 几百根骨骼也无压力——但当年这是一个真实的硬约束。

## CPU 蒙皮还要不要存在？

GPU 蒙皮虽然是默认选项，CPU 版本依然有用：服务器端的命中检测、用变换后的 mesh 做物理碰撞、以及——像 Jeremiah 在 demo 里那样——为了**调试可视化变换后的法线**而需要把结果读回。所以一个成熟的引擎里两种路径常常并存，由一个 enum 在运行时切换。

## 相关

- [[md5-model-format]] —— 教学示例使用的具体格式
- [[3d-rotation-math]] —— 关节方向用四元数存储
- [[mvp-transform]]
- [[fragment-shader]]
- [[draw-call]]
- [[jeremiah-van-oosten]]

## Sources

- [[sources/3dgep-md5-gpu-skinning]]
