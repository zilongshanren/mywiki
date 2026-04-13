---
title: 利用ZooKeeper服务实现分布式系统的Leader选举
url: https://tonybai.com/2013/08/23/leader-election-using-zookeeper/
published: '2013-08-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 利用ZooKeeper服务实现分布式系统的Leader选举

每次与Java组的同事们坐下来谈技术、谈理想、谈人生时，Java组的同事总会向我们投来羡慕的眼光：卧槽！又是自己开发的工具，太NB了。这时C程序 员们的脸上就会洋溢出自豪的笑容，然后内心骂道：谁让我们没有现成的呢。另一个空间里的某些“无C不欢”们或者某些“C Guru”们会骂道：靠，有了也不用，自己写！

有时候，[C程序员](http://tonybai.com/tag/c)真的有一种下意识：不情愿使用其他语言开发的工具、框架或服务，且比其他程序员更爱“[重新发明轮子](http://tonybai.com/2012/11/02/treat-reinventing-the-wheel-dialectically)”（有利有弊）。也许这是某种 骨子里的自负在搞怪；另外一个极端：今天和我聊天的一个经验丰富的C程序员还在忧虑：如果离职是否有公司会要他:(。

其实这个时代的C程序员一直活得**挺纠结**^_^。

这个世界，软硬件发展日新月异，越来越多的后端程序用Java等其他语言实现。Java高级选手在这个世界上也甚是吃香，这个你看看各大招聘网站 就知道了。再听听坊间“BAT”三巨头给出的高高在上的offer价格，也可以看出Java程序员是多么的有“钱途”和受欢迎了。当然拿好offer的前提是你的Java底子不薄。

其实无论用什么编程语言，成为牛人后，钱途也都是杠杠的。

没有什么好的开场白，于是有了上面一些“胡言乱语”。我们言归正传。

本文是一篇初级技术博文。讲的是如何使用[ZooKeeper](http://zookeeper.apache.org) C API通过ZooKeeper的服务实现分布式系统的Leader选举。当然这一试验是为了尝试解决我们自己的分布式系统在集中配置数据分发这一环节上的 一个“固疾”。还好我还不那么纠结，也没有重新实现ZooKeeper的冲动，于是我就用了ZooKeeper这一Java实现的成熟的分布式 系统的服务框架。

*** 搭建ZooKeeper服务环境**

– 下载官方stable release版本 – ZooKeeper3.4.5。解压后，将$*ZooKeeper_INSTALL_PATH*/bin加入到PATH变量中（其中ZooKeeper_INSTALL_PATH为解压后ZooKeeper-3.4.5目录的绝对路径）。

– 试验环境下，最简单的ZooKeeper用法就是使用单机版。

进入到$ZooKeeper_INSTALL_PATH/conf下，将zoo_sample.cfg改名为zoo.cfg，即可作为单机版ZooKeeper的配置文件。当然你也可以像我一样随意修改修改：

# The number of milliseconds of each tick

tickTime=2000

# The number of ticks that the initial

# synchronization phase can take

initLimit=5

# The number of ticks that can pass between

# sending a request and getting an acknowledgement

syncLimit=2

dataDir=/home/tonybai/proj/myZooKeeper

# the port at which the clients will connect

clientPort=2181


如果你要体验多机版ZooKeeper服务，那你还要继续动动手脚，以双机版为例，假设有两个ZooKeeper节点(10.0.0.13和10.0.0.14)：

10.0.0.13上的ZooKeeper节点1的配置文件如下：

# The number of milliseconds of each tick

tickTime=2000

# The number of ticks that the initial

# synchronization phase can take

initLimit=5

# The number of ticks that can pass between

# sending a request and getting an acknowledgement

syncLimit=2

dataDir=/home/tonybai/proj/myZooKeeper

# the port at which the clients will connect

clientPort=2181

server.1=10.0.0.13:2888:3888

server.2=10.0.0.14:2888:3888

10.0.0.14上的ZooKeeper节点2的配置文件如下：

# The number of milliseconds of each tick

tickTime=2000

# The number of ticks that the initial

# synchronization phase can take

initLimit=5

# The number of ticks that can pass between

# sending a request and getting an acknowledgement

syncLimit=2

dataDir=/home/tonybai/proj/myZooKeeper

# the port at which the clients will connect

clientPort=2181

server.1=10.0.0.13:2888:3888

server.2=10.0.0.14:2888:3888

别忘了在每个节点的dataDir下分别创建一个myid文件：

在10.0.0.13节点1上执行：


$> echo 1 > myid

在10.0.0.14节点2上执行：


$> echo 2 > myid

启动ZooKeeper执行：

$> zkServer.sh start

模拟一个客户端连到ZooKeeper服务上：

$> zkCli.sh

成功链接后，你将进入一个命令行交互界面：

[zk: 10.0.0.13:2181(CONNECTED) 1] help

ZooKeeper -server host:port cmd args

connect host:port

get path [watch]

ls path [watch]

set path data [version]

rmr path

delquota [-n|-b] path

… …

*** 选主原理**

ZooKeeper在选主过程中提供的服务就好比一栋名为"/election"小屋，小屋只有一个门，各节点只能通过这个门逐个进入。每个节点进入后， 都会被分配唯一编号(member-n)，编号n自小到大递增，节点编号最小的自封为Leader，其他节点只能做跟班的（follower) – 这年头还是小的吃香：原配干不过小三儿，小三儿干不过小四儿，不是么^_^！）。

每当一个节点离开，ZooKeeper都会通知屋内的所有节点，屋内节点收到通知后再次判断一下自己是否是屋内剩余节点中编号最小的节点，如果是，则自封为Leader，否则为Follower。

再用稍正式的语言重述一遍：

各个子节点同时在某个ZooKeeper数据路径/election下建立"ZOO_SEQUENCE|ZOO_EPHEMERAL"节点 – member，且各个节点监视(Watch) /election路径的子路径的变更事件。ZooKeeper的sequence节点特性保证节点创建时会被从小到大加上编号。同时节点的 ephemeral特性保证一旦子节点宕机或异常停掉，其对应的member节点会被ZooKeeper自动删除，而其他节点会收到该变更通知，重新判定 自己是leader还是follower以及谁才是真正的leader。

*** 示例代码**

关于ZooKeeper的C API的使用资料甚少，但这里就偏偏要用C API举例。

C API的安装方法：进入$ZOOKEEPER_INSTALL_PATH/src/c下面，configure->make->make install即可。

ZooKeeper的C API分为同步与异步两种模式，这里简单起见用的都是同步机制。代码不多，索性全贴出来。在[这里](https://github.com/bigwhite/experiments)能checkout到全部代码。

/* election.c */

#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <unistd.h>

#include "zookeeper.h"

static int

is_leader(zhandle_t* zkhandle, char *myid);

static void

get_node_name(const char *buf, char *node);

struct watch_func_para_t {

zhandle_t *zkhandle;

char node[64];

};

void

election_children_watcher(zhandle_t* zh, int type, int state,

const char* path, void* watcherCtx)

{

int ret = 0;

struct watch_func_para_t* para= (struct watch_func_para_t*)watcherCtx;

struct String_vector strings;

struct Stat stat;

/* 重新监听 */

ret = zoo_wget_children2(para->zkhandle, "/election", election_children_watcher,

watcherCtx, &strings, &stat);

if (ret) {

fprintf(stderr, "child: zoo_wget_children2 error [%d]\n", ret);

exit(EXIT_FAILURE);

}

/* 判断主从 */

if (is_leader(para->zkhandle, para->node))

printf("This is [%s], i am a leader\n", para->node);

else

printf("This is [%s], i am a follower\n", para->node);

return;

}

void def_election_watcher(zhandle_t* zh, int type, int state,

const char* path, void* watcherCtx)

{

printf("Something happened.\n");

printf("type: %d\n", type);

printf("state: %d\n", state);

printf("path: %s\n", path);

printf("watcherCtx: %s\n", (char *)watcherCtx);

}

int

main(int argc, const char *argv[])

{

const char* host = "10.0.0.13:2181";

zhandle_t* zkhandle;

int timeout = 5000;

char buf[512] = {0};

char node[512] = {0};

zoo_set_debug_level(ZOO_LOG_LEVEL_WARN);

zkhandle = zookeeper_init(host, def_election_watcher, timeout,

0, "Zookeeper examples: election", 0);

if (zkhandle == NULL) {

fprintf(stderr, "Connecting to zookeeper servers error…\n");

exit(EXIT_FAILURE);

}

/* 在/election下创建member节点 */

int ret = zoo_create(zkhandle,

"/election/member",

"hello",

5,

&ZOO_OPEN_ACL_UNSAFE, /* a completely open ACL */

ZOO_SEQUENCE|ZOO_EPHEMERAL,

buf,

sizeof(buf)-1);

if (ret) {

fprintf(stderr, "zoo_create error [%d]\n", ret);

exit(EXIT_FAILURE);

}

get_node_name(buf, node);

/* 判断当前是否是Leader节点 */

if (is_leader(zkhandle, node)) {

printf("This is [%s], i am a leader\n", node);

} else {

printf("This is [%s], i am a follower\n", node);

}

struct Stat stat;

struct String_vector strings;

struct watch_func_para_t para;

memset(¶, 0, sizeof(para));

para.zkhandle = zkhandle;

strcpy(para.node, node);

/* 监视/election的所有子节点事件 */

ret = zoo_wget_children2(zkhandle, "/election", election_children_watcher, ¶, &strings, &stat);

if (ret) {

fprintf(stderr, "zoo_wget_children2 error [%d]\n", ret);

exit(EXIT_FAILURE);

}

/* just wait for experiments*/

sleep(10000);

zookeeper_close(zkhandle);

}

static int

is_leader( zhandle_t* zkhandle, char *myid)

{

int ret = 0;

int flag = 1;

struct String_vector strings;

ret = zoo_get_children(zkhandle, "/election", 0, &strings);

if (ret) {

fprintf(stderr, "Error %d for %s\n", ret, "get_children");

exit(EXIT_FAILURE);

}

/* 计数 */

for (int i = 0; i < strings.count; i++) {

if (strcmp(myid, strings.data[i]) > 0) {

flag = 0;

break;

}

}

return flag;

}

static void

get_node_name(const char *buf, char *node)

{

const char *p = buf;

int i;

for (i = strlen(buf) – 1; i >= 0; i–) {

if (*(p + i) == '/') {

break;

}

}

strcpy(node, p + i + 1);

return;

}

编译这个代码：

$> gcc -g -std=gnu99 -o election election.c -DTHREADED -I/usr/local/include/zookeeper -lzookeeper_mt -lpthread

验证时，我们在不同窗口启动三次election程序：

窗口1， election启动：

$> election

Something happened.

type: -1

state: 3

path:

watcherCtx: Zookeeper examples: election

This is [member0000000001], i am a leader

窗口2，election启动：

$> election

Something happened.

type: -1

state: 3

path:

watcherCtx: Zookeeper examples: election

This is [member0000000002], i am a follower

此时窗口1中的election也会收到/election的字节点增加事件，并给出响应：

This is [member0000000001], i am a leader

同理当窗口3中的election启动时，窗口1和2中的election都能收到变动通知，并给予响应。

我们现在停掉窗口1中的election，大约5s后，我们在窗口2中看到：

This is [member0000000002], i am a leader

在窗口3中看到：

This is [member0000000003], i am a follower

可以看出窗口2和3中的election程序又做了一次自我选举。结果窗口2中的election由于节点编号最小而被选为Leader。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论