---
tags: [渲染, gaussian-splatting, cli, 工具链, 格式转换, 3dgs]
date: 2026-04-19
sources: 2
---

# SplatTransform：3DGS 的 CLI 瑞士军刀

**SplatTransform** 是 PlayCanvas 2025-07 开源的 CLI 工具，用途是把 3DGS 数据的"格式转换 + 空间变换 + 过滤 + 合并"收进一条命令。它是从 [[supersplat-publish-platform|SuperSplat]] 可视编辑器里拎出来的那一块**批量和脚本友好的能力**——SuperSplat 适合手工清洗一个场景，SplatTransform 适合脚本批处理一千个场景。安装是 `npm install -g @playcanvas/splat-transform`，MIT 开源。

## 核心能力四件套

### 1. 格式互转

**支持的格式**：PLY、SPLAT、KSPLAT、SOG（以及无捆绑的 `.json` + `.webp`）、CSV。几乎覆盖了 3DGS 生态主流。

```bash
# 最基础的格式转换
splat-transform input.ksplat converted.ply

# 生成 SOG（单文件 .sog 容器）
splat-transform input.ply output.sog
```

对于从别的渲染器（例如基于 Mark Kellogg 的 three.js 插件的 `.splat`/`.ksplat` 工具链）迁到 PlayCanvas 的团队，这是**最轻的迁移入口**——不必重新训练，转格式就行。

### 2. 空间变换

在转换过程里直接做位姿调整——translate / rotate / scale：

```bash
splat-transform input.ply -s 0.5 -t 0,0,10 -r 0,90,0 transformed.ply
```

对于扫描-入库-对齐这种流水线很实用。

### 3. 多文件合并与各自变换

最有意思的设计：**同一条命令里多个输入文件可以各自带变换参数**，合成一个 merged 场景。

```bash
splat-transform inputA.ply -r 0,90,0 inputB.ply -s 2 merged.ply
```

这个语法等价于一个小型场景图——参数紧跟在各自的输入后面，而不是全局 flag。做大型展厅/展馆场景时，把单件家具 splat 拼到一个房间里就是这个操作。

### 4. 过滤与瘦身

```bash
# 去掉 NaN + 按属性过滤 + 裁 SH band
splat-transform input.ply --filterNaN -c opacity,gt,0.3 --filterBands 2 filtered.ply
```

- `--filterNaN` —— 清掉扫描产物里的数值异常。
- `-c opacity,gt,0.3` —— 条件过滤：只保留 opacity > 0.3 的 Gaussian，清掉"飞点"。
- `--filterBands 2` —— 把球谐砍到 2 阶；3DGS 文件里 SH 系数可以占到 75%，降阶是最直接的瘦身手段。

## CSV 导出：把 splat 当数据集

SplatTransform 支持把 splat 数据导出成 **CSV**——每个 Gaussian 一行、每个属性一列。这条路径的价值不在"渲染"而在"分析"：

- **用 Excel / Sheets 直接读**：做分布统计、相关分析、离群点检测，不用写代码。
- **接 Pandas / NumPy**：`pandas.read_csv(...)` 之后就是标准的数据科学入口。
- **喂给 ML 流水线**：训练 classifier 清洗数据、做聚类、segment by property。

把 splat 从"二进制黑盒"变成"可读的表格"——这是 SplatTransform 相对单纯的转换工具多出来的那一层**数据科学工位**。

## 在 3DGS 工具链里的位置

SplatTransform 不是跟 SuperSplat 竞争，而是填它的空位：

- **SuperSplat** —— 可视编辑，适合单场景手工打磨、对齐、裁剪。
- **SplatTransform** —— 命令行批处理、CI 流水线、格式桥接、数据探索。

两者共享 PlayCanvas 团队的格式栈（Compressed PLY + [[sog-compression-format|SOG]]），生成的输出可以直接被 PlayCanvas Engine / SuperSplat / PlayCanvas Editor 消费。2026-03 起 SplatTransform 又新增**生成 walk mode 需要的体素碰撞数据**，以及**从多份不同 LOD 的 PLY 生成 streamed SOG**——工具链的新功能第一站就是落到 SplatTransform。

## 相关

- [[sog-compression-format]] —— SplatTransform 的目标压缩格式
- [[supersplat-publish-platform]] —— 可视化对位
- [[gaussian-splatting-web]]
- [[will-eastcott]]

## Sources

- [[sources/playcanvas-splat-transform-cli]]
- [[sources/playcanvas-sog-opensource]]
