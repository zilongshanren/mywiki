---
title: 云风的 BLOG
url: https://blog.codingnow.com/2020/02/
published: '2020-02-12'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### git shallow clone 的一个问题

最近在家办公，遇到的第一个问题就是家里网络极不稳定，无法 git clone 那些庞大的仓库。我知道 git 现在支持浅拷贝，用 --depth 1 就可以取出某个分支的 HEAD 指向的拷贝所依赖的所有文件。

但是，光用 git clone url --depth 1 还不能解决我的所有问题。因为需要传输的文件还是太大，不稳定的网络无法坚持到我顺利下载完成就断开了。而 git clone 得下载过程似乎不能续传，我只好另辟蹊径。

过去翻 git 文档时，曾经了解过有一个 git bundle 这个指令可以对需要传输的内容打包，然后大多数依赖接受数据的 git 指令都可以直接接收用 git bundle 打好的包，而不必通过网络传输。事实上，git clone 的过程就是在远程打好包，然后传输到本地，再解开的。

我想好的曲线救国的策略就是，找一台远程连接顺畅的虚拟主机，进行这样的步骤：

- git clone url --depth 1 在远程复制一份仓库的浅拷贝
- git bundle create bundlefile --all 打个包。
- 用支持续传的 sftp 下载这个 bundlefile 到本地。
- 在本地用 git clone bundlefile 还原。

但实际操作到第 4 步的时候，发现 git 报告 "fatal: Failed to traverse parents of commit xxxxxxxx" ，这个 xxxxxxxx 就是我那个仓库 HEAD 的 hash 。

我 google 了一下，找到 [一篇 2015 年的帖子](http://git.661346.n2.nabble.com/Clone-from-shallow-bundle-bug-td7628150.html) ，谈的是同样的问题。

大意是说，当我们的仓库是一个 shallow clone 的时候，有一个 .git/shallow 文件指明了这点。但是 bundle 却没有打包进这个文件。也就是说，一个 bundle 无法说明自己是一个 shallow clone 。

根据我的理解，bundle 其实是 git 给仓库生成的 delta 信息，而非对整个仓库的复制。而 git clone 必须依赖 base 和 delta 才能还原仓库（不知道是否理解正确）。对于完整仓库的 bundle 是一个特例，我们可以从中还原出来，但是对于 shallow 仓库来说，缺少了 delta 就失败了。

鉴于这个帖子的讨论是 2015 年的，可能现在已经解决了。但我把本地的 git client 升级到了最新的 2.25.0 ，依然无法处理以上问题。

第一天时因为急用，我直接对远程仓库目录打了个包下载到本地。今天有点时间，又重新研究了一下。

既然这个 bundlefile 文件中的确包含有所有我需要的所有文件，那么终归是有办法的。

我尝试用 git init 创建了一个新仓库，然后在仓库下运行 git bundle unbundle bundlefile ，还原出所有仓库文件。这时的仓库是没有 HEAD 的，不过既然我们知道 HEAD hash ，可以自己用 git checkout hash 取出来。然后再用 git switch -c master 固定在主分支上就好了。所有文件都能顺利检出。

不过，接下来，我们运行 git log 会发现出错。再检查，的确是缺少 .git/shallow 文件，也就是说现在复制出来的这个仓库，git 还不知道是 shallow clone 。好在这个文件很简单，就是 HEAD 的 hash 。手工创建一个就好了。

到这一步，大功告成。