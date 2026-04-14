---
tags: [渲染, metal, shader, msl, 图形api]
date: 2026-04-14
sources: 1
---

# Metal Shading Language 入门（vertex / fragment 函数）

**MSL（Metal Shading Language）** 是 Metal 自己的 shader 语言，基于 C++14 的子集 + 一组 GPU 专用属性。[[warren-moore|Warren Moore]] 在 *Up and Running with Metal, Part 2* 里用一个最小的带色三角形，把 MSL 的三个关键概念——**函数限定符**、**属性限定符**、**插值语义**——一次讲清楚。

## 一个最小示例

```metal
using namespace metal;

struct ColoredVertex {
    float4 position [[position]];
    float4 color;
};

vertex ColoredVertex vertex_main(
    constant float4 *position [[buffer(0)]],
    constant float4 *color    [[buffer(1)]],
    uint vid                  [[vertex_id]])
{
    ColoredVertex v;
    v.position = position[vid];
    v.color    = color[vid];
    return v;
}

fragment float4 fragment_main(ColoredVertex in [[stage_in]]) {
    return in.color;
}
```

这几十行里藏着 MSL 的几乎全部基础语法。

## 函数限定符（Function Qualifier）

MSL 用一个关键字标记函数的**用途**：

| 限定符 | 含义 |
|---|---|
| `vertex` | 每个顶点调用一次，返回一个结构体送入光栅化 |
| `fragment` | 每个 fragment 调用一次（见 [[fragment-shader]]） |
| `kernel` | 计算内核（compute shader），`dispatch` 启动 |

没有「shader program」概念——你只是在一个 library 里声明若干命名函数，**在 pipeline state descriptor 上按名字挑选**哪一个作 vertex function、哪一个作 fragment function。一个 `.metal` 文件可以同时放多种函数。

## 属性限定符（Attribute Qualifier）

MSL 借用 C++11 的 `[[...]]` 属性语法来标记**数据在 GPU 管线里的含义**：

- **`[[buffer(n)]]`**：函数参数从哪个 buffer 绑定槽位读。与 host 代码里 `[encoder setVertexBuffer:... atIndex:n]` 的 `n` 一一对应，是 shader 和 app 之间的**绑定契约**。
- **`[[vertex_id]]`**：自动注入的顶点索引，对应 `drawPrimitives:` 参数的 `vertexStart .. vertexStart+vertexCount-1`。
- **`[[position]]`**（用在结构体成员上）：标记「这个 float4 就是 clip-space 位置」，让光栅化器能找到要 /w 齐次除法的那一列。位置以 [[coordinate-spaces|normalized device coordinates]] 给出，最后一维 `w` 固定为 1 就是普通 2D 情况。
- **`[[stage_in]]`**（用在 fragment 函数参数上）：标记「这不是常量数据，而是由顶点函数输出**经光栅化插值**后得到的 per-fragment 数据」。

属性限定符的意义是：MSL 的类型系统**同时承担数据流图**，编译器靠它们把 CPU 绑定的 buffer、vertex stage 输出、fragment stage 输入三者对齐起来。

## 从 vertex 到 fragment：插值是默认行为

`vertex_main` 只会被调一次一个顶点，但同一个三角形的 `fragment_main` 可能被调成千上万次。中间发生的事是 **rasterization**：[[pineda-edge-rasterization|光栅化器]]决定三角形覆盖到哪些像素，并把顶点输出**按位置插值**后送进 fragment 函数。

默认插值规则（Warren 在评论里补的一条关键信息）：

- **浮点**类型：默认 [[perspective-correct-interpolation|perspective-correct]] 插值
- **整数**类型：`flat` 插值（取 provoking vertex 的值）
- 可以用 `[[flat]]` / `[[center_no_perspective]]` 等成员属性覆盖

结构体的嵌套成员也会**递归**地被插值处理。这说明 MSL 的 vertex → fragment 数据通道并不依赖某个预定义的 `varying` 列表，而是直接用**任意用户定义结构体 + 属性标记**来描述。

## 一次 draw call 的对接表

```
shader 侧                          host 侧
--------                           -------
[[buffer(0)]]      <-------->      setVertexBuffer:positionBuffer atIndex:0
[[buffer(1)]]      <-------->      setVertexBuffer:colorBuffer    atIndex:1
[[vertex_id]] vid  <-------->      drawPrimitives:Triangle start:0 count:3
[[position]]       <-------->      光栅化器的必需契约（不与 host 对应）
[[stage_in]]       <-------->      光栅化的隐式插值输出
```

## 编译模型：library 替代 link

OpenGL 需要你在 runtime `glCompileShader` + `glLinkProgram`，任何编译错误都只能等到装 app 之后才暴露。Metal 把 `.metal` 文件交给 **Xcode 编译期**预编译成二进制 `default.metallib`，打进 app bundle；runtime 只需要 `[device newDefaultLibrary]` + `[library newFunctionWithName:@"vertex_main"]` 去按名字**查**函数。pipeline state 对象负责把 vertex 函数和 fragment 函数的接口**隐式 link**。

这个改动把「shader 编译错」从 runtime 提前到 build time，是 Metal 作为显式 API 之外一个容易被忽视的工程学改进。

## 相关

- [[metal-api-overview]]
- [[fragment-shader]]
- [[rendering-pipeline]]
- [[perspective-correct-interpolation]]
- [[coordinate-spaces]]
- [[shader-vector-math-primer]]
- [[shaderlab-hlsl-basics]] —— Unity HLSL 的对照视角
- [[warren-moore]]

## Sources

- [[sources/metalbyexample-up-and-running-2]]
