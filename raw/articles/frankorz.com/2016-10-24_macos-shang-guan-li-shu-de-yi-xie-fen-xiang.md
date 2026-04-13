---
title: macOS 上管理书的一些分享
url: http://frankorz.com/2016/10/24/manage-books-on-macOS/
author: 文章作者 猫冬
published: '2016-10-24'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/58ed46ccb2e6c783.jpg)


在生活中，我时不时会买一些书，包括电子书和实体书。随着书籍的增多，我作为一个工具控也有着自己一套管理书籍的方式，在这里与大家分享。

本文不会涉及电子书解密与分享，仅作经验分享。

### 电子书

随着亚马逊的大力推广，我较关注的技术书也因其时效性多以电子书形式发布，电子书实际上占用了我生活中所购买书的一大部分。

下图是我所经历亚马逊一些较大的优惠，其中第二个限时优惠更是允许我不到 8 元买到四本接近百元的电子书(亚马逊药丸！！)。我也经常从[图灵社区](http://www.ituring.com.cn)购买一些技术书籍，图灵社区提供的是未加密的电子书，加之一些网友也有分享自制的电子书，因此能很方便地放到不同工具中阅读和管理。

![](../../assets/746265c1c3668914.jpg)


![](../../assets/71ade36b5201c4a8.jpg)


我们所经常遇到的电子书格式通常有 Mobi、Epub、PDF 等格式，阅读 PDF 我推荐使用 PDF Expert 2，其余类型电子书我推荐用 Clearview 阅读，epub 用 iBook 阅读也是不错的体验，Mobi 也能放到 Kindle for mac 上阅读。

[豆瓣读书](https://book.douban.com)也提供了一个很好的管理书籍的平台，也方便书友写书评和交流。

![书](../../assets/4baf58a17a71cd40.png)


#### Calibre

[Calibre](https://calibre-ebook.com) 是一款强大的免费开源电子书管理软件，支持 macOS、Windows、Linux。作者几乎每两周就会更新一次软件，这里是[开源地址](https://github.com/kovidgoyal/calibre)。

![](../../assets/c4a3916fdf623432.jpg)


##### 编辑书籍元数据

![](../../assets/1e62e0f71a611c22.jpg)


##### 下载元数据

![](../../assets/49847a22ba359284.jpg)


##### 转换书籍

Calibre 转换书籍也方便，能自定义字体、字体大小、自动检测增加目录、更改页面设置等，转 PDF 的时候注意下页面边距和行距。

![](../../assets/489ebffd480616df.jpg)


##### 多种分类方便搜索

![](../../assets/73116374cafd45c9.jpg)


在电子书右键选择 Calibre 打开后，Calibre 会把电子书复制到你设置的仓库中，根据作者名分类，编辑的书籍元数据也会储存到一起。仓库也能备份成一个文件，防止电子书丢失，方便转移。

![](../../assets/4d5cd2bc5958c2a0.jpg)


##### 推送电子书

![](../../assets/21ebc45d15863f34.jpg)


![](../../assets/93566cb0987229e5.jpg)


发送邮件的配置可以参考邮箱网页版的设置页面中STMP服务器项填写。

点击测试邮件发送按钮后会尝试发送一个内容为“Test mail from calibre”的邮件到亚马逊接收推送的电子邮箱，稍等片刻若收到如下图的邮件则说明测试成功。

![](../../assets/5d613987f9b8eb15.jpg)


其中接收电子书推送的邮箱可以在[管理我的内容和设备](https://www.amazon.cn/gp/digital/fiona/manage?ref=sa_menu_kindle_l3_device&#manageDevices)中“我的设备”或“设置”中找到。

![](../../assets/2dc518f8156b4d07.jpg)


同时别忘了把你的邮箱添加到“已认可的发件人电子邮箱列表”中，否则 Kindle 将会接收不到推送，该页面可以在同页面的“设置”底部。

![](../../assets/34ff4e527439df17.jpg)


![](../../assets/098a495567f9e9e7.jpg)


大概在半小时过后我的 Kindle 应用才同步到这本电子书，另外我只给 iPad 的 kindle 推送邮箱推送后，全部设备的 Kindle 应用云端上都可以看到这本电子书，还是很方便的。

更多Calibre 技巧可以参考[Calibre 使用教程](http://kindlefere.com/post/tag/calibre)，本文仅作抛砖引玉。

### 实体书

京东抽奖得的 200-100 图书券、会员每月可得的 200-80 勋章券，还有亚马逊时不时的活动，我对买实体书完全没有抵抗力…

实体书的管理可能没电子书管理这么有必要，我们仍然可以管理书籍读书状态，拥有的书籍信息。这里要介绍的是一款新生的工具——Shelf。

macOS 上在书籍方面有很多出色的工具，不仅仅是管理书籍，更多的是创作文字、阅读、制作电子书等各方面的工具。iPhone 上也有很多方便管理实体书的 App，例如：美丽阅读、藏书阁等，通过扫书籍条形码添加书籍再管理。这方面也是不同设备的优点吧，我认为 macOS 实际上更适合写书评、读后感之类的创造性行为。

### 小脚本

买书时我喜欢参考豆瓣网的评分，但是我不喜欢复制书名再打开新的页面搜索，有个小脚本可以帮到我们。

![](../../assets/9c59cdf6111014a7.jpg)


这个油猴脚本需要浏览器插件支持，详情如下：

- Microsoft Edge 14以上：
[Tampermonkey](http://tampermonkey.net/index.php?ext=dhdg&browser=edge)。 - Firefox 及相关的浏览器：
[Greasemonkey](https://addons.mozilla.org/zh-CN/firefox/addon/greasemonkey/)。 - Google Chrome、Chromium 及相关的浏览器：
[Tampermonkey](http://tampermonkey.net/index.php?ext=dhdg&browser=chrome)。 - Opera (版本 15 及更晚)：
[Tampermonkey](https://addons.opera.com/extensions/details/tampermonkey-beta/)或者[Violentmonkey](https://addons.opera.com/zh-cn/extensions/details/violent-monkey/?display=en)。 - Opera 版本 12 及更早原生支持用户脚本。但
[Violentmonkey](https://addons.opera.com/zh-cn/extensions/details/violent-monkey/?display=en)能提供更友好的界面和更好的兼容性。 - Safari：
[Tampermonkey](http://tampermonkey.net/index.php?ext=dhdg&browser=safari)

装完插件后到这安装脚本 [Douban Book Bar](https://greasyfork.org/zh-CN/scripts/3737-douban-book-bar) [安装此脚本]->[安装]

脚本适用于：图灵社区、京东、亚马逊中国、当当、多看、苏宁易购、文轩和 China-pub

祝买书快乐！

### 总结

“买书如山倒，读书如抽丝”这句话很适合我，本博文只为买书提供了一个管理方法的整理，关键还是”读书”。

前不久我写了篇关于[macOS 上的时间跟踪软件](http://frankorz.com/2016/10/21/new-time-tracking-app-on-macOS/)的文章，直到今天我写完本文章，心情是挺苦恼的，因为我能帮别人节省的仅仅是找书的时间。我真正想做到的是让人读书，估计得自己还有很长一段路要走。(一刹那宛如鲁迅再生，毅然弃医从文！！)

有了挤出来的时间，有了最好的阅读工具，有了方便的书籍管理工具，我们距离读书还差点什么呢？