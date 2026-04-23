---
tags: [渲染, 坐标, 浮点精度, 引擎架构]
date: 2026-04-19
sources: 1
---

# 大世界与 32-bit float 的坐标精度

当一个 3D 世界大到以公里、甚至地球尺度计量时，世界空间坐标会被推出 32-bit float 的可用精度范围。摄像机远离 origin 时先丢低位，再丢高位，最终出现**顶点抖动**（jittering）、**Z-fight**、**mesh cracking** 等症状。这是所有开放世界、飞行模拟、宇宙尺度游戏都必须解决的同一个问题。

[[ben-supnik|Supnik]] 在 2010 年总结了 X-Plane 当时面对的三条路，以及各自的成本：

## 方案一：停世界 → 整体 transform

把所有 mesh 的坐标减去一个偏移（或乘一个变换），把 origin 重新拉回观察者附近。X-Plane 当时采用的就是这种 "stop the world"，用多线程配合。真正的瓶颈不是 CPU：mesh 大量常驻 GPU，变换必须**从 VRAM 拖回 CPU**，PCIe 带宽成为上限。Transform feedback 能留在 GPU 上做，但 Supnik 说早期驱动对「写回已存在于显存的 buffer」路径往往表现很差。

## 方案二：双缓冲整个世界

保留两份世界，后台线程在第二份上做好变换，前台一个 swap 切过去。**切换成本接近零**，但内存占用翻倍——在 2010 年的消费机上不现实。

## 方案三：局部坐标系 + 层级变换

每个 tile / 区块使用自己的局部坐标系，只维护「局部到全局」的变换矩阵。移动时只改几个矩阵，mesh 数据原地不动。

这个方案的难点是**接缝**：两个相邻 tile 在各自局部空间下的「同一条共享边」经过不同 matrix 变换后，经过浮点误差未必会落到同一个设备像素，产生 1 像素 crack。Supnik 在评论区的 follow-up 给出一个「3a」优化：

- 每个顶点带上它所属局部坐标系的编号；
- Vertex shader 有全部 transforms 的访问权限，可处理「异质 transform 的三角形」；
- **边界三角形的边顶点统一用相邻 tile 中 master 那一侧的坐标系与 transform**，这样接缝处不会因为使用不同矩阵出现裂缝。

代价是每顶点多一个 index，以及更复杂的 shader。

## 业界的其他做法

评论区提到的相关实践：

- **Dungeon Siege**：Scott Bilas 的经典方案「there is no world space」——世界里压根没有一个全局坐标系，所有东西都是相对的。
- **Tom Forsyth**：对象位置用整数而非 float 存储，浮点只在渲染时用。
- **Scene graph 用 double，只在 draw 时转 float**：在 CPU 上做 `double(Model) * double(View)`，结果转 float 送 shader；光照一律在 view space 算。实现简单、精度够用。
- **24 字节编码顶点位置**：用两组 float 组合模拟 double，vertex shader 里重建高精度位置；vertex buffer 翻倍但永远不用再动。

## 相关

- [[coordinate-spaces]] — world space 的存在本身就是图形管线标准分层
- [[ben-supnik]]

## Sources

- [[sources/supnik-scroll-opengl-world]]
