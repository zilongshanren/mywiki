---
tags: [source, bytecode, 虚拟机, 系统, 安全]
date: 2026-04-14
sources: 1
---

# "Bytecode"（Jasper St. Pierre）

[[jasper-st-pierre]] 2012 年 12 月发表于 blog.mecheye.net 的短文，命题是："世界上最常用的字节码不是 Java、.NET、Flash，而是你每天开机都会跑的那几样"——ACPI、字体、网络包过滤器。

## 摘要

文章列了四个被"藏在系统里"的字节码解释器。**ACPI**（Advanced Configuration and Power Interface）规范有近 1000 页，第 20 章定义了 "ACPI Machine Language"——一套半寄存器式 VM，带 Add/Sub/Mul/Div、比较算子，还有 ToHexString、Mid（substring）和完整的对象模型与异步信号机制。OS 必须在内核启动早期实现这整件东西；所有主流 OS（Linux、BSD、macOS、ReactOS、Haiku）都共享 Intel 开源的 **ACPICA** 参考实现。**OpenType/CFF 字体** 里的 Type 2 Glyph Format 是一个真正的栈式解释器，连 "random" opcode 都有；它是 PostScript 的简化版——PostScript 本身是基于 Forth 的图灵完全 VM，也正因如此 PDF 被设计成剥掉它的流程控制之后的"静态版"。TrueType 的 **字体 hinting** 也是一个独立的字节码 VM（见 FreeType 的 `ttinterp.c`）。浏览一篇文章时，成千上万的微程序在每个字形渲染时被执行。**BPF**（Berkeley Packet Filter）是 tcpdump/libpcap 用的寄存器式 VM，2012 年时 Linux 刚把它塞进内核、还加了 JIT。四个 VM 各有故事：FreeType 的 CFF 解释器里的栈溢出漏洞 `CVE-2010-1797` 就是 JailbreakMe 2.0 iPhone 越狱的入口，通过 Apple PDF viewer 加载一个恶意字体。作者评论："字节码是诱人的通用方案，但实现几乎总有安全漏洞，ACPI 的复杂度甚至让全世界只敢维护一份实现——这是代价。"

读者评论还补充了一大串隐藏的字节码：**UEFI EBC**（EFI Byte Code，让显卡固件能在 x86/x86_64/Itanium 上跨架构跑）、**DWARF** 调试信息里的地址表达式 VM（GDB/libunwind 解释，C++ 异常抛出时也会跑）、**SQLite VDBE**（号称"世界最广用的字节码"候选）、**Python pickle**（栈式语言）、**regex 引擎**（字母表即 opcode）、**RarVM**、**Bitcoin Script**（故意非图灵完全的栈式 VM，大多数 opcode 被禁用）、**SCUMM**、**Z-machine**、Infocom 游戏、Notch 的 **DCPU-16**、Xorg VESA 驱动里的 **16 位 x86 模拟器**（为了跑 BIOS）。

## 关键要点

- **ACPI** 是全世界被最多 OS 实现的字节码 VM，一份 ACPICA 被 Linux/BSD/macOS/ReactOS/Haiku 共用；规范太复杂是这种"单一实现"的直接后果。
- **字体 = 小程序**：OpenType CFF 用栈式 Type 2 字节码描述字形、TrueType 用独立的 hinting 字节码做像素级渲染修正。渲染一页文字 = 解释成千上万个微程序。
- **PostScript → PDF 的动机**：PostScript 的 Forth 风格图灵完全 VM 会无限循环、状态耦合强，PDF 把流程控制砍掉换来"可以脱机渲染、能自动校验"的稳定性。
- **BPF** 是寄存器式 VM，Linux 2.2 起成为 Linux Socket Filter；2012 年加入 JIT 编译器（`arch/x86/net/bpf_jit_comp.c`）。
- **字节码 = 安全深水区**：每一个字节码解释器都有 CVE。CFF 的栈溢出漏洞 `CVE-2010-1797` 被 JailbreakMe 2.0 利用越狱 iPhone——入口是 PDF 里的恶意字体。
- **隐藏的字节码山**：UEFI EBC、DWARF、GCC C++ 异常处理（走 DWARF 格式）、libunwind、SQLite VDBE、Python pickle、regex、RarVM、Bitcoin Script……字节码比大多数人以为的要普遍得多。
- **UEFI EBC 的独特设计**："natural indexing"——指针偏移的计算从编译器推到运行时 VM，让同一份字节码可以在 32 位 ARM 和 64 位 Itanium 上跑。
- **设计启示**：命题"字节码 VM 让设计灵活"在系统层反复被证实有代价。文章结尾作者对 spec 作者的反问是："你真的需要那份灵活性吗？"

## 链接到的概念

- [[bytecode-everywhere]]
- [[jasper-st-pierre]]

## 原文

- 链接：<https://blog.mecheye.net/2012/12/bytecode/>
- 本地：`raw/articles/blog.mecheye.net/2012-12-09_bytecode.md`
