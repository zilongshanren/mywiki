---
tags: [渲染, hlsl, shader-compiler, mipmap, gradient, 调试]
date: 2026-04-14
sources: 1
---

# 分支内的发散 gradient：tex2D 的隐形代价

[[fragment-shader|pixel shader]] 的纹理采样有一个容易被忽视的隐式依赖：为了决定用哪一级 mip，采样器需要**相邻像素间的 uv 偏导数**（gradient / $\partial uv/\partial x$, $\partial uv/\partial y$）。GPU 通常在 2×2 像素组（quad）内做"差分"来得到这个偏导——同一 quad 的 4 个像素总是一起执行，最右像素减最左像素就是 $\partial uv/\partial x$，下一行减上一行就是 $\partial uv/\partial y$。

**这件事一旦与 `if` 分支相遇就会出事**：同一 quad 的四个像素可能走不同分支，quad 内差分变得没有意义。HLSL/D3D 把"分支里对 shader-computed uv 做 tex2D"标记为 **undefined behaviour**，编译器有三个自由度来处理它：

1. **把 `tex2D` 移出 `if`**（reorder）——等价于总是采样
2. **flatten 分支**——两条路径全部执行，最后用 `cmp`/select 选取一条的结果
3. **抛编译错误**："cannot have divergent gradient operations inside flow control"

前两种**对渲染结果没影响**，但都让 `if` 分支形同虚设：你写的 mask early-out 并没有真的 early-out，性能和没有 mask 一样。这是 [[kostas-anagnostou|Kostas Anagnostou]] 在 2014 年生产代码里碰到的原型 bug——功能一切正常，但 profiler 告诉你 mask 区域的成本没降。只有读反汇编才看得到编译器悄悄做的展平：

```
add r0.xy, v0, v0        ; uv * 2
texld r0, r0, s1         ; 两条分支的采样都跑了
texld r1, v0, s0
add r0.w, -r1.w, c0.x
cmp oC0.xyz, r0.w, r0, r1   ; 用 cmp 选
```

## 为什么这不是"动态分支的常识"

GPU 动态分支本身就有 warp/wavefront 合并成本——如果同一 warp 里像素走不同分支，两条分支都会执行，只有对应像素写回结果。这是经典的 SIMD divergence 成本，图形程序员都知道。本文的坑**不在这里**，而在于**编译器因为 gradient 未定义而主动放弃了分支**，连 SIMD-级别的分支都没有生成——即使同一 quad 的所有像素都走 else 分支、理论上 GPU 可以 skip if，编译器也已经把 if 拆成了两条并行路径。换句话说，成本不是"发散时的 worst case"，而是"**任何时候的 worst case**"。

## 三种修复

**显式 mip 级**——用 `tex2Dlod`，第四分量传 mip：

```hlsl
float4 uv4 = float4(input.uv * 2, 0, 0);  // mip = 0
float3 colour = tex2Dlod(texSampler2, uv4).rgb;
```

`tex2Dlod` 不需要 gradient，编译器再也不用担心 quad divergence，分支就能真的被保留。对应汇编出现了 `if_lt / else / endif`，物理上的分支终于存在。

**显式 gradient**——用四参数 `tex2D(sampler, uv, dx, dy)`，自己算或继承外层 quad 的 gradient。适用于你确实需要 trilinear filter、不愿意强制某一 mip 的情况。常见做法是**把 gradient 在 if 外面先算好、分支内部只用这个提前算好的值**。

**在 vertex shader 里算 uv**——如果 uv 只是顶点坐标的线性变换，那就在 vertex shader 里算好传下来，**pixel shader 里不做任何修改**直接用。这样 gradient 可以从插值后的 uv 属性自动推出（硬件本来就为每个插值 attribute 维护 quad-level 差分），不走 shader-computed 路径。限制是所有 uv 变换必须能提前到顶点级。

## `[branch]` attribute：把默默的展平变成编译错误

HLSL 允许在 `if` 前面加 `[branch]` / `[flatten]` / `[loop]` / `[unroll]` attribute 声明意图。加 `[branch]` 强制要求"生成真正的动态分支"——如果内部有 divergent gradient 操作，编译器不能再走 flatten 兜底，只能**报编译错误**。这把 bug 从"profile 不出的性能黑洞"变成"编译直接失败的显错误"。评论区 Tom 确认："cannot have divergent gradient operations inside flow control"——值得把这句错误提示抄进记忆里，搜索引擎上出现就是它。

Anagnostou 给的教训不止 gradient 这一件事：**关键 shader 路径永远读一眼反汇编**。HLSL 和底层 ISA 之间隔了两层编译器（前端 + 驱动），任何一层的优化决策都可能让高层代码的性能直觉完全失效。

## 相关

- [[fragment-shader]] — quad 粒度的执行模型是 gradient 机制的前提
- [[sampler-filter-wrap-modes]] — mip 选择是 filter 体系的一部分
- [[gpu-latency-hiding]] — warp divergence 的更一般性讨论
- [[early-z-late-z]] — 另一个"为了 discard 而牺牲的 hardware 优化"的例子
- [[kostas-anagnostou]]

## Sources
- [[sources/interplay-branches-texture-sampling]]
- [[sources/supnik-derivatives-two-parts]] —— Supnik 2011 从 GLSL spec §8.8 角度讲「non-uniform control flow 内 derivative 未定义」，HLSL 侧的 [[divergent-gradient-in-branches]] 是同一根因在不同语言的投影
