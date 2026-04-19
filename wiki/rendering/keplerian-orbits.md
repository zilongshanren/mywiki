---
tags: [physics, astronomy, math, simulation]
date: 2026-04-19
sources: 2
---

# Kepler 轨道与两体问题

Kepler 轨道是两体引力问题的闭式解：两个点状天体在相互引力作用下，各自沿**圆锥曲线**（椭圆/抛物/双曲）绕共同质心运动。本页用于归拢 [[bartosz-ciechanowski]] 的 *Moon* 和 [[alan-zucconi]] 的 *Orbital Mechanics* 两篇长文——前者偏物理直觉与地月案例，后者偏完整数学推导与模拟工程。

## Kepler 三定律

1. **轨道形状**：每颗行星沿椭圆轨道运动，太阳位于椭圆的一个焦点。
2. **等面积定律**：连接太阳与行星的矢径在相等时间扫过相等面积（等价于角动量守恒）。
3. **周期—半长轴律**：轨道周期的平方正比于半长轴的立方（T² ∝ a³）。

这三条来自 Newton 万有引力 **F = G·m₁·m₂ / r²** + 第二定律的闭式积分。Ciechanowski 在沙盒里让读者拖动初始速度，看同一个天体在速度不足、恰当、过大时如何分别绘出椭圆、抛物、双曲轨迹。

## 轨道元素（Orbital Elements）

描述一个 3D Kepler 轨道需要 6 个独立参数（也刚好是初始位置 + 速度的自由度）：

- **半长轴 a**、**偏心率 e**——形状与大小；
- **倾角 i**、**升交点经度 Ω**——轨道平面相对参考平面的朝向；
- **近点幅角 ω**——椭圆长轴在轨道面内的朝向；
- **真近点角 ν** 或**平近点角 M**——物体此刻在轨道上的位置。

Zucconi 的文章强调：从 M（时间的线性函数）推到 ν（几何角度）要解 **Kepler 方程** M = E − e·sin(E)——这是一个**超越方程**，没有初等闭式解，工程上用 Newton 迭代求根；这就是为什么「两体可解」并不等于「两体能算」。

## 为什么三体不可积

两体 12 个自由度 − 10 个守恒量（线动量 3、角动量 3、质心 3、能量 1）= 2 自由度；再通过把问题分解成「各自绕质心」把 12 维问题拆成两个 6 维，可解。三体 18 个自由度 − 10 个守恒量 = 8 个残余自由度，不再被守恒量「锁住」，出现 Poincaré 混沌。Ciechanowski 的两体 sandbox 扩充到三体之后立即失去可预测性——这是小球们「看起来一切都在守规矩但下一秒谁也说不准」的物理来源。

## 与 n 体数值仿真的分工

- **Kepler 轨道**（本页）——精确、廉价、长期稳定，适合**确定性强**的两体近似（行星绕恒星、卫星绕行星）。代价是叠加引力摄动时要手动加 correction。
- **[[n-body-gravity-simulation]]**——直接数值积分 F=ma，可处理任意体数、碰撞、非点状天体，但积分误差随时间累积，长期漂移明显。

游戏里 *Kerbal Space Program* 的 patched conics、*Children of a Dead Earth*、*Outer Wilds* 都在这两种做法之间做工程取舍——近轨用 Kepler 解析、远场摄动用 n-body、在 SOI（Sphere of Influence）切换时缝合。

## 相关

- [[n-body-gravity-simulation]]
- [[moon-phases-tides]]

## Sources

- [[sources/ciechanow-moon]]
- [[sources/alanzucconi-orbital-mechanics]]
