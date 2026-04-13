---
title: 云风的 BLOG
url: https://blog.codingnow.com/2014/05/
published: '2014-05-21'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### skynet logo

![skynet.png](../../assets/46f6075e85af4d66.png)


![skynet_b.png](../../assets/f941326a05de877a.png)


折腾了几天，终于把 skynet 的 logo 设计好了。

[« April 2014](https://blog.codingnow.com/2014/04/) |
[Main](https://blog.codingnow.com/)
| [June 2014 »](https://blog.codingnow.com/2014/06/)

![skynet.png](../../assets/46f6075e85af4d66.png)


![skynet_b.png](../../assets/f941326a05de877a.png)


折腾了几天，终于把 skynet 的 logo 设计好了。

按原计划, 我今天给 [skynet 的 github 仓库](https://github.com/cloudwu/skynet) 打上了 v0.2.0 的 tag 。

这个版本增加的主要特性是[组播](http://blog.codingnow.com/2014/04/skynet_multicast.html) 。其它都是对已有代码的整理。

虽然 skynet 只有不到三年的历史，但已经有不少历史包袱了。最早的 skynet 是用 erlang 实现的，在 erlang 中编写了一个 C driver 然后在里面嵌入 lua 虚拟机。设计 skynet 的 C 接口时，也没有经过实际项目的使用，有许多设计不当的地方。

有一些后来觉得不应该放在核心层的东西被实现在了核心内，一些本应该在底层提供的设施被放在了很高层实现。

还有一些小特性几乎没有被使用过，但却增加了整体实现的复杂度。

调整这些历史造成的设计需要一点点来，v0.2.0 向前迈了一步。

这次简化了 skynet 在 bootstrap 流程上花的代码量，且把它变成可定制的。这样，skynet 多节点网络的组网也被尽力分离出来了。这可以让我在未来多考虑一下更好的 skynet 网络的设计。

另外，还简化了 lua 服务的加载预处理的流程，把许多原本在 C 里实现的代码移到了 lua 代码中。

skynet 的异常处理的方法在底层被慢慢固定下来，寻找一个简单的异常传播方案花了我不少的时间。希望这次的方法是一个更好的选择。上次的 [monitor](http://blog.codingnow.com/2013/12/skynet_monitor.html) 方案加的太仓促，贸然去掉它又会影响许多已有的项目，所以还需要慢慢寻找调整的方法。

目前，skynet 的一些核心层之上，业务层之下的基础服务基本固定下来。在未来的版本里，我会多考虑一下这些基础服务的设计。并可以在此之上开发更多的工具。

值得高兴的是：这次的这些改变，没有增加整体代码的复杂度，反而去掉了上百行 C 代码。这符合我所信奉的设计哲学：保持实现的简单、更甚于简洁的接口。

最近接连有几位同学询问 skynet 的消息队列算法中为什么引入了一个独立的 flags bool 数组的问题。时间久远，我自己差点都忘记设计初衷了。今天在代码里加了点注释，防止以后忘记。

其实当时我就[写过一篇 blog](http://blog.codingnow.com/2012/10/bug_and_lockfree_queue.html) 记录过，这篇 blog 下面的评论中也有许多讨论。今天把里面一些细节再展开说一次：

我用了一个循环队列来保存 skynet 的二级消息队列，代码是这样的：

#define GP(p) ((p) % MAX_GLOBAL_MQ) static void skynet_globalmq_push(struct message_queue * queue) { struct global_queue *q= Q; uint32_t tail = GP(__sync_fetch_and_add(&q->tail,1)); q->queue[tail] = queue; __sync_synchronize(); q->flag[tail] = true; } struct message_queue * skynet_globalmq_pop() { struct global_queue *q = Q; uint32_t head = q->head; uint32_t head_ptr = GP(head); if (head_ptr == GP(q->tail)) { return NULL; } if(!q->flag[head_ptr]) { return NULL; } __sync_synchronize(); struct message_queue * mq = q->queue[head_ptr]; if (!__sync_bool_compare_and_swap(&q->head, head, head+1)) { return NULL; } q->flag[head_ptr] = false; return mq; }

有同学问我，为什么要用一个单独的 flag 数组。用指针数组里的指针是否为空来判断不是更简单吗？

代码可以写成这样：

#define GP(p) ((p) % MAX_GLOBAL_MQ) static void skynet_globalmq_push(struct message_queue * queue) { struct global_queue *q= Q; uint32_t tail = GP(__sync_fetch_and_add(&q->tail,1)); // 如果线程在这里挂起，q->queue[tail] 将不为空， // 却没有更新到新的值 q->queue[tail] = queue; } struct message_queue * skynet_globalmq_pop() { struct global_queue *q = Q; uint32_t head = q->head; uint32_t head_ptr = GP(head); if (head_ptr == GP(q->tail)) { return NULL; } if (!q->queue[head_ptr]) { return NULL; } struct message_queue * mq = q->queue[head_ptr]; // 这里无法确保 mq 读到的是 push 进去的值。 // 它有可能是队列用完一圈后，上一个版本的值。 if (!__sync_bool_compare_and_swap(&q->head, head, head+1)) { return NULL; } q->queue[head_ptr] = NULL; return mq; }

这样做其实是有陷阱的，我标记在里代码中。

这种情况只有在 64K 的队列全部转过一圈，某个 push 线程一直挂起在递增 tail 指针，还来不及写入新的值的位置。

看起来这种情况很难发生，但在我们早期的测试中的确出现了。

所以说，并发程序写起来一定要特别谨慎（不要随便改动之前推敲过的代码）。一不小心就掉坑里了。

另外，以前的代码有一个限制：当活跃的（有消息的）服务总数超过 64K 的时候，这段代码就不能正常工作了。虽然一个 skynet 节点中的服务数量很难超过这个限制（因为无消息的服务不会在全局队列中），但理论上一个 skynet 节点支持的服务数量上限是远大于 64K 的。

我这次在增加注释的同时加了几行代码，用了一个额外的链表来保存那些因为队列满无法立刻排进去的服务。在出队列的时候，再尝试把它们从链表中取回来。

static void skynet_globalmq_push(struct message_queue * queue) { struct global_queue *q= Q; if (q->flag[GP(q->tail)]) { // The queue may full seldom, save queue in list assert(queue->next == NULL); struct message_queue * last; do { last = q->list; queue->next = last; } while(!__sync_bool_compare_and_swap(&q->list, last, queue)); return; } uint32_t tail = GP(__sync_fetch_and_add(&q->tail,1)); // The thread would suspend here, and the q->queue[tail] is last version , // but the queue tail is increased. // So we set q->flag[tail] after changing q->queue[tail]. q->queue[tail] = queue; __sync_synchronize(); q->flag[tail] = true; } struct message_queue * skynet_globalmq_pop() { struct global_queue *q = Q; uint32_t head = q->head; if (head == q->tail) { // The queue is empty. return NULL; } uint32_t head_ptr = GP(head); struct message_queue * list = q->list; if (list) { // If q->list is not empty, try to load it back to the queue struct message_queue *newhead = list->next; if (__sync_bool_compare_and_swap(&q->list, list, newhead)) { // try load list only once, if success , push it back to the queue. list->next = NULL; skynet_globalmq_push(list); } } // Check the flag first, if the flag is false, the pushing may not complete. if(!q->flag[head_ptr]) { return NULL; } __sync_synchronize(); struct message_queue * mq = q->queue[head_ptr]; if (!__sync_bool_compare_and_swap(&q->head, head, head+1)) { return NULL; } q->flag[head_ptr] = false; return mq; }