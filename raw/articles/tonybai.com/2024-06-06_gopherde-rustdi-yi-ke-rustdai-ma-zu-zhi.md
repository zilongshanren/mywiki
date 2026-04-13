---
title: Gopher的Rust第一课：Rust代码组织
url: https://tonybai.com/2024/06/06/gopher-rust-first-lesson-organizing-rust-code/
published: '2024-06-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Gopher的Rust第一课：Rust代码组织

![](../../assets/d9fbf86a269c90cc.png)


[本文永久链接](https://tonybai.com/2024/06/06/gopher-rust-first-lesson-organizing-rust-code) – https://tonybai.com/2024/06/06/gopher-rust-first-lesson-organizing-rust-code

在上一章的讲解中，我们编写了[第一个Rust示例程序”hello, world”](https://tonybai.com/2024/05/27/gopher-rust-first-lesson-first-rust-program)，并给出了rustc版和cargo版本。在真实开发中，我们都会使用cargo来创建和管理Rust包。不过，Hello, world示例非常简单，仅仅由一个Rust源码文件组成，而且所有源码文件都在同一个目录中。但真实世界中的实用Rust程序，无论是公司商业项目，还是一些知名的开源项目，甚至是一些稍复杂一些的供教学使用的示例程序，它们通常可不会这么简单，都有着复杂的代码结构。

Rust初学者在阅读这些项目源码时便仿佛进入了迷宫，不知道该走哪条（阅读代码的）路径，不知道每个目录代表的含义，也不知道自己想看的源码究竟在哪个目录下。但目前市面上的Rust入门教程大多没有重视初学者的这一问题，要么没有对Rust项目代码组织结构进行针对性的讲解，要么是将讲解放到书籍的后面章节。

根据我个人的学习经验来看，理解一个实用Rust项目的代码组织结构越早，对后续的Rust学习越有益处。同时，掌握Rust项目的代码组织结构也是Rust开发者走向编写复杂Rust程序的必经的一步。并且，初学者在了解项目的代码组织结构后，便可以自主阅读一些复杂的Rust项目的源码，可提高Rust学习的效率，提升学习效果。因此，我决定在介绍Rust基础语法之前先在本章中系统地介绍Rust的代码组织结构，以满足很多Rust初学者的述求。

但在介绍Rust代码组织结构之前，我们需要先来系统说明一下Rust代码组织结构中的几个重要概念，它们是了解Rust项目代码组织结构的前提。

## 4.1 回顾Go代码组织

Go项目代码组织由module和package两级组成。通常来说，每个Go repo就是一个module，由repo根目录下的go.mod定义，go.mod文件所在目录也被称为module root。go.mod中典型内容如下：

```
// go.mod
module github.com/user/mymodule[/vN]
go 1.22.1
... ...
```


go.mod中的module directive一行后面的github.com/user/mymodule/[vN]是module path。module path一来可以反映该module的具体网络位置，同时也是该module下面的Go package导入(import)路径的组成部分。module root下的子目录中通常存放着该module下面的Go package，比如module root/foo目录下存放的Go包的导入路径为github.com/user/mymodule[/vN]/foo。

Go package是Go的编译单元，也是功能单元，代码内外部导入和引用的单位也都是包。而go module是后加入的，更多用于管理包的版本（一个module下的所有包都统一进行版本管理）以及构建时第三方依赖和版本的管理。

更多关于Go module和package管理以及Go项目布局的内容，可以详见我的极客时间

[《Go语言第一课》]专栏。

个人认为Go的module和package的两级管理还是很好理解和管理的，在这方面Rust的代码组织形式又是怎样的呢？接下来，我们就来正式看看Rust的代码组织。

## 4.2 rustc-only的Rust项目

Rust是系统编程语言，这让我想起了当初在Go成为我个人主力语言之前使用C/C++进行开发的岁月。C/C++是没有像go或Rust的cargo那样的统一的包依赖管理器和项目构建管理工具的。编译器(如gcc等)是核心工具，而项目构建管理则经常由其他工具负责，如Makefile、CMake，或者是Google的[Bazel](https://github.com/bazelbuild/bazel)等。在Windows上开发应用的，则往往使用微软或其他开发者工具公司提供的IDE，如当年炙手可热的Visual Studio系列。

下面表格展示了各语言的编译器/链接器和构建管理工具的关系：

![](../../assets/28f0a127c867bf31.png)


像cargo、go这样的“一站式”工具链都旨在为开发者提供体验更为友好的交互接口的，在幕后，它们仍然依赖于底层的编译器和链接器（如rustc和go tool compile/link）来执行实际的代码编译。

不过，像cargo这样的高级工具也给开发人员带来了额外的抽象，或是叫“掩盖”了一些真相，这有时候让人看不清构建过程的本质，比如：很多Gopher用了很多年Go，但却不知道go tool compile/link的存在。

本着只有in hard way，才能看到和抓住本质的思路，以及之前学习用系统编程语言C/C++时经验，这里我们先来看一些**rustc-only的Rust项目**。Rustc-only的Rust项目是指不使用Cargo创建和管理的Rust项目，而是直接使用rustc编译器来编译和构建项目。这意味着开发者需要编写自己的构建脚本，例如使用Makefile或其他构建工具来管理项目的构建过程。

不过，请注意：**这类项目极少用于生产**，即便是那些不需要复杂的依赖管理的小型项目。这里使用rustc-only的Rust项目仅仅是为了学习和了解Rustc编译器的主要功能机制以及Rust语言在代码组织上的一些抽象，比如module等。

下面我们就从最简单的rustc-only项目开始，先来看看只有一个Rust源文件且无其他依赖项的“最简项目”。

### 4.2.1 单文件项目

所谓单文件项目，即只有一个Rust源文件，例如前面章节中的hello_world.rs，这种项目可以直接使用rustc编译器来编译和运行：

```
// rust-guide-for-gopher/organizing-rust-code/rustc-only/single/hello-world/hello_world.rs
fn main() {
println!("Hello, world!");
}
```


对于顶层带有main函数的源文件，rustc会默认将其视为binary crate类型的源文件，并将其编译为可执行二进制文件hello_world。

我们当然也可以强制的让rustc将该源文件视为library crate类型的源文件，并将其编译为其他类型的crate输出文件，rustc支持多种crate type：

```
--crate-type [bin|lib|rlib|dylib|cdylib|staticlib|proc-macro]
Comma separated list of types of crates
for the compiler to emit
```


在[rustc的文档](https://doc.rust-lang.org/rustc/what-is-rustc.html)中，各种crate类型的含义如下：

```
lib — Generates a library kind preferred by the compiler, currently defaults to rlib.
rlib — A Rust static library.
staticlib — A native static library.
dylib — A Rust dynamic library.
cdylib — A native dynamic library.
bin — A runnable executable program.
proc-macro — Generates a format suitable for a procedural macro library that may be loaded by the compiler.
```


不过，如果强制将带有顶层main函数的rust源文件视为lib crate型的，那么rustc将会报warning，提醒你函数main将是死代码，永远不会被用到：

```
$rustc --crate-type lib hello_world.rs
warning: function `main` is never used
--> hello_world.rs:1:4
|
1 | fn main() {
| ^^^^
|
= note: `#[warn(dead_code)]` on by default
warning: 1 warning emitted
```


但即便如此，一个名为libhello_world.rlib的文件依然会被rustc生成出来！（目前–crate-type lib等同于–create-type rlib)。

### 4.2.2 有外部依赖项的单文件项目

日常开发中，像上面的Hello, World级别的trivial应用是极其少见的，一个non-trivial的Rust应用或多或少都会有一些依赖。这里我们也来看一下如何基于rustc来构建带有外部依赖的单文件项目。下面是一个带有外部依赖的示例：

```
// organizing-rust-code/rustc-only/single/hello-world-with-deps/hello_world.rs
extern crate rand;
use rand::Rng;
fn main() {
let mut rng = rand::thread_rng();
let num: u32 = rng.gen();
println!("Random number: {}", num);
}
```


这个示例程序依赖一个名为rand的crate，要编译该程序，我们必须先手动下载rand的crate源码，并在本地将rand源码编译为示例程序所需的rust library。下面步骤展示了如何下载和构建rand crate：

```
$curl -LO https://crates.io/api/v1/crates/rand/0.8.5/download
$tar -xvf download
```


解压后，我们将看到rand-0.8.5这样的一个crate目录，进入该目录，我们执行cargo build来构建rand crate：

```
$cd rand-0.8.5
$cargo build
... ...
Finished dev [unoptimized + debuginfo] target(s) in 0.19s
```


cargo构建出的librand.rlib就在rand-0.8.5/target/debug下。

注：rlib的命名方式：lib+{crate_name}.rlib


接下来，我们就来构建一下依赖rand crate的hello_world.rs：

```
// 在organizing-rust-code/rustc-only/single/hello-world-with-deps下面执行
$rustc --verbose -L ./rand-0.8.5/target/debug --extern rand=librand.rlib hello_world.rs
error[E0463]: can't find crate for `rand_core` which `rand` depends on
--> hello_world.rs:1:1
|
1 | extern crate rand;
| ^^^^^^^^^^^^^^^^^^ can't find crate
error: aborting due to 1 previous error
For more information about this error, try `rustc --explain E0463`.
```


我们看到rustc的编译错误提示：无法找到rand crate依赖的rand_core crate！也就是说我们除了向rustc提供hello_world.rs依赖的rand crate之外，还要向rustc提供rand crate的各种依赖！

rand crate的各种依赖在哪里呢？我们在构建rand crate时，cargo build将各种依赖都放在了rand-0.8.5/target/debug/deps目录下了：

```
$ls -l|grep ".rlib"
-rw-r--r-- 1 tonybai staff 6896 4 29 06:45 libcfg_if-cd6bebf18fb9c234.rlib
-rw-r--r-- 1 tonybai staff 204072 4 29 06:45 libgetrandom-df6a8e95e188fc56.rlib
-rw-r--r-- 1 tonybai staff 1651320 4 29 06:45 liblibc-f16531562d07b476.rlib
-rw-r--r-- 1 tonybai staff 959408 4 29 06:45 libppv_lite86-f1d97d485bc43617.rlib
-rw-r--r-- 1 tonybai staff 1784376 4 29 06:45 librand-9a91ea8db926e840.rlib
-rw-r--r-- 1 tonybai staff 987936 4 29 06:45 librand_chacha-6fe22bd8b3bb228c.rlib
-rw-r--r-- 1 tonybai staff 256768 4 29 06:45 librand_core-fc905f6ca5f8533b.rlib
```


我们看到其中还包含了librand自身：librand-9a91ea8db926e840.rlib。我们来试试基于deps目录下的这些依赖rlib编译一下：

```
$rustc --verbose --extern rand=rand-0.8.5/target/debug/deps/librand-9a91ea8db926e840.rlib -L rand-0.8.5/target/debug/deps --extern rand_core=librand_core-fc905f6ca5f8533b.rlib --extern getrandom=libgetrandom-df6a8e95e188fc56.rlib --extern cfg_if=libcfg_if-cd6bebf18fb9c234.rlib --extern libc=liblibc-f16531562d07b476.rlib --extern rand_chacha=librand_chacha-6fe22bd8b3bb228c.rlib --extern ppv_lite86=libppv_lite86-f1d97d485bc43617.rlib hello_world.rs
```


我们用rustc成功编译了带有外部依赖的Rust源码。不过这里要注意的是rustc对直接依赖和间接依赖的crate的定位方式有所不同。

对于直接依赖的crate，比如这里的rand crate，我们需要给出具体路径，它不依赖-L的位置指示，所以这里我们使用了–extern rand=rand-0.8.5/target/debug/deps/librand-9a91ea8db926e840.rlib。

对于间接依赖的crate，比如rand crate依赖的rand_core，rust会结合-L指示的位置以及–extern一起来定位，这里-L指示路径为rand-0.8.5/target/debug/deps，–extern rand_core=librand_core-fc905f6ca5f8533b.rlib，那么rustc就会在rand-0.8.5/target/debug/deps下面搜索librand_core-fc905f6ca5f8533b.rlib是否存在。

我们运行rustc构建出的可执行文件，输出如下：

```
$./hello_world
Random number: 431751199
```


### 4.2.3 有外部依赖的多文件项目

在Go中，如果某个目录下有多个源文件，那么通常这几个源文件均归属于同一个Go包(可能的例外的是*_test.go文件的包名)。但在Rust中，情况就会变得复杂了一些，我们来看一个例子：

```
// organizing-rust-code/rustc-only/multi/multi-file-with-deps
$tree -F -L 2
.
├── main.rs
├── sub1/
│ ├── bar.rs
│ ├── foo.rs
│ └── mod.rs
└── sub2.rs
```


在这个示例中，我们看到除了main.rs之外，还有一个sub2.rs以及一个目录sub1，sub1下面还有三个rs文件。我们从main.rs开始，逐一看一下各个源文件的内容：

```
// organizing-rust-code/rustc-only/multi/multi-file-with-deps/main.rs
1 extern crate rand;
2 use rand::Rng;
3
4 mod sub1;
5 mod sub2;
6
7 mod sub3 {
8 pub fn func1() {
9 println!("called {}::func1()", module_path!());
10 }
11 pub fn func2() {
12 self::func1();
13 println!("called {}::func2()", module_path!());
14 super::func1();
15 }
16 }
17
18 fn func1() {
19 println!("called {}::func1()", module_path!());
20 }
21
22 fn main() {
23 println!("current module: {}", module_path!());
24 let mut rng = rand::thread_rng();
25 let num: u32 = rng.gen();
26 println!("Random number: {}", num);
27
28 sub1::func1();
29 sub2::func1();
30 sub3::func2();
31 }
```


在main.rs中，我们除了看到了第1~2行的对外部rand crate的依赖外，我们还看到了一种新的语法元素：**rust module**。这里涉及sub1~sub3三个module，我们分别来看一下。先来看一下最直观的、定义在main.rs中的sub3 module。

第7行~第16行的代码定义了一个名为sub3的module，它包含两个函数func1和func2，这两个函数前面的pub关键字表明他们是sub3 module的publish函数，可以被module之外的代码所访问。任何未标记为pub的函数都是私有的，只能在模块内部及其子模块中使用。

在sub3 module的func2函数中，我们调用了self::func1()函数，self指代是模块自身，因此这个self::func1()函数就是sub3的func1函数。而接下来调用的super::func1()调用的语义你大概也能猜到。super指代的是sub3的父模块，而super::func1()就是sub3的父模块中的func1函数。

sub3的父模块就是这个项目的顶层模块，我们在main函数的入口处使用module_path!宏输出了该顶层模块的名称。

和sub3在main.rs中定义不同，sub1和sub2也分别代表了另外两种module的定义方式。

当Rust编译器看到第4行mod sub1后，它会寻找当前目录下是否有名为sub1.rs的源文件或是sub1/mod.rs源文件。在这个示例中，sub1定义在sub1目录下的mod.rs中：

```
// organizing-rust-code/rustc-only/multi/multi-file-with-deps/sub1/mod.rs
pub mod bar;
pub mod foo;
pub fn func1() {
println!("called {}::func1()", module_path!());
foo::func1();
bar::func1();
}
```


我们看到sub1/mod.rs中定义了一个公共函数func1，同时也在最开始处又嵌套定义了bar和foo两个module，并在func1中调用了两个嵌套子module的函数：

bar和foo两个module都是使用单文件module定义的，编译器会在sub1目录下搜寻foo.rs和bar.rs：

```
// organizing-rust-code/rustc-only/multi/multi-file-with-deps/sub1/foo.rs
pub fn func1() {
println!("called {}::func1()", module_path!());
}
// organizing-rust-code/rustc-only/multi/multi-file-with-deps/sub1/bar.rs
pub fn func1() {
println!("called {}::func1()", module_path!());
}
```


而main.rs中的sub2也是一个单文件的module，其源码位于顶层目录下的sub2.rs文件中：

```
// organizing-rust-code/rustc-only/multi/multi-file-with-deps/sub2.rs
pub fn func1() {
println!("called {}::func1()", module_path!());
}
```


现在我们来编译和执行一下这个既有外部依赖，又是多文件且有多个module的rustc-only项目：

```
$rustc --verbose --extern rand=rand-0.8.5/target/debug/deps/librand-9a91ea8db926e840.rlib -L rand-0.8.5/target/debug/deps --extern rand_core=librand_core-fc905f6ca5f8533b.rlib --extern getrandom=libgetrandom-df6a8e95e188fc56.rlib --extern cfg_if=libcfg_if-cd6bebf18fb9c234.rlib --extern libc=liblibc-f16531562d07b476.rlib --extern rand_chacha=librand_chacha-6fe22bd8b3bb228c.rlib --extern ppv_lite86=libppv_lite86-f1d97d485bc43617.rlib main.rs
$./main
current module: main
Random number: 2691905579
called main::sub1::func1()
called main::sub1::foo::func1()
called main::sub1::bar::func1()
called main::sub2::func1()
called main::sub3::func1()
called main::sub3::func2()
called main::func1()
```


上面示例演示了三种rust module的定义方法：

- 直接将定义嵌入在某个rust源文件中：

```
mod module_name {
}
```


- 通过module_name.rs
- 通过module_name/mod.rs

在一个单crate的项目中，通过rust module可以满足项目内部代码组织的需要。

最后，我们再来看一个有多个crate的项目形式。

### 4.2.4 有多个crate的项目

下面是一个有着多个crate项目的示例：

```
// organizing-rust-code/rustc-only/workspace
$tree -L 2 -F
.
├── main.rs
├── my_local_crate1/
│ └── lib.rs
└── my_local_crate2/
└── lib.rs
```


在这个示例中有三个crate，一个是顶层的binary类型的crate，入口为main.rs，另外两个都是lib类型的crate，入口都在lib.rs中，我们贴一下他们的源码：

```
// organizing-rust-code/rustc-only/workspace/main.rs
extern crate my_local_crate1;
extern crate my_local_crate2;
fn main() {
let x = 5;
let y = my_local_crate1::add_one(x);
let z = my_local_crate2::multiply_two(y);
println!("Result: {}", z);
}
// organizing-rust-code/rustc-only/workspace/my_local_crate1/lib.rs
pub fn add_one(x: i32) -> i32 {
x + 1
}
// organizing-rust-code/rustc-only/workspace/my_local_crate2/lib.rs
pub fn multiply_two(x: i32) -> i32 {
x * 2
}
```


要构建这个带有三个crate的项目，我们需要首先编译my_local_crate1和my_local_crate2这两个lib crates：

```
$rustc --crate-type lib --crate-name my_local_crate1 my_local_crate1/lib.rs
$rustc --crate-type lib --crate-name my_local_crate2 my_local_crate2/lib.rs
```


这会在项目顶层目录下生成两个rlib文件：

```
$ls |grep rlib
libmy_local_crate1.rlib
libmy_local_crate2.rlib
```


之后，我们就可以用之前学到的方法编译binary crate了：

```
$rustc --extern my_local_crate1=libmy_local_crate1.rlib --extern my_local_crate2=libmy_local_crate2.rlib main.rs
```


上述的几个rustc-only的rust项目都是hard模式的，即一切都需要手工去做，包括下载crate、编译crate时传入各种路径等。在真正的生产中，Rustacean们是不会这么做的，而是会直接使用cargo对rust项目进行管理。接下来，我们就来系统地看一下使用cargo进行rust项目管理以及对应的rust代码组织形式。

## 4.3 使用cargo管理的Rust项目

在前面的章节中，我们见识过了：Rust的包管理器Cargo是一个强大的工具，可以帮助我们轻松地管理Rust项目，cargo才是生产类项目的项目构建管理工具标准，它可以让Rustacean避免复杂的手工rustc操作。Cargo提供了许多功能，包括依赖项管理、构建和测试等。不过在这篇文章中，我不会介绍这些功能，而是看看使用cargo管理的Rust项目都有哪些代码组织模式。

Rust项目的代码组织结构可以分为两类：单一package和多个package。

什么是package？在之前的rust-only项目中，我们可从未见到过package！package是cargo引入的一个管理单元概念，它指的是一个独立的Rust项目，包含了源代码、依赖项和配置信息。每个Package都有一个唯一的名称和版本号，用于标识和管理项目。因此，在[the cargo book](https://doc.rust-lang.org/cargo/index.html)中，cargo也被称为“Rust package manager”，crates.io也被称为“the Rust community’s package registry”。

最能直观体现package存在的就是下面Cargo.toml中的配置了：

```
[package]
name = "hello_world"
version = "0.1.0"
edition = "2021"
[dependencies]
```


下面我们就来看看不同类型的rust package的代码组织形式。我们先从单一package形态的项目来开始。

### 4.3.1 单一package的rust项目

单一package项目是指整个项目只有一个Cargo.toml文件。这种项目还可以进一步分为三类：

- 单一Binary Crate
- 单一Library Crate
- 多个Binary Crate和一个Library Crate

下面我们分别举例来说明一下这三类项目。

#### 4.3.1.1 单一Binary Crate

我们进入organizing-rust-code/cargo/single-package/single-binary-crate，然后执行下面命令来创建一个单一Binary Crate的项目：

```
$cargo new hello_world --bin
Created binary (application) `hello_world` package
```


这个例子我们在之前的章节中也是见过的，它的结构如下：

```
$tree hello_world
hello_world
├── Cargo.toml
└── src
└── main.rs
1 directory, 2 files
```


默认生成的Cargo.toml内容如下：

```
[package]
name = "hello_world"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
```


使用cargo build即可完成该项目的构建：

```
$cargo build
Compiling hello_world v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/organizing-rust-code/cargo/single-package/single-binary-crate/hello_world)
Finished dev [unoptimized + debuginfo] target(s) in 1.16s
```


为了更显式地体现这是一个binary crate，我们可以在Cargo.toml增加如下内容：

```
[[bin]]
name = "hello_world"
path = "src/main.rs"
```


这不会影响cargo的构建结果！

通过cargo run可以查看构建出的可执行文件的运行结果：

```
$cargo run
Finished dev [unoptimized + debuginfo] target(s) in 0.06s
Running `target/debug/hello_world`
Hello, world!
```


接下来，我们再来看看单一library crate的rust项目。

#### 4.3.1.2 单一Library Crate

我们进入organizing-rust-code/cargo/single-package/single-library-crate，然后执行下面命令来创建一个单一Library Crate的项目：

```
$cargo new my_library --lib
Created library `my_library` package
```


创建后的my_library项目的结构如下：

```
$tree
.
├── Cargo.toml
└── src
└── lib.rs
```


默认生成的Cargo.toml如下：

```
[package]
name = "my_library"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
```


和binary crate的一样，我们也可以显式指定target：

```
[lib]
name = "my_library"
path = "src/lib.rs"
```


注意，这里是[lib]而不是[[lib]]，这是因为在一个carge package中最多只能存在一个library crate，但binary crate可以有多个。

接下来，我们就看看一个由多个binary crate和一个library crate混合构成的rust项目。

#### 4.3.1.3 多个Binary Crate和一个Library Crate

我们在organizing-rust-code/cargo/single-package/hybrid-crates下面执行如下命令创建这个多crates混合项目：

```
$cargo new my_project
Created binary (application) `my_project` package
```


上述命令默认创建了一个binary crate的project，我们需要配置一下Cargo.toml，将其改造为多个crates并存的project：

```
[package]
name = "my_project"
version = "0.1.0"
edition = "2021"
[[bin]]
name = "cmd1"
path = "src/main1.rs"
[[bin]]
name = "cmd2"
path = "src/main2.rs"
[lib]
name = "my_library"
path = "src/lib.rs"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
```


这里定义了三个crates。两个binary crates: cmd1、cmd2以及一个library crate：my_library。

如果我们执行cargo build，cargo会将三个crate都构建出来：

```
$cargo build
Compiling my_project v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/organizing-rust-code/cargo/single-package/hybrid-crates/my_project)
Finished dev [unoptimized + debuginfo] target(s) in 0.80s
```


我们可以在target/debug下找到构建出的crates：cmd1、cmd2和libmy_library.rlib：

```
$ls target/debug
build/ cmd1.d cmd2.d examples/ libmy_library.d
cmd1* cmd2* deps/ incremental/ libmy_library.rlib
```


我们也可以通过cargo分别运行两个binary crate：

```
$cargo run --bin cmd1
Finished dev [unoptimized + debuginfo] target(s) in 0.02s
Running `target/debug/cmd1`
cmd1
$cargo run --bin cmd2
Finished dev [unoptimized + debuginfo] target(s) in 0.00s
Running `target/debug/cmd2`
cmd2
```


#### 4.3.1.4 典型的cargo package

在The cargo book中，有一个典型的cargo package的示例：

```
.
├── Cargo.lock
├── Cargo.toml
├── src/
│ ├── lib.rs
│ ├── main.rs
│ └── bin/
│ ├── named-executable.rs
│ ├── another-executable.rs
│ └── multi-file-executable/
│ ├── main.rs
│ └── some_module.rs
├── benches/
│ ├── large-input.rs
│ └── multi-file-bench/
│ ├── main.rs
│ └── bench_module.rs
├── examples/
│ ├── simple.rs
│ └── multi-file-example/
│ ├── main.rs
│ └── ex_module.rs
└── tests/
├── some-integration-tests.rs
└── multi-file-test/
├── main.rs
└── test_module.rs
```


在这样一个典型的项目中：

- Cargo.toml和Cargo.lock文件存储在包的根目录（包根目录）中。
- 源代码位于src目录中。
- 默认的库文件是src/lib.rs。
- 默认的可执行文件是src/main.rs。
- 其他可执行文件可以放在src/bin/目录中。
- 基准测试位于benches目录中。
- 示例位于examples目录中。
- 集成测试位于tests目录中。

### 4.3.2 多package的rust项目

一些中大型的Rust项目都是多package的，比如rust的异步编程事实标准[tokio库](https://github.com/tokio-rs/tokio)、刚刚升级为Apache基金会顶级项目的[SQL查询引擎datafusion](https://github.com/apache/datafusion)等。以tokio为例，这些项目的顶层Cargo.toml都是这样的：

```
// https://github.com/tokio-rs/tokio/blob/master/Cargo.toml
[workspace]
resolver = "2"
members = [
"tokio",
"tokio-macros",
"tokio-test",
"tokio-stream",
"tokio-util",
# Internal
"benches",
"examples",
"stress-test",
"tests-build",
"tests-integration",
]
[workspace.metadata.spellcheck]
config = "spellcheck.toml"
```


上面这个Cargo.toml示例与我们在前面见到的Cargo.toml都不一样，它并不包含package配置，其主要的配置为workspace。我们看到workspace的members字段中配置了该项目下的其他package。正是通过这个配置，cargo可以在一个项目里管理和构建多个package。

[工作空间（Workspace）](https://doc.rust-lang.org/cargo/reference/workspaces.html)是一组一个或多个包（Package）的集合，这些包称为工作空间成员（Workspace Members），它们一起被管理。接下来，我们就来创建一个多package的cargo项目。

#### 4.3.2.1 cargo管理的多package项目

由于cargo并没有提供cargo new my-pakcage –workspace这样的命令行参数，项目的顶层Cargo.toml需要我们手动创建和编辑。

```
$cd organizing-rust-code/cargo/multi-packages
$mkdir my-workspace
$cd my-workspace
$cargo new package1 --bin
Created binary (application) `package1` package
$cargo new package2 --lib
Created library `package2` package
$cargo new package3 --lib
Created library `package3` package
```


接下来，我们手工创建和编辑一下项目顶层的Cargo.toml如下：

```
// organizing-rust-code/cargo/multi-packages/my-workspace/Cargo.toml
[workspace]
resolver = "2"
members = [
"package1",
"package2",
"package3",
]
```


保存后，我们可以在项目顶层目录下使用下面命令检查整个工作空间（workspace）中的所有包（package），确保它们的代码正确无误，不包含任何编译错误：

```
$cargo check --workspace
Checking package1 v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/organizing-rust-code/cargo/multi-packages/my-workspace/package1)
Checking package2 v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/organizing-rust-code/cargo/multi-packages/my-workspace/package2)
Checking package3 v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/organizing-rust-code/cargo/multi-packages/my-workspace/package3)
Finished dev [unoptimized + debuginfo] target(s) in 0.18s
```


在顶层目录执行cargo build，cargo会build工作空间中的所有package：

```
$cargo build
Compiling package3 v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/organizing-rust-code/cargo/multi-packages/my-workspace/package3)
Compiling package2 v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/organizing-rust-code/cargo/multi-packages/my-workspace/package2)
Compiling package1 v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/organizing-rust-code/cargo/multi-packages/my-workspace/package1)
Finished dev [unoptimized + debuginfo] target(s) in 0.64s
```


构建后，该项目的目录结构变成下面这个样子：

```
$tree -L 2 -F
.
├── Cargo.lock
├── Cargo.toml
├── package1/
│ ├── Cargo.toml
│ └── src/
├── package2/
│ ├── Cargo.toml
│ └── src/
├── package3/
│ ├── Cargo.toml
│ └── src/
└── target/
├── CACHEDIR.TAG
└── debug/
```


我们看到该项目下的所有package共享一个共同的 Cargo.lock 文件，该文件位于工作空间的根目录下。并且，所有包共享一个共同的输出目录，默认情况下是工作空间根目录下的一个名为target的目录，该target目录下的布局如下：

```
$tree -F -L 2 ./target
./target
├── CACHEDIR.TAG
└── debug/
├── build/
├── deps/
├── examples/
├── incremental/
├── libpackage2.d
├── libpackage2.rlib
├── libpackage3.d
├── libpackage3.rlib
├── package1*
└── package1.d
```


我们在这下面可以找到所有package的编译输出结果，比如package1、libpackage2.rlib以及libpackage3.rlib。

当然，你也可以指定一个package来构建或运行：

```
$cargo build -p package1
Finished dev [unoptimized + debuginfo] target(s) in 0.00s
$cargo build -p package2
Finished dev [unoptimized + debuginfo] target(s) in 0.00s
$cargo run -p package1
Finished dev [unoptimized + debuginfo] target(s) in 0.00s
Running `target/debug/package1`
Hello, world!
```


#### 4.3.2.2 带有外部依赖和内部依赖的多package项目

我们复制一份my-workspace，改名为my-workspace-with-deps，修改一下package1/src/main.rs，为其增加外部依赖rand crate：

```
// organizing-rust-code/cargo/multi-packages/my-workspace-with-deps/package1/src/main.rs
extern crate rand;
use rand::Rng;
fn main() {
let mut rng = rand::thread_rng();
let num: u32 = rng.gen();
println!("Random number: {}", num);
}
```


接下来，我们需要修改一下package1/Cargo.toml，手工加上对rand crate的依赖配置：

```
// organizing-rust-code/cargo/multi-packages/my-workspace-with-deps/package1/Cargo.toml
[package]
name = "package1"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
rand = "0.8.5"
```


保存后，我们执行package1的构建：

```
$cargo build -p package1
Downloaded getrandom v0.2.14 (registry `rsproxy`)
Downloaded libc v0.2.154 (registry `rsproxy`)
Downloaded 2 crates (780.6 KB) in 1m 07s
Compiling libc v0.2.154
Compiling cfg-if v1.0.0
Compiling ppv-lite86 v0.2.17
Compiling getrandom v0.2.14
Compiling rand_core v0.6.4
Compiling rand_chacha v0.3.1
Compiling rand v0.8.5
Compiling package1 v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/organizing-rust-code/cargo/multi-packages/my-workspace-with-deps/package1)
Finished dev [unoptimized + debuginfo] target(s) in 1m 46s
```


我们看到：cargo会自动下载package1的直接外部依赖以及相关间接依赖。构建成功后，可以执行一下package1的编译结果：

```
$cargo run -p package1
Finished dev [unoptimized + debuginfo] target(s) in 0.09s
Running `target/debug/package1`
Random number: 3840180495
```


接下来，我们再为package1添加内部依赖，比如依赖package2的编译结果：

```
// organizing-rust-code/cargo/multi-packages/my-workspace-with-deps/package1/src/main.rs
extern crate package2;
extern crate rand;
use rand::Rng;
fn main() {
let mut rng = rand::thread_rng();
let num: u32 = rng.gen();
println!("Random number: {}", num);
let result = package2::add(2, 2);
println!("result: {}", result);
}
// organizing-rust-code/cargo/multi-packages/my-workspace-with-deps/package1/Cargo.toml
[package]
name = "package1"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
rand = "0.8.5"
package2 = { path = "../package2" }
```


我们看到：package1的main.rs依赖package2这个crate中的add函数，我们在package1的Cargo.toml中为package1添加了新依赖package2，由于package2仅仅存放在本地，所以这里我们使用了path方式指定package2的位置。

我们执行一下添加内部依赖后的package1：

```
$cargo run -p package1
Finished dev [unoptimized + debuginfo] target(s) in 0.02s
Running `target/debug/package1`
Random number: 2485645524
result: 4
```


## 4.4 小结

本文循序渐进地讨论了在Rust项目中如何组织代码的问题，这对于Rust初学者来说尤为有用。

我们首先回顾了Go语言中的代码组织方式，介绍了Go项目代码组织的两个层级：module和package。然后，我们将Rust项目可以分为两种类型：使用rustc编译器的项目和使用Cargo的项目。

对于rustc-only的项目，开发者需要编写自己的构建脚本来管理项目的构建过程。

文章从最简单的单文件rustc-only项目开始介绍，展示了如何使用rustc编译器来编译和运行这种项目，并逐步介绍了带有外部依赖的rustc-only项目以及多文件项目的情况，引出了rust module概念。

rustc-only项目很少用于生产环境，这种方式主要用于学习和了解Rustc编译器的功能机制以及Rust语言的代码组织抽象。

在实际开发中，使用Cargo来创建和管理Rust包是常见的做法。在本章的后半段，我们介绍了使用cargo管理的rust项目的代码组织情况，包括单package项目和多package项目以及如何为项目引入外部和内部依赖。

总体而言，本文旨在帮助初学者理解和掌握Rust项目的代码组织结构，以提高学习效率和学习效果。通过介绍rustc-only项目和cargo管理的项目，读者可以逐步了解Rust代码组织的基本概念和实践方法。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/rust-guide-for-gopher/organizing-rust-code)下载。

## 4.5 参考资料

[The book](https://doc.rust-lang.org/book)– https://doc.rust-lang.org/book[The cargo book](https://doc.rust-lang.org/cargo/index.html)– https://doc.rust-lang.org/cargo/index.html[The rustc book](https://doc.rust-lang.org/rustc/index.html)– https://doc.rust-lang.org/rustc/index.html

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