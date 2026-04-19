---
tags: [physics, astronomy, simulation, numerical-methods]
date: 2026-04-19
sources: 1
---

# N 体引力模拟

N 体引力模拟通过**数值积分** Newton 万有引力方程在每个时间步更新所有天体的位置与速度，取代 [[keplerian-orbits]] 的解析解。[[alan-zucconi]] 在 *Orbital Mechanics* 中把这一类方法称为「物理正确但数值敏感」——它是处理三体以上、摄动、接近碰撞等情形的唯一可行路线，但代价是长期稳定性差。

## 最朴素版：Euler 积分

对每对天体 (i,j) 计算引力 **F = G·mᵢ·mⱼ / r²** 沿连线方向，累加给 i，最后：

```
vᵢ ← vᵢ + (Fᵢ / mᵢ) · Δt
xᵢ ← xᵢ + vᵢ · Δt
```

这是显式 Euler，一阶精度，能量**单调漂移**——椭圆轨道会逐渐「展开」或「收缩」。在课堂 demo 里能跑，做任何严肃模拟都不够。

## Symplectic 积分器（辛积分）

保守系统（只有引力）的数值积分应当用辛积分器，它保持 Hamilton 结构，**能量在长期内有界振荡**而非单调漂移。最简单的是 **Leapfrog / Verlet**：

```
vᵢ ← vᵢ + (Fᵢ / mᵢ) · (Δt/2)
xᵢ ← xᵢ + vᵢ · Δt
重新计算 Fᵢ(new)
vᵢ ← vᵢ + (Fᵢ(new) / mᵢ) · (Δt/2)
```

二阶精度，计算量几乎和 Euler 相同，但椭圆轨道能精确闭合几百万步。*Children of a Dead Earth* 等硬核太空游戏都用 leapfrog 或更高阶的 Yoshida symplectic。

## 性能拓展

- **Barnes-Hut / FMM**——把远距离天体组按八叉树节点打包成近似单点，复杂度从 O(N²) 降到 O(N log N)；星系级仿真必备。
- **Self-gravity on GPU**——tile-based compute shader 每 thread block 做局部引力累加，和 [[tiled-light-culling]] 思路同构。
- **分离时间尺度**：近距快速相互作用用小 Δt，远场摄动用大 Δt；和渲染里的 LOD 思路一致。

## 与 Kepler 解析法的缝合

游戏里常见的 **patched conics**：默认每颗天体只受其母星引力，走精确 Kepler 椭圆；当进入另一颗天体的 SOI（Sphere of Influence），切换母星；真正跨 SOI 转折点或多体摄动强的区段才开数值 n-body。*Kerbal Space Program* 就是这一派的代表。

## 混沌与初值敏感

Ciechanowski 的三体沙盒让读者直观体会：两组只差 0.1 像素的初始速度，十步后轨迹完全分岔。这是 **Lyapunov 指数 > 0** 的典型表现——决定性 ≠ 可预测性。任何长期 n 体预测都必须附上误差带与「再过多久失效」的估计；这也是为什么天文学上把「月球会不会撞地球」这种问题只敢预测到几亿年尺度。

## Sources

- [[sources/alanzucconi-orbital-mechanics]]
- [[sources/ciechanow-moon]]
