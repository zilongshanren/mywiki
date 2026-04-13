---
title: 将Roaring Bitmap序列化为JSON
url: https://tonybai.com/2023/02/01/serialize-roaring-bitmap-to-json/
published: '2023-02-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 将Roaring Bitmap序列化为JSON

![](../../assets/e014da7a7075a0f8.png)


[本文永久链接](https://tonybai.com/2023/02/01/serialize-roaring-bitmap-to-json) – https://tonybai.com/2023/02/01/serialize-roaring-bitmap-to-json

近期在实现一个数据结构时使用到了[位图索引(bitmap index)](https://en.wikipedia.org/wiki/Bitmap_index)，本文就来粗浅聊聊位图(bitmap)。

### 一. 什么是bitmap

位图索引使用位数组(bit array，也有叫bitset的，通常被称为位图(bitmap)，以下均使用bitmap这个名称)实现。一个bitmap是一个从某个域（通常是一个整数范围）到集合{0，1}中的值的映射：

```
映射：f(x) -> {0, 1}， x是[0, n)的集合中的元素。
```


以n=8的集合{1, 2, 5}为例：

```
f(0) = 0
f(1) = 1
f(2) = 1
f(3) = 0
f(4) = 0
f(5) = 1
f(6) = 0
f(7) = 0
```


如果用bit来表示映射后得到的值，我们将得到一个二进制数0b00100110(最右侧的bit位上的值指示集合中数值0的存在性)，这样我们就可以用**一个字节大小**的数值0b00100110来表示{1, 2, 5}这个集合中各个位置的数值的存在性了。

我们看到相比于使用一个byte数组来表示{1, 2, 5}这个集合(即便是8个数值，也至少要8x8=64个字节)，bitmap无疑具有更高的空间利用率。同时，通过bitmap的与、或、异或等操作，我们可以很容易且高性能地得到集合的交、并、Top-K等集合操作的结果。

不过，传统的bitmap并不总能带来空间上的节省，比如我们要表示{1, 2, 10, 50000000}这样一个集合，那么使用传统bitmap将带来很大的空间开销。对于这样的具有稀疏元素特性的集合，传统位图实现就失去了其优势，而[压缩位图(compressed bitmap)](https://en.wikipedia.org/wiki/Bitmap_index#Compression)则成为了更佳的选择。

### 二. 压缩位图(compressed bitmap)

压缩位图既可以很好的支持稀疏集合，又保留了传统位图的空间和高性能的集合操作优势。最常见的压缩位图的方案是RLE(run-length encoding)，对这种方案的粗浅理解是对连续的0和1进行分别计数，比如下面这bitmap就可以压缩编码为**n个0和m和1**：

```
0b0000....00001111...111
```


RLE方案(以及其变体)具有很好的压缩比并且编解码也很高效。不过其不足是很难随机访问某个bit，每次访问特定的bit都要从头进行解压缩。如果你想将两个大的bitmap进行交集操作，你必须解压缩整个大bitmap。

一种名为roaring bitmap的压缩位图方案可以解决上述的问题。

### 三. roaring bitmap工作原理简介

roaring bitmap 的工作方式是这样的：它将32位整型所能表示的整型数[0, 4294967296)划分为2^16个chunk（例如，[0，2^16)，[2^16，2x2^16)，...）。当向roaring bitmap加入一个数或从roaring bitmap获取一个数的存在性时，roaring bitmap通过这个数的前16位决定该数在哪个trunk中。一旦确定trunk后，便可以通过与该trunk关联的container指针找到真正存储该数后16位值的container，在container中通过查找算法定位：

![](../../assets/1b3809b4292395f7.png)


如上图所示：roaring bitmap的trunk关联的container类型不止有一种：

- array container：这是一个有序的16bit整型数组，也是默认的container type，最多存储4096个数值。当超出这个数量时，会考虑用bitset container存储；
- bitset container：就是一个非压缩的bitmap，有2^16个bit位；
- run container：这是一个采用RLE压缩的、适合存储连续数值的container type，从上面图中也可以看出，这个container中存储的是一个个数对<s,l>，表示的数值范围为[s, s + l]。

roaring bitmap会根据trunk中的数的特征选择适当的container类型，并且这种选择是动态的，以尽量减少内存使用为目标。当我们向roaring bitmap添加或删除值时，对应trunk的container type都可能会改变。不过从整体视角看，无论使用哪种container，roaring bitmap都支持对某个bit的快速随机访问。同时roaring bitmap在实现层面也更容易利用现代cpu提供的高性能指令，并且是缓存友好的。

### 四. roaring bitmap的效果

roaring bitmap官方提供了多种主流语言的实现，其中Go语言的实现是[roaring包](https://github.com/RoaringBitmap/roaring)。roaring包的使用十分简单，下面就是一个简单的示例：

```
package main
import (
"fmt"
"github.com/RoaringBitmap/roaring"
)
func main() {
rb := roaring.NewBitmap()
rb.Add(1)
rb.Add(100000000)
fmt.Println(rb.String())
fmt.Println(rb.Contains(1))
fmt.Println(rb.Contains(2))
fmt.Println(rb.Contains(100000000))
fmt.Println("cardinality:", rb.GetCardinality())
fmt.Println("rb size=", rb.GetSizeInBytes())
}
```


运行示例得到如下结果：

```
{1,100000000}
true
false
true
cardinality: 2
rb size= 16
```


我们看到{1, 100000000}的稀疏集合映射到roaring bitmap仅占用了16个字节的空间(和非压缩bitmap对比)。

下面是一个由3000w以内的随机整数构成的集合到roaring bitmap的映射示例：

```
func main() {
rb := roaring.NewBitmap()
for i := 0; i < 30000000; i++ {
rb.Add(uint32(rand.Int31n(30000000)))
}
fmt.Println("cardinality:", rb.GetCardinality())
fmt.Println("rb size=", rb.GetSizeInBytes())
}
```


下面是其执行结果：

```
cardinality: 18961805
rb size= 3752860
```


我们看到集合中一共加入近1900w个数，roaring bitmap总共占用了3.6MB的内存空间，这个和非压缩bitmap没有拉开差距。

下面是一个连续的3000w数字的集合到roaring bitmap的映射示例：

```
func main() {
rb := roaring.NewBitmap()
for i := 0; i < 30000000; i++ {
rb.Add(uint32(i))
}
fmt.Println("cardinality:", rb.GetCardinality())
fmt.Println("rb size=", rb.GetSizeInBytes())
}
```


其执行结果如下：

```
cardinality: 30000000
rb size= 21912
```


显然针对这样的连续数字集合，roaring bitmap的空间效率体现的十分明显。

### 五. roaring bitmap的序列化

以上是对roaring bitmap的粗浅入门介绍，如果对roaring bitmap感兴趣，可以去其官方站点或开源项目主页做深入了解和学习。不过这里我要说的是roaring bitmap的序列化问题(序列化后便可以传输和持久化存储了)，以序列化为JSON和从JSON反序列化为例。

考虑到性能问题，json序列化我选择的是[字节开源的sonic项目](https://github.com/bytedance/sonic)。sonic虽然说是一个Go开源项目，但由于其对JSON解析的极致优化的要求，目前该项目中Go代码的占比仅有30%不到，60%多都是**汇编代码**。sonic提供与Go标准库json包兼容的函数接口，并且sonic还支持streaming I/O模式，支持将特定类型对象序列化到io.Writer或从io.Reader中反序列化数据为一个特定类型对象，这个也是标准库json包所不支持的。当遇到超大JSON时，streaming I/O模式十分惯用，io.Writer和Reader可以让你的Go应用不至于瞬间分配大量内存，甚至被oom killed掉。

不过roaring bitmap并没有原生提供序列化(marshal)到JSON(或反向序列化)的函数/方法，那么我们如何将一个roaring bitmap序列化为一个JSON文本呢？Go标准库json包提供了Marshaler和Unmarshaler接口，凡是实现了这两个接口的自定义类型，json包都可以支持该自定义类型的序列化和反序列化。在这方面，**sonic项目与Go标准库json包保持兼容**。

不过roaring.Bitmap类型并没有实现Marshaler和Unmarshaler接口，roaring.Bitmap的序列化和反序列化需要我们自己来完成。

那么，我们首先想到的就是基于roaring.Bitmap自定义一个新类型，比如MyRB：

```
// https://github.com/bigwhite/experiments/blob/master/roaring-bitmap-examples/bitmap_json.go
type MyRB struct {
RB *roaring.Bitmap
}
```


然后，我们给出MyRB的MarshalJSON和UnmarshalJSON方法的实现以满足Marshaler和Unmarshaler接口的要求：

```
// https://github.com/bigwhite/experiments/blob/master/roaring-bitmap-examples/bitmap_json.go
func (rb *MyRB) MarshalJSON() ([]byte, error) {
s, err := rb.RB.ToBase64()
if err != nil {
return nil, err
}
r := fmt.Sprintf(`{"rb":"%s"}`, s)
return []byte(r), nil
}
func (rb *MyRB) UnmarshalJSON(data []byte) error {
// data => {"rb":"OjAAAAEAAAAAAB4AEAAAAAAAAQACAAMABAAFAAYABwAIAAkACgALAAwADQAOAA8AEAARABIAEwAUABUAFgAXABgAGQAaABsAHAAdAB4A"}
_, err := rb.RB.FromBase64(string(data[7 : len(data)-2]))
if err != nil {
return err
}
return nil
}
```


我们利用roaring.Bitmap提供的ToBase64方法将roaring bitmap转换为一个base64字符串，然后再序列化为JSON；反序列化则是利用FromBase64对JSON数据进行解码。下面我们测试一下MyRB类型与JSON间的相互转换：

```
// https://github.com/bigwhite/experiments/blob/master/roaring-bitmap-examples/bitmap_json.go
func main() {
var myrb = MyRB{
RB: roaring.NewBitmap(),
}
for i := 0; i < 31; i++ {
myrb.RB.Add(uint32(i))
}
fmt.Printf("the cardinality of origin bitmap = %d\n", myrb.RB.GetCardinality())
buf, err := sonic.Marshal(&myrb)
if err != nil {
panic(err)
}
fmt.Printf("bitmap2json: %s\n", string(buf))
var myrb1 = MyRB{
RB: roaring.NewBitmap(),
}
err = sonic.Unmarshal(buf, &myrb1)
if err != nil {
panic(err)
}
fmt.Printf("after json2bitmap, the cardinality of new bitmap = %d\n", myrb1.RB.GetCardinality())
}
```


运行该示例：

```
the cardinality of origin bitmap = 31
bitmap2json: {"rb":"OjAAAAEAAAAAAB4AEAAAAAAAAQACAAMABAAFAAYABwAIAAkACgALAAwADQAOAA8AEAARABIAEwAUABUAFgAXABgAGQAaABsAHAAdAB4A"}
after json2bitmap, the cardinality of new bitmap = 31
```


输出结果符合预期。

基于支持序列化的MyRB，顺便我们再看一下sonic和标准库json的benchmark对比，我们编写一个简单的对比测试用例：

```
// https://github.com/bigwhite/experiments/blob/master/roaring-bitmap-examples/benchmark_test.go
type Foo struct {
N int `json:"num"`
Name string `json:"name"`
Addr string `json:"addr"`
Age string `json:"age"`
RB MyRB `json:"myrb"`
}
func BenchmarkSonicJsonEncode(b *testing.B) {
var f = Foo{
N: 5,
RB: MyRB{
RB: roaring.NewBitmap(),
},
}
for i := 0; i < 3000; i++ {
f.RB.RB.Add(uint32(i))
}
b.ReportAllocs()
b.ResetTimer()
for i := 0; i < b.N; i++ {
_, err := sonic.Marshal(&f)
if err != nil {
panic(err)
}
}
}
func BenchmarkSonicJsonDecode(b *testing.B) {
var f = Foo{
N: 5,
RB: MyRB{
RB: roaring.NewBitmap(),
},
}
for i := 0; i < 3000; i++ {
f.RB.RB.Add(uint32(i))
}
buf, err := sonic.Marshal(&f)
if err != nil {
panic(err)
}
var f1 = Foo{
RB: MyRB{
RB: roaring.NewBitmap(),
},
}
b.ReportAllocs()
b.ResetTimer()
for i := 0; i < b.N; i++ {
err = sonic.Unmarshal(buf, &f1)
if err != nil {
panic(err)
}
}
}
func BenchmarkStdJsonEncode(b *testing.B) {
var f = Foo{
N: 5,
RB: MyRB{
RB: roaring.NewBitmap(),
},
}
for i := 0; i < 3000; i++ {
f.RB.RB.Add(uint32(i))
}
b.ReportAllocs()
b.ResetTimer()
for i := 0; i < b.N; i++ {
_, err := json.Marshal(&f)
if err != nil {
panic(err)
}
}
}
func BenchmarkStdJsonDecode(b *testing.B) {
var f = Foo{
N: 5,
RB: MyRB{
RB: roaring.NewBitmap(),
},
}
for i := 0; i < 3000; i++ {
f.RB.RB.Add(uint32(i))
}
buf, err := json.Marshal(&f)
if err != nil {
panic(err)
}
var f1 = Foo{
RB: MyRB{
RB: roaring.NewBitmap(),
},
}
b.ReportAllocs()
b.ResetTimer()
for i := 0; i < b.N; i++ {
err = json.Unmarshal(buf, &f1)
if err != nil {
panic(err)
}
}
}
```


执行这个benchmark：

```
$go test -bench .
goos: darwin
goarch: amd64
pkg: demo
... ...
BenchmarkSonicJsonEncode-8 71176 16331 ns/op 49218 B/op 13 allocs/op
BenchmarkSonicJsonDecode-8 85080 13710 ns/op 37236 B/op 11 allocs/op
BenchmarkStdJsonEncode-8 24490 49345 ns/op 47409 B/op 10 allocs/op
BenchmarkStdJsonDecode-8 20083 59593 ns/op 29000 B/op 15 allocs/op
PASS
ok demo 6.166s
```


从我们这个benchmark结果可以看到，sonic要比标准库json包快3-4倍。

本文中代码可以到[这里](https://github.com/bigwhite/experiments/blob/master/roaring-bitmap-examples)下载。

### 六. 参考资料

- Roaring Bitmap : June 2015 report - https://es.slideshare.net/lemire/roaringprezi-49478534
- Roaring Bitmap官网 - https://roaringbitmap.org/
- Roaring Bitmap Spec - https://github.com/RoaringBitmap/RoaringFormatSpec
- Roaring Bitmap Go实现 - https://github.com/RoaringBitmap/roaring
- 字节跳动的sonic项目 - https://github.com/bytedance/sonic
- paper: Consistently faster and smaller compressed bitmaps with Roaring - https://arxiv.org/pdf/1603.06549.pdf
- 基于Bitmap的精确去重和用户行为分析 - http://ai.baidu.com/forum/topic/show/987701
- paper: Roaring Bitmaps: Implementation of an Optimized Software Library - https://arxiv.org/pdf/1709.07821.pdf

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 - https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论