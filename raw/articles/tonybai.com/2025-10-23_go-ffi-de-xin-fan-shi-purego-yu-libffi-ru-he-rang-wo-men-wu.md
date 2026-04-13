---
title: Go FFI 的新范式：purego 与 libffi 如何让我们无痛拥抱 C 生态
url: https://tonybai.com/2025/10/23/go-ffi-new-paradigm/
published: '2025-10-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go FFI 的新范式：purego 与 libffi 如何让我们无痛拥抱 C 生态

![](../../assets/d1fbd6ef3368c0d5.png)


[本文永久链接](https://tonybai.com/2025/10/23/go-ffi-new-paradigm) – https://tonybai.com/2025/10/23/go-ffi-new-paradigm

大家好，我是Tony Bai。

import “C”，这行代码对于许多 Gopher 来说，既是通往强大 C 生态的桥梁，也是通往“地狱”的入口。CGO 作为 Go 语言内建的 FFI 机制，其为人诟病的远不止是编译期的种种不便，更包含了昂贵的运行时开销和复杂的心智负担。

正是这些“枷锁”，催生了 Go 社区一个心照不宣的共识：**能不用 CGO，就尽量不用。**

但如果我们的确需要调用 C 库呢？长期以来，我们似乎只能在“忍受 CGO”和“用 Go 重写一切”之间做出痛苦抉择。

现在，一场关于 Go FFI (Foreign Function Interface) 的变革正在悄然发生。以 ebitengine/purego 和 JupiterR-ider/ffi 为代表的一系列社区项目，正为我们开辟出一条全新的道路——一条**旨在卸下这些枷锁、纯 Go 的 FFI 之路**。这标志着 Go FFI 新范式的到来。

本文将系统性地梳理 Go FFI 的几种范式，并深入剖析 purego 与 ffi 协同工作的艺术，为你揭示 一条实现 Go FFI 的新路径。

![](../../assets/e7aa987414f58103.png)


## Go FFI 的三大范式之争

要理解 purego 带来的变革，我们必须首先系统性地审视 Go 社区在与 C 生态交互时，所探索出的三种主要路径或“范式”。它们在不同的维度（如编译期 vs. 运行时、性能 vs. 安全、耦合度 vs. 便利性）上，做出了截然不同的权衡。

### 范式一：原生 CGO —— 官方的“编译期绑定”范式

这是 Go 语言与生俱来的、深度集成在工具链中的官方解决方案。

**核心思想**：在**编译期间**，通过一个外部的 C 编译器（如 GCC 或 Clang），将 Go 代码与 C 代码紧密地静态链接在一起。**实现机制**：使用 import “C” 伪包，并在 Go 文件顶部的注释块中编写 C 代码或包含 C 头文件。Go 工具链会解析这些注释，调用 C 编译器，并生成大量的“胶水代码”，以处理 Go 与 C 之间在调用约定、内存模型和调度器上的差异。**代表项目**：Go 语言标准库自身，以及所有需要深度集成 C 库的项目。**优点**：**功能最强大**：支持处理复杂 C 宏、内联函数、位域，并能完美链接静态 C 库 (.a 文件) 的官方方案。**深度集成**：可以直接在 Go 代码中访问 C 的 struct, union, enum 等类型，体验相对无缝。

**缺点**：**构建复杂性**：引入了对 C 编译器的依赖，使得 Go 引以为傲的一键交叉编译能力几乎失效。**拖慢构建速度**：无法利用 Go 的构建缓存，每次构建都可能需要重新编译 C 代码。**性能开销**：Go 与 C 之间的函数调用，需要经过一个复杂的上下文切换，其开销远高于原生 Go 函数调用。**运行时复杂性**：Go 的垃圾回收器无法跟踪 C 代码分配的内存，需要手动管理。

**适用场景**：当你必须链接一个**只有静态库**的 C 项目，或者需要处理大量复杂的 C 宏和头文件时，CGO 几乎是唯一的选择。

### 范式二：LLGO / TinyGo —— “替代编译器融合”范式

这种范式代表了一种更底层的思路：与其在两个世界之间架设“桥梁”(CGO)，不如尝试将两个世界“融合”。

**核心思想**：使用一个基于**LLVM**的 Go 编译器，而不是官方的 gc 编译器。**实现机制**：由于 C/C++ (通过 Clang) 和 Go 都可以被编译到 LLVM 的中间表示 (IR)，理论上，在这个共享的中间层面上，可以实现比 CGO 更高效、更深度的互操作。**代表项目**：goplus/llgo, tinygo。**优点**：**潜在的更高性能**：在 LLVM 层面进行的函数调用优化，有可能省去 CGO 的部分运行时开销。**更好的 C++ 集成**：LLVM 生态使其在与 C++ 交互时可能更具优势。- tinygo 在嵌入式领域表现卓越，能生成极小的二进制文件。

**缺点**：**非官方工具链**：这是一个巨大的权衡。你将无法使用 Go 官方的编译器，可能无法及时跟上 Go 官方版本的最新特性和安全修复。**生态与成熟度**：作为一个相对小众的社区项目，其生态系统和在生产环境中的检验程度，与官方 gc 编译器不可同日而语。

**适用场景**：性能极其敏感的特定领域、嵌入式系统 (tinygo)、或者整个技术栈都深度绑定在 LLVM 生态中的环境。

### 范式三：PureGo / JupiterRider/FFI —— “纯 Go 运行时动态加载”范式

这是一种新兴的、旨在绕开 CGO 编译期痛苦的社区驱动方案，也是本文将重点剖析的**新范式**。

**核心思想**：**完全放弃编译期的 C 依赖，将与 C 的交互推迟到运行时解决。****实现机制**：- Go 程序在运行时，通过 purego.Dlopen 等函数，像插件一样
**动态加载**一个 C 的共享库 (.so, .dylib, .dll)。 - 通过 purego.Dlsym 找到目标 C 函数在内存中的地址。
- 通过平台特定的
**汇编代码**(SyscallN)，直接按照 C 的调用约定 (ABI) 来调用这个函数地址，将 Go 的参数“翻译”成 C 的格式。

- Go 程序在运行时，通过 purego.Dlopen 等函数，像插件一样
**代表项目**：ebitengine/purego, jupiterrider/ffi。**优点**：**保留 Go 的核心优势**：完美的交叉编译、极快的构建速度、纯 Go 的开发体验。**轻量与灵活**：以普通 Go 库的形式存在，按需引入，无侵入性。

**缺点**：**只支持共享库**：无法链接静态的 C 库。**功能受限**：对 C 类型的支持不如 CGO 完备。

**适用场景**：为你的 Go 应用编写跨平台的 GUI（调用系统的 GTK, Cocoa 等动态库）、构建插件系统、或者任何你需要调用一个以共享库形式发布的 C API 的场景。

这三种范式各有利弊。而 purego 的出现，恰好填补了一个巨大的空白：它为那些**只需要调用动态库中、函数签名相对简单**的 C 函数的广大 Gopher，提供了一个**摆脱 CGO 痛苦的、最具 Go 哲学**的解决方案。接下来的章节，我们将深入探讨这个新范式的具体实现与应用。

## purego —— 奠定“纯 Go” FFI 的基石

purego 项目诞生于著名游戏引擎 [Ebitengine](https://github.com/ebitengine) 的一个宏大愿景：实现真正的“纯 Go”跨平台编译。它的核心价值主张简单而强大：**提供一个无需 CGO 即可从 Go 调用 C 函数的库。**

其核心优势包括：

**真正的跨平台编译**：无需在构建环境中安装目标平台的 C 编译器。只需设置 GOOS 和 GOARCH，即可轻松构建。**更快的编译速度**：纯 Go 的构建可以被 Go 工具链高效缓存。**更小的二进制文件**：purego 直接在运行时调用 C 函数，避免了 CGO 为每个函数生成包装层所带来的体积膨胀。**动态链接**：在运行时加载 C 动态库 (.so, .dylib, .dll) 并查找符号，甚至可以此为基础构建 Go 的插件系统。

purego 的“魔法”主要源于几个巧妙的设计：

**动态库加载系统**：通过 purego.Dlopen, purego.Dlsym, purego.Dlclose 这一套与 POSIX dlfcn.h 高度相似的 API，实现了对动态库的运行时操作。

![](../../assets/4778bbc4f07df828.png)


**底层系统调用**：purego.SyscallN 是这一切的基石。它通过平台特定的**汇编桩 (assembly stubs)**，将 Go 函数的调用参数，按照目标平台的 C 调用约定 (ABI)，精确地放置到正确的 CPU 寄存器和栈上。**函数注册系统**：purego.RegisterLibFunc 将一个 Go 函数变量（如 var puts func(string)）的指针，与一个从动态库中找到的 C 函数地址绑定起来。

### 简单示例：调用 C 标准库的 puts

下面这个简单示例演示了如何通过purego在Go中调用 C 标准库的 puts：

```
// purego/demo1/main.go
package main
import (
"fmt"
"runtime"
"github.com/ebitengine/purego"
)
func getSystemLibrary() string {
switch runtime.GOOS {
case "darwin":
return "/usr/lib/libSystem.B.dylib"
case "linux":
return "libc.so.6"
// Windows 等其他平台...
default:
panic(fmt.Errorf("unsupported platform: %s", runtime.GOOS))
}
}
func main() {
// 1. 加载 C 库
libc, err := purego.Dlopen(getSystemLibrary(), purego.RTLD_NOW|purego.RTLD_GLOBAL)
if err != nil {
panic(err)
}
defer purego.Dlclose(libc) // 确保库被卸载
// 2. 声明一个 Go 函数变量，其签名与 C 函数匹配
var puts func(string)
// 3. 注册！将 Go 变量与 C 函数 "puts" 绑定
purego.RegisterLibFunc(&puts, libc, "puts")
// 4. 直接像调用普通 Go 函数一样调用它！
puts("Calling C from Go without CGO!")
}
```


我们可以通过CGO_ENABLED=0 go run main.go运行这个示例：

```
// purego/demo1下
$CGO_ENABLED=0 go run main.go
Calling C from Go without CGO!
```


此外，在调用任何 C 函数之前，我们首先需要加载包含它的动态库。对于 puts 这样的标准库函数，它位于系统的核心 C 库中。然而，这个核心库在不同操作系统上的**文件名是不同的**（例如，Linux 上是 libc.so.6，macOS 上是 libSystem.B.dylib）。示例中getSystemLibrary 这个辅助函数的作用，就是**抹平这种平台差异**，为我们的程序在不同系统上找到正确的库路径。

这个例子完美地展示了 purego 的优雅之处：一旦注册完成，C 函数的调用体验与原生 Go 函数几乎无异。

### 更复杂的示例：使用回调函数与 qsort

purego 的能力远不止于此。一个更复杂的、更能体现其价值的场景是**将 Go 函数作为回调 (Callback) 传递给 C 函数**。C 标准库中的 qsort 函数就是绝佳的例子，它需要一个函数指针作为比较器。

```
// purego/demo2/main.go
package main
import (
"fmt"
"reflect"
"runtime"
"unsafe"
"github.com/ebitengine/purego"
)
func getSystemLibrary() string {
switch runtime.GOOS {
case "darwin":
return "/usr/lib/libSystem.B.dylib"
case "linux":
return "libc.so.6"
// Windows 等其他平台...
default:
panic(fmt.Errorf("unsupported platform: %s", runtime.GOOS))
}
}
func main() {
libc, err := purego.Dlopen(getSystemLibrary(), purego.RTLD_NOW|purego.RTLD_GLOBAL)
if err != nil {
panic(err)
}
defer purego.Dlclose(libc)
// 1. 定义与 C 函数 qsort 签名匹配的 Go 函数变量
// void qsort(void *base, size_t nel, size_t width, int (*compar)(const void *, const void *));
// 注意：最后一个参数应该是 uintptr，表示 C 函数指针
var qsort func(data unsafe.Pointer, nitems uintptr, size uintptr, compar uintptr)
purego.RegisterLibFunc(&qsort, libc, "qsort")
// 2. 编写 Go 回调函数，签名必须与 qsort 的比较器兼容
compareInts := func(a, b unsafe.Pointer) int {
valA := *(*int)(a)
valB := *(*int)(b)
if valA < valB {
return -1
}
if valA > valB {
return 1
}
return 0
}
data := []int{88, 56, 100, 2, 25}
fmt.Println("Original data:", data)
// 3. 调用 qsort
// 使用 NewCallback 将 Go 函数转换为 C 可调用的函数指针
qsort(
unsafe.Pointer(&data[0]),
uintptr(len(data)),
unsafe.Sizeof(int(0)),
purego.NewCallback(compareInts),
)
fmt.Println("Sorted data: ", data)
// 验证结果
if !reflect.DeepEqual(data, []int{2, 25, 56, 88, 100}) {
panic("sort failed!")
}
}
```


运行这个示例输出如下结果：

```
// purego/demo2下
$CGO_ENABLED=0 go run main.go
Original data: [88 56 100 2 25]
Sorted data: [2 25 56 88 100]
```


这个 qsort 示例充分展示了 purego 的强大能力：它不仅能调用 C 函数，还能通过 NewCallback 实现 Go 与 C 之间的双向通信。

### 局限性与权衡

不过，天下没有免费的午餐。purego 为了实现“纯 Go”的 FFI 体验，也付出了代价，并存在一些重要的局限性，我们必须清醒地认识到：

-
**类型系统限制**：这可以说是 purego**最大的局限**。它原生不支持**按值传递或返回 C 结构体**（在 Darwin/macOS 之外的平台）。对于只涉及整数、浮点数和指针的简单函数，purego 游刃有余；但一旦遇到需要传递复杂结构体的 C API，purego 就显得力不从心了。 -
**平台与架构限制**：purego 的支持并非无处不在。例如，浮点数返回值仅在 amd64 和 arm64 上受支持。在 Windows 的 32 位 ARM 等非主流架构上，功能也受到限制。 -
**函数签名限制**：SyscallN 有最多 15 个参数的限制，并且在处理混合了浮点数和整数的复杂函数签名时，可能会出现参数传递错误。 -
**回调系统限制**：NewCallback 创建的回调函数，其底层资源是**永远不会被垃圾回收**的，并且存在一个硬性的最大数量限制（约 2000 个）。这意味着在高频创建回调的场景下，可能会导致内存泄漏。 -
**内存安全责任**：purego 并没有消除 CGO 的内存安全规则。你依然需要遵循“Go 内存不能被 C 持有”的黄金法则，并自行管理 C 代码分配的内存，以避免悬空指针和内存泄漏。

正是 purego 在**类型系统**上的核心局限（特别是结构体处理），催生了下一个将要登场的主角——JupiterRider/ffi。

## JupiterRider/ffi —— 补全 purego 的最后一块拼图

purego 虽然强大，但其 SyscallN 的设计主要针对的是整数和指针等基本类型。它有一个显著的局限：**原生不支持按值传递或返回 C 结构体**（在 Darwin/macOS 之外的平台），并且处理 C 结构体指针也需要大量 unsafe 操作。

这正是 JupiterRider/ffi 项目的用武之地。ffi 并非 purego 的竞争者，而是其**强大的补充**。它是一个**基于 purego 构建的、对 libffi 的纯 Go 绑定**。


libffi 是什么？

libffi 是一个久负盛名的 C 库，它的唯一目的就是在运行时，根据任意给定的函数签名，动态地构建函数调用。Python 的 ctypes 和许多其他语言的 FFI 功能，其底层都依赖于 libffi。

### ffi 的核心架构

ffi 巧妙地利用 purego 来调用 libffi 提供的 C 函数，然后让 libffi 去处理最棘手的、平台相关的 ABI 细节，特别是**结构体的内存布局和按值传递**。

**调用流程**：

```
Go Code -> ffi.Call() -> purego.SyscallN() -> libffi: ffi_call() -> Target C Function
```


### ffi 使用示例：优雅地处理 C 结构体指针

为了展示 ffi 如何弥补 purego 的不足，让我们来调用 C 标准库中的 gettimeofday 函数。其 C 语言签名如下：

```
int gettimeofday(struct timeval *tv, struct timezone *tz);
```


这个函数接受两个结构体指针作为参数。使用纯 purego 调用它会非常繁琐，需要手动进行内存布局和 unsafe.Pointer 转换。而 ffi 则让这个过程变得极其清晰和安全。

```
// ffi/main.go
package main
import (
"fmt"
"runtime"
"time"
"unsafe"
"github.com/ebitengine/purego"
"github.com/jupiterrider/ffi"
)
// getSystemLibrary 函数与前一个示例相同
func getSystemLibrary() string {
switch runtime.GOOS {
case "darwin":
return "/usr/lib/libSystem.B.dylib"
case "linux":
return "libc.so.6"
default:
panic(fmt.Errorf("unsupported platform: %s", runtime.GOOS))
}
}
// C 语言中的 struct timeval
// struct timeval {
// time_t tv_sec; /* seconds */
// suseconds_t tv_usec; /* microseconds */
// };
// Go 版本的结构体，注意字段类型和大小必须与 C 版本兼容
// 在 64 位系统上，time_t 和 suseconds_t 通常都是 int64
type Timeval struct {
TvSec int64 // 秒
TvUsec int64 // 微秒
}
func main() {
libc, err := purego.Dlopen(getSystemLibrary(), purego.RTLD_NOW|purego.RTLD_GLOBAL)
if err != nil {
panic(err)
}
defer purego.Dlclose(libc)
// 1. 获取 C 函数地址
gettimeofday_addr, err := purego.Dlsym(libc, "gettimeofday")
if err != nil {
panic(err)
}
// 2. 使用 ffi.PrepCif 准备函数签名
// int gettimeofday(struct timeval *tv, struct timezone *tz);
// 返回值: int (ffi.TypeSint32)
// 参数1: struct timeval* (ffi.TypePointer)
// 参数2: struct timezone* (ffi.TypePointer)，我们传入 nil
var cif ffi.Cif
if status := ffi.PrepCif(&cif, ffi.DefaultAbi, 2, &ffi.TypeSint32, &ffi.TypePointer, &ffi.TypePointer); status != ffi.OK {
panic(fmt.Sprintf("PrepCif failed with status: %v", status))
}
// 3. 准备 Go 结构体实例，用于接收 C 函数的输出
var tv Timeval
// 4. 准备参数
// ffi.Call 需要一个指向参数的指针数组
// 第一个参数：指向 Timeval 结构体的指针
// 第二个参数：nil（表示 timezone 参数为 NULL）
arg1 := unsafe.Pointer(&tv)
var arg2 unsafe.Pointer = nil
// 创建参数指针数组
args := []unsafe.Pointer{
unsafe.Pointer(&arg1),
unsafe.Pointer(&arg2),
}
// 5. 调用 C 函数
var ret int32
ffi.Call(&cif, gettimeofday_addr, unsafe.Pointer(&ret), args...)
if ret != 0 {
panic(fmt.Sprintf("gettimeofday failed with return code: %d", ret))
}
// 6. 解释结果
fmt.Printf("C gettimeofday result:\n")
fmt.Printf(" - Seconds: %d\n", tv.TvSec)
fmt.Printf(" - Microseconds: %d\n", tv.TvUsec)
// 与 Go 标准库的结果进行对比
goTime := time.Now()
fmt.Printf("\nGo time.Now() result:\n")
fmt.Printf(" - Seconds: %d\n", goTime.Unix())
fmt.Printf(" - Microseconds component: %d\n", goTime.Nanosecond()/1000)
// 验证秒数是否大致相等
timeDiff := goTime.Unix() - tv.TvSec
if timeDiff < 0 {
timeDiff = -timeDiff
}
if timeDiff > 1 {
panic(fmt.Sprintf("seconds mismatch! Diff: %d", timeDiff))
}
fmt.Println("\nSuccess! The results are consistent.")
}
```


这个例子完美地展示了 ffi 库在处理复杂 C 函数调用时的核心价值：

#### 类型安全的函数签名定义

通过 ffi.PrepCif，我们以类型安全的方式精确描述了 C 函数 gettimeofday 的签名：

```
var cif ffi.Cif
ffi.PrepCif(&cif, ffi.DefaultAbi, 2, &ffi.TypeSint32, &ffi.TypePointer, &ffi.TypePointer)
```


这行代码清晰地表达了：

- 函数返回值类型：int (ffi.TypeSint32)
- 参数个数：2 个
- 参数类型：两个指针 (ffi.TypePointer)

无需手动计算结构体的内存布局或字段偏移量，ffi 通过底层的 libffi 自动处理所有平台相关的 ABI 细节。

#### Go-idiomatic 的结构体传递

我们可以直接使用 Go 原生结构体：

```
type Timeval struct {
TvSec int64 // 秒
TvUsec int64 // 微秒
}
var tv Timeval
```


然后通过标准的指针传递方式与 C 函数交互：

```
arg1 := unsafe.Pointer(&tv)
var arg2 unsafe.Pointer = nil
args := []unsafe.Pointer{
unsafe.Pointer(&arg1),
unsafe.Pointer(&arg2),
}
ffi.Call(&cif, gettimeofday_addr, unsafe.Pointer(&ret), args...)
```


#### 关键优势

-
**跨平台兼容性**：libffi 在底层处理了不同操作系统和 CPU 架构的调用约定差异（如寄存器使用、栈对齐等） -
**内存安全**：虽然使用了 unsafe.Pointer，但整个流程是受控的。ffi 确保了：- Go 结构体的内存布局与 C 结构体兼容
- 指针正确传递到 C 函数
- 返回值正确写回到 Go 变量

-
**无需 CGO**：整个过程通过 purego 和 ffi 实现，完全不依赖 CGO，可以在 CGO_ENABLED=0 环境下编译运行 -
**双层指针机制**：ffi.Call 使用指向参数指针的数组 ([]unsafe.Pointer)，这是 libffi 的标准设计，允许它处理任意类型和大小的参数，包括结构体、数组等复杂类型

#### 示例运行结果

```
// ffi目录下
$CGO_ENABLED=0 go run main.go
C gettimeofday result:
- Seconds: 1760619822
- Microseconds: 971252
Go time.Now() result:
- Seconds: 1760619822
- Microseconds component: 971309
Success! The results are consistent.
```


这个例子证明了我们成功地从 Go 代码调用了 C 标准库函数，并且结果与 Go 标准库的时间函数一致(seconds部分)，展示了 ffi 作为 CGO 替代方案的可行性和可靠性。这也正是 purego 自身难以优雅实现的，也是 ffi 为“纯 Go FFI”范式带来的最关键的补充。

## 小结

在这篇文章中，我们从 Go 社区对 CGO 的普遍焦虑出发，最终完成了一次对 Go FFI 三大核心范式的系统性巡礼。这场探索之旅清晰地表明：Go 与 C 生态的交互，已不再是一条“非 CGO 即重写”的独木桥。

purego 和 ffi 的出现，标志着**“纯 Go 运行时动态加载”**这一新范式的起步以及逐渐成熟。它并非意在完全取代 CGO——对于需要深度集成静态 C 库、或处理复杂 C 宏的场景，CGO 依然是官方的、最强大的解决方案。同样，它也无法替代 LLGO 体系在特定领域（如嵌入式）的独特优势。

然而，对于绝大多数需要在 Go 的现代化开发体验与庞大的 C 库生态之间建立连接的场景，purego 与 ffi 的组合，为我们提供了一套**更轻量、更快速、更符合 Go 哲学**的 FFI 方案。它们将 Go 强大的跨平台编译能力，从纯 Go 世界，成功地延伸到了与 C 交互的边界。

现在，当你的 Go 项目需要拥抱 C 生态时，你有了一份更清晰的决策地图：

-
**当你必须链接一个 C 静态库 (.a)，或处理大量复杂的 C 宏时：**

-> 坚守**原生 CGO**。这是它不可替代的核心优势区。 -
**当你的整个技术栈深度绑定 LLVM，或在嵌入式 (.wasm) 等资源受限环境中追求极致性能时：**

-> 关注并评估**LLGO / TinyGo**这一“编译器融合”范式。 -
**当你需要调用一个以共享库 (.so, .dylib, .dll) 形式发布的 C API 时：**- 如果函数签名只涉及
**基本类型**（整数、浮点数、指针、字符串）：

-> 首选**purego**。它最轻量，无外部依赖。 - 如果函数签名涉及
**按值传递/返回结构体，或需要处理复杂回调**：

-> 采用**purego + ffi**的黄金组合。

- 如果函数签名只涉及

下一次，当你因为一个 C 库而对 CGO 望而却步时，请记住，你已经有了更好的选择。

本文涉及的源码可以在[这里下载](https://github.com/bigwhite/experiments/tree/master/purego-and-ffi) – https://github.com/bigwhite/experiments/tree/master/purego-and-ffi

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


**想系统学习Go，构建扎实的知识体系？**

我的新书《[Go语言第一课](https://book.douban.com/subject/37499496/)》是你的首选。源自2.4万人好评的极客时间专栏，内容全面升级，同步至Go 1.24。首发期有专属五折优惠，不到40元即可入手，扫码即可拥有这本300页的Go语言入门宝典，即刻开启你的Go语言高效学习之旅！

![](../../assets/d3fd3ab3e1fd7a7e.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

深度好文，收藏了