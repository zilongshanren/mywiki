---
title: 尝试博客搬家
url: https://tonybai.com/2010/11/30/try-to-move-blog/
published: '2010-11-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 尝试博客搬家

早在若干年前就有朋友建议我搭建一个独立博客，可当时的我觉得[blogbus](http://www.blogbus.com)提供的服务很不错，自己没有必要去折腾，费钱又费力，所以我选择了继续留在blogbus。

这两年blogbus服务一直在不断的提高，自己也一直很欣赏blogbus的简单、清新、无广告的风格，大巴后台管理中心的功能也变得越来越强大了。不过这期间blogbus也出现过几次较为严重的故障，导致长时间的无法提供服务。上周blogbus再次出现文件服务器故障，导致上传的图片不能正常显示。这次我做了另外一个选择：尝试搬家。之所以称为“尝试搬家”，是因为搬家可能成功，也可能失败。

上周末经朋友推荐，我购买了[dreamhost](http://www.dreamhost.com)的主机空间，注册了[独立域名](http://tonybai.com)，并花了周末两天的时间搭起了一个[wordpress](http://www.wordpress.com)博客，这个过程是一波三折，还好我的[这位朋友](http://www.wuwx.net)是建站方面的高手，经他指点，我少走了许多弯路。但博客搬家最难的地方不是建站，而是后续数据的迁移和整理。

搬家过程大致如下：

1、创建mysql数据库；

2、安装wordpress；

3、从blogbus后台管理中心将数据导出，导出一个blogbus自定义格式的xml文件;

4、下载[bus2wp.py](http://code.google.com/p/bus2wp)；

5、按照bus2wp.py的说明，执行bus2wp.py将blogbus自定义格式的xml文件转换成wordpress标准xml文件;

6、转换后的wordpress数据文件有4M多，我用[DivXml](http://code.google.com/p/haifeng)将该文件拆分成四个1M左右的xml文件；

7、通过wordpress后台提供的导入功能将数据文件导入

这里我安装的wordpress是[2.8.6中文版](http://code.google.com/p/wordpresschina/downloads/list)（据说高版本的wordpress再导入bus2wp.py转换后的数据时会出现各种各样的问题）。导入过程很顺利，导入的大部分数据的格式都还是可接受的。

8、选择wordpress themes

2.8.6版本wordpress默认的Kubrick主题我一眼就看中了，不过该主题页面宽度不足，看起来很别扭，遂自己查资料，终于找到了一个Wide版的Kubrick的主题，下载后，替换了默认的主题。

9、安装必要插件

wordpress做得很强大，插件很多，根据朋友和网上推荐安装了Akismet、Add Post URL、Google XML Sitemaps、WP-Syntax和WordPress Database Backup等这几个插件。虽说安装过程都很简单，但是每个插件都要配置和测试，还是耗费了我不少精力。

10、整理文章

这是最痛苦的事。wordpress自带的默认编辑器很不给力，在“可视化编辑器”和“HTML编辑器”之间切换居然还会导致格式变化，导致刚整理好的格式瞬间丢失，还得重来，很痛苦。另外我还是一个追求完美的人，我最初计划将搬来的600多篇博客文章都整理一遍，修改每篇文章的永久链接地址、重新分配标签、更改文章内容中的所有链接（指向新博客站点中的文章），可昨天刚整理了三篇文章，我就发现这几乎是一个不可能完成的任务，我目前确实没有精力折腾这些事儿。

到此为止，我开始反思：我真的需要这样一个独立博客吗？独立博客有诸多好处，这个不用我说。但是这些好处中哪些是我真正需要的呢？顶级域名和稳定服务也许是我更看重的。但是国外提供的虚拟主机空间就一定比大巴稳定么？这个用过才知道，我还没有发言权。至于顶级域名其实blogbus也可以做绑定。

整理数据的这几天耗费了我很多精力，很多事情都因此耽搁了。我决定不再整理了，本次尝试搬家宣告失败！继续遵循多年前的那个选择：只要blogbus还继续提供服务，我就一直扎根这里。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我做了一件事，花了400大洋，成了blogbus的VIP，主要目的是为了去掉广告。

Blogbus确实不错。

另外，关于修改原文章中的链接的问题，以前我搬家时是用Vim直接修改数据库文件再导入，还是比较方便的。

不管独立与否，把东西放在别处，总是得要留心备份的。