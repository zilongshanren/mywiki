---
title: Golang跨平台交叉编译
url: https://tonybai.com/2014/10/20/cross-compilation-with-golang/
published: '2014-10-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Golang跨平台交叉编译

近期在某本书上看到[Go](http://golang.org)跨平台交叉编译的强大功能，于是想自己测试一下。以下记录了测试过程以及一些结论，希望能给大家带来帮助。

我的Linux环境如下：

uname -a

Linux ubuntu-Server-14 3.13.0-32-generic #57-Ubuntu SMP Tue Jul 15 03:51:08 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux

$ go version

go version go1.3.1 linux/amd64

跨平台交叉编译涉及两个重要的环境变量：GOOS和GOARCH，分别代表Target Host OS和Target Host ARCH，如果没有显式设置这些环境变量，我们通过go env可以看到go编译器眼中这两个环境变量的当前值：

$ go env

GOARCH="amd64"

GOOS="linux"

GOHOSTARCH="amd64"

GOHOSTOS="linux"

… …

这里还有两个变量GOHOSTOS和GOHOSTARCH，分别表示的是当前所在主机的的OS和CPU ARCH。我的Go是采用安装包安装的，因此默认情况下，这两组环境变量的值都是来自当前主机的信息。

现在我们就来交叉编译一下：在linux/amd64平台下利用Go编译器编译一个可以运行在linux/amd64下的程序，样例程序如下：

//testport.go

package main

import (

"fmt"

"os/exec"

"bytes"

)

func main() {

cmd := exec.Command("uname", "-a")

var out bytes.Buffer

cmd.Stdout = &out

err := cmd.Run()

if err != nil {

fmt.Println("Err when executing uname command")

return

}

fmt.Println("I am running on", out.String())

}

在Linux/amd64下编译运行：

$ go build -o testport_linux testport.go

$ testport_linux

I am running on Linux ubuntu-Server-14 3.13.0-32-generic #57-Ubuntu SMP Tue Jul 15 03:51:08 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux

接下来，我们来尝试在Linux/amd64上编译一个可以运行在darwin/amd64上的程序。我只需修改GOOS和GOARCH两个标识目标主机OS和ARCH的环境变量：

$ GOOS=darwin GOARCH=amd64 go build -o testport_darwin testport.go

go build runtime: darwin/amd64 must be bootstrapped using make.bash

编译器报错了！提示darwin/amd64必须通过make.bash重新装载。显然，通过安装包安装到linux/amd64下的Go编译器还无法直接交叉编译出darwin/amd64下可以运行的程序，我们需要做一些准备工作。我们找找make.bash在哪里！

我们到Go的$GOROOT路径下去找make.bash，Go的安装路径下的组织很简约，扫一眼便知make.sh大概在$GOROOT/src下，打开make.sh，我们在文件头处看到如下一些内容：

# Environment variables that control make.bash:

#

# GOROOT_FINAL: The expected final Go root, baked into binaries.

# The default is the location of the Go tree during the build.

#

# GOHOSTARCH: The architecture for host tools (compilers and

# binaries). Binaries of this type must be executable on the current

# system, so the only common reason to set this is to set

# GOHOSTARCH=386 on an amd64 machine.

#

# GOARCH: The target architecture for installed packages and tools.

#

# GOOS: The target operating system for installed packages and tools.

… …

make.bash头并未简要说明文件的用途，但名为make.xx的文件想必是用来构建Go编译工具的。这里提到几个环境变量可以控制 make.bash的行为，显然GOARCH和GOOS更能引起我们的兴趣。我们再回过头来输出testport.go编译过程的详细信息：

$ go build -x -o testport_linux testport.go

WORK=/tmp/go-build286732099

mkdir -p $WORK/command-line-arguments/_obj/

cd /home/tonybai/Test/Go/porting

/usr/local/go/pkg/tool/linux_amd64/6g -o $WORK/command-line-arguments.a -trimpath $WORK -p command-line-arguments -complete -D _/home/tonybai/Test/Go/porting -I $WORK -pack ./testport.go

cd .

/usr/local/go/pkg/tool/linux_amd64/6l -o testport_linux -L $WORK -extld=gcc $WORK/command-line-arguments.a

我们发现Go实际上用的是$GOROOT/pkg/tool/linux_amd64下的6g（编译器）和6l（链接器）来完成整个编译过程的，看到6g 和6l所在目录名为linux_amd64，我们可以大胆猜测编译darwin/amd64 go程序应该使用的是$GOROOT/pkg/tool/darwin_amd64下的工具。不过在我在$GOROOT/pkg/tool下没有发现 darwin_amd64目录，也就是说我们通过安装包安装的Go仅自带了for linux_amd64的编译工具，要想交叉编译出for darwin_amd64的程序，我们需要通过make.bash来手工编译出这些工具。

tonybai@ubuntu-Server-14:/usr/local/go/pkg$ ls

linux_amd64 linux_amd64_race obj tool

tonybai@ubuntu-Server-14:/usr/local/go/pkg/tool$ ls

linux_amd64

根据前面make.bash的用法说明，我们来尝试构建一下：

cd $GOROOT/src

sudo GOOS=darwin GOARCH=amd64 ./make.bash

# Building C bootstrap tool.

cmd/dist

# Building compilers and Go bootstrap tool for host, linux/amd64.

… …

cmd/cc

cmd/gc

cmd/6l

cmd/6a

cmd/6c

cmd/6g

pkg/runtime

… …

cmd/go

pkg/runtime (darwin/amd64)

# Building packages and commands for host, linux/amd64.

runtime

… …

text/scanner

# Building packages and commands for darwin/amd64.

runtime

errors

… …

testing/quick

text/scanner

—

Installed Go for darwin/amd64 in /usr/local/go

Installed commands in /usr/local/go/bin

编译后，我们再来试试编译for darwin_amd64的程序：

$ GOOS=darwin GOARCH=amd64 go build -x -o testport_darwin testport.go

WORK=/tmp/go-build972764136

mkdir -p $WORK/command-line-arguments/_obj/

cd /home/tonybai/Test/Go/porting

/usr/local/go/pkg/tool/linux_amd64/6g -o $WORK/command-line-arguments.a -trimpath $WORK -p command-line-arguments -complete -D _/home/tonybai/Test/Go/porting -I $WORK -pack ./testport.go

cd .

/usr/local/go/pkg/tool/linux_amd64/6l -o testport_darwin -L $WORK -extld=gcc $WORK/command-line-arguments.a

将文件copy到我的Mac Air下执行：

$chmod +x testport_darwin

$testport_darwin

I am running on Darwin TonydeMacBook-Air.local 13.1.0 Darwin Kernel Version 13.1.0: Thu Jan 16 19:40:37 PST 2014; root:xnu-2422.90.20~2/RELEASE_X86_64 x86_64

编译虽然成功了，但从-x输出的详细编译过程来看，Go编译连接使用的工具依旧是linux_amd64下的6g和6l，为什么没有使用darwin_amd64下的6g和6l呢？原来$GOROOT/pkg/tool/darwin_amd64下根本就没有6g和6l：

/usr/local/go/pkg/tool/darwin_amd64$ ls

addr2line cgo fix nm objdump pack yacc

但查看一下pkg/tool/linux_amd64/下程序的更新时间：

/usr/local/go/pkg/tool/linux_amd64$ ls -l

… …

-rwxr-xr-x 1 root root 2482877 10月 20 15:12 6g

-rwxr-xr-x 1 root root 1186445 10月 20 15:12 6l

… …

我们发现6g和6l都是被刚才的make.bash新编译出来的，我们可以得出结论：新6g和新6l目前既可以编译本地程序（linux/amd64)，也可以编译darwin/amd64下的程序了，例如重新编译testport_linux依旧ok：

