---
title: Go中的系统Signal处理
url: https://tonybai.com/2012/09/21/signal-handling-in-go/
published: '2012-09-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go中的系统Signal处理

我们在生产环境下运行的系统要求优雅退出，即程序接收退出通知后，会有机会先执行一段清理代码，将收尾工作做完后再真正退出。我们采用系统Signal来 通知系统退出，即kill pragram-pid。我们在程序中针对一些系统信号设置了处理函数，当收到信号后，会执行相关清理程序或通知各个子进程做自清理。kill -9强制杀掉程序是不能被接受的，那样会导致某些处理过程被强制中断，留下无法恢复的现场，导致消息被破坏，影响下次系统启动运行。

最近用[Golang](http://golang.org)实现的一个代理程序也需要优雅退出，因此我尝试了解了一下[Golang](http://tonybai.com/2012/08/17/hello-go/)中对系统Signal的处理方式，这里和大家分享。Golang 的系统信号处理主要涉及os包、os.signal包以及syscall包。其中最主要的函数是signal包中的Notify函数：

func Notify(c chan<- os.Signal, sig …os.Signal)

该函数会将进程收到的系统Signal转发给channel c。转发哪些信号由该函数的可变参数决定，如果你没有传入sig参数，那么Notify会将系统收到的所有信号转发给c。如果你像下面这样调用Notify：

signal.Notify(c, syscall.SIGINT, syscall.SIGUSR1, syscall.SIGUSR2)

则Go只会关注你传入的Signal类型，其他Signal将会按照默认方式处理，大多都是进程退出。因此你需要在Notify中传入你要关注和处理的Signal类型，也就是拦截它们，提供自定义处理函数来改变它们的行为。

下面是一个较为完整的例子：

//signal.go

package main

import "fmt"

import "time"

import "os"

import "os/signal"

import "syscall"

type signalHandler func(s os.Signal, arg interface{})

type signalSet struct {

m map[os.Signal]signalHandler

}

func signalSetNew()(*signalSet){

ss := new(signalSet)

ss.m = make(map[os.Signal]signalHandler)

return ss

}

func (set *signalSet) register(s os.Signal, handler signalHandler) {

if _, found := set.m[s]; !found {

set.m[s] = handler

}

}

func (set *signalSet) handle(sig os.Signal, arg interface{})(err error) {

if _, found := set.m[sig]; found {

set.m[sig](sig, arg)

return nil

} else {

return fmt.Errorf("No handler available for signal %v", sig)

}

panic("won't reach here")

}

func main() {

go sysSignalHandleDemo()

time.Sleep(time.Hour) // make the main goroutine wait!

}

func sysSignalHandleDemo() {

ss := signalSetNew()

handler := func(s os.Signal, arg interface{}) {

fmt.Printf("handle signal: %v\n", s)

}

ss.register(syscall.SIGINT, handler)

ss.register(syscall.SIGUSR1, handler)

ss.register(syscall.SIGUSR2, handler)

for {

c := make(chan os.Signal)

var sigs []os.Signal

for sig := range ss.m {

sigs = append(sigs, sig)

}

signal.Notify(c)

sig := <-c

err := ss.handle(sig, nil)

if (err != nil) {

fmt.Printf("unknown signal received: %v\n", sig)

os.Exit(1)

}

}

}

上例中Notify函数只有一个参数，没有传入要关注的sig，因此程序会将收到的所有类型Signal都转发到channel c中。build该源文件并执行程序：

$> go build signal.go

$> signal

在另外一个窗口下执行如下命令：

$> ps -ef|grep signal

tonybai 25271 1087 0 16:27 pts/1 00:00:00 signal

$> kill -n 2 25271

$> kill -n 12 25271

$> kill 25271

我们在第一个窗口会看到如下输出：

$> signal

handle signal: interrupt

handle signal: user defined signal 2

unknown signal received: terminated

在sysSignalHandleDemo中我们也可以为Notify传入我们所关注的Signal集合：

signal.Notify(c, sigs…)

这样只有在该集合中的信号我们才能捕获，收到未在集合中的信号时，程序多直接退出。上面只是一个Demo，只是说明了我们可以捕捉到我们所关注的信号，并未体现程序如何优雅退出，不同程序的退出方式不同，这里没有通用方法，就不细说了，你的程序需要你专门的设计。

另外我们生产环境下的程序多是以Daemon守护进程的形式运行的。我们用C实现的程序多参考“[Unix高级编程](http://book.douban.com/subject/1788421/)”中的方法将程序转为Daemon Process，但在Go中目前尚提供相关方式，网上有一些实现，但据说都不理想。更多的Go开发者建议不要在代码中实现Daemon转换，建议直接利用 第三方工具。比如在[Ubuntu](http://ubuntu.com)下我们可以使用start-stop-daemon这个小程序轻松将你的程序转换为Daemon：

$> start-stop-daemon –start –pidfile ./signal.pid –startas /home/tonybai/test/go/signal –background -m

$> start-stop-daemon –stop –pidfile ./signal.pid –startas /home/tonybai/test/go/signal

这里注意：只有加上-m选项，pidfile才能成功创建。

start-stop-daemon在[Debian](http://www.debian.org)系的Linux发行版中都是默认自带的。但在[Redhat](http://www.redhat.com)系Linux发行版中却没有该工具，我们可以自行安装：

wget -c http://developer.axis.com/download/distribution/apps-sys-utils-start-stop-daemon-IR1_9_18-2.tar.gz

tar -xzf apps-sys-utils-start-stop-daemon-IR1_9_18-2.tar.gz

cd apps/sys-utils/start-stop-daemon-IR1_9_18-2

gcc start-stop-daemon.c -o start-stop-daemon

切换到root下

cp start-stop-daemon /sbin/

chmod +x /sbin/start-stop-daemon

另外Go 1.0.2提供的二进制安装包直接在Redhat 5.6(Linux tonybai 2.6.18-238.el5 #1 SMP Sun Dec 19 14:22:44 EST 2010 x86_64 x86_64 x86_64 GNU/Linux)下面运行出错，提示无法找到GLIBC 2.7版本。目前解决这一问题的方法似乎只有从源码编译安装。进入到$GOROOT/src下，执行./all.bash即可。重现编译链接后的go可执 行程序则运行一切正常。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

博主用一个代码高亮吧，这样看起来会更轻松。小小的建议，嘿嘿。。。

有什么好用的高亮插件推荐么？

受益匪浅

哎呀，到关键的地方就掉链了啊…http://www.oschina.net/translate/graceful-server-restart-with-go?cmp最近看到这篇文章，博主当时应该继续深入的…

赞同

我的go基本都是跟楼主学的

这是go什么版本啊，我的是go 1.8 怎么没有 syscall.SIGUSR1 和 syscall.SIGUSR2 了呢？

我貌似明白了！syscall包里面的常量底层时会根据当前操作系统做出选择的。win下的signal信号没有 syscall.SIGUSR1 和 syscall.SIGUSR2