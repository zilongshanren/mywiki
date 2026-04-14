---
tags: [渲染, 环境光遮蔽, 光照贴图, 老游戏]
date: 2026-04-14
sources: 1
---

# 预烘焙角落遮蔽（Pre-baked Corner Occlusion）

**Deus Ex（2000）** 在墙角和门框内侧有一圈明显变暗的阴影——比当时同类游戏看起来都要「有体积感」。这圈暗线不是 [[hbao-interleaved-sampling|SSAO/HBAO]]（当时 GPU 还做不到），而是**烘焙进光照贴图**的静态遮蔽，或者通过顶点色写进几何。

这种「把环境光遮蔽预先烘进静态 asset 里」的做法是屏幕空间 AO 时代之前的主流 workaround。它不需要运行时开销，但也只能处理静态几何之间的相互遮蔽；动态物体与场景之间的 AO 只能靠 fake（贴一张 blob shadow 在脚下）补足。

## Unreal Engine 1 的意外 bug

评论区里 *badsector* 指出，Deus Ex（基于 UE1）墙角那圈黑线其实**部分**源自 UE1 光照贴图器的一个 bug：烘焙时把多边形「外部」区域当成黑色填入，然后 blur 光照贴图去掉硬阴影边缘时，这团黑色**渗**进了可见区域的边缘。这不是艺术家主动做的 AO，而是烘焙工具链的副作用——但看起来像「角落被加重」，反而帮 Deus Ex 塑造出辨识度很高的画面。

badsector 说自己写的光照贴图器也有相同毛病：「光照贴图外的像素该填什么？」是一个容易被忽略但会影响边缘的问题；填零等于给整个 UV 边界都加了一道暗影。后来 Deus Ex: Human Revolution 把这种角落变暗作为**美术风格**延续了下来（尽管他们那时有 SSAO 了），相当于把 bug 升级成了 feature。

## The Sims 4 的混合方案

Simon Trümpler 观察到 Sims 4 在 [[hbao-interleaved-sampling|屏幕空间 AO]] 之上又叠加了一层**预置 AO 网格**（custom AO meshes）——在墙角等关键位置手动摆一张小 quad，上面贴一张径向衰减的 AO 贴图。SSAO 对窄角的响应经常不够强、不够整齐；手贴一块「补丁」能把角落那条暗线压得锐利又可控。

这个组合揭示了一个老问题的延续：**屏幕空间技术是对抽象的粗近似，而艺术家更想要可控的、形状正确的暗影**。与其等 SSAO 算对，不如在美术层补一块确定的几何。Sean Barrett 有一句被 Simon 引用的话：「AO is an abstraction, SSAO is a crude approximation of an abstraction。」预烘焙与手贴补丁是对这层抽象的另一条回路。

## 相关

- [[hbao-interleaved-sampling]] — 屏幕空间方案，与本技术互补
- [[voxel-ambient-occlusion]] — 体素场景下的离线 AO
- [[environment-probe-placement]] — 也属于「把场景光照预处理进 asset」的思路

## Sources

- [[sources/simonschreibt-deus-ex-occlusion]]
