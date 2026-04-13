---
title: 惊！Go在十亿次循环和百万任务中表现不如Java，究竟为何？
url: https://tonybai.com/2024/12/02/why-go-sucks/
published: '2024-12-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 惊！Go在十亿次循环和百万任务中表现不如Java，究竟为何？

![](../../assets/7f90389bfa4514ba.png)


[本文永久链接](https://tonybai.com/2024/12/02/why-go-sucks) – https://tonybai.com/2024/12/02/why-go-sucks

编程语言比较的话题总是能吸引程序员的眼球！

近期外网的两篇编程语言对比的文章在国内程序员圈里引起热议。一篇是由[Ben Dicken (@BenjDicken)](https://benjdd.com) 做的[语言性能测试](https://benjdd.com/languages/)，对比了十多种主流语言在执行10亿次循环(一个双层循环：1万 * 10 万)的速度；另一篇则是一个名为hez2010的开发者做的[内存开销测试](https://hez2010.github.io/async-runtimes-benchmarks-2024/)，对比了多种语言在处理百万任务时的内存开销。

下面是这两项测试的结果示意图：

![](../../assets/c984c246a1d47579.png)



![](../../assets/c24e4138fb6468b3.png)



我们看到：在这两项测试中，Go的表现不仅远不及NonGC的C/Rust，甚至还落后于Java，尤其是在内存开销测试中，Go的内存使用显著高于以“吃内存”著称的Java。这一结果让许多开发者感到意外，因为Go通常被认为是轻量级的语言，然而实际的测试结果却揭示了其在高并发场景下的“内存效率不足”。

那么究竟为何在这两项测试中，Go的表现都不及预期呢？在这篇文章中，我将探讨可能的原因，以供大家参考。

我们先从**十亿次循环测试**开始。

## 1. 循环测试跑的慢，都因编译器优化还不够

下面是作者给出的[Go测试程序](https://github.com/bddicken/languages/blob/main/loops/go/code.go)：

```
// why-go-sucks/billion-loops/go/code.go
package main
import (
"fmt"
"math/rand"
"os"
"strconv"
)
func main() {
input, e := strconv.Atoi(os.Args[1]) // Get an input number from the command line
if e != nil {
panic(e)
}
u := int32(input)
r := int32(rand.Intn(10000)) // Get a random number 0 <= r < 10k
var a [10000]int32 // Array of 10k elements initialized to 0
for i := int32(0); i < 10000; i++ { // 10k outer loop iterations
for j := int32(0); j < 100000; j++ { // 100k inner loop iterations, per outer loop iteration
a[i] = a[i] + j%u // Simple sum
}
a[i] += r // Add a random value to each element in array
}
fmt.Println(a[r]) // Print out a single element from the array
}
```


这段代码通过命令行参数获取一个整数，然后生成一个随机数，接着通过两层循环对一个数组的每个元素进行累加，最终输出该数组中以随机数为下标对应的数组元素的值。

我们再来看一下”竞争对手”的测试代码。C测试代码如下：

```
// why-go-sucks/billion-loops/c/code.c
#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
int main (int argc, char** argv) {
int u = atoi(argv[1]); // Get an input number from the command line
int r = rand() % 10000; // Get a random integer 0 <= r < 10k
int32_t a[10000] = {0}; // Array of 10k elements initialized to 0
for (int i = 0; i < 10000; i++) { // 10k outer loop iterations
for (int j = 0; j < 100000; j++) { // 100k inner loop iterations, per outer loop iteration
a[i] = a[i] + j%u; // Simple sum
}
a[i] += r; // Add a random value to each element in array
}
printf("%d\n", a[r]); // Print out a single element from the array
}
```


下面是Java的测试代码：

```
// why-go-sucks/billion-loops/java/code.java
package jvm;
import java.util.Random;
public class code {
public static void main(String[] args) {
var u = Integer.parseInt(args[0]); // Get an input number from the command line
var r = new Random().nextInt(10000); // Get a random number 0 <= r < 10k
var a = new int[10000]; // Array of 10k elements initialized to 0
for (var i = 0; i < 10000; i++) { // 10k outer loop iterations
for (var j = 0; j < 100000; j++) { // 100k inner loop iterations, per outer loop iteration
a[i] = a[i] + j % u; // Simple sum
}
a[i] += r; // Add a random value to each element in array
}
System.out.println(a[r]); // Print out a single element from the array
}
}
```


你可能不熟悉C或Java，但从代码的形式上来看，C、Java与Go的代码确实处于“同等条件”。这不仅意味着它们在相同的硬件和软件环境中运行，更包括它们采用了相同的计算逻辑和算法，以及一致的输入参数处理等方面的相似性。

为了确认一下原作者的测试结果，我在一台阿里云ECS上(amd64，8c32g，CentOS 7.9)对上面三个程序进行了测试(使用time命令测量计算耗时)，得到一个基线结果。我的环境下，C、Java和Go的编译器版本如下：

```
$go version
go version go1.23.0 linux/amd64
$java -version
openjdk version "17.0.9" 2023-10-17 LTS
OpenJDK Runtime Environment Zulu17.46+19-CA (build 17.0.9+8-LTS)
OpenJDK 64-Bit Server VM Zulu17.46+19-CA (build 17.0.9+8-LTS, mixed mode, sharing)
$gcc -v
使用内建 specs。
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-redhat-linux/4.8.5/lto-wrapper
目标：x86_64-redhat-linux
配置为：../configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap --enable-shared --enable-threads=posix --enable-checking=release --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-linker-hash-style=gnu --enable-languages=c,c++,objc,obj-c++,java,fortran,ada,go,lto --enable-plugin --enable-initfini-array --disable-libgcj --with-isl=/builddir/build/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/isl-install --with-cloog=/builddir/build/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/cloog-install --enable-gnu-indirect-function --with-tune=generic --with-arch_32=x86-64 --build=x86_64-redhat-linux
线程模型：posix
gcc 版本 4.8.5 20150623 (Red Hat 4.8.5-44) (GCC)
```


测试步骤与结果如下：

```
Go代码测试：
$cd why-go-sucks/billion-loops/go
$go build -o code code.go
$time ./code 10
456953
real 0m3.766s
user 0m3.767s
sys 0m0.007s
C代码测试：
$cd why-go-sucks/billion-loops/c
$gcc -O3 -std=c99 -o code code.c
$time ./code 10
459383
real 0m3.005s
user 0m3.005s
sys 0m0.000s
Java代码测试：
$javac -d . code.java
$time java -cp . jvm.code 10
456181
real 0m3.105s
user 0m3.092s
sys 0m0.027s
```


从测试结果看到(基于real时间)：采用-O3优化的C代码最快，Java落后一个身位，而**Go则比C慢了25%，比Java慢了21%**。

注：time命令的输出结果通常包含三个主要部分：real、user和sys。real是从命令开始执行到结束所经过的实际时间（墙钟时间），我们依次指标为准。user是程序在

用户模式下执行所消耗的CPU时间。sys则是程序在内核模式下执行所消耗的CPU时间（系统调用）。如果总时间（real）略低于用户时间（user），这表明程序可能在某些时刻被调度或等待，而不是持续占用CPU。这种情况可能是由于输入输出操作、等待资源等原因。如果real时间显著小于user时间，这种情况通常发生在并发程序中，其中多个线程或进程在不同的时间段执行，导致总的用户CPU时间远大于实际的墙钟时间。sys时间保持较低，说明系统调用的频率较低，程序主要是执行计算而非进行大量的系统交互。

这时作为Gopher的你可能会说：**原作者编写的Go测试代码不够优化，我们能优化到比C还快**！

大家都知道原代码是不够优化的，随意改改计算逻辑就能带来大幅提升。但我们不能忘了“同等条件”这个前提。你采用的优化方法，其他语言（C、Java）也可以采用。

那么，在不改变“同等条件”的前提下，我们还能优化点啥呢？本着能提升一点是一点的思路，我们尝试从下面几个点优化一下，看看效果：

- 去除不必要的if判断
- 使用更快的rand实现
- 关闭边界检查
- 避免逃逸

下面是修改之后的代码：

```
// why-go-sucks/billion-loops/go/code_optimize.go
package main
import (
"fmt"
"math/rand"
"os"
"strconv"
)
func main() {
input, _ := strconv.Atoi(os.Args[1]) // Get an input number from the command line
u := int32(input)
r := int32(rand.Uint32() % 10000) // Use Uint32 for faster random number generation
var a [10000]int32 // Array of 10k elements initialized to 0
for i := int32(0); i < 10000; i++ { // 10k outer loop iterations
for j := int32(0); j < 100000; j++ { // 100k inner loop iterations, per outer loop iteration
a[i] = a[i] + j%u // Simple sum
}
a[i] += r // Add a random value to each element in array
}
z := a[r]
fmt.Println(z) // Print out a single element from the array
}
```


我们编译并运行一下测试：

```
$cd why-go-sucks/billion-loops/go
$go build -o code_optimize -gcflags '-B' code_optimize.go
$time ./code_optimize 10
459443
real 0m3.761s
user 0m3.759s
sys 0m0.011s
```


对比一下最初的测试结果，这些“所谓的优化”没有什么卵用，优化前你估计也能猜测到这个结果，因为除了关闭边界检查，其他优化都**没有处于循环执行的热路径之上**。

注：rand.Uint32() % 10000的确要比rand.Intn(10000)快，我自己的benchmark结果是快约1倍。


那Go程序究竟慢在哪里呢？在“同等条件”下，我能想到的只能是**Go编译器后端在代码优化方面优化做的还不够**，相较于GCC、Java等老牌编译器还有明显差距。

比如说，原先的代码中在内层循环中频繁访问a[i]，导致数组访问的读写操作较多（从内存加载a[i]，更新值后写回）。GCC和Java编译器在后端很可能做了这样的优化：将数组元素累积到一个临时变量中，并在外层循环结束后写回数组，这样做可以**减少内层循环中的内存读写操作，充分利用CPU缓存和寄存器，加速数据处理**。

注：数组从内存或缓存读，而一个临时变量很大可能是从寄存器读，那读取速度相差还是很大的。


如果我们手工在Go中实施这一优化，看看能达到什么效果呢？我们改一下最初版本的Go代码(code.go)，新代码如下：

```
// why-go-sucks/billion-loops/go/code_local_var.go
package main
import (
"fmt"
"math/rand"
"os"
"strconv"
)
func main() {
input, e := strconv.Atoi(os.Args[1]) // Get an input number from the command line
if e != nil {
panic(e)
}
u := int32(input)
r := int32(rand.Intn(10000)) // Get a random number 0 <= r < 10k
var a [10000]int32 // Array of 10k elements initialized to 0
for i := int32(0); i < 10000; i++ { // 10k outer loop iterations
temp := a[i]
for j := int32(0); j < 100000; j++ { // 100k inner loop iterations, per outer loop iteration
temp += j % u // Simple sum
}
temp += r // Add a random value to each element in array
a[i] = temp
}
fmt.Println(a[r]) // Print out a single element from the array
}
```


编译并运行测试：

```
$go build -o code_local_var code_local_var.go
$time ./code_local_var 10
459169
real 0m3.017s
user 0m3.017s
sys 0m0.007s
```


我们看到，测试结果直接就比Java略好一些了。显然Go编译器没有做这种优化，从code.go的汇编也大致可以看出来：

![](../../assets/094b7e4c7d792ae9.png)



[lensm](https://github.com/loov/lensm)生成的汇编与go源码对应关系

而Java显然做了这类优化，我们在原Java代码版本上按上述优化逻辑修改了一下：

```
// why-go-sucks/billion-loops/java/code_local_var.java
package jvm;
import java.util.Random;
public class code {
public static void main(String[] args) {
var u = Integer.parseInt(args[0]); // 获取命令行输入的整数
var r = new Random().nextInt(10000); // 生成随机数 0 <= r < 10000
var a = new int[10000]; // 定义长度为10000的数组a
for (var i = 0; i < 10000; i++) { // 10k外层循环迭代
var temp = a[i]; // 使用临时变量存储 a[i] 的值
for (var j = 0; j < 100000; j++) { // 100k内层循环迭代，每次外层循环迭代
temp += j % u; // 更新临时变量的值
}
a[i] = temp + r; // 将临时变量的值加上 r 并写回数组
}
System.out.println(a[r]); // 输出 a[r] 的值
}
}
```


但从运行这个“优化”后的程序的结果来看，其对java代码的提升幅度几乎可以忽略不计：

```
$time java -cp . jvm.code 10
450375
real 0m3.043s
user 0m3.028s
sys 0m0.027s
```


这也直接证明了即便采用的是原版java代码，java编译器也会生成带有抽取局部变量这种优化的可执行代码，java程序员无需手工进行此类优化。

像这种编译器优化，还有不少，比如大家比较熟悉的循环展开(Loop Unrolling)也可以提升Go程序的性能：

```
// why-go-sucks/billion-loops/go/code_loop_unrolling.go
package main
import (
"fmt"
"math/rand"
"os"
"strconv"
)
func main() {
input, e := strconv.Atoi(os.Args[1]) // Get an input number from the command line
if e != nil {
panic(e)
}
u := int32(input)
r := int32(rand.Intn(10000)) // Get a random number 0 <= r < 10k
var a [10000]int32 // Array of 10k elements initialized to 0
for i := int32(0); i < 10000; i++ { // 10k outer loop iterations
var sum int32
// Unroll inner loop in chunks of 4 for optimization
for j := int32(0); j < 100000; j += 4 {
sum += j % u
sum += (j + 1) % u
sum += (j + 2) % u
sum += (j + 3) % u
}
a[i] = sum + r // Add the accumulated sum and random value
}
fmt.Println(a[r]) // Print out a single element from the array
}
```


运行这个Go测试程序，性能如下：

```
$go build -o code_loop_unrolling code_loop_unrolling.go
$time ./code_loop_unrolling 10
458908
real 0m2.937s
user 0m2.940s
sys 0m0.002s
```


循环展开可以增加指令级并行性，因为展开后的代码块中可以有更多的独立指令，比如示例中的计算j % u、(j+1) % u、(j+2) % u和(j+3) % u，这些计算操作是独立的，可以并行执行，打破了依赖链，从而更好地利用处理器的并行流水线。而原版Go代码中，每次迭代都会根据前一次迭代的结果更新a[i]，形成一个依赖链，这种顺序依赖性迫使处理器只能按顺序执行这些指令，导致流水线停顿。

不过其他语言也可以做同样的手工优化，比如我们对C代码做同样的优化(why-go-sucks/billion-loops/c/code_loop_unrolling.c)，c测试程序的性能可以提升至2.7s水平，这也证明了初版C程序即便在-O3的情况下编译器也没有自动为其做这个优化：

```
$time ./code_loop_unrolling 10
459383
real 0m2.723s
user 0m2.722s
sys 0m0.001s
```


到这里我们就不再针对这个10亿次循环的性能问题做进一步展开了，从上面的探索得到的初步结论就是**Go编译器优化做的还不到位所致**，期待后续Go团队能在编译器优化方面投入更多精力，争取早日追上GCC/Clang、Java这些成熟的编译器优化水平。

下面我们再来看Go在百万任务场景下内存开销大的“问题”。

## 2. 内存占用高，问题出在Goroutine实现原理

我们先来看第二个问题的测试代码：

```
package main
import (
"fmt"
"os"
"strconv"
"sync"
"time"
)
func main() {
numRoutines := 100000
if len(os.Args) > 1 {
n, err := strconv.Atoi(os.Args[1])
if err == nil {
numRoutines = n
}
}
var wg sync.WaitGroup
for i := 0; i < numRoutines; i++ {
wg.Add(1)
go func() {
time.Sleep(10 * time.Second)
wg.Done()
}()
}
wg.Wait()
}
```


这个代码其实就是根据传入的task数量启动等同数量的goroutine，然后每个goroutine模拟工作负载sleep 10s，这等效于百万长连接的场景，只有连接，但没有收发消息。

相对于上一个问题，这个问题更好解释一些。

Go使用的groutine是一种有栈协程，文章中使用的是每个task一个goroutine的模型，且维护百万任务一段时间，这会真实创建百万个goroutine（G数据结构），并为其分配栈空间(2k起步)，这样你可以算一算，不考虑其他结构的占用，仅每个goroutine的栈空间所需的内存都是极其可观的：

```
mem = 1000000 * 2000 Bytes = 2000000000 Bytes = 2G Bytes
```


所以启动100w goroutine，保底就2GB内存出去了，这与原作者测试的结果十分契合(原文是2.5GB多)。并且，内存还会随着goroutine数量增长而线性增加。

那么如何能减少内存使用呢？如果采用每个task一个goroutine的模型，这个内存占用很难省去，除非将来Go团队对goroutine实现做大修。

如果task是网络通信相关的，可以使用类似gnet这样的直接基于epoll建构的框架，其主要的节省在于不会启动那么多goroutine，而是通过一个goroutine池来处理数据，每个池中的goroutine负责一批网络连接或网络请求。

在一些Gopher的印象中，Goroutine一旦分配就不回收，这会使他们会误认为一旦分配了100w goroutine，这2.5G内存空间将始终被占用，真实情况是这样么？我们用一个示例程序验证一下就好了：

```
// why-go-sucks/million-tasks/million-tasks.go
package main
import (
"fmt"
"log"
"os"
"os/signal"
"runtime"
"sync"
"syscall"
"time"
)
// 打印当前内存使用情况和相关信息
func printMemoryUsage() {
var m runtime.MemStats
runtime.ReadMemStats(&m)
// 获取当前 goroutine 数量
numGoroutines := runtime.NumGoroutine()
// 获取当前线程数量
numThreads := runtime.NumCPU() // Go runtime 不直接提供线程数量，但可以通过 NumCPU 获取逻辑处理器数量
fmt.Printf("======>\n")
fmt.Printf("Alloc = %v MiB", bToMb(m.Alloc))
fmt.Printf("\tTotalAlloc = %v MiB", bToMb(m.TotalAlloc))
fmt.Printf("\tSys = %v MiB", bToMb(m.Sys))
fmt.Printf("\tNumGC = %v", m.NumGC)
fmt.Printf("\tNumGoroutines = %v", numGoroutines)
fmt.Printf("\tNumThreads = %v\n", numThreads)
fmt.Printf("<======\n\n")
}
// 将字节转换为 MB
func bToMb(b uint64) uint64 {
return b / 1024 / 1024
}
func main() {
const signal1Goroutines = 900000
const signal2Goroutines = 90000
const signal3Goroutines = 10000
// 用于接收退出信号
sigChan := make(chan os.Signal, 1)
signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
// 控制 goroutine 的退出
signal1Chan := make(chan struct{})
signal2Chan := make(chan struct{})
signal3Chan := make(chan struct{})
var wg sync.WaitGroup
ticker := time.NewTicker(5 * time.Second)
go func() {
for range ticker.C {
printMemoryUsage()
}
}()
// 等待退出信号
go func() {
count := 0
for {
<-sigChan
count++
if count == 1 {
log.Println("收到第一类goroutine退出信号")
close(signal1Chan) // 关闭 signal1Chan，通知第一类 goroutine 退出
continue
}
if count == 2 {
log.Println("收到第二类goroutine退出信号")
close(signal2Chan) // 关闭 signal2Chan，通知第二类 goroutine 退出
continue
}
log.Println("收到第三类goroutine退出信号")
close(signal3Chan) // 关闭 signal3Chan，通知第三类 goroutine 退出
return
}
}()
// 启动第一类 goroutine（在收到 signal1 时退出）
log.Println("开始启动第一类goroutine...")
for i := 0; i < signal1Goroutines; i++ {
wg.Add(1)
go func(id int) {
defer wg.Done()
// 模拟工作
for {
select {
case <-signal1Chan:
return
default:
time.Sleep(10 * time.Second) // 模拟一些工作
}
}
}(i)
}
log.Println("启动第一类goroutine(900000) ok")
time.Sleep(time.Second * 5)
// 启动第二类 goroutine（在收到 signal2 时退出）
log.Println("开始启动第二类goroutine...")
for i := 0; i < signal2Goroutines; i++ {
wg.Add(1)
go func(id int) {
defer wg.Done()
// 模拟工作
for {
select {
case <-signal2Chan:
return
default:
time.Sleep(10 * time.Second) // 模拟一些工作
}
}
}(i)
}
log.Println("启动第二类goroutine(90000) ok")
time.Sleep(time.Second * 5)
// 启动第三类goroutine（随程序退出而退出）
log.Println("开始启动第三类goroutine...")
for i := 0; i < signal3Goroutines; i++ {
wg.Add(1)
go func(id int) {
defer wg.Done()
// 模拟工作
for {
select {
case <-signal3Chan:
return
default:
time.Sleep(10 * time.Second) // 模拟一些工作
}
}
}(i)
}
log.Println("启动第三类goroutine(90000) ok")
// 等待所有 goroutine 完成
wg.Wait()
fmt.Println("所有 goroutine 已退出，程序结束")
}
```


这个程序我就不详细解释了。大致分三类goroutine，第一类90w个，在我发送第一个ctrl+c信号后退出，第二类9w个，在我发送第二个ctrl+c信号后退出，最后一类1w个，随着程序退出而退出。

在我的执行环境下编译和执行一下这个程序，并结合runtime输出以及使用top -p pid的方式查看其内存占用：

```
$go build million-tasks.go
$./million-tasks
2024/12/01 22:07:03 开始启动第一类goroutine...
2024/12/01 22:07:05 启动第一类goroutine(900000) ok
======>
Alloc = 511 MiB TotalAlloc = 602 MiB Sys = 2311 MiB NumGC = 9 NumGoroutines = 900004 NumThreads = 8
<======
2024/12/01 22:07:10 开始启动第二类goroutine...
2024/12/01 22:07:11 启动第二类goroutine(90000) ok
======>
Alloc = 577 MiB TotalAlloc = 668 MiB Sys = 2553 MiB NumGC = 9 NumGoroutines = 990004 NumThreads = 8
<======
2024/12/01 22:07:16 开始启动第三类goroutine...
2024/12/01 22:07:16 启动第三类goroutine(90000) ok
======>
Alloc = 597 MiB TotalAlloc = 688 MiB Sys = 2593 MiB NumGC = 9 NumGoroutines = 1000004 NumThreads = 8
<======
======>
Alloc = 600 MiB TotalAlloc = 690 MiB Sys = 2597 MiB NumGC = 9 NumGoroutines = 1000004 NumThreads = 8
<======
... ...
======>
Alloc = 536 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 10 NumGoroutines = 1000004 NumThreads = 8
<======
```


100w goroutine全部创建ok后，我们查看一下top输出：

```
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
5800 root 20 0 3875556 2.5g 988 S 54.0 8.2 0:30.92 million-tasks
```


我们看到RES为2.5g，和我们预期的一致！

接下来，我们停掉第一批90w个goroutine，看RES是否会下降，何时会下降！

输入ctrl+c，停掉第一批90w goroutine：

```
^C2024/12/01 22:10:15 收到第一类goroutine退出信号
======>
Alloc = 536 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 10 NumGoroutines = 723198 NumThreads = 8
<======
======>
Alloc = 536 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 10 NumGoroutines = 723198 NumThreads = 8
<======
======>
Alloc = 536 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 10 NumGoroutines = 100004 NumThreads = 8
<======
======>
Alloc = 536 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 10 NumGoroutines = 100004 NumThreads = 8
<======
... ...
```


但同时刻的top显示RES并没有变化：

```
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
5800 root 20 0 3875812 2.5g 988 S 0.0 8.2 0:56.38 million-tasks
```


等待两个GC间隔的时间后(大约4分)，Goroutine的栈空间被释放：

```
======>
Alloc = 465 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 12 NumGoroutines = 100004 NumThreads = 8
<======
======>
Alloc = 465 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 12 NumGoroutines = 100004 NumThreads = 8
<======
======>
Alloc = 465 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 12 NumGoroutines = 100004 NumThreads = 8
<======
======>
Alloc = 465 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 12 NumGoroutines = 100004 NumThreads = 8
<======
```


top显示RES从2.5g下降为大概700多MB（RES的单位是KB）：

```
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
5800 root 20 0 3875812 764136 992 S 0.0 2.4 1:01.87 million-tasks
```


接下来，我们再停掉第二批9w goroutine：

```
^C2024/12/01 22:16:21 收到第二类goroutine退出信号
======>
Alloc = 465 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 13 NumGoroutines = 100004 NumThreads = 8
<======
======>
Alloc = 465 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 13 NumGoroutines = 100004 NumThreads = 8
<======
======>
Alloc = 465 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 13 NumGoroutines = 10004 NumThreads = 8
<======
======>
Alloc = 465 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 13 NumGoroutines = 10004 NumThreads = 8
<======
```


此时，top值也没立即改变：

```
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
5800 root 20 0 3875812 764136 992 S 0.0 2.4 1:05.99 million-tasks
```


大约等待一个GC间隔(2分钟)后，top中RES下降：

```
======>
Alloc = 458 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 14 NumGoroutines = 10004 NumThreads = 8
<======
======>
Alloc = 458 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 14 NumGoroutines = 10004 NumThreads = 8
<======
======>
Alloc = 458 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 14 NumGoroutines = 10004 NumThreads = 8
<======
```


RES变为不到700M：

```
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
5800 root 20 0 3875812 699156 992 S 0.0 2.2 1:06.75 million-tasks
```


第三次按下ctrl+c，程序退出：

```
^C2024/12/01 22:18:46 收到第三类goroutine退出信号
======>
Alloc = 458 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 14 NumGoroutines = 10003 NumThreads = 8
<======
======>
Alloc = 458 MiB TotalAlloc = 695 MiB Sys = 2606 MiB NumGC = 14 NumGoroutines = 10003 NumThreads = 8
<======
所有 goroutine 已退出，程序结束
```


我们看到Go是会回收goroutine占用的内存空间的，并且归还给OS，只是这种归还比较lazy。尤其是，第二次停止goroutine前，go程序剩下10w goroutine，按理论来讲需占用大约200MB的空间，实际上却是700多MB；第二次停止goroutine后，goroutine数量降为1w，理论占用应该在20MB，但实际却是600多MB，我们看到go运行时这种lazy归还OS内存的行为可能也是“故意为之”，是为了避免反复从OS申请和归还内存。

## 3. 小结

本文主要探讨了Go语言在十亿次循环和百万任务的测试中的表现令人意外地逊色于Java和C语言的原因。我认为Go在循环执行中的慢速表现，主要是其编译器优化不足，影响了执行效率。 而在内存开销方面，Go的Goroutine实现是使得内存使用量大幅增加的“罪魁祸首”，这是由于每个Goroutine初始都会分配固定大小的栈空间。

通过本文的探讨，我的主要目的是希望大家不要以讹传讹，而是要搞清楚背后的真正原因，并正视Go在某些方面的不足，以及其当前在某些应用上下文中的局限性。 同时，也希望Go开发团队在编译器优化方面进行更多投入，以提升Go在高性能计算领域的竞争力。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/why-go-sucks)下载。

## 4. 参考资料

[Billion nested loop iterations](https://benjdd.com/languages/)– https://benjdd.com/languages/[How Much Memory Do You Need in 2024 to Run 1 Million Concurrent Tasks?](https://hez2010.github.io/async-runtimes-benchmarks-2024/)– https://hez2010.github.io/async-runtimes-benchmarks-2024/

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

关于编译优化这块，博主是否可以分享一些经验：

1. 对比 go、java、gcc/clang 等在编译优化方法；

2. go 性能调优经验。

持续关注或订阅我的博客或我的微信公众号吧，后续会有相关的文章输出:)。