---
tags: [渲染, 光照, 虚拟纹理, 体积纹理, 全局光照]
date: 2026-04-14
sources: 1
---

# 虚拟化体积纹理（Virtualized Volume Textures）

**把 2D 虚拟纹理的思路整体搬到体积纹理上**：用一张低分辨率的 indirection volume 做页表，把物理体积纹理切成 brick，按需从磁盘或实时生成加载，从而绕开「为了覆盖整个世界必须密铺一个高分辨率体积纹理」的巨大内存浪费。**[[brian-karis|Brian Karis]]** 在 2011 年初的一篇博文里把这个想法讲透——他当时在 Human Head 做 Prey 2 的照明研究，虚拟化体积纹理的目标是更高效地存储**辐照度体积（irradiance volume）**。

## 为什么 volume texture 需要虚拟化

irradiance volume 用体积纹理存储场景中每一点的球谐或小立方图光照，相对 lightmap 的好处是动态物体也能采样同一个解、不需要独立的 UV 参数化。代价是——**体积纹理很贵，而大部分体素落在空气里**。要想让实体表面附近的光照有足够分辨率，往往需要一张连空气都覆盖到的高频体积纹理，这在当时（2011）的硬件上完全不现实。

显而易见的反直觉观察是：空气里需要数据（供动态物体采样），但不需要和实体表面同样的分辨率。**我们希望空间能按「哪里有几何、哪里没有」自适应加细**。

## Indirection volume = page table

Karis 给出的直观解决方案是 2D 虚拟纹理的直接 3D 化：

- 一张**低分辨率的 indirection volume**（索引体积）充当页表。每个索引体素保存一个 brick 在**物理体积纹理**（volume texture cache）里的 `(x, y, z)` 起点。
- 物理体积纹理被切成固定大小的 **brick**（例如 8³ 或 16³）。
- 采样时：先按世界坐标查 indirection volume 得到 brick 的物理位置，再在物理 brick 内插值。和 [[id-tech|id Tech 5]] / Sean Barrett 的 2D 虚拟纹理管线概念完全一致。

所有 2D 虚拟纹理的限制也一视同仁地搬过来了：**brick 要留 border 来保证三线性过滤的正确性**；brick 越小，border 占比越高；brick 越大，页表越小但粒度越粗。三维下这个 border 开销因为是 $O(n^2 / n^3)$ 的形式所以比 2D 更痛。

## SVO 视角

另一种等价描述是**稀疏体素八叉树（SVO）**：页表管理换成八叉树、每个叶子节点存一个 brick。传统上 SVO 只用来做 ray casting、强调树遍历；但 Karis 指出——**只要你不是在单个 voxel 粒度工作，八叉树遍历就可以被折叠成一次索引纹理查询**，和 2D 四叉树虚拟纹理的页表查询没有本质区别。

SVO 框架的额外好处是**稀疏性更自然**：体积数据的稀疏度通常比 2D 纹理高得多——空气里根本不需要 brick，只需要**一个覆盖整个世界的根 brick** 给动态物体用。当物体走近实体表面时，按需 stream 进细粒度 brick。如果用屏幕空间 feedback 决定加载哪些 page，稀疏性完全是自动涌现的——甚至不需要提前烘焙、甚至不需要存盘。

## 现代工程继承

- **Smooth Mixed-Resolution GPU Volume Rendering**（VRVis, VG08）几乎就是 Karis 描述的方案：小 3D 索引纹理指向 3D cache texture 里的 brick。
- **GigaVoxels**（Crassin et al., 2009）把八叉树结构 + 反馈环路完整实现在 GPU 上，是后来 [[lumen|Lumen]] 的 Global SDF / Surface Cache 的重要先驱。
- Karis 本人 10 年后在 UE5 Lumen 里间接实现了类似的想法——静态场景的 Global Distance Field + Surface Cache 本质上就是一个**稀疏的、按需更新的、跨多分辨率级联的 volume cache**。

## 局限

- **高分辨率场合赢不了 lightmap**：当你真的需要每厘米级别的光照细节时，2D 参数化的 lightmap 仍然更省（只铺表面，没有 border 浪费）。
- **滤波 border 占比**在三维更严重，小 brick 不划算。
- **动态数据结构管理**：LRU、upload、defragmentation 都要自己写。

## 相关

- [[spherical-harmonics]] —— irradiance volume 最常见的每体素数据格式
- [[bindless-rendering]] —— 现代 volume cache 通常用 bindless 池管理
- [[greedy-voxel-meshing]]
- [[sdf-ray-marched-shadows]] —— SDF 也常以 brick 形式存储
- [[brian-karis]]

## Sources

- [[sources/karis-virtualized-volume-textures]]
