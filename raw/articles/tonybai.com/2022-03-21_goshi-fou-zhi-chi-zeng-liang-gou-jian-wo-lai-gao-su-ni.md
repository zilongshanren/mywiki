---
title: Go是否支持增量构建？我来告诉你！
url: https://tonybai.com/2022/03/21/go-native-support-incremental-build/
published: '2022-03-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go是否支持增量构建？我来告诉你！

![](../../assets/c456bcf042a85c3c.png)


[本文永久链接](https://tonybai.com/2022/03/21/go-native-support-incremental-build) – https://tonybai.com/2022/03/21/go-native-support-incremental-build

Go语言**以编译速度快闻名于码农界**。这缘于Go在设计之初就选择抛弃其祖辈C语言的头文件包含机制，选择了以包(package)作为基本编译单元。Go语言的这种以包为基本构建单元的构建模型使得依赖分析变得十分简单，避免了C语言那种通过头文件分析依赖的巨大开销。在我的[《Go语言精进之路》](https://mp.weixin.qq.com/s/h-lsWUbKRPnzFLINub5uYw)一书中，我也给出了Go编译速度快的三点具体原因，包括：

- Go要求每个源文件在开头处显式地列出所有依赖的包导入，这样Go编译器不必读取和处理整个文件就可以确定其依赖的包列表；
- Go要求包之间不能存在循环依赖，这样一个包的依赖关系便形成了一张有向无环图。由于无环，包可以被单独编译，也可以并行编译；
- 已编译的Go包对应的目标文件(file_name.o或package_name.a)中不仅记录了该包本身的导出符号信息，还记录了其所依赖包的导出符号信息。这样，Go编译器在编译某包P时，针对P依赖的每个包导入(比如：导入包Q)，只需读取一个目标文件即可（比如：Q包编译成的目标文件，该目标文件中已经包含了Q包的依赖包的导出信息），而无需再读取其他文件中的信息了。

不过近期有读者问到：**Go是否支持增量构建(incremental build)**？这是一个好问题，书中并未提到这方面内容。但语言编译器编译速度再快，如果没有增量构建，构建大型代码工程的时间也不会短。那么Go是否支持增量构建呢？在这篇文章中，我就来告诉你答案。

### 1. 什么是增量构建？

提到构建(build)，我们通常所指的是静态编译型语言，比如：C、Go、Java等。Python等动态语言不需要构建，直接用解释器run即可。每种静态编译型编程语言通常都有自己的编译单元，比如Go的编译单元为一个package，c/c++的编译单元是一个c/c++源文件，java则以class为编译单元等。**静态语言的构建就是将编译单元的源码编译为对应的中间目标文件(.o/.a/.class)，然后将这些目标文件通过链接器链接在一起形成最终可执行文件的过程**。不过Java除外，java在编译过程没有链接环节，jvm加载class文件时会有一个链接过程。

那么问题来了：每次项目构建，项目中的所有源文件都要被重新编译一遍而形成新的中间目标文件吗？如果我只改动了一个源文件中的几行代码，项目中的其他源文件也要跟着重新编译一遍么？我们显然不希望这样浪费算力、浪费开发者时间的事情发生！

为了避免这样的事情发生，“增量构建”被提了出来。简单来说就是**每次构建仅重新编译变动了的编译单元以及对这些变动的编译单元有依赖的编译单元的源码**！

![](../../assets/4295a6232b8e9db1.png)


上图展示了一个项目的编译单元的依赖关系。当开发人员修改了编译单元C的源码后，如果该项目支持增量编译，那么再次构建这个项目时，仅变动的编译单元C的源码以及直接依赖C的B、间接依赖C的A会被重新编译，而D、E两个编译单元不会被重新编译，其中间目标文件会被链接器重用。

对增量编译的支持，有两种策略：一种是编程语言的编译器自身就支持，比如Rust。另外一种则是语言自身编译器不支持，需要通过第三方项目构建管理工具协助实现，最典型的就是C/C++与Make/CMake的组合。

那么Go语言的编译器go compiler(gc)是否本身就支持增量编译呢？是否需要通过外部项目构建管理工具协助呢？我们继续往下看。

### 2. 通过示例看Go是否支持增量构建

Go语言提供了统一的go工具链，在这个工具链中用于构建的命令只有一个，那就是go build。下面我们就通过一系列实例来验证一下Go是否原生支持增量构建。

该示例的项目结构如下：

```
demo1/
├── go.mod
├── main.go
├── pkg1/
│ └── pkg1.go
└── pkg2/
└── pkg2.go
```


#### a) 首次构建

在这个项目中，顶层的module为demo1，main包依赖pkg1包与pkg2包。我们先通过go build命令对该项目做首次构建，我们通过命令行参数-x -v输出构建的详细日志，以便于我们分析：

```
$go build -x -v
### 笔者注：创建临时目录用于此次构建
WORK=/var/folders/cz/sbj5kg2d3m3c6j650z0qfm800000gn/T/go-build1907281507
cd /Users/tonybai/test/go
git status --porcelain
cd /Users/tonybai/test/go
git show -s --no-show-signature --format=%H:%ct
demo1/pkg2
demo1/pkg1
mkdir -p $WORK/b003/
mkdir -p $WORK/b002/
cat >$WORK/b003/importcfg << 'EOF' # internal
# import config
EOF
### 笔者注：编译demo1/pkg1和demo1/pkg2包
cd /Users/tonybai/test/go/incremental-build/demo1
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b003/_pkg_.a -trimpath "$WORK/b003=>" -p demo1/pkg2 -lang=go1.18 -complete -buildid 4ixic55Fpug9OyS7vsew/4ixic55Fpug9OyS7vsew -goversion go1.18rc1 -c=4 -nolocalimports -importcfg $WORK/b003/importcfg -pack ./pkg2/pkg2.go
cat >$WORK/b002/importcfg << 'EOF' # internal
# import config
EOF
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b002/_pkg_.a -trimpath "$WORK/b002=>" -p demo1/pkg1 -lang=go1.18 -complete -buildid jgyT36iBuu6-dYIzK5SD/jgyT36iBuu6-dYIzK5SD -goversion go1.18rc1 -c=4 -nolocalimports -importcfg $WORK/b002/importcfg -pack ./pkg1/pkg1.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b003/_pkg_.a # internal
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b002/_pkg_.a # internal
### 笔者注：将编译demo1/pkg1和demo1/pkg2包得到的目标文件缓存到gocache中
cp $WORK/b003/_pkg_.a /Users/tonybai/Library/Caches/go-build/fe/fef7890aa0cf3bb97e872d2b49cd834a5fad87cd5d8bf052dca65e4cecb541d2-d # internal
cp $WORK/b002/_pkg_.a /Users/tonybai/Library/Caches/go-build/24/24519941f74b316c8e83f2d2462b62370692c5f56b04ec3df97e3124ff8b4633-d # internal
runtime
mkdir -p $WORK/b004/
cat >$WORK/b004/go_asm.h << 'EOF' # internal
EOF
cd /Users/tonybai/.bin/go1.18rc1/src/runtime
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/asm -p runtime -trimpath "$WORK/b004=>" -I $WORK/b004/ -I /Users/tonybai/.bin/go1.18rc1/pkg/include -D GOOS_darwin -D GOARCH_amd64 -compiling-runtime -D GOAMD64_v1 -gensymabis -o $WORK/b004/symabis ./asm.s ./asm_amd64.s ./duff_amd64.s ./memclr_amd64.s ./memmove_amd64.s ./preempt_amd64.s ./rt0_darwin_amd64.s ./sys_darwin_amd64.s
cat >$WORK/b004/importcfg << 'EOF' # internal
# import config
packagefile internal/abi=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/abi.a
packagefile internal/bytealg=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/bytealg.a
packagefile internal/cpu=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/cpu.a
packagefile internal/goarch=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goarch.a
packagefile internal/goexperiment=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goexperiment.a
packagefile internal/goos=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goos.a
packagefile runtime/internal/atomic=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/atomic.a
packagefile runtime/internal/math=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/math.a
packagefile runtime/internal/sys=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/sys.a
EOF
### 笔者注：由于笔者在执行build前使用go clean -cache将所有cache清空，因此这里go build会重新编译Go运行时库并缓存到gocache中
cd /Users/tonybai/test/go/incremental-build/demo1
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b004/_pkg_.a -trimpath "$WORK/b004=>" -p runtime -std -+ -buildid cjuCOFTfsWmpOEnkAPsP/cjuCOFTfsWmpOEnkAPsP -goversion go1.18rc1 -symabis $WORK/b004/symabis -c=4 -nolocalimports -importcfg $WORK/b004/importcfg -pack -asmhdr $WORK/b004/go_asm.h /Users/tonybai/.bin/go1.18rc1/src/runtime/alg.go /Users/tonybai/.bin/go1.18rc1/src/runtime/asan0.go /Users/tonybai/.bin/go1.18rc1/src/runtime/atomic_pointer.go /Users/tonybai/.bin/go1.18rc1/src/runtime/cgo.go /Users/tonybai/.bin/go1.18rc1/src/runtime/cgocall.go /Users/tonybai/.bin/go1.18rc1/src/runtime/cgocallback.go /Users/tonybai/.bin/go1.18rc1/src/runtime/cgocheck.go /Users/tonybai/.bin/go1.18rc1/src/runtime/chan.go /Users/tonybai/.bin/go1.18rc1/src/runtime/checkptr.go /Users/tonybai/.bin/go1.18rc1/src/runtime/compiler.go /Users/tonybai/.bin/go1.18rc1/src/runtime/complex.go /Users/tonybai/.bin/go1.18rc1/src/runtime/cpuflags.go /Users/tonybai/.bin/go1.18rc1/src/runtime/cpuflags_amd64.go /Users/tonybai/.bin/go1.18rc1/src/runtime/cpuprof.go /Users/tonybai/.bin/go1.18rc1/src/runtime/cputicks.go /Users/tonybai/.bin/go1.18rc1/src/runtime/debug.go /Users/tonybai/.bin/go1.18rc1/src/runtime/debugcall.go /Users/tonybai/.bin/go1.18rc1/src/runtime/debuglog.go /Users/tonybai/.bin/go1.18rc1/src/runtime/debuglog_off.go /Users/tonybai/.bin/go1.18rc1/src/runtime/defs_darwin_amd64.go /Users/tonybai/.bin/go1.18rc1/src/runtime/env_posix.go /Users/tonybai/.bin/go1.18rc1/src/runtime/error.go /Users/tonybai/.bin/go1.18rc1/src/runtime/extern.go /Users/tonybai/.bin/go1.18rc1/src/runtime/fastlog2.go /Users/tonybai/.bin/go1.18rc1/src/runtime/fastlog2table.go /Users/tonybai/.bin/go1.18rc1/src/runtime/float.go /Users/tonybai/.bin/go1.18rc1/src/runtime/hash64.go /Users/tonybai/.bin/go1.18rc1/src/runtime/heapdump.go /Users/tonybai/.bin/go1.18rc1/src/runtime/histogram.go /Users/tonybai/.bin/go1.18rc1/src/runtime/iface.go /Users/tonybai/.bin/go1.18rc1/src/runtime/lfstack.go /Users/tonybai/.bin/go1.18rc1/src/runtime/lfstack_64bit.go /Users/tonybai/.bin/go1.18rc1/src/runtime/lock_sema.go /Users/tonybai/.bin/go1.18rc1/src/runtime/lockrank.go /Users/tonybai/.bin/go1.18rc1/src/runtime/lockrank_off.go /Users/tonybai/.bin/go1.18rc1/src/runtime/malloc.go /Users/tonybai/.bin/go1.18rc1/src/runtime/map.go /Users/tonybai/.bin/go1.18rc1/src/runtime/map_fast32.go /Users/tonybai/.bin/go1.18rc1/src/runtime/map_fast64.go /Users/tonybai/.bin/go1.18rc1/src/runtime/map_faststr.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mbarrier.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mbitmap.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mcache.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mcentral.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mcheckmark.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mem_darwin.go /Users/tonybai/.bin/go1.18rc1/src/runtime/metrics.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mfinal.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mfixalloc.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mgc.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mgcmark.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mgcpacer.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mgcscavenge.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mgcstack.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mgcsweep.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mgcwork.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mheap.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mpagealloc.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mpagealloc_64bit.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mpagecache.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mpallocbits.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mprof.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mranges.go /Users/tonybai/.bin/go1.18rc1/src/runtime/msan0.go /Users/tonybai/.bin/go1.18rc1/src/runtime/msize.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mspanset.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mstats.go /Users/tonybai/.bin/go1.18rc1/src/runtime/mwbbuf.go /Users/tonybai/.bin/go1.18rc1/src/runtime/nbpipe_pipe.go /Users/tonybai/.bin/go1.18rc1/src/runtime/netpoll.go /Users/tonybai/.bin/go1.18rc1/src/runtime/netpoll_kqueue.go /Users/tonybai/.bin/go1.18rc1/src/runtime/os_darwin.go /Users/tonybai/.bin/go1.18rc1/src/runtime/os_nonopenbsd.go /Users/tonybai/.bin/go1.18rc1/src/runtime/panic.go /Users/tonybai/.bin/go1.18rc1/src/runtime/plugin.go /Users/tonybai/.bin/go1.18rc1/src/runtime/preempt.go /Users/tonybai/.bin/go1.18rc1/src/runtime/preempt_nonwindows.go /Users/tonybai/.bin/go1.18rc1/src/runtime/print.go /Users/tonybai/.bin/go1.18rc1/src/runtime/proc.go /Users/tonybai/.bin/go1.18rc1/src/runtime/profbuf.go /Users/tonybai/.bin/go1.18rc1/src/runtime/proflabel.go /Users/tonybai/.bin/go1.18rc1/src/runtime/race0.go /Users/tonybai/.bin/go1.18rc1/src/runtime/rdebug.go /Users/tonybai/.bin/go1.18rc1/src/runtime/relax_stub.go /Users/tonybai/.bin/go1.18rc1/src/runtime/runtime.go /Users/tonybai/.bin/go1.18rc1/src/runtime/runtime1.go /Users/tonybai/.bin/go1.18rc1/src/runtime/runtime2.go /Users/tonybai/.bin/go1.18rc1/src/runtime/rwmutex.go /Users/tonybai/.bin/go1.18rc1/src/runtime/select.go /Users/tonybai/.bin/go1.18rc1/src/runtime/sema.go /Users/tonybai/.bin/go1.18rc1/src/runtime/signal_amd64.go /Users/tonybai/.bin/go1.18rc1/src/runtime/signal_darwin.go /Users/tonybai/.bin/go1.18rc1/src/runtime/signal_darwin_amd64.go /Users/tonybai/.bin/go1.18rc1/src/runtime/signal_unix.go /Users/tonybai/.bin/go1.18rc1/src/runtime/sigqueue.go /Users/tonybai/.bin/go1.18rc1/src/runtime/sizeclasses.go /Users/tonybai/.bin/go1.18rc1/src/runtime/slice.go /Users/tonybai/.bin/go1.18rc1/src/runtime/softfloat64.go /Users/tonybai/.bin/go1.18rc1/src/runtime/stack.go /Users/tonybai/.bin/go1.18rc1/src/runtime/string.go /Users/tonybai/.bin/go1.18rc1/src/runtime/stubs.go /Users/tonybai/.bin/go1.18rc1/src/runtime/stubs_amd64.go /Users/tonybai/.bin/go1.18rc1/src/runtime/stubs_nonlinux.go /Users/tonybai/.bin/go1.18rc1/src/runtime/symtab.go /Users/tonybai/.bin/go1.18rc1/src/runtime/sys_darwin.go /Users/tonybai/.bin/go1.18rc1/src/runtime/sys_libc.go /Users/tonybai/.bin/go1.18rc1/src/runtime/sys_nonppc64x.go /Users/tonybai/.bin/go1.18rc1/src/runtime/sys_x86.go /Users/tonybai/.bin/go1.18rc1/src/runtime/time.go /Users/tonybai/.bin/go1.18rc1/src/runtime/time_nofake.go /Users/tonybai/.bin/go1.18rc1/src/runtime/timestub.go /Users/tonybai/.bin/go1.18rc1/src/runtime/tls_stub.go /Users/tonybai/.bin/go1.18rc1/src/runtime/trace.go /Users/tonybai/.bin/go1.18rc1/src/runtime/traceback.go /Users/tonybai/.bin/go1.18rc1/src/runtime/type.go /Users/tonybai/.bin/go1.18rc1/src/runtime/typekind.go /Users/tonybai/.bin/go1.18rc1/src/runtime/utf8.go /Users/tonybai/.bin/go1.18rc1/src/runtime/vdso_in_none.go /Users/tonybai/.bin/go1.18rc1/src/runtime/write_err.go
cd /Users/tonybai/.bin/go1.18rc1/src/runtime
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/asm -p runtime -trimpath "$WORK/b004=>" -I $WORK/b004/ -I /Users/tonybai/.bin/go1.18rc1/pkg/include -D GOOS_darwin -D GOARCH_amd64 -compiling-runtime -D GOAMD64_v1 -o $WORK/b004/asm.o ./asm.s
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/asm -p runtime -trimpath "$WORK/b004=>" -I $WORK/b004/ -I /Users/tonybai/.bin/go1.18rc1/pkg/include -D GOOS_darwin -D GOARCH_amd64 -compiling-runtime -D GOAMD64_v1 -o $WORK/b004/asm_amd64.o ./asm_amd64.s
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/asm -p runtime -trimpath "$WORK/b004=>" -I $WORK/b004/ -I /Users/tonybai/.bin/go1.18rc1/pkg/include -D GOOS_darwin -D GOARCH_amd64 -compiling-runtime -D GOAMD64_v1 -o $WORK/b004/duff_amd64.o ./duff_amd64.s
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/asm -p runtime -trimpath "$WORK/b004=>" -I $WORK/b004/ -I /Users/tonybai/.bin/go1.18rc1/pkg/include -D GOOS_darwin -D GOARCH_amd64 -compiling-runtime -D GOAMD64_v1 -o $WORK/b004/memclr_amd64.o ./memclr_amd64.s
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/asm -p runtime -trimpath "$WORK/b004=>" -I $WORK/b004/ -I /Users/tonybai/.bin/go1.18rc1/pkg/include -D GOOS_darwin -D GOARCH_amd64 -compiling-runtime -D GOAMD64_v1 -o $WORK/b004/memmove_amd64.o ./memmove_amd64.s
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/asm -p runtime -trimpath "$WORK/b004=>" -I $WORK/b004/ -I /Users/tonybai/.bin/go1.18rc1/pkg/include -D GOOS_darwin -D GOARCH_amd64 -compiling-runtime -D GOAMD64_v1 -o $WORK/b004/preempt_amd64.o ./preempt_amd64.s
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/asm -p runtime -trimpath "$WORK/b004=>" -I $WORK/b004/ -I /Users/tonybai/.bin/go1.18rc1/pkg/include -D GOOS_darwin -D GOARCH_amd64 -compiling-runtime -D GOAMD64_v1 -o $WORK/b004/rt0_darwin_amd64.o ./rt0_darwin_amd64.s
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/asm -p runtime -trimpath "$WORK/b004=>" -I $WORK/b004/ -I /Users/tonybai/.bin/go1.18rc1/pkg/include -D GOOS_darwin -D GOARCH_amd64 -compiling-runtime -D GOAMD64_v1 -o $WORK/b004/sys_darwin_amd64.o ./sys_darwin_amd64.s
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/pack r $WORK/b004/_pkg_.a $WORK/b004/asm.o $WORK/b004/asm_amd64.o $WORK/b004/duff_amd64.o $WORK/b004/memclr_amd64.o $WORK/b004/memmove_amd64.o $WORK/b004/preempt_amd64.o $WORK/b004/rt0_darwin_amd64.o $WORK/b004/sys_darwin_amd64.o # internal
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b004/_pkg_.a # internal
cp $WORK/b004/_pkg_.a /Users/tonybai/Library/Caches/go-build/0e/0e28018e12d646c32443e88953b839c7ba0be3198e6a61afc8a74c0b3e76696a-d # internal
demo1
mkdir -p $WORK/b001/
cat >$WORK/b001/importcfg << 'EOF' # internal
# import config
packagefile demo1/pkg1=$WORK/b002/_pkg_.a
packagefile demo1/pkg2=$WORK/b003/_pkg_.a
packagefile runtime=$WORK/b004/_pkg_.a
EOF
### 笔者注：编译main包并缓存
cd /Users/tonybai/test/go/incremental-build/demo1
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b001/_pkg_.a -trimpath "$WORK/b001=>" -p main -lang=go1.18 -complete -buildid ZhPqHmBh6WQ6HFsDI1Yh/ZhPqHmBh6WQ6HFsDI1Yh -goversion go1.18rc1 -c=4 -nolocalimports -importcfg $WORK/b001/importcfg -pack ./main.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b001/_pkg_.a # internal
cp $WORK/b001/_pkg_.a /Users/tonybai/Library/Caches/go-build/e8/e86257379cbdd59856f799594b63f3bb33ae89011955fee50e6fe90d3809ce5a-d # internal
cat >$WORK/b001/importcfg.link << 'EOF' # internal
packagefile demo1=$WORK/b001/_pkg_.a
packagefile demo1/pkg1=$WORK/b002/_pkg_.a
packagefile demo1/pkg2=$WORK/b003/_pkg_.a
packagefile runtime=$WORK/b004/_pkg_.a
packagefile internal/abi=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/abi.a
packagefile internal/bytealg=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/bytealg.a
packagefile internal/cpu=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/cpu.a
packagefile internal/goarch=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goarch.a
packagefile internal/goexperiment=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goexperiment.a
packagefile internal/goos=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goos.a
packagefile runtime/internal/atomic=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/atomic.a
packagefile runtime/internal/math=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/math.a
packagefile runtime/internal/sys=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/sys.a
modinfo "0w\xaf\f\x92t\b\x02A\xe1\xc1\a\xe6\xd6\x18\xe6path\tdemo1\nmod\tdemo1\t(devel)\t\nbuild\t-compiler=gc\nbuild\tCGO_ENABLED=1\nbuild\tCGO_CFLAGS=\nbuild\tCGO_CPPFLAGS=\nbuild\tCGO_CXXFLAGS=\nbuild\tCGO_LDFLAGS=\nbuild\tGOARCH=amd64\nbuild\tGOOS=darwin\nbuild\tGOAMD64=v1\nbuild\tvcs=git\nbuild\tvcs.revision=6534186d4b5b80c6c056237191fc703fa99cd19e\nbuild\tvcs.time=2022-03-12T13:52:57Z\nbuild\tvcs.modified=true\n\xf92C1\x86\x18 r\x00\x82B\x10A\x16\xd8\xf2"
EOF
mkdir -p $WORK/b001/exe/
cd .
### 笔者注：执行链接过程
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/link -o $WORK/b001/exe/a.out -importcfg $WORK/b001/importcfg.link -buildmode=exe -buildid=mzN3WRwHiNhsESy6r89L/ZhPqHmBh6WQ6HFsDI1Yh/Nvx0U2gM2zWzj7FTESXk/mzN3WRwHiNhsESy6r89L -extld=clang $WORK/b001/_pkg_.a
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b001/exe/a.out # internal
### 笔者注：将构建出来的可执行文件放到正确位置并改名
mv $WORK/b001/exe/a.out demo1
rm -r $WORK/b001/
```


#### b) 删除可执行文件后，再次构建

接下来我们删除之前构建出来的可执行文件demo1，然后再执行一次go build：

```
$go build -x -v
WORK=/var/folders/cz/sbj5kg2d3m3c6j650z0qfm800000gn/T/go-build3889005616
cd /Users/tonybai/test/go
git status --porcelain
cd /Users/tonybai/test/go
git show -s --no-show-signature --format=%H:%ct
mkdir -p $WORK/b001/
cat >$WORK/b001/importcfg.link << 'EOF' # internal
### 笔者注：这次构建直接使用了上一次缓存的各个包的缓存结果
packagefile demo1=/Users/tonybai/Library/Caches/go-build/e8/e86257379cbdd59856f799594b63f3bb33ae89011955fee50e6fe90d3809ce5a-d
packagefile demo1/pkg1=/Users/tonybai/Library/Caches/go-build/24/24519941f74b316c8e83f2d2462b62370692c5f56b04ec3df97e3124ff8b4633-d
packagefile demo1/pkg2=/Users/tonybai/Library/Caches/go-build/fe/fef7890aa0cf3bb97e872d2b49cd834a5fad87cd5d8bf052dca65e4cecb541d2-d
packagefile runtime=/Users/tonybai/Library/Caches/go-build/0e/0e28018e12d646c32443e88953b839c7ba0be3198e6a61afc8a74c0b3e76696a-d
packagefile internal/abi=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/abi.a
packagefile internal/bytealg=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/bytealg.a
packagefile internal/cpu=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/cpu.a
packagefile internal/goarch=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goarch.a
packagefile internal/goexperiment=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goexperiment.a
packagefile internal/goos=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goos.a
packagefile runtime/internal/atomic=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/atomic.a
packagefile runtime/internal/math=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/math.a
packagefile runtime/internal/sys=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/sys.a
modinfo "0w\xaf\f\x92t\b\x02A\xe1\xc1\a\xe6\xd6\x18\xe6path\tdemo1\nmod\tdemo1\t(devel)\t\nbuild\t-compiler=gc\nbuild\tCGO_ENABLED=1\nbuild\tCGO_CFLAGS=\nbuild\tCGO_CPPFLAGS=\nbuild\tCGO_CXXFLAGS=\nbuild\tCGO_LDFLAGS=\nbuild\tGOARCH=amd64\nbuild\tGOOS=darwin\nbuild\tGOAMD64=v1\nbuild\tvcs=git\nbuild\tvcs.revision=6534186d4b5b80c6c056237191fc703fa99cd19e\nbuild\tvcs.time=2022-03-12T13:52:57Z\nbuild\tvcs.modified=true\n\xf92C1\x86\x18 r\x00\x82B\x10A\x16\xd8\xf2"
EOF
mkdir -p $WORK/b001/exe/
cd .
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/link -o $WORK/b001/exe/a.out -importcfg $WORK/b001/importcfg.link -buildmode=exe -buildid=mzN3WRwHiNhsESy6r89L/ZhPqHmBh6WQ6HFsDI1Yh/Nvx0U2gM2zWzj7FTESXk/mzN3WRwHiNhsESy6r89L -extld=clang /Users/tonybai/Library/Caches/go-build/e8/e86257379cbdd59856f799594b63f3bb33ae89011955fee50e6fe90d3809ce5a-d
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b001/exe/a.out # internal
mv $WORK/b001/exe/a.out demo1
rm -r $WORK/b001/
```


通过go build命令输出的日志我们看到：go build并没有重新编译各个包中的源文件，而是直接使用上一次构建缓存在cache中的demo1、demo1/pkg1和demo1/pkg2进行链接并输出最终可执行文件。初步判断，Go编译器是可以识别出项目中的源文件是否发生了改变并决定是否对其重新编译的。

#### c) 新增pkg3

我们为demo1新增pkg3，并在main.go中调用pkg3包中的函数，相当于建立了一个对pkg3的依赖，然后我们再来build一下该项目：

```
$go build -x -v
WORK=/var/folders/cz/sbj5kg2d3m3c6j650z0qfm800000gn/T/go-build3890553968
cd /Users/tonybai/test/go
git status --porcelain
cd /Users/tonybai/test/go
git show -s --no-show-signature --format=%H:%ct
demo1/pkg3
mkdir -p $WORK/b004/
cat >$WORK/b004/importcfg << 'EOF' # internal
# import config
EOF
### 笔者注：构建pkg3
cd /Users/tonybai/test/go/incremental-build/demo1
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b004/_pkg_.a -trimpath "$WORK/b004=>" -p demo1/pkg3 -lang=go1.18 -complete -buildid yVeHBkrjxeJ1Ib-jc5Fu/yVeHBkrjxeJ1Ib-jc5Fu -goversion go1.18rc1 -c=4 -nolocalimports -importcfg $WORK/b004/importcfg -pack ./pkg3/pkg3.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b004/_pkg_.a # internal
cp $WORK/b004/_pkg_.a /Users/tonybai/Library/Caches/go-build/2c/2c02674d62c50d4f2b8439c9314ef51b3e211d45d4114fa495fdd0e20c43440d-d # internal
demo1
mkdir -p $WORK/b001/
cat >$WORK/b001/importcfg << 'EOF' # internal
# import config
### 笔者注：直接重用demo1/pkg1和demo1/pkg2在cache中的目标文件
packagefile demo1/pkg1=/Users/tonybai/Library/Caches/go-build/24/24519941f74b316c8e83f2d2462b62370692c5f56b04ec3df97e3124ff8b4633-d
packagefile demo1/pkg2=/Users/tonybai/Library/Caches/go-build/fe/fef7890aa0cf3bb97e872d2b49cd834a5fad87cd5d8bf052dca65e4cecb541d2-d
packagefile demo1/pkg3=$WORK/b004/_pkg_.a
packagefile runtime=/Users/tonybai/Library/Caches/go-build/0e/0e28018e12d646c32443e88953b839c7ba0be3198e6a61afc8a74c0b3e76696a-d
EOF
### 笔者注：重新编译main.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b001/_pkg_.a -trimpath "$WORK/b001=>" -p main -lang=go1.18 -complete -buildid Jii_iiylmm9d82X_Mzem/Jii_iiylmm9d82X_Mzem -goversion go1.18rc1 -c=4 -nolocalimports -importcfg $WORK/b001/importcfg -pack ./main.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b001/_pkg_.a # internal
cp $WORK/b001/_pkg_.a /Users/tonybai/Library/Caches/go-build/52/52b5b7e233ac17201702c26f1da97c5a23e42e68f74040d576905323a016f66e-d # internal
cat >$WORK/b001/importcfg.link << 'EOF' # internal
packagefile demo1=$WORK/b001/_pkg_.a
packagefile demo1/pkg1=/Users/tonybai/Library/Caches/go-build/24/24519941f74b316c8e83f2d2462b62370692c5f56b04ec3df97e3124ff8b4633-d
packagefile demo1/pkg2=/Users/tonybai/Library/Caches/go-build/fe/fef7890aa0cf3bb97e872d2b49cd834a5fad87cd5d8bf052dca65e4cecb541d2-d
packagefile demo1/pkg3=$WORK/b004/_pkg_.a
packagefile runtime=/Users/tonybai/Library/Caches/go-build/0e/0e28018e12d646c32443e88953b839c7ba0be3198e6a61afc8a74c0b3e76696a-d
packagefile internal/abi=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/abi.a
packagefile internal/bytealg=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/bytealg.a
packagefile internal/cpu=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/cpu.a
packagefile internal/goarch=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goarch.a
packagefile internal/goexperiment=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goexperiment.a
packagefile internal/goos=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goos.a
packagefile runtime/internal/atomic=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/atomic.a
packagefile runtime/internal/math=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/math.a
packagefile runtime/internal/sys=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/sys.a
modinfo "0w\xaf\f\x92t\b\x02A\xe1\xc1\a\xe6\xd6\x18\xe6path\tdemo1\nmod\tdemo1\t(devel)\t\nbuild\t-compiler=gc\nbuild\tCGO_ENABLED=1\nbuild\tCGO_CFLAGS=\nbuild\tCGO_CPPFLAGS=\nbuild\tCGO_CXXFLAGS=\nbuild\tCGO_LDFLAGS=\nbuild\tGOARCH=amd64\nbuild\tGOOS=darwin\nbuild\tGOAMD64=v1\nbuild\tvcs=git\nbuild\tvcs.revision=6534186d4b5b80c6c056237191fc703fa99cd19e\nbuild\tvcs.time=2022-03-12T13:52:57Z\nbuild\tvcs.modified=true\n\xf92C1\x86\x18 r\x00\x82B\x10A\x16\xd8\xf2"
EOF
mkdir -p $WORK/b001/exe/
cd .
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/link -o $WORK/b001/exe/a.out -importcfg $WORK/b001/importcfg.link -buildmode=exe -buildid=GM4wTB4eDZmuIuIaQgup/Jii_iiylmm9d82X_Mzem/5aVh7LKgEkk3c4g5_WBq/GM4wTB4eDZmuIuIaQgup -extld=clang $WORK/b001/_pkg_.a
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b001/exe/a.out # internal
mv $WORK/b001/exe/a.out demo1
rm -r $WORK/b001/
```


我们看到Go只是编译了新增的pkg3以及依赖pkg3的main.go，pkg1和pkg2包并未被重新编译，而是直接使用了缓存在gocache中的中间目标文件。

#### d) 重新编译单个变更的源文件还是重新编译整个包？

如果一个go package包含多个源文件，当某一个源文件发生内容变化时，go编译器是只会编译该源文件还是整个包呢？我们来验证一下。

我们为pkg3添加另外一个源文件pkg3_1.go，然后做一次构建。之后再修改pkg3_1.go，再做构建：

```
$go build -x -v
WORK=/var/folders/cz/sbj5kg2d3m3c6j650z0qfm800000gn/T/go-build213842995
cd /Users/tonybai/test/go
git status --porcelain
cd /Users/tonybai/test/go
git show -s --no-show-signature --format=%H:%ct
demo1/pkg3
mkdir -p $WORK/b004/
cat >$WORK/b004/importcfg << 'EOF' # internal
# import config
EOF
cd /Users/tonybai/test/go/incremental-build/demo1
### 笔者注：编译pkg3包
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b004/_pkg_.a -trimpath "$WORK/b004=>" -p demo1/pkg3 -lang=go1.18 -complete -buildid pX9UOIUBAZfMKmMgHv3q/pX9UOIUBAZfMKmMgHv3q -goversion go1.18rc1 -c=4 -nolocalimports -importcfg $WORK/b004/importcfg -pack ./pkg3/pkg3.go ./pkg3/pkg3_1.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b004/_pkg_.a # internal
cp $WORK/b004/_pkg_.a /Users/tonybai/Library/Caches/go-build/0c/0c3ce444d214c6c2999ba01b01eb4888c7864947d88bfcf63a41db4ac44002c2-d # internal
demo1
mkdir -p $WORK/b001/
cat >$WORK/b001/importcfg << 'EOF' # internal
# import config
packagefile demo1/pkg1=/Users/tonybai/Library/Caches/go-build/24/24519941f74b316c8e83f2d2462b62370692c5f56b04ec3df97e3124ff8b4633-d
packagefile demo1/pkg2=/Users/tonybai/Library/Caches/go-build/fe/fef7890aa0cf3bb97e872d2b49cd834a5fad87cd5d8bf052dca65e4cecb541d2-d
packagefile demo1/pkg3=$WORK/b004/_pkg_.a
packagefile runtime=/Users/tonybai/Library/Caches/go-build/0e/0e28018e12d646c32443e88953b839c7ba0be3198e6a61afc8a74c0b3e76696a-d
EOF
### 笔者注：编译依赖pkg3包的main.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b001/_pkg_.a -trimpath "$WORK/b001=>" -p main -lang=go1.18 -complete -buildid cQBq3r5n1_wurKrb8Xmq/cQBq3r5n1_wurKrb8Xmq -goversion go1.18rc1 -c=4 -nolocalimports -importcfg $WORK/b001/importcfg -pack ./main.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b001/_pkg_.a # internal
cp $WORK/b001/_pkg_.a /Users/tonybai/Library/Caches/go-build/e2/e2818b14455f4dd54caf5f731c7b3b6b8254a37a8912e73c33b327771069bde7-d # internal
cat >$WORK/b001/importcfg.link << 'EOF' # internal
packagefile demo1=$WORK/b001/_pkg_.a
packagefile demo1/pkg1=/Users/tonybai/Library/Caches/go-build/24/24519941f74b316c8e83f2d2462b62370692c5f56b04ec3df97e3124ff8b4633-d
packagefile demo1/pkg2=/Users/tonybai/Library/Caches/go-build/fe/fef7890aa0cf3bb97e872d2b49cd834a5fad87cd5d8bf052dca65e4cecb541d2-d
packagefile demo1/pkg3=$WORK/b004/_pkg_.a
packagefile runtime=/Users/tonybai/Library/Caches/go-build/0e/0e28018e12d646c32443e88953b839c7ba0be3198e6a61afc8a74c0b3e76696a-d
packagefile internal/abi=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/abi.a
packagefile internal/bytealg=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/bytealg.a
packagefile internal/cpu=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/cpu.a
packagefile internal/goarch=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goarch.a
packagefile internal/goexperiment=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goexperiment.a
packagefile internal/goos=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goos.a
packagefile runtime/internal/atomic=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/atomic.a
packagefile runtime/internal/math=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/math.a
packagefile runtime/internal/sys=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/sys.a
modinfo "0w\xaf\f\x92t\b\x02A\xe1\xc1\a\xe6\xd6\x18\xe6path\tdemo1\nmod\tdemo1\t(devel)\t\nbuild\t-compiler=gc\nbuild\tCGO_ENABLED=1\nbuild\tCGO_CFLAGS=\nbuild\tCGO_CPPFLAGS=\nbuild\tCGO_CXXFLAGS=\nbuild\tCGO_LDFLAGS=\nbuild\tGOARCH=amd64\nbuild\tGOOS=darwin\nbuild\tGOAMD64=v1\nbuild\tvcs=git\nbuild\tvcs.revision=6534186d4b5b80c6c056237191fc703fa99cd19e\nbuild\tvcs.time=2022-03-12T13:52:57Z\nbuild\tvcs.modified=true\n\xf92C1\x86\x18 r\x00\x82B\x10A\x16\xd8\xf2"
EOF
mkdir -p $WORK/b001/exe/
cd .
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/link -o $WORK/b001/exe/a.out -importcfg $WORK/b001/importcfg.link -buildmode=exe -buildid=qvFsK1K1jm8CeANRL3a2/cQBq3r5n1_wurKrb8Xmq/BB3nEx0b9edm7IM0XGAQ/qvFsK1K1jm8CeANRL3a2 -extld=clang $WORK/b001/_pkg_.a
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b001/exe/a.out # internal
mv $WORK/b001/exe/a.out demo1
rm -r $WORK/b001/
```


我们看到：虽然只修改了pkg3包下面的源文件pkg3_1.go，但go build还是会将整个包的所有源文件都重新编译一次。依赖pkg3包的main.go也会被随之重新编译。就此可以证实，**Go的增量编译是以Go包为基本单位的，而不是以单个源文件为单位的**。这与go工具缓存在gocache中的中间目标文件(pkg.a)**以包为单位的**是一致的。

#### e) 当间接依赖的包发生了变动

前面的示例展示的都是直接依赖包发生变动后，增量构建涵盖的编译单元范畴。如果某个包的间接依赖包发生变化，该包是否会参与增量构建呢？答案是肯定的。我们继续用示例来证明一下。

我们为该demo1项目增加pkg4包，并使得pkg3依赖pkg4。这样就会出现main.go直接依赖pkg3包，间接依赖pkg4包的情况。我们在添加完pkg4包后，进行一次构建。之后修改pkg4包的部分内容，然后再执行构建，其输出日志如下：

```
$go build -x -v
WORK=/var/folders/cz/sbj5kg2d3m3c6j650z0qfm800000gn/T/go-build2817187631
cd /Users/tonybai/test/go
git status --porcelain
cd /Users/tonybai/test/go
git show -s --no-show-signature --format=%H:%ct
demo1/pkg4
mkdir -p $WORK/b005/
cat >$WORK/b005/importcfg << 'EOF' # internal
# import config
EOF
### 笔者注：编译demo1/pkg4包
cd /Users/tonybai/test/go/incremental-build/demo1
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b005/_pkg_.a -trimpath "$WORK/b005=>" -p demo1/pkg4 -lang=go1.18 -complete -buildid AIv0TfCgKL2o00SexGru/AIv0TfCgKL2o00SexGru -goversion go1.18rc1 -c=4 -nolocalimports -importcfg $WORK/b005/importcfg -pack ./pkg4/pkg4.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b005/_pkg_.a # internal
cp $WORK/b005/_pkg_.a /Users/tonybai/Library/Caches/go-build/7e/7e2b8f229f8ca2f1ee315438f61cad5421bb5af9ed155e88a460faca806f4f90-d # internal
demo1/pkg3
mkdir -p $WORK/b004/
cat >$WORK/b004/importcfg << 'EOF' # internal
# import config
packagefile demo1/pkg4=$WORK/b005/_pkg_.a
EOF
### 笔者注：编译直接依赖demo1/pkg4包的demo1/pkg3包
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b004/_pkg_.a -trimpath "$WORK/b004=>" -p demo1/pkg3 -lang=go1.18 -complete -buildid ObVmRzLu3J1liPWzEiXx/ObVmRzLu3J1liPWzEiXx -goversion go1.18rc1 -c=4 -nolocalimports -importcfg $WORK/b004/importcfg -pack ./pkg3/pkg3.go ./pkg3/pkg3_1.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b004/_pkg_.a # internal
cp $WORK/b004/_pkg_.a /Users/tonybai/Library/Caches/go-build/4f/4f69cad7558ecf297799e29353bc802415785847c195555c22151f52abe1d9d9-d # internal
demo1
mkdir -p $WORK/b001/
cat >$WORK/b001/importcfg << 'EOF' # internal
# import config
packagefile demo1/pkg1=/Users/tonybai/Library/Caches/go-build/24/24519941f74b316c8e83f2d2462b62370692c5f56b04ec3df97e3124ff8b4633-d
packagefile demo1/pkg2=/Users/tonybai/Library/Caches/go-build/fe/fef7890aa0cf3bb97e872d2b49cd834a5fad87cd5d8bf052dca65e4cecb541d2-d
packagefile demo1/pkg3=$WORK/b004/_pkg_.a
packagefile runtime=/Users/tonybai/Library/Caches/go-build/0e/0e28018e12d646c32443e88953b839c7ba0be3198e6a61afc8a74c0b3e76696a-d
EOF
### 笔者注：编译间接依赖demo1/pkg4包的main.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/compile -o $WORK/b001/_pkg_.a -trimpath "$WORK/b001=>" -p main -lang=go1.18 -complete -buildid i543xzAqlwVlWgQBYhsS/i543xzAqlwVlWgQBYhsS -goversion go1.18rc1 -c=4 -nolocalimports -importcfg $WORK/b001/importcfg -pack ./main.go
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b001/_pkg_.a # internal
cp $WORK/b001/_pkg_.a /Users/tonybai/Library/Caches/go-build/67/67a5ff80f6dbbbe01fcf9efb4d6ff380cb27fd1723b06b209a17987f1c74f425-d # internal
cat >$WORK/b001/importcfg.link << 'EOF' # internal
packagefile demo1=$WORK/b001/_pkg_.a
packagefile demo1/pkg1=/Users/tonybai/Library/Caches/go-build/24/24519941f74b316c8e83f2d2462b62370692c5f56b04ec3df97e3124ff8b4633-d
packagefile demo1/pkg2=/Users/tonybai/Library/Caches/go-build/fe/fef7890aa0cf3bb97e872d2b49cd834a5fad87cd5d8bf052dca65e4cecb541d2-d
packagefile demo1/pkg3=$WORK/b004/_pkg_.a
packagefile runtime=/Users/tonybai/Library/Caches/go-build/0e/0e28018e12d646c32443e88953b839c7ba0be3198e6a61afc8a74c0b3e76696a-d
packagefile demo1/pkg4=$WORK/b005/_pkg_.a
packagefile internal/abi=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/abi.a
packagefile internal/bytealg=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/bytealg.a
packagefile internal/cpu=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/cpu.a
packagefile internal/goarch=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goarch.a
packagefile internal/goexperiment=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goexperiment.a
packagefile internal/goos=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/internal/goos.a
packagefile runtime/internal/atomic=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/atomic.a
packagefile runtime/internal/math=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/math.a
packagefile runtime/internal/sys=/Users/tonybai/.bin/go1.18rc1/pkg/darwin_amd64/runtime/internal/sys.a
modinfo "0w\xaf\f\x92t\b\x02A\xe1\xc1\a\xe6\xd6\x18\xe6path\tdemo1\nmod\tdemo1\t(devel)\t\nbuild\t-compiler=gc\nbuild\tCGO_ENABLED=1\nbuild\tCGO_CFLAGS=\nbuild\tCGO_CPPFLAGS=\nbuild\tCGO_CXXFLAGS=\nbuild\tCGO_LDFLAGS=\nbuild\tGOARCH=amd64\nbuild\tGOOS=darwin\nbuild\tGOAMD64=v1\nbuild\tvcs=git\nbuild\tvcs.revision=6534186d4b5b80c6c056237191fc703fa99cd19e\nbuild\tvcs.time=2022-03-12T13:52:57Z\nbuild\tvcs.modified=true\n\xf92C1\x86\x18 r\x00\x82B\x10A\x16\xd8\xf2"
EOF
mkdir -p $WORK/b001/exe/
cd .
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/link -o $WORK/b001/exe/a.out -importcfg $WORK/b001/importcfg.link -buildmode=exe -buildid=5U4vzFHU8ahkEvKH4-CV/i543xzAqlwVlWgQBYhsS/GOFyatqByKmjWK1zLLiq/5U4vzFHU8ahkEvKH4-CV -extld=clang $WORK/b001/_pkg_.a
/Users/tonybai/.bin/go1.18rc1/pkg/tool/darwin_amd64/buildid -w $WORK/b001/exe/a.out # internal
mv $WORK/b001/exe/a.out demo1
rm -r $WORK/b001/
```


我们看到：pkg4包修改后，无论是直接依赖pkg4的包，还是间接依赖pkg4的包都会在下次增量构建时被重新编译。

### 3. 小结

由上面的示例我们看到：Go编译器是原生支持增量构建的，无需第三方构建管理工具的辅助。Go的增量构建是建立在[Go 1.10引入的build cache机制](https://tonybai.com/2018/02/17/some-changes-in-go-1-10)的基础上的。Go的增量构建以Go包为单位，当Go包中的任一源文件发生变化时，Go都会对其进行重新构建，并且会连带构建所有直接或间接依赖该包的Go包。

本文示例源码在[这里](https://github.com/bigwhite/experiments/tree/master/incremental-build/demo1)可以下载。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](http://image.tonybai.com/img/tonybai/imooc-go-column-pgo-with-qr.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论