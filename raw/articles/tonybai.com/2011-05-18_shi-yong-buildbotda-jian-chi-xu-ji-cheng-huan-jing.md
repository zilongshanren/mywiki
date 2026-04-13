---
title: 使用BuildBot搭建持续集成环境
url: https://tonybai.com/2011/05/18/set-up-ci-environment-with-buildbot/
published: '2011-05-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用BuildBot搭建持续集成环境

部门的[持续集成](http://book.douban.com/subject/2580604/)一直做的不太好，我们开发部这边甚至一直没能做起来，这其中有各种原因：工具、意识、执行力、沟通等等。将持续集成引入到我们的开发过程中也一直是我的一个目标。去年末启动的一个项目让我感到时机变得成熟了。

新项目的代码是完全重写的，这样的机会甚是难得。因为大多数情况下大家都是在维护现有系统：做些添添补补、修正Bug以及优化之类的事情。项目初期，我特别向大家强调了要严格遵守统一代码风格并将[astyle](http://http://tonybai.com/2010/07/29/use-astyle-to-beautify-your-code/)代码格式化工具介绍给大家，手把手地教大家如何利用类似[LCUT](http://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/)这样的[单元测试框架](http://tonybai.com/2005/11/08/the-design-and-implementation-of-c-unittest-framework/)编写单元测试，讲解什么是[Mock测试](http://tonybai.com/2008/04/12/mock-test-in-c-unit-test/)。前些时间我又将[代码风格检查](http://tonybai.com/2011/04/21/apply-style-check-to-c-code/)

脚本加入到工程的构建过程中，并将代码风格检查作为最终构建目标的关键依赖，强制大家编写出统一风格的代码。

情况就是这样的情况，的确我们现在只做到了这些。不过有了这些基础，我就更有信心去做持续集成了。

今年年初部门统一部署了产品的多平台移植的开发任务，作为新项目，我们的成果物被要求天生就应具备适合在多个平台上运行的能力。这次产品平台移植仿佛一针催化剂加快了我在项目中实施持续集成的脚步。我希望搭建出这样一套系统：每当开发人员提交代码后，持续集成框架都能发现这些代码变动，并在多个不同平台的主机上分别Checkout出最新代码，Build，Check代码风格并运行单元测试集，最终将结果通知所有人。

我需要找到满足我这一需求的工具。记得若干年前我第一次研究持续集成时曾经研究过一款名为[CruiseControl.rb](http://tonybai.com/2008/08/20/the-experience-of-cruisecontrol-rb/)的工具，不过很遗憾的是这款工具似乎早已不更新了。在[Thoughtworks的官方站点](http://cruisecontrolrb.thoughtworks.com)上，其最后一次发布是在2年前了。另外CruiseControl.rb一个比较大的缺憾就是性能差些。另外如果想满足我在多个不同平台主机上同时运行构建以及测试的要求，似乎需要部署多套CruiseControl.rb。

在寻找工具的路上，我发现了[BuildBot](http://trac.buildbot.net/)。这是一款由Python实现的开源持续集成工具。与CruiseControl.rb相比，其性能更好，其Master+Slaves的结构更易于扩展，并且可以很好地满足多平台版本构建的需求，大名鼎鼎的Google Chrome浏览器项目用的也是这款工具。另外我个人对Python的更加青睐也让我决定使用这款工具。

BuildBot的文档比较丰富和全面，这也使其安装过程比较简单。BuildBot由两部分组成，一部分是Master，用于监视代码库变动，控制各个Slave节点进行构建操作，并收集反馈结果以各种方式（Mail、Html等）展示给用户；另外一部分就是Slave了。每个Slave节点都承担着构建过程的具体工作：他们接收Master发过来的指令，并按指令一步一步完成构建工作，并将结果反馈给Master。

一个BuildBot持续集成环境就是由一个Master与一些Slaves组成的。其安装过程大致如下：

1、在装有Python（最好是Python 2.6.x版本）的Master主机上安装Buildbot master：下载BuildBot安装包（我用的是最新的[BuildBot-0.8.3p1](http://buildbot.googlecode.com/files/buildbot-0.8.3p1.zip)）。解包后，执行python setup.py build和python setup.py install安装BuildBot master包。注意install默认是需要root权限的。

2、安装BuildBot依赖包：下载最新的Twisted包（我用的是11.0.0）与zope.interface包（我用的是3.6.1），安装方法与BuildBot一致。

3、在装有Python（最好是Python 2.6.x版本）的各个Slave主机上安装BuildBot slave：下载[Buildslave](http://buildbot.googlecode.com/files/buildbot-slave-0.8.3.zip)安装包、最新的Twisted包与zope.interface包，安装方法与BuildBot Master一致。

4、以上安装完成后，在Master host上执行buildbot，在各Slave host上运行buildslave，检查一下是否成功安装了。

安装Ok，我们就可以建立Master实例以及诸多Slave的实例了。先说说Master。在Master主机上某路径下，创建foo_ci_master目录，进入foo_ci_master目录下，执行："buildbot create-master ./"。执行后，在当前目录下会有master.cfg.sample文件。这是一个样板文件，我们将其改名为master.cfg后，打开master.cfg，开始进行master的配置。

Master的master.cfg是这套持续集成系统的核心。我们用一个简单的例子来说明这个配置。假设我们的持续集成环境由三台主机组成：Master Host（假设其ip为10.0.0.1）以及两台Slave Host，其中一台Slave Host上运行着RHEL 5.5，而另外一台Slave Host上则运行着PC Solaris 10。我们希望当有代码被提交到代码库中后，Master可及时发现这一变化，并且指挥两台Slave Host检出最新代码并且都能Build成功。

下面是master.cfg中的一些关键配置及说明(省略了一些默认配置)：

#

# master.cfg

#

c['slaves'] = [BuildSlave("x86-solaris-bot", "x86-solaris-bot-passwd"),

BuildSlave("redhat-bot", "redhat-bot-passwd")]

这里告诉Master我们有两个Slave node，分别是x86-solaris-bot和redhat-bot，而这两个Slave登录Master的密码分别为x86-solaris-bot-passwd和redhat-bot-passwd。

我们使用[subversion](http://tonybai.com/2011/03/23/also-talk-about-solving-the-svn-conflicts/)作为我们源码版本管理工具，所以我们采用SVNPoller来监测源码库的变化：

from buildbot.changes.svnpoller import SVNPoller

c['change_source'] = SVNPoller("svn://10.10.0.1:8888",

svnuser='YOUR_SVN_USER',

svnpasswd='YOUR_SVN_PASSWD',

pollinterval=30,

split_file=foo_split_file)

def foo_split_file(path):

pieces = path.split('/')

if pieces[0] == ‘foo’ and pieces[1] == 'trunk':

return ('foo/trunk', '/'.join(pieces[2:]))

else:

return None

在SVNPoller的参数中split_file是比较难理解的一个。它是为下面的Scheduler提供服务的。split_file会将变更的源码文件的完整路径信息进行拆分，并返回一个(branch, relative_pathname)的元组。而Scheduler将尝试匹配元组中的branch以决定此次变更是否是自己所关心的。看下面配置代码：

c['schedulers'].append(Scheduler(name="foo-ci-plan",

branch='foo/trunk',

treeStableTimer=5,

builderNames=["foo-redhat-builder", "foo-x86-solaris-builder"]))

显然这个Scheduler关心"foo/trunk"这个branch。一旦某源码文件归属于该分支（如svn://10.10.0.1:8888/foo/trunk/main/main.c），则该Scheduler会启动构建过程。其构建过程将通过两个builder完成，它们分别是foo-redhat-builder和foo-x86-solaris-builder。这样一来，我们就可以适当定义foo_split_file并设置多个Scheduler，以满足我们对不同branch的不同构建需要。

builder都是关联到某个builder factory的，而下面则是factory的配置：

foo_builder_factory = factory.BuildFactory()

foo_builder_factory.addStep(SVN(mode='update',

baseURL='svn://10.10.0.1:8888/',

defaultBranch='foo/trunk'))

foo_builder_factory.addStep(Compile(command=["make"]))

这个factory生产出来的builder会执行两个step：首先执行svn update，将svn://10.10.0.1:8888/foo/trunk更新到本地；然后执行make命令。

下面是builder的设置：

b1 = {'name': "foo-redhat-builder",

'slavename': "redhat-bot",

'builddir': "foo-redhat",

'factory': foo_builder_factory,

}

b2 = {'name': "foo-x86-solaris-builder",

'slavename': "x86-solaris-bot",

'builddir': "foo-x86-solaris",

'factory': foo_builder_factory,

}

c['builders'] = [b1, b2]

builder的设置看起来没那么难，一目了然。

BuildBot Slave的创建和配置就更加简单了。首先到那台运行着solaris系统的Slave host上，在适当目录下创建foo_ci_slave目录，进入该目录后，执行“buildslave create-slave –umask=022 ./ 10.0.0.1:9989 x86-solaris-bot x86-solaris-bot-passwd”命令，一个Slave就创建完了，实际上也配置完了，无需额外配置了。其配置文件就是foo_ci_slave下面的buildbot.tac文件。Rhel上的slave也是如此创建的。

启动Master。在Master host的foo_ci_master下面，执行buildbot start ./即可启动buildbot master，其当前日志会被输出到twistd.log中；如果要停止buildbot master，依旧是在该目录下，但执行buildbot stop ./。

启动slave。在Slave Host的foo_ci_slave下面，执行buildslave start ./即可启动buildbot slave，其当前日志会被输出到twistd.log中；如果要停止buildbot slave，依旧是在该目录下，但执行buildslave stop ./。

当Master和各个Slave都成功启动后，我们就可以来试试执行一次Build过程：修改foo/trunk下的某源码文件并提交。Master将会侦听到变更，便会启动两个Slave Host上的build过程。此次构建的结果在哪里可以看到呢？试试访问http://10.0.0.1:8010，页面上红色代表构建失败，绿色代表构建成功。

Buildbot还支持将构建结果通过Mail通知的机制，不过由于公司用的是ssl方式，我试验了许久都没能将mail发出来。不知道是不是Twisted的Mail包的实现有问题还是其他什么原因，后续会继续查证。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论