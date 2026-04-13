---
title: 解决BuildBot构建结果mail无法发送的问题
url: https://tonybai.com/2011/05/31/solve-the-problem-that-buildbot-can-not-send-mail/
published: '2011-05-31'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 解决BuildBot构建结果mail无法发送的问题

在“[使用BuildBot搭建持续集成环境](http://tonybai.com/2011/05/18/set-up-ci-environment-with-buildbot/)”一文中我曾经说到：公司使用的mail服务器只支持SSL连接，而BuildBot似乎对SSL连接的支持有些问题，导致构建结果mail无法发送“。BuildBot实际上使用的是Twisted的mail库来发送邮件的，我下载了Twisted的一些mail发送的例子程序，并使用我的公司mail账户配置，但依旧发送失败。看来这个问题与Twisted的实现有关了。

这个问题已经折腾我许久了，难道非得让我去debug Twisted库？还好，今天我想到了另外一种方法：使用[stunnel](http://www.stunnel.org)。原理是这样的：通过stunnel将非SSL连接转换为到公司mail服务器的SSL连接，通过stunnel建立的这条转化通道，mail发送的问题就应该可以解决了。想法归想法，实际上能否达到我的目标，还得通过试验验证。

首先我们需要在BuildBot的master服务器上安装stunnel。

在[Ubuntu](http://tonybai.com/2011/04/29/feel-experience-after-using-ubuntu-for-one-year/)服务器上安装stunnel很简单，执行sudo apt-get install stunnel即可。不过今天我却遇到了问题，我的Ubuntu服务器版本是9.04，执行install时发现似乎所有源都不可用了。执行了多次还是这样，sudo apt-get update也无法更新了。突然想到也许是9.04的支持年限到了，到网上一查，果不其然：去年10月份Ubuntu 9.04就不在支持范围了。难道没有专门for老旧Ubuntu版本的源可以使用了吗？还好Ubuntu中文论坛上有答案：Ubuntu官方有一个源[http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu)是专为已经过了支持期限的版本服务的。将/etc/apt/sources.list备份后打开，将下面内容贴到该文件中：

deb [http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu) jaunty main restricted universe multiverse

deb [http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu) jaunty-security main restricted universe multiverse

deb [http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu) jaunty-updates main restricted universe multiverse

deb [http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu) jaunty-backports main restricted universe multiverse

deb [http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu) jaunty-proposed main restricted universe multiverse

deb-src [http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu) jaunty main restricted universe multiverse

deb-src [http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu) jaunty-security main restricted universe multiverse

deb-src [http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu) jaunty-updates main restricted universe multiverse

deb-src [http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu) jaunty-backports main restricted universe multiverse

deb-src [http://old-releases.ubuntu.com/ubuntu](http://old-releases.ubuntu.com/ubuntu) jaunty-proposed main restricted universe multiverse

保存后执行update，然后再重新install stunnel，这回一切OK了。

接下来，我们来配置stunnel。

我们先打开/etc/default/stunnel4，将其中的ENABLED配置项的值从0改为1，这样我们就允许stunnel在主机重启后可以被自动启动。

/etc/stunnel/stunnel.conf这个配置文件才是我们需要重点关注的。主要改动的配置项及说明如下：

; Use it for client mode

client = yes ; 我们使用的是stunnel的client模式，所以这里将no改为yes

; cert = /etc/stunnel/mail.pem ; 注释掉该行

; 打开debug模式以及log文件输出，便于我们在使用初期问题的查找

debug = 7

output = /var/log/stunnel4/stunnel.log

; 下面是关键配置，stunnel将接收本地到25端口的mail连接，并将该mail连接转换为到smtp.your_domain.com:465的SSL连接

[ssmtp]

accept = 127.0.0.1:25

connect = smtp.your_domain.com:465

配置就是这些了。我们通过sudo /etc/init.d/stunnel4 start启动stunnel。如果你在启动时遇到问题，别忘了查看一下/var/log/stunnel4/stunnel.log中的内容，多数情况下你都会很快的发现问题所在。比如我第一次启动stunnel时就得到了如下错误信息：

[Failed: /etc/stunnel/stunnel.conf]

You should check that you have specified the pid= in you configuration file

这个错误信息可能会让你误以为是配置出现了错误，但通过查看log会发现，原来错误原因是25端口已经被占用了。占用25端口的程序是sendmail，停掉sendmail服务，再次启动stunnel，我们得到以下的成功信息：

Starting SSL tunnels: [Started: /etc/stunnel/stunnel.conf] stunnel.

最后，我们来测试一下stunnel是否可以真正解决我们的问题。修改BuildBot master的master.cfg中的mail发送配置：

c['status'].append(mail.MailNotifier(fromaddr="SENDER_MAIL_ADDR",

extraRecipients=["RECIPIENT_MAIL_ADDR"],

sendToInterestedUsers=False,

useTls=False,

relayhost="127.0.0.1",

smtpUser='foo',

smtpPassword='foo!',

smtpPort=25))

有了stunnel，我们就可以使用非SSL连接来发送mail了，不过我们的buildbot连的是stunnel监听的本机25端口。

触发一次构建，稍等片刻，我的Thunderbird里就出现了BuildBot构建失败的提醒mail，我们成功了。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

你好，我也遇到mail无法发送的情况，我参照你这篇文章的方法还是没有解决。buildbot启动的时候有一条异常的log：

unable to import dnotify, so Maildir will use polling instead

我机器是gentoo系统，已经安装了sys-apps/dnotify，是不是master.cfg还需要对应的配置？

希望能够得到你的指导，非常感谢