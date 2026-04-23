---
tags: [字体渲染, bezier, 反走样, cpu-tessellation]
date: 2026-04-19
sources: 1
---

# 屏幕空间自适应曲线细分阈值

CPU 侧把 Bézier / 二次抛物线弧线拆分成线段再交给 GPU 光栅化，是 [[slug-gpu-glyph-rendering|Slug]] 这类「GPU 直接光栅轮廓」出现之前的主流做法。递归细分的终止条件是「弧与其弦的中点距离是否够小」——关键是「够小」到底用什么尺度衡量。

Patrick Stein 在 2010 年 CL-OpenGL + ZPB-TTF 的字形渲染里指出一个常见错误：**直接和常数 1 比较**。在模型空间里「1 个单位」和屏幕上一个像素之间没有固定换算，当文字被缩得很小时，算法会在同一个屏幕像素内塞进几十个顶点（他实测一条抛物线弧可以贡献 63 个），最终像素颜色被这些重叠顶点反复叠加，反走样退化成「比实际覆盖更实心」的字形——细节糊成一团。

## 正确的 cutoff

正确做法是把判断阈值换成**当前屏幕一个像素对应的模型空间距离**，并在每次 `glScale / glLoadMatrix` 变化后重算一次：

1. 用 `glGetDoublev` 拿到当前 modelview、projection、viewport
2. `gluUnProject` 把屏幕空间的原点和相邻两个单位点（(1,0,0)、(0,1,0)）反投影回模型空间
3. 取反投影后到原点的最小距离的一半——这就是「半个像素对应的模型距离」
4. 递归细分时，只要抛物线中点与弦中点的距离平方小于 `cutoff²`，就停止继续分裂，用线段代替

伪代码骨架（对二次 Bézier `int-x/int-y` 参数化）：

```
midpoint_approx = ((sx+ex)/2, (sy+ey)/2)
midpoint_exact  = (int-x(mt), int-y(mt))
if |midpoint_approx - midpoint_exact|² > cutoff²:
    recurse(s, mid)
    emit vertex at mid
    recurse(mid, e)
```

## 为什么值得单独记一笔

这个小细节是所有「CPU 先细分，再扔给 GPU 画三角形」路线都要面对的共性问题：**细分终止阈值必须跟随当前变换动态计算**，否则放大/缩小后视觉质量和顶点开销都会失控。这也是为什么后来 [[slug-gpu-glyph-rendering|Slug]] 选择把整条决策链（in/out 判定 + 覆盖计算）挪到 GPU、在 shader 里直接按 pixel 为单位求解——就彻底绕过了 cutoff 参数的存在。

阈值自适应思路同样适用于路径渲染、矢量 UI、Canvas 类 2D API 的后端实现。

## 相关

- [[slug-gpu-glyph-rendering]] — GPU 直接光栅 Bézier，消除 cutoff 参数
- [[sdf-font-atlas-rendering]] — 另一种绕过曲线细分问题的主流方案：离线生成 SDF 纹理
- [[analytical-antialiasing]] — 解析反走样的通用框架

## Sources

- [[sources/nklein-cl-opengl-text-cutoff]]
