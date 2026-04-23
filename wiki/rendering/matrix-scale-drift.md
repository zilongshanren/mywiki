---
tags: [矩阵, 旋转, 缩放, 浮点, 场景图, bitsquid]
date: 2026-04-19
sources: 1
---

# Matrix4x4 的缩放漂移问题

[[niklas-frykholm|Niklas Frykholm]] 2012 年的一篇工程笔记：如果用 `Matrix4x4` 存节点 transform 并且支持 scale，**每帧旋转一次就会让 scale 慢慢飘**，飘到可感知要 28 分钟左右——对一个要跑长时间的游戏就是 bug。

## 漂移的机制

`Matrix4x4` 的 rotation 和 scale 在同一个 3×3 子矩阵里混在一起。于是"只改旋转不改缩放"必须写成：

```cpp
void set_rotation(Matrix4x4 &pose, const Quaternion &rot) {
    Vector3 s = scale(pose);
    Matrix3x3 rotm = matrix3x3(rot);
    scale(rotm, s);
    set_3x3(pose, rotm);
}
```

问题：`scale(pose)` 由于浮点误差，**取出来的 s 不是精确的原值**。每帧把这个被"污染"的 s 喂回去，就构成一个反馈回路。

关键点——**误差线性增长、不是几何增长**。每轮误差正比于当前 scale 本身而不是当前误差（`1+e` 而不是 `e` 数量级），所以不会指数爆炸，但也不会靠中心极限自动回退。Niklas 的实测数据：

| 误差 | 帧数 | 时间（60Hz）|
|---|---|---|
| 0.00001 | 202 | 3 s |
| 0.00010 | 1 654 | 28 s |
| 0.00100 | 100 575 | 28 min |

28 分钟 0.1% 的放大，肉眼可见。

注意**平移 + 旋转**没这个毛病——因为平移存在独立的列里，不会被 rotation 的写回蹭到。只有 rotation 和 scale 共享存储时才出事。

## 为何是系统性偏差而非 random walk

如果每轮误差真是随机的，按 random walk 误差应该按 `e·sqrt(N)` 增长；实测却是 `e·N`。这说明流程里有**系统性偏差**——某个方向的 round-off 一直被推向同一侧。这是第 4 种方案可以着手的切入点。

## 四条解法

**1. 分开存**（推荐）——pose 直接拆成 translation + rotation + scale，rotation 改用 `Matrix3x3`，scale 独立 3 个 float。总共 15 个 float，甚至比 `Matrix4x4` 少一个。代价是不能直接用矩阵乘法和求逆，需要转成 `Matrix4x4` 再用；Niklas 估算场景图 local-to-world 变换约 12% 额外开销，整个引擎的 2% 里的 12% ≈ 总 0.2%，完全可接受。

**2. 始终 rotation + scale 一起设**——消除"取出 scale 再塞回"的反馈回路：

```cpp
void set_rotation_and_scale(Matrix4x4 &pose, const Quaternion &rot, const Vector3 &s);
```

但把 scale 的维护责任推给了调用方。用户自己若不小心还是会复刻 `scale = get_scale(pose); set_rotation_and_scale(..., scale)` 的模式，把反馈回路种回来。Bitsquid 在确定最终方案前临时采用的就是这个。

**3. 量化 scale**——让 `scale(pose)` 返回时总是 snap 到离散网格（比如每 0.0001 一个刻度）。浮点误差不足以翻过一个刻度，反馈就自然断了。有趣的是**这不影响动画**——动画从外部 `set_scale` 喂进去，不经过 `scale()`。像是个 hack，但 Niklas 承认几乎在任何现实场景都 work。

**4. 消除系统性偏差**——最漂亮但最难：重新推导 `set_rotation` 的 floating-point 路径，让误差变成真正的 random walk。误差从 28 分钟 0.1% 变 5.2 年 0.1%——但 Niklas 没时间深入。

## Bitsquid 最终选的

临时用 #2，然后文章结论是倾向迁到 #1。**评论区 Steve-Lombardi 的补强建议**：把 scale 直接塞进 `Matrix4x4` 最后一行的前三个元素（这几个位本就恒为 0），取 scale 时直接返回这三个数、不做任何 decomposition——既省空间又绕开 round-trip 误差。这是个实用的折中。

## 更普遍的启示

这篇文章其实是个小型案例研究——**同一个表达上方便的数据结构（`Matrix4x4`）可能在数值稳定性上隐藏 bug**，问题的根子不是 floating-point 本身而是"把正交的概念耦合进同一块存储、再用 round-trip 去还原它们"。识别这个反馈回路比找到修法更重要。

## 相关

- [[niklas-frykholm]]
- [[3d-rotation-math]]
- [[matrix-multiplication-ordering]]
- [[mvp-transform]]
- [[floating-point-geometric-predicates]]

## Sources

- [[sources/bitsquid-matrices-rotation-scale-drifting]]
