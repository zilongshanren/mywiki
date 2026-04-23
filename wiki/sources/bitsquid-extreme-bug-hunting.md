---
tags: [source, bitsquid, 调试, 内存, 工程实践]
date: 2026-04-19
sources: 1
---

# Extreme Bug Hunting（Niklas Frykholm / bitsquid blog）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 4 月的一篇 war story：submission 前一周碰到"只在 release、只在 PS3、每次崩在不同调用栈、复现率低"的 bug，如何在几天内收网。

## 摘要

文章前半段是**方法论**：不要盯着"怎么修"，而是盯着"我能学到什么"；把已知未知都写下来；每条恼人属性都是信息（release-only → 可能是未初始化或时序；PS3-only → 平台专属系统；低复现率 → 随机性来源；调用栈漂移 → 有坏系统正在越界写）。中段是**实验清单**：脚本化复现（至少把概率稳到 30% 再算）；逐系统 disable；git bisect；memory breakpoint；malloc 填 pattern（zero / 0xFF / 0x12345678）；free 清零；canary value 检测 buffer overflow；memory walker 周期校验；切 allocator；对可疑子系统换 virtual memory allocator，访问已释放地址直接 page fault。末尾给了一个具体案例：上述套路把嫌疑锁到新加的 PS3 SPU 解压库，VMM 触发 DMA 错误暴露了"buffer free 之后 SPU 还在 DMA 往里写"的 lifetime race，修掉。评论区补充：PC 端跑 Valgrind 一键搞定很多此类 bug——但对 SPU 无效，也是为什么当年这套手动方法必须存在。

## 关键要点

- **别慌写下来**：每个 hypothesis / elimination 都加进列表；焦虑来源是信息不足；
- **从 symptom 读 hypothesis**：release-only / 平台-only / 低复现率 / 调用栈漂移，每个都对应一组可能原因；
- **稳定复现是做实验的前提**：哪怕 30% 也比无复现强，脚本化跑 20 次代替手感；
- **受控改动 + 观察变化**：一次只改一样；一次只 disable 一个子系统；记录 bug 的"消失 / 更频繁 / 换地方"作为信号；
- **自定义 allocator 是这套流程的前提**——filling pattern / canary / memory walk / 切 VMM 都得 allocator 支持；
- **Git bisect** 应对"最近引入"类 bug；
- **Race condition 先 disable multi-threading** 验证；
- **VMM 换 allocator** 让 use-after-free 立即 page-fault，是 2011 年主机端接近 ASan 的替代方案。

## 链接到的概念

- [[memory-corruption-bug-hunting]]
- [[custom-allocator-interface]]
- [[managing-coupling]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2011/04/extreme-bug-hunting.html
- 本地：`raw/articles/bitsquid.blogspot.com/2011-04-12_extreme-bug-hunting.md`
