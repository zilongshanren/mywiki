---
tags: [prng, rng, determinism, procedural-generation, javascript]
date: 2026-04-19
sources: 1
---

# Mulberry32：极简 32-bit 确定性 PRNG

Mulberry32 是一个用几行代码就能写完的 32-bit 伪随机数生成器。种子、状态、输出全都是 uint32，最后除以 2³² 落到 `[0,1)`。它不是 [[inversion-sampling-prng]] 里讨论的 PCG 那种「统计严谨」的默认选择，而是另一端——**实现成本低到几乎可以嵌进任何项目**，同时保留确定性这一件最关键的事。

## 为什么不是 `Math.random()`

JavaScript 的 `Math.random()` 有两个工程硬伤：**不能 seed**，**规范不定实现**。一旦需要「同种子 → 同序列」的性质，就必须自己带一个 PRNG。典型场景：

- 从 seed 回放程序生成的游戏世界
- debug 时精确复现一次仿真
- 单元测试里稳定的「随机」fixture
- 用户之间用 seed 字符串分享生成结果

一句话：**只要 seed + 调用顺序不变，整个世界就能 byte-for-byte 重建**。

## 核心算法

```javascript
function mulberry32(seed) {
  let t = seed >>> 0;
  return function next() {
    t = (t + 0x6D2B79F5) >>> 0;
    let x = Math.imul(t ^ (t >>> 15), t | 1);
    x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
}
```

每一步拆开看：

- `t = (t + 0x6D2B79F5) >>> 0`：状态线性推进，`>>> 0` 把 JS number 钉死在 uint32。这是 **Weyl 序列**，保证状态周期恰好 2³²。
- `t ^ (t >>> 15)`：把高 17 位折回低位，做一次 bit diffusion。
- `t | 1`：强制奇数，奇数在模 2³² 乘法里保持可逆，保留每个 bit 位置的信息量。
- `Math.imul(a, b)`：JS 普通 `*` 走 64-bit float，会吃掉溢出；`Math.imul` 显式给出 32-bit 带 wrap 的整数乘法，PRNG 公式依赖这个溢出行为。
- `x ^= x + Math.imul(x ^ (x >>> 7), x | 61)`：第二轮 xor-shift-multiply，把信息扩散到整 32 bit。
- `x ^ (x >>> 14)`：final avalanche。
- `/ 4294967296`：uint32 映射到 `[0, 1)`。

整个结构和 [[non-cryptographic-hash]] 里常见的 xor-shift-multiply 混合器是一家的——**一个 PRNG 的 output 函数其实就是一个 avalanche 好的 integer hash**。

## Weyl 序列 + xor-shift mixer

Mulberry32 不是独立发明，是把两个经典 pattern 拼起来：

1. **Weyl 序列**：`t ← (t + c) mod 2³²`。只要 c 和 2³² 互素（这里 `0x6D2B79F5` 显然是奇数），`t` 就会穷尽 2³² 个值，周期精准。
2. **好的 output mixer**：Weyl 序列本身太过有序（每步只变 32 bit 的低位），直接当随机数会被统计测试打穿。上面两轮 `imul + xor-shift` 负责把 uint32 搅成随机性分布，同时不破坏周期。

这套「简单 state step + 复杂 output 混合」是现代 PRNG 的通用结构——[[non-cryptographic-hash]] 中的 rapidhash、xxhash 用的也是同一个配方，区别只在 state 驱动方式（PRNG 是自驱动，hash 是输入数据驱动）。

## 字符串 → seed：FNV-1a

用户更愿意分享 `"world-7-night-rain"` 这样的可读 seed 而不是 `3735928559`。用一个 32-bit 整数哈希把字符串折成 uint32 即可：

```javascript
function hashStringToUint32(input) {
  let h = 2166136261 >>> 0;           // FNV offset basis
  for (let i = 0; i < input.length; i += 1) {
    h ^= input.charCodeAt(i);
    h = Math.imul(h, 16777619);       // FNV prime
  }
  return h >>> 0;
}
```

FNV-1a 是经典的 [[non-cryptographic-hash]]，对这种短字符串的雪崩效果足够，再复杂没有必要。

## 使用纪律：调用顺序就是 API

确定性 PRNG 的「确定」完全依赖调用顺序。一旦某个代码路径多 call 了一次 `next()`，后续所有输出整体漂移，两次运行肉眼看不出 bug，但表现并不一致。几条工程戒律：

- **不要在同一系统里混 `Math.random()` 和 seeded RNG**——一旦混了，调用顺序就不再由你掌控。
- **不要每帧重新 seed**——保留演进的 state，每帧只 step。
- **不同子系统用不同 RNG 实例**——地形、战斗、AI 各一个，避免顺序耦合。跨子系统的随机性用 [[pcg3d-hash]] 那种基于坐标的 hash 更稳。
- **重构前后输出可能对不上**——如果决定算法/调用顺序变了，老 seed 生成的世界就永久失效，要么接受、要么写迁移。

## 适用与不适用

适用：

- 程序化地图、掉落 roll、spawn 模式
- 生成式艺术、视觉效果，seed 可分享
- 需要轻量速度的 Monte Carlo 小实验
- 需要确定「随机」fixture 的测试

**不适用**：

- 任何密码学场景（token、密码重置链接、密钥）——这不是 CSPRNG，状态空间只有 2³²，可被暴力穷举
- 赌博 / 合规性公平抽奖
- 大流量、统计严格的仿真——PCG32、SFC32、Xoroshiro 等家族经过更全面的 TestU01 / PractRand 检验

Mulberry32 的定位是「便利优先」的一类：[[pcg3d-hash]] 负责「每像素 / 每坐标的独立流」，而 Mulberry32 负责「一个 app 内共享的一条确定性流」——两者互补，不互相替代。

## Sources

- [[sources/4rknova-mulberry32]]
