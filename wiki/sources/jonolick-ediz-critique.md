---
tags: [source, 图像处理, 上采样, 超分]
date: 2026-04-14
sources: 1
---

# EDIZ: A Critical Look at a Simplistic Image Upscaling Approach（Jon Olick）

[[jon-olick|Jon Olick]] 2024 年 1 月的文章，对 Saryazdi 等人提出的 EDIZ（Error Diffusion Image Zooming）简单图像放大算法做批判性拆解。

## 摘要

EDIZ 的做法是对原图先 downsample 再 upsample 得到重建图，用原图减重建图得"误差图"，加权叠加到常规上采样结果上作为最终输出。Jon Olick 从五个角度指出它的问题：**下采样已经丢失了高频信息**，单靠误差重分布无法恢复；**误差本身是复合失真**（混叠+插值误差），叠回去只会引入新误差；**缺乏理论基础**，更像启发式而非信号处理上站得住的方法；**没有生成新细节的机制**，只是在已有能量里倒腾；**可能引入伪影**，尤其在纹理密集区域。结论是它相对基于 ML 的 super-resolution 是"退步一步"，虽然便宜，但画质上无法竞争。

## 关键要点

- EDIZ 核心公式：原图 − （downsample → upsample）得到误差图，再加权到上采样结果上；
- 它只是**重新分配已有能量**，没有生成或推断新细节的机制；
- 误差项本身已经包含了下采样混叠 + 上采样插值的双重失真；
- 观察到的效果：边缘被"增强"但不是"变清晰"，没有新细节出现；
- 对比方向：基于 NN / GAN 的方法（参考 Jon Olick 自己的 jo_nn.h 实时 SRNN 实验）能真正生成合理细节。

## 链接到的概念

- [[ediz-upscaling-critique]]
- [[jon-olick]]

## 原文

- 链接：https://www.jonolick.com/home/ediz-a-critical-look-at-a-simplistic-image-upscaling-approach
- 本地：`raw/articles/jonolick.com/2024-01-09_ediz-a-critical-look-at-a-simplistic-image-upscaling-approac.md`
