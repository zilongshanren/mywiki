---
title: docker容器内服务程序的优雅退出
url: https://tonybai.com/2014/10/09/gracefully-shutdown-app-running-in-docker/
published: '2014-10-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# docker容器内服务程序的优雅退出

近期在试验如何将我们的产品部署到[docker容器](http://docker.com)中去，这其中涉及到一个技术环节，那就是如何让docker容器退出时其内部运行的服务程序也 可以优雅的退出。所谓优雅退出，指的就是程序在退出前有清理资源（比如关闭文件描述符、关闭socket），保存必要中间状态，持久化内存数据 （比如将内存中的数据flush到文件中）的机会。docker作为目前最火的轻量级虚拟化技术，其在后台服务领域的应用是极其广泛的，其设计者 在程序优雅退出方面是有考虑的。下面我们由简单到复杂逐一考量一下。

**一、优雅退出的原理**

对于服务程序而言，一般都是以daemon形式运行在后台的。通知这些服务程序退出需要使用到系统的signal机制。一般服务程序都会监听某个 特定的退出signal，比如SIGINT、SIGTERM等（通过kill -l命令你可以查看到几十种signal）。当我们使用kill + 进程号时，系统会默认发送一个SIGTERM给相应的进程。该进程通过signal handler响应这一信号，并在这个handler中完成相应的“优雅退出”操作。

与“优雅退出”对立的是“暴力退出”，也就是我们常说的使用kill -9，也就是kill -s SIGKILL + 进程号，这个行为不会给目标进程任何时间空隙，而是直接将进程杀死，无论进程当前在做何种操作。这种操作常常导致“不一致”状态的出现。SIGKILL这 个信号比较特殊，进程无法有效监听该信号，无法有效针对该信号设置handler，无法改变其信号的默认处理行为。

**二、****测试用“服务程序”**

为了测试docker容器对优雅退出的支持，我们编写如下“服务程序”用于放在docker容器中运行：

//dockerapp1.go

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

func signalSetNew() *signalSet {

ss := new(signalSet)

ss.m = make(map[os.Signal]signalHandler)

return ss

}

func (set *signalSet) register(s os.Signal, handler signalHandler) {

if _, found := set.m[s]; !found {

set.m[s] = handler

}

}

func (set *signalSet) handle(sig os.Signal, arg interface{}) (err error) {

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

if s == syscall.SIGTERM {

fmt.Printf("signal termiate received, app exit normally\n")

os.Exit(0)

}

}

ss.register(syscall.SIGINT, handler)

ss.register(syscall.SIGUSR1, handler)

ss.register(syscall.SIGUSR2, handler)

ss.register(syscall.SIGTERM, handler)

for {

c := make(chan os.Signal)

var sigs []os.Signal

for sig := range ss.m {

sigs = append(sigs, sig)

}

signal.Notify(c)

sig := <-c

err := ss.handle(sig, nil)

if err != nil {

fmt.Printf("unknown signal received: %v, app exit unexpectedly\n", sig)

os.Exit(1)

}

}

}

