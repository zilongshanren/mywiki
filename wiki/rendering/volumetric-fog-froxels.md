---
tags: [渲染, 体积光, 雾, compute]
date: 2026-04-14
sources: 1
---

# Volumetric Fog with Froxels

**Froxel = frustum voxel**——即将相机视锥切成一个 3D 小格子体素网格，每个 voxel 在屏幕上占据一个 tile、在深度方向占据一段距离。这个数据结构是现代体积光与雾效的标准载体：把复杂的 ray marching 工作从 per-pixel 摊成一个 compute pipeline，按深度方向累积即可。Rise of the Tomb Raider 的 Foundation 引擎给出了一个经典实现。

## 为什么需要体积化

传统 fog 只是 per-pixel 的深度函数，做不到**光在雾里被散射**的效果——比如聚光灯在烟雾里形成的光束、阳光穿过树叶的光柱。要做到这些，必须在空间中离散地记录「某处有多少光，多少被散射回相机」。直接 per-pixel ray march 太贵；把空间预先离散化成格子、每个 voxel 只算一次，再在 per-pixel pass 里查表就便宜多了。

## ROTR 的三 pass 流程

ROTR 的 volumetric 纹理是 **160×90×64**（xy 是屏幕 tile，z 是深度切片），三个 compute shader 接力完成：

1. **光贡献收集 pass**：对每个 voxel，遍历覆盖它的（预先标记为「volumetric」的）光源，累积入射光量——就好像 voxel 里漂浮着的微尘粒子，每个粒子返回一部分光给相机。这一步依赖一个更粗的 40×23×16 tile grid 用来 cull 光源，就像 [[tiled-light-prepass|tiled light culling]] 但 3D 版本。
2. **小半径模糊 pass**：对收集好的光场做一次小半径模糊。ROTR 的 volumetric 分辨率很低（160×90），纯粹的离散化会让相机移动时产生 flicker——模糊把空间—时间稳定性都一起修掉。
3. **front-to-back 累积 pass**：从 voxel grid 的近面开始，沿 z 方向**累加**每个 voxel 的贡献。这一步等价于沿每条相机射线做积分，结果是「距离 d 之前累积的总散射光」，塞进同一个 3D 纹理的另一个通道。再做一次 blur。

完成之后 3D 纹理每个 voxel 都能回答「从相机出发走这么远，一路上进入眼睛的散射光是多少」。

## Per-pixel 查询

最终的全屏 pass 只做一件事——把屏幕像素的 UV + 深度转换成 voxel 坐标（3D），在 3D 纹理里做一次三线性采样，得到那一条射线上的 in-scattering，加到 HDR buffer 上。像素着色器总共只有约 **16 条指令**——所有复杂工作已经在 compute 阶段完成并摊薄到 voxel 分辨率上。

## 与其他 fog 的对比

Foundation 同时还有一个更便宜的 **lit fog**——不做 voxel grid，只用一张 cubemap 做 directional in-scattering 加上一条全局 attenuation 曲线。用于远景大气层染色效果。另外一些闭合区域的 god rays 则用手动放置的 billboard 假光柱，便宜但效果也好。

Froxel volumetric 留给真正需要光在 3D 空间里和几何交互的场景——比如 Lara 站在雾气里被一束聚光灯打穿的那种。

## 相关

- [[tiled-light-prepass]]
- [[deferred-rendering]]
- [[rendering-pipeline]]
- [[volumetric-raymarching-intro]] — 另一条体积渲染路线：per-fragment raymarching

## Sources

- [[sources/elopezr-rotr-rendering]]
