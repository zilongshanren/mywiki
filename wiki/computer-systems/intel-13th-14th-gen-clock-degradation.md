---
tags: [cpu, intel, 硬件故障, oodle, 调试]
date: 2026-04-19
sources: 1
---

# Intel 13 / 14 代桌面 CPU 时钟树退化

2023 年春开始，Fortnite 等 Unreal Engine 游戏在 Intel Core 13 / 14 代桌面 CPU 上大批量出现**间歇性 shader 解压失败、驱动报 out-of-memory、shader 编译错误**。Intel 2024 年确认这是**时钟树电路随时间发生物理退化**导致时钟 skew 增大的硬件 bug。对软件侧而言，这是「别人家的坏硬件却落在你 bug 列表里」的典型灾难。

## 症状特征

[[fabian-giesen|Fabian Giesen]] 在 Oodle 2.9.14 的 work-around 复盘里总结：

- 同一块 256 KB 数据**第二次解压常常成功**——失败不是真的 ECC 失效或存储损坏。
- 失败日志里**从来没有 bitstream desync**；bit reader 永远跑完，只是在后续 LZ 步才发现 Huffman 解出了错值。
- 错值**永远是单字节**：连续 7000–10000 字节正常，某一字节出错，然后继续正常。memory stomp 通常会 32 / 64 bit 一起坏——这明显不是 stomp。
- 出错字节的值**总在 1–11 范围**——正好是 Oodle Huffman 码长字段 (`uint8_t len` / 11-bit limit) 的取值范围。

## 根因推测

Oodle 的 Huffman 解码核心循环（BMI2 版本 4 条指令）是：

```asm
andn rcx, rMask, rBits           ; peek
movzx ecx, word [rTable + rcx*2] ; {len, sym} 表项
shrx rBits, rBits, rcx           ; 更新 bit buffer
mov [rDest + <idx>], ch          ; 存高字节 sym
```

错乱发生在**最后一条**：存的应当是 `ch`（bits [15:8]，即 `sym`），但硬件偶尔存成了 `cl`（bits [7:0]，即 `len`）。Giesen 的推测是 x86-64 支持 byte-high 寄存器写存储，需要 mux 选择要存哪一 byte；在超频或 turbo boost 高端频率下，**控制信号的 timing slack 很薄，偶尔来不及到位**，默认落到 low byte。

## Oodle 2.9.14 的 work-around

回避 byte-high 存储即可：

```asm
shrx rBits, rBits, rcx
shr  ecx, 8                      ; 先把 sym 移到 cl
mov  [rDest + <idx>], cl         ; 再存低字节
```

多一条 shift 指令，约 0.5% 吞吐损失——因为该循环的瓶颈是依赖链 latency，不是指令吞吐。`gcc` / `clang` 在同样的 C 代码下也会生成相同的 byte-high 指令序列，不是 ASM 手写的错。

## 启示

- 对开发者：出错的**统计模式**（值域 1-11、单字节、重试能救）比任何 perf counter 都先告诉你「这是硬件 bug」。
- 对用户：一旦出现症状，时钟树已经**物理损坏**；Intel 微码更新只能减缓新机器的退化速率，不会修好已损坏的机器。
- 历史教训：2023 年调查过程里走了无数弯路——坏声卡驱动污染向量寄存器、主板厂默认 BIOS 把 253 W TDP 的芯片配 500 A 限流、「禁 E-core 能救」等传言都是干扰噪声。真正的"烟枪"来自客户的 consistent repro，再加上 Oodle workspace 可 dump 的特性。

## 相关

- [[fabian-giesen]]
- [[oodle-compression-suite]]
- [[cpu-performance-formula]]

## Sources

- [[sources/ryg-oodle-2-9-14-intel-13th-14th-gen]]
