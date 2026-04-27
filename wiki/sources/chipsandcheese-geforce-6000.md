---
tags: [source, gpu, nvidia, geforce, shader, 历史架构, april-fools]
date: 2026-04-27
sources: 1
---

# Inside Nvidia's GeForce 6000 Series（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2025 年 4 月 1 日的 April Fools 文章，以戏谑口吻对 2004 年 NV40（GeForce 6000 系列）芯片进行了严肃的技术解析。

## 摘要

文章以"庆祝 2025 年，聊聊 GeForce 6 系列"为切入点，最后揭示这是 April Fools 彩蛋（"Wait, what year is it again?"）。但正文内容完全真实：深入分析了 NV40 的顶点着色核心（MIMD，3-way SMT，向量+标量双发射）与像素着色核心（SIMT，~256 线程向量，两级串联 128-bit 执行单元），以及 GPU 通用计算雏形（Brook API）。文章揭示了 GeForce 6 作为 GPU 可编程化转型节点的历史地位：ISA 与 DirectX 9 高度对齐，为后来 CUDA 奠定基础，同时指出 GPGPU 当时面临的内存访问与精度限制。

## 关键要点

- NV40：6 顶点着色核 + 16 像素着色核，IBM 130nm，>2 亿晶体管
- 顶点着色核：MIMD + 3-way SMT，向量/标量双流水线，512 条指令 RAM
- 像素着色核：SIMT（~256 线程向量），两级串联 FP32 单元，FP16 双倍吞吐
- L1（per pixel core）+ 全局 L2 纹理缓存，目标命中率 90%（非 CPU 式的 99%）
- 256-bit GDDR3，AGP + PCIe 支持
- Brook API 展示了早期 GPGPU 可能性，但受内存/精度/时序限制

## 链接到的概念

- [[nv40-geforce6-architecture]]
- [[rendering-pipeline]]

## 原文

- 链接：https://chipsandcheese.com/p/inside-nvidias-geforce-6000-series
- 本地：`raw/articles/chipsandcheese.com/2025-04-01_inside-nvidia-s-geforce-6000-series.md`
