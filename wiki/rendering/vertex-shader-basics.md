---
tags: [渲染, shader, gpu, 顶点, gamemaker, glsl]
date: 2026-04-19
sources: 1
---

# Vertex Shader 基础：什么时候写，怎么写

Shader 教程绝大多数篇幅都在 fragment shader——毕竟"那里才有 pixel art"。但 **vertex shader** 掌管着 fragment shader **能作用在屏幕上哪些区域**，以及**数据如何插值传下来**——它在 2D 游戏里也经常被低估。[[xor-shader-artist|Xor]] 在 GM Shaders 里这篇 Vertex Shaders 教程把"何时要写 VS"和"VS 能做/不能做什么"讲得很清楚，非常适合把 [[rendering-pipeline]] 这一段从抽象图表变成具体代码。

## 管线里的位置

一切 draw 都从 **顶点**开始：`draw_sprite()` = 4 个顶点组成两个三角形；`draw_text()` = 每个字符一个 textured quad；`draw_circle()` = 多个三角形扇形扩散。**Vertex shader 跑在 primitive assembly 之前**——这是它的关键特权：可以**改变 fragment shader 能覆盖的屏幕区域**。

经典 GameMaker GLSL 顶点着色器：

```glsl
attribute vec3 in_Position;
attribute vec4 in_Colour;
attribute vec2 in_TextureCoord;

varying vec2 v_coord;
varying vec4 v_color;

void main() {
    vec4 object_space_pos = vec4(in_Position, 1.0);
    gl_Position = gm_Matrices[MATRIX_WORLD_VIEW_PROJECTION] * object_space_pos;
    v_color = in_Colour;
    v_coord = in_TextureCoord;
}
```

三件事：读 attribute、算投影空间位置、把插值数据交给 fragment。

## Attribute：每顶点输入

默认三件套是 `position / color / texcoord`。**不同的 draw 函数会传入不同的 attribute 集合**——`draw_line()` / `draw_circle()` **没有 texcoord**，用期待 texcoord 的 shader 会悄悄失败（或读到 `(0,0)` 取到 atlas 角）。有经验的做法：为不同 attribute 组合准备不同 shader，避免条件式失败。

自定义 attribute 是 [[compact-vertex-format]] 的入口：3D 里常用 bone weight、tangent、bitangent、baked vertex lighting，甚至 shader 特有的状态都可以塞进来。**attribute 数据量直接影响顶点带宽**——大网格里把多余 attribute 去掉能显著节省 GPU 时间。

> 现代 GLSL 里 `attribute` 被 `layout(location = N) in` 替换；概念一样，语法更显式。

## Varying：插值到 fragment

`varying` 的值在三角形三个顶点间**线性插值**传给 fragment shader。颜色、texcoord、法线都用这个机制。类型限制：**floats、float vectors、matrices**，但**不支持 int/bool**——int 没法做线性插值。

一个非常典型的性能模式：**per-vertex lighting**。把 Lambert / specular 在顶点处算完，`varying` 传下来；fragment 只做 texture fetch。代价是插值 artifact（N-gon 网格低密度时 Gouraud 光照看起来"塑料感"），但省下的 fragment 计算量对移动端是量级级的节省。[[fragment-shader]] 的高成本是 GPU 优化永远绕不开的主题，per-vertex 是最大的一把"刀"。

## Transformation：不止是 MATRIX_WORLD_VIEW_PROJECTION

VS 输出 `gl_Position` 必须是**投影空间坐标**（clip space，`-1 ~ +1`）。多数情况下 `M_WVP * position` 就够了——[[mvp-transform|MVP]] 这个变换链已经把 world、view、projection 都做了。

但 VS 能做 MVP 做不到的事：**在投影前修改位置**。典型场景：

- **波浪/风/水面**：`position.xy += cos(position.yx/8 + u_time) * 12`，4 行代码把静态平面变活。
- **Shockwave / ripple**：在冲击波处理顶点位移。
- **Padding around primitives**：把 quad 的顶点向外推开一圈，让后续 fragment shader 能画出**超出原 primitive 边界**的模糊 / 羽化 / soft particle 效果——因为 rasterizer 只会在顶点定义的三角形里跑 FS，想让 blur 超出边界就必须先扩顶点。

这是 VS 和 FS 的分工根本区别：**FS 没法写出自己的作用域外**，但 VS 可以。

## Vertex Shader 里不能做的事

这些限制在教程里被 Xor 单独列出——因为都是新手踩过的坑：

- **同一 uniform 不能在 VS/FS 共用**——GLSL 1.0 要求分别声明同名 uniform，GM 对此特别严格。
- **GameMaker 的 VS 不能采样纹理**。理论上 `texture2DLod(sampler, uv, lod)` 可以用，但 GM 桌面版没支持（只在 HTML5 上工作）。这挡住了 vertex-texture-fetch 做 terrain displacement / GPU skinning 的路。
- **`dFdx / dFdy / fwidth` 在 VS 无意义**——derivative 只在 rasterization 阶段（FS 的 2×2 quad）才有上下文。但这些函数在 FS 里作用于 varying 却异常有用——例如从 `dFdx(v_pos)`、`dFdy(v_pos)` 叉乘得到 **flat shading 的法线**，不需要 attribute 传 normal。

## 什么时候该去写 VS

Xor 的总结很实用：

- **顶点位移**（wind、wave、shockwave）——FS 办不到。
- **扩展 primitive 作用域**（padding、outline extrusion、fur shell）——FS 办不到。
- **per-vertex 优化**（把能摊到顶点的都摊下去）——不写就是浪费。
- **自定义 attribute**（tangent、bone weight、baked AO）——3D 必备。
- **复古风格**的 flat shading、Gouraud lighting——美学选择。

这四类之外，fragment shader 能做的大多数效果 VS 不必介入，直接用默认 VS 即可。

## 相关

- [[rendering-pipeline]] —— VS 所处的管线阶段
- [[fragment-shader]] —— VS 的"下一级"
- [[mvp-transform]] —— VS 的默认变换
- [[coordinate-spaces]] —— object / world / view / clip space
- [[compact-vertex-format]] —— 自定义 attribute 的性能影响
- [[waving-grass-shader-vertex-offset]] —— VS 位移的 Unity 实例
- [[shockwave-effect]] —— VS 位移的 2D 美术实例
- [[tangent-space-normal-mapping]] —— 需要 VS 传 tangent
- [[gpu-skinning-matrix-palette]] —— VS 做骨骼动画
- [[hlsl-derivation-correctness]] —— FS 里 `dFdx/dFdy` 的使用
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-vertex-shaders]]
