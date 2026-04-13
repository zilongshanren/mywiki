---
title: 编译Go应用的黑盒挑战：无源码只有.a文件，你能搞定吗？
url: https://tonybai.com/2023/08/30/how-to-build-with-only-archive-in-go/
published: '2023-08-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 编译Go应用的黑盒挑战：无源码只有.a文件，你能搞定吗？

![](../../assets/54288d90350b8894.png)


[本文永久链接](https://tonybai.com/2023/08/30/how-to-build-with-only-archive-in-go) – https://tonybai.com/2023/08/30/how-to-build-with-only-archive-in-go

上周末，一个Gopher在微信上与我交流了一个有关Go程序编译的问题。他的述求说起来也不复杂，那就是合作公司提供的API包仅包括golang archive(使用go build -buildmode=archive构建的.a文件)，没有Go包的源码。如何将这个.a链接到项目构建出的最终可执行程序中呢？

对于C、C++、Java程序员来说，仅提供静态链接库或[动态链接库](https://tonybai.com/2011/07/07/also-talk-about-shared-library-2/)(包括头文件)、jar包而不提供源码的API是十分寻常的。但对于Go来说，仅提供Go包的archive(.a)文件，而不提供Go包源码的情况却是极其不常见的。究其原因，简单来说就是**go build或go run不支持**！

注：

[《Go语言精进之路vo1》]一书的第16条“理解Go语言的包导入”对Go的编译过程和原理做了系统说明。

那么真的就没有方法实现没有source、仅基于.a文件的Go应用构建了吗？也不是。的确有一些hack的方法可以实现这点，本文就来从技术角度来探讨一下这些hack方法，但并**不推荐使用**！

## 1. 回顾go build不支持”no source, only .a”

我们首先来回顾一下go build在”no source, only .a”下的表现。为此，我们先建立一个实验环境，其目录和文件布局如下：

```
// 没有外部依赖的api包: foo
$tree goarchive-nodeps
goarchive-nodeps
├── Makefile
├── foo.a
├── foo.go
└── go.mod
$tree library
library
└── github.com
└── bigwhite
└── foo.a
// 依赖foo包的app工程
$tree app-link-foo
app-link-foo
├── Makefile
├── go.mod
└── main.go
```


这里我们已经将app-link-foo依赖的foo.a构建了出来(通过go build -buildmode=arhive)，并放入了library对应的目录下。

注：可通过ar -x foo.a命令可以查看foo.a的组成。


现在我们使用go build来构建app-link-foo工程：

```
$cd app-link-foo
$go build
main.go:6:2: no required module provides package github.com/bigwhite/foo; to add it:
go get github.com/bigwhite/foo
```


我们看到：go build会分析app-link-foo的依赖，并要求获取其依赖的foo包的代码，但我们无法满足go build这一要求！

有人可能会说：go build支持向go build支持向compiler和linker传递参数，是不是将foo.a的位置告知compiler和linker就可以了呢？我们来试试：

```
$go build -x -v -gcflags '-I /Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/library' -ldflags '-L /Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/library' -o main main.go
main.go:6:2: no required module provides package github.com/bigwhite/foo; to add it:
go get github.com/bigwhite/foo
make: *** [build] Error 1
```


我们看到：即便向go build传入gcflags和ldflags参数，告知了foo.a的搜索路径，go build依然报错，仍然提示需要foo包的源码！也就是说go build还没到调用go tool compile和go tool link那一步就开始报错了！

go build不支持在无源码情况下链接.a，那么我们**只能绕过go build**了！

## 2. 绕过go bulid

认真读过[《Go语言精进之路vo1》](https://item.jd.com/13694000.html)一书的朋友都会知道：go build实质是调用go tool compile和go tool link两个命令来完成go应用的构建过程的，使用go build -x -v可以查看到go build的详细构建过程。

接下来，我们就来扮演一下”go build”，以手动的方式分别调用go tool compile和go tool link，看看是否能达到无需依赖包源码就能成功构建的目标。

我们以foo.a这个自身没有外部依赖的go archive为例，用手动方式构建一下app-link-foo这个工程。

首先确保通过-buildmode=archive构建出的foo.a被正确放入library/github.com/bigwhite下面。

接下来，我们通过go tool compile编译一下app-link-foo：

```
$cd app-link-foo
$go tool compile -I /Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/library -o main.o main.go
```


我们看到：手动执行go tool compile在通过-I传入依赖库的.a文件时是可以正常编译出object file(目标文件)的。go tool compile的手册告诉我们-I选项为compile提供了搜索包导入路径的目录：

```
$go tool compile -h
... ...
-I directory
add directory to import search path
... ...
```


接下来我们用go tool link将main.o和foo.a链接在一起形成可执行二进制文件main：

```
$cd app-link-foo
$go tool link -L /Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/library -o main main.o
```


通过go tool link并在-L传入foo.a的链接路径的情况下，我们成功地将main.o和foo.a链接在了一起，形成了最终的可执行文件main。

go tool link的-L选项为link提供了搜索.a的路径：

```
$go tool link -h
... ...
-L directory
add specified directory to library path
... ...
```


执行一下编译链接后的二进制文件main，我们将看到与预期相同的输出结果：

```
$./main
invoke foo.Add
11
```


有些童鞋在执行go tool compile时可能会遇到找不到fmt.a或fmt.o的错误！这是因为Go 1.20版本及以后，Go安装包默认将不会在\$GOROOT/pkg/\$GOOS_\$GOARCH下面安装标准库的.a文件集合，这样go tool compile在这个路径下面就找不到app-link-foo所依赖的fmt.a：

```
➜ /Users/tonybai/.bin/go1.20/pkg git:(master) ✗ $ls
darwin_amd64/ include/ tool/
➜ /Users/tonybai/.bin/go1.20/pkg git:(master) ✗ $cd darwin_amd64
➜ /Users/tonybai/.bin/go1.20/pkg/darwin_amd64 git:(master) ✗ $ls
```


解决方法也很简单，那就是手动执行下面命令编译和安装一下标准库的.a文件：

```
$GODEBUG=installgoroot=all go install std
➜ /Users/tonybai/.bin/go1.20/pkg/darwin_amd64 git:(master) ✗ $ls
archive/ database/ fmt.a index/ mime/ plugin.a strconv.a time/
bufio.a debug/ go/ internal/ mime.a reflect/ strings.a time.a
bytes.a embed.a hash/ io/ net/ reflect.a sync/ unicode/
compress/ encoding/ hash.a io.a net.a regexp/ sync.a unicode.a
container/ encoding.a html/ log/ os/ regexp.a syscall.a vendor/
context.a errors.a html.a log.a os.a runtime/ testing/
crypto/ expvar.a image/ math/ path/ runtime.a testing.a
crypto.a flag.a image.a math.a path.a sort.a text/
```


这样无论是go tool compile，还是go tool link都会找到对应的标准库包了！

在这个例子中，foo.a仅依赖标准库，没有依赖第三方库，这样相对简单一些。通常合作伙伴提供的.a中的包都是依赖第三方的包的，下面我们就来看看如果.a有第三方依赖，上面的编译链接方法是否还能奏效！

## 3. 要链接的.a文件自身也依赖第三方包

goarchive-with-deps目录下的bar.a就是一个自身也依赖第三方包的go archive文件，它依赖的是uber的[zap日志包](https://tonybai.com/2021/07/14/uber-zap-advanced-usage)以及zap包的依赖链，下面是bar的go.mod文件的内容：

```
// goarchive-with-deps/go.mod
module github.com/bigwhite/bar
go 1.20
require go.uber.org/zap v1.25.0
require go.uber.org/multierr v1.10.0
```


我们先来安装app-link-foo的思路来编译链接一下app-link-bar：

```
$cd app-link-bar
$make
go tool compile -I /Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/library -o main.o main.go
go tool link -L /Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/library -o main main.o
/Users/tonybai/.bin/go1.20/pkg/tool/darwin_amd64/link: cannot open file /Users/tonybai/.bin/go1.20/pkg/darwin_amd64/go.uber.org/zap.o: open /Users/tonybai/.bin/go1.20/pkg/darwin_amd64/go.uber.org/zap.o: no such file or directory
make: *** [all] Error 1
```


上面报的错误符合预期，因为zap.a尚没有放入build-with-archive-only/library下面。接下来我们基于uber zap的源码构建出一个zap.a并放入指定目录。bar.a依赖的uber zap的版本为v1.25.0，于是我们git clone一下uber zap，checkout出v1.25.0并执行构建：

```
$cd go/src/go.uber.org/zap
$go build -o zap.a -buildmode=archive .
$cp zap.a /Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/library/go.uber.org/
```


再来编译一下app-link-bar：

```
$make
go tool compile -I /Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/library -o main.o main.go
go tool link -L /Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/library -o main main.o
/Users/tonybai/.bin/go1.20/pkg/tool/darwin_amd64/link: fingerprint mismatch: go.uber.org/zap has b259b1e07032c6d9, import from github.com/bigwhite/bar expecting 8118f660c835360a
make: *** [all] Error 1
```


我们看到go tool link报错，提示“fingerprint mismatch”。这个错误的意思是bar.a期望的zap包的指纹与我们提供的在Library目录下的zap包的指纹不一致！

我们重新用go build -v -x来看一下bar.a的构建过程：

```
$go build -x -v -o bar.a -buildmode=archive
WORK=/var/folders/cz/sbj5kg2d3m3c6j650z0qfm800000gn/T/go-build3367014838
github.com/bigwhite/bar
mkdir -p $WORK/b001/
cat >/var/folders/cz/sbj5kg2d3m3c6j650z0qfm800000gn/T/go-build3367014838/b001/importcfg << 'EOF' # internal
# import config
packagefile fmt=/Users/tonybai/Library/Caches/go-build/d3/d307b52dabc7d78a8ff219fb472fbc0b0a600038f43cd4c737914f8ccbd2bd70-d
packagefile go.uber.org/zap=/Users/tonybai/Library/Caches/go-build/00/006d48e40c867a336b9ac622478c1e5bf914e6a5986f649a096ebede3d117bba-d
EOF
cd /Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/goarchive-with-deps
/Users/tonybai/.bin/go1.20/pkg/tool/darwin_amd64/compile -o $WORK/b001/_pkg_.a -trimpath "$WORK/b001=>" -p github.com/bigwhite/bar -lang=go1.20 -complete -buildid mIMNOXMPJH00mEpw6WVc/mIMNOXMPJH00mEpw6WVc -goversion go1.20 -c=4 -nolocalimports -importcfg $WORK/b001/importcfg -pack ./bar.go
/Users/tonybai/.bin/go1.20/pkg/tool/darwin_amd64/buildid -w $WORK/b001/_pkg_.a # internal
cp $WORK/b001/_pkg_.a /Users/tonybai/Library/Caches/go-build/60/604b60360d384c49eb9c030a2726f02588f54375748ce1421e334bedfda2af47-d # internal
mv $WORK/b001/_pkg_.a bar.a
rm -r $WORK/b001/
```


我们看到在编译bar.a的过程中，go tool compile用的是-importcfg来得到的go.uber.org/zap的位置，而从打印的内容来看，go.uber.org/zap指向的是go module cache中的某个文件：packagefile go.uber.org/zap=/Users/tonybai/Library/Caches/go-build/00/006d48e40c867a336b9ac622478c1e5bf914e6a5986f649a096ebede3d117bba-d。

那是不是在build app-link-bar时也使用这个同样的go.uber.org/zap就可以成功通过go tool link的过程呢？我们来试一下：

```
$cd app-link-bar
$make build-with-importcfg
go tool compile -importcfg import.link -o main.o main.go
go tool link -importcfg import.link -o main main.o
$./main
invoke foo.Add
{"level":"info","ts":1693203940.0701509,"caller":"goarchive-with-deps/bar.go:14","msg":"invoke bar.Add\n"}
11
```


使用-importcfg的确成功的编译链接了app-link-bar，其执行结果也符合预期！注意：这里我们放弃了之前使用的-I和-L，即便应用-I和-L，在与-importcfg联合使用时，go tool compile和link也会以-importcfg的信息为准！

现在还有一个问题摆在面前，那就是上述命令行中的import.link这个文件的内容是啥，又是如何生成的呢？这里的import.link文件十分“巨大”，有500多行，其内容大致如下：

```
// app-link-bar/import.link
# import config
packagefile internal/goos=/Users/tonybai/Library/Caches/go-build/fa/facce9766a2b3c19364ee55c509863694b205190c504a3831cde7c208bb09f37-d
packagefile vendor/golang.org/x/crypto/chacha20=/Users/tonybai/Library/Caches/go-build/e0/e042b43b78d3596cc00e544a40a13e8cd6b566eb8f59c2d47aeb0bbcbd52aa56-d
... ...
packagefile github.com/bigwhite/bar=/Users/tonybai/Go/src/github.com/bigwhite/experiments/build-with-archive-only/library/github.com/bigwhite/bar.a
packagefile go.uber.org/zap=/Users/tonybai/Library/Caches/go-build/00/006d48e40c867a336b9ac622478c1e5bf914e6a5986f649a096ebede3d117bba-d
packagefile go.uber.org/zap/zapcore=/Users/tonybai/Library/Caches/go-build/e0/e0d81701b5d15628ce5bf174e5c1b7482c13ac3a3c868e9b054da8b1596eaace-d
packagefile go.uber.org/zap/internal/pool=/Users/tonybai/Library/Caches/go-build/bf/bfa96ebb89429b870e2c50c990c1945384e50d10ba354a3dab2b995a813c56a3-d
packagefile go.uber.org/zap/internal=/Users/tonybai/Library/Caches/go-build/33/33cb66c30939b8be915ddc1e237a04688f52c492d3ae58bfbc6196fff8b6b2b5-d
packagefile go.uber.org/zap/internal/bufferpool=/Users/tonybai/Library/Caches/go-build/68/68e58338a5acd96ee1733de78547720f26f4e13d8333defbc00099ac8560c8e8-d
packagefile go.uber.org/zap/buffer=/Users/tonybai/Library/Caches/go-build/7b/7bf00a1d4a69ddb1712366f45451890f3205b58ba49627ed4254acd9b0938ef8-d
packagefile go.uber.org/multierr=/Users/tonybai/Library/Caches/go-build/e7/e7cc278d56fc8262d9cf9de840a04aa675c75f8ac148e955c1ae9950c58c8034-d
packagefile go.uber.org/zap/internal/exit=/Users/tonybai/Library/Caches/go-build/18/187b2b490c810f37c3700132fba12b805e74bd3c59303972bcf74894a63de604-d
packagefile go.uber.org/zap/internal/color=/Users/tonybai/Library/Caches/go-build/e4/e419c93bea7ff2782b2047cf9e7ad37b07cf4a5a5b7f361bf968730e107a495b-d
```


这里包含了编译链接app-link-bar是依赖的标准库包、bar.a以及bar包依赖的所有第三方包的实际包.a文件的位置，显然这里用的大多数都是go module cache中的包缓存。

那么这个import.link如何得到呢？Go在golang.org/x/tools包中有一个[importcfg.go文件](https://raw.githubusercontent.com/golang/tools/master/internal/goroot/importcfg.go)，基于该文件中的Importcfg函数可以获取标准库相关所有包的package link信息。我将该文件放在了build-with-archive-only/importcfg下了，大家可以自行取用。

importcfg生成了大部分package link，但仍会有一些bar.a依赖的第三方的包的link没有着落，go tool link在链接时会报错，根据报错信息中提供的包导入路径信息，比如：找不到go.uber.org/zap/internal/exit、go.uber.org/zap/internal/color，我们可以利用下面go list命令找到这些包的在本地go module cache中的link位置：

```
$go list -export -e -f "{{.ImportPath}} {{.Export}}" go.uber.org/zap/internal/exit go.uber.org/zap/internal/color
go.uber.org/zap/internal/exit /Users/tonybai/Library/Caches/go-build/18/187b2b490c810f37c3700132fba12b805e74bd3c59303972bcf74894a63de604-d
go.uber.org/zap/internal/color /Users/tonybai/Library/Caches/go-build/e4/e419c93bea7ff2782b2047cf9e7ad37b07cf4a5a5b7f361bf968730e107a495b-d
```


然后可以手工将这些信息copy到import.link中。import.link文件就是在这样自动化+手工的过程中生成的（当然你完全可以自己编写一个工具，获取app-link-bar所需的所有package的link信息）。

## 4. 小结

到这里，我们通过hack的方法实现了在没有源码只有.a文件情况下的可执行程序的编译。

不过上述仅仅是纯技术上的探索，并非标准答案，也更非理想的答案。经过上述探索后，更巩固了我的观点：**不要仅使用.a来构建go应用**。

但非要这么做，如果你是.a的提供方，考虑fingerprint mismatch的情况，你估计要考虑在提供.a的同时，还要提供import.link、你构建.a时所有用到的go module cache的副本，并提供安装这些副本到目标主机上的脚本。这样你的.a用户才可能使用相同的依赖版本完成对.a文件的链接过程。

本文试验的代码都是在[Go 1.20版本](https://tonybai.com/2023/02/08/some-changes-in-go-1-20/)下编译链接的。如果编译.a的Go版本与编译链接可执行文件的Go版本不同，是否会失败呢？这个问题就当做作业留个大家去探索了！

本文涉及的代码可以从[这里](https://github.com/bigwhite/experiments/blob/master/build-with-archive-only)下载。

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论