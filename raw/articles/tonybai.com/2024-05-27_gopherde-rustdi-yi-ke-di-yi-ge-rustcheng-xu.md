---
title: Gopher的Rust第一课：第一个Rust程序
url: https://tonybai.com/2024/05/27/gopher-rust-first-lesson-first-rust-program/
published: '2024-05-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Gopher的Rust第一课：第一个Rust程序

![](../../assets/50bd9b06024f4be1.png)


[本文永久链接](https://tonybai.com/2024/05/27/gopher-rust-first-lesson-first-rust-program) – https://tonybai.com/2024/05/27/gopher-rust-first-lesson-first-rust-program

经过[上一章](https://tonybai.com/2024/05/10/gopher-rust-first-lesson-setup-dev-env/)的学习，我想现在你已经成功安装好一个Rust开发环境了，是时候撸起袖子开始写Rust代码了！

程序员这个历史并不算悠久的行当，却有着一个历史悠久的传统，那就是每种编程语言都将一个名为“hello, world”的示例作为这门语言学习的第一个例子，这个传统始于20世纪70年代那本大名鼎鼎的由布莱恩·科尼根（Brian W. Kernighan）与C语言之父丹尼斯·里奇（Dennis M. Ritchie）合著的《C程序设计语言》。

![](../../assets/6961676f300d081c.png)


在这一章中，我们也将遵从传统，从编写和运行一个可以打印出“hello, world”的Rust示例程序开始我们正式的Rust编码之旅。我希望通过这个示例程序你能够对Rust程序结构有一个直观且清晰的认识。

## 3.1 Hello, World

“Hello, World”是一门编程语言的最简单示例的表达形式。在Go中，我们可以像下面这样编写Go版本的Hello, World程序：

```
package main
func main() {
println("Hello, World!")
}
```


为了简单，我们甚至没有使用fmt包的Printf系列函数（这样就可以减少一行导入包的语句），而是用了内置函数println来完成将“Hello, World”输出到控制台（更准确的说是标准错误(stderr)）的任务。

Rust版本的Hello, World可以比Go还要简洁，我们在一个目录下（比如rust-guide-for-gopher/helloworld/rustc）创建一个hello_world.rs的文件。哦，没错！rust的源码文件都是**以.rs作为源文件扩展名的**。并且对于多个单词构成的文件名，rust的惯例是采用全小写单词+下划线连接的方式命名。这个hello_world.rs文件的内容如下：

```
fn main() {
println!("Hello, World!");
}
```


相比于Go在每个源文件中都要使用package指定该文件归属的包名，Rust无需这样的一行。和Go一样，这里的main是函数，所有可执行的Rust程序都必须有一个main函数，它是Rust程序的入口函数。和Go使用func函数声明函数不同，Rust声明函数的关键字为fn。在这个main函数中，我们调用println!将“Hello, World!”输出到控制台上。

不过，和Go内置的println函数不同的是，这里的println!并非是一个函数，而是一个**Rust宏(macro)**。

如果你只是学过Go，而没有学过C/C++语言，你甚至都不会知道宏(macro)是什么。在Rust中，宏是一种用于代码生成和转换的元编程工具。宏允许你在编译时根据一定的模式或规则来扩展代码。Rust宏分为声明宏（Declarative Macros）和过程宏（Procedural Macros）。println!就属于声明宏，它由macro_rules! 宏定义，我们在Rust标准库的源码中可以看到其定义：

```
// $(rustc --print sysroot)/lib/rustlib/src/rust/library/std/src/macros.rs
#[macro_export]
#[stable(feature = "rust1", since = "1.0.0")]
#[cfg_attr(not(test), rustc_diagnostic_item = "println_macro")]
#[allow_internal_unstable(print_internals, format_args_nl)]
macro_rules! println {
() => {
$crate::print!("\n")
};
($($arg:tt)*) => {{
$crate::io::_print($crate::format_args_nl!($($arg)*));
}};
}
```


在Rust源码编译过程中，声明宏是在最开始的预处理阶段进行扩展的，我们也可以通过nightly版的rustc命令来查看println!宏展开后的结果(-Z选项只能在nightly版本中使用)：

```
$rustc +nightly-2022-07-14-x86_64-apple-darwin -Zunpretty=expanded hello_world.rs
#![feature(prelude_import)]
#![no_std]
#[prelude_import]
use ::std::prelude::rust_2015::*;
#[macro_use]
extern crate std;
fn main() {
{
::std::io::_print(::core::fmt::Arguments::new_v1(&["Hello, World!\n"],
&[]));
};
}
```


我们看到：println!宏被替换为一个标准库下的函数(_print)的调用。btw，到这里，你可能和我一样，看不懂println!展开后的代码，没关系，我们后续会逐步学习并掌握这些语法的。此外，宏是Rust的高级特性，这里也不展开说了。

另外一个和Go在语法上有所不同的是，Rust在每行语句后面都要**显式使用分号**，对于Gopher而言，这个很容易遗忘。

接下来，我们来编译和运行一下这个Rust版的Hello，World!，编译运行Rust代码的最简单方法就是通过rustc编译器将rust源码文件编译为可执行程序：

```
$rustc hello_world.rs
$ls
hello_world* hello_world.rs
```


我们看到，示例通过调用rustc将hello_world.rs编译为了hello_world可执行文件。

运行rustc编译后的可执行文件将得到下面输出结果：

```
$./hello_world
Hello, World!
```


我们看到”Hello, World!”被打印到控制台。

如果觉得默认编译出的hello_world文件名字较长，我们也可以像go build -o那样指定rustc编译后得到的目标可执行文件的名字，下面的命令通过-o选项将编译后的程序命名为hello：

```
$rustc -o hello hello_world.rs
```


rustc编译出来的二进制文件size并不大，仅有400多KB（而Go默认构建的Hello, World!有1.3MB，在我的macOS上）：

```
$ls -lh
total 856
-rwxr-xr-x 1 tonybai staff 423K 4 20 17:56 hello_world*
```


我们还可以通过去掉symbols的方式继续让其“瘦身”到不到300KB(通过go build -ldflags=”-s -w” helloworld.go去除符号表和调试信息的Go二进制程序还有近900K的大小)：

```
$rustc -C strip=symbols hello_world.rs
$ll -h
total 608
-rwxr-xr-x 1 tonybai staff 297K 4 20 17:57 hello_world*
```


上面的”Hello, World”程序虽然足够简单，也能够运行，但对于初学者而言，它有两个“不足”：一来这个例子的确“太简单”，简单到无法充分展示单个Rust源码文件的结构；二来这个示例只使用了一个单个源文件，与实际开发中那种由多个文件组成的Rust实用工程有差别，同样无法帮助我们理解实用性的Rust工程的结构。

为了更好地理解Rust工程与单个源文件的构成，我们将编写一个稍微复杂一点的版本，它将使用Rust的构建管理工具cargo建立，并使用Rust标准库中的std::io模块进行输入/输出操作。

## 3.2 cargo版本的Hello, World

在实际开发中，Rust程序通常由多个源文件组成，并使用Cargo作为构建系统和包管理器。Cargo可以帮助我们管理项目的源代码、依赖库、构建任务等。下面我们就来创建一个使用Cargo的”Hello, World”。

### 3.2.1 使用Cargo创建Hello，World

我们在一个目录下（比如：rust-guide-for-gopher/helloworld/cargo）执行下面命令来创建hello_world：

```
$cargo new hello_world
Created binary (application) `hello_world` package
```


cargo默认创建了一个binary（application）类型的rust package，我们来看看初始情况下这个rust package下都有哪些内容：

```
$tree hello_world
hello_world
├── Cargo.toml
└── src
└── main.rs
1 directory, 2 files
```


其中，Cargo.toml是Rust包的清单(manifest)文件。它包含有关包及其依赖项的元数据。以下是上面Cargo.toml文件的全部内容：

```
// Cargo.toml
[package]
name = "hello_world"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
```


其中package下面的字段含义如下：

- name: 包的名称；
- version: 包的版本，遵循语义化版本控制规则；
- edition: 包使用的Rust版本(edition)。在这里，它被设置为目前的最新edition：2021版。edition提供了一种向后兼容的方式来演化和改进Rust。每个edition都是向后兼容的，这意味着旧edition下编写的Rust代码可以继续在新edition版本的Rust下编译和运行，而无需进行修改。这样，开发者可以按照自己的节奏选择是否迁移到新的edition。

dependencies下面则是会记录该package对第三方依赖的情况，这个示例中并无三方依赖，因此这里为空。

我们的代码放在了src目录下，这也是rust包的标准布局。为了更好地理解Rust程序的构成，我们将编写一个稍微复杂一点的Hello, World!版本，它使用Rust标准库中的std::io模块进行输入/输出操作：

```
// rust-guide-for-gopher/helloworld/cargo/hello_world/src/main.rs
use std::io;
use std::io::Write;
fn main() {
let mut output = io::stdout();
output.write(b"Hello, World!").unwrap();
output.flush().unwrap();
}
```


这个Rust的”Hello, World”程序展示了一个典型的Rust源文件结构，包括导入语句、主函数定义以及一系列的方法调用。它演示了如何使用标准库的io模块来向标准输出流打印”Hello, World!”。下面是对其程序结构的简单总结：

- 导入语句

源文件在最开始处使用use std::io; 和use std::io::Write;这两行导入了标准库中的io模块及其Write trait。这样程序就可以在后面的代码中直接使用io和Write，而无需完整地写出它们的命名空间。这里我们先不用关心trait是什么，你大可将其理解为和Go interface差不多的语法元素就行了。

- 主函数

main定义了程序的入口点。Rust 程序从main函数开始执行。

- 可变变量

let mut output = io::stdout(); 这行代码创建了一个可变变量output，它绑定到了一个标准输出流（stdout）。mut关键字表示该变量是可变的，可以在后续代码中修改它的值。关于变量以及绑定，我们在后面有专门的章节说明。这里要注意的是，和Go变量不同的是，Rust中的变量默认是不可变的，只有显式用mut声明的变量才是可变的。

- 方法调用

output.write(b”Hello, World!”).unwrap(); 调用了output的write方法，传递了一个字节串作为参数。该方法用于将字节写入输出流。unwrap方法用于处理方法调用可能产生的错误，它在这里表示“我相信这个方法调用会成功，如果不成功，就让程序 panic”。同理，output.flush().unwrap()也是这样的。关于错误以及异常处理的话题，我们会在后面进行专题性学习。

理解了源码后，我们来编译和运行一下这个程序，这次我们不再使用rustc，而是用cargo来实现。

### 3.2.2 使用Cargo构建Hello, World

要构建上面的示例程序，我们只需在项目根目录下运行下面命令:

```
$cargo build
Compiling hello_world v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/helloworld/cargo/hello_world)
Finished dev [unoptimized + debuginfo] target(s) in 1.23s
```


构建成功后，我们再来查看一下当前项目下的结构变化：

```
$tree -F
.
├── Cargo.lock
├── Cargo.toml
├── src/
│ └── main.rs
└── target/
├── CACHEDIR.TAG
└── debug/
├── build/
├── deps/
│ ├── hello_world-07284f5d84374479*
│ ├── hello_world-07284f5d84374479.1atc14vk0u28taij.rcgu.o
│ ├── hello_world-07284f5d84374479.1bu89c2i9mazzqif.rcgu.o
│ ├── hello_world-07284f5d84374479.26e3nxhmk9lhy9zy.rcgu.o
│ ├── hello_world-07284f5d84374479.29l81xyv0i4g8s88.rcgu.o
│ ├── hello_world-07284f5d84374479.41i7ln85cwseljfw.rcgu.o
│ ├── hello_world-07284f5d84374479.4iz3ubiqrvegnjdp.rcgu.o
│ ├── hello_world-07284f5d84374479.53vu8cjirf8g6rnw.rcgu.o
│ ├── hello_world-07284f5d84374479.5f6ye0ayl23rccqv.rcgu.o
│ └── hello_world-07284f5d84374479.d
├── examples/
├── hello_world*
├── hello_world.d
└── incremental/
└── hello_world-16yuztatbr0vh/
├── s-gvfwmugno5-1gy801r-1i2g78r4nmg489ix0nuktmqgb/
│ ├── 1atc14vk0u28taij.o
│ ├── 1bu89c2i9mazzqif.o
│ ├── 26e3nxhmk9lhy9zy.o
│ ├── 29l81xyv0i4g8s88.o
│ ├── 41i7ln85cwseljfw.o
│ ├── 4iz3ubiqrvegnjdp.o
│ ├── 53vu8cjirf8g6rnw.o
│ ├── 5f6ye0ayl23rccqv.o
│ ├── dep-graph.bin
│ ├── query-cache.bin
│ └── work-products.bin
└── s-gvfwmugno5-1gy801r.lock*
9 directories, 28 files
```


我们看到cargo build执行后，项目下多出了好多目录和文件。这些目录和文件都是做什么的呢？我们挑选主要的来看一下。

- Cargo.lock文件

Cargo的锁定文件，用于记录每个依赖项的确切版本号，以保证构建的可重复性。

这个示例中由于没有使用第三方依赖，这个Cargo.lock文件中的内容不具典型性：

```
# This file is automatically @generated by Cargo.
# It is not intended for manual editing.
version = 3
[[package]]
name = "hello_world"
version = "0.1.0"
```


另外Cargo.lock文件完全由cargo自动管理，开发人员不需要也不应该对其进行手动修改。

- target目录

存放构建输出的目录，用于存储编译后的目标文件和可执行文件。

- target/CACHEDIR.TAG

用于标记target目录为一个缓存目录的文件。它的内容如下：

```
$cat CACHEDIR.TAG
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag created by cargo.
# For information about cache directory tags see https://bford.info/cachedir/
```


这是一个符合[Cache Directory Tagging Specification](https://bford.info/cachedir/)的Tag文件。

- target/debug

调试模式下的构建输出目录，存储生成的可执行文件和相关文件。

- target/debug/incremental

增量编译的目录，用于存储增量编译过程中的临时文件和缓存。

Rust编译过程缓慢，这个对比Go简直就是地下天上。在日常开发中，基于增量编译的文件进行增量构建可以大幅缩短编译时间。

- target/debug/build

编译过程中生成的临时构建文件的目录。

- target/debug/deps

存储编译生成的目标文件（.o 文件）和相关的依赖项。

- target/debug/hello_world

调试模式下生成的可执行文件。

- target/debug/hello_world.d

与hello_world相关的依赖关系信息的文件。

执行debug目录下的hello_world将得到如下输出：

```
$./target/debug/hello_world
Hello, World!
```


在Go中我们可以使用go run来直接编译和运行Go源码文件，cargo也提供了该功能，我们在项目根目录下运行cargo run也可以编译和执行hello_world：

```
$cargo run
Finished dev [unoptimized + debuginfo] target(s) in 0.05s
Running `target/debug/hello_world`
Hello, World!
```


无论是cargo run还是cargo build，默认构建的都是debug版本的可执行程序，程序中包含大量符号信息和调试信息，并且其优化级别也不是很高。发布到生产环境的程序应该是release模式下的，通过–release参数，我们可以构建release版本的可执行程序：

```
$cargo build --release
Compiling hello_world v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/helloworld/cargo/hello_world)
Finished release [optimized] target(s) in 1.06s
```


构建后，target目录下会多出一个release目录，其下面的内容如下：

```
$tree -F target/release
target/release
├── build/
├── deps/
│ ├── hello_world-c41defdc625f9244*
│ └── hello_world-c41defdc625f9244.d
├── examples/
├── hello_world*
├── hello_world.d
└── incremental/
4 directories, 4 files
```


相对于debug版本，release版本由于实时了大量优化，通常其构建时间会比debug版本要长。但构建出的release版本的size则要小很多。

无论是debug，还是release版，target下面都生成了许多中间文件，如果要清理文件并重头构建，我们可以使用cargo clean命令将target彻底清除：

```
$cargo clean
Removed 40 files, 2.1MiB total
```


当然cargo clean也支持一些命令行参数，可以选择清除哪些文件。

### 3.2.3 使用Cargo创建library类包

通过上面的例子，我们知道cargo new默认创建的binary类型的rust package，如果我们要创建library类型的rust package，我们需要向cargo new传递–lib选项。下面的命令创建一个名为foo的library类型的rust package：

```
$cargo new --lib foo
Created library `foo` package
```


我们看一下foo package下的目录结构：

```
$tree -F foo
foo
├── Cargo.toml
└── src/
└── lib.rs
1 directory, 2 files
```


和binary类不同的是，src目录下不再是main.rs，而是lib.rs，它是library类package的入口：

```
//rust-guide-for-gopher/helloworld/cargo/foo/lib.rs
pub fn add(left: usize, right: usize) -> usize {
left + right
}
#[cfg(test)]
mod tests {
use super::*;
#[test]
fn it_works() {
let result = add(2, 2);
assert_eq!(result, 4);
}
}
```


lib.rs中只是一个library类package的入口模板，开发人员需要根据自己的需要对其进行调整。关于lib.rs中的内容，我们将在下一章讲解Rust代码组织时做细致说明，这里就不展开说了。

对于library类Rust package，我们同样可以通过cargo build和cargo build –release构建，下面是执行构建后目录文件情况：

```
$tree
.
├── Cargo.lock
├── Cargo.toml
├── src
│ └── lib.rs
└── target
├── CACHEDIR.TAG
├── debug
│ ├── build
│ ├── deps
│ │ ├── foo-24c6d6228c521501.2k5t0f94hnorqpgh.rcgu.o
│ │ ├── foo-24c6d6228c521501.d
│ │ ├── libfoo-24c6d6228c521501.rlib
│ │ └── libfoo-24c6d6228c521501.rmeta
│ ├── examples
│ ├── incremental
│ │ └── foo-m2biu8poxl6i
│ │ ├── s-gvg68shtlp-1oqrf4n-irxhgoe7rhwmtvj6jwexcu0h
│ │ │ ├── 2k5t0f94hnorqpgh.o
│ │ │ ├── dep-graph.bin
│ │ │ ├── query-cache.bin
│ │ │ └── work-products.bin
│ │ └── s-gvg68shtlp-1oqrf4n.lock
│ ├── libfoo.d
│ └── libfoo.rlib
└── release
├── build
├── deps
│ ├── foo-9f2dd76beda509bd.d
│ ├── libfoo-9f2dd76beda509bd.rlib
│ └── libfoo-9f2dd76beda509bd.rmeta
├── examples
├── incremental
├── libfoo.d
└── libfoo.rlib
14 directories, 20 files
```


我们看到，无论是debug还是release，cargo build构建的结果都是libfoo.rlib。.rlib文件是Rust的静态库文件，通常用于代码的模块化和重用，我们在后续章节讲解中，会详细说明如何使用这些构建出来的静态库。

## 3.3 小结

本文介绍了如何使用Rust编写”Hello, World”程序，并分别给出了rustc版和cargo版的hello, world程序版本。

在这个过程中，文章还介绍了Rust中的宏概念，并展示了如何使用println!宏来输出文本。

之后，文章聚焦于使用Cargo构建的hello，world程序版本，介绍了cargo的构建、清理、debug和release版本的区别等，最后还提及了如何使用cargo创建library类的Rust package。

cargo贯穿Rust程序的整个生命周期，在后续的每一章中可能都会提及cargo。

本章中涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/rust-guide-for-gopher/helloworld)下载。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论