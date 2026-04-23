---
tags: [cgal, computational-geometry, arrangement, polygon-set]
date: 2026-04-19
sources: 1
---

# CGAL arrangement 直接塞进 General_polygon_set_2

把已经构造好的 `Arrangement_2` 强行接进 `General_polygon_set_2`（GPS）做布尔运算，是 [[ben-supnik]] 在 X-Plane 地图管线里的一个 workaround。2013 年他又踩了一遍三年前自己文档过的坑——这次终于记下来。

## 为什么要这么做

标准接口是给 GPS 喂多边形、它内部自行构造 arrangement 做布尔。但 Supnik 的场景里：

- 输入数据**本来就是 arrangement**——从更上游的几何处理流水线继承过来，而且 arrangement **很大**。让 GPS 从多边形重新构造 arrangement 意味着**丢弃拓扑、重新跑几何测试恢复**，对大 map 性能爆炸。
- 某些前置步骤（例如机场跑道面积的 contour 简化）本来就跑在 arrangement 上。GPS 的布尔运算只是管线的一站。

所以他 sub-class GPS 模板实例化，拿到内部 arrangement 的直接访问口。代价是：arrangement 要包含 GPS 所需的**containment 标记**（face data 里"我是内部吗"）。

## 两件必须做的预处理

直接塞 arrangement 进 GPS 会拿到无效多边形（有重复点）。根因是 GPS 代码假设 arrangement 满足两条不变量：

### 1. 删除冗余边

GPS 的遍历算法**假定没有 antenna**（零宽尖刺：一条 edge 两侧是同一个 face）。CGAL 官方提供了清理函数，直接调用即可——删了之后 CCB 遍历才能安全走。

### 2. 统一 CCB 上所有曲线的方向

这是 Supnik 早年踩坑、这次又踩坑的那个**隐性契约**。

Arrangement 的 half-edge 带一条底层 `Curve_2`，而 curve 本身有方向（起点 → 终点）。GPS 遍历一条逆时针 CCB（counter-clockwise boundary）时，要求这条 boundary 上**所有 edge 对应的 curve 方向一致**——要么全部顺着 halfedge 走、要么全部逆着走。乱混就会在导出多边形时得到重复点。

**修复策略**：扫一遍每条 halfedge，对每条 edge 检查：

- 这条 halfedge 的 curve 方向（起点→终点）和 halfedge 本身的方向（source→target）一致吗？
- 这条 halfedge 是不是贴在"内部" face 的那侧？

如果 (1) 不一致 **并且** (2) 这条 halfedge 贴在内部侧，就**翻转 underlying curve 的方向**（`Curve_2::reverse`，不是换 halfedge）。删去 antenna 之后，每条 edge 两侧 face 内外互斥，这套规则能在所有 CCB 上同时成立。

## 与相关 CGAL 陷阱的关联

Supnik 长期抱怨 CGAL 的**抽象 vs 实现裂缝**——这条 curve 方向的要求无论是 CGAL 手册还是头文件注释都没有明文讲清楚，只能在用的时候撞 bug。延伸谱系：

- [[cgal-arrangement-import-antennas]] — 2010 年对脏多边形批量导入时 antenna 如何破坏 winding 判定。
- [[cgal-halfedge-direction-cache-pitfall]] — 2008/2011 年 `merge_edge` 的方向缓存 bug。
- [[cgal-exact-arithmetic-mantissa-growth]] — 精确算术路径下 mantissa 爆炸的性能代价。
- [[floating-point-geometric-predicates]] — 为什么 `orient_2d` 不能用普通浮点。

共同结论：**CGAL 正确性强大但边角多，工程侧只能用大量 in-tree 断言和 adapter 驯化**。

## 相关

- [[ben-supnik]]
- [[cgal-arrangement-import-antennas]]
- [[cgal-halfedge-direction-cache-pitfall]]
- [[arrangement-mesh-simplification]]

## Sources

- [[sources/supnik-arrangement-to-polygon-set]]
