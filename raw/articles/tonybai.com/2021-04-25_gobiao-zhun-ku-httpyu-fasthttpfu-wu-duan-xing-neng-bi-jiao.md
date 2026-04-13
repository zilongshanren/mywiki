---
title: Go标准库http与fasthttp服务端性能比较
url: https://tonybai.com/2021/04/25/server-side-performance-nethttp-vs-fasthttp/
published: '2021-04-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go标准库http与fasthttp服务端性能比较

![](../../assets/d9ce2a35c9e8b347.png)


[本文永久链接](https://tonybai.com/2021/04/25/server-side-performance-nethttp-vs-fasthttp) – https://tonybai.com/2021/04/25/server-side-performance-nethttp-vs-fasthttp

### 1. 背景

Go初学者学习Go时，在编写了经典的“hello, world”程序之后，可能会迫不及待的体验一下Go强大的标准库，比如：用几行代码写一个像下面示例这样拥有完整功能的web server：

```
// 来自https://tip.golang.org/pkg/net/http/#example_ListenAndServe
package main
import (
"io"
"log"
"net/http"
)
func main() {
helloHandler := func(w http.ResponseWriter, req *http.Request) {
io.WriteString(w, "Hello, world!\n")
}
http.HandleFunc("/hello", helloHandler)
log.Fatal(http.ListenAndServe(":8080", nil))
}
```


go net/http包是一个比较**均衡**的通用实现，能满足大多数gopher 90%以上场景的需要，并且具有如下优点：

- 标准库包，无需引入任何第三方依赖；
- 对http规范的满足度较好；
- 无需做任何优化，即可获得相对较高的性能；
- 支持HTTP代理；
- 支持HTTPS；
- 无缝支持HTTP/2。

不过也正是因为http包的“均衡”通用实现，在一些对性能要求严格的领域，net/http的性能可能无法胜任，也没有太多的调优空间。这时我们会将眼光转移到其他第三方的http服务端框架实现上。

而在第三方http服务端框架中，一个“行如其名”的框架[fasthttp](https://github.com/valyala/fasthttp)被提及和采纳的较多，fasthttp官网宣称**其性能是net/http的十倍**(基于go test benchmark的测试结果)。

fasthttp采用了许多[性能优化上的最佳实践](https://github.com/valyala/fasthttp#fasthttp-best-practices)，尤其是在内存对象的重用上，大量使用[sync.Pool](https://www.imooc.com/read/87/article/2432)以降低对Go GC的压力。

那么在真实环境中，到底fasthttp能比net/http快多少呢？恰好手里有两台性能还不错的服务器可用，在本文中我们就在这个真实环境下看看他们的实际性能。

### 2. 性能测试

我们分别用net/http和fasthttp实现两个几乎“零业务”的被测程序：

- nethttp:

```
// github.com/bigwhite/experiments/blob/master/http-benchmark/nethttp/main.go
package main
import (
_ "expvar"
"log"
"net/http"
_ "net/http/pprof"
"runtime"
"time"
)
func main() {
go func() {
for {
log.Println("当前routine数量:", runtime.NumGoroutine())
time.Sleep(time.Second)
}
}()
http.Handle("/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
w.Write([]byte("Hello, Go!"))
}))
log.Fatal(http.ListenAndServe(":8080", nil))
}
```


- fasthttp:

```
// github.com/bigwhite/experiments/blob/master/http-benchmark/fasthttp/main.go
package main
import (
"fmt"
"log"
"net/http"
"runtime"
"time"
_ "expvar"
_ "net/http/pprof"
"github.com/valyala/fasthttp"
)
type HelloGoHandler struct {
}
func fastHTTPHandler(ctx *fasthttp.RequestCtx) {
fmt.Fprintln(ctx, "Hello, Go!")
}
func main() {
go func() {
http.ListenAndServe(":6060", nil)
}()
go func() {
for {
log.Println("当前routine数量:", runtime.NumGoroutine())
time.Sleep(time.Second)
}
}()
s := &fasthttp.Server{
Handler: fastHTTPHandler,
}
s.ListenAndServe(":8081")
}
```


对被测目标实施压力测试的客户端，我们基于[hey](https://github.com/rakyll/hey)这个http压测工具进行，为了方便调整压力水平，我们将hey“包裹”在下面这个shell脚本中(仅适于在linux上运行)：

```
// github.com/bigwhite/experiments/blob/master/http-benchmark/client/http_client_load.sh
# ./http_client_load.sh 3 10000 10 GET http://10.10.195.181:8080
echo "$0 task_num count_per_hey conn_per_hey method url"
task_num=$1
count_per_hey=$2
conn_per_hey=$3
method=$4
url=$5
start=$(date +%s%N)
for((i=1; i<=$task_num; i++)); do {
tm=$(date +%T.%N)
echo "$tm: task $i start"
hey -n $count_per_hey -c $conn_per_hey -m $method $url > hey_$i.log
tm=$(date +%T.%N)
echo "$tm: task $i done"
} & done
wait
end=$(date +%s%N)
count=$(( $task_num * $count_per_hey ))
runtime_ns=$(( $end - $start ))
runtime=`echo "scale=2; $runtime_ns / 1000000000" | bc`
echo "runtime: "$runtime
speed=`echo "scale=2; $count / $runtime" | bc`
echo "speed: "$speed
```


该脚本的执行示例如下：

```
bash http_client_load.sh 8 1000000 200 GET http://10.10.195.134:8080
http_client_load.sh task_num count_per_hey conn_per_hey method url
16:58:09.146948690: task 1 start
16:58:09.147235080: task 2 start
16:58:09.147290430: task 3 start
16:58:09.147740230: task 4 start
16:58:09.147896010: task 5 start
16:58:09.148314900: task 6 start
16:58:09.148446030: task 7 start
16:58:09.148930840: task 8 start
16:58:45.001080740: task 3 done
16:58:45.241903500: task 8 done
16:58:45.261501940: task 1 done
16:58:50.032383770: task 4 done
16:58:50.985076450: task 7 done
16:58:51.269099430: task 5 done
16:58:52.008164010: task 6 done
16:58:52.166402430: task 2 done
runtime: 43.02
speed: 185960.01
```


从传入的参数来看，该脚本并行启动了8个task(一个task启动一个hey)，每个task向http://10.10.195.134:8080建立200个并发连接，并发送100w http GET请求。

我们使用两台服务器分别放置被测目标程序和压力工具脚本：

- 目标程序所在服务器：10.10.195.181(物理机，Intel x86-64 CPU，40核，128G内存, CentOs 7.6)

```
$ cat /etc/redhat-release
CentOS Linux release 7.6.1810 (Core)
$ lscpu
Architecture: x86_64
CPU op-mode(s): 32-bit, 64-bit
Byte Order: Little Endian
CPU(s): 40
On-line CPU(s) list: 0-39
Thread(s) per core: 2
Core(s) per socket: 10
座： 2
NUMA 节点： 2
厂商 ID： GenuineIntel
CPU 系列： 6
型号： 85
型号名称： Intel(R) Xeon(R) Silver 4114 CPU @ 2.20GHz
步进： 4
CPU MHz： 800.000
CPU max MHz: 2201.0000
CPU min MHz: 800.0000
BogoMIPS： 4400.00
虚拟化： VT-x
L1d 缓存： 32K
L1i 缓存： 32K
L2 缓存： 1024K
L3 缓存： 14080K
NUMA 节点0 CPU： 0-9,20-29
NUMA 节点1 CPU： 10-19,30-39
Flags: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch epb cat_l3 cdp_l3 intel_pt ssbd mba ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm cqm mpx rdt_a avx512f avx512dq rdseed adx smap clflushopt clwb avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts pku ospke spec_ctrl intel_stibp flush_l1d
```


- 压力工具所在服务器：10.10.195.133(物理机，鲲鹏arm64 cpu，96核，80G内存, CentOs 7.9)

```
# cat /etc/redhat-release
CentOS Linux release 7.9.2009 (AltArch)
# lscpu
Architecture: aarch64
Byte Order: Little Endian
CPU(s): 96
On-line CPU(s) list: 0-95
Thread(s) per core: 1
Core(s) per socket: 48
座： 2
NUMA 节点： 4
型号： 0
CPU max MHz: 2600.0000
CPU min MHz: 200.0000
BogoMIPS： 200.00
L1d 缓存： 64K
L1i 缓存： 64K
L2 缓存： 512K
L3 缓存： 49152K
NUMA 节点0 CPU： 0-23
NUMA 节点1 CPU： 24-47
NUMA 节点2 CPU： 48-71
NUMA 节点3 CPU： 72-95
Flags: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma dcpop asimddp asimdfhm
```


我用dstat监控被测目标所在主机资源占用情况(dstat -tcdngym)，尤其是cpu负荷；通过[expvarmon监控memstats](https://mp.weixin.qq.com/s/cr2JeUq5HOYQC0qji_Ip5g)，由于没有业务，内存占用很少；通过[go tool pprof](https://www.imooc.com/read/87/article/2440)查看目标程序中对各类资源消耗情况的排名。

下面是多次测试后制作的一个数据表格：

![](../../assets/fdadddef9e6e6d97.png)



### 3. 对结果的简要分析

受特定场景、测试工具及脚本精确性以及压力测试环境的影响，上面的测试结果有一定局限，但却真实反映了被测目标的性能趋势。我们看到在给予同样压力的情况下，fasthttp并没有10倍于net http的性能，甚至在这样一个特定的场景下，两倍于net/http的性能都没有达到：我们看到在目标主机cpu资源消耗接近70%的几个用例中，fasthttp的性能仅比net/http高出30%~70%左右。

那么为什么fasthttp的性能未及预期呢？要回答这个问题，那就要看看net/http和fasthttp各自的实现原理了！我们先来看看net/http的工作原理示意图：

![](../../assets/1cd554177975ac95.png)



http包作为server端的原理很简单，那就是accept到一个连接(conn)之后，将这个conn甩给一个worker goroutine去处理，后者一直存在，直到该conn的生命周期结束：即连接关闭。

下面是fasthttp的工作原理示意图：

![](../../assets/b81b56f5c0489dab.png)



而fasthttp设计了一套机制，目的是尽量复用goroutine，而不是每次都创建新的goroutine。fasthttp的Server accept一个conn之后，会尝试从workerpool中的ready切片中**取出**一个channel，该channel与某个worker goroutine一一对应。一旦**取出**channel，就会将accept到的conn写到该channel里，而channel另一端的worker goroutine就会处理该conn上的数据读写。当处理完该conn后，该worker goroutine不会退出，而是会将自己对应的那个channel重新**放回**workerpool中的ready切片中，等待这下一次被**取出**。

fasthttp的goroutine复用策略初衷很好，**但在这里的测试场景下效果不明显**，从测试结果便可看得出来，在相同的客户端并发和压力下，net/http使用的goroutine数量与fasthttp相差无几。这是由测试模型导致的：在我们这个测试中，每个task中的hey都会向被测目标发起固定数量的[长连接(keep-alive)](https://mp.weixin.qq.com/s/uH4lmsMs-hq5B3Ivq2jR5w)，然后在每条连接上发起“饱和”请求。这样fasthttp workerpool中的goroutine一旦接收到某个conn就只能在该conn上的通讯结束后才能重新放回，而该conn直到测试结束才会close，因此这样的场景相当于**让fasthttp“退化”成了net/http的模型**，也染上了net/http的“缺陷”：goroutine的数量一旦多起来，go runtime自身调度所带来的消耗便不可忽视甚至超过了业务处理所消耗的资源占比。下面分别是fasthttp在200长连接、8000长连接以及16000长连接下的cpu profile的结果：

```
200长连接：
(pprof) top -cum
Showing nodes accounting for 88.17s, 55.35% of 159.30s total
Dropped 150 nodes (cum <= 0.80s)
Showing top 10 nodes out of 60
flat flat% sum% cum cum%
0.46s 0.29% 0.29% 101.46s 63.69% github.com/valyala/fasthttp.(*Server).serveConn
0 0% 0.29% 101.46s 63.69% github.com/valyala/fasthttp.(*workerPool).getCh.func1
0 0% 0.29% 101.46s 63.69% github.com/valyala/fasthttp.(*workerPool).workerFunc
0.04s 0.025% 0.31% 89.46s 56.16% internal/poll.ignoringEINTRIO (inline)
87.38s 54.85% 55.17% 89.27s 56.04% syscall.Syscall
0.12s 0.075% 55.24% 60.39s 37.91% bufio.(*Writer).Flush
0 0% 55.24% 60.22s 37.80% net.(*conn).Write
0.08s 0.05% 55.29% 60.21s 37.80% net.(*netFD).Write
0.09s 0.056% 55.35% 60.12s 37.74% internal/poll.(*FD).Write
0 0% 55.35% 59.86s 37.58% syscall.Write (inline)
(pprof)
8000长连接：
(pprof) top -cum
Showing nodes accounting for 108.51s, 54.46% of 199.23s total
Dropped 204 nodes (cum <= 1s)
Showing top 10 nodes out of 66
flat flat% sum% cum cum%
0 0% 0% 119.11s 59.79% github.com/valyala/fasthttp.(*workerPool).getCh.func1
0 0% 0% 119.11s 59.79% github.com/valyala/fasthttp.(*workerPool).workerFunc
0.69s 0.35% 0.35% 119.05s 59.76% github.com/valyala/fasthttp.(*Server).serveConn
0.04s 0.02% 0.37% 104.22s 52.31% internal/poll.ignoringEINTRIO (inline)
101.58s 50.99% 51.35% 103.95s 52.18% syscall.Syscall
0.10s 0.05% 51.40% 79.95s 40.13% runtime.mcall
0.06s 0.03% 51.43% 79.85s 40.08% runtime.park_m
0.23s 0.12% 51.55% 79.30s 39.80% runtime.schedule
5.67s 2.85% 54.39% 77.47s 38.88% runtime.findrunnable
0.14s 0.07% 54.46% 68.96s 34.61% bufio.(*Writer).Flush
16000长连接：
(pprof) top -cum
Showing nodes accounting for 239.60s, 87.07% of 275.17s total
Dropped 190 nodes (cum <= 1.38s)
Showing top 10 nodes out of 46
flat flat% sum% cum cum%
0.04s 0.015% 0.015% 153.38s 55.74% runtime.mcall
0.01s 0.0036% 0.018% 153.34s 55.73% runtime.park_m
0.12s 0.044% 0.062% 153s 55.60% runtime.schedule
0.66s 0.24% 0.3% 152.66s 55.48% runtime.findrunnable
0.15s 0.055% 0.36% 127.53s 46.35% runtime.netpoll
127.04s 46.17% 46.52% 127.04s 46.17% runtime.epollwait
0 0% 46.52% 121s 43.97% github.com/valyala/fasthttp.(*workerPool).getCh.func1
0 0% 46.52% 121s 43.97% github.com/valyala/fasthttp.(*workerPool).workerFunc
0.41s 0.15% 46.67% 120.18s 43.67% github.com/valyala/fasthttp.(*Server).serveConn
111.17s 40.40% 87.07% 111.99s 40.70% syscall.Syscall
(pprof)
```


通过上述profile的比对，我们发现当长连接数量增多时(即workerpool中goroutine数量增多时），go runtime调度的占比会逐渐提升，在16000连接时，runtime调度的各个函数已经排名前4了。

### 4. 优化途径

从上面的测试结果，我们看到fasthttp的模型不太适合这种连接连上后进行持续“饱和”请求的场景，更适合短连接或长连接但没有持续饱和请求，在后面这样的场景下，它的goroutine复用模型才能更好的得以发挥。

但即便“退化”为了net/http模型，fasthttp的性能依然要比net/http略好，这是为什么呢？这些性能提升主要是fasthttp在内存分配层面的优化trick的结果，比如大量使用sync.Pool，比如避免在[]byte和string互转等。

那么，在持续“饱和”请求的场景下，如何让fasthttp workerpool中goroutine的数量不会因conn的增多而线性增长呢？fasthttp官方没有给出答案，但一条可以考虑的路径是使用os的多路复用(linux上的实现为epoll)，即go runtime netpoll使用的那套机制。在多路复用的机制下，这样可以让每个workerpool中的goroutine处理同时处理多个连接，这样我们可以根据业务规模选择workerpool池的大小，而不是像目前这样几乎是任意增长goroutine的数量。当然，在用户层面引入epoll也可能会带来系统调用占比的增多以及响应延迟增大等问题。至于该路径是否可行，还是要看具体实现和测试结果。

注：fasthttp.Server中的Concurrency可以用来限制workerpool中并发处理的goroutine的个数，但由于每个goroutine只处理一个连接，当Concurrency设置过小时，后续的连接可能就会被fasthttp拒绝服务。因此fasthttp的默认Concurrency为：


```
const DefaultConcurrency = 256 * 1024
```


本文涉及的源码可以在[这里](https://tonybai.com/github.com/bigwhite/experiments/blob/master/http-benchmark) github.com/bigwhite/experiments/blob/master/http-benchmark 下载。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

搜索点进来，看了几篇文章，发现质量好高！厉害！

写得不错，有自己的思考，蛮珍贵的。

“饱和”请求指的什么？ 能否举例说明

在文中，我所说的“饱和”指的是客户端与服务端建立connection后，持续不断的发送请求，绑定的goroutine持续处理这个conn的请求，没机会放回worker pool中。这样，fasthttp的“goroutine池”的意义就不那么明显了。基本上就“退化”成与net/http一样的处理模型了。