---
title: 也谈SVN冲突解决
url: https://tonybai.com/2011/03/23/also-talk-about-solving-the-svn-conflicts/
published: '2011-03-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈SVN冲突解决

当今的软件开发更多是团队合作，团队的所有成员均工作在同一份代码库上。这样即便是有了先进的[版本控制](http://tonybai.com/2011/02/18/put-everything-under-version-control/)管理工具（诸如[Subversion](http://tonybai.com/2010/08/07/use-svn-pre-commit-hook/)、[Git](http://tonybai.com/2011/01/20/try-git-svn/)等），出现冲突（Conflict）的情况也是在所难免的。这就需要你学会解决冲突。

以Subversion为例，多数人在学习这类工具时都选择了浅尝辄止，仅仅停留在会使用update和commit这些常用的命令上。这样大家就错过了那些可以帮助你快速解决冲突的命令，以致很多人无论遇到任何冲突情况都采用了低效的全手工处理的方式。实际上不同的冲突情形处理的方式是有差别的。某些情况下，利用类似svn resolve这样的命令可以帮你快速解决冲突。我们应该有意识地采用一些专业的做法，不是吗？^_^

这里简单回顾一下版本冲突的产生过程：

- 版本库中存在一个代码源文件Foo.c，当前修订号：#BASE-REV；

- 甲、乙二人同时Checkout出文件Foo.c的最新版本#BASE-REV；

- 乙对其本地目录下的文件Foo.c进行了修改，并提交了代码，提交后文件Foo.c的修订号变为了#HEAD-REV；

- 由于缺乏沟通或沟通有误，在不知乙已经作出修改的情况下，甲也对其本地的文件Foo.c进行了修改；

- 当甲尝试将其本地目录下的Foo.c文件提交（commit)到代码库时，SVN给出错误提示：提交失败(细节如下): … …；或当甲尝试Update最新代码到其本地目录下时，发现SVN给出冲突提示："C Foo.c"或在 “Foo.c” 中发现冲突…。

Subversion 1.5版本之前不支持所谓的"交互式冲突解决(interactive conflict resolution)"，而1.5之后的版本则支持这种交互式的解决过程，即当冲突时，你会在控制台上看到的这样的提示：

在 “Foo.c” 中发现冲突。

选择: (p) 推迟，(df) 显示全部差异，(e) 编辑, (h) 使用帮助以得到更多选项:_

如果你选择p，或者你用的是低于1.5版本的Subversion，你在执行svn update后会在你的本地目录下得到如下几个文件：

Foo.c Foo.c.mine Foo.c.r#BASE-REV Foo.c.r#HEAD-REV

分别解释一下这几个文件：

Foo.c – 这个是由Subversion自动将版本库中的最新改动合并到你本地的一个包含了<<<>>>等标记的冲突文件；

Foo.c.mine – 这个是甲在执行svn update前自己修改的那份Foo.c文件；

Foo.c.r#BASE-REV – 这个文件的内容与修订号为#BASE-REV的Foo.c文件一致，也就是那份基（Base）文件；

Foo.c.r#HEAD-REV – 这个文件是乙修改后并提交的Foo.c文件，也是目前代码库中的HEAD revision。

那么甲如何来处理这个冲突呢？在不会使用svn resolve命令之前，甲很可能会这么做：打开Foo.c，逐个冲突进行解决。然后删除其余的三个Foo.c.xxx文件，最后提交代码。

这么做无可厚非，不过不是所有情况下都需要这么做的。我们将冲突情况进行一下分类：

1. 甲的代码完全包含了乙对Foo.c的修改，Foo.c.mine中的内容正是我们想要的;

2. 乙的代码完全包含了甲对Foo.c的修改，Foo.c.r#HEAD-REV中的内容正式我们想要的；

3. 甲、乙两人修改的代码确实存在不可融合之处，那么需要手工分析和解决Foo.c中的冲突。

下面我们用svn resolve命令分别处理上面三种情况：

针对情况1，甲可直接在自己的环境中执行svn resolve –accept mine-full Foo.c，执行后，冲突状态消失，甲可以从容地提交代码了；

针对情况2，甲可直接在自己的环境中执行svn resolve –accept theirs-full Foo.c，执行后，冲突状态消失，甲也可以从容地提交代码；

针对情况3，工具无法给予甲更有力的支持了，只能依靠甲自己去打开Foo.c并手工解决所有冲突了。待所有冲突解决后，执行svn resolve –accept working Foo.c或直接删除其它三个Foo.c.xxx文件，使冲突状态消失，Subversion这时将允许你提交你的代码。

有两点需要注意的是：

1. svn resolve命令只是在Subversion 1.5以及以后版本中才提供，在1.5版本前Subversion提供了一个resolved命令，不过这个命令似乎不是那么给力，基本上和你手工解决没啥差别，1.5以后这个resolved命令就被废弃了。

2. 对于第三种情况，一旦你删除了其余三个Foo.c.xxx文件，那svn就会认为你的冲突状态已经不存在了，这时即使你的Foo.c中依旧包含<<<>>>等冲突标记也是可以提交成功的，这里要小心对待。

另外对于情况3，如果甲并不想打开Foo.c手工解决冲突，而是想Undo自己的修改的话，那么甲可以通过执行svn resolve –accept base Foo.c或svn revert来将Foo.c恢复到#BASE-REV状态。接下来可以先update到乙的版本，然后再做出自己的修改。不过此前要做好代码的备份，否则一旦执行这些命令，甲之前所作的修改就会瞬间消失。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论