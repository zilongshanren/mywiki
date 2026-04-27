---
tags: [gpu, rendering, qualcomm, adreno, mobile, wave128, tiled-rendering, snapdragon]
date: 2026-04-27
sources: 1
---

# Adreno 640 架构

Adreno 640 是高通 Snapdragon 855（2018 年，TSMC 7 nm）的集成 GPU，属于 Adreno 6xx 系列。相较前代 Adreno 530（Snapdragon 821，Samsung 14 nm），Adreno 640 大幅提升算力，但在极度受限的移动功耗预算下采用了一系列非常规设计决策。

## 核心架构变化

### Shader Processor 重组

Adreno 530 有 4 个 Shader Processor（SP），各 SP 拥有独立的 Local Memory 和内存接口。Adreno 640 将 SP 数量扩展至 6 个，但将资源共享推进一步：每三个 SP 编为一组（推测对应一个 CCU，Color Cache Unit），组内共享 Local Memory（32 KB/组）和外部内存接口；只有执行单元和 L1 Texture Cache（1 KB）保持 SP 私有。

这种重组让高通在不成比例地增加支撑逻辑面积的前提下提升了执行单元数量——典型的"晶体管预算极限优化"。

### Wave128：极宽向量宽度

Adreno 640 采用 wave128（每 wave 128 个 32 位 lane），比 AMD GCN 的 wave64 宽一倍，比 AMD RDNA 和 Nvidia 的 wave32 宽四倍。更宽的 wave 意味着每条指令的 fetch/decode/schedule 开销被摊薄到更多计算单元上，降低前端成本。

代价是分支发散（branch divergence）的惩罚翻倍：当 128 个 lane 中部分走不同分支路径时，必须串行执行两侧，无效 lane 更多。这在通用计算（如 FluidX3D 流体仿真）中造成严重性能退化，甚至不如 Adreno 530。

寄存器文件容量 64 KB/SP，仅够 16 个 wave128 线程各分配 8 个寄存器，明显小于 AMD RDNA2 的 128 KB（可分配 32-64 个寄存器/线程）。复杂着色器可能因此遭遇低占用率（low occupancy）。

## 时钟频率退步

出人意料地，Adreno 640 的时钟从 Adreno 530 的 653 MHz 降至 585 MHz（下降 10.4%）。这是主动权衡：在 7 nm 工艺下，更低的频率换取更低的动态功耗，同时 7 nm 本身已带来大量晶体管效率提升。最终结果是算力大幅提升而热功耗保持合理，Snapdragon 855 在无主动散热的手机中保持 585 MHz 全速运行而温度低于 70 °C。

## 缓存层次

- **L1 Texture Cache**：1 KB/SP，只读，非一致；所有 Adreno GPU 通用值
- **L2 Cache**：128 KB 全 GPU 共享，与 Adreno 530 相同容量；约 47 周期延迟
- **Local Memory**：64 KB 总量，每组（3 SP）32 KB，需软件显式管理
- **GMEM**：1 MB 专用 Tile Buffer，支持 Tile-Based Deferred Rendering

L2 带宽相比 Adreno 530 翻倍，且与 Local Memory 带宽几乎相当——在通常 L2 带宽远低于 Local Memory 的 GPU 设计中属罕见情况。

## 光栅化性能

Tiled Rendering 是 Adreno GPU 的传统优势。几何体先按 tile 分类，每 tile 渲染期间数据驻留在 GMEM 中，避免大量帧缓冲读写回主存。3DMark Slingshot Extreme 测试下，Adreno 640 的 GPU 内存带宽极少超过 10 GB/s（Adreno 730 约 20 GB/s），说明 tiling 有效控制了带宽需求——这在 64 位 LPDDR 总线宽度下尤为重要。

L1 Texture Cache 命中率达 68%，L2 捕获 >90% 的 L1 缺失，caching 效果优秀，与 [[tiled-rendering]] 相互增益。

## 后记：Adreno 730 的部分回退

高通在 Adreno 730（Snapdragon 8 Gen 1）上撤回了部分 Adreno 640 的激进决策：向量宽度从 wave128 收回至 wave64，Local Memory 恢复 SP 私有。这是对 wave128 在通用计算场景下发散惩罚过高的承认，也印证了 Adreno 640 的某些设计选择超出了合理平衡点。

## Sources

- [[sources/chipsandcheese-snapdragon855-igpu]]
- [[sources/chipsandcheese-sde-adreno]]
