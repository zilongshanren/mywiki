---
tags: [位操作, bit-twiddling, bc7]
date: 2026-04-14
sources: 1
---

# 在值的中间插入一个 0 bit

这个小品来自 [[fabian-giesen]] 在 Oodle Texture BC7 解码器里的需求。BC7 把每个像素的 color index 压到 2–4 bit，但某些被称作 "anchor" 的像素的 MSB 被强制为 0，因而不传输——解码时的第一件事就是**把这些隐式 0 bit 重新插回去**，让所有 index 恢复成等宽形式，方便后面统一处理。问题本身非常基础：**在给定位置 pos 插入一个 0 bit，把 pos 及以上的位全部左移 1 位。**

## 朴素做法

拆成上下两段，上段左移一位后再或回去：

```c
uint64 insert_zero_bit(uint64 value, int pos) {
    uint64 bottom_mask = (1u64 << pos) - 1;
    uint64 top_mask    = ~bottom_mask;
    uint64 bottom_bits = value & bottom_mask;
    uint64 top_bits    = value & top_mask;
    return bottom_bits | (top_bits << 1);
}
```

能工作，没错，也完全不是热点——但做一件「听起来很简单」的事用了 5 条语句，ryg 觉得浑身别扭。

## 一行版本

```c
uint64 insert_zero_bit(uint64 value, int pos) {
    uint64 top_mask = ~0u64 << pos;
    return value + (value & top_mask);
}
```

两个关键观察：

- **上半 mask 比下半 mask 更便宜**。通常教科书教我们「用 `(1 << N) - 1` 做下 N 位 mask」，但当我们只需要「最高若干位」时，直接 `-1 << N`（全 1 常量左移）更短一条指令。
- **把一个值加到自己身上等于左移 1 位**。那么「把高位段左移 1、低位段保留」就可以写成「value + 只保留高位的副本」：低位段在副本里是 0，加了等于没加；高位段在副本里不为零，两份相加就是乘 2，即左移 1 位。

只能一次插一个 bit，但 BC7 里一共只有 1–3 个 anchor，重复三次就是。

## 对偶：移除一个已知为 0 的 bit

```c
uint64 remove_zero_bit(uint64 value, int pos) {
    uint64 top_mask = ~0u64 << pos;
    return value - ((value & top_mask) >> 1);
}
```

看起来别扭的是：既然要删掉 pos 这一位，为啥 `top_mask` 还是从 pos 开始？不应该是 `pos + 1` 吗？答：**正是因为「我们已经假设那一位是 0」**，把它纳入 mask 不会改变任何东西——这是一个语义可验证的偷懒（留给读者自证）。减法走的还是上面「+ mask = ×2」的对偶逻辑，不过这次是 ÷2。

## 推广

如果不要求结果对齐到 bit 0，也可以用「下半 mask 版」的同样诀窍：

```c
// 把 pos-1 及以下的位原地左移 1 位、pos 那一位清零；
// pos 以上的位保持不变。
return value + (value & bottom_mask);
```

这一类技巧属于「可爱但不关键」——它们的价值更多在于**训练 bit 层面的思维弹性**，让你在下一个真正卡吞吐的场景下能看出「加法可以替代 mask + 拼接」这种代换。

## 相关

- [[bc7-solid-color-encoding]] —— 同源于 Oodle Texture BC7 的另一枚小品
- [[sign-extend-without-shift]] —— 同一批 ryg bit-twiddling 笔记
- [[sse-tricks]]
- [[fabian-giesen]]

## Sources

- [[sources/ryg-insert-zero-bit-middle]]
