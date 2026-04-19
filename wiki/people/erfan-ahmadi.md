---
tags: [人物, 作者, 渲染工程师, vulkan, the-forge, nabla]
date: 2026-04-19
sources: 3
---

# Erfan Ahmadi

渲染工程师，长期参与 [[Nabla|Nabla]] 开源 GPU 框架（Devsh Graphics Programming）的开发，主攻 [[rendering-api-depth|显式图形 API]] 下的同步、上传、内存与后处理。更早的个人项目是基于 [[the-forge-renderer|The Forge]] 的 **Bokeh Depth of Field** UnitTest，把 Kleber Garcia 的 [[circular-separable-dof|圆形可分离景深]]、GPU Zen 的 Practical Gather-based 景深、Dennis Gustafsson 的单 pass 景深三条路线在同一框架里平铺比较。

他的博客风格偏"给 Vulkan 老手看的说人话文档"——不怕贴代码、不怕直面 Vulkan spec 的晦涩（`optimalBufferCopyRowPitchAlignment`、`minImageTransferGranularity`、binary semaphore 模拟 timeline 等）。

## 相关

- [[Nabla|Nabla 框架]]（Vulkan 子端的开源 GPU 框架）
- [[the-forge-renderer|The Forge]]
- [[streaming-staging-texture-upload]]
- [[frames-in-flight]]
- [[circular-separable-dof]]

## Sources

- [[sources/erfan-ahmadi-texture-upload-staging]]
- [[sources/erfan-ahmadi-frames-in-flight]]
- [[sources/erfan-ahmadi-bokeh-dof-project]]
