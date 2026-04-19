---
tags: [经验, 创造力, 工程文化, 反思]
date: 2026-04-19
sources: 1
---

# 经验是噪声过滤器

[[angelo-pesce|Angelo Pesce]] 2010 年的 *The pitfalls of experience* 提出一个让资深工程师不太舒服的观察：**经验在 3A 游戏行业是被过度崇拜的美德，而它的副作用往往被忽视**。

AAA 项目的现实是：两三年周期、不可滑动的 deadline、糟糕的遗留代码、惩罚式的迭代时间、全球市场的残酷竞争。只能打一次的仗、必须做对。在这种条件下，经验确实运转得极好——你见过类似问题、能一眼看出方案是否可行、能估算投入产出、能快速砍掉烂点子。

问题在于后半句：**经验在砍烂点子的同时，也砍掉了那些看起来不可能但其实是革命性的点子。** Pesce 引 Lewis Carroll 的 *Alice in Wonderland*："Why, sometimes I've believed as many as six impossible things before breakfast." ——天才之所以是天才，就是因为他们愿意去相信六件不可能的事，而经验则让你学会迅速识别并拒绝它们。

## 深度缓冲 SSAO 的启蒙故事

这篇文章里 Pesce 讲了一个后来被反复引用的亲历故事：同事用 3DRipper 抓了一帧 Crysis 的渲染，发现一张看起来像 **环境光遮蔽（AO）** 的贴图——但它不是烘焙的，是动态生成的。当时 Pesce 不知道这怎么可能做到，也不会主动去尝试。但**一旦知道它可能**，他几天内就写出了一个几乎一样的 shader：在 **[[z-buffer|深度缓冲]]** 上按步长采样、做类似 relief mapping 的简化 raymarching——这正是今天所有 **SSAO / [[hbao-interleaved-sampling|HBAO]] / [[ground-truth-ambient-occlusion|GTAO]]** 的祖师爷思路。

他的总结异常锋利：*"All it took was to know it was possible."* 技术本身并不复杂，难的是**打破"这事做不到"的先验**。

## 实践建议

Pesce 给出的抗性处方很朴素：

- **好奇心要大于专业**。知识是可以被重组的噪声，经验会把这些噪声过滤成"只该这么做"——把两者始终保持在动态平衡。
- **多给外行讲你的工作**。做 presentation、和美术或初级工程师讨论——不是因为他们会给出更好方案，而是讲述的过程本身会把你的大脑摇松。Pesce 自述"我有新想法通常是在写 slides 或讲解的那一刻，甚至还没开始讨论"。
- **重视 preproduction 阶段**。评论区 Txkun 补充的观点：preproduction 才是真正能做新东西的时候，进入量产后就是 grunt work。但 Pesce 反驳说，如果工具链和迭代时间足够快，创造性思维可以贯穿整个项目。**迭代速度是创造力能持续多久的决定性变量**。

## 相关

- [[unknown-unknowns]] —— 经验过滤掉的是"已知未知"，真正危险的是"未知未知"
- [[red-flags]]
- [[taste-development]]
- [[strategic-programming]] 与 [[tactical-programming]]
- [[angelo-pesce]]
- [[hbao-interleaved-sampling]] / [[ground-truth-ambient-occlusion]] —— 这一脉 SSAO 技术的源头就是"知道它可能之后"的几天复现

## Sources

- [[sources/c0de517e-pitfalls-of-experience]]
