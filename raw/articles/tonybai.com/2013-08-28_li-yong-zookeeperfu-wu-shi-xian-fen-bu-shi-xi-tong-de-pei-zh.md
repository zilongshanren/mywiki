---
title: 利用ZooKeeper服务实现分布式系统的配置数据同步
url: https://tonybai.com/2013/08/28/implement-config-sync-for-distributed-system-with-zookeeper-services/
published: '2013-08-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 利用ZooKeeper服务实现分布式系统的配置数据同步

*很多时候，一旦习惯了某些事情，也就习惯了它们的恶劣，习惯了它们的丑陋，习惯了它们“赋予”你的各种痛苦。
– Tony Bai*

**一、痼疾难解**

曾几何时，在那个还没有集群化，没有分布式的时代，它还是一个不错的方案，至少在线上没有暴露出太多问题，它也不在我们关注的重点范围之内。但随 着集群化、分布式的新版本的到来，那一大坨遗留的代码就变得格外让人不顺眼，同时问题也随之在线上暴露开来了。

这里的“它”指的就是我们目前的业务配置数据同步方案。简单描述这个方案如下：

* 方案涉及两个角色 – 数据库(DB)与应用节点（app_node)；

* 所有的业务配置数据均统一存储在DB中；

* 应用节点在启动后从DB中读取最新业务配置数据；

* 应用节点运行过程中，如果DB中的业务配置数据发生变更（增/删/改），DB中的触发器(trigger)将会执行。在触发器的脚本中，触发器将会【串 行】地与每个应用节点建立TCP链接，并将业务配置表的变更信息发给各个应用节点。 应用节点会接收并【解析】触发器发过来变更数据包，并同步到自己的本地内存中。这样就达到了运行时更新配置的目的。

上面我用【】标记了两个关键词：“串行”和“解析”。这两个词隐含有这个方案的两个主要问题。

“串行” – 意味着每一次DB的业务配置数据变更，trigger脚本都要逐个与应用节点建立链接并收发数据。当应用节点逐渐增多时，每一次业务数据同步都会相当地耗 时。尤其是当某个应用节点所在主机出现问题时，到该节点链接建立的过程会阻塞，导致整个业务配置数据同步的时间达到无法忍受的地步。

“解析” – 我们自定义了trigger与应用节点之间的协议包。协议包中包含了每次变更的详细信息，比如在某个表添加一条记录，trigger会将这个记录的每个字 段信息排成一行打包发给应用节点。应用节点收到这个包后，会根据已有的表字段信息对该包进行解析。看得出这是一个很强的耦合：表字段一旦修 改，trigger脚本要修改，应用节点的解析函数要修改，还要考虑协议包中表字段的排序。如果应用节点解析时与trigger脚本打包时的字段 顺序不同的话，那就可能出现严重错误，而且这种错误有时难于校验并难于发现。

**二、曾经的努力**

针对这个方案的不足，我们曾经也做过改进，但主要针对的是解决“串行”这个问题上。

第一次改进：同步的发起能否并行做？trigger脚本能否并行发起对各个应用节点的链接建立请求？

Java组同事对trigger脚本做了改进。让trigger脚本调用function，而function中又调用了写好的Java方 法，Java代码由DB加载到环境中。在Java方法中创建多个同步线程，并发与各应用节点建立链接并发送数据。这个方法的确可以变“串行”为 “并行”，但不知为何生产环境中实际运行时偶尔会出现异常，该异常发生在DB中，影响很大。有时还会导致DB的一些异常现象。至今原因尚未明确， 我们无奈退回到以前的方案。

第二次改进：从Push模式到Pull模式

在之前部门新规划的一个产品中，开发人员对数据同步的机制做了重新的设计，将原来的Push模式改为了Pull模式。大致方案是：


* 业务数据变更时，trigger直接将变更内容（以老方案中那个协议包的打包格式）写到一个“变更日志表”中，每条记录有一个唯一的序号，序号递增。

* 应用节点启动后，从DB加载最新配置信息，查询“变更日志表”，得到该表内最新的一条记录的序号n。

* 应用节点以“轮询”的方式定期查询“变更日志表”，并读取和解析那些序号比序号n更新的记录；更新完后，将继续保存最新的一条记录序号。

* 数据库中有job定期对“变更日志表”中的记录进行过期删除处理。

个人感觉第二个方案应该是理想方案的一个雏形，虽然目前它的同步更新可能不是那么及时，与DB交互过多（方案细节中每个应用节点在处理完一条记录 后还要更新记录的状态）。该方案设计者也完全也可以放弃那个导致耦合的协议包设计，但他最终还是选择保留了原有协议包解析函数。目前该方案在产品 环境下运行还算良好，并未暴露出什么问题。这算是一次有效的改进，也为本文中要提到的方案提供了一些思路启示。

**三、与时俱进**

