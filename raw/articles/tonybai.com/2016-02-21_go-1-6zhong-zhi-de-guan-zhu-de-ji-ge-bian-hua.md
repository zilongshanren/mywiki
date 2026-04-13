---
title: Go 1.6中值得关注的几个变化
url: https://tonybai.com/2016/02/21/some-changes-in-go-1-6/
published: '2016-02-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.6中值得关注的几个变化

北京时间2016年2月18日凌晨，在[Go 1.5发布](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/) 半年后，[Go 1.6正式Release](http://blog.golang.org/go1.6) 了。与Go 1.5的“惊天巨变”（主要指Go自举）相比，[Go 1.6的Change](https://golang.org/doc/go1.6) 算是很小的了，当然这也与Go 1.6的dev cycle过于短暂有关。但Go社区对此次发布却甚是重视，其热烈程度甚至超出了Go 1.5。在[Dave Cheney](http://dave.cheney.net/)的倡导 下，Gophers们在全球各地举行了[Go 1.6 Release Party](https://github.com/golang/go/wiki/Go-1.6-release-party)。 Go Core Team也在Reddit上开了一个[AMA – Ask Me Anything](https://www.reddit.com/r/golang/comments/46bd5h/ama_we_are_the_go_contributors_ask_us_anything/)，RobPike、Russ Cox(Rsc)、Bradfitz等Go大神齐上阵，对广大Gophers们在24hour内的问题有问必答。

言归正传，我们来看看Go 1.6中哪些变化值得我们关注。不过在说变化之前，我们先提一嘴Go 1.6没变的，那就是Go语言的language specification，依旧保持Go 1兼容不变。预计在未来的几个stable release版本中，我们也不会看到Go language specification有任何改动。

### 一、cgo

cgo的变化在于：

1、定义了在Go code和C code间传递Pointer，即C code与Go garbage collector共存的rules和restriction；

2、在runtime加入了对违规传递的检查，检查的开关和力度由GODEBUG=cgocheck=1[0,2]控制。1是默认；0是关闭检 查；2是更全面彻底但代价更高的检查。

这个[Proposal](https://github.com/golang/proposal/blob/master/design/12416-cgo-pointers.md)是由Ian Lance Taylor提出的。大致分为两种情况：

#### (一) Go调用C Code时

Go调用C Code时，Go传递给C Code的Go Pointer所指的Go Memory中不能包含任何指向Go Memory的Pointer。我们分为几种情况来探讨一下：

1、传递一个指向Struct的指针

```
//cgo1_struct.go
package main
/*
#include <stdio.h>
struct Foo{
int a;
int *p;
};
void plusOne(struct Foo *f) {
(f->a)++;
*(f->p)++;
}
*/
import "C"
import "unsafe"
import "fmt"
func main() {
f := &C.struct_Foo{}
f.a = 5
f.p = (*C.int)((unsafe.Pointer)(new(int)))
//f.p = &f.a
C.plusOne(f)
fmt.Println(int(f.a))
}
```


从cgo1_struct.go代码中可以看到，Go code向C code传递了一个指向Go Memory（Go分配的）指针f，但f指向的Go Memory中有一个指针p指向了另外一处Go Memory: new(int)，我们来run一下这段代码：

```
$go run cgo1_struct.go
# command-line-arguments
./cgo1_struct.go:12:2: warning: expression result unused [-Wunused-value]
panic: runtime error: cgo argument has Go pointer to Go pointer
goroutine 1 [running]:
panic(0x4068400, 0xc82000a110)
/Users/tony/.bin/go16/src/runtime/panic.go:464 +0x3e6
main.main()
/Users/tony/test/go/go16/cgo/cgo1_struct.go:24 +0xb9
exit status 2
```


代码出现了Panic，并提示：“cgo argument has Go pointer to Go pointer”。我们的代码违背了Cgo Pointer传递规则，即便让f.p指向struct自身内存也是不行的，比如f.p = &f.a。

2、传递一个指向struct field的指针

按照rules中的说明，如果传递的是一个指向struct field的指针，那么”Go Memory”专指这个field所占用的内存，即便struct中有其他field指向其他Go memory也不打紧：

```
//cgo1_structfield.go
package main
/*
#include <stdio.h>
struct Foo{
int a;
int *p;
};
void plusOne(int *i) {
(*i)++;
}
*/
import "C"
import (
"fmt"
"unsafe"
)
func main() {
f := &C.struct_Foo{}
f.a = 5
f.p = (*C.int)((unsafe.Pointer)(new(int)))
C.plusOne(&f.a)
fmt.Println(int(f.a))
}
```


上述程序的运行结果：

```
$go run cgo1_structfield.go
6
```


3、传递一个指向slice or array中的element的指针

和传递struct field不同，传递一个指向slice or array中的element的指针时，需要考虑的Go Memory的范围不仅仅是这个element，而是整个Array或整个slice背后的underlying array所占用的内存区域，要保证这个区域内不包含指向任意Go Memory的指针。我们来看代码示例：

```
//cgo1_sliceelem.go
package main
/*
#include <stdio.h>
void plusOne(int **i) {
(**i)++;
}
*/
import "C"
import (
"fmt"
"unsafe"
)
func main() {
sl := make([]*int, 5)
var a int = 5
sl[1] = &a
C.plusOne((**C.int)((unsafe.Pointer)(&sl[0])))
fmt.Println(sl[0])
}
```


从这个代码中，我们看到我们传递的是slice的第一个element的地址，即&sl[0]。我们并未给sl[0]赋值，但sl[1] 被赋值为另外一块go memory的address(&a)，当我们将&sl[0]传递给plusOne时，执行结果如下：

```
$go run cgo1_sliceelem.go
panic: runtime error: cgo argument has Go pointer to Go pointer
goroutine 1 [running]:
panic(0x40dbac0, 0xc8200621d0)
/Users/tony/.bin/go16/src/runtime/panic.go:464 +0x3e6
main.main()
/Users/tony/test/go/go16/cgo/cgo1_sliceelem.go:19 +0xe4
exit status 2
```


由于违背规则，因此runtime panic了。

#### (二) C调用Go Code时

1、C调用的Go函数不能返回指向Go分配的内存的指针

我们看下面例子：

//cgo2_1.go

```
package main
// extern int* goAdd(int, int);
//
// static int cAdd(int a, int b) {
// int *i = goAdd(a, b);
// return *i;
// }
import "C"
import "fmt"
//export goAdd
func goAdd(a, b C.int) *C.int {
c := a + b
return &c
}
func main() {
var a, b int = 5, 6
i := C.cAdd(C.int(a), C.int(b))
fmt.Println(int(i))
}
```


可以看到：goAdd这个Go函数返回了一个指向Go分配的内存(&c)的指针。运行上述代码，结果如下：

```
$go run cgo2_1.go
panic: runtime error: cgo result has Go pointer
goroutine 1 [running]:
panic(0x40dba40, 0xc82006e1c0)
/Users/tony/.bin/go16/src/runtime/panic.go:464 +0x3e6
main._cgoexpwrap_872b2f2e7532_goAdd.func1(0xc820049d98)
command-line-arguments/_obj/_cgo_gotypes.go:64 +0x3a
main._cgoexpwrap_872b2f2e7532_goAdd(0x600000005, 0xc82006e19c)
command-line-arguments/_obj/_cgo_gotypes.go:66 +0x89
main._Cfunc_cAdd(0x600000005, 0x0)
command-line-arguments/_obj/_cgo_gotypes.go:45 +0x41
main.main()
/Users/tony/test/go/go16/cgo/cgo2_1.go:20 +0x35
exit status 2
```


2、Go code不能在C分配的内存中存储指向Go分配的内存的指针

下面的例子模拟了这一情况：

```
//cgo2_2.go
package main
// #include <stdlib.h>
// extern void goFoo(int**);
//
// static void cFoo() {
// int **p = malloc(sizeof(int*));
// goFoo(p);
// }
import "C"
//export goFoo
func goFoo(p **C.int) {
*p = new(C.int)
}
func main() {
C.cFoo()
}
```


不过针对此例，默认的GODEBUG=cgocheck=1偏是无法check出问题。我们将GODEBUG=cgocheck改为=2试试：

```
$GODEBUG=cgocheck=2 go run cgo2_2.go
write of Go pointer 0xc82000a0f8 to non-Go memory 0x4300000
fatal error: Go pointer stored into non-Go memory
runtime stack:
runtime.throw(0x4089800, 0x24)
/Users/tony/.bin/go16/src/runtime/panic.go:530 +0x90
runtime.cgoCheckWriteBarrier.func1()
/Users/tony/.bin/go16/src/runtime/cgocheck.go:44 +0xae
runtime.systemstack(0x7fff5fbff8c0)
/Users/tony/.bin/go16/src/runtime/asm_amd64.s:291 +0x79
runtime.mstart()
/Users/tony/.bin/go16/src/runtime/proc.go:1048
... ...
goroutine 17 [syscall, locked to thread]:
runtime.goexit()
/Users/tony/.bin/go16/src/runtime/asm_amd64.s:1998 +0x1
exit status 2
```


果真runtime panic: write of Go pointer 0xc82000a0f8 to non-Go memory 0×4300000

### 二、HTTP/2

HTTP/2原本是[bradfitz](https://github.com/bradfitz)维护的x项目，之前位于golang.org/x/net/http2包中，Go 1.6无缝合入Go标准库net/http包中。并且当你你使用[https](http://tonybai.com/2015/04/30/go-and-https/)时，client和server端将自动默认使用HTTP/2协议。

HTTP/2与HTTP1.x协议不同在于其为二进制协议，而非文本协议，性能自是大幅提升。HTTP/2标准已经发布，想必未来若干年将大行其道。

HTTP/2较为复杂，这里不赘述，后续maybe会单独写一篇GO和http2的文章说明。

### 三、Templates

由于不开发web，templates我日常用的很少。这里粗浅说说templates增加的两个Feature

#### trim空白字符

Go templates的空白字符包括：空格、水平tab、回车和换行符。在日常编辑模板时，这些空白尤其难于处理，由于是对beatiful format和code readabliity有“强迫症”的同学，更是在这方面话费了不少时间。

Go 1.6提供了{{-和-}}来帮助大家去除action前后的空白字符。下面的例子很好的说明了这一点：

```
//trimwhitespace.go
package main
import (
"log"
"os"
"text/template"
)
var items = []string{"one", "two", "three"}
func tmplbefore15() {
var t = template.Must(template.New("tmpl").Parse(`
<ul>
{{range . }}
<li>{{.}}</li>
{{end }}
</ul>
`))
err := t.Execute(os.Stdout, items)
if err != nil {
log.Println("executing template:", err)
}
}
func tmplaftergo16() {
var t = template.Must(template.New("tmpl").Parse(`
<ul>
{{range . -}}
<li>{{.}}</li>
{{end -}}
</ul>
`))
err := t.Execute(os.Stdout, items)
if err != nil {
log.Println("executing template:", err)
}
}
func main() {
tmplbefore15()
tmplaftergo16()
}
```


这个例子的运行结果：

```
$go run trimwhitespace.go
<ul>
<li>one</li>
<li>two</li>
<li>three</li>
</ul>
<ul>
<li>one</li>
<li>two</li>
<li>three</li>
</ul>
```


#### block action

block action提供了一种在运行时override已有模板形式的能力。

```
package main
import (
"log"
"os"
"text/template"
)
var items = []string{"one", "two", "three"}
var overrideItemList = `
{{define "list" -}}
<ul>
{{range . -}}
<li>{{.}}</li>
{{end -}}
</ul>
{{end}}
`
var tmpl = `
Items:
{{block "list" . -}}
<ul>
{{range . }}
<li>{{.}}</li>
{{end }}
</ul>
{{end}}
`
var t *template.Template
func init() {
t = template.Must(template.New("tmpl").Parse(tmpl))
}
func tmplBeforeOverride() {
err := t.Execute(os.Stdout, items)
if err != nil {
log.Println("executing template:", err)
}
}
func tmplafterOverride() {
t = template.Must(t.Parse(overrideItemList))
err := t.Execute(os.Stdout, items)
if err != nil {
log.Println("executing template:", err)
}
}
func main() {
fmt.Println("before override:")
tmplBeforeOverride()
fmt.Println("after override:")
tmplafterOverride()
}
```


原模板tmpl中通过block action定义了一处名为list的内嵌模板锚点以及初始定义。后期运行时通过re-parse overrideItemList达到修改模板展示形式的目的。

上述代码输出结果：

```
$go run blockaction.go
before override:
Items:
<ul>
<li>one</li>
<li>two</li>
<li>three</li>
</ul>
after override:
Items:
<ul>
<li>one</li>
<li>two</li>
<li>three</li>
</ul>
```


### 四、Runtime

#### 降低大内存使用时的GC latency

Go 1.5.x用降低一些吞吐量的代价换取了10ms以下的GC latency。不过针对Go 1.5，官方给出的benchmark图中，内存heap size最多20G左右。一旦超过20G，latency将超过10ms，也许会线性增长。

在Go 1.6中，官方给出的benchmark图中当内存heap size在200G时，GC latency依旧可以稳定在10ms；在heap size在20G以下时，latency降到了6ms甚至更小。

#### panic info

Go 1.6之前版本，一旦程序以panic方式退出，runtime便会将所有goroutine的stack信息打印出来：

```
$go version
go version go1.5.2 darwin/amd64
[ ~/test/go/go16/runtime]$go run panic.go
panic: runtime error: invalid memory address or nil pointer dereference
[signal 0xb code=0x1 addr=0x0 pc=0x20d5]
goroutine 1 [running]:
main.main()
/Users/tony/test/go/go16/runtime/panic.go:19 +0x95
goroutine 4 [select (no cases)]:
main.main.func1(0x8200f40f0)
/Users/tony/test/go/go16/runtime/panic.go:13 +0x26
created by main.main
/Users/tony/test/go/go16/runtime/panic.go:14 +0x72
... ...
```


而Go 1.6后，Go只会打印正在running的goroutine的stack信息，因此它才是最有可能造成panic的真正元凶：

```
go 1.6：
$go run panic.go
panic: runtime error: invalid memory address or nil pointer dereference
[signal 0xb code=0x1 addr=0x0 pc=0x20d5]
goroutine 1 [running]:
panic(0x61e80, 0x8200ee0c0)
/Users/tony/.bin/go16/src/runtime/panic.go:464 +0x3e6
main.main()
/Users/tony/test/go/go16/runtime/panic.go:19 +0x95
exit status 2
```


#### map race detect

Go原生的map类型是goroutine-unsafe的，长久以来，这给很多Gophers带来了烦恼。这次Go 1.6中Runtime增加了对并发访问map的检测以降低gopher们使用map时的心智负担。

这里借用了Francesc Campoy在最近一期”The State of Go”中的示例程序：

```
package main
import "sync"
func main() {
const workers = 100
var wg sync.WaitGroup
wg.Add(workers)
m := map[int]int{}
for i := 1; i <= workers; i++ {
go func(i int) {
for j := 0; j < i; j++ {
m[i]++
}
wg.Done()
}(i)
}
wg.Wait()
}
```


执行结果：

```
$ go run map.go
fatal error: concurrent map writes
fatal error: concurrent map writes
... ...
```


这里在双核i5 mac air下亲测时，发现当workers=2,3,4均不能检测出race。当workers >= 5时可以检测到。

### 五、其他

#### 手写parser替代yacc生成的parser

这个变化对Gopher们是透明的，但对于Go compiler本身却是十分重要的。

Robert Riesemer在Go 1.6代码Freezing前commit了手写Parser，以替代yacc生成的parser。在AMA上RobPike给出了更换Parser的些许理由：

1、Go compiler可以少维护一个yacc工具，这样更加cleaner；

2、手写Parser在性能上可以快那么一点点。

#### Go 1.6中GO15VENDOREXPERIMENT将默认开启

根据当初在Go 1.5中引入vendor时的计划，Go 1.6中GO15VENDOREXPERIMENT将默认开启。这显然会导致一些不兼容的情况出现：即如果你的代码在之前并未使用vendor机制，但目录组织中有vendor目录。Go Core team给出的解决方法就是删除vendor目录或改名。

### 遗留问题是否解决

在[Go 1.5发布](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)后，曾经发现两个问题，直到Go 1.5.3版本发布也未曾解决，那么Go 1.6是否解决了呢？我们来验证一下。

#### internal问题

该问题的具体细节可参看我在go github上提交的[issue 12217](https://github.com/golang/go/issues/12217)，我在自己的[experiments](https://github.com/bigwhite/experiments/tree/master/go15-internal-issue-12217)中提交了问题的验证环境代码，这次我们使用Go 1.6看看internal问题是否还存在：

```
$cd $GOPATH/src/github.com/bigwhite/experiments/go15-internal-issue-12217
$cd otherpkg/
$go build main.go
package main
imports github.com/bigwhite/experiments/go15-internal-issue-12217/mypkg/internal/foo: use of internal package not allowed
```


这回go compiler给出了error，而不是像之前版本那样顺利编译通过。看来这个问题是fix掉了。

#### GOPATH之外vendor机制是否起作用的问题

我们先建立实验环境：

```
$tree
.
└── testvendor
└── src
└── proj1
├── main.go
└── vendor
└── github.com
└── bigwhite
└── foo
└── foolib.go
```


进入proj1，build main.go

```
go build main.go
main.go:3:8: cannot find package "github.com/bigwhite/foo" in any of:
/Users/tony/.bin/go16/src/github.com/bigwhite/foo (from $GOROOT)
/Users/tony/Test/GoToolsProjects/src/github.com/bigwhite/foo (from $GOPATH)
```


go 1.6编译器没有关注同路径下的vendor目录，build失败。

我们设置GOPATH=xxx/testvendor后，再来build：

```
$export GOPATH=~/Test/go/go16/others/testvendor
$go run main.go
Hello from temp vendor
```


这回编译运行ok。

由此看来，Go 1.6 vendor在GOPATH外依旧不生效。

#### 六、小结

Go 1.6标准库细微变化还是有很多的，在[Go 1.6 Release Notes](https://golang.org/doc/go1.6)中可细细品味。

Go 1.6的编译速度、编译出的程序的运行性能与Go 1.5.x也大致无二异。

另外本文实现环境如下：

```
go version go1.6 darwin/amd64
Darwin tonydeair-2.lan 13.1.0 Darwin Kernel Version 13.1.0: Thu Jan 16 19:40:37 PST 2014; root:xnu-2422.90.20~2/RELEASE_X86_64 x86_64
```


实验代码可在[这里](https://github.com/bigwhite/experiments/tree/master/go16-examples)下载。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

看起来，我这里北京联通，看到了被运营商劫持加了淘宝的广告。望尽快上 HTTPS。

今天才发现你的博客，连着看了几篇呢