---
title: 升级Thunderbird
url: https://tonybai.com/2011/03/21/upgrade-thunderbird/
published: '2011-03-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 升级Thunderbird

自从[换装Ubuntu](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/)后，就一直使用[Thunderbird](http://tonybai.com/2009/11/20/cross-platform-configuration-of-thunderbird/)。很是喜欢Thunderbird超快的搜索速度、按主题组织和展示Mail以及易用的快捷键。不过这两天Thunderbird一直在给我制造麻烦。通过Top查看，我发现我的Thunderbird一直在持续占用20%-30%的CPU，这导致我的本子变得很慢。虽然能看到这个进程，但是并不清楚Thunderbird究竟在做什么。开始怀疑它在后台压缩文件夹，我遂显式对每个mail较多的文件夹进行了一次压缩。压缩后Thunderbird似乎安静了一会儿，不过好景不长，不久那个进程又开始运转起来了。我怀疑这是个Bug，于是有了升级Thunderbird的想法。

翻看了一下Thunderbird的菜单，发现它似乎不支持在线升级更新。我使用的版本是3.0.6，官方最新稳定版本为3.1.9。下载最新安装包后菜发现这个包不过就是一个压缩的文件夹，文件夹里有Thunderbird可执行程序和一切它依赖的资源文件。这样看来Thunderbird的升级实际上就是一个“替换”的过程。

“which thunderbird”的结果告诉我/usr/bin下的Thunderbird不过是一个符号链接，Thunderbird真正的安装目录在/usr/lib/thunderbird-3.0.6下面。这样就好办了，以下是升级替换步骤：

1. 将3.1.9安装包解压到/usr/lib下，改名为/usr/lib/thunderbird-3.1.9

2. 修改/usr/lib/thunderbird-3.1.9/thunderbird文件，将mod_libdir的值改为/usr/lib/thunderbird-3.1.9

3. 删除/usr/bin/thunderbird符号链接

4. 在/usr/bin下重新创建到新安装位置的符号链接：ln -s /usr/lib/thunderbird-3.1.9/thunderbird thunderbird

启动新thunderbird，一切ok。不过过了一会，cpu又上去了。看来这不是一个bug，Thunderbird确实是在后台在做着某些定期任务。还好今天Thunderbird启动后没有占用高CPU，也许是那个定时任务执行完毕了^_^。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论