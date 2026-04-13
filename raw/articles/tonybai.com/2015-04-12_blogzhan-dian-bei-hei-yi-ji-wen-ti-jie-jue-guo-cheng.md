---
title: Blog站点被黑以及问题解决过程
url: https://tonybai.com/2015/04/12/fix-hacked-blog-site/
published: '2015-04-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Blog站点被黑以及问题解决过程

记得前些日子，我在Blog评论里发现有人说我的Blog站点被黑：

"YOUR SITE HAS BEEN HACKED – THERE ARE PARASITE PAGES IN http://tonybai.com/dl SECURE YOUR SITE!!!"

粗浅检查了一番，没有发现什么异常，也就没把这事当回事儿。

昨天上Gmail(由于需要搭梯子，不经常登录)，发现一位网友发来mail说我的站点被入侵了，还附上了google search结果的截图：

![](../../assets/2a8c3211d52aab53.jpg)


接着我也发现了google webmaster发来的mail，同样是警告我的博客站点被黑，并给出了两个可疑URL：

http://tonybai.com/dl

http://tonybai.com/dl/call-of-duty-4-modern-warfare-crack-download-tpb.html

我自己访问了一下上述URL，我靠！果然被黑了。

以前blog站点无论是搭建在dreamhost上还是朋友的主机上时都未出现过被黑的情况，这次在DO上居然被黑，之前没有解决类似问题的经验，这次只能从头摸索。

看了几篇解决wordpress被黑问题的文章，都推荐先安装几个安全插件对site进行扫描，于是我就试了两个：iThemes Security和Wordfence Security。前者似乎有问题，安装后，dashboard页一片空白。Wordfence Security还好，只是每次scan都无法finish，也就无法得到到底哪些wordpress文件被感染的结果。

插件不可靠，只能自己“手工”解决了。

首先到server上利用find , ls等命令对比时间，发现是否有哪些文件的最近访问时间戳与其他文件有差异。不过search了半天，也没发现半点痕迹。

网上还推荐用文件比对工具，比对现在的wordpress文件与backup的文件异同。多亏有backup插件的备份包，于是下载了20150326和20150409的backup zip，使用beyond compare进行目录比对。不比不知道，一比吓一跳啊：**index.php文件时间戳相同，但内容居然不同**。

0409中的index.php的头部居然多了一段代码：

<?php $V3a3xH8="JQAgHfEmQKV+JuR5Y38ZdWofSxp4PSPn00uzTC

….

….

($CdFxbnu0g($nGXNegRe($dvXZv9($cDjofDA))));?>

显然这就是入侵代码了。删除这段代码，重启apache2，试试再访问以下上述那两个URL。结果是令人悲伤的，页面居然还能正常打开和显示。我第一时间想到的是浏览器和apache2的缓存。

强制刷新brower，无用。

查找apache2关于Cache的配置，发现一个：/etc/apache2/mods-available/cache_disk.conf

其内容：

<IfModule mod_cache_disk.c>

# cache cleaning is done by htcacheclean, which can be configured in

# /etc/default/apache2

#

# For further information, see the comments in that file,

# /usr/share/doc/apache2/README.Debian, and the htcacheclean(8)

# man page.

# This path must be the same as the one in /etc/default/apache2

CacheRoot **/var/cache/apache2/mod_cache_disk**

# This will also cache local documents. It usually makes more sense to

# put this into the configuration for just one virtual host.

#CacheEnable disk /

# The result of CacheDirLevels * CacheDirLength must not be higher than

# 20. Moreover, pay attention on file system limits. Some file systems

# do not support more than a certain number of inodes and

# subdirectories (e.g. 32000 for ext3)

CacheDirLevels 2

CacheDirLength 1

</IfModule>

查看CacheRoot，发现/var/cache/apache2/mod_cache_disk下是空的。显然并未缓存。

难道还有其他位置为hacked了？难道0326的backup也是被hack过的？

于是我翻箱倒柜，在电脑里发现了20150101的backup，用这个Backup和0409又对比了一次，这回发现了另外一个被hack的文件：.htaccess。

.htaccess中多了这么一行代码：

RewriteRule ^dl/(.*)$ wp-add.php [L]

原来入侵的人或程序总共在我的主机上做了多处修改，这里总结一下：

1、.htaccess中增加一行规则

2、添加wp-add.php

3、修改了index.php

4、修改了wp-includes/theme-compat/header.php

5、修改了wp-content/themes/xx/header.php和footer.php

我ls了一下0409下的文件：

-rw-r–r– 1 tony staff 4343 11 28 04:01 wp-activate.php

**-rw-r–r– 1 tony staff 1991 11 28 04:01 wp-add.php**

drwxr-xr-x 89 tony staff 3026 4 9 11:00 wp-admin/

-rw-r–r– 1 tony staff 40243 11 28 04:01 wp-app.php

可以看出入侵代码在添加文件之后，对文件时间做了调整，让简单的时间戳对比无法揪出这个罪魁。

去除以上入侵代码后，上述可以网址就无法访问了。

在google webmaster提交request，期望google 早日将搜索结果中的"[此网站可能遭到黑客入侵](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0CC0QpwgwAQ&url=https%3A%2F%2Fsupport.google.com%2Fwebsearch%3Fp%3Dws_hacked&ei=7rgpVcXGMYXKmAXt5IHAAQ&usg=AFQjCNH1k7hr1cnoyVQ7hXq1P5Ozrgz7Zw&sig2=eCRkyr4PWwZI7yoAvn5iSw)"标签去掉。

之后将密码修改了一遍，希望后续能免疫。

后记：

根据朋友建议，将blog的文件用git管理起来，并push到bitbucket的private repository中，这样一旦再被hack，恢复起来也较为方便。

步骤如下：

1、在/var/www目录下git init

2、git add ./

3、git commit -m”initial import” ./

4、git remote add origin https://user@bitbucket.org/user/blog.git

5、git push origin master

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

用干净的代码做份git仓库吧，这样被黑之后比较起来就很方便了。

好主意。