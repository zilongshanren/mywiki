---
tags: [渲染, 头发, alpha-test, forward, deferred]
date: 2026-04-14
sources: 1
---

# 混合 Deferred/Forward 头发渲染

[[bartosz-wronski|Bart Wronski]] 在 CD Projekt Red 为 Witcher 3 / Cyberpunk 2077 原型期提出的一个小 trick：**用 alpha-tested 发丝条的传统头发资产**，在 [[deferred-rendering|deferred pipeline]] 里把头发拆成「大部分不透明 + 边缘半透明」两段处理，避开 deferred shading 与头发两个老大难的冲突。

## 头发在 deferred 里的两个痛点

1. **材质模型不匹配**。头发需要强各向异性高光，把这些材质参数硬塞进 G-Buffer 通常要靠分支 / material ID，vgpr 占用与指令数都被拖高，而头发在屏幕上往往只占很小一块面积——为一小撮像素付全屏成本很不划算。Witcher 2 的 hack 是用单一主光方向 + per-character cube-map 假装高光，只能靠美术师救场，远非 next-gen 方案。
2. **alpha 抗锯齿**。发丝条用 alpha test 必然产生锯齿；[[msaa-ssaa|MSAA]]、alpha-to-coverage、沿切线方向的屏幕空间模糊都只能部分缓解，真正干净的做法是 forward + OIT（如 AMD TressFX），但成本高。

## Wronski 提出的四步流程

所有 pass 共享同一个发丝 mesh，差别在 depth/alpha 状态：

1. **G-Buffer pass**：写入头发，**镜面关闭 / 镜面遮蔽拉满**。`Aref` 取接近 1 的大值（美术可调），alpha test 只留下**最实心**的那部分像素。这样 G-Buffer 里的头发只贡献漫反射项，不污染 specular 通道。
2. **标准 deferred 光照 pass**：正常跑，头发的 Lambertian diffuse 自动到位。
3. **Forward 高光补写 pass**：对头发再画一次，`ZTest = Equal`、**无 alpha blend**，alpha test 与第 1 步完全相同。这一次跑真正的各向异性头发 BRDF（或任何需要 forward 的模型），加到已有的 lighting buffer 上。`Equal` 保证零 overdraw。
4. **Forward 透明边缘 pass**：再画一次，反向 alpha test（`1 - Aref`）挑出前面被扔掉的半透明发梢；alpha blend 打开，alpha 从原 `[0, Aref]` remap 到 `[0, 1]`；深度按常规 less-equal 测试。这一 pass 顺便处理 albedo + 高光，与粒子/其他 transparent 复用排序规则。

## 优点与代价

- **无需污染 G-Buffer**，任意头发 BRDF 都可以用，分支 / vgpr 消耗留在头发 pixel 上。
- 绝大部分发丝写了 depth，与粒子/透明物体不会互相穿插；真正 alpha blend 的只剩边缘小块，排序问题大幅缓解。
- `ZTest = Equal` + 深度图早已建立，forward 高光 pass 没有 overdraw；后续透明 pass 的范围也很小。
- 代价是**头发走 3 个几何 pass**（3、4 可以合并但会失去若干优势），对 spline / tessellation 级别的复杂头发不合适——那种应该直接用 TressFX。
- 多 pass 也让 renderer pipeline 与调试更复杂。

## 今天还值不值得

Wronski 在 2020 年的后记里承认这条 trick「部分过时」：现代 GPU 对分支与 fat G-Buffer 容忍度更高，很多引擎干脆把头发特征打进更厚的 G-Buffer。但**把头发按「不透明 + 透明边缘」切成两段处理**的核心想法，在移动端 forward 引擎里至今仍是便宜有效的解法——移动端 OIT 成本高，mesh-based alpha test + blend 分离依然香。

## 同一篇的 SSS hack

文章后半还顺手记录了 Witcher 2 的皮肤 [[subsurface-scattering|SSS]] hack：G-Buffer 里皮肤 albedo 强制为白、specularity 强制为 0；光照 pass 里把**未调制**的 specular 响应额外写进 lighting buffer 的 alpha 通道（独立混合状态）；随后对皮肤像素跑 [Jimenez 的可分离 bilateral SSS blur](http://www.iryoku.com/sssss/)（stencil / G-Buffer bit 掩码），最后再画一次皮肤网格，用 blurred RGB × albedo 恢复漫反射、加回 specular。缺点是 lighting 对皮肤丢失色度——当年靠 per-environment 全局 specular 乘子救回。现代引擎应当直接分离 diffuse / specular lighting buffer，但思路仍然示范了**G-Buffer 的通道可以被「征用」来承载非材质数据**这条 hack 美学。

## 相关

- [[deferred-rendering]]
- [[deferred-alpha-lighting]]
- [[alpha-blending]]
- [[dither-alpha-clipping]]
- [[msaa-ssaa]]
- [[bartosz-wronski]]

## Sources

- [[sources/bartwronski-hair-rendering-tricks]]
