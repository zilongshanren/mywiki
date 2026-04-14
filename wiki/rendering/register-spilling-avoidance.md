---
tags: [渲染, GPU, 着色器优化, 性能, 寄存器]
date: 2026-04-14
sources: 1
---

# 寄存器溢出与规避（Register Spilling）

**寄存器溢出**（register spilling）是 shader 性能最阴险的悬崖之一。一段算法看起来正确、计算量合理、profiler 里却显示 L2 吞吐率异常高、SM throughput 却提不上去——几乎总是一行"无意间"引入了动态数组下标。

## 寄存器为什么重要

GPU 的内存层次大致是 VRAM → L1/L2/(L3) → **寄存器文件**。寄存器是真正给算术单元喂数据的地方：

- RTX 4070 的寄存器文件总容量约 11.5 MiB；
- 如果每条 FMA（fused multiply-add）读 3 个浮点写 1 个浮点，峰值寄存器带宽约 **361 TB/s**；
- 同一张卡 VRAM 带宽约 500 GB/s——**差 718 倍**。

一条 GPU 机器指令里，寄存器号是**硬编码**的。这意味着：如果某个数组访问的下标在编译时不能被确定，就无法为它生成"从寄存器 R7 读到 R12"这种指令——编译器只能把这个数组存到 **local memory**（实际走 L1/L2 缓存），代价是每次访问都变成若干条内存指令。这就是 spill。

## 典型触发模式

```glsl
int positive_count = 0;
for (int i = 0; i != 6; ++i) {
    if (numbers[i] > 0) {
        numbers[positive_count] = numbers[i]; // positive_count 动态
        positive_count++;
    }
}
```

`numbers[positive_count]` 的下标是运行时计算出来的，不是编译期常量——整个 `numbers` 数组会被强制 spill。即使只有 6 个元素。

另一种更隐蔽的例子：

```glsl
for (int i = 0; i != 6; ++i)
    sum += numbers[i];
```

如果循环真的按变量 `i` 执行，`i` 也不是编译期常量——也会触发 spill。解法：`[[unroll]]`，让编译器展开成 `sum += numbers[0]; sum += numbers[1]; ...`。

## 三条规避规则

Christoph Peters 在写度 26 多项式求根时总结出的节奏：

1. **循环下标 → 数组下标，强制 `[[unroll]]`。** 启用 `GL_EXT_control_flow_attributes`。
2. **编译器不听话的场合手工展开。** 常见 hack：写一段 `[[unroll]] for (int i = 0; i != N; ++i) dst = (cond_on_i) ? src[i] : dst;`——用静态下标 + 条件选择来模拟动态索引。
3. **不必须展开的循环用 `[[loop]]`。** 过度展开会撑大代码体积，让**指令缓存**开始 miss，反而变慢——Peters 测到把所有 `[[loop]]` 换成 `[[unroll]]` 后度 10 的 shader 从 1.46 ms 变成 3.85 ms。

## 识别 spill 的信号

Nsight 上的两个主要证据：

- **L2 cache throughput 异常偏高**，而 shader 本身不读/写任何 buffer；
- **local memory traffic 非零**（NVIDIA 术语，就是 spill 的内存）。

优化前后的对比可以很极端——Peters 的度 18 多项式求根：

| | 度 10 | 度 18 |
|---|---|---|
| 优化实现 | 1.46 ms | 10.4 ms |
| 含 spill 的导数计算 | 4.82 ms（3.3×） | **2650 ms（255×）** |

度 18 那一行基本确认 spill 是一路穿透到 VRAM 的。

## 展开不是万能

- **代码膨胀**：展开一个度 26 的多项式内循环，生成的机器码可能几 KB，撑爆 instruction cache，同样减速；
- **编译时间**：展开后编译器要反复 inline、常量传播，编译可能上分钟；
- **可读性**：展开之后的手写 workaround 丑得无法维护——要加注释说明为什么非得这么写。

规则是"**哪里非得展开才能躲 spill 才展开**"。其它地方用 `[[loop]]`。

## 和其它领域的对应

- **[[sources/ryg-trip-through-graphics-pipeline-2011-part-6|ryg 的 rasterizer 流水线]]** 里的"unrolled"段也是同样的逻辑：硬编码下标。
- **AVX / SSE** 代码里的"动态 shuffle 不能走 register path，要走 pshufb"——本质是同一个"硬件对静态索引友好"的原则。
- **[[cache-friendliness]]** 强调数据布局；这里强调的是**控制流**——但底层都是"让硬件提前知道下一次要访问什么"。

## 相关

- [[polynomial-root-finding-gpu]] — 这个规避手册的起源案例
- [[gpu-printf-debugging]]
- [[sse-tricks]]
- [[cache-friendliness]]

## Sources

- [[sources/peters-gpu-polynomial-roots]]
