---
title: Go编译的几个细节，连专家也要停下来想想
url: https://tonybai.com/2024/11/11/some-details-about-go-compilation/
published: '2024-11-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go编译的几个细节，连专家也要停下来想想

![](../../assets/e51b318b5c065a13.png)


[本文永久链接](https://tonybai.com/2024/11/11/some-details-about-go-compilation) – https://tonybai.com/2024/11/11/some-details-about-go-compilation

在Go开发中，编译相关的问题看似简单，但实则蕴含许多细节。有时，即使是Go专家也需要停下来，花时间思考答案或亲自验证。本文将通过几个具体问题，和大家一起探讨Go编译过程中的一些你可能之前未曾关注的细节。

注：本文示例使用的环境为

[Go 1.23.0]、Linux Kernel 3.10.0和CentOS 7.9。

## 1. Go编译默认采用静态链接还是动态链接？

我们来看第一个问题：Go编译默认采用静态链接还是动态链接呢？

很多人脱口而出：[动态链接](https://tonybai.com/2011/07/07/also-talk-about-shared-library-2/)，因为CGO_ENABLED默认值为1，即开启Cgo。也有些人会说：“其实Go编译器默认是静态链接的，只有在使用C语言库时才会动态链接”。那么到底哪个是正确的呢？

我们来看一个具体的示例。但在这之前，我们要承认一个事实，那就是CGO_ENABLED默认值为1，你可以通过下面命令来验证这一点：

```
$go env|grep CGO_ENABLED
CGO_ENABLED='1'
```


验证Go默认究竟是哪种链接，我们写一个hello, world的Go程序即可：

```
// go-compilation/main.go
package main
import "fmt"
func main() {
fmt.Println("hello, world")
}
```


构建该程序：

```
$go build -o helloworld-default main.go
```


之后，我们查看一下生成的可执行文件helloworld-default的文件属性：

```
$file helloworld-default
helloworld-default: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
$ldd helloworld-default
不是动态可执行文件
```


我们看到，虽然CGO_ENABLED=1，但默认情况下，Go构建出的helloworld程序是静态链接的(statically linked)。

那么默认情况下，Go编译器是否都会采用静态链接的方式来构建Go程序呢？我们给上面的main.go添加一行代码：

```
// go-compilation/main-with-os-user.go
package main
import (
"fmt"
_ "os/user"
)
func main() {
fmt.Println("hello, world")
}
```


和之前的hello, world不同的是，这段代码多了一行**包的空导入**，导入的是os/user这个包。

编译这段代码，我们得到helloworld-with-os-user可执行文件。

```
$go build -o helloworld-with-os-user main-with-os-user.go
```


使用file和ldd检视文件helloworld-with-os-user：

```
$file helloworld-with-os-user
helloworld-with-os-user: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), not stripped
$ldd helloworld-with-os-user
linux-vdso.so.1 => (0x00007ffcb8fd4000)
libpthread.so.0 => /lib64/libpthread.so.0 (0x00007fb5d6fce000)
libc.so.6 => /lib64/libc.so.6 (0x00007fb5d6c00000)
/lib64/ld-linux-x86-64.so.2 (0x00007fb5d71ea000)
```


我们看到：**一行新代码居然让helloworld从静态链接变为了动态链接**，同时这也是如何编译出一个hello world版的动态链接Go程序的答案。

通过nm命令我们还可以查看Go程序依赖了哪些C库的符号：

```
$nm -a helloworld-with-os-user |grep " U "
U abort
U __errno_location
U fprintf
U fputc
U free
U fwrite
U malloc
U mmap
U munmap
U nanosleep
U pthread_attr_destroy
U pthread_attr_getstack
U pthread_attr_getstacksize
U pthread_attr_init
U pthread_cond_broadcast
U pthread_cond_wait
U pthread_create
U pthread_detach
U pthread_getattr_np
U pthread_key_create
U pthread_mutex_lock
U pthread_mutex_unlock
U pthread_self
U pthread_setspecific
U pthread_sigmask
U setenv
U sigaction
U sigaddset
U sigemptyset
U sigfillset
U sigismember
U stderr
U strerror
U unsetenv
U vfprintf
```


由此，我们可以得到一个结论，在默认情况下(CGO_ENABLED=1)，Go会尽力使用静态链接的方式，但在某些情况下，会采用动态链接。那么究竟在哪些情况下会默认生成动态链接的程序呢？我们继续往下看。

## 2. 在何种情况下默认会生成动态链接的Go程序？

在以下几种情况下，Go编译器会默认(CGO_ENABLED=1)生成动态链接的可执行文件，我们逐一来看一下。

### 2.1 一些使用C实现的标准库包

根据上述示例，我们可以看到，在某些情况下，即使只依赖标准库，Go 仍会在CGO_ENABLED=1的情况下采用动态链接。这是因为代码依赖的标准库包使用了C版本的实现。虽然这种情况并不常见，但[os/user包](https://pkg.go.dev/os/user)和[net包](https://pkg.go.dev/net)是两个典型的例子。

os/user包的示例在前面我们已经见识过了。user包允许开发者通过名称或ID查找用户账户。对于大多数Unix系统(包括linux)，该包内部有两种版本的实现，用于解析用户和组ID到名称，并列出附加组ID。一种是用纯Go编写，解析/etc/passwd和/etc/group文件。另一种是基于cgo的，依赖于标准C库（libc）中的例程，如getpwuid_r、getgrnam_r和getgrouplist。当cgo可用(CGO_ENABLED=1)，并且特定平台的libc实现了所需的例程时，将使用基于cgo的（libc支持的）代码，即采用动态链接方式。

同样，net包在名称解析(Name Resolution，即域名或主机名对应IP查找)上针对大多数Unix系统也有两个版本的实现：一个是纯Go版本，另一个是基于C的版本。C版本会在cgo可用且特定平台实现了相关C函数(比如getaddrinfo和getnameinfo等)时使用。

下面是一个简单的使用net包并采用动态链接的示例：

```
// go-compilation/main-with-net.go
package main
import (
"fmt"
_ "net"
)
func main() {
fmt.Println("hello, world")
}
```


编译后，我们查看一下文件属性：

```
$go build -o helloworld-with-net main-with-net.go
$file helloworld-with-net
helloworld-with-net: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), not stripped
$ldd helloworld-with-net
linux-vdso.so.1 => (0x00007ffd75dfd000)
libresolv.so.2 => /lib64/libresolv.so.2 (0x00007fdda2cf9000)
libpthread.so.0 => /lib64/libpthread.so.0 (0x00007fdda2add000)
libc.so.6 => /lib64/libc.so.6 (0x00007fdda270f000)
/lib64/ld-linux-x86-64.so.2 (0x00007fdda2f13000)
```


我们看到C版本实现依赖了libresolv.so这个用于名称解析的C库。

由此可得，当Go在默认cgo开启时，一旦依赖了标准库中拥有C版本实现的包，比如os/user、net等，Go编译器会采用动态链接的方式编译Go可执行程序。

### 2.2 显式使用cgo调用外部C程序

如果使用cgo与外部C代码交互，那么生成的可执行文件必然会包含动态链接。下面我们来看一个调用cgo的简单示例。

首先，建立一个简单的C lib：

```
// go-compilation/my-c-lib
$tree my-c-lib
my-c-lib
├── Makefile
├── mylib.c
└── mylib.h
// go-compilation/my-c-lib/Makefile
.PHONY: all static
all:
gcc -c -fPIC -o mylib.o mylib.c
gcc -shared -o libmylib.so mylib.o
static:
gcc -c -fPIC -o mylib.o mylib.c
ar rcs libmylib.a mylib.o
// go-compilation/my-c-lib/mylib.h
#ifndef MYLIB_H
#define MYLIB_H
void hello();
int add(int a, int b);
#endif // MYLIB_H
// go-compilation/my-c-lib/mylib.c
#include <stdio.h>
void hello() {
printf("Hello from C!\n");
}
int add(int a, int b) {
return a + b;
}
```


执行make all构建出动态链接库libmylib.so！接下来，我们编写一个Go程序通过cgo调用libmylib.so中：

```
// go-compilation/main-with-call-myclib.go
package main
/*
#cgo CFLAGS: -I ./my-c-lib
#cgo LDFLAGS: -L ./my-c-lib -lmylib
#include "mylib.h"
*/
import "C"
import "fmt"
func main() {
// 调用 C 函数
C.hello()
// 调用 C 中的加法函数
result := C.add(3, 4)
fmt.Printf("Result of addition: %d\n", result)
}
```


编译该源码：

```
$go build -o helloworld-with-call-myclib main-with-call-myclib.go
```


通过ldd可以看到，可执行文件helloworld-with-call-myclib是动态链接的，并依赖libmylib.so：

```
$ldd helloworld-with-call-myclib
linux-vdso.so.1 => (0x00007ffcc39d8000)
libmylib.so => not found
libpthread.so.0 => /lib64/libpthread.so.0 (0x00007f7166df5000)
libc.so.6 => /lib64/libc.so.6 (0x00007f7166a27000)
/lib64/ld-linux-x86-64.so.2 (0x00007f7167011000)
```


设置LD_LIBRARY_PATH(为了让程序找到libmylib.so)并运行可执行文件helloworld-with-call-myclib：

```
$ LD_LIBRARY_PATH=./my-c-lib:$LD_LIBRARY_PATH ./helloworld-with-call-myclib
Hello from C!
Result of addition: 7
```


### 2.3 使用了依赖cgo的第三方包

在日常开发中，我们经常依赖一些第三方包，有些时候这些第三方包依赖cgo，比如[mattn/go-sqlite3](https://github.com/mattn/go-sqlite3)。下面就是一个依赖go-sqlite3包的示例：

```
// go-compilation/go-sqlite3/main.go
package main
import (
"database/sql"
"fmt"
"log"
_ "github.com/mattn/go-sqlite3"
)
func main() {
// 打开数据库（如果不存在，则创建）
db, err := sql.Open("sqlite3", "./test.db")
if err != nil {
log.Fatal(err)
}
defer db.Close()
// 创建表
sqlStmt := `CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);`
_, err = db.Exec(sqlStmt)
if err != nil {
log.Fatalf("%q: %s\n", err, sqlStmt)
}
// 插入数据
_, err = db.Exec(`INSERT INTO user (name) VALUES (?)`, "Alice")
if err != nil {
log.Fatal(err)
}
// 查询数据
rows, err := db.Query(`SELECT id, name FROM user;`)
if err != nil {
log.Fatal(err)
}
defer rows.Close()
for rows.Next() {
var id int
var name string
err = rows.Scan(&id, &name)
if err != nil {
log.Fatal(err)
}
fmt.Printf("%d: %s\n", id, name)
}
// 检查查询中的错误
if err = rows.Err(); err != nil {
log.Fatal(err)
}
}
```


编译和运行该源码：

```
$go build demo
$ldd demo
linux-vdso.so.1 => (0x00007ffe23d8e000)
libdl.so.2 => /lib64/libdl.so.2 (0x00007faf0ddef000)
libpthread.so.0 => /lib64/libpthread.so.0 (0x00007faf0dbd3000)
libc.so.6 => /lib64/libc.so.6 (0x00007faf0d805000)
/lib64/ld-linux-x86-64.so.2 (0x00007faf0dff3000)
$./demo
1: Alice
```


到这里，有些读者可能会问一个问题：如果需要在上述依赖场景中生成静态链接的Go程序，该怎么做呢？接下来，我们就来看看这个问题的解决细节。

## 3. 如何在上述情况下实现静态链接？

到这里是不是有些烧脑了啊！我们针对上一节的三种情况，分别对应来看一下静态编译的方案。

### 3.1 仅依赖标准包

在前面我们说过，之所以在使用os/user、net包时会在默认情况下采用动态链接，是因为Go使用了这两个包对应功能的C版实现，如果要做静态编译，让Go编译器选择它们的纯Go版实现即可。那我们仅需要关闭CGO即可，以依赖标准库os/user为例：

```
$CGO_ENABLED=0 go build -o helloworld-with-os-user-static main-with-os-user.go
$file helloworld-with-os-user-static
helloworld-with-os-user-static: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
$ldd helloworld-with-os-user-static
不是动态可执行文件
```


### 3.2 使用cgo调用外部c程序（静态链接）

对于依赖cgo调用外部c的程序，我们要使用静态链接就必须要求外部c库提供静态库，因此，我们需要my-c-lib提供一份libmylib.a，这通过下面命令可以实现(或执行make static)：

```
$gcc -c -fPIC -o mylib.o mylib.c
$ar rcs libmylib.a mylib.o
```


有了libmylib.a后，我们还要让Go程序静态链接该.a文件，于是我们需要修改一下Go源码中cgo链接的flag，加上静态链接的选项：

```
// go-compilation/main-with-call-myclib-static.go
... ...
#cgo LDFLAGS: -static -L my-c-lib -lmylib
... ...
```


编译链接并查看一下文件属性：

```
$go build -o helloworld-with-call-myclib-static main-with-call-myclib-static.go
$file helloworld-with-call-myclib-static
helloworld-with-call-myclib-static: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 2.6.32, BuildID[sha1]=b3da3ed817d0d04230460069b048cab5f5bfc3b9, not stripped
```


我们得到了预期的结果！

### 3.3 依赖使用cgo的外部go包（静态链接）

最麻烦的是这类情况，要想实现静态链接，我们需要找出外部go依赖的所有c库的.a文件(静态共享库)。以我们的go-sqlite3示例为例，go-sqlite3是sqlite库的go binding，它依赖sqlite库，同时所有第三方c库都依赖libc，我们还要准备一份libc的.a文件，下面我们就先安装这些：

```
$yum install -y gcc glibc-static sqlite-devel
... ...
已安装:
sqlite-devel.x86_64 0:3.7.17-8.el7_7.1
更新完毕:
glibc-static.x86_64 0:2.17-326.el7_9.3
```


接下来，我们就来以静态链接的方式在go-compilation/go-sqlite3-static下编译一下：

```
$go build -tags 'sqlite_omit_load_extension' -ldflags '-linkmode external -extldflags "-static"' demo
$file ./demo
./demo: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 2.6.32, BuildID[sha1]=c779f5c3eaa945d916de059b56d94c23974ce61c, not stripped
```


这里命令行中的-tags ‘sqlite_omit_load_extension’用于禁用SQLite3的动态加载功能，确保更好的静态链接兼容性。而-ldflags ‘-linkmode external -extldflags “-static”‘的含义是使用外部链接器(比如gcc linker)，并强制静态链接所有库。

我们再看完略烧脑的几个细节后，再来看一个略轻松的话题。

## 4. Go编译出的可执行文件过大，能优化吗？

Go编译出的二进制文件一般较大，一个简单的“Hello World”程序通常在2MB左右：

```
$ls -lh helloworld-default
-rwxr-xr-x 1 root root 2.1M 11月 3 10:39 helloworld-default
```


这一方面是因为Go将整个runtime都编译到可执行文件中了，另一方面也是因为Go静态编译所致。那么在默认情况下，Go二进制文件的大小还有优化空间么？方法不多，有两种可以尝试：

- 去除符号表和调试信息

在编译时使用-ldflags=”-s -w”标志可以去除符号表和调试符号，其中-s用于去掉符号表和调试信息，-w用于去掉DWARF调试信息，这样能显著减小文件体积。以helloworld为例，可执行文件的size减少了近四成：

```
$go build -ldflags="-s -w" -o helloworld-default-nosym main.go
$ls -l
-rwxr-xr-x 1 root root 2124504 11月 3 10:39 helloworld-default
-rwxr-xr-x 1 root root 1384600 11月 3 13:34 helloworld-default-nosym
```


- 使用tinygo

[TinyGo](https://github.com/tinygo-org/tinygo/)是一个Go语言的编译器，它专为资源受限的环境而设计，例如微控制器、WebAssembly和其他嵌入式设备。TinyGo的目标是提供一个轻量级的、能在小型设备上运行的Go运行时，同时尽可能支持Go语言的特性。tinygo的一大优点就是生成的二进制文件通常比标准Go编译器生成的文件小得多：

```
$tinygo build -o helloworld-tinygo main.go
$ls -l
总用量 2728
-rwxr-xr-x 1 root root 2128909 11月 5 05:43 helloworld-default*
-rwxr-xr-x 1 root root 647600 11月 5 05:45 helloworld-tinygo*
```


我们看到：tinygo生成的可执行文件的size仅是原来的30%。

注：虽然TinyGo在特定场景（如IoT和嵌入式开发）中非常有用，但在常规服务器环境中，由于生态系统兼容性、性能、调试支持等方面的限制，可能并不是最佳选择。对于需要高并发、复杂功能和良好调试支持的应用，标准Go仍然是更合适的选择。

注：这里使用的tinygo为0.34.0版本。


## 5. 未使用的符号是否会被编译到Go二进制文件中？

到这里，相信读者心中也都会萦绕一些问题：到底哪些符号被编译到最终的Go二进制文件中了呢？未使用的符号是否会被编译到Go二进制文件中吗？在这一小节中，我们就来探索一下。

出于对Go的了解，我们已经知道无论是GOPATH时代，还是Go module时代，Go的编译单元始终是包(package)，一个包（无论包中包含多少个Go源文件）都会作为一个编译单元被编译为一个目标文件(.a)，然后Go链接器会将多个目标文件链接在一起生成可执行文件，因此如果一个包被依赖，那么它就会进入到Go二进制文件中，它内部的符号也会进入到Go二进制文件中。

那么问题来了！是否被依赖包中的所有符号都会被放到最终的可执行文件中呢？我们以最简单的helloworld-default为例，它依赖fmt包，并调用了fmt包的Println函数，我们看看Println这个符号是否会出现在最终的可执行文件中：

```
$nm -a helloworld-default | grep "Println"
000000000048eba0 T fmt.(*pp).doPrintln
```


居然没有！我们初步怀疑是inline优化在作祟。接下来，关闭优化再来试试：

```
$go build -o helloworld-default-noinline -gcflags='-l -N' main.go
$nm -a helloworld-default-noinline | grep "Println"
000000000048ec00 T fmt.(*pp).doPrintln
0000000000489ee0 T fmt.Println
```


看来的确如此！不过当使用”fmt.”去过滤helloworld-default-noinline的所有符号时，我们发现fmt包的一些常见的符号并未包含在其中，比如Printf、Fprintf、Scanf等。

这是因为Go编译器的一个重要特性：死码消除(dead code elimination)，即编译器会将未使用的代码和数据从最终的二进制文件中剔除。

我们再来继续探讨一个衍生问题：如果Go源码使用空导入方式导入了一个包，那么这个包是否会被编译到Go二进制文件中呢？其实道理是一样的，如果用到了里面的符号，就会存在，否则不会。

以空导入os/user为例，即便在CGO_ENABLED=0的情况下，因为没有使用os/user中的任何符号，在最终的二进制文件中也不会包含user包：

```
$CGO_ENABLED=0 go build -o helloworld-with-os-user-noinline -gcflags='-l -N' main-with-os-user.go
[root@iZ2ze18rmx2avqb5xgb4omZ helloworld]# nm -a helloworld-with-os-user-noinline |grep user
0000000000551ac0 B runtime.userArenaState
```


但是如果是带有init函数的包，且init函数中调用了同包其他符号的情况呢？我们以expvar包为例看一下：

```
// go-compilation/main-with-expvar.go
package main
import (
_ "expvar"
"fmt"
)
func main() {
fmt.Println("hello, world")
}
```


编译并查看一下其中的符号：

```
$go build -o helloworld-with-expvar-noinline -gcflags='-l -N' main-with-expvar.go
$nm -a helloworld-with-expvar-noinline|grep expvar
0000000000556480 T expvar.appendJSONQuote
00000000005562e0 T expvar.cmdline
00000000005561c0 T expvar.expvarHandler
00000000005568e0 T expvar.(*Func).String
0000000000555ee0 T expvar.Func.String
00000000005563a0 T expvar.init.0
00000000006e0560 D expvar..inittask
0000000000704550 d expvar..interfaceSwitch.0
... ...
```


除此之外，如果一个包即便没有init函数，但有需要初始化的全局变量，比如crypto包的hashes：

```
// $GOROOT/src/crypto/crypto.go
var hashes = make([]func() hash.Hash, maxHash)
```


crypto包的相关如何也会进入最终的可执行文件中，大家自己动手不妨试试。下面是我得到的一些输出：

```
$go build -o helloworld-with-crypto-noinline -gcflags='-l -N' main-with-crypto.go
$nm -a helloworld-with-crypto-noinline|grep crypto
00000000005517b0 B crypto.hashes
000000000048ee60 T crypto.init
0000000000547280 D crypto..inittask
```


有人会问：os/user包也有一些全局变量啊，为什么这些符号没有被包含在可执行文件中呢？比如：

```
// $GOROOT/src/os/user/user.go
var (
userImplemented = true
groupImplemented = true
groupListImplemented = true
)
```


这就要涉及Go包初始化的逻辑了。我们看到crypto包包含在可执行文件中的符号中有crypto.init和crypto..inittask这两个符号，显然这不是crypto包代码中的符号，而是Go编译器为crypto包自动生成的init函数和inittask结构。

Go编译器会为每个包生成一个init函数，即使包中没有显式定义init函数，同时[每个包都会有一个inittask结构](https://go.dev/src/cmd/compile/internal/pkginit/init.go)，用于运行时的包初始化系统。当然这么说也不足够精确，如果一个包没有init函数、需要初始化的全局变量或其他需要运行时初始化的内容，则编译器不会为其生成init函数和inittask。比如上面的os/user包。

os/user包确实有上述全局变量的定义，但是这些变量是在编译期就可以确定值的常量布尔值，而且未被包外引用或在包内用于影响控制流。Go编译器足够智能，能够判断出这些初始化是”无副作用的”，不需要在运行时进行初始化。只有真正需要运行时初始化的包才会生成init和inittask。这也解释了为什么空导入os/user包时没有相关的init和inittask符号，而crypto、expvar包有的init.0和inittask符号。

## 6. 如何快速判断Go项目是否依赖cgo？

在使用开源Go项目时，我们经常会遇到项目文档中没有明确说明是否依赖Cgo的情况。这种情况下，如果我们需要在特定环境（比如CGO_ENABLED=0）下使用该项目，就需要事先判断项目是否依赖Cgo，有些时候还要快速地给出判断。

那究竟是否可以做到这种快速判断呢？我们先来看看一些常见的作法。

第一类作法是源码层面的静态分析。最直接的方式是检查源码中是否存在import “C”语句，这种引入方式是CGO使用的显著标志。

```
// 在项目根目录中执行
$grep -rn 'import "C"' .
```


这个命令会递归搜索当前目录下所有文件，显示包含import “C”的行号和文件路径，帮助快速定位CGO的使用位置。

此外，CGO项目通常包含特殊的编译指令，这些指令以注释形式出现在源码中，比如前面见识过的#cgo CFLAGS、#cgo LDFLAGS等，通过对这些编译指令的检测，同样可以来判断项目是否依赖CGO。

不过第一类作法并不能查找出Go项目的依赖包是否依赖cgo。而找出直接依赖或间接依赖是否依赖cgo，我们需要工具帮忙，比如使用Go工具链提供的命令分析项目依赖：

```
$go list -deps -f '{{.ImportPath}}: {{.CgoFiles}}' ./... | grep -v '\[\]'
```


其中ImportPath是依赖包的导入路径，而CgoFiles则是依赖中包含import “C”的Go源文件。我们以go-sqlite3那个依赖cgo的示例来验证一下：

```
// cd go-compilation/go-sqlite3
$go list -deps -f '{{.ImportPath}}: {{.CgoFiles}}' ./... | grep -v '\[\]'
runtime/cgo: [cgo.go]
github.com/mattn/go-sqlite3: [backup.go callback.go error.go sqlite3.go sqlite3_context.go sqlite3_load_extension.go sqlite3_opt_serialize.go sqlite3_opt_userauth_omit.go sqlite3_other.go sqlite3_type.go]
```


用空导入os/user的示例再来看一下：

```
$go list -deps -f '{{.ImportPath}}: {{.CgoFiles}}' main-with-os-user.go | grep -v '\[\]'
runtime/cgo: [cgo.go]
os/user: [cgo_lookup_cgo.go getgrouplist_unix.go]
```


我们知道os/user有纯go和C版本两个实现，因此上述判断只能说“对了一半”，当我关闭CGO_ENABLED时，Go编译器不会使用基于cgo的C版实现。

那是否在禁用cgo的前提下对源码进行一次编译便能验证项目是否对cgo有依赖呢？这样做显然谈不上是一种“快速”的方法，那是否有效呢？我们来对上面的go-sqlite3项目做一个测试，我们在关闭CGO_ENABLED时，编译一下该示例：

```
// cd go-compilation/go-sqlite3
$ CGO_ENABLED=0 go build demo
```


我们看到，Go编译器并未报错！似乎该项目不需要cgo! 但真的是这样吗？我们运行一下编译后的demo可执行文件：

```
$ ./demo
2024/11/03 22:10:36 "Binary was compiled with 'CGO_ENABLED=0', go-sqlite3 requires cgo to work. This is a stub": CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);
```


我们看到成功编译出来的程序居然出现运行时错误，提示需要cgo！

到这里，没有一种方法可以快速、精确的给出项目是否依赖cgo的判断。也许判断Go项目是否依赖CGO并没有捷径，需要从源码分析、依赖检查和构建测试等多个维度进行。

## 7. 小结

在本文中，我们深入探讨了Go语言编译过程中的几个重要细节，尤其是在静态链接和动态链接的选择上。通过具体示例，我们了解到：

-
默认链接方式：尽管CGO_ENABLED默认值为1，Go编译器在大多数情况下会采用静态链接，只有在依赖特定的C库或标准库包时，才会切换到动态链接。

-
动态链接的条件：我们讨论了几种情况下Go会默认生成动态链接的可执行文件，包括依赖使用C实现的标准库包、显式使用cgo调用外部C程序，以及使用依赖cgo的第三方包。

-
实现静态链接：对于需要动态链接的场景，我们也提供了将其转为静态链接的解决方案，包括关闭CGO、使用静态库，以及处理依赖cgo的外部包的静态链接问题。

-
二进制文件优化：我们还介绍了如何通过去除符号表和使用TinyGo等方法来优化生成的Go二进制文件的大小，以满足不同场景下的需求。

-
符号编译与死码消除：最后，我们探讨了未使用的符号是否会被编译到最终的二进制文件中，并解释了Go编译器的死码消除机制。


通过这些细节探讨，我希望能够帮助大家更好地理解Go编译的复杂性，并在实际开发中做出更明智的选择，亦能在面对Go编译相关问题时，提供有效的解决方案。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go-compilation)下载。

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
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论