关于[Go语言](http://tonybai.com/tag/golang)对系统Signal的处理，可以参考《[Go中的系统Signal处理](http://tonybai.com/2012/09/21/signal-handling-in-go/)》一文。

**三、制作测试用docker image**

在《 [Ubuntu Server 14.04安装docker](http://tonybai.com/2014/09/26/install-docker-on-ubuntu-server-1404/)》一文中，我们完成了在ubuntu 14.04上安装docker的步骤。要制作测试用docker image，我们首先需要pull一个base image。我们以CentOS6.5为例：

在Ubuntu 14.04上执行：

sudo docker pull centos:centos6

docker会自动从[官方仓库](https://registry.hub.docker.com)下载一个制作好的docker image。下载成功后，我们可以run一下试试，像这样：

$> sudo docker run -t -i centos:centos6 /bin/bash

我们查看一下CentOS6的小版本：

$> cat /etc/centos-release

CentOS release 6.5 (Final)

这是一个极其精简的CentOS，各种工具均未安装：

bash-4.1# telnet

bash: telnet: command not found

bash-4.1# ssh

bash: ssh: command not found

bash-4.1# ftp

bash: ftp: command not found

bash-4.1# echo $PATH

/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

如果你要安装一些必要的工具，可以直接使用yum install，默认的base image已经将yum配置好了，可以直接使用。如果通过公司代理访问外部网络，别忘了先export http_proxy。另外docker直接使用宿主机的/etc/resolv.conf作为容器的DNS，我们也无需额外设置DNS。

接下来，我们就制作我们的第一个测试用image。安装官方推荐的Best Practice，我们使用Dockerfile来bulid一个测试用image。步骤如下：

- 建立~/ImagesFactory目录

- 将构建好的dockerapp1拷贝到~/ImagesFactory目录下

- 进入~/ImagesFactory目录，创建Dockerfile文件，Dockerfile内容如下：

FROM centos:centos6

MAINTAINER Tony Bai [<bigwhite.cn@gmail.com>](mailto:bigwhite.cn@gmail.com)

COPY ./dockerapp1 /bin

CMD /bin/dockerapp1

- 执行docker build，结果如下：

$ sudo docker build -t="test:v1" ./

Sending build context to Docker daemon 7.496 MB

Sending build context to Docker daemon

Step 0 : FROM centos:centos6

—> 68edf809afe7

Step 1 : MAINTAINER Tony Bai [<bigwhite.cn@gmail.com>](mailto:bigwhite.cn@gmail.com)

—> Using cache

—> c617b456934a

Step 2 : COPY ./dockerapp1 /bin

2014/10/09 16:05:25 lchown /var/lib/docker/aufs/mnt/fb0e864d3f07ca17ef8b6b69f034728e1f1158fd3f9c83fa48243054b2f26958/bin/dockerapp1: not a directory

居然build失败，提示什么not a directory。于是各种Search，终于发现问题所在，原来是“COPY ./dockerapp1 /bin”这条命令错了，少了个“/”，将" /bin"改为“/bin/”就OK了，Docker真是奇怪啊，这块明显应该做得更兼容些。新的Dockerfile如下：

FROM centos:centos6

MAINTAINER Tony Bai [<bigwhite.cn@gmail.com>](mailto:bigwhite.cn@gmail.com)

COPY ./dockerapp1 /bin/

CMD /bin/dockerapp1

构建结果如下：

$ sudo docker build -t="test:v1" ./

Sending build context to Docker daemon 7.496 MB

Sending build context to Docker daemon

Step 0 : FROM centos:centos6

—> 68edf809afe7

Step 1 : MAINTAINER Tony Bai [<bigwhite.cn@gmail.com>](mailto:bigwhite.cn@gmail.com)

—> Using cache

—> c617b456934a

Step 2 : COPY ./dockerapp1 /bin/

—> 20c3783c42ab

Removing intermediate container cab639ab4321

Step 3 : CMD /bin/dockerapp1

—> Running in 31875d3c37f9

—> 21a720a808a7

Removing intermediate container 31875d3c37f9

Successfully built 21a720a808a7

$ sudo docker images

REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE

test v1 21a720a808a7 59 seconds ago 214.6 MB

**四、第一个测试容器**

我们基于image "test:v1"启动一个测试容器：

$ sudo docker run -d "test:v1"

daf3ae88fec23a31cde9f6b9a3f40057953c87b56cca982143616f738a84dcba

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

daf3ae88fec2 test:v1 "/bin/sh -c /bin/doc 17 seconds ago Up 16 seconds condescending_sammet

通过docker run命令，我们基于image"test:v1"启动了一个容器。通过docker ps命令可以看到容器成功启动，容器id：daf3ae88fec2，别名为：condescending_sammet。

根据Dockerfile我们知道，容器启动后将执行"/bin/dockerapp1"这个程序，dockerapp1退出，容器即退出。 run命令的"-d"选项表示容器将以daemon的形式运行，我们在前台无法看到容器的输出。那么我们怎么查看容器的输出呢？我们可以通过 docker logs + 容器id的方式查看容器内应用的标准输出或标准错误。我们也可以进入容器来查看。

进入容器有多种方法，比如用sudo docker attach daf3ae88fec2。attach后，就好比将daemon方式运行的容器 拿到了前台，你可以Ctrl + C一下，可以看到如下dockerapp1的输出:

^Chandle signal: interrupt

另外一种方式是利用nsenter工具进入我们容器的namespace空间。ubuntu 14.04下可以通过如下方式安装该工具：

$ wget [https://www.kernel.org/pub/linux/utils/util-linux/v2.24/util-linux-2.24.tar.gz](https://www.kernel.org/pub/linux/utils/util-linux/v2.24/util-linux-2.24.tar.gz); tar xzvf util-linux-2.24.tar.gz

$ cd util-linux-2.24

$ ./configure –without-ncurses && make nsenter

$ sudo cp nsenter /usr/local/bin

安装后，我们通过如下方式即可进入上面的容器：

$ echo $(sudo docker inspect –format "{{ .State.Pid }}" daf3ae88fec2)

5494

$ sudo nsenter –target 5494 –mount –uts –ipc –net –pid

-bash-4.1# ps -ef

UID PID PPID C STIME TTY TIME CMD

root 1 0 0 09:20 ? 00:00:00 /bin/dockerapp1

root 16 0 0 09:32 ? 00:00:00 -bash

root 27 16 0 09:32 ? 00:00:00 ps -ef

-bash-4.1#

进入容器后通过ps命令可以看到正在运行的dockerapp1程序。在容器内，我们可以通过kill来测试dockerapp1的运行情况：

-bash-4.1# kill -s SIGINT 1

通过前面的attach窗口，我们可以看到dockerapp1输出:

handle signal: interrupt

如果你发送SIGTERM信号，那么dockerapp1将终止运行，容器也就停止了。

-bash-4.1# kill 1

attach窗口显示：

signal termiate received, app exit normally

我们可以看到容器启动后默认执行的时Dockerfile中的CMD命令，如果Dockerfile中有多行CMD命令，Docker在启动容器 时只会执行最后一条CMD命令。如果在docker run中指定了命令，docker则会执行命令行中的命令而不会执行dockerapp1，比如：

$ sudo docker run -t -i "test:v1" /bin/bash

bash-4.1#

这里我们看到直接执行的时bash，dockerapp1并未执行。

**五、docker stop的行为**

我们先来看看docker stop的manual：

$ sudo docker stop –help

Usage: docker stop [OPTIONS] CONTAINER [CONTAINER...]

Stop a running container by sending SIGTERM and then SIGKILL after a grace period

-t, –time=10 Number of seconds to wait for the container to stop before killing it. Default is 10 seconds.

可以看出当我们执行docker stop时，docker会首先向容器内的当前主程序发送一个SIGTERM信号，用于容器内程序的退出。如果容器在收到SIGTERM后没有马上退出， 那么stop命令会在等待一段时间（默认是10s）后，再向容器发送SIGKILL信号，将容器杀死，变为退出状态。

我们来验证一下docker stop的行为。启动刚才那个容器：

$ sudo docker start daf3ae88fec2

daf3ae88fec2

attach到容器daf3ae88fec2

$ sudo docker attach daf3ae88fec2

新打开一个窗口，执行docker stop命令：

$ sudo docker stop daf3ae88fec2

daf3ae88fec2

可以看到attach窗口输出：

handle signal: terminated

signal termiate received, app exit normally

通过docker ps查看，发现容器已经退出。

也许通过上面的例子还不能直观的展示stop命令的**两阶段行为**，因为dockerapp1收到SIGTERM后直接就退出 了，stop命令无需等待容器慢慢退出，也无需发送SIGKILL。我们改造一下dockerapp1这个程序。

我们复制一下dockerapp1.go为dockerapp2.go，编辑dockerapp2.go，将handler中对SIGTERM的 处理注释掉，其他不变：

handler := func(s os.Signal, arg interface{}) {

fmt.Printf("handle signal: %v\n", s)

/*

if s == syscall.SIGTERM {

fmt.Printf("signal termiate received, app exit normally\n")

os.Exit(0)

}

*/

}

我们使用dockerapp2来构建一个新image：test:v2，将Dockerfile中得dockerapp1换成 dockerapp2即可。

$ sudo docker build -t="test:v2" ./

Sending build context to Docker daemon 9.369 MB

Sending build context to Docker daemon

Step 0 : FROM centos:centos6

—> 68edf809afe7

Step 1 : MAINTAINER Tony Bai [<bigwhite.cn@gmail.com>](mailto:bigwhite.cn@gmail.com)

—> Using cache

—> c617b456934a

Step 2 : COPY ./dockerapp2 /bin/

—> 27cd613a9bd7

Removing intermediate container 07c760b6223b

Step 3 : CMD /bin/dockerapp2

—> Running in 1aac086452a7

—> 82eb876fefd2

Removing intermediate container 1aac086452a7

Successfully built 82eb876fefd2

利用image "test:v2"创建一个容器来测试stop。

$ sudo docker run -d "test:v2"

29f3ec1af3c355458cbbd802a5e8a53da28e9f51a56ce822c7bba2a772edceac

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

29f3ec1af3c3 test:v2 "/bin/sh -c /bin/doc 7 seconds ago Up 6 seconds romantic_feynman

Attach到这个容器并观察，在另外一个窗口stop该container。我们在attach窗口只看到如下输出：

handle signal: terminated

stop命令的执行没有立即返回，而是等待容器退出。等待10s后，容器退出，stop命令执行结束。从这个例子我们可以明显看出stop的两阶 段行为。

如果我们以sudo docker run -i -t "test:v1" /bin/bash形式启动容器，那stop命令会将SIGTERM发送给bash这个程序，即使你通过nsenter进入容 器，启动了dockerapp1，dockerapp1也不会收到SIGTERM，dockerapp1会随着容器的退出而被强行终止，就像被 kill -9了一样。

**六、多进程容器服务**程序

上面无论是dockerapp1还是dockerapp2，都是一个单进程服务程序。如果我们在容器内执行一个多进程程序，我们该如何优雅退出 呢？我们先来编写一个多进程的服务程序dockerapp3：

在dockerapp1.go的基础上对main和sysSignalHandleDemo进行修改形成dockerapp3.go，修改后这两 个函数的代码如下：

//dockerapp3.go

… …

func main() {

go sysSignalHandleDemo()

pid, _, err := syscall.RawSyscall(syscall.SYS_FORK, 0, 0, 0)

if err != 0 {

fmt.Printf("err fork process, err: %v\n", err)

return

}

if pid == 0 {

fmt.Printf("i am in child process, pid = %v\n", syscall.Getpid())

time.Sleep(time.Hour) // make the child process wait

}

fmt.Printf("i am parent process, pid = %v\n", syscall.Getpid())

fmt.Printf("fork ok, childpid = %v\n", pid)

time.Sleep(time.Hour) // make the main goroutine wait!

}

func sysSignalHandleDemo() {

ss := signalSetNew()

handler := func(s os.Signal, arg interface{}) {

fmt.Printf("%v: handle signal: %v\n", syscall.Getpid(), s)

if s == syscall.SIGTERM {

fmt.Printf("%v: signal termiate received, app exit normally\n", syscall.Getpid())

os.Exit(0)

}

}

ss.register(syscall.SIGINT, handler)

ss.register(syscall.SIGUSR1, handler)

ss.register(syscall.SIGUSR2, handler)

ss.register(syscall.SIGTERM, handler)

for {

c := make(chan os.Signal)

var sigs []os.Signal

for sig := range ss.m {

sigs = append(sigs, sig)

}

signal.Notify(c)

sig := <-c

err := ss.handle(sig, nil)

if err != nil {

fmt.Printf("%v: unknown signal received: %v, app exit unexpectedly\n", syscall.Getpid(), sig)

os.Exit(1)

}

}

}

dockerapp3利用fork创建了一个子进程，这样dockerapp3实际上是两个进程在运行，各自有自己的signal监听 goroutine，goroutine的处理逻辑是相同的。注意：由于Windows和Mac OS X不具备fork语义，因此在这两个平台上运行dockerapp3不会得到预期结果。

利用dockerapp3，我们创建image "test:v3":

$ sudo docker build -t="test:v3" ./

[sudo] password for tonybai:

Sending build context to Docker daemon 11.24 MB

Sending build context to Docker daemon

Step 0 : FROM centos:centos6

—> 68edf809afe7

Step 1 : MAINTAINER Tony Bai [<bigwhite.cn@gmail.com>](mailto:bigwhite.cn@gmail.com)

—> Using cache

—> c617b456934a

Step 2 : COPY ./dockerapp3 /bin/

—> 6ccf97065853

Removing intermediate container 6d85fe241939

Step 3 : CMD /bin/dockerapp3

—> Running in 75d76380992a

—> c9e7bf361ed7

Removing intermediate container 75d76380992a

Successfully built c9e7bf361ed7

启动基于test:v3 image的容器：

$ sudo docker run -d "test:v3"

781cecb4b3628cb33e1b104ea57e506ad5cb4a44243256ebd1192af86834bae6

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

781cecb4b362 test:v3 "/bin/sh -c /bin/doc 5 seconds ago Up 4 seconds insane_bohr

通过docker logs查看dockerapp3的输出：

$ sudo docker logs 781cecb4b362

i am parent process, pid = 1

fork ok, childpid = 13

i am in child process, pid = 13

可以看出主进程pid为1，子进程pid为13。我们通过stop停止该容器：

$ sudo docker stop 781cecb4b362

781cecb4b362

再次通过docker logs查看：

$ sudo docker logs 781cecb4b362

i am parent process, pid = 1

fork ok, childpid = 13

i am in child process, pid = 13

1: handle signal: terminated

1: signal termiate received, app exit normally

我们可以看到主进程收到了stop发来的SIGTERM并退出，主进程的退出导致容器退出，导致子进程13也无法生存，并且没有优雅退出。而在非 容器状态下，子进程是可以被init进程接管的。

因此对于docker容器内运行的多进程程序，stop命令只会将SIGTERM发送给容器主进程，要想让其他进程也能优雅退出，需要在主进程与 其他进程间建立一种通信机制。在主进程退出前，等待其他子进程退出。待所有其他进程退出后，主进程再退出，容器停止。这样才能保证服务程序的优雅 退出。

**七、容器内启动多个服务程序**

虽说docker [best practice](https://docs.docker.com/articles/dockerfile_best-practices/)建议一个container内只放置一个服务程序，但对已有的一些遗留系统，在架构没有做出重构之前，很可能会有在一个 container中部署两个以上服务程序的情况和需求。而docker Dockerfile只允许执行一个CMD，这种情况下，我们就需要借助类似supervisor这样的进程监控管理程序来启动和管理container 内的多个程序了。

下面我们来自制作一个基于centos:centos6的安装了supervisord以及两个服务程序的image。我们将dockerapp1拷贝一份，并将拷贝命名为dockerapp1-brother。下面是我们的Dockerfile：

FROM centos:centos6

MAINTAINER Tony Bai <bigwhite.cn@gmail.com>

RUN yum install python-setuptools -y

RUN easy_install supervisor

RUN mkdir -p /var/log/supervisor

COPY ./supervisord.conf /etc/supervisord.conf

COPY ./dockerapp1 /bin/

COPY ./dockerapp1-brother /bin/

CMD ["/usr/bin/supervisord"]

supervisord的配置文件supervisord.conf内容如下：

; supervisor config file

[unix_http_server]

file=/var/run/supervisor.sock ; (the path to the socket file)

chmod=0700 ; sockef file mode (default 0700)

[supervisord]

logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)

pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)

childlogdir=/var/log/supervisor ; ('AUTO' child log dir, default $TEMP)

[rpcinterface:supervisor]

supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]

serverurl=unix:///var/run/supervisor.sock ; use a unix:// URL for a unix socket

[supervisord]

nodaemon=false

[program:dockerapp1]

command=/bin/dockerapp1

stdout_logfile=/tmp/dockerapp1.log

stopsignal=TERM

stopwaitsecs=10

[program:dockerapp1-brother]

command=/bin/dockerapp1-brother

stdout_logfile=/tmp/dockerapp1-brother.log

stopsignal=QUIT

stopwaitsecs=10

开始build镜像：

$> sudo docker build -t="test:supervisor-v1" ./

… …

Successfully built d006b9ad10eb

基于该镜像，启动一个容器：

$> sudo docker run -d "test:supervisor-v1"

05ded2b898c90059d4c9b5c6ccc8603b6848ae767360c42bd9b36ff87fb4b9df

执行ps命令查看镜像id：

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

怎么回事？Container没有启动起来？

$ sudo docker ps -a

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

05ded2b898c9 test:supervisor-v1 "/usr/bin/supervisor 22 seconds ago Exited (0) 21 seconds ago hungry_engelbart

通过ps -a查看，container启动是成功了，但是成功退出了。于是尝试查看一下log：

sudo docker logs 05ded2b898c9

/usr/lib/python2.6/site-packages/supervisor-3.1.2-py2.6.egg/supervisor/options.py:296: UserWarning: Supervisord is running as root and it is searching for its configuration file in default locations (including its current working directory); you probably want to specify a "-c" argument specifying an absolute path to a configuration file for improved security.

'Supervisord is running as root and it is searching '

似乎是supervisord转为daemon程序，容器主进程退出了，容器随之终止了。

看来容器内的supervisord不能以daemon形式运行，应该以前台形式run。修改一下supervisord.conf中得配置：

将

[supervisord]

nodaemon=false

改为

[supervisord]

nodaemon=true

重新制作镜像:

$ sudo docker build -t="test:supervisor-v2" ./

Sending build context to Docker daemon 13.12 MB

Sending build context to Docker daemon

Step 0 : FROM centos:centos6

—> 68edf809afe7

Step 1 : MAINTAINER Tony Bai <bigwhite.cn@gmail.com>

—> Using cache

—> c617b456934a

Step 2 : RUN yum install python-setuptools -y

—> Using cache

—> e09c66a1ea8c

Step 3 : RUN easy_install supervisor

—> Using cache

—> 9c8797e8c27e

Step 4 : RUN mkdir -p /var/log/supervisor

—> Using cache

—> 9bfc67f8517d

Step 5 : COPY ./supervisord.conf /etc/supervisord.conf

—> 8c514f998363

Removing intermediate container 4a185856e6ed

Step 6 : COPY ./dockerapp1 /bin/

—> 0317bd4914d3

Removing intermediate container ac5738380854

Step 7 : COPY ./dockerapp1-brother /bin/

—> d89711888bdf

Removing intermediate container eadc9444e716

Step 8 : CMD ["/usr/bin/supervisord"]

—> Running in aaa042ac3914

—> 9655256bbfed

Removing intermediate container aaa042ac3914

Successfully built 9655256bbfed

有了前面的铺垫，这次build image瞬间完成。启动容器，查看容器启动状态，查看容器内supervisord的运行日志如下：

$ sudo docker run -d "test:supervisor-v2"

61916f1c82338b28ced101b6bde119e4afb7c7fa349b4332ed51a43a4586b1b9

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

61916f1c8233 test:supervisor-v2 "/usr/bin/supervisor 16 seconds ago Up 16 seconds prickly_einstein

$ sudo docker logs 8eb3e9892e66

/usr/lib/python2.6/site-packages/supervisor-3.1.2-py2.6.egg/supervisor/options.py:296: UserWarning: Supervisord is running as root and it is searching for its configuration file in default locations (including its current working directory); you probably want to specify a "-c" argument specifying an absolute path to a configuration file for improved security.

'Supervisord is running as root and it is searching '

2014-10-09 14:36:02,334 CRIT Supervisor running as root (no user in config file)

2014-10-09 14:36:02,349 INFO RPC interface 'supervisor' initialized

2014-10-09 14:36:02,349 CRIT Server 'unix_http_server' running without any HTTP authentication checking

2014-10-09 14:36:02,349 INFO supervisord started with pid 1

2014-10-09 14:36:03,354 INFO spawned: 'dockerapp1' with pid 14

2014-10-09 14:36:03,363 INFO spawned: 'dockerapp1-brother' with pid 15

2014-10-09 14:36:04,368 INFO success: dockerapp1 entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)

2014-10-09 14:36:04,369 INFO success: dockerapp1-brother entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)

