---
title: Gopher的Rust第一课：建立Rust开发环境
url: https://tonybai.com/2024/05/10/gopher-rust-first-lesson-setup-dev-env/
published: '2024-05-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Gopher的Rust第一课：建立Rust开发环境

![](../../assets/b32d939c0786805a.png)


[本文永久链接](https://tonybai.com/2024/05/10/gopher-rust-first-lesson-setup-dev-env) – https://tonybai.com/2024/05/10/gopher-rust-first-lesson-setup-dev-env

经过上一章的对[Rust诞生演化的了解以及设计哲学的探讨](https://tonybai.com/2024/04/22/gopher-rust-first-lesson-all-about-rust/)后，如果你依然决定继续Rust编程学习之旅，那么欢迎你和我一起正式走进Rust学习和实践的课堂。

编程不是“纸上谈兵”，它是一门实践的艺术。编程语言的学习离不开动手实践，因此学习任何一门编程语言的第一步都是要拥有一个这门编程语言的开发环境，这样我们才可以动手编码，理论与实践结合，不仅加速学习效率，还能取得更好的学习效果。

在这一章中我们就先来学习下如何安装和配置Rust开发环境。如果你的机器上还没有Rust开发环境，那么就请跟我一起选择一种适合你的Rust安装方法吧。

第一步，我们先来挑一个合适的Rust版本。

## 2.1 选择Rust版本

### 2.1.1 Go与Rust发布版本与节奏的对比

在[《Go语言第一课专栏》](http://gk.link/a/10AVZ)讲解如何建立Go开发环境时，我首先讲解的也是选择Go版本。我们知道Go一年发布两次大版本，分别是每年的2月和8月，并且Go核心团队只对最近的两个大版本提供support。在处于support时间窗口中的时候，Go核心团队会发布一些补丁版本，修正及少量的严重问题或安全漏洞。比如[Go 1.22版本](https://tonybai.com/2024/02/18/some-changes-in-go-1-22/)是2024年2月份发布的，到2024年4月中旬，Go 1.22的最新补丁版本已经到了Go 1.22.2了。下图展示了Go版本发布的节奏以及support的窗口：

![](../../assets/1eded4c90c951c03.png)


在Go中，我们可以选择最新稳定版（比如图中的Go 1.22.2）和次新稳定版（比如图中的1.21.8），这两个是Go社区选择最多的。此外，也可以选择某个特定的稳定版（因某种特殊原因，被阻塞在该版本上）以及tip版，其中tip版（master分支上的最新commit版本）主要用于体验最新的、尚未发布的功能特性或问题修复，或是contributor多使用tip版。

Rust的版本发布节奏与Go完全不同，因此Rust版本的选择逻辑与Go相比也就有所不同。下图展示了Rust的版本发布方法与节奏：

![](../../assets/fd4010bf7123c7d8.png)


我们看到：Rust采用“6周一个稳定版”的滚动发布节奏，并且有三类版本：稳定版(stable)、公测版(beta)和nightly版，分别对应的是stable分支、beta分支和master分支。三个版本间是关联紧密的。

以图中的[rust 1.77.0的发布](https://blog.rust-lang.org/2024/03/21/Rust-1.77.0.html)为例，rust 1.77.0稳定版本的发布动作是这样的：

- 基于当前beta分支(其实就是1.77.0 beta)创建新的stable分支，并tag 1.77.0；
- 基于当前master分支(nightly版本)创建新的beta分支，并在新的beta分支上公测1.78.0版本，为六周后的1.78.0稳定版做准备；
- 而master分支上继续开发v1.79.0的新特性，并每天发布Nightly版本。

之后，原1.76.0稳定版便会从support窗口删除，1.77.0进入Support窗口。如果新发布的1.77.0有紧急或安全问题需要修复，则通过补丁(patch)版本进行，比如rust 1.77.1、1.77.2等。

Rust这种“稳定一版，公测一版，开发一版”的“三路并发”的滚动开发节奏，显然要比Go的“稳定一版，开发一版”的“两路并发”节奏要快上很多。不过，频繁的更新可能对某些用户来说是一个挑战，需要他们不断学习和适应新的变化。另外，较快的演进速度也可能导致一些不稳定因素，需要开发者更加谨慎地使用新功能特性。

### 2.1.2 Rust的三类版本

选择Rust版本根据自己的角色和面对的场合来进行：

- 对于大多数Rust开发者而言，最新的稳定版(stable)是最好和最明智的选择；
- 也有少部分因为各种特殊原因，可能阻塞在某个特定的稳定版上；
- Beta版contributor，或是想提前尝鲜下一个稳定版新特性的开发人员，可以临时使用beta版本；
- Nightly版，主要针对的也是contributor，或是想临时尝鲜最新不稳定功能特性的开发人员。

Rust提供的安装和升级工具[rustup](https://rustup.rs/)可以灵活的在三类版本间切换：

```
rustup default beta
rustup default nightly
rustup default stable
```


切换后，rustup会自动同步该类版本到最新版：

```
$rustup default beta
info: syncing channel updates for 'beta-x86_64-apple-darwin'
info: latest update on 2024-04-11, rust version 1.78.0-beta.6 (27011d5dc 2024-04-09)
... ...
```


确定了要使用的Rust版本后，我们接下来就来看看究竟如何安装Rust。

## 2.2 安装Rust

### 2.2.1 使用rustup安装

和Go尽可以通过安装包或下载预编译二进制包进行首次安装不同，Rust官方提供了统一的Rust安装、管理和升级工具- [rustup](https://rustup.rs)。 Rust官方在Linux和macOS上提供了“curl | sh”的一键式安装命令：

```
$curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```


我们以Linux下安装rustup为例，看一下执行上面命令的过程和最终结果：

```
$curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
info: downloading installer
Welcome to Rust!
This will download and install the official compiler for the Rust
programming language, and its package manager, Cargo.
Rustup metadata and toolchains will be installed into the Rustup
home directory, located at:
/root/.rustup
This can be modified with the RUSTUP_HOME environment variable.
The Cargo home directory is located at:
/root/.cargo
This can be modified with the CARGO_HOME environment variable.
The cargo, rustc, rustup and other commands will be added to
Cargo's bin directory, located at:
/root/.cargo/bin
This path will then be added to your PATH environment variable by
modifying the profile files located at:
/root/.profile
/root/.bashrc
You can uninstall at any time with rustup self uninstall and
these changes will be reverted.
Current installation options:
default host triple: x86_64-unknown-linux-gnu
default toolchain: stable (default)
profile: default
modify PATH variable: yes
1) Proceed with standard installation (default - just press enter)
2) Customize installation
3) Cancel installation
> // 敲击回车
info: profile set to 'default'
info: default host triple is x86_64-unknown-linux-gnu
info: syncing channel updates for 'stable-x86_64-unknown-linux-gnu'
info: latest update on 2024-04-09, rust version 1.77.2 (25ef9e3d8 2024-04-09)
info: downloading component 'cargo'
info: downloading component 'clippy'
info: downloading component 'rust-docs'
info: downloading component 'rust-std'
info: downloading component 'rustc'
info: downloading component 'rustfmt'
info: installing component 'cargo'
info: installing component 'clippy'
info: installing component 'rust-docs'
14.9 MiB / 14.9 MiB (100 %) 3.7 MiB/s in 3s ETA: 0s
info: installing component 'rust-std'
24.3 MiB / 24.3 MiB (100 %) 8.2 MiB/s in 2s ETA: 0s
info: installing component 'rustc'
60.3 MiB / 60.3 MiB (100 %) 9.6 MiB/s in 6s ETA: 0s
info: installing component 'rustfmt'
info: default toolchain set to 'stable-x86_64-unknown-linux-gnu'
stable-x86_64-unknown-linux-gnu installed - rustc 1.77.2 (25ef9e3d8 2024-04-09)
Rust is installed now. Great!
To get started you may need to restart your current shell.
This would reload your PATH environment variable to include
Cargo's bin directory ($HOME/.cargo/bin).
To configure your current shell, you need to source
the corresponding env file under $HOME/.cargo.
This is usually done by running one of the following (note the leading DOT):
. "$HOME/.cargo/env" # For sh/bash/zsh/ash/dash/pdksh
source "$HOME/.cargo/env.fish" # For fish
```


接下来按照提示执行下面命令，使得Rust相关的环境变量生效：

```
$. "$HOME/.cargo/env"
$which rustup
/root/.cargo/bin/rustup
```


. “$HOME/.cargo/env”这行代码也被追加到/root/.bashrc文件中，如果新启动一个terminal窗口，这行shell配置也会被执行，即rustup的环境变量也生效。

查看一下安装的rustup的版本：

```
$rustup -V
rustup 1.27.0 (bbb9276d2 2024-03-08)
info: This is the version for the rustup toolchain manager, not the rustc compiler.
info: The currently active `rustc` version is `rustc 1.77.2 (25ef9e3d8 2024-04-09)`
```


同时我们看到：首次安装rustup时，如果选择“standard installation”，rustup会为我们安装一个最新的Rust stable版本，这里是1.77.2，我们可以通过rustup show命令查看已安装的rust工具链：

```
$rustup show
Default host: x86_64-unknown-linux-gnu
rustup home: /root/.rustup
stable-x86_64-unknown-linux-gnu (default)
rustc 1.77.2 (25ef9e3d8 2024-04-09)
```


除此之外，rustup还在你的系统中都做了啥呢？我们下面来探索一下。

#### 2.2.1.1 安装后的探索

根据rustup在安装过程中的提示，有两个路径是需要重点关注的。

一个就是\$HOME/.cargo，rustup将.cargo/bin加入到了\$PATH变量下，我们来看看.cargo下都有哪些目录和文件：

```
$tree -F .cargo
.cargo
|-- bin/
| |-- cargo*
| |-- cargo-clippy*
| |-- cargo-fmt*
| |-- cargo-miri*
| |-- clippy-driver*
| |-- rls*
| |-- rust-analyzer*
| |-- rustc*
| |-- rustdoc*
| |-- rustfmt*
| |-- rust-gdb*
| |-- rust-gdbgui*
| |-- rust-lldb*
| `-- rustup*
`-- env
```


.cargo下主要的目录就是bin，这里存放了日常rust开发时在命令行使用的所有cli命令，包括cargo(构建管理工具)、rustc(编译器)、rustdoc、rustfmt以及rustup自身等。

另外一个更值得关注的目录就是\$HOME/.rustup目录，这个目录下的内容较多，我们通过tree命令查看的结果如下：

```
$tree -F -L 3 .rustup
.rustup
|-- downloads/
|-- settings.toml
|-- tmp/
|-- toolchains/
| `-- stable-x86_64-unknown-linux-gnu/
| |-- bin/
| |-- etc/
| |-- lib/
| |-- libexec/
| `-- share/
`-- update-hashes/
`-- stable-x86_64-unknown-linux-gnu
```


settings.toml是一个rustup配置文件，它的内容如下：

```
$cat .rustup/settings.toml
default_toolchain = "stable-x86_64-unknown-linux-gnu"
profile = "default"
version = "12"
[overrides]
```


这里的default_toolchain指示了当前默认使用的工具链版本为stable-x86_64-unknown-linux-gnu。这个版本也是一个target，Rust支持的不同平台上的target以及含义如下图：

![](../../assets/75e391a9cb10bb91.png)


.rustup下的另外一个值得注意的目录是toolchains，它下面存放了安装到本地的所有版本的toolchain，上面由于只安装了stable的最新版本，因此当前toolchains下只有一个stable-x86_64-unknown-linux-gnu目录。

值得注意的是.rustup中存储了rust工具链的所有内容，因此它的空间占用也着实可观：

```
$ du -sh .rustup
1.2G .rustup
```


现在我们来切换默认版本到beta：

```
$rustup default beta
info: syncing channel updates for 'beta-x86_64-unknown-linux-gnu'
info: latest update on 2024-04-11, rust version 1.78.0-beta.6 (27011d5dc 2024-04-09)
info: downloading component 'cargo'
info: downloading component 'clippy'
info: downloading component 'rust-docs'
info: downloading component 'rust-std'
info: downloading component 'rustc'
info: downloading component 'rustfmt'
info: installing component 'cargo'
info: installing component 'clippy'
info: installing component 'rust-docs'
15.1 MiB / 15.1 MiB (100 %) 3.4 MiB/s in 3s ETA: 0s
info: installing component 'rust-std'
24.2 MiB / 24.2 MiB (100 %) 9.3 MiB/s in 2s ETA: 0s
info: installing component 'rustc'
63.5 MiB / 63.5 MiB (100 %) 9.6 MiB/s in 6s ETA: 0s
info: installing component 'rustfmt'
info: default toolchain set to 'beta-x86_64-unknown-linux-gnu'
beta-x86_64-unknown-linux-gnu installed - rustc 1.78.0-beta.6 (27011d5dc 2024-04-09)
```


我们看到rustup会自动下载安装最新的beta版本，安装后，我们再执行rustc -V来查看当前版本，我们发现结果已经变为了下面这样：

```
$ rustc -V
rustc 1.78.0-beta.6 (27011d5dc 2024-04-09)
```


这里值得注意的是，虽然我们执行的rustc是.cargo/bin/rustc，但.cargo/bin/rustc有些类似于一个指针，真正执行的是其“指向”的某个工具链版本的rustc，我们可以使用rustup which rustc来查看究竟执行的是哪个rustc：

```
$ rustup which rustc
/root/.rustup/toolchains/beta-x86_64-unknown-linux-gnu/bin/rustc
```


此时，.rustup目录下面发生了怎样的变化呢？我们来看看：

```
$ tree -F -L 3 .rustup
.rustup
|-- downloads/
|-- settings.toml
|-- tmp/
|-- toolchains/
| |-- beta-x86_64-unknown-linux-gnu/
| | |-- bin/
| | |-- etc/
| | |-- lib/
| | |-- libexec/
| | `-- share/
| `-- stable-x86_64-unknown-linux-gnu/
| |-- bin/
| |-- etc/
| |-- lib/
| |-- libexec/
| `-- share/
`-- update-hashes/
|-- beta-x86_64-unknown-linux-gnu
`-- stable-x86_64-unknown-linux-gnu
```


我们看到toolchains下面多了一个beta-x86_64-unknown-linux-gnu目录，存放的就是刚刚安装的beta最新版本工具链。

现在我们在用rustup show命令查看已安装的rust工具链，其结果如下：

```
$rustup show
Default host: x86_64-unknown-linux-gnu
rustup home: /root/.rustup
installed toolchains
--------------------
stable-x86_64-unknown-linux-gnu
beta-x86_64-unknown-linux-gnu (default)
active toolchain
----------------
beta-x86_64-unknown-linux-gnu (default)
rustc 1.78.0-beta.6 (27011d5dc 2024-04-09)
```


现在，我们切换回stable版本，由于stable版本之前已经安装完毕，也就无需下载和安装过程了：

```
$rustup default stable
info: using existing install for 'stable-x86_64-unknown-linux-gnu'
info: default toolchain set to 'stable-x86_64-unknown-linux-gnu'
stable-x86_64-unknown-linux-gnu unchanged - rustc 1.77.2 (25ef9e3d8 2024-04-09)
```


#### 2.2.1.2 安装和使用特定版本rust工具链

我们还可以使用rustup安装特定版本的rust工具链，比如通过下面的命令，我们安装stable版本的1.66.0：

```
$ rustup install 1.66.0
info: syncing channel updates for '1.66.0-x86_64-unknown-linux-gnu'
info: latest update on 2022-12-15, rust version 1.66.0 (69f9c33d7 2022-12-12)
info: downloading component 'cargo'
info: downloading component 'clippy'
info: downloading component 'rust-docs'
info: downloading component 'rust-std'
info: downloading component 'rustc'
info: downloading component 'rustfmt'
info: installing component 'cargo'
info: installing component 'clippy'
info: installing component 'rust-docs'
19.0 MiB / 19.0 MiB (100 %) 4.4 MiB/s in 3s ETA: 0s
info: installing component 'rust-std'
29.7 MiB / 29.7 MiB (100 %) 8.1 MiB/s in 3s ETA: 0s
info: installing component 'rustc'
68.0 MiB / 68.0 MiB (100 %) 10.2 MiB/s in 6s ETA: 0s
info: installing component 'rustfmt'
1.66.0-x86_64-unknown-linux-gnu installed - rustc 1.66.0 (69f9c33d7 2022-12-12)
info: checking for self-update
```


安装ok后，我们再来看看.rustup目录下的变化：

```
$tree -F -L 3 .rustup
.rustup
|-- downloads/
|-- settings.toml
|-- tmp/
|-- toolchains/
| |-- 1.66.0-x86_64-unknown-linux-gnu/
| | |-- bin/
| | |-- etc/
| | |-- lib/
| | |-- libexec/
| | `-- share/
| |-- beta-x86_64-unknown-linux-gnu/
| | |-- bin/
| | |-- etc/
| | |-- lib/
| | |-- libexec/
| | `-- share/
| `-- stable-x86_64-unknown-linux-gnu/
| |-- bin/
| |-- etc/
| |-- lib/
| |-- libexec/
| `-- share/
`-- update-hashes/
|-- 1.66.0-x86_64-unknown-linux-gnu
|-- beta-x86_64-unknown-linux-gnu
`-- stable-x86_64-unknown-linux-gnu
```


我们看到toolchains下面多了一个1.66.0-x86_64-unknown-linux-gnu，那我们如何使用新下载的1.66.0 stable版本呢？有几种方法，下面逐一介绍一下。

我们可以使用rust工具链的“plus语法”在命令行上指定要使用的工具链，这个语法对cargo、rustc等工具链中的命令行程序都适用：

```
$ rustc +1.66.0 -V
rustc 1.66.0 (69f9c33d7 2022-12-12)
$ rustc +1.65.0 -V
error: toolchain '1.65.0-x86_64-unknown-linux-gnu' is not installed
$ cargo +1.66.0 -V
cargo 1.66.0 (d65d197ad 2022-11-15)
$ cargo +1.65.0 -V
error: toolchain '1.65.0-x86_64-unknown-linux-gnu' is not installed
```


注：

[cargo]是Rust语言的官方构建系统和包管理器，它提供了一组命令行工具，可以自动化构建、测试和发布Rust项目。它还支持自动解析和下载依赖项，使得管理项目的依赖关系变得简单和可靠。Cargo是Rust生态系统中重要的工具之一，为开发者提供了高效和方便的开发体验。在后面的章节中我会详细介绍cargo。

对于要使用特定版本进行构建的rust项目，我们可以通过rustup override来指定版本号。下面就是一个这样的例子：

```
$cargo new hellorust
Created binary (application) `hellorust` package
$cd hellorust/
$rustup override set 1.66.0
info: override toolchain for '/root/test/rust/hellorust' set to '1.66.0-x86_64-unknown-linux-gnu'
```


我们用cargo创建了一个新的hellorust项目，在hellorust项目下，我们执行rustup override来指定该项目使用1.66.0版本进行构建。

之后，我们分别在该项目目录下以及其他目录下执行rustc，我们看到输出结果如下：

```
~/test/rust/hellorust$ rustc -V
rustc 1.66.0 (69f9c33d7 2022-12-12)
$ cd ..
~/test/rust$ rustc -V
rustc 1.77.2 (25ef9e3d8 2024-04-09)
```


rustc override的原理其实是在$HOME/.rustup/settings.toml文件中添加了一些内容：

```
$cat .rustup/settings.toml
default_toolchain = "stable-x86_64-unknown-linux-gnu"
profile = "default"
version = "12"
[overrides]
"/root/test/rust/hellorust" = "1.66.0-x86_64-unknown-linux-gnu"
```


我们看到在overrides下新增了一条规则，指定了hellorust项目需要使用1.66.0-x86_64-unknown-linux-gnu这个工具链。

不过这种与本地路径紧耦合的配置方案并不是适合大范围协作，无法提交到git仓库中分享给其他人。

Rust还提供了另外一种override toolchain版本的方法，我们可以在hellorust项目的根目录下放置一个名为rust-toolchain.toml的文件，其内容如下：

```
// rust-toolchain.toml
[toolchain]
channel = "1.66.0"
```


我们先执行rustup override unset将上面设置的override规则取消掉:

```
$rustup override unset
info: override toolchain for '/root/test/rust/hellorust' removed
```


然后toolchain.toml就会生效了：

```
// 在hellorust路径下
$rustc -V
rustc 1.66.0 (69f9c33d7 2022-12-12)
```


显然，这里涉及到了override的优先级顺序问题。Rust规定版本override的优先级顺序由高到低依次是：

- plus语法：“rustc +1.66.0 -V”
- RUSTUP_TOOLCHAIN环境变量 (default: none)
- rustup override命令
- rust-toolchain.toml
- 默认toolchain

#### 2.2.1.3 在Windows上安装Rust

上述通过“curl|ssh”安装rustup，并通过rustup安装Rust工具链的方法是在Linux和macOS上安装Rust的主流方法，但在习惯于图形化安装的Windows上，略有变通。在Windows上，我们可以下载和安装一个名为[rustup-init.exe的程序](https://static.rust-lang.org/rustup/dist/i686-pc-windows-gnu/rustup-init.exe)，它等价于其他os上的rustup，但可以交互式的引导用户安装。

由于手旁没有Windows环境，具体的安装过程这里就不详细说明了。

### 2.2.2 离线安装包安装

和Go一样，Rust也提供了离线安装包的安装方式，在[离线安装包下载页面](https://forge.rust-lang.org/infra/other-installation-methods.html#standalone-installers)可以找到各个平台的多种文件格式（目前包括.tar.xz、.msi和.pkg）的离线安装包。

习惯在Windows上开发Rust程序的开发者可以直接下载和使用.msi来安装Rust开发环境。

## 2.3 更新和卸载Rust

使用rustup来更新和卸载Rust非常简单方便。

以更新stable版本为例，通过下面命令，我们就可以将本地的stable版本更新到最新stable版本。以我的macOS为例，我通过rustup将stable版本更新为最新的Rust 1.77.2：

```
$rustup update stable
info: syncing channel updates for 'stable-x86_64-apple-darwin'
info: latest update on 2024-04-09, rust version 1.77.2 (25ef9e3d8 2024-04-09)
info: downloading component 'cargo'
info: downloading component 'clippy'
info: downloading component 'rust-docs'
14.9 MiB / 14.9 MiB (100 %) 9.3 MiB/s in 1s ETA: 0s
info: downloading component 'rust-std'
25.4 MiB / 25.4 MiB (100 %) 764.8 KiB/s in 12s ETA: 0s
info: downloading component 'rustc'
54.9 MiB / 54.9 MiB (100 %) 8.6 MiB/s in 7s ETA: 0s
info: downloading component 'rustfmt'
1.8 MiB / 1.8 MiB (100 %) 564.9 KiB/s in 3s ETA: 0s
info: removing previous version of component 'cargo'
info: removing previous version of component 'clippy'
info: removing previous version of component 'rust-docs'
info: removing previous version of component 'rust-std'
info: removing previous version of component 'rustc'
info: removing previous version of component 'rustfmt'
info: installing component 'cargo'
info: installing component 'clippy'
info: installing component 'rust-docs'
14.9 MiB / 14.9 MiB (100 %) 4.2 MiB/s in 3s ETA: 0s
info: installing component 'rust-std'
25.4 MiB / 25.4 MiB (100 %) 13.8 MiB/s in 2s ETA: 0s
info: installing component 'rustc'
54.9 MiB / 54.9 MiB (100 %) 13.9 MiB/s in 4s ETA: 0s
info: installing component 'rustfmt'
stable-x86_64-apple-darwin updated - rustc 1.77.2 (25ef9e3d8 2024-04-09) (from rustc 1.75.0 (82e1608df 2023-12-21))
... ...
```


通过更新的日志，我们看到rust的相关工具组件（比如cargo、rustfmt等）也得到了一并的更新。

Rust通过rustup提供了卸载Rust环境的命令：

```
$rustup self uninstall
Thanks for hacking in Rust!
This will uninstall all Rust toolchains and data, and remove
$HOME/.cargo/bin from your PATH environment variable.
Continue? (y/N) _
```


我们看到：rustup会在控制台上与你进行一个确认继续的交互，确认你真的要卸载。如果你输入y并按Enter键继续，那么rustup会移除所有与Rust相关的文件，包括工具链、库、环境变量等。

如果你需要保留一些Rust版本，可以先运行rustup toolchain list，查看已安装的版本。然后用rustup toolchain uninstall命令单独卸载不需要的版本：

```
$rustup toolchain uninstall 1.64-x86_64-apple-darwin
info: uninstalling toolchain '1.64-x86_64-apple-darwin'
info: toolchain '1.64-x86_64-apple-darwin' uninstalled
```


## 2.4 配置Rust

在[《Go语言第一课专栏》](http://gk.link/a/10AVZ)讲解安装Go之后的配置时，我们主要提到了国内开发者要配置一个合适的GOPROXY。而Rust的各个站点都在合规访问范围内，我们安装Rust后无需做任何配置即可敞开使用Rust。

不过也有开发者觉得通过Rust官方下载crate慢，希望更换国内源，这种换源主要涉及的是cargo这个工具，我们后续学习Cargo时再来说明如何换源以及换哪个稳定的国内源。

## 2.5 在线体验Rust

[Go提供了在线的Go playground](https://go.dev/play/)可供尚未在本地安装Go环境的开发者体验Go语法，Go playground提供了三个版本：最新稳定版、次新稳定版以及tip版本，并且可以将代码通过短连接分享给其他开发者，十分方便。

这方面Rust也不逞多让，提供了功能足够丰富的[Rust Playground](https://play.rust-lang.org)：

![](../../assets/379ddda7aac18205.png)


在这里，我们可以选择Rust的版本：stable、beta还是nightly；可以选择编译模式，是debug还是release；可以选择Rust edition；可以选择执行一些工具，比如rustfmt；可以选择执行的命令：Run、Build、Test、MIR等。

不过，Rust、Go的playground毕竟只是用于在线体验的站点，他们具有共同的一些局限，比如：不支持第三方依赖，无法做复杂的多源文件项目的体验。

## 2.6 编辑器与IDE

对于开发人员来说，一门语言的开发环境不仅包含语言官方提供的编译器以及其他工具链，代码编辑器或IDE也是必不可少的。接下来，我们就来简单说说使用什么编辑器或IDE来开发Rust代码。

2023年Rust官方年度的用户调查显示，在编辑器/IDE使用排名中VSCode和VIM位列前二：

![](../../assets/6b67090ce49581a8.png)


Jetbrain推出的商业版[RustRover](https://www.jetbrains.com/rust/)位居第三，正在迎头赶上，但由于是商业版，这里就不详细介绍了。下面我们分别介绍一下如何使用VSCode和VIM来开发Rust代码，都需要安装哪些插件。

### 2.6.1 使用VSCode开发Rust

使用上面介绍的rustup在本地安装Rust环境后，rust的相关工具(cargo、rustc、rustfmt、[rust-analyzer](https://github.com/rust-lang/rust-analyzer)等)就都已经就绪！使用VSCode开发Rust只需再安装一个扩展插件即可，它就是由Rust官方维护的[rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)：

![](../../assets/3419df3d928a7965.png)


该插件实现了Rust语言的Language Server Protocol，可以在开发者编写Rust代码时，提供代码补全、转到定义/实现/类型定义、查找所有引用、工作区符号搜索、符号重命名、悬停时的类型和文档、类型和参数名称的嵌入提示、语义语法高亮等功能。可以说，有了Rust-analyzer的帮助，开发者可以自由在Rust代码中徜徉了。

更详细的VSCode支持Rust开发的文档，可以参考[Rust in Visual Studio Code](https://code.visualstudio.com/docs/languages/rust)。

### 2.6.2 使用VIM开发Rust

和VSCode仅需安装一个扩展插件相比，VIM的配置就相对复杂一些了。目前Rust+VIM的主流方案是**rust.vim + coc.nvim + coc-rust-analyzer**。

我们以安装了[vim-plug插件管理器](https://github.com/junegunn/vim-plug)的VIM为例，下面是VIM的插件关系以及插件与Rust工具链的交互图：

![](../../assets/3941d33219f8cb69.png)


首先，通过vim-plug安装coc.nvim和rust.vim，我们需要在~/.vimrc中添加下面代码：

```
call plug#begin()
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'rust-lang/rust.vim' "for rust
call plug#end()
```


然后在vim中执行:PlugInstall安装coc.nvim和rust.vim。

rust.vim是Rust团队官方维护的vim插件，用于提供Rust文件检测、语法高亮显示、代码格式化等，它需要Vim 8或更高版本才能实现完整功能。

[coc.nvim](https://github.com/neoclide/coc.nvim)则是一个强大的Neovim (Vim的衍生版本)插件，主要用于提供代码补全、语法检查、代码导航等功能，支持多种编程语言。它基于微软的 Language Server Protocol (LSP)，可以与各种语言服务器集成，从而为不同语言提供智能化的开发体验。

安装coc.nvim成功后，我们再在VIM中使用:CocInstall coc-rust-analyzer安装coc.nvim的插件：[coc-rust-analyzer](https://github.com/fannheyward/coc-rust-analyzer)，通过该插件可以实现与LSP实现rust-analyzer的交互，从而实现代码补全、转到定义/实现/类型定义、查找所有引用等功能。

此外，我们还需要配置一下coc.nvim，配置文件在~/.vim/coc-settings.json中：

```
{
"languageserver" : {
"rust": {
"command": "rust-analyzer",
"filetypes": ["rust"],
"rootPatterns": ["Cargo.toml"]
}
}
}
```


安装好上述插件并完成配置后，你同样可以使用VIM在Rust代码中徜徉！

## 2.7 小结

在这一章里，我们学习了如何建立Rust开发环境。

首先我了解到，Rust有stable(稳定版)、beta(公测版)和nightly(每晚版)三种版本渠道，发布节奏是每6周一个新的稳定版，与Go语言有所区别。对于大多数开发者来说，选择最新的稳定版是最明智的选择。

接着，我介绍了在Linux环境下使用rustup这个官方工具安装Rust的方法。rustup提供了一键安装命令，可以方便地安装不同渠道的Rust版本。

安装完成后，rustup在主机的主目录下创建了.cargo和.rustup两个目录。.cargo/bin存放了cargo、rustc等命令行工具，.rustup/toolchains则存放了安装的Rust工具链。

我们还学会了如何使用rustup在不同版本间切换，并演练了如何安装指定版本的Rust。另外，通过rustup的”plus语法”，可以在单个命令中临时使用特定的Rust版本。当然Rust提供了不止一种方法，还有rust-toolchain.toml文件、环境变量等方法，请注意这些方法的优先级顺序。

最后，我们还介绍了如何利用Rust playground在线体验Rust编码，以及Rust编码使用的两种最常使用的IDE和编辑器：VSCode和VIM，针对这两个工具，我分别介绍了Rust开发环境的配置方法。

相信大家通过本章内容，已经可以成功搭建了Rust开发环境了，这为后续的Rust编程学习打下了坚实的基础。

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