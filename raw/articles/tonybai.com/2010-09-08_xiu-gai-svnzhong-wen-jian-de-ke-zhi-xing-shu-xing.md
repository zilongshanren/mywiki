---
title: 修改SVN中文件的可执行属性
url: https://tonybai.com/2010/09/08/modify-the-executable-property-of-files-in-svn-repository/
published: '2010-09-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 修改SVN中文件的可执行属性

今天做了一些[项目版本库](http://tonybai.com/2010/08/26/also-talk-about-branch/)的搭建工作，主要是将相关模块和库目录建立好，将Makefile编写好，并添加到SVN库中。

工作接近尾声时，无意中发现提交到SVN库中的文件居然都带着可执行权限(以下称x属性)，如：

-rwxr-xr-x 1 tonybai tonybai 203 2010-04-21 17:26 Makefile*

这着实让人觉得别扭！Svn居然记录了文件的权限信息，至少我以前还没有关注过这点。

摆在面前有两件问题要搞清楚：

1、我在本地建立的文本文件为何带上了可执行的权限？

2、如何将SVN库中文件的可执行权限属性去掉？

我检查了一下我的[Ubuntu](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/) Shell设置，没有显式设置umask，但是在/etc/profile中[Bash](http://tonybai.com/2009/02/27/make-bash-my-default-shell/)默认设置了"umask 022"，这样我新建的文件应该具有-rw-r–r–的权限属性才对，为什么变成了-rwxr-xr-x了呢？ 回想了一下，Makefile是我从其他项目的本地代码目录下Copy过来的，难道这个项目的代码文件原本就携带了可执行权限吗？打开那个本地目录，ls -l查看了一下，果然所有文本文件都是带有x权限的。在这个目录下touch了一个新文件，居然也是携带x权限的！回到“主文件夹”，又尝试touch了一个文件，这个文件却不带有x权限！难道与分区有关系？那个项目的本地代码是放在Windows的FAT32分区下的，这个分区是在Ubuntu启动后通过点击分区磁盘符后才mount上的。这个问题我没有继续深挖，但原因八九不离十就是Ubuntu在挂接这些分区时传递并采用的umask的值与Bash默认配置的值不同。

事已至此，那如何“亡羊补牢”将SVN库中存储的文件的x属性去掉呢？ [SVN手册](http://svnbook.red-bean.com)给了我们一些线索！手册中谈到通过设置svn:executable可以保持文件的x属性，例如：如果想给SVN库中的某个文件加上x属性，可使用：

svn propset svn:executable on test.c

执行结果提示：设置属性 “svn:executable” 于 “test.c”

查看一下文件属性：

-rwxr-xr-x 1 tonybai tonybai 50 2010-09-08 15:44 test.c*

本地文件已经被加上了x属性，svn status查看一下，发现svn认为test.c已经发生了改变。svn commit后，test.c就会被加上executable属性，之后你无论在哪里checkout文件test.c，你都会发现test.c有着x权限。

如何删除x权限呢？没有细致查看手册之前，我猜想应该执行: "svn propset svn:executable off test.c"，结果svn给出提示:

svn: 警告: 使用 “svn propdel” 关闭属性 svn:executable；

设置属性为 “off” 不会关闭它。

svn提示我使用svn propdel，再查看一下手册，的确svn propdel是用于删除各种prop的正确命令，执行：svn propdel svn:executable test.c

提示：删除属性 “svn:executable” 于 “test.c”。

使用ls -l查看，test.c的x属性已经被删除，如果想删除svn server端的x属性，还需进行一次svn commit。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论