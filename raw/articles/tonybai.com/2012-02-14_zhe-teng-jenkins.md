---
title: 折腾Jenkins
url: https://tonybai.com/2012/02/14/install-and-configure-jenkins/
published: '2012-02-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 折腾Jenkins

[Buildbot](http://tonybai.com/2011/05/18/set-up-ci-environment-with-buildbot/)是产品线C应用项目中采用的唯一持续集成工具，一直以来用得还不错。但前些日子部门负责过程改善的同事找到我，说今年部门计划统一各个项目组所使用的[Continuous Integration](http://en.wikipedia.org/wiki/Continuous_integration)工具，Buildbot有些小众，没有入大家的法眼，部门期望使用的是[Jenkins](http://jenkins-ci.org/)(即原来的Hudson)。既然组织有统一规划，那我自然积极支持。但首先要做的就是评估Jenkins是否能满足我们的需求，并且看看从Buildbot迁移到Jenkins的难度及工作量有多少。这不，今天下午就一直在折腾Jenkins。

一、安装Jenkins

Jenkins(前身Hudson)很流行，在各大主流操作系统平台上都有很好的支持，其安装甚是方便，特别是在各主流的Linux发行版平台上，均可使用OS自带的应用包管理工具进行自动安装；当然你也可以直接在官方下载war包。我采用的就是第二种方式，旨在获得更高的Jenkins版本，不过让我失望的是在Ubuntu 9.04(Java version: 1.6.0_20)上，最新的1.451和1.450版本均启动失败，这也是我之前不太喜欢使用Java实现的工具的一个原因之一 – 总是容易出现莫名其妙的异常，而且较难找到原因，也很难fix，除非自己重新构建war包。在这方面像Python等动态脚本语言就有先天优势，一旦出现问题，我可以直接在源码中定位和修改。

1.441版本的Jenkins让我看到了希望，至少启动是没有问题的。启动是通过下面命令行完成的：

java -jar jenkins.war –logfile=~/.jenkins/jenkins.log –daemon –httpPort=9333

如果你是使用包管理工具自动安装的Jenkins，那么Jenkins将被作为服务安装到指定位置(比如：/etc/default/jenkins)，并且在/etc/init.d下面创建了jenkins的init脚本。这样当主机重启后，Jenkins会被自动拉起。但如果你和我一样是手工下载的war包，那你就需要自己来保证Jenkins服务一直可用了。这里的一个简单的方法就是编写一个Jenkins运行的监控脚本，如果发现Jenkins未启动，就启动它，Jenkins_monitor.sh示例如下：

#! /bin/bash

result=`ps -ef|sed '/grep/d'|grep jenkins.war`

if [[ x$result == x ]];

then

cd '/home/tonybai/proj/jenkins' && java -jar jenkins.war –logfile=/home/tonybai/.jenkins/jenkins.log –daemon –httpPort=9333

else

echo "jenkins is alive!"

fi

最后将Jenkins_monitor.sh加到crontab中即可：

$> crontab -l

# m h dom mon dow command

* * * * * bash /home/tonybai/proj/script/jenkins_monitor.sh

二、配置Jenkins

Jenkins的配置是完全通过Web页面完成的，这点全面超越了Buildbot。关于Jenkins如何配置，网上的资料可谓是汗牛充栋，这里就不再重复了，这里只说说配置过程中遇到的一些问题以及解决方法。

我们的产品需要进行多平台上并行持续集成，也就是说当trunk上有代码commit后，Jenkins应该发现代码变更，并同时通知多个不同Slave平台进行集成。之前的Buildbot是通过手工在不同平台上部署Buildslave满足这一需求的，Jenkins也是支持Master/Slave模式的，但Jenkins比Buildbot更加平易近人的地方在于Slave节点无需手工到主机上安装，只需通过在Web页面上添加Slave Node即可（实际上Jenkins在Slave Node上启动了一个Java程序"slave.jar"）。

在配置Slave node时，我遇到了第一个问题：一个x86 Solaris平台的Slave node配置完后始终无法Online，而之前配置相同的一个x86 linux Slave节点却可以顺利Online。

直到查看Log后，我才弄清楚真正的缘由。下面是Jenkins Master通过ssh连接Slave Node的Log节选：

SSH connection reports a garbage before a command execution.

Check your .bashrc, .profile, and so on to make sure it is quiet.

The received junk text is as follows:

######################

Application Server

On Solaris 10

######################

hudson.AbortException

at hudson.plugins.sshslaves.SSHLauncher.verifyNoHeaderJunk(SSHLauncher.java:364)

… …

[02/14/12 14:03:23] [SSH] Connection closed.

原来问题出在我在Slave Node节点的.bashrc中增加的那段个性化签名。Jenkins无法识别这段签名，从而抛出异常，导致Connect失败。注释掉这段签名后就可以看到Slave Node的状态为Online了。

另外一个问题是有关Mail的配置的。公司的Mail Server年前做了一次升级，将安全连接方式由原先的SSL改为了STARTTLS，而Jenkins只支持SSL。没有mail通知的CI Server显然是不合格的。为此，我再次想起了当时[Buildbot的Mail发送解决方案](http://tonybai.com/2011/05/31/solve-the-problem-that-buildbot-can-not-send-mail/)- 使用[Stunnel](http://www.stunnel.org)。原先的Stunnel配置因公司Mail Server升级而失效了，所以需要对Stunnel做一些配置调整：

这个配置调整着实花了我一些时间，也走了一些弯路，最后在反复阅读[Stunnel配置手册](http://www.stunnel.org/static/stunnel.html)后，才发现让Stunnel在Client Mode下支持STARTTLS，只需要做一项配置修改，即增加"protocol = smtp"这一行，示例如下：

/* /etc/stunnel/stunnel.conf */

client = yes

… …

[smtp]

accept = host_ip : listen_port

connect = mailserver_ip : mailserver_port

protocol = smtp

这样Jenkins就可以用普通smtp连接方式(非SSL)通过stunnel与公司Mail Server进行数据交互了。

三、创建Job并执行集成

有了Node(没有也行，在Master上也可以执行集成)，我们就可以创建Job进行集成了。Jenkins Job的创建和配置也比较简单，这里同样不赘述了。我们的项目有了[buildc](http://tonybai.com/2011/12/08/buildc-a-building-assistant-tool-for-c-app/)这样的工具作为铺垫后，其构建脚本就变得相当简单了。在Job的execute shell中填写几行命令即可：

buildc config-make

make check-style

make compile-tests

make run-tests

make

对于[setup工程](http://tonybai.com/2012/02/10/add-packing-feature-to-buildc/)来说，由于buildc的存在，我们也可以通过执行buildc pack build完成构建，甚至是上传安装包到指定位置。所以在折腾Jenkins的同时，我也在考虑是否可以利用Jenkins搭建一套安装包制作和发布系统呢！

四、其他

Jenkins还有一点要优于Buildbot，那就是Jenkins拥有Buildbot所没有的"立即构建(Build Now)"功能(经提醒，buildbot也支持force build功能，只不过需要在master配置中这样来配置：c['status'].append(html.WebStatus(http_port=8011, allowForce=True)))，对于我来说，这个功能在调试CI脚本时尤其有用。另外，市面上有关Jenkins的书籍并不多，《[Jenkins: The Definitive Guide](http://book.douban.com/subject/6434790/)》算是目前市面上讲解Jenkins最为系统和全面的一本了，目前它也在我的"在读"列表中。

从目前的实验结果来看，Jenkins替代Buildbot是完全可行的，而且迁移难度和工作量也没有太多。由于接触Jenkins时间尚短，其强大的功能还需待日后进一步挖掘。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

Buildbot对每个builder都有一个force build按钮，这个和Jenkins的Build Now功能有什么不同呢？

以前没有发现这个功能。经你的提醒，又翻阅了一下manual，看到的确可以force build，但用起来似乎还没有jenkins那么容易。我的版本是0.8.3p1。

你好，请问下，现在项目组要配置一个ci环境，我改选用buildbot还是jenkins呢？谢谢

jenkins更成熟，插件多，支持广泛，资料更多，我们现在都在用jenkins。