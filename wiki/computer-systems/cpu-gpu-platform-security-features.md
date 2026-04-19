---
tags: [安全, cpu, gpu, 虚拟化, 固件]
date: 2026-04-19
sources: 1
---

# CPU / GPU 平台级安全特性综述

同一台服务器上，CPU 和 GPU 都需要面对一组相似的威胁：**篡改固件、跨租户数据泄露、未授权代码执行**。AMD、Intel、Nvidia 三家给出了三条不同的路径。理解它们的差异有助于看清「datacenter/enterprise vs 桌面消费级」两套安全栈是怎么分化出来的。

## 威胁模型三要素

- **启动完整性**：BIOS / GPU VBIOS 是否可以被改写或被未签名代码替换。
- **多租户隔离**：虚拟化时，一个 VM / 一个 GPU 用户能否窥探另一个的 RAM/VRAM、寄存器、scheduler 时间片。
- **物理层攻击**：直接接触硬件时能做什么——改 BIOS、冷冻内存后物理迁移、侧信道等。

## AMD：加密一切

- **Secure Boot**（EPYC 专属）：可以把 CPU 封装锁定到**单一主板 + 单一 BIOS 版本**，任一改变都会拒绝启动。极端安全但牺牲转售和升级性。
- **SEV（Secure Encrypted Virtualization）**：每个 VM 用独立密钥加密；一颗 CPU 持有 509 个并发密钥槽。
- **SME（Secure Memory Encryption）**：整块 RAM 用一个随机 128-bit AES 密钥透明加密，针对 LN2 冷冻内存迁移这类物理层攻击。
- **MxGPU**：AMD GPU 的多用户方案，基于 PCIe 的 **SR-IOV** 规范，把每个用户锁到独立的显存区与调度窗口；相比纯软件虚拟化更难逃逸。

## Intel：信任根与 CSME 悖论

- **Boot Guard + BIOS Guard**：分别阻止启动时运行未签名代码、阻止刷入未签名 BIOS。两件事分开做。
- **TXT（Trusted Execution Technology）**：测量已运行代码并在异常时告警；主要对抗已经进入系统的恶意代码。
- **IRBR（Runtime BIOS Resilience）**：锁定 SMM/BIOS 的页表，防止被感染的 BIOS 反过来窥探 OS。
- **VT-x**：OS/软件栈层面的硬件虚拟化扩展。
- **TME（Total Memory Encryption）**：Ice Lake SP 才上，对标 AMD 的 SME，用 AES-XTS，但密钥由 **RDRAND 生成**——该指令在当时已被公开研究指出存在可预测性问题。
- **CSME（Converged Security and Management Engine）**：400+ 已知漏洞、大量面向云的攻击面；CPU 本身无法扫描或修改 CSME 的 boot ROM 与固件，导致 CSME 一旦被攻陷，其他所有 CPU 侧安全机制都形同虚设。这是 Intel 安全栈里一个「反面教材」级别的设计。

## Nvidia：不透明 + Falcon 协处理器

Nvidia 公开信息极少，基本是**靠混淆和封闭**。

- **VBIOS 签名**：Hash + 签名阻止刷入改过的 VBIOS，主要影响超频社区，但也能给服务器加点安全。
- **硬件虚拟化**：支持，但**不走 SR-IOV**，因此在严格多租户隔离上弱于 AMD MxGPU。
- **缺失**：无内存加密；任意代码执行的防线据独立研究测得相当薄（甚至有人在 GPU 上跑过完整 OS）。
- **Falcon 协处理器**：从 Maxwell 1（GTX 750Ti）开始植入 GPU，负责锁死部分传感器（温度、热保护阈值），并隔离其他片上微控制器直接访问物理内存——只能走虚拟地址。对付的是「刷固件绕过温控」这类具体攻击，不是通用安全边界。

## 厂商对比的方法学启示

- **数据中心 vs 消费级**：三家的安全栈几乎都偏向企业/服务器——SEV、TXT、MxGPU 都是针对云租户隔离和节点锁定；桌面用户能摸到的只是 Secure Boot 表层。
- **加密 vs 隔离 vs 签名验证** 是三种正交策略；最强的方案（AMD）把三种都用上，而不是押宝单点。
- **单点失效会抵消一切**：Intel CSME 和 Nvidia 私有虚拟化的例子说明，一个大的不可审计组件就足以废掉其余防线。

## 相关

- [[mttf-reliability]]
- [[intel-13th-14th-gen-clock-degradation]]

## Sources

- [[sources/chipsandcheese-security-overview]]