[ZooKeeper](http://zookeeper.apache.org)生来就具备解决分布式系统的配置分发和同步的能力。利用ZooKeeper服务实现分布式系统的统一配置中心已经不是那么新鲜 的话题了。最简单的模型莫过于将配置数据存储在ZooKeeper上的路径节点上，然后应用节点在这些配置节点上添加watch。当配置数据变更 时，每个应用节点都可以及时得到通知，同步到最新数据。这种模型对于一些量少简单的系统配置来说较为合适。对于我们每个表动辄上万条配置的情形似 乎不那么适合，想象一下每个应用节点要添加上万个watch，这对ZooKeeper而言也是压力山大啊。因此用ZooKeeper提供的诸多服 务如何来优化我们上面提到的两个主要问题呢？这里提出一种方案仅供参考。

方案示意图：

DB —-> **Config Center Services**(css_agent + ZooKeeper) —> App Node

在新方案中，我们要：

保留 – 保留trigger脚本，作为业务数据变更的唯一的触发起点；

摒弃 – 摒弃那个复杂的带来耦合的协议格式；

借鉴 – 借鉴“Push -> Pull”的数据获取方式。

新方案中除了DB、应用节点(app_node)外，新增加了一个角色Config Center Services(缩写为ccs），ccs由ZooKeeper + ccs_agent的集群组成。简单起见，每个ZooKeeper节点上部署一个ccs_agent。这些角色之间的数据流和指令流关系，即该方案的原理 如下：

*** 初始化**

– ZooKeeper集群启动；

– ccs_agent启动，利用ZooKeeper提供的[leader election服务](http://tonybai.com/2013/08/23/leader-election-using-zookeeper/)，选出ccs_agent leader。ccs_agent leader启动后负责在ZooKeeper中建立业务配置表node，比如：表employee_info_tab对应的node路径为“/ccs /foo_app/employee_info_tab”；

– ccs_agent启动后会监听一个端口，用来接受DB trigger向其发起的数据链接；

– 应用节点启动，监听ZooKeeper上所有（数量有限的）业务配置表node的child event；


*** 数据变更**

– DB中某业务表比如employee_info_tab增加了一条id为"1234567"的记录；

– 触发器启动，向ccs_agent cluster中任意一个可用的节点建立链接，并将数据包“^employee_info_tab|ADD|1234567$"发送给 ccs_agent；

– ccs_agent收取并解析trigger发来的数据包，在对应的/ccs/foo_app/employee_info_tab下建立**ZOO_SEQUENCE**类 型节点“item-000000000”，该节点的值为“ADD 1234567"；

– ZooKeeper将/ccs/foo_app/employee_info_tab节点的child事件发给所有watch该节点事件的应用节点；

– 应用节点“取出”/ccs/foo_app/employee_info_tab节点下的children节点"item-000000000"，并读取 其值，后续到DB的employee_info_tab中将id = 1234567的这条记录select出来，将该条记录更新到本地内存中。应用节点记录下处理过的当下节点id为"item-000000000"；

– DB业务表employee_info_tab又增加了两条记录，id分别为"7777777"和"8888888"，经过上面描述的流程，/ccs /foo_app/employee_info_tab节点下会增加"item-000000001"和"item-000000002"两项； 应用节点最终会收到child事件通知。应用节点“取出”/ccs/foo_app/employee_info_tab节点下的所有 children节点并排序。之后，处理那些id号大于"item-000000000"的节点，并将当前节点id记录为“item- 000000002"。依次类推。

*** 过期处理**

– ccs_agent leader负责定期扫描ZooKeeper中/ccs下各个表节点下的子项，对于超出过期时间的item进行删除处理。

*** 应用节点重启**

- 应用节点重启后，会首先从db读取最新信息，并记录启动时间戳；

- 应用节点重启后，在收到zookeeper的数据变更事件后，会根据当前时间戳与变更表节点下的item创建时间进行比较，并仅处理比启动时间戳新的 item的数据。


这个方案主要利用了ZooKeeper提供的leader election服务以及sequence节点的特性，几点好处在于：

– 串行通知变为并行通知，且通知到达及时；

– 变更数据的Push模式为Pull模式，降低了或去除了诸多耦合，包括：

1) 去除trigger脚本与表字段及字段顺序的耦合；

2) 去除应用节点与表字段顺序的耦合；

3) 降低应用节点与表字段构成的耦合。

– 应用节点无需复杂的包解析，简化后期维护。

当然为了该方案新增若干网元会给产品部署和维护带来一些复杂性，这算是不足之处吧。

**四、Demo**

[这里](https://github.com/bigwhite/experiments/tree/master/zookeeper_c_bindings_examples/config_center_services)有一个600多行代码的Demo，模拟新方案中几个角色：

DB – trigger_sim.py

应用节点 – app.c

ccs_agent – ccs_agent.c

模拟的步骤大致如下（单机版）：

a) 启动ZooKeeper

$> zkServer.sh start

JMX enabled by default

Using config: /home1/tonybai/.bin/zookeeper-3.4.5/bin/../conf/zoo.cfg

Starting zookeeper … STARTED

b) 启动ccs_agent

$> ccs_agent

This is [ccs-member0000000037], i am a leader

/ccs node exists

/ccs/employee_info_tab node exists

/ccs/boss_info_tab node exists

trigger listen thread start up!

item expire thread start up!

c) 启动app

d) 使用trigger_sim.py模拟DB触发trigger

$> trigger_sim.py employee_info_tab ADD 1234567

可以看到ccs_agent输出结果如下：

table[employee_info_tab], oper_type[ADD], id[1234567]

app的输出如下：

child event happened: type[4]

item-0000000015

employee_info_tab: execute [ADD 1234567]

大约30s后，ccs_agent会输出如下：

[expire]: employee_info_tab: expire [item-0000000015]

模拟步骤在README里有写。这里仅是Demo代码，存在硬编码以及异常处理考虑不全面的情况，不要拍砖哦。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

2篇zookeeper博文都很赞，

推荐一款开源轻量的配置管理中心：https://github.com/ihaolin/diablo