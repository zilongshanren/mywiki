---
tags: [source, D3D12, root-signature, shader编译, 渲染]
date: 2026-04-27
sources: 1
---

# Shapes and Forms of DX12 Root Signatures（Adam Sawicki）

[[adam-sawicki]] 发表于 2024 年 5 月的文章，系统梳理了 Direct3D 12 根签名（root signature）的所有存储格式及相互转换路径。

## 摘要

Root signature 是描述管线各着色器阶段资源绑定的数据结构，是 D3D12 显式资源管理体系的核心。文章以一个简单 VS+PS shader 为例，完整梳理了根签名的六种"表示形式"并展示了它们之间的互转路径：①`D3D12_ROOT_SIGNATURE_DESC` C++ 数据结构、②通过 `D3D12SerializeRootSignature` 序列化后的二进制 blob、③`ID3D12RootSignature` GPU 对象、④内嵌在编译好的 shader binary 中、⑤HLSL `#define` 宏文本格式、⑥通过 DXC 编译该宏生成的独立二进制文件。文章还介绍了 DXC 命令行工具和 Radeon GPU Analyzer（RGA）如何在这些格式之间转换，以及 DXC 库 API（IDxcCompiler3、shader reflection）的编程用法。最后讨论了"一个大根签名 vs. 按 shader 切换"的工程权衡，并援引 Cyberpunk 2077 和 Frostbite 引擎使用单一根签名的实践。

## 关键要点

- 根签名有六种表示，序列化二进制（#2）是贯穿所有表示的"公共货币"
- HLSL 文本格式（`#define` 宏 + `[RootSignature()]` 属性）是最可读的写法，DXC 可直接将其编译为二进制
- `D3D12CreateRootSignatureDeserializer` 可将序列化 blob 反序列化回 C++ 结构
- DXC 的命令行参数设计混乱（如 `-E` vs `-rootsig-define`、`-Fo` vs `-Frs`），需特别注意区分
- Shader reflection（`IDxcUtils::CreateReflection`）可自动生成与 shader 兼容的根签名，但只有一种可能的布局
- PSO 中如果多个 stage 嵌入了不一致的根签名，创建会报错
- 实际工程中"全局大根签名"是可行策略，AAA 游戏已有先例

## 链接到的概念

- [[d3d12-root-signature]]
- [[d3d12-resource-binding]]
- [[bindless-rendering]]
- [[advanced-shader-delivery]]

## 原文

- 链接：https://asawicki.info/news_1778_shapes_and_forms_of_dx12_root_signatures
- 本地：`raw/articles/asawicki.info/2024-05-14_shapes-and-forms-of-dx12-root-signatures.md`
