---
tags: [rendering, marching-squares, procedural-generation, mesh, tileset]
date: 2026-04-27
sources: 2
---

# 多色 Marching Squares

标准 [[marching-cubes]]（2D 版本即 Marching Squares）处理的是二值状态——每个顶点为"内"或"外"。当需要在一张地图上表达 N 种颜色，并在所有颜色之间绘制分界线时，标准版本无法直接胜任。本页描述 Boris The Brave 为此设计的多色扩展方案。

## 案例归约

标准 Marching Squares 有 16 种情形（2 种状态 × 4 个角顶 = 2⁴）。引入多色后，理论上有 N⁴ 种组合，但实际上我们关心的只是**哪些角顶颜色相同、哪些不同**，与具体颜色标签无关。通过如下重标签规则，所有组合可归约为 **15 种基本情形**：

1. 以右上角顶的颜色作为颜色 0；
2. 按逆时针顺序遍历其余三角，依次将首次出现的新颜色命名为 1、2、3。

这样任何合法的顶点着色方案都对应一种唯一的规范形式（canonical case）。

```python
def classify(case):
    labels = dict()
    uniq_case = []
    for corner in case:
        uniq_case.append(labels.setdefault(corner, len(labels)))
    return uniq_case
```

其中情形 17（两对对角顶颜色交叉，如 ABAB）存在歧义，与标准 Marching Squares 中的歧义情形对应，需通过 [[marching-squares-ambiguities]] 中的 Asymptotic Decider 方法处理。

## 自适应定位

与标准版本类似，基础情形将所有边界点放在格边中点，导致锯齿状 45° 边界。自适应版本为每个顶点额外存储一个**权重（weight）**——表示该顶点"推开边界"的强度，通常等于顶点到实际边界的距离。

对于相邻两顶点颜色不同、权重分别为 w₁ 和 w₂ 的情况，边界点位置为：

```
t = w1 / (w1 + w2)
boundary = lerp(t, v1, v2)
```

某些情形需要在格的中心添加顶点（当四个角各有不同颜色时）。推荐的中心点公式为调和加权平均：

```
center = (v1/w1 + v2/w2 + v3/w3 + v4/w4) / (1/w1 + 1/w2 + 1/w3 + 1/w4)
```

或借鉴 [[dual-contouring]] 的方式求更精确的中心位置。

## 适用范围

该方案仅适用于 2D。在 3D 场景中，建议用标准 [[marching-cubes]] 提取单一等值面网格，再通过像素着色器或三角形细分来着色。

## 相关

- [[marching-cubes]] — 基础算法，本页是其多色 2D 扩展
- [[marching-squares-ambiguities]] — 歧义情形的 Asymptotic Decider 解法
- [[dual-contouring]] — 提供更精确中心顶点计算的替代算法

## Sources

- [[sources/boris-2d-marching-cubes-multicolor]]
- [[sources/boris-marching-squares-ambiguities]]
