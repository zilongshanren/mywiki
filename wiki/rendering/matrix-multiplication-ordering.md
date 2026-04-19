---
tags: [rendering, math, shader, graphics-api]
date: 2026-04-19
sources: 1
---

# 矩阵乘法与顺序

矩阵乘法在图形编程里反复被搞混，根源只有一条：**"across times down"（横乘竖）的算法规则**永远不变，变的只是我们把向量摆成列（column vector）还是行（row vector）、把矩阵内存排成列优先（column-major）还是行优先（row-major），以及在源代码里把 `M * v` 写在左边还是右边。Jasper St. Pierre 在《The Ultimate Guide to Matrix Multiplication and Ordering》里把这些"正交的维度"一条条拆开：HLSL 和 GLSL 的矩阵乘法底层是同一种运算（点乘：A 的行 × B 的列），只是索引语法、构造器、默认 pack 顺序有一些历史遗留的差异。

矩阵乘法**非交换但可结合**——这件事直接决定了图形 pipeline 的写法。列向量约定下，一条标准的变换链写成 `clip = projection * view * model * model_space_P`；行向量约定下变成 `clip = model_space_P * model * view * projection`。两者表达的计算完全相同（彼此互为转置），但空间"阅读顺序"是反的。Jasper 推荐的工程习惯是：**给矩阵起"A_from_B"的命名**（例如 `clip_from_view`、`view_from_world`），让乘法顺序里"相邻两个矩阵的内外空间名一致"——这样哪怕哪天你搞混了列向量/行向量，读代码也能立刻看出空间链对不对。

[[row-major-column-major-packing]] 是另一个独立的维度——它只影响矩阵在内存里怎么打包、shader 里怎么索引，不改变数学。把这两个维度混为一谈是"DirectX is row-major / OpenGL is column-major"这种误解的根源。实际 GLSL 和 HLSL 都默认 column-major packing，真正有分歧的是向量乘法的编码习惯（HLSL codebase 偏行向量，OpenGL codebase 偏列向量）。

逆矩阵的使用有一条反直觉的规则：**顺序不变，方向反向**——`world_from_model * model_P = world_P`，那么 `inverse(world_from_model) * world_P = model_P`，乘法顺序里 inverse 还是放在左边。

## Sources

- [[sources/jasper-matrix-multiplication-guide]]
