---
title: 凌晨3点的警报：一个导致 50000 多个 Goroutine 泄漏的 Bug 分析
url: https://tonybai.com/2026/01/22/a-bug-cause-50000-goroutine-leak/
published: '2026-01-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 凌晨3点的警报：一个导致 50000 多个 Goroutine 泄漏的 Bug 分析

![](../../assets/ae2782fb2ad6d217.png)


[本文永久链接](https://tonybai.com/2026/01/22/a-bug-cause-50000-goroutine-leak) – https://tonybai.com/2026/01/22/a-bug-cause-50000-goroutine-leak

大家好，我是Tony Bai。

内存占用 47GB，响应时间飙升至 32秒，Goroutine 数量达到惊人的 50847 个。

这是一个周六凌晨 3 点，发生在核心 API 服务上的真实噩梦。运维正准备重启服务止损，但 Serge Skoredin 敏锐地意识到：这不是普通的内存泄漏，而是[一场已经潜伏了 6 周、呈指数级增长的 Goroutine 泄漏](https://skoredin.pro/blog/golang/goroutine-leak-debugging)。

导致这场灾难的代码，曾通过了三位资深工程师的 Code Review，看起来“完美无缺”。今天，让我们跟随 Serge 的视角，层层剥开这个隐蔽 Bug 的伪装，学习如何避免同样的悲剧发生在你身上。

![img{512x368}](../../assets/e9c16d84a31ad3b6.png)


## 看似“无辜”的代码

问题的核心出在一个 WebSocket 通知服务中。让我们看看这段“看起来很合理”的代码：

```
func (s *NotificationService) Subscribe(userID string, ws *websocket.Conn) {
// 1. 创建带取消功能的 Context
ctx, cancel := context.WithCancel(context.Background())
sub := &subscription{
userID: userID,
ws: ws,
cancel: cancel, // 保存 cancel 函数以便后续调用
}
s.subscribers[userID] = sub
// 2. 启动消息处理和心跳
go s.pumpMessages(ctx, sub)
go s.heartbeat(ctx, sub)
}
```


这看起来非常标准：使用了 context.WithCancel 来管理生命周期，将 cancel 存入结构体以便连接断开时调用。然而，魔鬼就藏在细节里。

## 泄漏的“三重奏”

经过排查，Serge 发现了导致泄漏的三个致命错误，它们环环相扣，最终酿成了大祸。

### Bug #1：无人调用的 cancel

```
// 预期：连接断开时调用 s.Unsubscribe -> sub.cancel()
// 现实：WebSocket 断开连接时，根本没有人通知 Service 去执行清理逻辑！
```


当 WebSocket 连接意外断开（如用户直接关掉浏览器），如果没有显式地监听关闭事件并调用清理函数，s.subscribers 中不仅残留了无效的订阅对象，更重要的是，**ctx 永远不会被取消**。这意味着所有依赖该 ctx 的 Goroutine 将永生。

### Bug #2：永不停歇的 Ticker

```
func (s *NotificationService) heartbeat(ctx context.Context, sub *subscription) {
ticker := time.NewTicker(30 * time.Second)
// 致命错误：缺少 defer ticker.Stop()
for {
select {
case <-ctx.Done():
return // Goroutine 退出了，但 Ticker 还在！
case <-ticker.C:
// ...
}
}
}
```


即便 ctx 被取消，Goroutine 退出了，但 time.NewTicker 创建的计时器是由 Go 运行时全局管理的。**如果不显式调用 Stop()，Ticker 将永远存在，持续消耗内存和 CPU 资源。** 50,000 个泄漏的 Ticker，足以让 Go 运行时崩溃。

### Bug #3：阻塞的 Channel

```
type subscription struct {
messages chan Message // 无缓冲 Channel（或者缓冲区满了）
// ...
}
func (s *NotificationService) pumpMessages(...) {
// ...
case msg := <-sub.messages:
sub.ws.WriteJSON(msg)
}
```


如果写入端还在不断尝试发送消息（因为不知道连接已断开），而读取端（pumpMessages）因为网络阻塞或已退出而不再读取，那么写入端的 Goroutine 就会被永久阻塞在 channel 发送操作上，形成另一种泄漏。

## 修复与预防：构建防漏体系

修复后的代码不仅加上了必要的清理逻辑，更引入了一套完整的防御体系。

### 修复：确保生命周期的闭环

**监听关闭事件**：利用 ws.SetCloseHandler 确保在连接断开时主动调用 Unsubscribe。**停止 Ticker**：永远使用 defer ticker.Stop()。**关闭 Channel**：在清理时关闭 sub.messages，解除写入端的阻塞。

注：关闭 channel务必由写入者goroutine进行，如果写入者goroutine阻塞在channel写上，此时由其他goroutine close channel，会导致panic on send on closed channel的问题。


### 预防：Goleak 与监控

Serge 强烈推荐使用 Uber 开源的 **goleak** 库进行单元测试。

```
func TestNoGoroutineLeaks(t *testing.T) {
defer goleak.VerifyNone(t) // 测试结束时检查是否有泄漏的 Goroutine
// ... 运行测试逻辑 ...
}
```


此外，在生产环境中，必须监控 runtime.NumGoroutine()。设置合理的告警阈值（例如：当 Goroutine 数量超过正常峰值的 1.5 倍时告警），能在灾难发生前 6 周就发现端倪，而不是等到凌晨 3 点。

注：Go 1.26已经吸收了uber的goleak项目思想，并

[原生支持goroutine leak检测]！此特性可在编译时通过设置GOEXPERIMENT=goroutineleakprofile开启。

## 小结：经验教训

这次事故给所有 Go 开发者敲响了警钟：

**Goroutine 必须有明确的退出策略**：每当你写下 go func() 时，必须清楚地知道它将在何时、何种条件下退出。**Context 是生命线**：正确传播和取消 Context 是管理并发生命周期的核心。**资源必须显式释放**：Ticker、Channel、Timer 等资源不会自动被垃圾回收，必须手动关闭。**测试是最后一道防线**：不要只测试逻辑正确性，还要测试资源清理的正确性。

Goroutine 泄漏是“沉默的杀手”，它不报错、不崩溃，只是悄悄地吞噬你的系统。保持警惕，定期体检，别让它成为你凌晨 3 点的噩梦。

资料链接：https://skoredin.pro/blog/golang/goroutine-leak-debugging

**你的“惊魂时刻”**

50000 个 Goroutine 的泄漏听起来很吓人，但它可能就潜伏在我们看似正常的代码里。在你的开发生涯中，是否也遇到过类似的内存泄漏或资源耗尽的“惊魂时刻”？你最后是如何定位并解决的？

欢迎在评论区分享你的排查故事或避坑心得！让我们一起把 Bug 扼杀在摇篮里。

如果这篇文章让你对 Goroutine 的生命周期有了更深的敬畏，别忘了点个【赞】和【在看】，并转发给你的团队，今晚睡个好觉！

还在为“复制粘贴喂AI”而烦恼？我的新专栏 **《 AI原生开发工作流实战》** 将带你：

- 告别低效，重塑开发范式
- 驾驭AI Agent(Claude Code)，实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

扫描下方二维码，开启你的AI原生开发之旅。

![](../../assets/305ffd23f32ce780.png)


你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论