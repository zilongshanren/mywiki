---
tags: [程序化生成, 空间索引, 四叉树, 分形坐标, 无限网格]
date: 2026-04-27
sources: 1
---

# 无限四叉树与分形坐标（Fractal Coordinates）

标准四叉树要求预先确定根节点的边界范围，这使得扩展到无限平面变得笨拙。分形坐标系（Fractal Coordinates，Mawhorter 2021）通过重新解释四叉树的结构，自然地支持无限平面操作。

## 核心思想

把四叉树理解为**覆盖全平面的多级格网集合**，而非"一个有边界矩形的递归细分"：

- **第 h 级格网**：每格大小为 `2^h × 2^h`，铺满整个无限平面
- 任意格子用三元组 `(h, x, y)` 唯一标识，称为**分形坐标**
- 任意 h 级格子包含恰好 4 个 (h-1) 级子格，形成树结构，但树延伸到无限高

这样就消除了根节点边界问题——只要 h 足够大，任何区域都有包含它的格子。

## 交替坐标系

朴素的多级格网有一个缺陷：坐标原点始终是某一级格子的角，导致左右相邻的 `(0, 0, 0)` 和 `(0, -1, 0)` 在任何高度都无法找到共同父节点。

**交替方案**：按奇偶级别交替改变子节点的偏移方向——偶数级向右移，奇数级向左移（y 方向同理）。这样每隔两级就能让相邻格子汇入同一父节点，保证：

> **对任意有限矩形区域，都存在某个级别 h，使得该区域完全落在单个 (h, x, y) 格子内。**

这是一个非常有用的性质：存储形状时只需找到最小包含格存一次，而不必在多个格子里重复存储。

## 代码概览（Python 风格伪码）

```python
def parent(h, x, y):
    if h % 2 == 0:
        return (h+1, (x+1)//2, (y+1)//2)
    else:
        return (h+1, x//2, y//2)

def children(h, x, y):
    if h % 2 == 0:
        return [(h-1, 2*x+dx, 2*y+dy) for dx in (0,1) for dy in (0,1)]
    else:
        return [(h-1, 2*x+dx, 2*y+dy) for dx in (-1,0) for dy in (-1,0)]
```

## 应用场景

- **zoomable 地图**：按分形坐标存储地图数据，天然支持多级 LOD 查询
- **无限迷宫**：Mawhorter 用此坐标设计的迷宫可保证任意两点之间连通，且结构细节存在于所有尺度
- **[[game-development/substitution-tilings]]**：Boris 将同一思路用于替换铺砖的惰性树结构——inflate 对应向上一级，dissect 对应向下展开子节点
- **[[infinite-random-rhombus-tilings]]**：相位化 chunk 算法同样依赖"有限区域总有包含正方形"这一性质

## 相关

- [[game-development/substitution-tilings]] —— 分形坐标思路的直接应用
- [[infinite-random-rhombus-tilings]] —— 无限程序化铺砖方法论

## Sources

- [[sources/boris-infinite-quadtrees]]
