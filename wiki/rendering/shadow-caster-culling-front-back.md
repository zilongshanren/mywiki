---
tags: [渲染, 阴影, shadow-mapping, 优化]
date: 2026-04-19
sources: 1
---

# Shadow map 的 caster culling：front-face 还是 back-face？

[[shadow-mapping-basics|Shadow mapping]] 的第一步是从光源视角画一次深度图。问题来了：画这张图的时候要剔除哪一面三角形？两种答案各有代价，这是一道需要按游戏类型决定的**工程选择题**。

## 两种路线

**Front-face 投射（剔掉 back-face）**
从光源看，只有朝向光的那些三角形被写进 shadow map。

- ✅ 自然：地表的上表面、屋顶的上表面、墙朝光的那面正常投影。
- ✅ 允许 mesh 把**朝下的那半**（背面）去掉做「艺术家减面」，tabletop 的下面可以不存在。
- ❌ 容易出 **peter-panning**：阴影和投射物在接触点之间有一条亮缝，看着像物体悬空。bias 一大就更明显。
- ❌ 如果几何是「薄而自闭合」的（比如一张纸），两面深度几乎相同，自阴影会和「接收到的阴影」抢精度。

**Back-face 投射（剔掉 front-face / 即所谓 front-face culling）**
只有背向光的三角形写深度。参考 [LearnOpenGL 的 Shadow Mapping 教程](https://learnopengl.com/Advanced-Lighting/Shadows/Shadow-Mapping) 里介绍的做法。

- ✅ 天然消除 peter-panning——接触点的正面像素永远在「深度测试」里比背面更近，被判定为受光。
- ✅ 自阴影精度更好（朝光那一面完全不参与测试）。
- ❌ 闭合要求：**所有投射者必须是实心封闭 mesh**。一张单面的地板或一座只有上表面的桥会**完全不投影**。
- ❌ 会出 **light leak**：薄墙、门缝底下会漏光。

## Simon 的 Sacred 2 经验

[[simon-trumpler]] 在《Sacred 2》上的做法是 back-face 投射，所以组里不得不放弃「俯视游戏里桌子底面不做几何」这种常规艺术优化——**所有桌面、桥、栈板都要有底面**，否则阳光会从下穿过打在地面，等于桌子对着太阳变透明。作为交换他们拿到了干净的接触阴影，没有 peter-panning。

## 一个用于「单向窗户」的衍生后果

当外壳几何是**单面**的时（见 [[one-way-window-backface-culling]]），你只能用 **front-face 投射**：因为房子大墙的「背面」根本不存在，无法作为 back-face shadow caster。Simon 的推测是 Infinity Nikki 采取了这条路线——正好匹配它那个「从里往外被剔掉、阳光仍能穿过窗打进房间」的效果。

## 工程权衡汇总

| 场景 | 推荐 |
|---|---|
| 等距俯视、mesh 常省下表面 | front-face 投射 + 小心 peter-panning bias |
| 角色/厚实物多、希望自阴影干净 | back-face 投射，mesh 保持封闭 |
| 单面外壳、one-way 建筑 | 只能 front-face |
| 薄物多（布料、纸、栅栏） | 两端都难，考虑 VSM / MSM（见 [[moment-shadow-mapping]]）或 raytraced shadows |

## 相关

- [[shadow-mapping-basics]]
- [[one-way-window-backface-culling]]
- [[selective-shadow-fade-pass-switch]]
- [[cached-shadowmaps]]
- [[moment-shadow-mapping]]

## Sources

- [[sources/simonschreibt-nikki-one-way-window]]
