---
tags: [source, bitsquid, 资源系统, 平台差异, 本地化]
date: 2026-04-19
sources: 1
---

# Platform Specific Resources（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 12 月的文章，讲 Bitsquid 资源系统怎么用一套 property 机制同时吃掉平台差异、本地化变体、以及任意业务维度的变体。

## 摘要

资源由路径派生的 name+type 标识，name 被哈希成 64 位整数——运行期只认哈希。**Property** 是文件名里 type 之前的点分字符串段，表示"同一资源的变体"。两大类：**platform**（x360、ps3、android、win32）和 **language**（en、fr、jp）。由于所有资源统一走这套机制，Lua 脚本也能按平台分叉——`PlayerController.android.lua`。Property 可以由开发者任意造：`bullet_hit.noblood.particle_effect`、`foilage.withkittens.texture`。关键设计是**解析时机分离**：platform property 在**数据编译期**解析，编 PS3 时只打包 ps3 变体（若没有 ps3 变体则打包所有无平台标签的）；其余 property 全部打进运行期数据，运行期由游戏设置 **property preference order** 按优先级展开查找，比如 `{withkittens, noblood, fr}` 会生成 `buttons.withkittens.noblood.fr.texture` → `buttons.withkittens.noblood.texture` → …… → `buttons.texture` 的降级序列。在此框架上扩展"跨平台预览"只需要允许编译器用**一个平台**解析 property、用**另一个平台**写出 runtime 格式——编辑器就可以在 PC 上跑但呈现掌机下的资源形态。

## 关键要点

- **资源名 = 哈希 64 位整数**——运行期不认路径，只认哈希；
- **property 是文件名里的点分段**，天然落在文件系统元数据里，不需要额外 manifest；
- **platform 编译期解析、language 运行期解析** 是关键分工：一个是打包裁剪，一个是动态查找；
- **property preference order** 是降级序列，按优先级枚举所有子集；
- **任意维度扩展**：`withkittens` 这种业务 flag 和 `ps3` 完全同构，开发者可自定义；
- **跨平台预览**只是"编译输入平台"和"编译输出平台"的参数解耦——很小的扩展点吃掉很大的需求。

## 链接到的概念

- [[platform-specific-resources-property-system]]
- [[resource-system-design]]
- [[handle-based-resource-manager]]
- [[non-cryptographic-hash]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/12/platform-specific-resources.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-12-22_platform-specific-resources.md`
