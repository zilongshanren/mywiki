---
title: Blog新起点 – 从BlogBus搬家到WordPress
url: https://tonybai.com/2012/02/29/a-new-departure-of-my-blog-move-from-blogbus-to-wordpress/
published: '2012-02-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Blog新起点 – 从BlogBus搬家到WordPress


自从2004年

[开博](http://tonybai.com/2004/09/15/the-first-blog/)以来，我坚持了七年多，至今仍孜孜不倦，写博客已经成为我的生活中不可或缺的一部分，即使在[微博](http://en.wikipedia.org/wiki/Microblogging)等大行其道的今天，我亦然如此。作出搬家的决定显然是十分痛苦的，因为要抛弃已经建立起来的使用习惯以及Blog人气(包括搜索引擎索引、外部引用的等)是十分艰难的。但我还是决定搬家，更多是因为我的一个小小的梦想：拥有一个自己可以完全控制的独立域名的个人站点。tonybai.com这个顶级域名是在2010年申请的，2010年末曾经尝试过一次

[搬家](http://tonybai.com/2010/11/30/try-to-move-blog/)，但因技术原因最终没能实现。但鉴于BlogBus提供的服务愈发地不稳定，我又动了搬家的念头，而且有了上次失败的教训，这次我做好了充足的资料和技术准备。但即使如此，搬家过程依旧很辛苦，并且足足花了我一周多的业余时间，下面就来罗嗦一下搬家的过程。一、准备工作

· 申请域名

· 购买主机服务

· 安装WordPress

由Puras帮忙在我的主机空间上安装了WordPress 3.2.1。

· 从BlogBus导出Blog数据

使用BlogBus后台管理提供的导出工具，将你的Blog导出，顺利地话你将得到一个类似backup-20120217204644.xml这样的文件。导出后用编辑工具打开瞧瞧，看看导出的是否完整。

· 将BlogBus数据文件转换为可导入WordPress的数据文件

这次搬家我直接使用了"

[爱写字](http://ixiezi.com)"提供的转换服务。首先在"爱写字"申请一个博客，然后通过其导入工具将上面导出的BlogBus的数据文件导入到"爱写字"中，我的导入过程很顺利，没有报错，但遗憾的是我在BlogBus上回复朋友的评论无法导入。· 修改Blog文章和链接

"爱写字"支持免费域名绑定。我先将tonybai.com绑定到"爱写字"上，然后直接在"爱写字"上修改博客数据，包括建立分类、修改每篇Blog的自定义地址、内容中的链接以及自定义标签，这是一个极其繁琐且痛苦的活儿，也是整个搬家过程中最最耗时耗力的环节，我足足花了一周多。

· 导出WordPress数据文件

通过WordPress后台的导出工具，将修改好的Blog数据导出，这里有一个缺陷：那就是你的友情链接数据无法导出。

二、WordPress站点配置及数据导入

· WordPress设置链接格式

进入WordPress控制面板，选择"设置"->"固定链接"，设置链接形式为："http://tonybai.com/2012/02/29/sample-post/"，之后WordPress提示我需要修改".htaccess"文件。由于之前没有该文件，我按WordPress的提示，编辑好.htaccess文件后，上传到站点根目录下。

· WordPress媒体设置

进入WordPress控制面板，选择"设置"->"媒体"，去除"以年—月目录形式组织上传内容"选项，统一使用默认的上传文件目录(需在wp-content下手工创建uploads目录)。

· 安装WordPress Importer插件

WordPress的导入功能是通过插件提供的，我们需要手动安装。在"安装插件"中搜索"WordPress Importer"，得到结果后，点击"安装"，WordPress就会自动进行插件安装。

· 导入WordPress数据文件

WordPress Importer安装完毕后，即可进行数据导入。导入前先用Ftp工具将uploads目录权限设置为777，然后选择本地要导入的文件，导入即可。WordPress Importer支持.gz结尾的压缩文件，它可以在上传后自动解压并导入数据。

· 配置WordPress Theme

我选择的是"Notepad Theme 1.3"，这个比较简单，不多说了。

· 设置边栏布局

通过控制面板中的"外观"-> "小工具"，我们可以通过拖拽的方式自定义边栏的布局，比如使用分类、日历、标签云等。

· 安装必要插件

目前我安装的必要插件有CKEditor for WordPress、Akismet、Copyrighted Post、Google XML Sitemaps、WP-RecentComments、BackUpWordPress、Google Analytics for WordPress等。

· 安装robots.txt

为了控制搜索引擎的行为，编写了一个robots.txt，放到了站点根目录下：

User-agent: *

Disallow: /wp-

Disallow: /feed/

Disallow: /?feed

Disallow: /comments/feed

Disallow: /trackback/

· 设置Feed

为了编译了解订阅情况，我增加了一个二级域名feed.tonybai.com用于统一Feed地址。我通过

[Feedsky](http://feedsky.com)提供的服务将feed.tonybai.com绑定到feedsky提供的一个Feed(http://feed.feedsky.com/bigwhite)上，而Feed源使用的是WordPress自带的Feed地址http://tonybai.com/feed。另外我修改了Notepad Theme 1.3的源码，将页眉的RSS图标对应的Feed地址统一也改为了http://feed.tonybai.com，希望各位朋友也使用这个地址订阅本博客。三、WordPress站点备份

· 采用BackUpWordPress备份整个站点

BackUpWordPress不仅仅可以备份DB，还可以备份整个站点文件。备份前将wp-content目录的权限改为777，这样该插件就会在wp-content/backups下自动定期生成备份文件。如果需要，还可设置将备份的文件mail到指定邮箱中。

· 备份Blog文章数据

为了保险，我还会定期将最重要的Blog文章数据导出(xml格式)并压缩备份。

四、其他设置

· 统计服务

原BlogBus是自带统计服务的，搬到WordPress后我采用两个第三方的统计服务：

[Google Analytics](https://www.google.com/analytics/)和[StatCounter](http://statcounter.com)，其中Google Analytics可通过"Google Analytics for WordPress"进行设置和验证；StatCounter的安装则是通过在边栏的自定义Html代码区域添加完成的。· 自定义Html代码

新浪微博秀、Google Reader分享等Widgets可通过边栏的自定义Html代码添加到站点上。

OK，至此搬家过程的大部分工作都算是结束了，后续还会从BlogBus迁移一些图片到WordPress上，但都是些小活儿了。另外这次虽然离开了BlogBus(博客大巴)，但我仍要感激BlogBus这七年来为我提供的免费服务，也希望BlogBus能够坚持地走下去，并且能走得更好。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

一周业余时间弄好也差不多啦

嗯，不过这一次做完就一劳永逸了，以后再搬家应该就没有这么难和痛苦了。

你也终于加入WP的阵营了:) 祝贺搬家成功~

嗯，主要还是喜欢能独立控制的blog，再者不知怎么搞的blogbus最近一年来实在是不稳定，没有安全感阿。