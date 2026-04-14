---
tags: [dct, simd, fma, 定点数, 压缩]
date: 2026-04-14
sources: 1
---

# DCT 平面旋转的四种实现

几乎所有快速 DCT 都可以分解成两类基本算子：**蝴蝶变换（butterfly）** 和 **平面旋转（planar rotation）**。蝴蝶就是一对 `(a+b, a-b)`，与 2 点 FFT、2 点 Hadamard、2 点 DCT 本质等价；而旋转就是一个 2×2 的标准正交矩阵 `[[cos θ, -sin θ], [sin θ, cos θ]]` 作用在两个通道上。对 DCT 的优化很大程度上就是在对旋转算子做文章。[[fabian-giesen|ryg]] 把旋转的四种写法与它们背后的成本模型并列陈列，恰好对应现代 [[memory-hierarchy|存储层级]] 与 SIMD 流水线下「经典优化常识」已经错位的一个例子。

## 四种写法

1. **直接矩阵乘法**：4 乘 2 加，或 2 乘 2 FMA。依赖链长度为 2。最直观，FMA 时代最便宜。
2. **提取公因子（经典节乘）**：先算 `t = (a - b) cos θ` 之类的中间量，再用它把另一个乘法省掉。成本 3 乘 3 加，或 1 乘 1 加 2 FMA。依赖链长度 3。IJG libjpeg 的 LL&M 整数 DCT 就用这招。
3. **scaled rotation（AA&N）**：把整个旋转乘上一个公共缩放因子（常用 `1/cos θ`），让后续的蝴蝶把这个缩放因子吸收进去，相当于用两条独立 FMA 完成一次旋转。AA&N DCT 的核心思路。
4. **三次剪切分解（three-shear）**：把旋转写成三个 shear 矩阵的积，可以就地完成、没有额外寄存器占用，而且**在截断整数下天然可逆**——这就是 BinDCT 做 integer-to-integer DCT 的基础，也是小波变换 lifting 方案的同一把刀。代价是三次乘法全部串行，依赖链 3。

## 为什么「经典优化常识」不再对

传统 DCT 文献的前提是「乘法贵 / 加法便宜」以及「算术运算数决定成本」。ryg 指出两条都过时了：现代 SIMD 与浮点单元上乘法和加法同价、FMA 一步顶两步；而真正的瓶颈往往是**数据 shuffle、load/store、寄存器排布**，不是纯算术。在 Xbox 360 上实测一个 FMA 版 8×8 IDCT，一半时间都花在 load / unpack / transpose / pack / store 上。

另一个隐藏的成本是**定点精度**：每个乘法都会把一次 round-off 注入路径，所以定点实现下你反而怕乘法堆叠在同一条依赖链上。Bink 2 的工业级整数 DCT 最后选择了 scaled-but-orthogonal 的方案，而不是 lifting，原因就是重度量化下 lifting 的非正交性会让 trellis 量化的 L2 代价函数不再可分离。

## 和其他话题的连线

- **FMA 的影响**：和 [[latency-vs-throughput]]、[[cpu-performance-formula]] 同族的思考——乘加同价后，优化目标从「少乘几次」变成「短依赖链」和「少搬运数据」。
- **熵编码才是真瓶颈**：IDCT 只有 4.5 cycles/pixel，但前面的 VLC / 算术编码器是串行的，单核微操作 shift 在 PPC / Cell 上又贵又会阻塞另一条硬件线程；这是 ryg 对媒体解码流水线架构的长期痛点（参见 [[adaptive-arithmetic-coding]]）。
- **几何视角**：剪切分解让人想起 Givens 旋转，把它接到任意正交矩阵的 QR 分解上就能得到任意正交变换的 integer-to-integer lifting 版本。

## 相关

- [[fabian-giesen]]
- [[adaptive-arithmetic-coding]]
- [[faster-math-functions]]
- [[sse-tricks]]

## Sources

- [[sources/ryg-planar-rotations-and-dct]]
