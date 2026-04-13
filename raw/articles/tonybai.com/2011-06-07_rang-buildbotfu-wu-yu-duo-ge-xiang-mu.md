---
title: 让BuildBot服务于多个项目
url: https://tonybai.com/2011/06/07/use-buildbot-serves-serveral-projects-simultaneously/
published: '2011-06-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 让BuildBot服务于多个项目

多数公司不会仅有一个项目，当你为一个项目引入持续集成实践后，其他项目就会接踵而来。这时你会重新考量[BuildBot](http://tonybai.com/2011/05/18/set-up-ci-environment-with-buildbot/)，考虑如何让BuildBot可以服务于多个项目。

如果你有足够的主机资源和人力资源，那为每个项目单独搭建一套CI环境是再好不过的了，每个项目都有专人维护CI环境，各个项目的配置互不干扰。不过对于一些公司来说，这显然有些浪费，BuildBot Master的资源消耗是不大的，我们完全可以使用一套BuildBot Master来服务于多个项目，至少BuildBot是可以支持这样做的。

CI环境中，我们首要关注的就是源码库。多个项目可能各自使用单独的源码库，也可能共享一个源码库并通过目录隔离和识别。无论怎样，我们都可以通过BuildBot Master的配置来满足我们的要求。

如果说多个项目共享一个源码库或是一个项目下的多个子系统放在一个源码库中，这时我们在配置change_source时指定一个变更监测器即可，这个监测器的监测范围从源码库的根路径开始。以Subversion源码库为例，我们可以这样来配置：

c['change_source'] = [SVNPoller("svn://10.0.0.1:3000",

svnuser='tony',

svnpasswd='tony',

pollinterval=60,

split_file=change_path_split)]

我们通过change_path_split来拆分变更文件的路径，假设SVN库结构是这样的：

svn://10.0.0.1:3000

– foo_proj

– trunk

– main/main.c

– branches

– tags

– bar_proj

– trunk

– main/main.c

– branches

– tags

我们可以这样来实现change_path_split：

def change_path_split(path):

pieces = path.split('/')

if pieces[0] == ‘foo_proj’ and pieces[1] == 'trunk':

return ('foo_proj/trunk', '/'.join(pieces[2:]))

elif pieces[0] == ‘bar_proj’ and pieces[1] == 'trunk':

return ('bar_proj/trunk', '/'.join(pieces[2:]))

else:

return None

不同项目下的文件变更，会导致change_path_split返回不同的值，而change_path_split返回值会被用于匹配不同的Scheduler：

c['schedulers'].append(Scheduler(name="foo-ci-plan",

branch='foo_proj/trunk',

treeStableTimer=5,

builderNames=["foo-redhat-builder", "foo-x86-solaris-builder"])

c['schedulers'].append(Scheduler(name="bar-ci-plan",

branch='bar_proj/trunk',

treeStableTimer=5,

builderNames=["bar-redhat-builder", "bar-x86-solaris-builder"])

上面各个Scheduler的branch属性会与change_path_split返回值元组中的第一个元素匹配，这样foo-ci-plan便是foo_proj的scheduler，而bar-ci-plan则是bar_proj的scheduler。这样某个项目路径下的文件变更只会触发对应的scheduler开始工作，不会出现误触发。

如果多个项目或一个项目的多个模块使用不同的源码库，同理，我们可以为c['change_source']赋予多个SVNPoller，例如：

c['change_source'] = [SVNPoller("svn://10.0.0.1:3000",

svnuser='tony',

svnpasswd='tony',

pollinterval=60,

split_file=change_path_split)，

SVNPoller("svn://10.0.0.1:4000",

svnuser='tony',

svnpasswd='tony',

pollinterval=60,

split_file=another_change_path_split)]

与Scheduler的匹配方式也与上述描述一致，这里就不重复说明了。

不同项目的干系人多不相同，那么集成的结果是如何准确地反馈给项目各自对应的干系人呢？以[Mail反馈通知](http://tonybai.com/2011/05/31/solve-the-problem-that-buildbot-can-not-send-mail/)为例，我在BuildBot手册中找到了两种方式，一种方式是通过设置Scheduler的owner属性，然后指定MailNotifier的sendToInterestedUsers=True，意图让BuildBot将Mail通知发到owner list中的每个邮件地址，但经测试后发现，这种方式似乎不好用，不知道是否是BuildBot对该功能的实现上存在问题。

另外一种方式则是配置多个MailNotifier。每个MailNotifier中指定对应builder的名称列表，并通过extraRecipients指定这些Builder对应的项目的干系人Mail地址列表，例如：

c['status'].append(mail.MailNotifier(fromaddr="[foo-buildbot@buildbot.net](mailto:foo-buildbot@buildbot.net)",

extraRecipients=["[foo1@buildbot.net](mailto:foo1@buildbot.net)", "[foo2@buildbot.net](mailto:foo2@buildbot.net)"],

builders=['foo-x86-solaris-builder', 'foo-redhat-builder'],

useTls=False,

sendToInterestedUsers=False,

relayhost="smtp.buildbot.net",

smtpUser='tony',

smtpPassword='tony',

smtpPort=25))

c['status'].append(mail.MailNotifier(fromaddr="[bar-buildbot@buildbot.net](mailto:bar-buildbot@buildbot.net)",

extraRecipients=["[bar1@buildbot.net](mailto:bar1@buildbot.net)", "[bar2@buildbot.net](mailto:bar2@buildbot.net)"],

builders=['bar-x86-solaris-builder', 'bar-redhat-builder'],

useTls=False,

sendToInterestedUsers=False,

relayhost="smtp.buildbot.net",

smtpUser='tony',

smtpPassword='tony',

smtpPort=25))

这样foo的builders构建的结果将发到foo1和foo2；而bar的builders构建结果将反馈到bar1和bar2。

多个项目共享一套BuildBot Master有利有弊，其不足之处可能有如下几点：

1、项目过多时，可能存在潜在的性能问题

2、Master的配置被多个项目共享，存在潜在的Conflict问题；

3、另外master.cfg可能size过大，也不利于阅读和维护。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论