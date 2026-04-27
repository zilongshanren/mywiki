---
tags: [渲染, directx12, root-signature, 资源绑定, 显式api]
date: 2026-04-27
sources: 1
---

# D3D12 根签名（Root Signature）

根签名是 Direct3D 12 中描述渲染管线所有着色器阶段资源绑定布局的数据结构，是 [[d3d12-resource-binding]] 体系的核心接口之一。它等价于 Vulkan 中的 `VkPipelineLayout`（通过 `VkDescriptorSetLayout` 组合而成）。

## 根签名的作用

着色器在执行时可以访问常量缓冲（CBV）、纹理（SRV）、可读写缓冲（UAV）和采样器（Sampler），这些资源绑定到哪些 register slot、以何种方式传递（root constant、root descriptor 或 descriptor table）、哪个 shader stage 可见——这一切都由根签名在 PSO 创建之前声明。

根签名的三种根参数类型：

| 类型 | 特点 |
|------|------|
| Root Constants | 直接内联 32-bit 值，无需 descriptor，延迟最低 |
| Root Descriptors | 直接内联 GPU VA，一级间接，适合 CBV/SRV/UAV |
| Descriptor Table | 指向 GPU 可见堆中的连续描述符区间，两级间接，适合批量绑定 |

## 六种表示形式

Adam Sawicki 在 2024 年的文章中梳理了根签名的完整表示体系：

1. `D3D12_ROOT_SIGNATURE_DESC` — C++ 数据结构，人类可读但冗长
2. 序列化二进制 blob（`D3D12SerializeRootSignature` 输出）— 格式同 DXBC，188 字节典型大小
3. `ID3D12RootSignature` GPU 对象 — 通过 `CreateRootSignature` 创建，用于挂载到 PSO
4. 内嵌于编译 shader binary 中 — 通过 `[RootSignature(MyRootSig)]` 属性绑定后由 DXC 打包
5. HLSL 文本格式（`#define` 宏）— 最可读，可由 DXC 直接编译为二进制
6. 通过 DXC 将 HLSL 文本编译出的独立 `.bin` 文件

各格式之间可通过 DXC 命令行（`-extractrootsignature`、`-setrootsignature`、`-T rootsig_1_0`）以及 `D3D12CreateRootSignatureDeserializer` API 互相转换。

## 工程权衡：一签还是多签

理论上每个 shader 应有精确匹配的根签名以节省根参数槽位，但切换根签名有 CPU 和 GPU 开销。Cyberpunk 2077 和 Frostbite 引擎的做法是：图形 shader 全局一个大根签名，compute shader 另一个。这在实践中被证明足够高效，说明过度精细化的根签名并非必要。

## Shader Reflection 自动生成

DXC 库的 `IDxcUtils::CreateReflection` 接口可通过读取编译好的 shader binary 自动生成一个兼容的根签名，适合引擎自动化资源绑定场景。但自动生成的根签名只是众多可行布局之一，不一定符合工程需求。

## 相关

- [[d3d12-resource-binding]]
- [[bindless-rendering]]
- [[d3d12-resource-alignment]]
- [[advanced-shader-delivery]]

## Sources

- [[sources/asawicki-dx12-root-signatures]]
- [[sources/graphics-guy-d3d12-intro]]
