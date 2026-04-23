---
tags: [渲染, shader, GLSL, 编译器, X-Plane]
date: 2026-04-19
sources: 1
---

# 依赖 GLSL 编译器而不是手写 #define 迷宫

[[ben-supnik|Supnik]] 用 AMD ShaderAnalyzer（一个把 GLSL 编译到 R700 / RV790 汇编的 Windows 工具）逐个观察驱动编译器替他做了什么、没做什么，然后用这份观察改造了 X-Plane 10 的 shader 组织方式。

## ShaderAnalyzer 看到的真相

RV790 的 ALU 非常复杂：每个 ALU 指令组由 **5 个 scalar 子指令** 构成，其中只有一条可以跑 `log` / `exp` 之类的超越函数。因此 `pow(vec4, vec4)` 在每个通道上都要 log+exp，整体要 **8 个指令组**——这是实测代价，不是直觉。

驱动编译器替你做的事：

- **全程 inline**。Supnik 写了一个递归 factorial（虽然 GLSL 规范明确禁止递归），编译器直接展开 127 层；实际递归不合法，但这说明 inline 的激进程度。
- **常量折叠 + 乘 0 消除**。写 `expensive_albedo() * vec4(0.0)`，整段 expensive_albedo 被整体删掉，只留一个 load 0。
- **编译期已知分支消除**。`if (const_expr)` 只留一边，另一边的代码彻底不生成。

编译器**不**替你做的事：

- **值域推理 (range inference)**。`if (max(0.6, x) > 0.3)` 对人来说恒真，但编译器不会从 `[0.6, +∞)` 推出「一定大于 0.3」。Supnik 推测 LLVM 能做，但 2010 年的 GLSL 前端做不到。**在这类地方你得替编译器用脑**。

## 对 X-Plane shader 组织的启发

X-Plane 的 physical shader 基于 **条件编译**：把所有可用效果组合成一堆 `#define` 开关，针对 state 向量重新编译出一个个「只包含用到的特性」的 shader。第一代 DX9 硬件甚至连运行时分支都没有，编译出空代码是唯一拿到 fixed-function 性能的方式。

问题是这条路**不随代码规模线性扩展**。到 X-Plane 9/10 效果堆多了以后，手写 conditional logic 变成人肉优化器。

观察编译器以后 Supnik 得出的结论：**把 shader 切成「每个阶段一个函数」，让 `#define` 只决定每个函数的内部实现**，然后交给编译器把 `0.0` 传递出去、把 MAD 消掉。例子：

```glsl
float calc_spec() {
#if has_spec
    return pow(max(0.0, dot(N, L)), 128.0);
#else
    return 0.0;
#endif
}

void main() {
    float s = calc_spec();
    gl_FragColor = albedo * lighting * shadow + ambient + shadow * vec4(s, s, s, 0.0);
}
```

关 spec 时 `s = 0.0` 常量折叠，整条 `shadow * vec4(s, s, s, 0.0)` MAD 会被整块删除——人不用手动把它从 `main()` 里 `#ifdef` 出来。

## 界限：不是所有场景都能躺平

代价是 shader 可能会比「一次性手写纯净 case」多**泄露几条指令**，GLSL 写出来的也未必和手写汇编一样紧。但 Supnik 的权衡是：**绝大多数 shader 走编译器、真正要命的几个热点路径单独手调**——人没时间把每个 feature 组合都写一份，但热路径值得手术。

## 相关

- [[shader-instruction-cost]] — 指令级代价的另一面
- [[divergent-gradient-in-branches]] — 编译器对分支 + 梯度的「偷偷展平」是另一种躺不平的情况
- [[common-shader-pitfalls]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-glsl-compiler-observations]]
