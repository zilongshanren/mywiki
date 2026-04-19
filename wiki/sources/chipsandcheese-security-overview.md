---
tags: [source, chipsandcheese, 安全, cpu, gpu]
date: 2026-04-19
sources: 1
---

# Security and You, an Overview（Chips and Cheese）

[[chips-and-cheese]] 2021 年 2 月发表的横向对比文章，把 AMD、Intel、Nvidia 三家在平台安全上的做法并列摊开，引用各厂官方白皮书与官方声明，少量使用第三方独立测试。

## 摘要

文章以 **「datacenter/enterprise 才是重点」** 为前提，依次走完三家的安全栈。AMD 主打「加密一切」：EPYC 级 Secure Boot 可把 CPU 封装锁死在某块主板某版 BIOS，SEV 给每个 VM 独立 AES 密钥（一颗 CPU 509 槽），SME 整机内存加密，GPU 侧用 PCIe SR-IOV 的 **MxGPU** 做硬件多租户。Intel 的栈更碎片化：Boot Guard / BIOS Guard / TXT / IRBR / VT-x 各司其职，Ice Lake SP 才加了对标 SME 的 TME；但文章直接点名 **CSME** 是一堆安全漏洞的温床——CPU 甚至没法扫描或修改 CSME 的固件，一旦被攻陷前面所有机制就废了。Nvidia 选择「混淆即安全」：公开信息极少，硬件虚拟化不走 SR-IOV，没有内存加密，任意代码执行的防线薄到可以在 GPU 上跑完整 OS；仅靠 Falcon 协处理器守住几个具体场景（热保护被绕过、其他微控制器接触物理内存）。

## 关键要点

- **AMD SEV/SME/MxGPU** 是三家里最完整的一套，既加密又隔离又走标准 SR-IOV。
- **Intel CSME 是反面教材**：一个大的不可审计组件足以废掉其余防线。
- **Nvidia 靠封闭**——Falcon 协处理器只锁几个具体攻击点，不构成通用隔离边界。
- **消费级桌面用户** 能摸到的基本只是 Secure Boot 表层，强安全特性都绑在服务器/企业产品线上。
- 文章避开了 Spectre/Meltdown 一类侧信道话题，专注于**官方已实现的安全功能**。

## 链接到的概念

- [[cpu-gpu-platform-security-features]]

## 原文

- 链接：https://chipsandcheese.com/p/security-and-you-an-overview
- 本地：`raw/articles/chipsandcheese.com/2021-02-07_security-and-you-an-overview.md`
