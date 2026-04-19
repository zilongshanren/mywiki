---
tags: [gpu, hlsl, packing, memory, shader]
date: 2026-04-19
sources: 1
---

# GPU 数据打包（Packing）

把每一 bit 都用上是 GPU 程序员的日常。顶点数据、GBuffer、constant buffer、storage buffer 的带宽都有限，数据打包直接影响缓存命中率与带宽预算。[[emilio-lopez-ros]] 的 *The Art of Packing Data* 给出 HLSL + RDNA 汇编级别的实战手册。

## 基本路数

| 数据类型 | 格式示例 | 关键细节 |
|---|---|---|
| 归一化颜色 | `R8G8B8A8_UNORM` | `x*255 + 0.5` 再整数化，避开 `round` 指令 |
| 带符号归一化 | `R8G8B8A8_SNORM` | 精确 0 的代价是 -128 和 -127 都映射到 -1.0 |
| 非对称位宽 | `R10G10B10A2_UNORM` | RGB 10 位、alpha 2 位，HDR / SDR 中立 |
| 法线 | octahedral 2×16 | 单位法线用 2D oct 投影存更省 |
| half float | `R16G16_FLOAT` | fp16 范围 ±65504，IEEE754 subnormal 需注意 |
| flag 位 | bitfield `uint x : 3;` | DXC 支持 HLSL bitfield，GLSL 多不支持 |

## SNORM 的陷阱：精确 0

D3D12 SNORM 有个不直觉的规则：**8-bit SNORM 里 -128 与 -127 都映射到 -1.0**，放弃 256 个可表示值里的一个，以换得 0、+1、-1 均有精确表示。写 packer 必须跟随这个规则：

```hlsl
// 正：使用 round + clamp 到 [-127, 127]
int4 ivalue = int4(round(value * 127.0));
// 负：如果写成 value * 128.0，0 就不精确
```

解包时必须用 **int 移位** 而非 uint mask——后者丢失 sign extension；HLSL 编译器能把 `<<24 >> 24` 这种模式识别成 `v_bfe_i32`。

## HLSL SM 6.6 的 pack/unpack intrinsics

```hlsl
uint packed = pack_u8(uint4(value * 255.0 + 0.5));
float4 v = float4(unpack_u8u32(packed)) / 255.0;
```

底层映射到 `v_perm_b32`，比手写 shift-or 少 2 条指令。SNORM 版本用 `pack_s8` / `unpack_s8s32`。

## Bitfield 与 BFE/BFI

```hlsl
struct Data {
    uint feature1 : 1;
    uint type : 2;
    uint count : 8;
};
```

DXC 对 HLSL bitfield 的支持让 `if(data.feature1)` 直接映射到 `s_bfe_i32`——它自带 compare 功能，省掉一条 cmp 指令。GLSL 生态此时多数不支持，需要 fallback 到手写 mask。

想显式发射 `v_bfe` / `v_bfi`：

```hlsl
uint bfe_u32(uint v, uint off, uint bits) {
    uint mask = (1U << bits) - 1U;
    return (v >> off) & mask;
}
```

注意：**必须写 `1U` 而非 `1`**，否则编译器可能识别为有符号；**`bfi` 的识别不稳定**，性能关键路径要手写 `(v & ~mask) | (new << off)` 并在 RGA 里对照。

## 与其它 packing 主题的关系

- [[compact-vertex-format]]——顶点 stream 的 packing 目标；
- [[unorm-float-conversion]]——Fabian Giesen 对 UNORM ↔ float 的精确数学处理；
- [[cuda-memory-hierarchy]] / [[gcn-wave-occupancy]]——packing 直接决定 VGPR 占用；
- [[oodle-compression-suite]]——离线压缩和运行时 packing 是不同层次的带宽优化。

## Sources

- [[sources/elopezr-art-of-packing-data]]
