---
tags: [渲染, 体素, 纹理, gamemaker, lut]
date: 2026-04-19
sources: 1
---

# 用 2D 纹理拼出 3D 体素 LUT

许多 2D 为主的引擎（典型代表 [[game-engine|GameMaker]]）既没有 **3D texture** 也没有 **Shader Storage Buffer Object**，但只要有一张 2D 纹理，就可以把一个可编辑的体素世界塞进去。Xor 在 *GM Shaders: Voxels 2* 里给出的做法很朴素：**把 3D 世界按 z 层铺开，每层作为一块子区域拼在同一张 2D 纹理上**——读写时再把 3D 坐标换算回 2D UV。

## 核心布局

设世界大小 `RES.xy = (cell_w, cell_h)`，层数沿两个方向拆分 `RES.zw = (cols, rows)`，则纹理真实尺寸是 `(cell_w * cols) × (cell_h * rows)`。一个 64×64×64 的世界用 8×8 的层布局，只要一张 512×512 纹理；想更大就横向 / 纵向多拼几层，最大可以塞到约 1024×1024×256（上限是 GPU 的 16k 纹理边长）。读法是「从左上开始、像读一本书一样按行走到右下」——对应代码里的行优先布局。

概念上它是一个 **4D 数据结构**：需要 cell 宽、cell 高、横向 cell 数、纵向 cell 数 四个参数才能定位任一 voxel。

## 地址转换

核心两个函数：

```glsl
vec3 uv_to_block(vec2 uv) {
    vec2 p  = floor(uv * RES.xy * RES.zw);   // 像素坐标
    vec2 xy = mod(p, RES.xy);                // 子 cell 内部 x/y
    vec2 zw = mod((p - xy) / RES.xy, RES.zw);// 属于哪一块 cell
    float z = dot(zw, vec2(1, RES.z));       // 把 (col,row) 压回 z
    return vec3(xy, z);
}
vec2 block_to_uv(vec3 b) {
    b.z = clamp(b.z, 0.0, RES.z * RES.w - 1.0);
    vec2 sub  = fract(b.xy / RES.xy) / RES.zw;
    vec2 cell = fract(floor(b.z / vec2(1, RES.z)) / RES.zw);
    return sub + cell;
}
```

`uv_to_block` 把采样点还原成 3D voxel 索引——它是 [[raymarching-intro|raymarching]] 里每一步 DDA 查询时的入口。`block_to_uv` 反过来，编辑器放置方块时用来写 render target。本质是两个 `mod` 拆解出「子 cell 位置」和「cell 索引」，再把后者线性化为 z。

## 为什么选 LUT 而非 SSBO

- **可编辑**：纹理既可作为 shader 输入采样，也可以作为 render target 写入，编辑操作（鼠标点击放置 / 破坏方块）就是对这张 LUT 的单点覆盖绘制。
- **跨引擎**：3D texture 在 Web、移动、老版本 OpenGL 里兼容性参差，2D 纹理到处都有。
- **便于持久化**：LUT 本身就是一张图，可以直接存盘或作为关卡资产打包。

代价是每次采样多几条 `mod / floor` 指令，以及地图尺寸受纹理最大边长约束——对 Minecraft 规模的 chunk 够用了。

## 和相关概念的关系

- **生成 vs 存储**：Xor 的 voxels-1 讲用 **DDA** 在公式生成的体素上做 raytrace；这篇补齐了**持久化和可编辑**那一半——公式只能画山坡，LUT 才能让玩家挖洞。
- **压缩 / mesh 化**：如果要从 LUT 出发生成可见面，可以接到 [[greedy-voxel-meshing]] 做一次贪心合并，再配 [[voxel-ambient-occlusion|烘焙 AO]] 得到 Minecraft 风格的最终管线。
- **DDA 搭档**：LUT 只是存储后端，raymarch 时仍然用 DDA 按格步进，每步 `uv_to_block + block_to_uv` 查询占用位。

## 相关

- [[raymarching-intro]]
- [[greedy-voxel-meshing]]
- [[voxel-ambient-occlusion]]
- [[color-lut]]
- [[texture-swizzle-nested-tiling]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-voxels-2]]
