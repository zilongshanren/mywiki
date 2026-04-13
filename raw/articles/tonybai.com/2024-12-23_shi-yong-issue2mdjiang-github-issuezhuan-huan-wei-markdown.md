---
title: 使用issue2md将Github issue转换为Markdown
url: https://tonybai.com/2024/12/23/convert-github-issue-to-markdown-with-issue2md/
published: '2024-12-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用issue2md将Github issue转换为Markdown

![](../../assets/d3ba4f52ac53d626.png)


[本文永久链接](https://tonybai.com/2024/12/23/convert-github-issue-to-markdown-with-issue2md) – https://tonybai.com/2024/12/23/convert-github-issue-to-markdown-with-issue2md

到2024年底，不论你是否承认，[AI时代都已经到来](https://tonybai.com/2024/10/14/programming-in-ai-era)！近两个月，三大顶级商业AI模型巨头：[Claude Sonnet 3.5](https://claude.ai/chats)、[Google Gemini 2.0 Flash Experimental](https://aistudio.google.com/)以及[ChatGPT o3](https://openai.com/12-days/)你方唱罢我登场，好不热闹！

作为走在AI应用前沿的程序员，利用AI辅助自己提高学习和工作实践的效率都是必不可少的。在使用AI的过程中，我们经常需要向其提供一些文档资料，对于文字资料，AI更偏爱TXT、Markdown、PDF等格式的文件。[部署在Vercel上的MarkdownDown](https://markdowndown.vercel.app/)支持输入网页URL并将其转换为Markdown，而[微软开源的MarkItdown](https://github.com/microsoft/markitdown)则能将多种格式(pdf、ppt、word、html、zip等)转换为Markdown。这些工具在实践中帮助我们实现对AI的快速“投喂”。

然而，一些资料，如GitHub Issues，尚不能通过上述工具方便地转换为干净的、无额外干扰内容的Markdown或其他适合投喂给AI的格式。受到MarkdownDown的启发，我思考是否可以将GitHub Issues转换为Markdown，最终促成了issue2md这个想法。该工具旨在简化GitHub Issues与Markdown之间的转换过程，使得开发者可以更高效地利用AI理解Github issue中的内容，包括用户讨论中的一些观点和想法。

三个月前，我利用AI完成了issue2md这个小工具，我自己甚至没有写下一行代码。我仅仅对其提出一个小小的要求，那就是**不要依赖任何第三方包，仅可以依赖Go标准库**。在这三个月中，该工具给了我很大的帮助，将由它生成的Github Issue对应的Markdown文档投喂给AI后，可以让我快速理解Github issue的要点，尤其是那些历经几年讨论，积累了数百条comment的issue！

这里我将[issue2md放到github上](https://github.com/bigwhite/issue2md)供大家下载使用，也希望能给大家带去相同的帮助。

下面简单介绍一下issue2md的用法。

issue2md项目有两个工具，或者说两种使用模式，一种是命令行模式，使用issue2md这个命令行工具。另外一种则是Web模式，使用issue2mdweb这个工具。

如果你喜欢命令行模式，那么你只需要使用下面命令安装issue2md即可：

```
$go install github.com/bigwhite/issue2md/cmd/issue2md@latest
```


issue2md cli程序的使用方法非常简单：

```
Usage: issue2md issue-url [markdown-file]
Arguments:
issue-url The URL of the GitHub issue to convert.
markdown-file (optional) The output markdown file.
```


它的第一个参数是github issue的URL。以[Go 1.24版本](https://tonybai.com/2024/12/17/go-1-24-foresight-part2/)json包[增加对omitzero的支持](https://tonybai.com/2024/09/12/solve-the-empty-value-dilemma-in-json-encoding-with-omitzero/)的issue为例，它的url是https://github.com/golang/go/issues/45669，我们原封不动的将其作为issue2md的第一个参数执行：

```
$issue2md https://github.com/golang/go/issues/45669
Issue and comments saved as Markdown in file golang_go_issue_45669.md
```


issue2md cli默认会生成一个命名格式如下的文件：

```
{owner}_{repo}_issue_number.md
```


其内容使用markdown编辑器打开并渲染后将呈现如下的效果：

![](../../assets/9f6542a6652e1922.png)


当然你也可以通过传入第二个命令行参数，作为最终生成的markdown的文件名！

如果你不喜欢命令行模式，你可以**使用issue2mdweb提供的Web模式**。最简单的启动一个issue2mdweb服务的方法就是利用我发布到Docker hub上的issue2md的公共镜像，你可以像下面这样在本地或你的私有云里运行一个issue2mdweb服务：

```
$docker run -d -p 8080:8080 bigwhite/issue2mdweb
```


然后用你的浏览器打开http://{host}:8080这个地址，你将看到如下的页面：

![](../../assets/f58780f2cf7f47cc.png)


在中间的文本框中输入你要转换的Github issue地址，比如前面的https://github.com/golang/go/issues/45669，点击“Convert”，你的浏览器就会自动将转换后的Markdown文件下载到你的本地，文件命名和issue2md cli的默认命名格式一致！

如果你不想使用Docker运行，你可以自行下载issue2md代码并编译，也可以使用scripts中的命令将issue2mdweb安装为一个Systemd unit服务！

这里要注意的是，issue2md使用了Go标准口实现了对Github API的访问且没有使用任何账号信息，它仅适合将Public仓库的issue转换为Markdown，并且由于Github对API调用的限速，你在使用issue2md时不能过于频繁！此外，你若发现issue2md的bug或者你有什么新的想法，欢迎[在issue2md仓库中提出你宝贵的issue](https://github.com/bigwhite/issue2md/issues)。

最后打个“广告”，根据极客时间的专栏推广计划，我在春节前会为“[Go语言第一课](http://gk.link/a/10AVZ)”专栏[续写五篇文章](https://time.geekbang.org/column/article/835197)，其中的第一篇“[Go测试的5个使用建议](https://time.geekbang.org/column/article/835208)”已经上线。

无论你是“Go语言第一课”的学员，还是首次听说这门专栏的小伙伴，我都欢迎你阅读这些文章，希望这些专栏文章能你带去新的收获！也欢迎你将阅读后的感受在评论区分享出来！

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论