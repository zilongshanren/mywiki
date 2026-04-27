---
tags: [gpu, nvidia, geforce, 渲染管线, shader, 历史架构, rasterization]
date: 2026-04-27
sources: 1
---

# NV40 与 GeForce 6000 系列架构

NV40 是 Nvidia 于 2004 年推出的 GeForce 6000 系列旗舰芯片，也是早期可编程 GPU 的标志性设计之一。Chester Lam 在 Chips and Cheese 以"April Fools 逆向考古"的风格深度解析了这颗芯片的内部结构。

## 总体架构

GeForce 6 系列将顶点着色器（Vertex Shader）与像素着色器（Pixel Shader）分开设计，各自针对不同的并行特性进行了优化。NV40 最高配置拥有 6 个顶点着色核心与 16 个像素着色核心，使用 IBM 130nm 工艺，晶体管数量超过 2 亿，内存子系统支持最宽 256-bit GDDR3。系统接口支持 AGP 与 PCIe。

## 顶点着色核心（MIMD）

顶点着色核心采用类 CPU 的 MIMD 执行模型，同时跟踪最多 3 个硬件线程以隐藏纹理采样延迟。其 ISA 与 DirectX 9 Vertex Shader 3.0 紧密对齐，支持分支、循环和函数调用。指令布局将标量与向量操作拆分到两条并行流水线，实现指令级双发射。单核配备 512 条指令 RAM（约 8 KB），无需 tag 比较，节省功耗。

## 像素着色核心（SIMT）

像素着色核心采用早期 SIMT 模型，将多个像素调用组织为一个向量并行执行。GeForce 6 的像素着色器建议将分支保持在超过 1000 个像素（约 256 个 2×2 quad）的区域内一致，否则两侧分支均须执行并用 mask 关闭不活跃线程。

像素核心的执行管线具备两级 128-bit 向量单元串联结构：上级处理特殊函数与纹理寻址，下级执行 FMA；两级依赖指令可"双发射"。FP16 执行可倍增吞吐，同时降低寄存器文件占用，进而提升 occupancy 与延迟隐藏能力。

每个像素着色核心拥有独立 L1 纹理缓存，全 GPU 共享 L2 纹理缓存，Nvidia 目标命中率约 90%（相比 CPU 缓存常见的 99%）。

## 通用计算的萌芽

GeForce 6 大量的并行计算能力开始被用于非图形领域。Stanford 的 Brook API 提供了一套面向 GPU 的流式并行编程模型，成为后来 CUDA 的早期实验。像素着色器也首次被用于实时光线追踪实验（简单场景）。然而，着色器只能通过纹理访问内存、不能修改正在绑定的纹理、精度不足 IEEE 754 等限制，制约了 GPGPU 的普及。

## 历史意义

GeForce 6 代表了 GPU 从固定功能向可编程过渡的关键一步，Nvidia 的 ISA 设计高度贴近 DirectX 9 HLSL，保证了游戏的向后兼容性。可编程像素着色器与 PCIe 的组合，为 2006 年 CUDA 的诞生奠定了基础。

## Sources

- [[sources/chipsandcheese-geforce-6000]]
