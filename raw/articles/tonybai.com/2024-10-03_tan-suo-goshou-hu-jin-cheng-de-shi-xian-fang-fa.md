---
title: 探索Go守护进程的实现方法
url: https://tonybai.com/2024/10/03/how-to-daemonize-go-program/
published: '2024-10-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 探索Go守护进程的实现方法

![](../../assets/39b24e496699fb2f.png)


[本文永久链接](https://tonybai.com/2024/10/03/how-to-daemonize-go-program) – https://tonybai.com/2024/10/03/how-to-daemonize-go-program

在后端开发的世界里，[守护进程（daemon）](https://en.wikipedia.org/wiki/Daemon_(computing))这个概念与Unix系统一样古老。守护进程是在后台运行的长期服务程序，不与任何终端关联。尽管现代进程管理工具如[systemd](https://tonybai.com/2016/12/27/when-docker-meets-systemd)和[supervisor](http://supervisord.org)等让应用转化为守护进程变得十分简单，我们甚至可以使用以下命令来在后台运行程序：

```
nohup ./your_go_program &
```


但在某些情况下，程序的原生转化为守护进程的能力仍然是有必要的。比如分布式文件系统juicefs cli的mount子命令，它就支持以-d选项启动，并以守护进程方式运行：

```
$juicefs mount -h
NAME:
juicefs mount - Mount a volume
USAGE:
juicefs mount [command options] META-URL MOUNTPOINT
... ...
OPTIONS:
-d, --background run in background (default: false)
... ...
... ...
```


这种自我守护化的能力会让很多Go程序受益，在这一篇文章中，我们就来探索一下Go应用转化为守护进程的实现方法。

## 1. 标准的守护进程转化方法

[W.Richard Stevens]的经典著作《[UNIX环境高级编程](https://book.douban.com/subject/25900403/)》中对将程序转化为一个守护进程的 (daemonize) 步骤进行了详细的说明，主要步骤如下：

- 创建子进程并终止父进程

通过fork()系统调用创建子进程，父进程立即终止，保证子进程不是控制终端的会话组首领。

- 创建新的会话

子进程调用setsid()来创建一个新会话，成为会话组首领，从而摆脱控制终端和进程组。

- 更改工作目录

使用chdir(“/”) 将当前工作目录更改为根目录，避免守护进程持有任何工作目录的引用，防止对文件系统卸载的阻止。

- 重设文件权限掩码

通过umask(0) 清除文件权限掩码，使得守护进程可以自由设置文件权限。

- 关闭文件描述符

关闭继承自父进程的已经open的文件描述符（通常是标准输入、标准输出和标准错误)。

- 重定向标准输入/输出/错误

重新打开标准输入、输出和错误，重定向到/dev/null，以避免守护进程无意输出内容到不应有的地方。

注：fork()系统调用是一个较为难理解的调用，它用于在UNIX/Linux系统中创建一个新的进程。新创建的进程被称为子进程，它是由调用fork()的进程（即父进程）复制出来的。子进程与父进程拥有相同的代码段、数据段、堆和栈，但它们是各自独立的进程，有不同的进程ID (PID)。在父进程中，fork()返回子进程的PID（正整数），在子进程中，fork()返回0，如果fork()调用失败（例如系统资源不足），则返回-1，并设置errno以指示错误原因。


下面是一个符合UNIX标准的守护进程转化函数的C语言实现，参考了《UNIX环境高级编程》中的经典步骤：

```
// daemonize/c/daemon.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <syslog.h>
#include <signal.h>
void daemonize()
{
pid_t pid;
// 1. Fork off the parent process
pid = fork();
if (pid < 0) {
exit(EXIT_FAILURE);
}
// If we got a good PID, then we can exit the parent process.
if (pid > 0) {
exit(EXIT_SUCCESS);
}
// 2. Create a new session to become session leader to lose controlling TTY
if (setsid() < 0) {
exit(EXIT_FAILURE);
}
// 3. Fork again to ensure the process won't allocate controlling TTY in future
pid = fork();
if (pid < 0) {
exit(EXIT_FAILURE);
}
if (pid > 0) {
exit(EXIT_SUCCESS);
}
// 4. Change the current working directory to root.
if (chdir("/") < 0) {
exit(EXIT_FAILURE);
}
// 5. Set the file mode creation mask to 0.
umask(0);
// 6. Close all open file descriptors.
for (int x = sysconf(_SC_OPEN_MAX); x>=0; x--) {
close(x);
}
// 7. Reopen stdin, stdout, stderr to /dev/null
open("/dev/null", O_RDWR); // stdin
dup(0); // stdout
dup(0); // stderr
// Optional: Log the daemon starting
openlog("daemonized_process", LOG_PID, LOG_DAEMON);
syslog(LOG_NOTICE, "Daemon started.");
closelog();
}
int main() {
daemonize();
// Daemon process main loop
while (1) {
// Perform some background task...
sleep(30); // Sleep for 30 seconds.
}
return EXIT_SUCCESS;
}
```


注：这里省略了书中设置系统信号handler的步骤。


这里的daemonize函数完成了标准的守护化转化过程，并确保了程序在后台无依赖地稳定运行。我们编译运行该程序后，程序进入后台运行，通过ps命令可以查看到类似下面内容：

```
$ ./c-daemon-app
$ ps -ef|grep c-daemon-app
root 28517 1 0 14:11 ? 00:00:00 ./c-daemon-app
```


我们看到c-daemon-app的父进程是ppid为1的进程，即linux的init进程。我们看到上面c代码中转化为守护进程的函数daemonize进行了两次fork，至于为何要做两次fork，在我的《[理解Zombie和Daemon Process](https://tonybai.com/2005/09/21/understand-zombie-and-daemon-process/)》一文中有说明，这里就不赘述了。

那么Go是否可以参考上述步骤实现Go程序的守护进程转化呢？我们接着往下看。

## 2. Go语言实现守护进程的挑战

关于Go如何实现守护进程的转换，在Go尚未发布1.0之前的2009年就有issue提到，在[runtime: support for daemonize](https://github.com/golang/go/issues/227)中，Go社区与Go语言的早起元老们讨论了在Go中实现原生守护进程的复杂性，主要挑战源于Go的运行时及其线程管理方式。当一个进程执行fork操作时，只有主线程被复制到子进程中，如果fork前Go程序有多个线程(及多个goroutine)在执行(可能是由于go runtime调度goroutine和gc产生的线程)，那么fork后，这些非执行fork线程的线程(以及goroutine)将不会被复制到新的子进程中，这可能会导致后续子进程中线程运行的不确定性(基于一些fork前线程留下的数据状态)。

理想情况下是Go runtime提供类似的daemonize函数，然后在多线程启动之前实现守护进程的转化，不过Go团队至今也没有提供该机制，而是建议大家使用如systemd的第三方工具来实现Go程序的守护进程转化。

既然Go官方不提供方案，Go社区就会另辟蹊径，接下来，我们看看目前Go社区的守护进程解决方案。

## 3. Go社区的守护进程解决方案

尽管面临挑战，Go社区还是开发了一些库来支持Go守护进程的实现，其中一个star比较多的解决方案是github.com/sevlyar/go-daemon。

go-daemon库的作者巧妙地解决了Go语言中无法直接使用fork系统调用的问题。go-daemon采用了一个简单而有效的技巧来模拟fork的行为：该库定义了一个特殊的环境变量作为标记。程序运行时，首先检查这个环境变量是否存在。如果环境变量不存在，执行父进程相关操作，然后使用os.StartProcess(本质是fork-and-exec)启动带有特定环境变量标记的程序副本。如果环境变量存在，执行子进程相关操作，继续执行主程序逻辑，下面是该库作者提供的原理图：

![](../../assets/145c4c94fa636375.png)


这种方法有效地模拟了fork的行为，同时避免了Go运行时中与线程和goroutine相关的问题。下面是使用go-daemon包实现Go守护进程的示例：

```
// daemonize/go-daemon/main.go
package main
import (
"log"
"time"
"github.com/sevlyar/go-daemon"
)
func main() {
cntxt := &daemon.Context{
PidFileName: "example.pid",
PidFilePerm: 0644,
LogFileName: "example.log",
LogFilePerm: 0640,
WorkDir: "./",
Umask: 027,
}
d, err := cntxt.Reborn()
if err != nil {
log.Fatal("无法运行：", err)
}
if d != nil {
return
}
defer cntxt.Release()
log.Print("守护进程已启动")
// 守护进程逻辑
for {
// ... 执行任务 ...
time.Sleep(time.Second * 30)
}
}
```


运行该程序后，通过ps可以查看到对应的守护进程：

```
$make
go build -o go-daemon-app
$./go-daemon-app
$ps -ef|grep go-daemon-app
501 4025 1 0 9:20下午 ?? 0:00.01 ./go-daemon-app
```


此外，该程序会在当前目录下生成example.pid(用于实现file lock)，用于防止意外重复执行同一个go-daemon-app：

```
$./go-daemon-app
2024/09/26 21:21:28 无法运行：daemon: Resource temporarily unavailable
```


虽然原生守护进程化提供了精细的控制且无需安装和配置外部依赖，但进程管理工具提供了额外的功能，如[开机自启](https://tonybai.com/2022/09/12/how-to-install-a-go-app-as-a-system-service-like-gitlab-runner)、异常退出后的自动重启和日志记录等，并且Go团队推荐使用进程管理工具来实现Go守护进程。进程管理工具的缺点在于需要额外的配置(比如systemd)或安装设置(比如supervisor)。

## 4. 小结

在Go中实现守护进程化，虽然因为语言运行时的特性而具有挑战性，但通过社区开发的库和谨慎的实现是可以实现的。随着Go语言的不断发展，我们可能会看到更多对进程管理功能的原生支持。同时，开发者可以根据具体需求，在原生守护进程化、进程管理工具或混合方法之间做出选择。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/daemonize)下载。

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