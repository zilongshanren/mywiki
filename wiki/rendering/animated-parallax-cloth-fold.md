---
tags: [渲染, shader, parallax, 法线贴图, 布料, deus-ex]
date: 2026-04-14
sources: 1
---

# 用动画 parallax 伪造会动的布料褶皱

《Deus Ex: Human Revolution》开场的奥运风旗上印着一条缓缓滚动的布料褶皱——表面像被风鼓起又松下，褶皱从右上方慢慢滑向左下。直觉会告诉你这是「顶点动画 + 法线贴图」，但 [[simon-trumpler|Simon Trümpler]] 用 Intel GPA 抓帧后发现：**整面旗的 mesh 几乎没有三角形密度，顶点在游戏时完全不动**。他一开始以为是 UV 动画 + 滚动 tileable 法线贴图，但 wireframe 里 UV 岛也基本不变。那这波「动」到底来自哪里？

答案是 **animated parallax mapping**（即视差贴图）——一项通常用于静态细节的技术在这里被用来做循环流动的布料。底层输入是：

1. 一张**静态** object-space normal map，定义整面旗最终的「大致褶皱形状」。
2. 一张非常小（几十像素）的**灰度高度噪声纹理**，其上被 scroll 进来的 UV 缓慢平移。
3. parallax shader 把这张噪声图当高度场，**按视线方向做 bump offset**，使得 diffuse 采样像是从一个连续变化的高度表面上打出来的。

把 noise 按 scroll 的速度滑动，等价于「这块布的高度场本身在时间里演化」。由于 parallax 影响的是 **UV 采样位置**而非几何，我们看到的只是 diffuse 贴图被一个缓慢流动的位移场抽搐，但观感上大脑会把它解读成「有起伏的布料正在被风吹动」。Simon 最初之所以搞错，是因为 debug 里发现「关掉纹理过滤」时 noise 图显示为一大堆像素马赛克——他原本以为是 bug，但其实游戏把一张低分辨率 noise 放大成了高频高度场，**靠 bilinear filter 把锐利的像素边界糊成连续的 half-sphere 凸起**。换句话说：高精度 parallax 效果是用「小图 + 双线性」换来的，不需要烘焙大张高分辨率置换贴图。

这招在同时代的游戏里有好几例平行发明：

- **Batman: Arkham City** 的旗帜做了同一件事，甚至再进一步——虽然顶点不动，但他们对 silhouette 做了额外的 mask，在旗下沿允许轮廓被「推出去」一点点看起来像真的在飘。这么做的前提是镜头不会从侧面看；一旦你站到旗子侧后方，动画瞬间破功。
- **Deus Ex** 自己用的是灰度高度图 + reconstructed 法线。
- **Mirror's Edge** 的脚手架防尘布也是同一个 trick；当 PhysX 开启时会切换成真正的布料模拟，否则就走这条 animated parallax 路径。

可以把这种方法理解为**以时间为 UV 的视差贴图**：静态的 mesh + 静态的 object-space normal + 会动的 heightfield + 运行时 bump offset，四个组件共同欺骗你眼睛里那个「这面布在飘」的感知器。它的强项在于：

- **正面看时极度便宜**。per-pixel 一次 parallax 采样，没有任何 CPU、没有任何物理。
- **侧面看立即穿帮**。所有「仅靠纹理动起来的布」都有同一个弱点——正交视角下 mesh 没厚度变化，直接裸奔。
- **噪声图可以极小**。`16×16` 足矣，靠 filter 模糊成高频高度场。
- **对艺术家调参友好**。速度、方向、幅度都是 shader 参数；换一张 noise 就换一套褶皱节奏。

这套思路和 [[animated-uv-scrolling-water]]、[[flow-map-directed-advection]] 是同一族：**让时间流进贴图坐标，便宜地伪造物理模拟**。

## 相关

- [[parallax-occlusion-mapping]] —— 通用版 parallax 技法，本条是它在动画域的应用
- [[flow-map-directed-advection]] —— 以 flow map 为驱动的同类 UV 动画
- [[animated-uv-scrolling-water]]
- [[normal-decal-edge-blending]]

## Sources

- [[sources/simonschreibt-deus-ex-folds]]
