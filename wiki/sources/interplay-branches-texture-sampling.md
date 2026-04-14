---
tags: [source, rendering, hlsl, shader-compiler, 调试]
date: 2026-04-14
sources: 1
---

# Branches and texture sampling（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2014 年 3 月一篇短故事：生产代码中一个屏幕空间 shader **用 if 分支 + mask 做 early-out**，实测性能却和不分支一样——真正的原因藏在 shader 汇编里。

## 摘要

作者在一个繁重的 screen-space shader 里用 `tex2D` 读一张 mask 贴图，用 `if` 分支 early-out 避免后续昂贵计算。功能正常，但 mask 区域并没有带来预期的性能提升。反汇编揭示了原因：`tex2D` 在 mask 为假的分支里使用了**在 shader 里算出来的 uv 坐标**，而 [[fragment-shader|pixel shader]] 的纹理采样需要 2×2 像素 quad 上的 gradient 才能决定 mip 级；当 2×2 内的像素在 `if` 分支里走不同路径，gradient 未定义。HLSL 编译器看到"分支里带 shader-computed uv 的 tex2D"时有三种选项：（A）把采样移出 if；（B）**flatten 分支**——两条路径都跑然后 `cmp` 选结果；（C）直接报编译错误。前两种都对可见结果没影响，但都会让分支名存实亡，性能和"不分支"相同。解决方案是让采样不依赖动态 gradient：用 `tex2Dlod` 显式指定 mip 级，或用 `tex2D(s, uv, dx, dy)` 显式传 gradient，或把 uv 留在 vertex shader 里**不经修改**传下来。也可以用 `[branch]` attribute 强制编译器**报错**而不是悄悄展平。

## 关键要点

- **tex2D 的 gradient 隐式依赖 2×2 quad**——同一个 quad 的像素在分支里走不同路径时，shader-computed uv 的 gradient 未定义。
- **编译器的悄悄展平**是 root cause：你以为 mask 在省电，其实两条路径都在跑然后用 `cmp` 选一个。汇编能看到展平，高层 HLSL 看不到。
- **修复三选一**：(1) `tex2Dlod(sampler, float4(uv, 0, mip))` 用显式 mip；(2) `tex2D(sampler, uv, dx, dy)` 自己传 gradient；(3) 把 uv 全部在 vertex shader 里算好、pixel shader 里**不碰**，这样 gradient 仍可以从顶点插值里推出。
- **用 `[branch]` attribute 声明意图**。它要么强制 D3D 真的生成动态分支（不再展平），要么直接在编译期抛错："cannot have divergent gradient operations inside flow control"。不加 attribute 是默认让编译器自由发挥，常常得到相反结果。
- **教训**：不要信任编译器"做对的事"。关键 shader 路径永远看一眼反汇编。

## 链接到的概念

- [[divergent-gradient-in-branches]]
- [[fragment-shader]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2014/03/25/branches-and-texture-sampling/
- 本地：`raw/articles/interplayoflight.wordpress.com/2014-03-25_branches-and-texture-sampling.md`
