---
tags: [source, 渲染, 光照, 延迟渲染, 剔除]
date: 2026-04-14
sources: 1
---

# Tiled Light Culling（Brian Karis / Graphic Rants）

[[brian-karis|Brian Karis]] 2012 年 4 月 29 日发表在 Graphic Rants。本是 Prey 2 的 GDC 2012 演讲内容（被迫取消）的一部分延伸思考——主题是：在 tiled deferred / tiled forward 的 per-tile 光源剔除里，**如何把 specular 的方向性和光泽度也纳入剔除判据**。

## 摘要

主流 tile 光照剔除只做 sphere-vs-frustum，这依赖于「光源半径」这个人为构造——物理正确的 $1/d^2$ 没有零点。Karis 先用一节清理了**物理光衰减**的基本公式：球形/圆盘光源的 $r^2/d^2$ 和 $r^2/(r^2+d^2)$——当单位用 lumen 时 $r^2$ 被 fold 进光强常数，才化简为我们熟悉的 $1/d^2$——顺带解释了「把灯嵌进地面会让计算崩掉」的道理。然后引入**容差剔除** $\max(0, 1/d^2 - \text{tol})$。关键观察：能量守恒的 specular 峰值远高于 Lambert，**diffuse 的剔除距离和 specular 的剔除距离差好几个数量级**。但正因为能量守恒——**高光泽度光源作用距离远、但影响的立体角很小**（chrome 球反射一根远处蜡烛只占一像素），所以 tile 级可以构造一个**specular cone**（类似 normal cone）把 tile 内所有 pixel 的反射向量 $R$ union 起来，用方向约束追加剔除。Phong 形式下锥角给出解析解 $\arccos(\text{tol}^{1/n})$。最后 Karis 说他在 Prey 2 当前世代实际做法是把 artist 设定半径外的 diffuse 烘进 lightmap、specular 烘进 env map——这个新想法希望用 runtime 剔除替掉那种「slop」。

## 关键要点

- **物理光衰减**：sphere $r^2/d^2$，disk $r^2/(r^2+d^2)$；单位是 lumen 时 $r^2$ 化简为 1。**不要让表面穿透光源形状**。
- **$1/d^2$ 的工程截断**：减常数 max 0（整域失能量）vs 距离窗口函数（仅远端失能量）。
- **diffuse 和 specular 的剔除距离差异**：用统一 radius 等于浪费 diffuse 的剔除机会。
- **关键洞见**：能量守恒让 specular 的「峰值 × 作用立体角」近似常数——**作用距离长就意味着作用方向窄**。
- **Specular cone 剔除**：tile 内 $R$ 向量的锥 union + $\arccos(\text{tol}^{1/n})$ 的锥角，和 normal cone 做 backface 剔除是同构思路。
- **工程细节**：$(n+2)/2$ 因子卷进距离衰减而不是角度门槛；spec 距离锥和影响球同时缩放；**不分两份光源列表**，而是 diffuse **或** spec 过关都保留。
- **Prey 2 当前世代做法**：artist 半径 + 远场烘焙（diffuse → lightmap，specular → env map）是他希望替掉的现状。
- 评论区 Stephen Hill 提出「bumpy 高频内容会让 cone union 退化」的担忧——Karis 回答：specular AA 把高频 bump 转成低光泽 case，正好化解问题；唯一反例是刚好一个 tile 大小频率的 bump。

## 链接到的概念

- [[tiled-light-culling]]
- [[tiled-light-prepass]]
- [[microfacet-brdf]]
- [[physically-based-shading]]
- [[deferred-rendering]]
- [[culling]]
- [[brian-karis]]

## 原文

- 链接：http://graphicrants.blogspot.com/2012/04/tiled-light-culling.html
- 本地：`raw/articles/graphicrants.blogspot.com/2012-04-29_tiled-light-culling.md`
- 参考 [1]: Andersson/Lauritzen, Intel tiled deferred
- 参考 [2]: Christina Coffin, SPU Deferred Shading in Battlefield 3
- 参考 [3]: Aras Pranckevicius, Tiled Forward Shading links (2012)
- 参考 [4]: iq sphereao — analytic sphere/disk falloff
