---
tags: [computational-geometry, exact-arithmetic, floating-point, cgal, performance]
date: 2026-04-19
sources: 1
---

# CGAL 精确算术与尾数膨胀陷阱

[[CGAL]] 的核心卖点是几何算法永不因浮点舍入而行为异常——两条几乎平行的线求交，在 IEEE float 下可能报出一个距两条原线「数公里远」的交点，而 CGAL 通过动态分配、无限延伸的尾数（mantissa）配合独立维护分子/分母来避免循环小数，保证任意复杂的构造都是符号精确的。代价藏在深处：尾数长度没有上界。[[ben-supnik]] 在 X-Plane 的 OSM 城市道路生成管线中撞上了这个陷阱。

他的流程是先把 OpenStreetMap 的大量向量数据合成为一张整体地图——这一步的交点已经是 CGAL 「完美」构造出的长尾数点；然后再以每个街区为单位计算人行道偏移——长尾数点上再做一次复杂几何构造，尾数进一步暴涨。结果是为整个圣地亚哥跑一次人行道计算要 36 分钟，完全不可接受。

修复出乎意料地直接：在第二阶段入口把每个街区角点 round-trip 一次——转成 64-bit IEEE float 再转回 CGAL number type，强行抛掉多余精度。float64 已经给出亚毫米精度，这对道路几何是严重溢出。简化后的管线在 67 秒内跑完，近 32 倍提速。

这种精度截断不是零风险：如果原始数据里因为 OSM 编辑冲突产生了尺寸小于 1mm 的「真街区」，CGAL 会诚实地按无穷精度保留它，而四舍五入会把它翻面或退化。因此生产化这个降精度步骤必须配一道 sanity check——所幸对路面应用，亚毫米以下的数据天然是噪声，直接丢弃即可。这条经验的一般化结论是：符号精确算术的成本随「构造深度」累积，必须在语义允许的边界处主动重置精度，而不是让 CGAL 替你记住每一位有效数字。参见 [[floating-point-basics]] 附近的精度概念与 [[planet-terrain-dem-pipeline]] 里的坐标精度处理。

## 相关
- [[huge-world-coordinate-precision]]
- [[planet-terrain-dem-pipeline]]
- [[cgal-arrangement-import-antennas]] —— CGAL arrangement 导入脏多边形时的拓扑策略与 antenna 陷阱

## Sources

- [[sources/supnik-cgal-mantissa]]
