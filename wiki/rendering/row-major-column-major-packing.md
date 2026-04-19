---
tags: [rendering, shader, graphics-api, hlsl, glsl]
date: 2026-04-19
sources: 1
---

# 行主序与列主序的矩阵打包

矩阵的"majority"**只是一个内存布局的选择**，不是矩阵本身的属性。一个 3×4 矩阵（3 行 4 列）有 12 个浮点，row-major 打包把它看成 3 个连续的行向量（每行 4 float），column-major 把它看成 4 个连续的列向量（每列 3 float）。两种解码方式对应的矩阵形状、维度、和 [[matrix-multiplication-ordering|across-times-down 乘法]] 结果都完全一样——变的只是从 buffer/UBO 读进来时按什么顺序填。

在着色语言里的表现：

- **HLSL** 默认 column-major，可以用 `#pragma pack_matrix(row_major)` 或命令行 `/Zpr` 切换。索引 `m[i][j]` 返回 i 行 j 列（行优先的索引语义），构造器 `float3x4(...)` 按**行**填充。
- **GLSL** 默认 column-major，用 `layout(row_major)` / `layout(column_major)` 切换。索引 `m[i][j]` 返回 i **列** j 行（列优先的索引语义），构造器 `mat3x4(...)` 按**列**填充。注意 GLSL 的 `matCxR` 命名和标准数学的 MxN（M 行 N 列）相反。

Jasper 的一条个人偏好：**列向量乘法 + row-major packing**。列向量乘法贴近数学论文习惯，也更容易映射到 `A(B(C(v)))` 的函数应用心智模型；row-major packing 对仿射变换矩阵更省空间——如果最后一行恒为 `(0,0,0,1)`，只需要存前 3 行，用三个 `float4` 就能存下一个 `mat3x4`，std140 下比 column-major 节省 16 字节。

**关键结论**：乘法永远是 across-times-down；packing 只影响载入/存储；向量是"行还是列"完全取决于它出现在矩阵的哪一侧。三者是正交的，不要用一个描述另一个。

## Sources

- [[sources/jasper-matrix-multiplication-guide]]
