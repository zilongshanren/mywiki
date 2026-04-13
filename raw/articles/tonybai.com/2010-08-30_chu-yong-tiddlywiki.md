---
title: 初用TiddlyWiki
url: https://tonybai.com/2010/08/30/learn-tiddlywiki/
published: '2010-08-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 初用TiddlyWiki

2008年末和一位同事在山西出差，发现那位同事在用[TiddlyWiki](http://www.tiddlywiki.com/)写一些日记，那时候算是第一次知道TiddlyWiki，但不知是为什么，当时的我并没有被TiddlyWiki所吸引，也就失去了一次使用TiddlyWiki的机会。

近期新启动了一个产品版本的开发任务，该版本是对之前遗留系统版本的重构和优化，我们想趁此机会将梳理遗留系统时总结下来的东西以及一些新的设计想法记录下来，以便于后人参考并迅速上手。曾经使用[Confluence](http://www.atlassian.com/software/confluence/)搭建过一个Wiki，但是该系统因公司政策被取消了。公司一年多以前建立了一个知识管理系统，不过我们发现这个系统极其难用，完全不能满足我们需要，这时我们又想起了TiddlyWiki。

TiddlyWiki应该算是世界上最小巧、最简单的Wiki工具了，只有一个大概300多K的html文件，所有功能都内置在该文件里，你编辑的内容也会在文件中存储着。从官方站下载后，用[Firefox](http://tonybai.com/2008/12/17/accelerate-the-firefox-on-ubuntu/)打开即算安装完毕了。

-> 定制你的TiddlyWiki

使用TiddlyWiki第一步想必都是定制界面吧。如果你想用TiddlyWiki写日记，那起码应该把Wiki页面上方的"My TiddlyWiki a reusable non-linear personal web notebook"字样修改一下，改成"Tony's Diary"之类的描述文字。另外英文看起来比较费劲，至少都应翻译成中文，TiddlyWiki默认采用[UTF-8编码](http://tonybai.com/2007/11/03/also-talk-about-char-encoding/)，对中文的支持完全没有问题。

TiddlyWiki默认页面中的"GettingStarted"会引导你做一些页面元素信息修改和定制。

* SiteTitle: 页面的主标题，点击斜体的"SiteTitle"，在延伸打开的"SiteTitle"编辑区域中找到"edit"，点击它编辑SiteTitle，比如改为“XX Developer Guide"。

* SiteSubtitle：

页面副标题，修改方式同上。

-> 关于Tiddler

在Wiki页面上你会看到较多的提示说明中都有Tiddler一词，官方给出的术语解释是”A content pane inside TiddlyWiki“，实际上Tiddler就是我们输入内容、图片、链接的地方。我们可以新建、修改和删除一个Tiddler，我们的Wiki实际上也是众多Tiddler的聚合体。系统有很多内建的特殊Tiddler，比如SiteTitle、SiteSubtitle、MainMenu、DefaultTidders(记录在启动时自动打开的Tiddlers列表)等，对于这些内建的Tiddlers建议保留。Tiddlers是按照名字识别和组织的，在页面右侧的包含多个Tab的那个栏里有一个"all" Tab，那里记录着所有的Tiddlers。


-> Tiddler内容编辑

新建一个Tiddler，我们就可以编辑Tiddler的内容了，一般我们最常使用文字、图片和超链接来表达我们的想法。

文字没有什么特殊的地方，顶多是字体上的差异，关于字体语法在[中文TiddlyWiki](http://www.tiddly.cn/)上有详尽的说明。

贴图编辑格式：[img[果果|images/果果.jpg]] ，其中“果果”是鼠标悬浮在图片上时显示的文字，“images/果果.jpg”是图片的本地地址或Web Url”。当使用本地地址时，当前目录为TiddlyWiki文件所在目录。

链接到某文件：[[安装方法|install_guide.txt]]中的xxxx，其中“安装方法”将在界面中以带下划线的超链接显示出来，点击后Firefox会自动打开install_guide.txt; 如果把install_guide.txt换成install_guide.odt，那么Firefox会弹出对话框让你选择是打开还是Save。

链接到另外一个TiddlyWiki的Tiddler: [[安装指南|user_guide.html#快速入门]]中的xxx，其中user_guide.html是另外一个TiddlyWiki文件，“快速入门”是user_guide.html中的一个Tiddler，用一个#号将两者联系起来，这样点击后，Firefox会自动打开user_guide.html并跳转到打开的“快速入门”Tiddler上。

TiddlyWiki有一些高级功能还待挖掘中，不过估计可能也用不上多少，毕竟我们更多是提供内容。

由于不能为TiddlyWiki搭建一个Web服务器，因为那可能又与公司策略抵触，因此我们用[svn管理](http://tonybai.com/2010/08/07/use-svn-pre-commit-hook/)TiddlyWiki文件(必要时可采用lock-modify-unlock模式。 另外TiddlyWiki毕竟采用的是单文件格式，一旦内容过多会导致文件Size过大，所以在使用TiddlyWiki之前最好做好规划，采用多TiddlyWiki files配合使用的方式，充分利用TiddlyWiki file之间的超链接和自动识别功能。

最后建议设立专人定期负责内容的整理和重编排，使信息的组织逻辑更清晰合理，也算是对Wiki的“重构”了。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

这玩意儿和网博士等知识管理类软件有啥区别？

我的天

这东西太神奇了