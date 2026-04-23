---
tags: [字体渲染, gpu, bezier, 矢量渲染]
date: 2026-04-19
sources: 1
---

# Slug：GPU 直接光栅 Bézier 字形

Eric Lengyel 2017 年在 JCGT 发表的 "GPU-Centered Font Rendering Directly from Glyph Outlines" 算法。**它让 GPU 直接从 Bézier 轮廓光栅化字形**——不走 texture atlas、不走 multi-channel SDF 中介——能在任意投影变换下做 pixel-perfect 渲染。论文原本被申请了专利，2026 年 3 月 Lengyel **提前 12 年把专利捐到公共领域**，[[warren-moore|Warren Moore]] 立刻发表了在 Metal 上的最小实现。

## 解决了什么问题

GPU 直接光栅 Bézier 的两个历史障碍：

1. **数值稳健性**：判断 pixel 是否在 glyph 内需要对二次方程找根，浮点精度下射线扫描容易抖动、开裂，尤其在动画 / 投影变换下
2. **视觉保真**：二值 in/out 判定产生锯齿

Slug 对前者用一套专门的**二次方程根分类**方法（2018 I3D presentation 详述），稳健性足够支撑任意投影。对后者用**分数覆盖计算**：每像素给出被 glyph 覆盖的比例，自然抗锯齿。

## 核心算法

### 1. Winding number + nonzero rule

TrueType glyph 由**二次 Bézier 样条**组成（OpenType / Type 1 可能是三次）。给每条闭合曲线定方向（逆时针正），从采样点向外发射线，每个交点按局部曲线方向贡献 ±1。所有贡献之和非零则点在内部（nonzero rule）。

### 2. 双射线消除退化

完全水平 / 垂直的线段让单射线判定失效。Slug 同时算**水平和垂直两方向射线** coverage 再合并。完全水平的线段不计入水平 band、完全垂直的不计入垂直 band。

### 3. Bands 加速

brute-force 每采样点对所有曲线段做计算太贵。预处理：把 glyph 切成**水平 bands 和垂直 bands**（两组矩形 slab），每条曲线段分配到与其包围盒相交的所有 band。采样时只看所在 band 的曲线段——平均每采样只处理少量曲线。

### 4. Dynamic Dilation（2019 扩展）

极小字号时窄特征可能因为采样不够消失（类似纹理 minification 没 mipmap）。Slug 用 MVP 精确推出 glyph 包围矩形，保证任何可能覆盖到 pixel 的曲线段都被光栅化到。

## GPU 实现骨架

维护每 typeface 一个 **font atlas**，两张纹理：

- **band texture**：每个 (水平 / 垂直) band 里的曲线索引
- **curve texture**：Bézier 控制点的实际坐标

Shader inner loop：

1. 找到 pixel 在哪个水平 band，算 X 维 coverage
2. 找到垂直 band，算 Y 维 coverage
3. 合并得总 coverage × glyph color 作为 fragment 输出

Warren 的 Metal 实现：text layout / shaping 交给 **Core Text**（等价于 Harfbuzz / Uniscribe / DirectWrite），处理 ligature / bidi / 连字脚本 / combining characters / hinting；shader 约 200 行 MSL；GitHub `metal-by-example/MetalSlug`、Apache 2.0。

## 为什么是"最终答案"

- **不依赖 texture atlas**：缩放 / 倾斜 / 任意投影都不丢分辨率
- **不依赖 SDF**：没 SDF 的连锁伪影
- **pixel-perfect 分数覆盖**：小字号也能清晰
- Bands 加速让性能可接受
- Core Text 等成熟 shaping lib 负责复杂书写系统

## 限制 / 工程注意

- Warren 样例不支持 emoji（emoji 是 raster / svg / sbix glyph，不走 outline 路径）
- 每 run 一次 draw call，正式版应合并同资源 run
- Font atlas 一 typeface 一个，可合并成 atlas array
- Dynamic dilation 数学要仔细——Warren 承认自己实测没看出明显差别，疑似公式写错

## 相关

- [[bezier-curve-triangulation]]
- [[analytical-antialiasing]]
- [[metal-api-overview]]
- [[sdf-2d-primitives]]
- [[warren-moore]]

## Sources
- [[sources/metalbyexample-slug]]

## 相关

- [[screen-space-curve-tessellation-cutoff]] — 在 CPU-side tessellation 路线里用屏幕空间阈值控制 Bézier 细分密度，是 GPU 直接光栅化之前的代表性做法
