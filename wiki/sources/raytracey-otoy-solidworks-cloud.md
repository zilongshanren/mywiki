---
tags: [source, 云渲染, 云游戏, OTOY, GPU]
date: 2026-04-19
sources: 1
---

# OTOY 与 SolidWorks：RV770 GPU 云渲染细节（Sam Lapere / Ray Tracey's blog）

[[sam-lapere|Sam Lapere]] 于 2010-03-02 转载的 upfrontezine 采访。OTOY 的 Jules Urbach 向记者讲了他们在 SolidWorks World 2010 云 CAD 演示背后的硬件/软件架构，给出了这一代云渲染工程**具体的延迟预算、GPU 规格和编码吞吐**——远比 OTOY 官网市场语言有信息量。

## 摘要

SolidWorks 在 2010 年展会上演示云端 CAD 但对媒体闭口不谈技术细节；幕后是 OTOY 提供的云渲染方案。Urbach 对延迟问题的工程拆解是：总延迟由带宽、距离、分辨率/压缩率、服务器算力组成。OTOY 以 AMD **RV770**（800 stream processor、2 GB / 256-bit 显存、115 GB/s）为核心，在软件侧做极致压缩、在硬件侧以"每 vector core 几分钱"的成本把像素算力打下来。实测能做到 **3840×2160 实时编码**，1080p 下**每毫秒一帧**（1000 fps 编码能力）——为整条云流水线腾出延迟预算。Urbach 把合格游戏体验的延迟阈值设在 16 ms、对应约 1000 mile 服务器半径；SF-NY 85 ms，SF-日本 100 ms。因此他强调类似 Akamai 的边缘分发拓扑才是真正的解。

## 关键要点

- OTOY 2010 的 GPU 选型：AMD RV770（HD 4800 系列核心）——靠 800 个便宜 stream processor 摊薄每像素成本
- 编码吞吐数字：1080p 1 ms/帧（1000 fps 编码能力），可实时编到 4K（3840×2160）
- 延迟预算：目标 ≤16 ms，对应服务器半径约 1000 mile
- 分发拓扑与 Akamai 类比：**物理距离是解不掉的，只能往用户侧推节点**
- 云游戏是更大愿景的子集：Urbach 还提到把 BluRay 视频/菜单通过云流到 iPhone

## 链接到的概念

- [[otoy-cloud-rendering]]
- [[gpu-unbiased-path-tracing]]
- [[sam-lapere]]

## 原文

- 链接：http://raytracey.blogspot.com/2010/03/otoy-teams-up-with-solidworks.html
- 本地：`raw/articles/raytracey.blogspot.com/2010-03-02_otoy-teams-up-with-solidworks.md`
