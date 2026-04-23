---
tags: [bytecode, 虚拟机, 系统, 安全, acpi, 字体]
date: 2026-04-14
sources: 1
---

# 字节码无处不在：被藏起来的解释器

提到"字节码"，大多数人想到的是 JVM、CLR、Flash AVM——一类有明确身份的语言运行时。但现代计算机里跑得最多的字节码恰恰是那些**没有身份**的：它们躲在规范的某一章里，只被 one implementation 实现，使用者不知道自己正在调用一个解释器。[[jasper-st-pierre]] 在 2012 年的 [[sources/jasper-bytecode|一篇短文]] 里把这件事的四个典型例子拎出来，本页把要点与后续讨论汇总成"字节码考古索引"。

## 开机即见：ACPI AML

**ACPI**（Advanced Configuration and Power Interface）规范接近 1000 页，第 20 章定义了 "ACPI Machine Language"——一套半寄存器式 VM，带算术、比较、字符串操作（`ToHexString`、`Mid`）、完整对象模型、异步信号。每块主板、每个外设的 ACPI 表都是 AML 字节码，从 BIOS 通过 `DSDT/SSDT` 表流向 OS，由 OS 在**内核早期启动阶段**解释执行。

因为规范太复杂，全世界实际上只有一份共享的参考实现：Intel 开源的 **ACPICA**，被 Linux、所有 BSD、macOS、ReactOS、Haiku 共同使用（`drivers/acpi/acpica/` 在 Linux 源码树里）。这是"规范复杂度驱动实现单一化"的极端例子——没有第二家能独立实现整套 VM。Windows 是否用 ACPICA 不明，但 Microsoft 是 ACPI 规范的共同作者，它的实现可能自给自足。

## 每一帧文字：字体里的两个 VM

渲染一篇文章，屏幕上每个字形的诞生通常要跑**两个**不同的字节码 VM。

