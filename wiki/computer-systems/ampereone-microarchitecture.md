---
tags: [cpu, ampere, arm, server, cloud, density, microarchitecture]
date: 2026-04-27
sources: 1
---

# AmpereOne 微架构

AmpereOne 是 Ampere Computing 首款完全自研的数据中心 CPU 核心，推出于 2024 年前后，与此前授权自 Arm Neoverse 的 Altra 形成鲜明对比。其设计哲学可以用一个词概括：**密度（density）**——在单块物理服务器上同时服务尽可能多的云用户，同时保证性能一致性与安全隔离，而非追求单核峰值性能。

## 设计取舍

为了密度与一致性，AmpereOne 明确舍弃了两类常见的性能手段：一是 SMT，多租户环境中 SMT 会带来安全隔离复杂性与性能不一致；二是动态频率调整（boost），按需超频会让延迟 SLA 难以预测。核心最高运行在 3.7 GHz，Oracle 云实例可见型号上限为 3 GHz。

整颗芯片采用 chiplet 设计（Ampere 首次）：计算核心 die 基于 TSMC 5nm，PCIe 与内存控制器 die 基于 TSMC 7nm，支持 8 或 12 通道 DDR5，最高 128 条 PCIe 5.0 通道。核心按 4 核集群组织，排列在 8×9 的片内 mesh（基于 Arm CMN，Ampere 自定义扩展）上。

## 前端

AmpereOne 使用 **8 表 TAGE** 分支预测器，预测准确率宣称达到高 90% 区间，实测与 AMD Zen 4/5 处于同一量级。BTB 分两级：L1 约 256 项（零气泡延迟），L2 共 8K 项，L2 BTB 脱靶后会命中 L2 数据缓存侧的延迟（约 11-12 周期）。分支预测器通过 32 项解耦队列超前运行，驱动指令预取。

前端最具特色之处是 **16 KB L1 指令缓存**——相当小，甚至不如许多密度优化核心（如 Crestmont 的 64 KB）。Ampere 此举有意为之：更小的 L1i 延迟更低，有助于将分支预测失误恢复时间压至 10 周期，而 Zen 4 的常见情形是 11–18 周期。L2 到前端有专用低延迟路径，在实测中可充分填满解码器，效果类似 Zen 4/5 的微操作缓存角色。

解码宽度为 **4 微操作/周期**，但每周期最多扫描 **5 条指令**，以充分利用指令融合（macro-op fusion）。Ampere 宣称其融合激进度为业界最高，在 libx264 等分支密集型工作负载中可实现负微操作膨胀（instruction count < micro-op count 的逆向），节省后端资源。

## 后端

后端共有 **8 组调度器，192 总项**，供给 12 条执行管道。整数侧 4 组调度器，每组约 20 项；FP/向量侧 2 组，每组约 24 项，支持两条 FP 端口（均可处理 BF16/FP16/AES），另有两组 LS 调度器各 32 项。分布式调度器在高负载时可能出现不均衡（某个队列拥塞而其他端口空闲），实测文件压缩时整数调度器 IXA 队列利用率异常偏高，是潜在瓶颈。

FP/向量侧的 2×24 项相比高性能核心（Neoverse V2 的 2×28、Zen 4 的 2×32）偏浅，但对密度定位的设计而言属预期内的取舍。FP 调度器同样缺少非调度队列（NSQ），使 in-flight FP 操作数少于 Zen 4。

## 缓存与存储器

L1D 为 **64 KB 写直达（write-through）**，配合高带宽 L2 写通路（实测约 16 B/cycle 写吞吐），避免了早期写直达设计（Bulldozer、Pentium 4）的 L2 写瓶颈问题。Store forwarding 延迟 6–7 周期，条件较 Arm 官方核心宽松（只需 load 包含于 store 范围内，而非 Neoverse V2 要求的对齐子集）。

**私有 2 MB L2** 是密度优化策略的核心：11 周期（约 3.68 ns）延迟，足以隔离核心与高延迟 mesh。每核 2 MB L2 与 Graviton 4 相同，但比 Grace（Nvidia 的 Neoverse V2 实现，仅 1 MB L2）更合理。L2 有 48 条未完成请求跟踪槽，以及准确率优先的预取队列。AmpereOne 没有传统意义的片级 L3，而是依赖 mesh 上的分布式系统缓存（coherency engine 切片）。

**系统级**配备"自适应流量管理"：下游（coherency engine、内存控制器）向上游（核心）反馈拥塞信号，延迟敏感型与带宽密集型工作负载采用不同的访问节奏，宣称在带宽压力下保持更优的延迟。

## 性能定位

实测中，AmpereOne 的 IPC 水平接近 Intel Skylake，但 FP/向量侧弱于同属密度优化的 Intel Crestmont，股票频率下输给高性能核心（Zen 5、Neoverse V2 高频版）。这符合其设计目标：不是最快的单核，而是最适合同时服务大量用户的核心。

## Sources

- [[sources/chipsandcheese-ampereone]]