$ go build -x -o testport_linux testport.go

WORK=/tmp/go-build636762567

mkdir -p $WORK/command-line-arguments/_obj/

cd /home/tonybai/Test/Go/porting

/usr/local/go/pkg/tool/linux_amd64/6g -o $WORK/command-line-arguments.a -trimpath $WORK -p command-line-arguments -complete -D _/home/tonybai/Test/Go/porting -I $WORK -pack ./testport.go

cd .

/usr/local/go/pkg/tool/linux_amd64/6l -o testport_linux -L $WORK -extld=gcc $WORK/command-line-arguments.a

如果我们还想给Go编译器加上交叉编译windows/amd64程序的功能，我们再执行一次make.bash：

sudo GOOS=windows GOARCH=amd64 ./make.bash

编译成功后，我们来编译一下Windows程序：

$ GOOS=windows GOARCH=amd64 go build -x -o testport_windows.exe testport.go

WORK=/tmp/go-build626615350

mkdir -p $WORK/command-line-arguments/_obj/

cd /home/tonybai/Test/Go/porting

/usr/local/go/pkg/tool/linux_amd64/6g -o $WORK/command-line-arguments.a -trimpath $WORK -p command-line-arguments -complete -D _/home/tonybai/Test/Go/porting -I $WORK -pack ./testport.go

