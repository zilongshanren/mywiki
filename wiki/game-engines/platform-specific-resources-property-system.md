---
tags: [资源系统, 平台差异, 本地化, 构建系统, bitsquid]
date: 2026-04-19
sources: 1
---

# Property 资源变体系统

Bitsquid 引擎用一套"文件名里的点分段"机制把**平台差异、本地化、以及任意业务 flag** 全部统一成同一种变体概念，叫 **property**。

## 数据模型

资源的规范形式：

```
<name>.<property1>.<property2>.<...>.<type>
```

- **name** — 路径派生的唯一标识，运行期被哈希成 64 位整数，不再是字符串；
- **type** — 最后一段，如 `texture`、`lua`、`particle_effect`；
- **property** — 中间所有段，都是变体维度。

例子：

```
buttons.texture
buttons.ps3.texture
buttons.en.x360.texture
buttons.fr.x360.texture
PlayerController.android.lua
bullet_hit.noblood.particle_effect
foilage.withkittens.texture
```

## 两种 property、两种解析时机

- **Platform property**（`ps3`、`x360`、`win32`、`android`……）在**数据编译期**解析。编 PS3 时只打包带 ps3 的变体；若没有 ps3 变体则退回打包所有无平台标签的。**编译期确定 → 包体最小**。
- **Language + 其他 custom property** 在**运行期**解析。全部变体打进 runtime 数据，由游戏设置 **property preference order** 按优先级展开查找。

## Property preference order

`Application.set_property_preference_order {"withkittens", "noblood", "fr"}` 请求 `buttons.texture` 会按降级序列枚举所有子集：

```
buttons.withkittens.noblood.fr.texture
buttons.withkittens.noblood.texture
buttons.withkittens.fr.texture
buttons.withkittens.texture
buttons.noblood.fr.texture
buttons.noblood.texture
buttons.fr.texture
buttons.texture
```

顺序体现优先级——左边的 property 权重高。

## 为什么漂亮

1. **零 manifest**——变体信息全在文件名上，文件系统元数据即是 metadata；
2. **维度正交**——`ps3` 和 `withkittens` 在机制上完全同构，新增业务维度不需要改引擎；
3. **Lua 脚本也是资源**——所以脚本本身能按平台分叉，`PlayerController.android.lua`；
4. **跨平台预览是小扩展**：允许编译器用"平台 A"解析 property、输出"平台 B"的 runtime 格式——编辑器就能在 PC 上跑但呈现掌机下的资源形态。

## 和其他方案对比

相比 Unity 的 platform-specific override 或 Unreal 的 INI 分层，property 系统更像一个**正交维度集合的通用展开器**——特别适合国际化/分级/平台差异这种"多 flag 交叉"的场景。它对接的运行时身份是 64 位哈希（见 [[non-cryptographic-hash]]、[[static-hash-values]]），通过 [[handle-based-resource-manager]] 查找。属于 Bitsquid [[resource-system-design]] 的一部分。

## 相关

- [[resource-system-design]]
- [[handle-based-resource-manager]]
- [[non-cryptographic-hash]]
- [[game-resource-pack-format]]
- [[data-driven-architecture]]

## Sources

- [[sources/bitsquid-platform-specific-resources]]
