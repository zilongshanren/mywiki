---
title: godep支持Go 1.5 vendor
url: https://tonybai.com/2015/08/05/godep-support-go15-vendor/
published: '2015-08-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# godep支持Go 1.5 vendor

[Go 1.5 vendor](http://tonybai.com/2015/07/31/understand-go15-vendor/)/实验特性出炉后，市面上的go第三方包依赖和管理工具显然都无法与之兼容，除了修改代码，别无它法。市场占有率最大的[godep](http://tonybai.com/2014/10/30/a-hole-of-godep/)做出了表 率，目前其最新版本(go get github.com/tools/godep)已经初步支持了这一实验特性，即在GO15VENDOREXPERIMENT=1时，将使用vendor 目录（而不是Godeps目录）存放copy的第三方包，并在godep go build时不再rewrite GOPATH就可以实现利用vendor下第三方包的构建。下面我们就用例子来验证一下Godep对vendor的支持。

**一、升级godep到最新版本**

如果要用到go 1.5 vendor，那么[godep](http://github.com/tools/godep)要升级（go get -u github.com/tools/godep;go build github.com/tools/godep）到当前的最新版本“commit d8799f112f6c8dfe1e56142831bc3bb5c8796a0e”。最新版本兼容老版本的功能，同时提供对go 1.5 vendor支持，两者之间转换的开关就是环境变量：GO15VENDOREXPERIMENT。

当GO15VENDOREXPERIMENT没有被set时，godep沿用以前的方式；当GO15VENDOREXPERIMENT = 1时，godep将用vendor替代Godeps目录以存放第三方包，同时go save将无法使用-r命令行选项(-r选项用于重写源码中的import path)：

$ godep save -r

godep: flag -r is incompatible with the vendoring experiment

**二、****例子**

下面是一个godep的例子（go 1.5 beta3），例子的目录结构如下：

$(GOPATH)/src/tonybai.com/

├── app

│ └── main.go

└── foolib

└── foolib.go

//foolib.go package foo import "fmt" func Hello() { fmt.Println("Hello from foolib") } //main.go package main import "tonybai.com/foolib" func main() { foo.Hello() }

如果GO15VENDOREXPERIMENT没有被set时，godep的各种命令将按之前的方式执行。

$ godep save

$ godep go build

$(GOPATH)/src/tonybai.com/

├── Godeps

│ ├── Godeps.json

│ ├── Readme

│ └── _workspace

│ └── src

│ └── tonybai.com

│ └── foolib

│ └── foolib.go

├── app*

└── main.go

$./app

Hello from foolib

godep将第三方包放在Godeps/_workspace/src下面。godep go build会rewrite GOPATH以实现使用_workspace下面的第三方包来构建的目的。

如果GO15VENDOREXPERIMENT = 1,那么godep会按照新的方式执行各种命令：

$ godep save

$ godep go build

$(GOPATH)/src/tonybai.com/

├── Godeps

│ ├── Godeps.json

│ └── Readme

├── app*

├── main.go

└── vendor

└── tonybai.com

└── foolib

└── foolib.go

可以看出godep建立vendor目录来存放第三方包，Godeps目录依然保留，但只是存放Godeps.json，以保存些第三方包的meta信息:

//Godeps.json

{

"ImportPath": "tonybai.com/app",

"GoVersion": "go1.5beta3",

"Deps": [

{

"ImportPath": "tonybai.com/foolib",

"Rev": "7f2f94dc589ba9e053ef13b3b01fa327c27bf161"

}

]

}

**三、迁移**

由于godep前后的两种工作模式并不兼容，因此大量存量的使用godep的repo，如果想使用Go 1.5 vendor，那么在升级到Go 1.5之后需要做一些迁移工作。godep没有提供自动的迁移工具，目前只能手动迁移，godep github主页上给出了手动迁移的命令步骤：

$ unset GO15VENDOREXPERIMENT

$ godep restore

//如果之前使用了godep save -r，那么下面这行命令将自动undo rewritten import。

$ godep save ./…

$ rm -rf Godeps

$ export GO15VENDOREXPERIMENT=1

$ godep save ./…

# You should see your Godeps/_workspace/src files "moved" to vendor/.

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

您好，请教一下 Godep 能否处理两个包依赖不同版本的同一个包的问题呢。谢谢。

如果你说的两个包共享同一level的vendor目录，那么做不到；如果两个包各自有自己的vendor，那就应该可以实现依赖同一个包的不同版本。这样要看你的项目源码目录组织结构了

我在这里贴图提问了，您能看一下吗，谢谢。https://segmentfault.com/q/1010000008765693