可以看到supervisord已经将dockerapp1和dockerapp1-brother启动起来了。

现在我们尝试停止容器，我们预期是supervisord在退出前通知dockerapp1和dockerapp1-brother先退出，我们可以通过 查看容器内的/tmp/dockerapp1.log和/tmp/dockerapp1-brother.log来确认supervisord是否做了通 知。

$ sudo docker stop 61916f1c8233

61916f1c8233

$ sudo docker logs 61916f1c8233

… …

2014-10-09 14:37:52,253 WARN received SIGTERM indicating exit request

2014-10-09 14:37:52,254 INFO waiting for dockerapp1, dockerapp1-brother to die

2014-10-09 14:37:52,254 INFO stopped: dockerapp1-brother (exit status 0)

2014-10-09 14:37:52,256 INFO stopped: dockerapp1 (exit status 0)

通过容器的log，我们看出supervisord是等待两个程序退出后才退出的，不过我们还是要看看两个程序的输出日志以最终确认。重新启动容器，通过nsenter进入到容器中。

-bash-4.1# vi /tmp/dockerapp1.log

handle signal: terminated

signal termiate received, app exit normally

-bash-4.1# vi /tmp/dockerapp1-brother.log

handle signal: terminated

signal termiate received, app exit normally

两个程序的标准输出日志证实了我们的预期。

