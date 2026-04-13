---
title: SVN命令输出结果的语言选择
url: https://tonybai.com/2013/03/15/choose-lang-for-svn-cmd-output/
published: '2013-03-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# SVN命令输出结果的语言选择

今天一位网上的朋友在使用[reviewboard](http://tonybai.com/2009/09/19/review-board-installation-and-configuration/)时遇到了问题，我们在评论中探讨了一下。他的问题目前已经定位，大致是这样的：他在Windows上用svn diff生成的patch文件在提交给[reviewboard](http://www.reviewboard.org)时出错，但在linux上生成的patch文件是没有问题的。后来他发现这两个patch文件内容稍有区别：Windows上的patch文件中的diff结果包含中文，比如“版本 10”；而在linux下生成的那份patch文件中，"版本 10"变成了"revision 10"。reviewboard拒绝了带中文的那份patch，估计是reviewboard的字符编码设置让其无法识别windows下的那个字符集。

多数情况下，我们根本无需关心svn命令输出中到底是英文还是中文。[subversion](http://tonybai.com/2011/03/23/also-talk-about-solving-the-svn-conflicts/)对国际化支持到很好，它会根据自己所在环境下的区域和语言设置来选择到底输出哪种文字，对不同地区说不同语言的程序员来说，这绝对是一个好事。

但问题毕竟是出现了。我们该如何解决呢？我们该如何选择svn输出的语言呢？我不用Windows，所以这里我说说Linux下的设置方法，这也是今天在思考那位朋友的问题时才找到的方法。

方法的关键就在于前面说过的Subversion会自动检测你的区域和语言环境设置。以我的[Ubuntu 12.04LTS](http://tonybai.com/2012/12/04/upgrade-ubuntu-to-1204-lts/)为例，执行locale命令，可以看到以下输出：

LANG=zh_CN.UTF-8

LANGUAGE=zh_CN:zh

LC_CTYPE="zh_CN.UTF-8"

LC_NUMERIC="zh_CN.UTF-8"

LC_TIME="zh_CN.UTF-8"

LC_COLLATE="zh_CN.UTF-8"

LC_MONETARY="zh_CN.UTF-8"

LC_MESSAGES="zh_CN.UTF-8"

LC_PAPER="zh_CN.UTF-8"

LC_NAME="zh_CN.UTF-8"

LC_ADDRESS="zh_CN.UTF-8"

LC_TELEPHONE="zh_CN.UTF-8"

LC_MEASUREMENT="zh_CN.UTF-8"

LC_IDENTIFICATION="zh_CN.UTF-8"

LC_ALL=

也就是说默认情况下，我的区域是CN，语言是zh。在这种环境下svn命令的输出都是包含中文的，比如下面这段输出：

路径: .

URL: https://lcut.googlecode.com/svn/trunk

版本库根: https://lcut.googlecode.com/svn

版本库 UUID: 22405a7c-d843-be82-cc3b-46f1d7cb9705

版本: 57

节点种类: 目录

调度: 正常

最后修改的作者: bigwhite.cn@gmail.com

最后修改的版本: 57

我尝试修改locale。先将LC_ALL修改为en_US.UTF-8（通过locale -a你可以查看系统支持的locale列表，从中能看到en_US.utf8）。修改后(export LC_ALL=en_US.utf8)，执行locale，发现除了LANGUAGE和LANG还是原值外，其余变量都已经改为en_US.utf8了。不过svn info的输出结果依旧包含中文。

看来LANGUAGE或LANG两个变量中的一个会影响到svn的输出结果。先修改LANG为en_US.utf8，执行svn info，发现结果依旧包含中文。再试试修改LANGUAGE，export LANGUAGE=en_US.en（注意不是en_US.utf8，LANGUAGE变量的值与其他的变量稍有不同）。再执行svn info，这回终于等到英文结果输出了：

Path: .

URL: https://lcut.googlecode.com/svn/trunk

Repository Root: https://lcut.googlecode.com/svn

Repository UUID: 22405a7c-d843-be82-cc3b-46f1d7cb9705

Revision: 57

Node Kind: directory

Schedule: normal

Last Changed Author: bigwhite.cn@gmail.com

Last Changed Rev: 57

目前还不清楚这招在Windows下是否也生效，记得Windows上也有设置环境变量的地方。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论