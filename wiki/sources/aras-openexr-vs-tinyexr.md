---
tags: [source, 渲染, 图像压缩, 文件格式, openexr]
date: 2026-04-14
sources: 1
---

# OpenEXR vs tinyexr（Aras Pranckevičius / aras-p.info）

[[aras-pranckevicius]] 发表于 2025 年 11 月的短文，比较广受欢迎的单文件库 `tinyexr` 与「官方」OpenEXR 在体积、构建复杂度、读写速度上的取舍，并展示 OpenEXR 从 3.2 到 3.4.4 连续几版的瘦身成果。

## 摘要

tinyexr 的卖点是「一个 `.h` 就能用」，但代价是不支持 PXR24/B44/B44A/DWAA/DWAB/HTJ2K、深度图像，且性能落后。OpenEXR 官方库在 2015 年确实难编译，但 2025 年的 CMake 构建自动拉取依赖，体验已大为改观。作者借鉴 OpenUSD 里的做法——把 `src/lib/OpenEXRCore` + `external/deflate` 合并成单个 C 源文件，配合 nanoexr 这个极薄 C 包装——在单线程模式下跑一个「读入 + 2x 下采样 + 写回」的测试。六张 3840×2160 的 EXR 文件：tinyexr 6.55 秒、OpenEXR 3.2.4 2.19 秒、3.3.5 降到 1.68 秒（移除了巨大的 DWAA/DWAB 查找表）、3.4.4 稳在 1.65 秒。二进制体积从 3.2.4 的 2221 KB 一路瘦到 3.4.4 的 649 KB；如果再关掉 HTJ2K/DWA/B44/PXR24，最小可以压到 303 KB，已经比 tinyexr（251 KB）大不了多少，却快 3-4 倍且功能齐全。

## 关键要点

- **OpenEXR Core 可以当单文件库用**：OpenUSD 的 nanoexr 路径 + OpenEXRCoreUnity.h 合成一个 C 源文件，构建开销和 tinyexr 接近。
- **体积驱动的版本迭代**：3.3 删 DWA 查找表、3.4 删 B44 查找表，是 OpenEXR 团队真的在意依赖瘦身的证据。
- **特性是可编译剥离的**：HTJ2K、DWAA/DWAB、B44/B44A、PXR24 都可以通过构建开关一一拿掉，为「只要 ZIP 能跑就行」的场景留了下限。
- **性能差距大约 3-4 倍**：单线程下读+下采样+写 6 张 EXR，tinyexr 6.55 秒 vs OpenEXR 3.4.4 1.65 秒。tinyexr 的线程池模型（每次处理都新建/销毁）也是一个性能短板。
- **代码量对比**：tinyexr 726 KB 源码 vs 完整 OpenEXR 3.4.4 3216 KB；但真正要装进包里的也就几百 KB 的二进制。
- 暗示 tinyexr 的「上手简单」溢价在 2025 年已明显缩水，尤其对需要完整格式支持的工业管线。

## 链接到的概念

- [[openexr-format]]
- [[lossless-float-image-compression]]

## 原文

- 链接：https://aras-p.info/blog/2025/11/22/OpenEXR-vs-tinyexr/
- 本地：`raw/articles/aras-p.info/2025-11-22_openexr-vs-tinyexr-aras-website.md`