cd .

/usr/local/go/pkg/tool/linux_amd64/6l -o testport_windows.exe -L $WORK -extld=gcc $WORK/command-line-arguments.a

把testport_windows.exe扔到Windows上执行，结果：

Err when executing uname command

显然Windows下没有uname命令，提示执行出错。

至此，我的Go编译器具备了在Linux下编译windows/amd64和darwin/amd64的能力。如果你还想增加其他平台的能力，就像上面那样操作执行make.bash即可。

如果在go源文件中有与C语言的交互代码，那么交叉编译功能是否还能奏效呢？毕竟C在各个平台上的运行库、链接库等都是不同的。我们先来看看这个例子，我们使用之前在《[探讨docker容器对共享内存的支持情况](http://tonybai.com/2014/10/12/discussion-on-shared-mem-support-in-docker/)》一文中的一个例子：

//testport_cgoenabled.go

package main

//#include <stdio.h>

//#include <sys/types.h>

//#include <sys/mman.h>

//#include <fcntl.h>

//

//#define SHMSZ 27

//

//int shm_rd()

//{

// char c;

// char *shm = NULL;

// char *s = NULL;

// int fd;

// if ((fd = open("./shm.txt", O_RDONLY)) == -1) {

// return -1;

// }

//

// shm = (char*)mmap(shm, SHMSZ, PROT_READ, MAP_SHARED, fd, 0);

// if (!shm) {

// return -2;

// }

//

// close(fd);

// s = shm;

// int i = 0;

// for (i = 0; i < SHMSZ – 1; i++) {

// printf("%c ", *(s + i));

// }

// printf("\n");

//

// return 0;

//}

import "C"

import "fmt"

func main() {

i := C.shm_rd()

if i != 0 {

fmt.Println("Mmap Share Memory Read Error:", i)

return

}

fmt.Println("Mmap Share Memory Read Ok")

}

我们先编译出一个本地可运行的程序：

$ go build -x -o testport_cgoenabled_linux testport_cgoenabled.go

WORK=/tmp/go-build977176241

mkdir -p $WORK/command-line-arguments/_obj/

cd /home/tonybai/Test/Go/porting

CGO_LDFLAGS="-g" "-O2" /usr/local/go/pkg/tool/linux_amd64/cgo -objdir $WORK/command-line-arguments/_obj/ — -I $WORK/command-line-arguments/_obj/ testport_cgoenabled.go

/usr/local/go/pkg/tool/linux_amd64/6c -F -V -w -trimpath $WORK -I $WORK/command-line-arguments/_obj/ -I /usr/local/go/pkg/linux_amd64 -o $WORK/command-line-arguments/_obj/_cgo_defun.6 -D GOOS_linux -D GOARCH_amd64 $WORK/command-line-arguments/_obj/_cgo_defun.c

gcc -I . -fPIC -m64 -pthread -fmessage-length=0 -print-libgcc-file-name

gcc -I . -fPIC -m64 -pthread -fmessage-length=0 -I $WORK/command-line-arguments/_obj/ -g -O2 -o $WORK/command-line-arguments/_obj/_cgo_main.o -c $WORK/command-line-arguments/_obj/_cgo_main.c

gcc -I . -fPIC -m64 -pthread -fmessage-length=0 -I $WORK/command-line-arguments/_obj/ -g -O2 -o $WORK/command-line-arguments/_obj/_cgo_export.o -c $WORK/command-line-arguments/_obj/_cgo_export.c

gcc -I . -fPIC -m64 -pthread -fmessage-length=0 -I $WORK/command-line-arguments/_obj/ -g -O2 -o $WORK/command-line-arguments/_obj/testport_cgoenabled.cgo2.o -c $WORK/command-line-arguments/_obj/testport_cgoenabled.cgo2.c

gcc -I . -fPIC -m64 -pthread -fmessage-length=0 -o $WORK/command-line-arguments/_obj/_cgo_.o $WORK/command-line-arguments/_obj/_cgo_main.o $WORK/command-line-arguments/_obj/_cgo_export.o $WORK/command-line-arguments/_obj/testport_cgoenabled.cgo2.o -g -O2

/usr/local/go/pkg/tool/linux_amd64/cgo -objdir $WORK/command-line-arguments/_obj/ -dynimport $WORK/command-line-arguments/_obj/_cgo_.o -dynout $WORK/command-line-arguments/_obj/_cgo_import.c

/usr/local/go/pkg/tool/linux_amd64/6c -F -V -w -trimpath $WORK -I $WORK/command-line-arguments/_obj/ -I /usr/local/go/pkg/linux_amd64 -o $WORK/command-line-arguments/_obj/_cgo_import.6 -D GOOS_linux -D GOARCH_amd64 $WORK/command-line-arguments/_obj/_cgo_import.c

gcc -I . -fPIC -m64 -pthread -fmessage-length=0 -o $WORK/command-line-arguments/_obj/_all.o $WORK/command-line-arguments/_obj/_cgo_export.o $WORK/command-line-arguments/_obj/testport_cgoenabled.cgo2.o -g -O2 -Wl,-r -nostdlib /usr/lib/gcc/x86_64-linux-gnu/4.8/libgcc.a

/usr/local/go/pkg/tool/linux_amd64/6g -o $WORK/command-line-arguments.a -trimpath $WORK -p command-line-arguments -D _/home/tonybai/Test/Go/porting -I $WORK -pack $WORK/command-line-arguments/_obj/_cgo_gotypes.go $WORK/command-line-arguments/_obj/testport_cgoenabled.cgo1.go

pack r $WORK/command-line-arguments.a $WORK/command-line-arguments/_obj/_cgo_import.6 $WORK/command-line-arguments/_obj/_cgo_defun.6 $WORK/command-line-arguments/_obj/_all.o # internal

cd .

/usr/local/go/pkg/tool/linux_amd64/6l -o testport_cgoenabled_linux -L $WORK -extld=gcc $WORK/command-line-arguments.a

输出了好多日志！不过可以看出Go编译器先调用CGO对Go源码中的C代码进行了编译，然后才是常规的Go编译，最后通过6l链接在一起。Cgo似乎直接使用了Gcc。我们再来试试跨平台编译：

$ GOOS=darwin GOARCH=amd64 go build -x -o testport_cgoenabled_darwin testport_cgoenabled.go

WORK=/tmp/go-build124869433

can't load package: no buildable Go source files in /home/tonybai/Test/Go/porting

当我们编译for Darwin/amd64平台的程序时，Go无法像之前那样的顺利完成编译，而是提示错误。从网上给出的资料来看，如果Go源码中包含C互操作代码，那么 目前依旧无法实现交叉编译，因为cgo会直接使用各个平台的本地c编译器去编译Go文件中的C代码。默认情况下，make.bash会置 CGO_ENABLED=0。

如果你非要将CGO_ENABLED设置为1去编译go的话，至少我得到了如下错误，导致无法编译通过：

$ sudo CGO_ENABLED=1 GOOS=darwin GOARCH=amd64 ./make.bash –no-clean

… …

# Building packages and commands for darwin/amd64.

… …

37: error: 'AI_MASK' undeclared (first use in this function)


© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

您好，您这边文章中提到“如果Go源码中包含C互操作代码，那么 目前依旧无法实现交叉编译”， 目前现在依然如此吗，我现在在尝试编译android平台能用的so库，我的命令也是跟您差不多：GOOS=android GOARCH=arm go build -buildmode=c-shared -o=libgojni.so，提示can’t load package，我的go代码中也是import了C库，应该就是这个import导致的问题，我接着又尝试了“CGO_ENABLED=1 GOOS=android GOARCH=arm go build -buildmode=c-shared -o=libgojni.so”，错误成了“clang: error: argument unused during compilation: ‘-mno-thumb’ [-Werror,-Wunused-command-line-argument]”，我是现在才接触的go，我下载的时候go已经是1.9几的版本了，现在依然没有办法解决这个问题吗？虚心求教，这个问题困扰我两三天了，求解

从go程序编译的原理上讲，目前如果代码这种使用了cgo，依然无法时间交叉编译。因为你在macos上或linux上编译目标平台是arm的android版本的go程序，cgo_enabled=0 时，编译器要resolve你代码中的c代码的的各种符号以及相关syscall。但是在macos或linux根本没有对应的.a或.so文件。cgo_enabled=1的情况下，go compiler会自动选择external linking的机制，即会调用系统默认的c compiler去编译那部分c代码。你的第二种情况的错误输出就是这个情况：go compiler调用了clang去编译c代码时报错了。建议你在看看我的这篇文章：http://tonybai.com/2017/06/27/an-intro-about-go-portability