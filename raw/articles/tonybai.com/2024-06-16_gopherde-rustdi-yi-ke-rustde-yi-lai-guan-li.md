---
title: Gopher的Rust第一课：Rust的依赖管理
url: https://tonybai.com/2024/06/16/gopher-rust-first-lesson-managing-deps/
published: '2024-06-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Gopher的Rust第一课：Rust的依赖管理

![](../../assets/3f3bffd923fb5bde.png)


[本文永久链接](https://tonybai.com/2024/06/16/gopher-rust-first-lesson-managing-deps) – https://tonybai.com/2024/06/16/gopher-rust-first-lesson-managing-deps

在上一章《[Gopher的Rust第一课：Rust代码组织](https://tonybai.com/2024/06/06/gopher-rust-first-lesson-organizing-rust-code)》中，我们了解了Rust的代码组织形式，知道了基于Cargo构建项目以及Rust代码组织是目前的标准方式，同时Cargo也是管理项目外部依赖的标准方法，而项目内部的代码组织则由Rust module来完成。

在这一章中，我们将聚焦Rust的依赖管理，即Cargo对外部crate依赖的管理操作。我将先介绍几种依赖的来源类型（来自crates.io或其他Package Registries、来自某个git仓库以及来自本地的crate等），然后说说Cargo依赖的常见操作，包括依赖的添加、升降版本和删除；最后，聊一下如何处理依赖同一个依赖项的不同版本。

作为Gopher，我们先来简略回顾一下**Go的依赖管理要点**，大家可以在学习Cargo依赖管理后自己做个简单的对比，看看各自的优缺点是什么。

## 5.1 Go依赖管理回顾

从[Go 1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)开始，Go引入了[Go Modules](https://go.dev/ref/mod)以替代旧的GOPATH方式进行依赖管理。

我们可以使用go mod init命令初始化一个新的Go模块。go mod init会创建一个go.mod文件，该文件记录了当前项目的模块路径，并通过require directive记录了当前模块的依赖项以及版本：

```
require github.com/some/module v1.2.3
```


在开发过程中，我们也可以使用replace替换某个模块的路径，例如将依赖指向本地代码库进行调试：

```
replace example.com/some/module => ../local/module
```


或是通过replace将依赖指向某个特定版本的包。[Go 1.18](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)引入的[Go工作区模式](https://tonybai.com/2021/11/12/go-workspace-mode-in-go-1-18)让依赖本地包的动作更为便利丝滑。

Go Modules支持语义版本控制（semver），版本号格式为vX.Y.Z（其中X是major，Y为minor，Z为patch）。当发生不兼容变化时X编号需要+1。Go创新性地使用了语义版本导入机制，通过在包导入路径上使用vX来支持导入同一个包的不同major版本：

```
import (
"github.com/some/module"
v2 "github.com/some/module/v2"
)
```


无论是Go代码中引入新依赖，还是通过go mod edit命令手工修改依赖（升级、更新版本或降级版本），通过go mod tidy这个万能命令都可以**自动清理和整理依赖**。 go module还支持使用go.sum文件来记录每个依赖项的精确版本和校验和，确保依赖的完整性和安全性。go.sum文件应当提交到版本控制系统中。

此外，go mod vendor支持将依赖项副本存储在本地，这可以使你的项目在没有网络连接的情况下构建，并且可以避免依赖项版本冲突。

Go并没有采用像Rust、Js那样的中心module registry，而是采用了分布式go proxy来实现依赖发现与获取，默认的goproxy为proxy.golang.org，国内Gopher可以使用goproxy.cn、goproxy.io以及几个大厂提供的GOPROXY。

注：更多关于Go module依赖管理的系统且详细的内容，可以看看我在

[极客时间“Go语言第一课”专栏]中的两讲：[06｜构建模式：Go是怎么解决包依赖管理问题的？]和[07｜构建模式：Go Module的6类常规操作]。

接下来，我们正式进入Rust的依赖管理环节，我们先来看看Cargo依赖的来源。

## 5.2 Cargo依赖的来源

Rust的依赖管理系统中，Rust项目主要有以下几种依赖来源：

**来自crates.io的依赖**：这是Rust官方的crate registry，包含了大量开源的Rust库。**来自某个git仓库的依赖**：可以从任何git仓库添加依赖，特别是在开发阶段或使用未发布的版本时非常有用。**来自本地的crate依赖**：可以添加本地文件系统中的crate，便于在开发过程中引用本地代码。

接下来，我们就来逐一看看在一个Cargo项目中如何配置这三种不同来源的依赖。

### 5.2.1 来自crates.io的依赖

在Rust中，最常见的依赖来源是crates.io，这也是Rust官方维护的中心crate registry，我们可以通过cargo命令或手工修改Cargo.toml文件来添加这些依赖。我们用一个示例来说明一下如何为当前项目添加来自crates.io的依赖。

我们先用cargo创建一个名为hello_world的binary项目：

```
$cargo new hello_world --bin
Created binary (application) `hello_world` package
$cat Cargo.toml
[package]
name = "hello_world"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
//managing-deps/hello_world/src/main.rs
fn main() {
println!("Hello, world!");
}
```


构建该项目，这与我们在《[Gopher的Rust第一课：第一个Rust程序](https://tonybai.com/2024/05/27/gopher-rust-first-lesson-first-rust-program/)》一文中描述的别无二致：

```
$cargo build
Compiling hello_world v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/hello_world)
Finished dev [unoptimized + debuginfo] target(s) in 1.07s
$./target/debug/hello_world
Hello, world!
```


现在我们改造一下main.rs代码，添加点“实用”代码（改自serde的example）：

```
//managing-deps/hello_world/src/main.rs
use serde::{Deserialize, Serialize};
#[derive(Serialize, Deserialize, Debug)]
struct Point {
x: i32,
y: i32,
}
fn main() {
println!("Hello, world!");
let point = Point { x: 1, y: 2 };
// Convert the Point to a JSON string.
let serialized = serde_json::to_string(&point).unwrap();
// Prints serialized = {"x":1,"y":2}
println!("serialized = {}", serialized);
// Convert the JSON string back to a Point.
let deserialized: Point = serde_json::from_str(&serialized).unwrap();
// Prints deserialized = Point { x: 1, y: 2 }
println!("deserialized = {:?}", deserialized);
}
```


然后我们通过cargo check命令检查一下源码是否可以编译通过：

```
$cargo check
Checking hello_world v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/hello_world)
error[E0432]: unresolved import `serde`
--> src/main.rs:1:5
|
1 | use serde::{Deserialize, Serialize};
| ^^^^^ use of undeclared crate or module `serde`
error[E0433]: failed to resolve: use of undeclared crate or module `serde_json`
--> src/main.rs:14:22
|
14 | let serialized = serde_json::to_string(&point).unwrap();
| ^^^^^^^^^^ use of undeclared crate or module `serde_json`
error[E0433]: failed to resolve: use of undeclared crate or module `serde_json`
--> src/main.rs:20:31
|
20 | let deserialized: Point = serde_json::from_str(&serialized).unwrap();
| ^^^^^^^^^^ use of undeclared crate or module `serde_json`
Some errors have detailed explanations: E0432, E0433.
For more information about an error, try `rustc --explain E0432`.
error: could not compile `hello_world` (bin "hello_world") due to 3 previous errors
```


cargo check提示找不到serde、serde_json两个crate。并且，cargo check执行后，多出一个Cargo.lock文件。由于此时尚未在Cargo.toml中添加依赖（虽然代码中明确了对serde和serde_json的依赖），Cargo.lock中还没有依赖package的具体信息：

```
$cat Cargo.lock
# This file is automatically @generated by Cargo.
# It is not intended for manual editing.
version = 3
[[package]]
name = "hello_world"
version = "0.1.0"
```


Rust是否可以像go module那样通过go mod tidy自动扫描源码并在Cargo.toml中补全依赖信息呢？然而并没有。Rust添加依赖的操作还是需要手动完成。

我们的rust源码依赖serde和serde_json，接下来，我们就需要在Cargo.toml中手工添加serde、serde_json依赖，当然最标准的方法还是通过cargo add命令：

```
$cargo add serde serde_json
Adding serde v1.0.202 to dependencies.
Features:
+ std
- alloc
- derive
- rc
- serde_derive
- unstable
Adding serde_json v1.0.117 to dependencies.
Features:
+ std
- alloc
- arbitrary_precision
- float_roundtrip
- indexmap
- preserve_order
- raw_value
- unbounded_depth
```


我们查看一下cargo add执行后的Cargo.toml：

```
$cat Cargo.toml
[package]
name = "hello_world"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
serde = "1.0.202"
serde_json = "1.0.117"
```


我们看到在dependencies下新增了两个直接依赖信息：serde和serde_json以及它们的版本信息。

关于依赖版本，[Cargo定义了的兼容性规则](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html)如下：

针对在1.0版本之前的版本，比如0.x.y，[语义版本规范](https://semver.org/)认为是处于初始开发阶段，公共API是不稳定的，因此没有明确兼容性语义。但Cargo对待这样的版本的规则是：0.x.y与0.x.z是兼容的，如果x > 0且y >=z。比如：0.1.10是兼容0.1.1的。而在1.0版本之后，Cargo参考语义版本规范确定版本兼容性。

基于上述的兼容性规则，在Cargo.toml中指定依赖版本的形式与语义有如下几种情况：

```
some_crate = "1.2.3" => 版本范围[1.2.3, 2.0.0)。
some_crate = "1.2" => 版本范围[1.2.0, 2.0.0)。
some_crate = "1" => 版本范围[1.0.0, 2.0.0)。
some_crate = "0.2.3" => 版本范围[0.2.3, 0.3.0)。
some_crate = "0.2" => 版本范围[0.2.0, 0.3.0)。
some_crate = "0" => 版本范围[0.0.0, 1.0.0)。
some_crate = "0.0" => 版本范围[0.0.0, 0.1.0)。
some_crate = "0.0.3" => 版本范围[0.0.3, 0.0.4)。
some_crate = "^1.2.3" => 版本范围[1.2.3]。
some_crate = "~1.2.3" => 版本范围[1.2.3, 1.3.0)。
some_crate = "~1.2" => 版本范围[1.2.0, 1.3.0)。
some_crate = "~1" => 版本范围[1.0.0, 2.0.0)。
```


Cargo还支持一些带有通配符的版本需求形式：

```
some_crate = "*" => 版本范围[0.0.0, )。
some_crate = "1.*" => 版本范围[1.0.0, 2.0.0)。
some_crate = "1.2.*" => 版本范围[1.2.0, 1.3.0)。
```


如果要限制最高版本范围，可以用带有多版本的需求形式：

```
some_crate = ">=1.2, < 1.5" => 版本范围[1.2.0, 1.5.0)。
```


有了版本范围后，Cargo初始就会使用该范围内的当前最大版本号版本作为依赖的最终版本。比如some_crate = "1.2.3"，但当前some_crate的最高版本为1.3.5，那么Cargo会选择1.3.5的some_crate作为当前项目的依赖。

如果一个项目有两个依赖项同时依赖另外一个共同的依赖，比如(例子来自Cargo book)：

```
# Package A
[dependencies]
bitflags = "1.0"
# Package B
[dependencies]
bitflags = "1.1"
```


那么A依赖bitflags的范围在[1.0.0, 2.0.0)，B依赖bitflags的范围在[1.1.0, 2.0.0)，这样如果当前bitflags的最新版本为1.2.1，那么Cargo会选择1.2.1作为bitflags的最终版本。这点与Go的[最小版本选择(mvs)](https://research.swtch.com/vgo-mvs)是不一样的，在这个示例情况下，Go会选择bitflags的1.1.0版本，即满足A和B的bitflags的最小版本即可。

后续当依赖的版本有更新时，可以执行cargo update升级依赖的版本到一个兼容的、更高的版本(体现在Cargo.lock文件中依赖的版本更新)。

Cargo.lock是锁定Cargo最终采用的依赖的版本的描述文件，这个文件由cargo管理，不要手动修改，这时的Cargo.lock文件如下：

```
$cat Cargo.lock
# This file is automatically @generated by Cargo.
# It is not intended for manual editing.
version = 3
[[package]]
name = “hello_world”
version = “0.1.0″
dependencies = [
"serde",
"serde_json",
]
[[package]]
name = “itoa”
version = “1.0.11″
source = “registry+https://github.com/rust-lang/crates.io-index”
checksum = “49f1f14873335454500d59611f1cf4a4b0f786f9ac11f4312a78e4cf2566695b”
[[package]]
name = “proc-macro2″
version = “1.0.83″
source = “registry+https://github.com/rust-lang/crates.io-index”
checksum = “0b33eb56c327dec362a9e55b3ad14f9d2f0904fb5a5b03b513ab5465399e9f43″
dependencies = [
"unicode-ident",
]
[[package]]
name = “quote”
version = “1.0.36″
source = “registry+https://github.com/rust-lang/crates.io-index”
checksum = “0fa76aaf39101c457836aec0ce2316dbdc3ab723cdda1c6bd4e6ad4208acaca7″
dependencies = [
"proc-macro2",
]
[[package]]
name = “ryu”
version = “1.0.18″
source = “registry+https://github.com/rust-lang/crates.io-index”
checksum = “f3cb5ba0dc43242ce17de99c180e96db90b235b8a9fdc9543c96d2209116bd9f”
[[package]]
name = “serde”
version = “1.0.202″
source = “registry+https://github.com/rust-lang/crates.io-index”
checksum = “226b61a0d411b2ba5ff6d7f73a476ac4f8bb900373459cd00fab8512828ba395″
dependencies = [
"serde_derive",
]
[[package]]
name = “serde_derive”
version = “1.0.202″
source = “registry+https://github.com/rust-lang/crates.io-index”
checksum = “6048858004bcff69094cd972ed40a32500f153bd3be9f716b2eed2e8217c4838″
dependencies = [
"proc-macro2",
"quote",
"syn",
]
[[package]]
name = “serde_json”
version = “1.0.117″
source = “registry+https://github.com/rust-lang/crates.io-index”
checksum = “455182ea6142b14f93f4bc5320a2b31c1f266b66a4a5c858b013302a5d8cbfc3″
dependencies = [
"itoa",
"ryu",
"serde",
]
[[package]]
name = “syn”
version = “2.0.65″
source = “registry+https://github.com/rust-lang/crates.io-index”
checksum = “d2863d96a84c6439701d7a38f9de935ec562c8832cc55d1dde0f513b52fad106″
dependencies = [
"proc-macro2",
"quote",
"unicode-ident",
]
[[package]]
name = “unicode-ident”
version = “1.0.12″
source = “registry+https://github.com/rust-lang/crates.io-index”
checksum = “3354b9ac3fae1ff6755cb6db53683adb661634f67557942dea4facebec0fee4b”
```


和go.sum类似（但go.sum并不指示依赖项采用的具体版本), Cargo.lock中对于每个依赖项都包括名字、具体某个版本、来源与校验和。

我们再用cargo check一下该项目是否可以编译成功：

```
$cargo check
Compiling serde v1.0.202
Compiling serde_json v1.0.117
Checking ryu v1.0.18
Checking itoa v1.0.11
Checking hello_world v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/hello_world)
error: cannot find derive macro `Serialize` in this scope
--> src/main.rs:3:10
|
3 | #[derive(Serialize, Deserialize, Debug)]
| ^^^^^^^^^
|
note: `Serialize` is imported here, but it is only a trait, without a derive macro
--> src/main.rs:1:26
|
1 | use serde::{Deserialize, Serialize};
| ^^^^^^^^^
error: cannot find derive macro `Deserialize` in this scope
--> src/main.rs:3:21
|
3 | #[derive(Serialize, Deserialize, Debug)]
| ^^^^^^^^^^^
|
note: `Deserialize` is imported here, but it is only a trait, without a derive macro
--> src/main.rs:1:13
|
1 | use serde::{Deserialize, Serialize};
| ^^^^^^^^^^^
error[E0277]: the trait bound `Point: Serialize` is not satisfied
--> src/main.rs:14:44
|
14 | let serialized = serde_json::to_string(&point).unwrap();
| --------------------- ^^^^^^ the trait `Serialize` is not implemented for `Point`
| |
| required by a bound introduced by this call
|
= help: the following other types implement trait `Serialize`:
bool
char
isize
i8
i16
i32
i64
i128
and 131 others
note: required by a bound in `serde_json::to_string`
--> /Users/tonybai/.cargo/registry/src/rsproxy.cn-8f6827c7555bfaf8/serde_json-1.0.117/src/ser.rs:2209:17
|
2207 | pub fn to_string<T>(value: &T) -> Result<String>
| --------- required by a bound in this function
2208 | where
2209 | T: ?Sized + Serialize,
| ^^^^^^^^^ required by this bound in `to_string`
error[E0277]: the trait bound `Point: Deserialize<'_>` is not satisfied
--> src/main.rs:20:31
|
20 | let deserialized: Point = serde_json::from_str(&serialized).unwrap();
| ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ the trait `Deserialize<'_>` is not implemented for `Point`
|
= help: the following other types implement trait `Deserialize<'de>`:
bool
char
isize
i8
i16
i32
i64
i128
and 142 others
note: required by a bound in `serde_json::from_str`
--> /Users/tonybai/.cargo/registry/src/rsproxy.cn-8f6827c7555bfaf8/serde_json-1.0.117/src/de.rs:2676:8
|
2674 | pub fn from_str<'a, T>(s: &'a str) -> Result<T>
| -------- required by a bound in this function
2675 | where
2676 | T: de::Deserialize<'a>,
| ^^^^^^^^^^^^^^^^^^^ required by this bound in `from_str`
For more information about this error, try `rustc --explain E0277`.
error: could not compile `hello_world` (bin "hello_world") due to 4 previous errors
```


似乎是依赖包缺少某个feature。我们重新add一下serde依赖，这次带着必要的feature：

```
$cargo add serde --features derive,serde_derive
Adding serde v1.0.202 to dependencies.
Features:
+ derive
+ serde_derive
+ std
- alloc
- rc
- unstable
```


然后再执行check：

```
$cargo check
Compiling proc-macro2 v1.0.83
Compiling unicode-ident v1.0.12
Compiling serde v1.0.202
Compiling quote v1.0.36
Compiling syn v2.0.65
Compiling serde_derive v1.0.202
Checking serde_json v1.0.117
Checking hello_world v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/hello_world)
Finished dev [unoptimized + debuginfo] target(s) in 8.50s
```


我们看到，当开启serde的derive和serde_derive feature后，项目代码就可以正常编译和运行了，下面是运行结果：

```
$cargo run
Compiling itoa v1.0.11
Compiling ryu v1.0.18
Compiling serde v1.0.202
Compiling serde_json v1.0.117
Compiling hello_world v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/hello_world)
Finished dev [unoptimized + debuginfo] target(s) in 4.16s
Running `target/debug/hello_world`
Hello, world!
serialized = {"x":1,"y":2}
deserialized = Point { x: 1, y: 2 }
```


注：feature是cargo提供的一种条件编译和选项依赖的机制，有些类似于

[Go build constraints]，但表达能力和控制精细度要远超go build constraints，但其复杂度也远超go build constraints。在本章中，我们不对feature进行展开说明，更多关于feature的详细说明，请参见[cargo feature参考手册]。

除了官方的crates.io，Cargo还支持来自其他非官方的Registry的依赖，比如使用企业私有crate registry，这个不在本章内容范围内，后续会考虑用专题的形式说明。

考虑crates.io在海外，国内Rustaceans可以考虑[使用国内的crate源](https://doc.rust-lang.org/cargo/reference/source-replacement.html)，比如使用rsproxy源的配置如下：

```
// ~/.cargo/config
[source.crates-io]
replace-with = 'rsproxy'
[source.rsproxy]
registry = "https://rsproxy.cn/crates.io-index"
[source.rsproxy-sparse]
registry = "sparse+https://rsproxy.cn/index/"
[registries.rsproxy]
index = "https://rsproxy.cn/crates.io-index"
[net]
git-fetch-with-cli = true
```


git-fetch-with-cli = true表示使用本地git命令去获取registry index，否则使用内置的git库来获取。

### 5.2.2 来自git仓库的依赖

有时候，我们可能需要依赖一个尚未发布到crates.io上的库，这时可以通过git仓库来添加依赖。当然，这一方式也非常适合一些企业内的私有git仓库上的依赖。在Go中，如果没有一些额外的IT设置支持，便很难[拉取私有仓库上的go module](https://tonybai.com/2021/09/03/the-approach-to-go-get-private-go-module-in-house)。

下面我们使用下面命令将Cargo.toml中的serde依赖改为从git repo获取：

```
$cargo add serde --features derive,serde_derive --git https://github.com/serde-rs/serde.git
Updating git repository `https://github.com/serde-rs/serde.git`
Adding serde (git) to dependencies.
Features:
+ derive
+ serde_derive
+ std
- alloc
- rc
- unstable
```


更新后的Cargo.toml依赖列表变为了：

```
[dependencies]
serde = { git = "https://github.com/serde-rs/serde.git", version = "1.0.202", features = ["derive", "serde_derive"] }
serde_json = "1.0.117"
```


不过当我执行cargo check时报如下错误：

```
$cargo check
Updating git repository `https://github.com/serde-rs/serde.git`
remote: Enumerating objects: 28491, done.
remote: Counting objects: 100% (6879/6879), done.
remote: Compressing objects: 100% (763/763), done.
remote: Total 28491 (delta 6255), reused 6560 (delta 6111), pack-reused 21612
Receiving objects: 100% (28491/28491), 7.97 MiB | 205.00 KiB/s, done.
Resolving deltas: 100% (20065/20065), done.
From https://github.com/serde-rs/serde
* [new ref] -> origin/HEAD
* [new tag] v0.2.0 -> v0.2.0
* [new tag] v0.2.1 -> v0.2.1
* [new tag] v0.3.0 -> v0.3.0
* [new tag] v0.3.1 -> v0.3.1
... ...
* [new tag] v1.0.98 -> v1.0.98
* [new tag] v1.0.99 -> v1.0.99
Compiling serde v1.0.202
Compiling serde_derive v1.0.202 (https://github.com/serde-rs/serde.git#37618545)
Compiling serde v1.0.202 (https://github.com/serde-rs/serde.git#37618545)
Checking serde_json v1.0.117
Checking hello_world v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/hello_world)
error[E0277]: the trait bound `Point: serde::ser::Serialize` is not satisfied
--> src/main.rs:14:44
... ...
```


在serde的github issue中，[这个问题似乎已经修正](https://github.com/serde-rs/serde/issues/2526)，但在我的环境下不知何故依旧存在。

在使用git来源时，我们也可以指定一个特定的分支、tag或者commit：

```
[dependencies]
serde = { git = "https://github.com/serde-rs/serde.git", branch = "next" }
# 或者
serde = { git = "https://github.com/serde-rs/serde.git", tag = "v1.0.104" }
# 或者
serde = { git = "https://github.com/serde-rs/serde.git", rev = "a1b2c3d4" }
```


### 5.2.3 来自本地的crate依赖

在开发过程中，我们还可能需要引用本地文件系统中的crate。在Go中，我们可以使用go mod的replace或者Go workspace来解决该问题。在Rust中，我们也可以通过下面方式来添加本地依赖：

```
$cargo add serde --features derive,serde_derive --path ../serde/serde
Adding serde (local) to dependencies.
Features:
+ derive
+ serde_derive
+ std
- alloc
- rc
- unstable
// Cargo.toml
[dependencies]
serde = { version = "1.0.202", features = ["derive", "serde_derive"], path = "../serde/serde" }
```


不过，和来自git一样，基于来自本地的crate依赖，cargo check也报和基于git的crate依赖同样的错误。

## 5.3 Cargo依赖常见操作

下面简要说说依赖的常见操作，以来自crates.io的依赖为例。

### 5.3.1 添加依赖

正如上面示例中我们演示的那样，我们可以通过cargo add来添加一个依赖，或者可以通过手工编辑Cargo.toml文件添加对应的配置。例如，添加一个源自crates.io的新依赖rand库：

```
[dependencies]
rand = "0.8"
```


### 5.3.2 升降版本

要升级某个依赖到兼容的最新版本，可以使用cargo update；如果升级到不兼容版本，需要先修改Cargo.toml中的版本需求。例如，将rand库升级到2.x版本：

```
[dependencies]
rand = "2.0"
```


然后运行cargo update，Cargo会根据新的版本号需求进行重新解析依赖。

当然要降级依赖的版本到一个兼容的版本，通常可能需要在版本需求中使用类似“^x.y.z”来精确指定版本；如果要降级到一个不兼容版本，和升级到不兼容版本一样，需要先修改Cargo.toml中的版本需求，然后运行cargo update，Cargo会根据新的版本号需求进行重新解析依赖。

### 5.3.3 删除依赖

删除一个依赖则十分容易，只需从Cargo.toml中移除或注释掉对应的依赖配置， 然后运行cargo build，Cargo会更新项目的依赖关系。

## 5.4 处理依赖同一个依赖项的不同版本

在某些情况下，不同的crate可能依赖同一个crate的不同版本，这也是编程语言中典型的钻石依赖问题！是一个常见的依赖管理挑战。它发生在一个依赖项被两个或更多其他依赖项共享时。比如：app依赖A、B ，而A、B又同时依赖C。

在这样的情况下，前面我们提过Go给出的解决方案包含三点：

- 若A、B依赖的C的版本相同，那么选取这个相同的C版本即可；
- 若A、B依赖的C的版本不同但兼容（依照semver规范），那么选取C满足A、B依赖的最小版本，这叫做最小版本选择；
- 若A、B依赖的C的版本不同且不兼容，那么通过
[语义导入版本](https://research.swtch.com/vgo-import)，最终app将导入C的不同版本，这两个版本将在app中共存。

那么在Rust项目中，Cargo又是如何处理的呢？我们通过一个示例分别来看看这三种情况，我们创建一个app的示例：

```
// 在rust-guide-for-gopher/managing-deps目录下
$tree -F app
app
├── A/
│ ├── Cargo.toml
│ └── src/
│ └── lib.rs
├── B/
│ ├── Cargo.toml
│ └── src/
│ └── lib.rs
├── C/
│ ├── Cargo.lock
│ ├── Cargo.toml
│ └── src/
│ └── lib.rs
├── Cargo.lock
├── Cargo.toml
└── src/
└── main.rs
7 directories, 10 files
```


app是一个binary cargo project，它的Cargo.toml和src/main.rs内容如下：

```
// app/Cargo.toml
[package]
name = "app"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
A = { path = "./A", version = "0.1.0" }
B = { path = "./B", version = "0.1.0" }
// app/src/main.rs
fn main() {
println!("Hello, world!");
A::hello_from_a();
B::hello_from_b();
}
```


我们看到：app依赖crate A和B，并且分别调用了两个crate的公共函数。

接下来，我们再来看看A和B的情况，我们分场景说明。

### 5.4.1 依赖C的相同版本

当A和B依赖C的相同版本时，这个不难推断cargo最终会为A和B选择同一个依赖C的版本。比如：

```
$cat A/Cargo.toml
[package]
name = "A"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
C = { path = "../C", version = "1.0.0" }
$cat B/Cargo.toml
[package]
name = "B"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
C = { path = "../C", version = "1.0.0" }
$cat A/src/lib.rs
pub fn hello_from_a() {
println!("Hello from A begin");
C::hello_from_c();
println!("Hello from A end");
}
$cat B/src/lib.rs
pub fn hello_from_b() {
println!("Hello from B begin");
C::hello_from_c();
println!("Hello from B end");
}
$cat C/Cargo.toml
[package]
name = "C"
version = "1.3.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
$cat C/src/lib.rs
pub fn hello_from_c() {
println!("Hello from C 1.3.0");
}
```


在这里A和B对C的依赖都是version = "1.0.0"，通过前面的讲解我们知道，这等价于C的版本范围为[1.0.0, 2.0.0)。而C目前的版本为1.3.0，那么Cargo就会为A和B都选择1.3.0版本的C。我们运行一下这个app程序：

```
$cargo run
... ...
Hello, world!
Hello from A begin
Hello from C 1.3.0
Hello from A end
Hello from B begin
Hello from C 1.3.0
Hello from B end
```


我们还可以通过cargo tree命令验证一下对A和B对C版本的依赖：

```
$cargo tree --workspace --target all --all-features --invert C
C v1.3.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app/C)
├── A v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app/A)
│ └── app v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app)
└── B v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app/B)
└── app v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app)
```


我们看到A和B都依赖了C的v1.3.0版本。

### 5.4.2 依赖C的两个兼容版本

现在我们修改一下A和B对C的依赖版本需求：

```
$cat A/Cargo.toml
[package]
name = "A"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
C = { path = "../C", version = "1.1.1" }
$cat B/Cargo.toml
[package]
name = "B"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
C = { path = "../C", version = "1.2.3" }
```


让A对C的依赖需求为1.1.1，让B依赖需求为1.2.3，这回我们再来运行一下cargo run和cargo tree：

```
$cargo run
... ...
Hello, world!
Hello from A begin
Hello from C 1.3.0
Hello from A end
Hello from B begin
Hello from C 1.3.0
Hello from B end
$cargo tree --workspace --target all --all-features --invert C
C v1.3.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app/C)
├── A v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app/A)
│ └── app v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app)
└── B v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app/B)
└── app v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app)
```


由于1.1.1和1.2.3是兼容版本，因此Cargo选择了兼容这两个版本的C当前的最高版本1.3.0。

### 5.4.3 依赖C的两个不兼容版本

现在我们来试验一下当A和B依赖的C版本不兼容时，Cargo会为A和B选择C的什么版本！由于是本地环境，我们无法在一个目录下保存两个C版本，因此我们copy一份当前的C组件，将拷贝重命名为C-1.3.0，然后将C下面的Cargo.toml和src/lib.rs修改成下面的样子：

```
$cat C/Cargo.toml
[package]
name = "C"
version = "2.4.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
$cat C/src/lib.rs
pub fn hello_from_c() {
println!("Hello from C 2.4.0");
}
```


然后我们修改一下A和B的依赖，让他们分别依赖C-1.3.0和C：

```
$cat A/Cargo.toml
[package]
name = "A"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
C = { path = "../C-1.3.0", version = "1.1.1" }
$cat B/Cargo.toml
[package]
name = "B"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
C = { path = "../C", version = "2.2.3" }
```


我们再来运行一下该app：

```
$cargo run
... ...
Hello, world!
Hello from A begin
Hello from C 1.3.0
Hello from A end
Hello from B begin
Hello from C 2.4.0
Hello from B end
```


我们看到cargo为A选择的版本是C v1.3.0，而为B选择的C版本是C v2.4.0，也就是说C的两个不兼容版本在app中可以同时存在。

让我们再来用cargo tree查看一下对C的依赖关系：

```
$cargo tree --workspace --target all --all-features --invert C
error: There are multiple `C` packages in your project, and the specification `C` is ambiguous.
Please re-run this command with one of the following specifications:
C@1.3.0
C@2.4.0
```


我们看到，cargo tree提示我们两个版本不兼容，必须明确指明是要查看哪个C版本的依赖，那我们就分别按版本查看一下：

```
$cargo tree --workspace --target all --all-features --invert C@1.3.0
C v1.3.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app/C-1.3.0)
└── A v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app/A)
└── app v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app)
$cargo tree --workspace --target all --all-features --invert C@2.4.0
C v2.4.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app/C)
└── B v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app/B)
└── app v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/app)
```


### 5.4.4 直接依赖C的不同版本

在Go中我们可以通过语义导入版本实现在app中直接依赖同一个包的两个不兼容版本：

```
import (
"github.com/user/repo"
v2 "github.com/user/repo/v2"
)
```


在Rust中，是否也可以实现这一点？如果可以，又是如何实现的呢？答案是可以。至少我们可以通过使用Cargo的依赖别名功能来实现。我们建立一个名为dep_alias的示例，其目录结构如下：

```
$tree -F dep_alias
dep_alias
├── C/
│ ├── Cargo.lock
│ ├── Cargo.toml
│ └── src/
│ └── lib.rs
├── C-1.3.0/
│ ├── Cargo.lock
│ ├── Cargo.toml
│ └── src/
│ └── lib.rs
├── Cargo.lock
├── Cargo.toml
└── src/
└── main.rs
5 directories, 9 files
```


在这个示例中，app依赖C-1.3.0目录下的C 1.3.0版本以及C目录下的C 2.4.0版本，下面是app/Cargo.toml和app/src/main.rs的代码：

```
// rust-guide-for-gopher/managing-deps/dep_alias/Cargo.toml
$cat Cargo.toml
[package]
name = "app"
version = "0.1.0"
edition = "2021"
# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
[dependencies]
C_v1 = { path = "C-1.3.0", version = "1.0.0", package = "C" }
C_v2 = { path = "C", version = "2.3.0", package = "C" }
$cat src/main.rs
$cat src/main.rs
extern crate C_v1 as C_v1;
extern crate C_v2 as C_v2;
fn main() {
C_v1::hello_from_c();
C_v2::hello_from_c();
}
```


这里，我们为C的两个不兼容版本建立了两个别名：C_v1和C_v2，然后在代码中分别使用C_v1和C_v2，cargo会分别为C_v1和C_v2选择合适的版本，这里C_v1最终选择为1.3.0，而C_v2最终定为2.4.0：

```
$cargo run
Hello from C 1.3.0
Hello from C 2.4.0
```


由于包名依然是C，所以在使用cargo tree查看依赖关系时，依然要带上不同版本：

```
$cargo tree --workspace --target all --all-features --invert C@1.3.0
C v1.3.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/dep_alias/C-1.3.0)
└── app v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/dep_alias)
$cargo tree --workspace --target all --all-features --invert C@2.4.0
C v2.4.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/dep_alias/C)
└── app v0.1.0 (/Users/tonybai/Go/src/github.com/bigwhite/experiments/rust-guide-for-gopher/managing-deps/dep_alias)
```


## 5.5 小结

在这一章中，我们介绍了Rust中通过Cargo进行依赖管理的基本方法。

我们首先简要回顾了Go语言的依赖管理，特别是Go Modules的相关内容，如go.mod文件、版本控制机制等。

接着我们介绍了Rust中通过Cargo进行依赖管理的方法。Cargo依赖主要有三种来源：crates.io官方注册中心、Git仓库和本地文件系统。通过Cargo.toml文件和cargo命令，我们可以灵活添加、升级、降级或删除依赖项。文中还讲解了Cargo的版本兼容性规则和各种指定版本的语法。

针对依赖同一个库的不同版本的情况，我通过示例说明了Cargo的处理方式：如果版本相同或兼容，Cargo会选择满足要求的当前最高版本；如果版本不兼容，Cargo允许在项目中同时使用这些不兼容的版本，可以通过别名来区分使用。

总体来看，Cargo提供的依赖管理方式表达能力很强大，但相对于Go来说，还是复杂了很多，学习起来曲线要高很多，troubleshooting起来也不易，文中尚有一个遗留问题尚未解决，如果大家有解决方案或思路，可以在文章评论中告知我，感谢。

注：本文涉及的都是cargo依赖管理的基础内容，还有很多细节以及高级用法并未涉及。


本章中涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/rust-guide-for-gopher/managing-deps)下载。

## 5.6 参考资料

[Cargo Book: Specifying Dependencies](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html)- https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html[Cargo Book: Registries](https://doc.rust-lang.org/cargo/reference/registries.html)- https://doc.rust-lang.org/cargo/reference/registries.html

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) - https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 - https://github.com/bigwhite/gopherdaily

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论