---
tags: [渲染, gpu, shader, spir-v, vulkan, hlsl]
date: 2026-04-19
sources: 1
---

# 手动解析与改写 SPIR-V

对大多数图形程序员来说 [SPIR-V](https://www.khronos.org/spir/) 是个不透明的二进制 blob：用 DXC/glslang 把 HLSL/GLSL 编进去，用 SPIRV-Tools 做优化/汇编，用 SPIRV-Cross/SPIRV-Reflect 做反射和跨编译，基本不需要自己碰字节流。[[people/panagiotis-charitos|Charitos]] 在 AnKi 里却遇到两个现成工具解决不了的场景，于是索性自己写解析器——结论是 SPIR-V 的编码比想象中简单得多。

## 两个动机

1. **检测片元 shader 是否 discard**。只要在二进制里扫一遍有没有 `spv::OpKill` 就行。引擎用这个结果决定 render state（带 discard 的 shader 不能做 early-z 优化）。
2. **重写 HLSL register 绑定号**。AnKi 把 shader 统一切到 HLSL 并用 `register(t0, space0)` 这种 DXC 风格绑定。HLSL 的 binding model 和 Vulkan/SPIR-V 没有直接映射，DXC 通过 `-fvk-b-shift` 等参数把 HLSL register 重映射成"逻辑 Vulkan binding"（体现为 `spv::DecorationBinding`）。反射完成后，AnKi 需要把这些逻辑 binding 再改写成引擎自己的最终绑定号——就得原地写回 SPIR-V。

## 格式本身

SPIR-V 二进制开头 20 字节（5 个 32-bit word）是 header，后面连续堆指令。每条指令第一个 32-bit word 的高 16 位是**指令长度**（含自身），低 16 位是 opcode。迭代主循环只要：

```cpp
uint32_t offset = 5;
while (offset < codeSize) {
    uint32_t instruction = pCode[offset];
    uint32_t length = instruction >> 16;
    uint32_t opcode = instruction & 0xffff;
    // ... 处理 ...
    offset += length;
}
```

就能遍历所有指令。查 `OpKill` 就是循环里匹配 opcode；改写 binding 就是遇到 `OpDecorate id DecorationBinding literal` 时把 `pCode[offset+3]` 原地改掉。整件事不到 20 行代码。

## 为什么值得自己写

- **没有现成工具能做这件事**——SPIRV-Cross 是反射+跨编译，SPIRV-Tools 是优化+反汇编，都不提供"原地改写 decoration literal"这种小 API。
- **依赖最小化**。AnKi 的构建里少一个第三方依赖就是胜利。
- **性能可控**。SPIRV-Tools 的做法是把二进制展开成 IR 再序列化回去，内存和时间成本远超"只想改一个 word"的场景。

## 相关

- [[shader-permutation-explosion]] —— 运行期 SPIR-V 改写的另一条出路（相对于离线穷举）
- [[compilation-pipeline]] —— DXC → SPIR-V → 驱动后端的完整链
- [[slang-shader-language]] —— 新一代 shader 语言同样在处理 binding model 跨 API 映射问题

## Sources

- [[sources/anki-spirv-parsing-rewriting]]
