---
tags: [c, cpp, 构建系统, 资源嵌入, incbin, 链接器]
date: 2026-04-19
sources: 1
---

# C/C++ 把资源文件嵌入可执行文件

在 C/C++ 工程里经常需要把 shader、字体、图标、查表这类小资源直接打进可执行文件，避免运行时再去文件系统找路径。Nikos Papadopoulos 在一篇短文里把常见做法梳理成三档，每档的权衡都不一样。

## 外部工具流：xxd / imagemagick

最老实的办法是构建前用外部工具把二进制转成 C 头文件，比如 `xxd -i input.bin output.h` 会生成一个 `unsigned char input_bin[] = { ... }` 加一个 `unsigned int input_bin_len`。图像类的可以用 `imagemagick` 的 `convert` 链配脚本。

这一档的优点是跨平台、人人看得懂；缺点是构建流水线里多了一个外部依赖，头文件往往巨大（展开成逗号分隔的十进制字节），编译器也要替这个大数组做词法分析和常量折叠，编译时间被拉长。

## 预处理器 trick：`#include` 一段 ASCII

对纯文本资源（典型如 GLSL shader），可以利用 C 的字符串字面量拼接加一个 `STRINGIFY` 宏，直接把文件 `#include` 进来：

```c
#define STRINGIFY(A) #A
const char *fsource =
#include "file.ext"
;
```

然后把 `file.ext` 的内容用 `STRINGIFY(...)` 包起来。这样省了外部工具，但**被嵌入的文件本身要改一行**——加 `STRINGIFY(` 前缀和 `)` 后缀。对 shader 这种场景还凑合，换到任意二进制就没法用。

## 汇编 `.incbin`：让链接器背锅

最干净的一档是用 GCC 的内联汇编 `.incbin` 指令，直接命令汇编器把文件原样拷进 `.rodata` 段，同时生成两个全局符号 `_start` / `_end`：

```c
__asm__(".section .rodata\n"
".global incbin_name_start\n"
"incbin_name_start:\n"
".incbin \"binary.bin\"\n"
".global incbin_name_end\n"
"incbin_name_end:\n");
```

C 侧用 `extern const void* incbin_name_start;` 声明，`(char*)&end - (char*)&start` 就是文件长度。零编译开销（汇编器直接 memcpy），零额外构建依赖，资源按链接器规则对齐。代价是明显的：依赖 GCC/Clang 的内联汇编语法和 ELF 风格的段指令，**Windows MSVC 不支持**，跨平台时要准备一份 `resource.rc` 或者 PE 侧的回退路径。

## 工程取舍

这三种方案覆盖了不同痛点：`xxd` 最通用但最慢；预处理器 `STRINGIFY` 适合纯文本 shader、不适合二进制；`.incbin` 最快最干净但绑死 toolchain。现代引擎一般会再套一层，比如 [[game-resource-pack-format]] 的 pak 表或 [[offset-based-resource-blobs]]，把这些方案当作「把 pak 内嵌进 exe」的实现细节。

## Sources

- [[sources/4rknova-cpp-embed-files]]
