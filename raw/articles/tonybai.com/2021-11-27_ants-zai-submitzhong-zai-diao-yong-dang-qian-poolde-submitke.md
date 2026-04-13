---
title: ants：在Submit中再调用当前Pool的Submit可能导致阻塞
url: https://tonybai.com/2021/11/27/ants-call-submit-in-submit-may-cause-blocking/
published: '2021-11-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# ants：在Submit中再调用当前Pool的Submit可能导致阻塞

![](../../assets/b480a4313dd838c3.png)


[本文永久链接](https://tonybai.com/2021/11/27/ants-call-submit-in-submit-may-cause-blocking) – https://tonybai.com/2021/11/27/ants-call-submit-in-submit-may-cause-blocking

### 1. goroutine pool的必要性

Go在并发程序方面的一个小创新就是支持轻量级用户线程goroutine，不过虽然goroutine很轻，但并不是免费的，尤其是Go程序中存在大量goroutine反复启停时(比如采用每连接一个goroutine的处理http短连接的http server，在大并发的情况下就是如此)，[Go运行时启停和调度goroutine的开销还是蛮大的](https://mp.weixin.qq.com/s/aX9_ZAXfDQZQZrkq-6DZew)。这个时候我们对goroutine pool的需求就诞生了。

goroutine pool减小开销的主要思路就是**复用**：即创建出的goroutine在做完一个task后不退出，而是等待下一个task，这样来减少goroutine反复创建和销毁带来的开销。除此之外，由于goroutine已经被创建，当任务到达时，可以不需要等待goroutine创建就能立即执行，提高响应速度。并且通过goroutine pool，我们还可以严格控制启动的goroutine的数量，避免因外部条件变化带来的goroutine数量的暴涨与暴跌。

在Go社区中，优秀的goroutine pool的实现有不少，[Andy Pan](https://andypan.me)开源的[ants](https://github.com/panjf2000/ants)就是其中之一。根据ants在github上的当前状态来看，它在Go社区范围的应用很广泛，Andy Pan对issue的响应也是十分快的。这也是我们在项目中引入ants的原因。

这篇文章要写的就是我们在使用ants过程中遇到的问题，以及对问题的简单分析与解决过程，这里分享出来的目的也是希望大家能避免遇到同类问题。

### 2. 问题描述

我们在对系统进行压测时，发现系统出现了“死锁”。经过查找，我们将问题锁定在对ants包的使用上面了。我们的工程师使用ants时，在传给Pool.Submit方法的task函数中又调用了同一个Pool的Submit方法。之后他便用下面代码复现了这个问题：

```
package main
import (
"fmt"
"time"
"github.com/panjf2000/ants/v2"
)
func main() {
p, _ := ants.NewPool(100)
for {
p.Submit(func() {
for i := 0; i < 3; i++ {
p.Submit(func() {
fmt.Println(time.Now().Unix())
})
}
})
}
}
```


这个代码使用了ants 2.4.6版本，我们在ubuntu 20.04上使用[Go 1.17](https://mp.weixin.qq.com/s/y_pC6GYeZnKuHG8ycNy6rg)运行这个程序，很快程序就锁住了。

### 3. 原因分析

ants代码不多，原理上也不复杂，我们直接来看看Submit的代码：

```
// https://github.com/panjf2000/ants/blob/master/pool.go (commit fdb318c1d7cef8e448f1bc2bbb03519ff69939da)
func (p *Pool) Submit(task func()) error {
if p.IsClosed() {
return ErrPoolClosed
}
var w *goWorker
if w = p.retrieveWorker(); w == nil {
return ErrPoolOverload
}
w.task <- task
return nil
}
```


我们看到，Submit方法的主要逻辑就是从Pool中获取一个worker，然后将传入的task写入worker的task channel中。再来看看retrieveWorker方法：

```
// https://github.com/panjf2000/ants/blob/master/pool.go(commit fdb318c1d7cef8e448f1bc2bbb03519ff69939da)
225 func (p *Pool) retrieveWorker() (w *goWorker) {
226 spawnWorker := func() {
227 w = p.workerCache.Get().(*goWorker)
228 w.run()
229 }
230
231 p.lock.Lock()
232
233 w = p.workers.detach()
234 if w != nil { // first try to fetch the worker from the queue
235 p.lock.Unlock()
236 } else if capacity := p.Cap(); capacity == -1 || capacity > p.Running() {
237 // if the worker queue is empty and we don't run out of the pool capacity,
238 // then just spawn a new worker goroutine.
239 p.lock.Unlock()
240 spawnWorker()
241 } else { // otherwise, we'll have to keep them blocked and wait for at least one worker to be put back into pool.
242 if p.options.Nonblocking {
243 p.lock.Unlock()
244 return
245 }
246 retry:
247 if p.options.MaxBlockingTasks != 0 && p.blockingNum >= p.options.MaxBlockingTasks {
248 p.lock.Unlock()
249 return
250 }
251 p.blockingNum++
252 p.cond.Wait() // block and wait for an available worker
253 p.blockingNum--
254 var nw int
255 if nw = p.Running(); nw == 0 { // awakened by the scavenger
256 p.lock.Unlock()
257 if !p.IsClosed() {
258 spawnWorker()
259 }
260 return
261 }
262 if w = p.workers.detach(); w == nil {
263 if nw < capacity {
264 p.lock.Unlock()
265 spawnWorker()
266 return
267 }
268 goto retry
269 }
270
271 p.lock.Unlock()
272 }
273 return
274 }
```


retrieveWorker方法负责从Pool中取出一个空闲worker。

retrieveWorker先加锁(line 231)，然后尝试从worker queue中获取空闲worker(line 233)，如果成功获得，那么解锁返回(line 234~235)；

如果队列为空，且池子容量(capacity)还没有满，那就创建一个新worker(line 236~240)；

如果队列为空，且池子容量(capacity)也满了(line 241)，那么判断一下p.options.Nonblocking是否为true，如果为true，说明不想阻塞，那么retrieveWorker返回nil(line 247~250)。retrieveWorker返回nil，那么Submit返回ErrPoolOverload错误。

如果用户没有将p.options.Nonblocking设置为true(p.options.Nonblocking默认为false)，retrieveWorker判断p.options.MaxBlockingTasks这个option，但p.options.MaxBlockingTasks这个option默认为0，所以不满足条件。代码进入p.cond.Wait()，**问题就出在这里**！

我们简化一下复现的步骤，假设我们的pool的容量是1，初始我们调用1次Submit获得了worker，这个worker开始执行task，而这个被执行的task又调用了同一个Pool的Submit，之后进入retrieveWorker方法，由于没有设置p.options.Nonblocking=true，cap容量也满了，由于此时没有空闲worker了，于是该worker进入p.cond.Wait。此时程序便进入死锁状态。将这个示例整理为代码，如下：

```
package main
import (
"fmt"
"time"
"github.com/panjf2000/ants/v2"
)
func main() {
p, _ := ants.NewPool(1)
p.Submit(func() {
p.Submit(func() {
fmt.Println(time.Now().Unix())
})
})
time.Sleep(1000 *time.Second)
}
```


大家可以执行一下这段代码，死锁必然马上出现。

如果我们修改一下ants的pool.go中的代码，在p.cond.Wait()前后加入一些打印语句，就像下面这样：

```
p.blockingNum++
fmt.Println("==== cond wait ...===")
p.cond.Wait() // block and wait for an available worker
fmt.Println("==== cond wait return ===")
p.blockingNum--
```


然后，我们通过replace将demo对ants的依赖改为本地依赖，运行demo后，我们将看到下面输出：

```
==== cond wait ...===
```


demo将一直停在上面这行输出的地方不再向下执行了。

### 4. 官方策略

我将这个问题[提交到ants的issue列表](https://github.com/panjf2000/ants/issues/197)中，Andy Pan很快给了响应。按照Andy的说法，目前ants并不禁止Submit()里再调用同一个Pool的Submit()，只是需要设置一下Pool无可用worker时不阻塞即可，就像下面代码这样：

```
p, _ := ants.NewPool(1, ants.WithNonblocking(true))
```


我个人又考虑了一下这个问题，设置WithNonblocking为true，Submit方法会返回ErrPoolOverload错误，那么调用者需要考虑如何处理这个错误，最大的可能就是反复重试。

另外如果不设置ants.WithNonblocking(true)，我就是要让代码去等，正常情况下，这种阻塞应该是可以解开的，当task执行完毕后，自然可以空闲出一个goroutine来接新task。但问题就在于：如果我在Submit()里再调用同一个Pool的Submit()，一旦所有task都是这种情况，这个阻塞可能是无法解开的。所以我建议Andy在文档中说明一下这种情况。Andy也接受了这个建议，在[最新的commit中](https://github.com/panjf2000/ants/commit/91b12588dbf96e6cd56850300fe07bafd4452dee)在Submit和Invoke方法的注释中增加了对这种情况的说明。

### 5. 解决方法

那么如果我就是要在Submit中调用Submit该如何处理呢？一种很直接的思路就是使用两个Pool！比如将上面的demo改成下面这样就可以正常运行了：

```
func main() {
p1, _ := ants.NewPool(1)
p2, _ := ants.NewPool(1)
p1.Submit(func() {
p2.Submit(func() {
fmt.Println(time.Now().Unix())
})
})
time.Sleep(10*time.Second)
}
```


### 6. 补充一个因上述ants阻塞问题导致的其他问题

我们的系统在生产场景中会有大量并发连接，针对每个连接都会有定时器处理会话相关的过期、删除等。考虑到定时器太多，我们选择了维护定时器开销更小的[时间轮算法](http://www.cs.columbia.edu/~nahum/w6998/papers/ton97-timing-wheels.pdf)的定时器实现。在github上，[RussellLuo/timingwheel](https://github.com/RussellLuo/timingwheel)是[目前star最多的](https://github.com/search?q=timingwheel)，但美中不足的是其作者Russelluo似乎对这一项目不是很热心了，issue响应也很少了。我们抱着先使用再自主改进的态度引入了RussellLuo/timingwheel。

考虑到RussellLuo/timingwheel每执行一个fired的timer对应的task时，都启动一个新goroutine去执行，我们将下面代码做了修改：

```
func (tw *TimingWheel) addOrRun(t *Timer) {
if !tw.add(t) {
// Already expired
// Like the standard time.AfterFunc (https://golang.org/pkg/time/#AfterFunc),
// always execute the timer's task in its own goroutine.
go t.task()
}
}
```


改为：

```
func (tw *TimingWheel) addOrRun(t *Timer) {
if !tw.add(t) {
// Already expired
// Like the standard time.AfterFunc (https://golang.org/pkg/time/#AfterFunc),
// always execute the timer's task in its own goroutine.
tw.workerPool.Submit(func() {
t.task()
})
}
}
```


我们用一个ants pool(pool size默认为1024)来减少goroutine频繁创建销毁带来的开销。

在开发与功能测试阶段，改造后的RussellLuo/timingwheel表现不错，一切都还ok。进入到压测阶段，我们发现，在大量连接一起断连后，大部分新启动的用于清除会话的定时器都无法工作，时间到了后，timer也不fire，导致我们的连接断连逻辑无法执行。我用下面的例子复现了这个问题(为了方便复现现象，我们把ants的Pool size改为1)：

```
package main
import (
"fmt"
"sync"
"time"
"github.com/RussellLuo/timingwheel"
)
var tw *timingwheel.TimingWheel
type tickScheduler struct {
interval time.Duration
}
func (s *tickScheduler) Next(prev time.Time) time.Time {
next := prev.Add(s.interval)
return next
}
type Timer struct {
timer *timingwheel.Timer
}
func (t *Timer) Stop() bool {
return t.timer.Stop()
}
func TickFunc(d time.Duration, f func()) *Timer {
s := &tickScheduler{
interval: d,
}
t := tw.ScheduleFunc(s, f)
return &Timer{t}
}
func main() {
tw = timingwheel.NewTimingWheel(10*time.Millisecond, 60)
tw.Start()
defer tw.Stop()
var c = make(chan string)
var wg sync.WaitGroup
wg.Add(10)
for i := 0; i < 10; i++ {
go func() {
timer := TickFunc(time.Millisecond*10, func() {
c <- "timer fired"
})
defer timer.Stop()
time.Sleep(time.Second)
for i := 0; i < 10; i++ {
s := <-c
if s != "timer fired" {
fmt.Errorf("%d: want [timer fired], got [%s]\n", i+1, s)
} else {
fmt.Printf("%d: timer fired\n", i+1)
}
}
wg.Done()
}()
}
wg.Wait()
}
```


运行这个程序，程序也很快锁住：

```
$ go run main.go
1: timer fired
1: timer fired
1: timer fired
1: timer fired
1: timer fired
2: timer fired
2: timer fired
2: timer fired
2: timer fired
//锁住
```


这个问题与本文开始的问题一样，也是在Submit中调用同pool的Submit，调用Submit的两处位置，我在下面的代码中用注释标记了出来。

```
func (tw *TimingWheel) ScheduleFunc(s Scheduler, f func()) (t *Timer) {
expiration := s.Next(time.Now().UTC())
if expiration.IsZero() {
// No time is scheduled, return nil.
return
}
t = &Timer{
expiration: timeToMs(expiration),
task: func() {
// Schedule the task to execute at the next time if possible.
expiration := s.Next(msToTime(t.expiration))
if !expiration.IsZero() {
t.expiration = timeToMs(expiration)
tw.addOrRun(t) // 如果timer已经fire，那么就调用pool.Submit
}
// Actually execute the task.
f()
},
}
tw.addOrRun(t) // 如果timer已经fire，那么就调用pool.Submit
return
}
```


btw，关于时间轮算法是否在资源占用，维护timer开销方面胜过Go标准库timer，这里其实并没有细致比对过。Go标准库的timer性能一直在完善，后续有时间需要认真对比一下。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强，欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


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


微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

哈哈，我想起我在面试中，经常问的一个问题：如何构造一个死锁。从来没有人给出过最简单的一个情景：单线程，自己获取自己这个资源。。用erlang这种actor模型来说，更形象一点，自己call 自己，然后等待自己回复。。解决方法，一个如上面给出的多个资源池，或者说，进一步划分职责，就像数据库mysql连接池就是数据库自己持有的，mongo连接池就是mongo自己的。一种是请求队列化，如果这个请求会分裂，那么把分裂出来的操作一样的进来排队(或者类似压栈也可以），看起来像处理递归一样，但是如果没有终止条件，肯定要爆炸的。