**OpenType CFF / Type 2 Glyph Format**：基于 [Adobe Type 2 Charstring Format](http://wwwimages.adobe.com/www.adobe.com/content/dam/Adobe/en/devnet/font/pdfs/5177.Type2.pdf)，是一个真正的栈式解释器——栈、子程序、甚至有 `random` opcode 可以让字形在运行时随机变化。它是 **PostScript** 的剥离版本：PostScript 本身是基于 Forth 的图灵完全 VM，带循环和条件跳转，结果就是"渲染一页可能不终止"、"整份文档有全局状态"——这两个坑正是 **PDF** 选择砍掉流程控制、把文档切成独立可渲染页的直接原因。

**TrueType Hinting**：为了让字体在低分辨率屏幕上**看起来**正确（字冠对齐、笔画粗细一致），TrueType 规定了一个独立的字节码 hinting VM。FreeType 的 `src/truetype/ttinterp.c` 就是它的实现。一个字体文件里同时带 CFF 字形和 TrueType hinting 并不罕见；这意味着显示一篇长文时"成千上万的微程序"被顺序解释——一个字形一次。

FreeType 的 CFF 解释器有一个 CVE：`CVE-2010-1797`。它是 **JailbreakMe 2.0** 越狱 iPhone 的入口——恶意字体通过 Apple 的 PDF viewer 触发栈溢出，一键越狱。字体 = 代码执行面，不是隐喻。

## 每一个网络包：BPF

**Berkeley Packet Filter** 是 tcpdump / libpcap / Wireshark / Linux Socket Filter 用来在内核里高效筛选网络包的寄存器式 VM。原设计来自 4.3 BSD，Linux 2.2 起被移植成 Linux Socket Filter。2012 年时它刚在内核里获得 JIT 编译器（`arch/x86/net/bpf_jit_comp.c`）——这也是今天 **eBPF** 的史前身形，后者把它从"包过滤 DSL"推到"通用内核可插拔执行环境"。

## 一堆没被收进主线的小字节码

社区评论补上的"字节码考古山"（本页同等看待）：

- **UEFI EBC**（EFI Byte Code）：为了让显卡固件能在 x86/x86_64/Itanium/ARM 上跨架构跑，UEFI 定义了一个私有 VM。它的独特设计是"natural indexing"——指针偏移的计算从编译器推到运行时 VM，所以同一份字节码在 32 位和 64 位指针上都能跑。
- **DWARF** 调试信息格式里的地址表达式 VM：由 GDB / libunwind 解释，用来在运行时计算变量位置、栈帧展开信息。**C++ 异常抛出**走的正是 DWARF VM——`gcc` 的 `Dwarf2EHNewbiesHowto` 说得很清楚，一次 `throw` 会触发一堆字节码解释。
- **SQLite VDBE**：SQLite 的查询引擎把 SQL 编译成内部字节码再解释，社区有声音认为它是"世界最广用字节码"最强竞争者。
- **Python pickle**：栈式语言，格式即 VM。pickle 的不安全性正源于它的图灵能力。
- **Regex 引擎**：bytecode 的字母表就是字符集本身，但本质上确实是一个解释器。
- **RarVM**：RAR 压缩格式里嵌的 VM，有完整研究（`blog.cmpxchg8b.com` 的 "Fun with Constrained Programming"）。
- **Bitcoin Script**：故意**非图灵完全**的栈式 VM——没有循环、没有 `JUMP`——这样链上脚本可以被静态验证、不会陷入死循环。大多数 opcode 目前被禁用。
- **Xorg VESA 驱动的 16 位 x86 模拟器**：为了跑显卡的 BIOS option ROM，Xorg 自带一个 x86-16 模拟器。KMS 普及后才不再是热路径。
- **Z-machine / SCUMM / DCPU-16**：Infocom 的 Zork、LucasArts 的 Maniac Mansion、Notch 的 0x10c 都各自有自己的 VM。

## 共同主题：字节码 = 灵活性 × 安全成本

四个主例 + 一堆补例揭示同一个 pattern：把"在设备/文档/字体/包里塞一段代码让 OS 去跑"这件事做成字节码 VM，带来两件事：

1. **灵活性爆炸**：ACPI 从一个声明式表规范 scope creep 到完整对象模型 + 异步信号，TrueType hinting 可以对每种像素密度单独做像素级修正，PostScript 可以在字形里摇色子。
2. **安全债永远还不清**：上面列出的每个 VM 都有 CVE 史——CFF 栈溢出越狱了 iPhone，TrueType hinting 也吃过 CVE（`CVE-2010-3814`），DWARF、ACPI、pickle 都有自己的惨案史。"解释器实现难以写对"是规律，不是个例。

这也是为什么 **ACPICA 是世界唯一** 的 ACPI 实现——大家不是不想重写一份，是真写不起——以及 **PDF 选择砍掉 PostScript 的图灵能力**、**Bitcoin 选择非图灵完全**、**eBPF 在内核里强加 verifier** 的动因：对字节码灵活性喊停是持续工程的必要动作。

## 设计启示：你真的需要图灵完全吗？

原文结尾的一句反问放在这里合适：**"你真的需要那份灵活性吗？"** 大多数"规范里有个小表"的场景其实不需要可变状态、不需要循环、甚至不需要算术——把它写成声明式结构比写成字节码要省下几十个 CVE 的未来成本。字节码的诱惑很大，但系统设计里它应该是**最后一个**选项而不是第一个。

## 相关
- [[jasper-st-pierre]]
- [[lambda-calculus]] —— 另一个"语言 = 最小 VM"的母题
- [[lua-design-philosophy]] —— 被评论者提议"能不能都换成 Lua？"的那个候选
- [[vector-field-bytecode-vm]] —— 外循环指令/内循环数据的大规模向量化字节码 VM

## Sources

- [[sources/jasper-bytecode]]
