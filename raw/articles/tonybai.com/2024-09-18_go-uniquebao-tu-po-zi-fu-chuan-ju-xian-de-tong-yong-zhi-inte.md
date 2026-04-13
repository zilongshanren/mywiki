---
title: Go unique包：突破字符串局限的通用值Interning技术实现
url: https://tonybai.com/2024/09/18/understand-go-unique-package-by-example/
published: '2024-09-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go unique包：突破字符串局限的通用值Interning技术实现

![](../../assets/4aec412c4a8f9335.png)


[本文永久链接](https://tonybai.com/2024/09/18/understand-go-unique-package-by-example) – https://tonybai.com/2024/09/18/understand-go-unique-package-by-example

[Go的1.23版本](https://tonybai.com/2024/08/19/some-changes-in-go-1-23)中引入了一个[新的标准库包unique](https://pkg.go.dev/unique?ref=tonybai.com)，为Go开发者带来了高效的值[interning能力](https://en.wikipedia.org/wiki/Interning_(computer_science))。这种能力不仅适用于字符串类型值，还可应用于任何可比较(comparable)类型的值。

本文将简要探讨interning技术及其在Go中的实现方式，通过介绍unique包的功能，帮助读者更好地理解这一技术及其实际应用。

## 1. 从string interning技术说起

通常提到interning技术时，指的是传统的字符串驻留（string interning）技术。它是一种优化方法，旨在**减少程序中重复字符串的内存占用**，并**提高字符串比较操作的效率**。其基本原理是将相同的字符串值在内存中只存储一次，所有对该字符串的引用都指向同一内存地址，而不是为每个相同字符串创建单独的副本。下图展示了使用和不使用string interning技术的对比:

![](../../assets/fd7ab8b36cfc2ab5.png)


这个图直观地展示了string interning如何通过共享相同的字符串来节省内存和提高效率。我们看到：在不使用string interning的情况下，每个字符串都有自己的内存分配，即使内容相同，比如”Hello”字符串出现两次，占用了两块不同的内存空间。而在使用string interning的情况下，相同内容的字符串只存储一次，比如：两个”Hello”字符串引用指向同一个内存位置。

string interning在多种场景下非常有用，比如在解析文本格式(如XML、JSON)时，interning能高效处理标签名称经常重复的问题；在编译器或解释器的实现时，interning能够减少符号表中的重复项等。

传统的string interning通常使用哈希表或字典来存储字符串的唯一实例。每次出现新字符串时，程序首先会检查哈希表中是否已有相同的字符串，若存在则返回其引用，若不存在则将其存储在表中。

Michael Knyszek在[Go官博介绍interning技术](https://go.dev/blog/unique?ref=tonybai.com)时，也给出了一个传统实现的代码片段：

```
var internPool map[string]string
// Intern returns a string that is equal to s but that may share storage with
// a string previously passed to Intern.
func Intern(s string) string {
pooled, ok := internPool[s]
if !ok {
// Clone the string in case it's part of some much bigger string.
// This should be rare, if interning is being used well.
pooled = strings.Clone(s)
internPool[pooled] = pooled
}
return pooled
}
```


这种实现虽然简单，但Knyszek指出了其存在几个问题：

- 一旦字符串被intern，就永远不会被释放。
- 在多goroutine环境下使用需要额外的同步机制。
- 仅限于字符串类型值，不能用于其他类型的值。

Go 1.23版本引入的unique包就是string interning技术的一种Go官方实现，当然就像前面所说，unique包不仅仅支持传统的string interning，还支持任何支持比较的类型的值的interning。

不过，在介绍unique包之前，我们简单看看这些年来Go社区对interning技术的贡献。

## 2. Go社区interning技术的实现简史

由于其他主流语言都或多或少有了对string interning的支持，Go社区显然也需要这样的包，在Go issues列表中，我能找到的最早提出在Go中添加interning技术实现的是2013年go核心开发人员Brad Fitzpatrick提出的”[proposal: runtime: optionally allow callers to intern strings](https://github.com/golang/go/issues/5160?ref=tonybai.com)“。

2019年，Josh Bleecher Snyder发表了一篇博文[Interning strings in Go](https://commaok.xyz/post/intern-strings?ref=tonybai.com)，探讨了interning的Go实现方法，并给出一个[简单但重度使用sync.Pool的interning实现](https://github.com/josharian/intern)，该实现支持对string和字节切片的interning。

2021年，tailscale为了实现[可以高效表示ip地址的netaddr包](https://github.com/inetaf/netaddr)，构建和开源了[go4.org/intern包](https://github.com/go4org/intern)，这是一个可用于量产级别的interning实现。

注：go4.org中这个go4的名字很可能就是因为go4.org这个组织只有四个contributors：Brad Fitzpatrick、Josh Bleecher Snyder、Dave Anderson和Matt Layher。之前的一篇文章《

[理解unsafe-assume-no-moving-gc包]》中的unsafe-assume-no-moving-gc包也是go4.org下面的。

之后，Brad Fitzpatrick将inetaf/netaddr包的实现合并到了Go标准库net/netip中，而netaddr包依赖的go4.org/intern包也被移入Go项目，变为internal/intern包，并被net/netip包所使用。

直到2023年9月，mknyszek提出”[unique: new package with unique.Handle](https://github.com/golang/go/issues/62483)“的proposal，给出unique包的API设计和参考实现。unique落地后，原先使用internal/intern包的net/netip也都改为使用unique包了，internal/intern在Go 1.23版本被移除。

接下来，我们来看看这篇文章的主角unique包。

## 3. Go的unique包介绍

相较于传统的interning实现以及Go社区之前的实现，Go 1.23引入的unique包提供了一个更加通用和高效的interning实现方案。下面我们就分别从API、unique包的优势以及实现原理等几个方面介绍一下这个包。

### 3.1 unique包的API

从用户角度看，unique包提供的核心API非常简洁：

```
$go doc unique.Handle
package unique // import "unique"
type Handle[T comparable] struct {
// Has unexported fields.
}
func Make[T comparable](value T) Handle[T]
func (h Handle[T]) Value() T
```


Make函数就是unique包的”Intern”函数，它接受一个可比较类型的值，返回一个intern后的值，不过和前面那个传统实现方式的Intern函数不同，Make函数返回的是一个Handle[T]类型的值。针对同一个传给Make函数的值，返回的Handle[T]类型的值是相同的：

```
// unique-examples/string_interning.go
package main
import "unique"
func main() {
h1 := unique.Make("hello")
h2 := unique.Make("hello")
h3 := unique.Make("hello")
h4 := unique.Make("golang")
println(h1 == h2) // true
println(h1 == h3) // true
println(h1 == h4) // false
println(h2 == h4) // false
}
```


unique包的作者Knyszek认为Handle[T]和Lisp语言中的Symbol十分类似，Symbol在Lisp中是interned后的字符串，Lisp确保相同的字符串只存储一次，提高内存存储和使用效率。

不过前面说了，unique不仅支持字符串值的interning，还支持其他可比较类型的值的interning，下面是一个int interning和一个自定义可比较类型的interning的例子：

```
// unique-examples/int_interning.go
package main
import "unique"
func main() {
var a, b int = 5, 6
h1 := unique.Make(a)
h2 := unique.Make(a)
h3 := unique.Make(b)
println(h1 == h2) // true
println(h1 == h3) // false
}
// unique-examples/user_type_interning.go
package main
import "unique"
type UserType struct {
a int
z float64
s string
}
func main() {
var u1 = UserType{
a: 5,
z: 3.14,
s: "golang",
}
var u2 = UserType{
a: 5,
z: 3.15,
s: "golang",
}
h1 := unique.Make(u1)
h2 := unique.Make(u1)
h3 := unique.Make(u2)
println(h1 == h2) // true
println(h1 == h3) // false
}
```


注：如果要intern的类型T是包含指针的结构体，这些指针指向的值几乎总是会逃逸到堆上。


通过Make获得的Handle[T]的Value方法可以获取到interning值的原始值，我们看下面示例：

```
// unique-examples/value.go
package main
import (
"fmt"
"unique"
)
type UserType struct {
a int
z float64
s string
}
func main() {
var u1 = UserType{
a: 5,
z: 3.14,
s: "golang",
}
h1 := unique.Make(u1)
h2 := unique.Make("hello, golang")
h3 := unique.Make(567890)
v1 := h1.Value()
v2 := h2.Value()
v3 := h3.Value()
fmt.Printf("%T: %v\n", v1, v1) // main.UserType: {5 3.14 golang}
fmt.Printf("%T: %v\n", v2, v2) // string: hello, golang
fmt.Printf("%T: %v\n", v3, v3) // int: 567890
}
```


注：Value方法返回的是值的浅拷贝，对于复合类型可能存在共享底层数据的情况。


### 3.2 unique包的实现原理

传统的字符串interning实现起来可能并不难，但unique包的目标是设计支持可比较类型、interning值也可被GC且支持快速interning值比较的方案，unique包的实现涉及到hashtrimap、细粒度锁以及与runtime内gc相关函数结合的技术难题，因此其门槛还是很高的，即便是Go核心团队成员Knyszek实现的unique包，在Go 1.23发布后也被发现了[较为“严重”的bug](https://github.com/golang/go/issues/69370)，该问题将[在Go 1.23.2版本修正](https://github.com/golang/go/issues/69383)。

下面是一个unique包实现原理的示意图：

![](../../assets/e49e63222fb454c2.png)


上图展示了Make、Handle[T]和Value方法之间的关系，以及它们如何与内部的map(hashtrieMap)交互。

我们看到，图中三次调用Make(“hello”)都返回相同的Handle[string]{ptr1}，即无论调用多少次Make，对于相同的输入值，Make总是返回相同的Handle。

图中的Handle[string]{ptr1}是一个包含指向存储”hello”的内存位置指针的结构，所有三次Make调用返回的Handle都指向同一个内存位置。下面是Handle结构体的定义，看了你就明白了这句话的含义：

```
// $GOROOT/src/unique/handle.go
type Handle[T comparable] struct {
value *T
}
```


注：这里Handle内部的指针*T都是strong pointer(强指针)，以图中示例，只要有一个Handle实例(由Make返回的)存在，内存中的”hello”就不会被GC。


Handle[string]{ptr1}的Value()方法返回存储的字符串值”hello”。

unique包有一个内部map(hashtrieMap)存储键值对，键是字符串”hello”的clone，值是一个weak.Pointer，指向存储实际字符串值的内存位置。weak.Pointer 是Go 1.23版本的内部包internal/weak中的一个类型，主要用于实现弱指针（weak pointer）的功能。weak.Pointer的主要作用是允许引用一个对象，而不会阻止该对象被垃圾收集器回收。具体来说，它允许你持有一个指向对象的指针，但当该对象的强指针消失时，垃圾收集器仍然可以回收该对象。下面是一张weak Pointer工作机制的示意图，展示了弱指针的生命周期以及对GC行为的影响：

![](https://tonybai.com/wp-content/uploads/understand-go-unique-package-by-example-4.png)


初始状态下，应用创建一个对象，同时创建一个强指针和一个weak.Pointer指向该对象。GC检查对象，但因为存在强指针，所以不能回收。强指针被移除，只剩下weak.Pointer指向对象。GC检查对象，发现没有强指针，于是回收对象。内存被释放，weak.Pointer变为nil。

由于weak包位于internal包中，它只能在Go的标准库或特定包中使用，我们只能用下面的伪代码来展示weak.Pointer的机制：

```
package main
import (
"fmt"
"runtime"
"unsafe"
"internal/weak"
)
type MyStruct struct {
name string
}
func main() {
// 创建一个对象，obj可以理解为该对象的强指针
obj := &MyStruct{name: "object1"}
// 创建一个weak.Pointer指向obj，weakPtr是对obj指向内存的弱指针
weakPtr := weak.Make(obj)
// 显示对象的值，通过强指针和弱指针都可以
fmt.Println("Before GC:", weakPtr.Value())
fmt.Println("Before GC:", *obj)
// 释放原始对象的强指针
obj = nil
// 强制执行GC，这时由于弱指针无法阻止GC，obj指向的内存可能被回收
runtime.GC()
// 查看弱指针是否仍然有效，这里不能直接使用obj，因为对象可能已经被回收
fmt.Println("After GC:", weakPtr.Value())
}
```


弱指针有一些典型的使用场景，比如在缓存机制中，可能希望引用某些对象而不阻止它们被垃圾回收。这样可以在内存不足时自动释放不再使用的缓存对象；又比如在某些场景下，不希望对象长时间驻留在内存中，但仍然希望能够在需要时重新创建或加载它们，即延迟加载的对象；在某些数据结构中（如哈希表或链表），持有强指针可能会导致内存泄漏，弱指针可以有效避免这种情况。

注：目前Knyszek已经提出proposal，

[将weak包提升为标准库公共API]，该proposal已经被accept，最早将在Go 1.24版本落地。

### 3.3 unique包的优势

从上面示例和原理示意图来看，unique包的设计和实现有几个显著的优势：

- 泛型支持

通过使用Go的泛型特性，unique包可以处理任何可比较的类型，大大扩展了其应用范围，不再局限于字符串类型。

- 高效的内存管理

unique包使用了运行时级别的弱指针实现，确保当所有相关的Handle[T](即强指针)都不再被使用时，内部map中的值可以被垃圾回收，这既避免了内存长期占用，也避免了内存泄漏问题。

- 快速比较操作

Handle[T]类型的比较操作被优化为简单的指针比较，这比直接比较值(特别是对于大型结构体或长字符串内容)要快得多。

### 3.4 unique包的实际应用

unique包刚刚诞生，目前在Go标准库中的实际应用主要就是在net/netip包中，替代了之前由go4.org/intern移植到标准库中的internal/intern包。

net/netip包使用unique来优化Addr结构体中的addrDetail字段：

```
type Addr struct {
// 其他字段...
// Details about the address, wrapped up together and canonicalized.
z unique.Handle[addrDetail]
}
// addrDetail represents the details of an Addr, like address family and IPv6 zone.
type addrDetail struct {
isV6 bool // IPv4 is false, IPv6 is true.
zoneV6 string // != "" only if IsV6 is true.
}
// z0, z4, and z6noz are sentinel Addr.z values.
// See the Addr type's field docs.
var (
z0 unique.Handle[addrDetail]
z4 = unique.Make(addrDetail{})
z6noz = unique.Make(addrDetail{isV6: true})
)
// WithZone returns an IP that's the same as ip but with the provided
// zone. If zone is empty, the zone is removed. If ip is an IPv4
// address, WithZone is a no-op and returns ip unchanged.
func (ip Addr) WithZone(zone string) Addr {
if !ip.Is6() {
return ip
}
if zone == "" {
ip.z = z6noz
return ip
}
ip.z = unique.Make(addrDetail{isV6: true, zoneV6: zone})
return ip
}
```


通过使用unique，net/netip包能够显著减少处理大量IP地址时的内存占用。特别是对于具有相同zone的IPv6地址，内存使用可以大幅降低。

下面我们也通过一个简单的示例来看看使用unique包的内存占用减少的效果。

### 3.5 内存占用减少的效果

现在我们创建100w个长字符串，这100w个字符串中，有1000种不同的字符串，相当于每种字符串有1000个重复值。下面分别用unique包和不用unique包来演示这个示例，看看内存占用情况：

```
// unique-examples/effect_with_unique.go
package main
import (
"fmt"
"runtime"
"strings"
"unique"
)
const (
numItems = 1000000
stringLen = 20
numDistinct = 1000
)
func main() {
// 创建一些不同的字符串
distinctStrings := make([]string, numDistinct)
for i := 0; i < numDistinct; i++ {
distinctStrings[i] = strings.Repeat(string(rune('A'+i%26)), stringLen)
}
// 使用unique包
withUnique := make([]unique.Handle[string], numItems)
for i := 0; i < numItems; i++ {
withUnique[i] = unique.Make(distinctStrings[i%numDistinct])
}
runtime.GC() // 强制GC
printMemUsage("With unique")
runtime.KeepAlive(withUnique)
}
func printMemUsage(label string) {
var m runtime.MemStats
runtime.ReadMemStats(&m)
fmt.Printf("%s:\n", label)
fmt.Printf(" Alloc = %v MiB\n", bToMb(m.Alloc))
fmt.Printf(" TotalAlloc = %v MiB\n", bToMb(m.TotalAlloc))
fmt.Printf(" Sys = %v MiB\n", bToMb(m.Sys))
fmt.Printf(" HeapAlloc = %v MiB\n", bToMb(m.HeapAlloc))
fmt.Printf(" HeapSys = %v MiB\n", bToMb(m.HeapSys))
fmt.Printf(" HeapInuse = %v MiB\n", bToMb(m.HeapInuse))
fmt.Println()
}
func bToMb(b uint64) uint64 {
return b / 1024 / 1024
}
// unique-examples/effect_without_unique.go
...
func main() {
// 创建一些不同的字符串
distinctStrings := make([]string, numDistinct)
for i := 0; i < numDistinct; i++ {
distinctStrings[i] = strings.Repeat(string(rune('A'+i%26)), stringLen)
}
// 不使用unique包
withoutUnique := make([]string, numItems)
for i := 0; i < numItems; i++ {
withoutUnique[i] = distinctStrings[i%numDistinct]
}
runtime.GC() // 强制GC以确保准确的内存使用统计
printMemUsage("Without unique")
runtime.KeepAlive(withoutUnique)
}
...
```


下面分别运行这两个源码：

```
$go run effect_with_unique.go
With unique:
Alloc = 7 MiB
TotalAlloc = 7 MiB
Sys = 15 MiB
HeapAlloc = 7 MiB
HeapSys = 11 MiB
HeapInuse = 8 MiB
$go run effect_without_unique.go
Without unique:
Alloc = 15 MiB
TotalAlloc = 15 MiB
Sys = 22 MiB
HeapAlloc = 15 MiB
HeapSys = 19 MiB
HeapInuse = 15 MiB
```


这个结果清楚地显示了使用unique包后的内存节省。不使用unique包时，每个重复的字符串都会单独分配内存。而使用unique包后，相同的字符串只会分配一次，大大减少了内存使用。在实际应用中，内存节省的效果可能更加显著，特别是在处理大量重复数据（如日志处理、文本分析等）的场景中。

## 4. 小结

本文粗略探讨了Go 1.23版本引入的unique包：我们从字符串interning技术说起，介绍了Go社区在interning技术实现方面的努力历程，重点阐述了unique包的API设计、实现原理及其优势。

我们看到：unique包不仅支持传统的字符串interning，还扩展到任何可比较类型的值。其核心API设计简洁，通过Handle[T]类型和Make、Value方法实现了高效的值interning。

在实现原理上，unique包巧妙地结合了hashtrieMap、细粒度锁以及与runtime内gc相关函数，实现了支持可比较类型、interned值可被GC且支持快速比较的方案。

总的来说，unique包为Go开发者提供了一个强大而灵活的interning工具，有望在未来的Go社区项目中得到广泛应用。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/unique-examples)下载。

## 5. 参考资料

[Interning strings in Go](https://commaok.xyz/post/intern-strings/)– https://commaok.xyz/post/intern-strings/[Interning](https://en.wikipedia.org/wiki/String_interning)– https://en.wikipedia.org/wiki/String_interning[unique: new package with unique.Handle](https://github.com/golang/go/issues/62483)– https://github.com/golang/go/issues/62483[New unique package](https://go.dev/blog/unique)– https://go.dev/blog/unique[unique: large string still referenced, after interning only a small substring](https://github.com/golang/go/issues/69370)– https://github.com/golang/go/issues/69370[netaddr.IP: a new IP address type for Go](https://tailscale.com/blog/netaddr-new-ip-type-for-go?ref=tonybai.com)– https://tailscale.com/blog/netaddr-new-ip-type-for-go

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

Really cool content. I can see the effort that has gone into this website. Every article is full of crucial information.