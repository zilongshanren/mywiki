---
title: 一种基于内存映射文件的系统运行数据提取方法
url: https://tonybai.com/2013/03/18/sys-running-data-extraction-method-using-mmap/
published: '2013-03-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一种基于内存映射文件的系统运行数据提取方法

这是我无意中想到的一个方法，估计这个方法已经不是什么新鲜的东西了，很可能在类似的问题场景中早已经被使用了。不过这里还是要说说我的思维过程。

近期在学习一些[Linux](http://www.kernel.org)性能查看和分析方面的工具，比如[top](http://tonybai.com/2013/03/02/deep-into-top/)、iostat、vmstat以及sar等。在学习过程中我发现这些工具有个共同的特点，那就是她们采集的Linux运行数据都是从/proc下的文件中实时获取并计算而得出的。众所周知，/proc是[Linux内核](http://tonybai.com/2012/03/15/linux-kernel-hacking-series-kernel-config-compile-and-install/)维护的一个虚拟文件系统，他允许用户在Linux运行时查看内核运行数据（用户可以像查看普通文件一样查看/proc下的目录和文件），甚至是运行时实时改变内核设置。Linux实现/proc的细节不是这里要关注的，吸引我的是Linux的这种提取运行数据的设计。这个设计将Linux运行数据的产生实现细节与第三方性能采集工具间的耦合最大化地解开，这样一来/proc就像是一种Linux的基础服务，为用户提供一种实时的运行数据信息。而用户侧的运行数据查看工具也可以根据用户的需求自由定制，因此有了top、iostat、vmstat、iotop、sar等关注点不同的工具。

好了，说完/proc后，再来说说我们的产品。用户长期以来一直在抱怨我们的产品监控和维护方面手段太过单一，产品就像是一个黑盒，没有提供一种自我运行观察的能力，让客户看不清阿看不清，用户无法实时获取当前某个节点上的业务运行状况，无法采集到这些业务运行的实时基础数据，这的确是我们长期以来的短板（以前这块受重视度也的确不足）。虽然这两年我们在改善运维手段方面的投入已经加大，并收到一些显著的效果，但方案都是集中的，且相对重量级的，不那么敏捷灵活 – 在单节点上依旧无法简单地获取该节点的运行数据。

结合/proc的设计以及我们所遇到的问题，我有了一个大胆的想法：是否可以给我们的业务系统也加上一种类似Linux /proc这样的可提供基础运行数据的服务能力呢？于是就有了下面的解决方法。

Linux /proc下面的数据文件是[Linux Kernel](http://tonybai.com/2012/03/27/how-to-participate-linux-community-section-1/)维护的，并允许用户层的进程实时查看和配置数据。而对于我们的产品而言，提供基础数据的产品实例与提取基础数据的第三方程序是两个独立的用户level的进程，显然我们需要找到一种让这两个进程实时通信、低耦合的且性能代价极低的方法。

我首先想到的是文件，这似乎和/proc的方式一样。你查看一下[sysstat](http://sebastien.godard.pagesperso-orange.fr)源码会发现，像iostat、sar等工具都是用fopen以"r"方式打开/proc/下的各种stat文件，匹配和读取指标项后再统计的。但在User层，两个无亲缘关系进程共同操作一个文件 – 一个读，一个写，the file position indicator是很难控制的，可能涉及文件锁(flock/fcntl)，还要考虑使用的库函数是否是带缓冲的（fread/fgets都是带缓冲 的，不能用），写端需要及时fsync/fflush。总而言之，这么做是甚为自讨没趣的，会给两个程序的实现都带来很大的复杂性以及各种“坑”的。

那用named fifo如何呢？一但用named fifo，这两个进程就会产生启动依赖，如果一端没有启动，另一端会一直阻塞；而且通过fifo传递多种业务数据还可能存在打包和解包的过程，实现起来复杂的很。这显然是耦合十分严重的糟糕方案。

两个进程既要有共同的识别目标，就像/proc/cpuinfo这样的已知路径，一个进程还要能及时地得到另外一个进程运行时的数据，我们不妨尝试一下内存文件映射这个方案：运行数据提供的进程映射一个已知目标文件，比如perf/xxstat，然后在映射后的地址上创建和更新指标数据。比如我们建立一个整型数组，数组的每个元素都代表一种运行指标；而运行数据提取进程同样映射该文件，并在映射后获得数组中的各个元素值。下面是一个示例程序：

/* producer */

int

main()

{

FILE *fp = NULL;

errno = 0;

fp = fopen(STAT_FILE, "w+");

if (fp == NULL) {

printf("can not create stat file , err = %d\n", errno);

return -1;

}

errno = 0;

long size = sysconf(_SC_PAGESIZE);

if (ftruncate(fileno(fp), size) != 0) {

printf("can not set stat file size, err = %d\n", errno);

fclose(fp);

return -1;

}

errno = 0;

char *p = NULL;

p = mmap(NULL, size, PROT_WRITE|PROT_READ, MAP_SHARED, fileno(fp), 0);

if (p == MAP_FAILED) {

printf("can not mmap file, error = %d\n", errno);

fclose(fp);

return -1;

}

errno = 0;

if (fclose(fp) != 0) {

printf("can not close file, error = %d\n", errno);

return -1;

}

/* round up to 8 */

while((int)p % 8 != 0) {

p++;

}

long long *q = (long long*)p;

q[0] = 1;

q[1] = 1000;

q[2] = 10000;

q[3] = 100000;

while(1) {

q[0] += 1;

q[1] += 10;

q[2] += 100;

q[3] += 1000;

usleep(200);

}

return 0;

}

该producer程序首先尝试以"w+"方式打开xxstat文件，并设置文件的大小，然后调用mmap做内存文件映射，理论上来说mmap成功时返回的地址一定是按该平台下最严格内存系数对齐的地址，但这里为了安全起见，又做了一次内存地址的圆整。producer以映射的地址为首地址，建立了一个包含四个元素的、每个元素大小为8字节的整型数组，其中每个元素模拟一个运行指标。在while(1)循环中，producer模拟更新这四个指标数据。

下面是提取producer运行数据的例子程序，其映射过程与producer类似，这里就不贴出完整代码了，完整代码可在[这里](http://code.google.com/p/bigwhite-code)下载。

/* reader.c */

int

main()

{

FILE *fp = NULL;

… …

char *p = NULL;

p = mmap(NULL, size, PROT_READ,

MAP_SHARED, fileno(fp), 0);

if (p == MAP_FAILED) {

printf("can not mmap file, error = %d\n", errno);

fclose(fp);

return -1;

}

… …

long long *q = (long long*)p;

while(1) {

printf("%lld\t\t%lld\t\t%lld\t\t%lld\n", q[0], q[1], q[2], q[3]);

sleep(1);

}

return 0;

}

在producer执行一段时间后，我们可以用reader去提取producer的实时运行数据了。

$ reader

2583 26820 268200 2682000

5793 58920 589200 5892000

9142 92410 924100 9241000

12431 125300 1253000 12530000

15586 156850 1568500 15685000

… …

需要注意的是两个进程映射的虽然是同一个文件，但各自进程空间映射的地址是不同的。如果在指标里存储地址数据，那另外一个进程在访问该地址时必然会出现问题。

在这个方案中，由于两个进程是读写同一块内存(虽然在各自进程空间的地址是不同的），因此数据是实时的。但由于两个进程间并没有任何同步机制，可能会产生误差，就好比一个进程中的两个线程对进程中某块地址空间一读一写这种情况一样。不过对于我们这种场景，这个问题是一般是可以被容忍和接受的，毕竟我们通过运行数据只是想了解一种运行趋势而已。如果producer中存在多个有亲缘关系的子进程或多线程要同时更新基础运行数据，那势必是要用锁或其他原子操作做数据操作的同步的。另外我们用的是内存映射具名的文件，OS会定期将数据刷到磁盘上，不过这个消耗对于小文件来说，对整体性能影响可忽略不计。

一旦业务系统具备了提供基础运行数据的能力，我们就可以根据我们的需求按照数据的格式打造我们所需要的各类数据提取和分析工具了。如果需要长期记录业务系统的运行情况，我们也可以实现类似sar这样的工具，以在后台定期对系统的运行数据进行记录，并提供历史查询等相关功能。

这种基于内存映射文件的方法还有一个好处，那就是我们可以用任何支持mmap调用的编程语言来实现数据提取工具，而不一定非得用C/C++这种原生适配Linux API的语言。

如果你觉得这种方案可行，那后续的重点就是基础运行数据的设计问题了。罗马不是一天建成的，/proc下的基础数据也不是一天就设计到位的。在基础数据设计这方面也是需要有很多考虑的，比如是文本还是二进制，用什么类型数据，还可能需要考虑一些[数据对齐](http://tonybai.com/2005/08/09/also-talk-about-memory-alignment/)问题等。当然这就不是本文的重点了，就不细说了。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

好点子，为什么不是交易数据实时数据往自己到监控平台发送？

这种方式主要是可以简单快速的看到某个节点的运行压力趋势，主要是运维观测用，并非要精确统计。你提到的那种我们也有的，相对更重量级一些，需要外部配合。

了解了，不过我觉得我说的更可控一点，实现简单，只需在联机交易添加一个发送接口即可，UDP也可