BTW，在物理机上测试supervisord以daemon形式运行，当kill掉supervisord时，supervisord是不会通知其监控 和管理的程序退出的。只有在以non-daemon形式运行时，supervisord才会在退出前先通知下面的程序退出。如果在一段时间内下面程序没有 退出，supervisord在退出前会kill -9强制杀死这些程序的进程。

最后要说的时，在验证一些想法时，没有必要build image，我们可以直接将本地文件copy到容器中，下面是一个例子，我们将dockerapp1和dockerapp1-brother拷贝到镜像中：

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

4d8982bfccc7 centos:centos6 "/bin/bash" 26 minutes ago Up 26 minutes sharp_thompson

$ sudo docker inspect -f '{{.Id}}' 4d8982bfccc7

4d8982bfccc79dea762b41f8a6f669bda1ec73c8881b6ca76e7a7917c62972c4

$ sudo cp dockerapp1 /var/lib/docker/aufs/mnt/4d8982bfccc79dea762b41f8a6f669bda1ec73c8881b6ca76e7a7917c62972c4/bin/dockerapp1

$ sudo cp dockerapp1-brother /var/lib/docker/aufs/mnt/4d8982bfccc79dea762b41f8a6f669bda1ec73c8881b6ca76e7a7917c62972c4/bin/dockerapp1-brother

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

“run命令的”-d”选项表示容器将以daemon的形式运行””-d” 选项的含义是后台（background）运行而不是daemon运行。