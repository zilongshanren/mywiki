---
tags: [渲染, shader, outline, distance-field, unity]
date: 2026-04-14
sources: 1
---

# 动画虚线描边 Shader

[[linden-reid]] 的这篇教程建立在 [[cel-shader-outline|cel shader 外扩描边]] 的基础上——描边本身还是「Pass 1 写 stencil，Pass 2 沿法线外推再画一遍」的两 pass 结构，她只在 Pass 2 的 fragment shader 里做两件事，就把原本的纯色轮廓变成一圈会沿着模型爬动的断续短线。核心是把「用 [[sdf-2d-primitives|距离场]] 决定是否绘制像素」和「用 `_Time` 偏移采样坐标做动画」两个非常便宜的技巧叠在一起。

## 断线：用 `sin(distance)` 做一维距离场剔除

断线效果的诀窍是把屏幕空间位置到某个参考点 `_SourcePos` 的距离丢进 `sin`——`sin` 在正负之间周期性摆动，正值段落就是「画」、负值段落就是「不画」：

```hlsl
// _OutlineDot  = 一段实/虚的频率（越大段越密）
// _OutlineDot2 = 正负偏置，决定实体段和透明段的比例
float skip = sin(_OutlineDot * abs(distance(_SourcePos.xy, pos))) + _OutlineDot2;
clip(skip);          // skip < 0 直接丢像素
return _OutlineColor;
```

把参数拎清楚会更直观：`_OutlineDot` 控制正弦波的角频率——换算成图像上就是**单位距离内重复多少段实-虚**；`_OutlineDot2` 是竖直偏置——把整条 sin 曲线抬一点点，正段就变长、负段变短，等效于实线占空比。因为参考点是**一个点**而不是一条曲线，`distance` 给出的是到中心的径向距离，`clip` 掉负值后出现的是一圈一圈的同心环。这圈同心环再和 Pass 1 留下的「外扩描边环」在 stencil 上相交，最终屏幕上看到的就只剩下外扩的那一圈上被正弦采样切成的碎段。

这是 [[sdf-2d-primitives|2D SDF]] 思维最朴素的用法：用距离场直接在 fragment shader 里做几何决定，避免任何几何体。代价是这套公式只在**屏幕空间**里对了——相机旋转、物体离相机远近变化时，描边密度会跟着视口变化。作者没提这个限制，但对静态相机的美术向项目足够。

## 动画：`_Time` 平移采样坐标

把断线沿描边「走」起来的改动只有一行：

```hlsl
float2 pos = input.pos.xy + _Time * _OutlineSpeed;
```

这里利用了一个很容易被初学者忽略的细节——`sin` 是位置的函数，所以**平移位置等价于平移相位**。让位置每帧加一点，所有实-虚段就一起水平漂移，于是描边看起来是在往一个方向爬动。`_OutlineSpeed` 是个二维向量，就能让描边沿任意方向走。

同样的思路可以扩展到更复杂的形态：

- 把参考点 `_SourcePos` 换成**多点取最小值**，得到多中心的同心波；
- 把距离函数换成到一段折线的距离，描边会在该折线方向上均匀铺开；
- 把 `sin` 换成 `frac` 或其他 [[shaping-functions|塑形函数]]，断线的占空比可以独立于频率调。

## 和主线 cel shader 的关系

这个 shader 只改动了 outline pass 的 fragment shader——Pass 1 的 ramp 光照、stencil 写入都不变。换句话说，**断线描边对现有 cel 管线是无侵入的**：你可以把同一套断线 fragment 套到任何「沿法线外推 + stencil mask」风格的描边 shader 上，不需要改光照、不需要改 stencil 规则。这也是 Linden 教程的典型结构：把一个小技巧剥离出来，让它能插到更大的管线里复用。

## 相关

- [[cel-shader-outline]] —— 这个 shader 继承的两 pass outline 管线
- [[stencil-buffer]] —— 描边的 masking 依赖
- [[sdf-2d-primitives]] —— `distance()` + `clip()` 的同族技巧
- [[shaping-functions]] —— `sin / frac / step` 等周期函数的塑形
- [[texture-encoded-state]] —— Linden 系列里的另一种「把逻辑外化」范式
- [[linden-reid]]

## Sources

- [[sources/lindenreid-animated-dotted-outline]]
