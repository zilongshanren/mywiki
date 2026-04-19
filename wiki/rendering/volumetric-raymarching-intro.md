---
tags: [渲染, shader, 体积渲染, raymarching, sdf, unity]
date: 2026-04-14
sources: 1
---

# 体积 Raycasting 与 Raymarching 入门

传统 3D 引擎的几何都是**空壳**：无论是球还是立方体，GPU 只渲染三角形组成的外表面，shader 的所有计算都停在那个外壳上。这是 3D 渲染流水线的一个硬性约定：对每个像素，只算"相机射线第一次命中表面那个点"的颜色。

很多现实中的视觉效果——雾、烟、水、玻璃、等离子体球、Plasma Globe——需要光在**体积内部**传播、散射、吸收。要实现这些就必须"欺骗" shader：让 fragment shader 返回的颜色不再只反映外壳几何，而是**沿相机射线对内部体积做积分**得到的值。[[alan-zucconi|Alan Zucconi]] 的 Volumetric Rendering 系列用 Unity Surface Shader 教了最基础的这一跳。

## 把外壳当作 Portal

整个套路的关键观念是：**外层几何只是入口**。你在 Unity 里放一个 cube，用自定义 shader 覆盖它；shader 并不一定要把它画成立方体——它可以在 fragment 阶段自己决定"从相机到这个像素的射线上，体积里有没有东西"。

在 fragment shader 里最终要的是两样东西：

1. **worldPosition** — 这个像素在世界空间里的起点（就是外壳上那个被击中的点）。
2. **viewDirection** — 从相机指向 worldPosition 的射线方向，归一化。

两者都很容易拿到：

```hlsl
// vertex
o.wPos = mul(_Object2World, v.vertex).xyz;
// fragment
float3 viewDirection = normalize(i.wPos - _WorldSpaceCameraPos);
```

## 从 raycasting 到 raymarching

"这条射线有没有击中虚拟球体" 这个问题有两种解法：

- **Analytic raycasting**：解析地求相机射线和球的交点（一元二次方程）。精确但**只能针对能写出闭式解的几何**——任意 SDF 就没法做。
- **Volumetric raymarching**：**沿射线走离散的小步**，每步询问"当前点在不在体积里"。只要 `inside(p)` 函数能写出来，raymarching 就能处理任意形状。

教程里最简单的版本用**固定步长**：

```hlsl
#define STEPS 64
#define STEP_SIZE 0.01

bool raymarchHit (float3 position, float3 direction) {
    for (int i = 0; i < STEPS; ++i) {
        if (sphereHit(position)) return true;
        position += direction * STEP_SIZE;
    }
    return false;
}

bool sphereHit (float3 p) {
    return distance(p, _Centre) < _Radius;
}
```

这条路线的代价是极其浪费——绝大多数步都落在空白处。下一步就是用 **distance-aided raymarching**（a.k.a. sphere tracing）：让 SDF 函数返回当前点到最近表面的距离 `d`，步长直接取 `d`，保证永远不会跨越物体。这是 Inigo Quilez / Shadertoy 生态最常见的 ray marching 形式。

## 为什么用 cube 当外壳

raymarching 需要先进入体积，而进入体积的唯一方式是**让相机射线先击中某个真实三角形**触发 fragment shader。Quad 只能从一面看、sphere 浪费三角形，cube 是最省力的选择：六面都能触发 shader、从任何角度都能让 ray 进入。真正的"内部形状"完全由 shader 里 `sceneSDF` 函数决定，和外壳几何无关——外壳纯粹是 fragment shader 的发射触发器。

## 和其他体积技术的分野

- **[[volumetric-fog-froxels|Volumetric fog via froxels]]**：走 compute + 3D 纹理，把相机视锥离散化成 voxel 网格，光照收集在 compute pass 里完成，fragment 阶段只做三线性采样。适合"雾 + 动态光"的全场景效果。
- **本文的 per-fragment raymarching**：走 surface/fragment shader + 64 步循环，每像素独立计算。适合单个体积物体（plasma 球、烟雾 blob、体积云）或 Shadertoy 风格的 demoscene。

两者不是竞品而是定位不同：froxel 是"所有像素共享一份 3D 光照数据"的摊薄方案，per-fragment raymarching 是"每个像素独立沿射线积分"的原教旨方案。

## 相关
- [[sdf-ray-marched-shadows]] — 把 raymarching 用在 2D / 3D 阴影
- [[sdf-2d-primitives]] — SDF 基元工具箱
- [[volumetric-fog-froxels]] — 另一条体积渲染路线
- [[fragment-shader]]
- [[coordinate-spaces]]
- [[alan-zucconi]]
- [[raymarching-intro]] —— sphere-traced 表面 raymarching 的入门路线
- [[density-field-volumetric]] — 密度场 + 样本累积的体积渲染

## Sources

- [[sources/alanzucconi-volumetric-rendering]]
