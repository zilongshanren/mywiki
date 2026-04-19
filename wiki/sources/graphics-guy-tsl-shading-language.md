---
tags: [source, 渲染, 离线渲染, 着色器, 语言设计]
date: 2026-04-19
sources: 1
---

# Making a Shading Language for my Offline Renderer（A Graphics Guy's Note）

[[graphics-guy-notes|Jiayin Cao]] 发表于 2021 年 3 月的长文，复盘自己花四个月业余时间为 SORT 渲染器写 [[tiny-shading-language|Tiny Shading Language (TSL)]] 的设计思路与收获。

## 摘要

作者先交代动机：OSL 虽然成熟，但依赖链重（OpenImageIO、OpenEXR、libpng 等），在 Apple Silicon 尚未被支持，加之他当时在索尼（Naughty Dog），想避免直接评论 OSL。自研 TSL 的决定让他能**借 Flex + Bison + LLVM 几乎不写编译器本体**，把精力集中在"一个为 CPU 路径追踪器定制的语言系统"上。全文核心在讲 CPU shader 与 GPU shader 的本质差异——一对一执行、允许 call stack、输出 closure tree 而非颜色——以及这些差异如何推导出 shader unit template / shader group template / closure / TslGlobal 的设计。最后用 SORT 的 Disney BRDF + Coat 材质例子展示 closure 与递归 closure 的用法。

## 关键要点

- TSL 不追求与 OSL 功能对等，只求"一人四月能做出可用的版本"。
- 依赖 LLVM JIT 产出 CPU 机器码，对手写汇编零依赖。
- closure 是延迟求值的占位符，BXDF 真正评估仍在 C++ 侧——避免"每新增一个 BXDF 接口就要多一种 shader"的组合爆炸。
- shader group template 本身是 shader unit template → 材质图可递归嵌套，Blender 插件里的 ungroup hack 自然消失。
- TslGlobal 宏化的全局数据结构让 shader 与 host C++ 共享同一份 memory layout，避免逐类 shader 各配一份 cbuffer。
- TSL 承认自己比 OSL 脆弱（"随便写点奇怪代码就能 crash"），但核心的"语言 + 材质图"闭环已经跑通。

## 链接到的概念

- [[tiny-shading-language]]
- [[path-tracing-basics]]
- [[microfacet-brdf]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/making_a_shading_lagnauge_for_my_offline_renderer/
- 本地：`raw/articles/agraphicsguynotes.com/2021-03-09_making-a-shading-language-for-my-offline-renderer.md`
