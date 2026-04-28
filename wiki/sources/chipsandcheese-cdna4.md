---
tags: [source, gpu, amd, cdna4, mi355x, hpc, ai, chiplet]
date: 2026-04-27
sources: 1
---

# AMD's CDNA 4 Architecture Announcement（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 6 月的文章，分析 CDNA 4 架构相对 CDNA 3 的改动重点与设计哲学。

## 摘要

CDNA 4（MI355X）是对 CDNA 3（MI300X）的渐进式迭代，核心变化集中在两处：一是重新平衡执行单元以强化低精度矩阵运算吞吐；二是将 LDS 容量从 64 KB 提升至 160 KB 并将带宽翻倍，同时引入 LDS 转置读指令与增强版 GLOBAL_LOAD_LDS。系统级架构沿用 CDNA 3 的大型 chiplet 设计，XCD + IO Die 组合；内存升级至 HBM3E，带宽提至 8 TB/s，总容量 288 GB。文章指出 CDNA 4 的调整策略与 Nvidia Blackwell 类似——在向量执行保持不变的基础上，专注于提升矩阵侧能力。

## 关键要点

- CDNA 4 CU 低精度矩阵吞吐翻倍，FP6 性能与 Nvidia B200 SM 持平
- 向量操作（FP32）保持 CDNA 3 的巨大优势，MI355X 仍比 B200 有更高整机向量算力
- LDS 从 64 KB 增至 160 KB，读带宽翻倍至 256 B/cycle
- 新增 LDS 转置读指令，配合矩阵乘法 row-major/column-major 转换
- GLOBAL_LOAD_LDS 指令扩展至最大 128 bits/lane（原为 32 bits/lane）
- XCD 保持 8 片架构，但 CU 数量略减（MI300X 每 XCD 38 CU → MI355X 更少，以提升良率与时钟）
- 内存升级 HBM3E：288 GB / 8 TB/s，领先 Nvidia B200 的 180 GB / 7.7 TB/s
- Blackwell SM 同样维持 Hopper 向量执行不变，两家均延续"胜利方程式"

## 链接到的概念

- [[computer-systems/cdna4-architecture]]
- [[computer-systems/cdna3-mi300x-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-cdna-4-architecture-announcement
- 本地：`raw/articles/chipsandcheese.com/2025-06-17_amds-cdna-4-architecture-announcement.md`
