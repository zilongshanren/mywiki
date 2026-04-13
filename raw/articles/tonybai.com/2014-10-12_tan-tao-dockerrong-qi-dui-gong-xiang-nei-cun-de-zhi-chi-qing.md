---
title: 探讨docker容器对共享内存的支持情况
url: https://tonybai.com/2014/10/12/discussion-on-shared-mem-support-in-docker/
published: '2014-10-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 探讨docker容器对共享内存的支持情况

我们的遗留系统广泛使用了性能最佳的IPC方式 – [共享内存](http://en.wikipedia.org/wiki/Shared_memory)，而且用到了两种共享内存的实现方式：System V共享内存(shmget、shmat、shmdt)以及Mmap映射Regular File。System V共享内存支持一定程度上的内存数据持久化，即当程序创建共享内存对象后，如果不显式删除或物理主机重启，该IPC对象会一直保留，其中的数据也不会丢 失；mmap映射Regular File的方式支持内存数据持久化到文件中，即便物理主机重启，这部分数据依旧不会丢失，除非显式删除文件。这两个共享内存机制，尤其是其持久化的特性是 我们的系统所依赖的。但是在[Docker](http://docker.com)容器中，这两种共享内存机制依旧能被很好的支持吗？我们通过试验来分析一下。

**一、System V共享内存**

一个启动的Docker容器就是一个拥有了自己的内核名字空间的进程，其**pid****、net****、ipc****、mnt****、uts****、user**等均与其他进程隔离，对于运行于该容器内的程序而言，它仿佛会觉得它独占了一台“主机”。对于这类“主机”，我们首先来测试一下其中的system v共享内存是否依旧能像物理主机上一样，在程序退出后依旧能保持持久化？在容器退出后能保持么？

我们先来写两个测试程序，一个用于创建system v共享内存，并写入一些数据，另外一个程序则映射该共享内存并尝试读出内存中的数据。由于Golang目前仍未提供对System V共享内存的高级封装接口，通过syscall包的Syscall调用又太繁琐，因此我们直接使用C代码与Go代码结合的方式实现这两个测试程序。之前写 过一篇名为《[Go与C语言互操作](http://tonybai.com/2012/09/26/interoperability-between-go-and-c/)》的博文，看不懂下面代码的朋友，可以先阅读一下这篇文章。

//systemv_shm_wr.go

package main

//#include <sys/types.h>

//#include <sys/ipc.h>

//#include <sys/shm.h>

//#include <stdio.h>

//

//#define SHMSZ 27

//

//int shm_wr() {

// char c;

// int shmid;

// key_t key;

// char *shm, *s;

//

// key = 5678;

//

// if ((shmid = shmget(key, SHMSZ, IPC_CREAT | 0666)) < 0) {

// return -1;

// }

//

// if ((shm = shmat(shmid, NULL, 0)) == (char *) -1) {

// return -2;

// }

//

// s = shm;

// for (c = 'a'; c <= 'z'; c++)

// *s++ = c;

// s = NULL;

//

// return 0;

//}

import "C"

import "fmt"

func main() {

i := C.shm_wr()

if i != 0 {

fmt.Println("SystemV Share Memory Create and Write Error:", i)

return

}

fmt.Println("SystemV Share Memory Create and Write Ok")

}

//systemv_shm_rd.go

package main

//#include <sys/types.h>

//#include <sys/ipc.h>

//#include <sys/shm.h>

//#include <stdio.h>

//

//#define SHMSZ 27

//

//int shm_rd() {

// char c;

// int shmid;

// key_t key;

// char *shm, *s;

//

// key = 5678;

//

// if ((shmid = shmget(key, SHMSZ, 0666)) < 0) {

// return -1;

// }

//

// if ((shm = shmat(shmid, NULL, 0)) == (char *) -1) {

// return -2;

// }

//

// s = shm;

//

// int i = 0;

// for (i = 0; i < SHMSZ-1; i++)

// printf("%c ", *(s+i));

// printf("\n");

// s = NULL;

//

// return 0;

//}

import "C"

import "fmt"

import "fmt"

func main() {

i := C.shm_rd()

if i != 0 {

fmt.Println("SystemV Share Memory Create and Read Error:", i)

return

}

fmt.Println("SystemV Share Memory Create and Read Ok")

}

我们通过go build构建上面两个程序，得到两个测试用可执行程序：systemv_shm_wr和systemv_shm_rd。下面我们来构建我们的测试用docker image，Dockerfile内容如下：

FROM centos:centos6

MAINTAINER Tony Bai <bigwhite.cn@gmail.com>

COPY ./systemv_shm_wr /bin/

COPY ./systemv_shm_rd /bin/

构建Docker image：“shmemtest:v1”：

$ sudo docker build -t="shmemtest:v1" ./

Sending build context to Docker daemon 16.81 MB

Sending build context to Docker daemon

Step 0 : FROM centos:centos6

—> 68edf809afe7

Step 1 : MAINTAINER Tony Bai <bigwhite.cn@gmail.com>

—> Using cache

—> c617b456934a

Step 2 : COPY ./systemv_shm_wr /bin/

—> ea59fb767573

Removing intermediate container 4ce91720897b

Step 3 : COPY ./systemv_shm_rd /bin/

—> 1ceb207b1009

Removing intermediate container 7ace7ad53a3f

Successfully built 1ceb207b1009

启动一个基于该image的容器：

$ sudo docker run -it "shmemtest:v1" /bin/bash

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

0a2f37bee6eb shmemtest:v1 "/bin/bash" 28 seconds ago Up 28 seconds elegant_hawking

进入容器，先后执行systemv_shm_wr和systemv_shm_rd，我们得到如下结果：

bash-4.1# systemv_shm_wr

SystemV Share Memory Create and Write Ok

bash-4.1# systemv_shm_rd

a b c d e f g h i j k l m n o p q r s t u v w x y z

SystemV Share Memory Create and Read Ok

在容器运行过程中，SystemV共享内存对象是可以持久化的。systemv_shm_wr退出后，数据依旧得以保留。我们接下来尝试一下重启container后是否还能读出数据：

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

0a2f37bee6eb shmemtest:v1 "/bin/bash" 8 minutes ago Up 8 minutes elegant_hawking

$ sudo docker stop 0a2f37bee6eb

0a2f37bee6eb

$ sudo docker start 0a2f37bee6eb

0a2f37bee6eb

$ sudo docker attach 0a2f37bee6eb

bash-4.1# systemv_shm_rd

SystemV Share Memory Create and Read Error: -1

程序返回-1，显然在shmget时就出错了，系统已经没有了key为"5678"的这个共享内存IPC对象了。也就是说当容器stop时，就好比我们的物理主机关机，docker将该容器对应的共享内存IPC对象删除了。

从原理上分析，似乎我们也能得出此结论：毕竟Docker container是通过kernel namespace隔离的，容器中的进程在IPC资源申请时需要加入namespace信息。打个比方，如果我们启动容器的进程pid(物理主机视角)是 1234，那么这容器内进程申请的共享内存IPC资源（比如key=5678）的标识应该类似于“1234:5678”这样的形式。重启容器 后，Docker Daemon无法给该容器分配与上次启动相同的pid，因此pid发生了变化，之前容器中的"1234:5678"保留下来也是毫无意义的，还无端占用系 统资源。因此，System V IPC在Docker容器中的运用与物理机有不同，这方面要小心，目前似乎没有很好的方法，也许以后Docker会加入全局IPC，这个我们只能等待。

**二、Mmap映射共享内存**

接下来我们探讨mmap共享内存在容器中的支持情况。mmap常见的有两类共享内存映射方式，一种映射到/dev/zero，另外一种则是映射到 Regular Fiile。前者在程序退出后数据自动释放，后者则保留在映射的文件中。后者对我们更有意义，这次测试的也是后者。

同样，我们也先来编写两个测试程序。

//mmap_shm_wr.go

package main

//#include <stdio.h>

//#include <sys/types.h>

//#include <sys/mman.h>

//#include <fcntl.h>

//

//#define SHMSZ 27

//

//int shm_wr()

//{

// char c;

// char *shm = NULL;

// char *s = NULL;

// int fd;

// if ((fd = open("./shm.txt", O_RDWR|O_CREAT, S_IRUSR|S_IWUSR)) == -1) {

// return -1;

// }

//

// lseek(fd, 500, SEEK_CUR);

// write(fd, "\0", 1);

// lseek(fd, 0, SEEK_SET);

//

// shm = (char*)mmap(shm, SHMSZ, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);

// if (!shm) {

// return -2;

//

// }

//

// close(fd);

// s = shm;

// for (c = 'a'; c <= 'z'; c++) {

// *(s+(int)(c – 'a')) = c;

// }

// return 0;

//}

import "C"

import "fmt"

func main() {

i := C.shm_wr()

if i != 0 {

fmt.Println("Mmap Share Memory Create and Write Error:", i)

return

}

fmt.Println("Mmap Share Memory Create and Write Ok")

}

//mmap_shm_rd.go

package main

//#include <stdio.h>

//#include <sys/types.h>

//#include <sys/mman.h>

//#include <fcntl.h>

//

//#define SHMSZ 27

//

//int shm_rd()

//{

// char c;

// char *shm = NULL;

// char *s = NULL;

// int fd;

// if ((fd = open("./shm.txt", O_RDONLY)) == -1) {

// return -1;

// }

//

// shm = (char*)mmap(shm, SHMSZ, PROT_READ, MAP_SHARED, fd, 0);

// if (!shm) {

// return -2;

// }

//

// close(fd);

// s = shm;

// int i = 0;

// for (i = 0; i < SHMSZ – 1; i++) {

// printf("%c ", *(s + i));

// }

// printf("\n");

//

// return 0;

//}

import "C"

import "fmt"

func main() {

i := C.shm_rd()

if i != 0 {

fmt.Println("Mmap Share Memory Read Error:", i)

return

}

fmt.Println("Mmap Share Memory Read Ok")

}

我们通过go build构建上面两个程序，得到两个测试用可执行程序：mmap_shm_wr和mmap_shm_rd。下面我们来构建我们的测试用docker image，Dockerfile内容如下：

FROM centos:centos6

MAINTAINER Tony Bai <bigwhite.cn@gmail.com>

COPY ./mmap_shm_wr /bin/

COPY ./mmap_shm_rd /bin/

构建Docker image：“shmemtest:v2”：

$ sudo docker build -t="shmemtest:v2" ./

Sending build context to Docker daemon 16.81 MB

Sending build context to Docker daemon

Step 0 : FROM centos:centos6

—> 68edf809afe7

Step 1 : MAINTAINER Tony Bai <bigwhite.cn@gmail.com>

—> Using cache

—> c617b456934a

Step 2 : COPY ./mmap_shm_wr /bin/

—> Using cache

—> 01e2f6bc7606

Step 3 : COPY ./mmap_shm_rd /bin/

—> 0de95503c851

Removing intermediate container 0c472e92809f

Successfully built 0de95503c851

启动一个基于该image的容器：

$ sudo docker run -it "shmemtest:v2" /bin/bash

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

1182f9eca367 shmemtest:v2 "/bin/bash" 11 seconds ago Up 11 seconds distracted_elion

进入容器，先后执行mmap_shm_wr和mmap_shm_rd，我们得到如下结果：

bash-4.1# mmap_shm_wr

Mmap Share Memory Create and Write Ok

bash-4.1# mmap_shm_rd

a b c d e f g h i j k l m n o p q r s t u v w x y z

Mmap Share Memory Read Ok

我们接下来尝试一下重启container后是否还能读出数据：

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

1182f9eca367 shmemtest:v2 "/bin/bash" About a minute ago Up About a minute distracted_elion

$ sudo docker stop 1182f9eca367

1182f9eca367

$ sudo docker start 1182f9eca367

1182f9eca367

$ sudo docker attach 1182f9eca367

bash-4.1# mmap_shm_rd

a b c d e f g h i j k l m n o p q r s t u v w x y z

Mmap Share Memory Read Ok

通过执行结果可以看出，通过mmap映射文件方式，共享内存的数据即便在容器重启后依旧可以得到保留。从原理上看，shm.txt是容器内 的一个文件，该文件存储在容器的可写文件系统layer中，从物理主机上看，其位置在/var/lib/docker/aufs/mnt /container_full_id/下，即便容器重启，该文件也不会被删除，而是作为容器文件系统的一部分：

$ sudo docker inspect -f '{{.Id}}' 1182f9eca367

1182f9eca36756219537f9a1c7cd1b62c6439930cc54bc69e87915c5dc8f7b97

$ sudo ls /var/lib/docker/aufs/mnt/1182f9eca36756219537f9a1c7cd1b62c6439930cc54bc69e87915c5dc8f7b97

bin dev etc home lib lib64 lost+found media mnt opt proc root sbin selinux ** shm.txt ** srv sys tmp usr var

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

不错

赞。