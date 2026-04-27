---
tags: [numpy, image-processing, performance, reshape]
date: 2026-04-19
sources: 1
---

# NumPy 图像切瓦片的 reshape + transpose 技巧

把一张 `[H × W]` 或 `[H × W × C]` 的图切成 `B × B` 的小瓦片，朴素双重 for 循环可写，但对 512×512 图就能跑出明显延迟。[[pekka-vaananen]] 在 *Efficiently split a NumPy array into tiles* 里给出无拷贝的解法：两行 `reshape + transpose` 比 for 循环快 **1000×**，比 scikit-image 的 `view_as_blocks` 还快 **15×**——后者用 `np.lib.stride_tricks.as_strided`，反倒不如纯 reshape。

## 代码模式

```python
def split_to_tiles(img, B):
    if img.ndim == 2:
        h, w = img.shape
        tiles = img.reshape(h//B, B, w//B, B).transpose(0, 2, 1, 3)
    else:
        h, w, C = img.shape
        tiles = img.reshape(h//B, B, w//B, B, C).transpose(0, 2, 1, 3, 4)
    return tiles  # [bh, bw, B, B(, C)]，read-only view
```

## 为什么这样 reshape

- `reshape(bh, B, bw, B, C)` 把 **H 轴**拆成「瓦片行 `bh` × 瓦片内 `B`」，同理拆 W 轴；
- 此时轴次序是 `(bh, B, bw, B, C)`——行相邻像素仍被 `bw` 分开，块内像素跳着走；
- `transpose(0, 2, 1, 3, 4)` 把块坐标 `(bh, bw)` 挪到前面、块内坐标 `(B, B)` 挪后面，得到「块为单位的 2D 数组」。

如果直接 `reshape(bh, bw, B, B, C)` 会得到「64 × 1 像素切片」而不是 8×8 方块——因为原始内存布局是按行存的，没有 transpose 给它正确跳步。

## 副作用

- 返回的是原数组的 **view**，不能直接写（`tiles[y,x][:] = 0` 会抛 `ValueError`）；要修改必须 `.copy()`。
- 若 `H % B != 0` 要先裁掉。
- 逆操作对称：`tiles.transpose(0, 2, 1, 3).reshape(h, w)` 还原整图。
- 想拿到 `[N × D]` 的向量矩阵（`D = B·B·C`），只需再 `.reshape(-1, D)`，这就是 [[vector-quantization-tilemap]] 的输入格式。

## 为什么 as_strided 反而慢

`view_as_blocks` 用 `as_strided` 捏出更高维的 view，理论上零拷贝；但它的迭代步长不连续，下游如果 `.reshape(-1, D)` 会触发隐式拷贝；而 reshape + transpose 在 C-contiguous 布局上可以复用底层指针，实测就更快。作者的建议：**优先 reshape + transpose，被迫要 overlap window 才考虑 `as_strided`。**

## 相关

- [[vector-quantization-tilemap]]
- [[pca-image-compression]]

## Sources

- [[sources/30fps-split-tiles]]
