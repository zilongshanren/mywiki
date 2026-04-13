---
title: 迁移 blog 到 wordpress
url: https://69d0b043.blog-yq6.pages.dev/blog/wordpress-migration/
published: '2022-01-01'
source_blog: lucida
source_site: http://lucida.me/
category: game programming
fetched: '2026-04-13'
---

### lucida.me

lucida.me 是我在 2014 年时创建的 blog。

最初我在模仿 刘未鹏 的 [mindhacks](http://mindhacks.cn/)：深度长文，技术为主，顺带一些诙谐。

7 年之后，lucida.me 只有十余篇文章，虽然一些文章的点击量还可以（比如 [程序员必读书单 1.0](https://blog.lucida.me/blog/developer-reading-list/) 和 [我的算法学习之路](https://blog.lucida.me/blog/on-learning-algorithms/) 这两篇），但更新极慢，中间还断更两三年之久。

2021 年的年底，我打算重新写点东西。

不会像之前写书单推荐一百多本书那么夸张，毕竟那类长文工作量太大，既没有时间，也没有动力。况且工作时间越长，越能意识到自己的不足，越不敢随便推荐。

应该会写点书评，偶尔吐个槽。

### jekyll → hexo → wordpress

lucida.me 经历了三个阶段：

- github pages + jekyll（2014 - 2016）：利用
[github pages](https://pages.github.com/)作为托管空间，[jekyll](https://jekyllrb.com/)作为博客框架 - VPS + hexo （2016 - 2021）：鉴于 github 间歇抽风，更换到一个更稳定的 VPS，并把迟迟没更新的 jekyll 换到
[hexo](https://hexo.io/) - VPS + wordpress（2021 -）：当前状态

#### 为什么要从 hexo 切换到 wordpress

一个字：懒。

hexo 是很好的静态博客框架：刚刚发布了 [6.0 版](https://hexo.io/news/2021/12/26/hexo-6-0-0-released/)，拥有大量主题和插件，其静态特性使其及其高效。

很多程序员都喜欢用 hexo 搭建自己的技术博客，静态页面和免费的 github pages 搭配很好。

但程序员喜欢的，往往不太靠谱：

- hexo 的配置过于麻烦：需要本地安装 node.js，git 和 npm，并需要设置 git hooks 来在 git push 时重新构建整个博客。每次更换机器，都需要重新配置一遍。
- hexo 写文章时，使用 markdown 再用 git 推送，诚然这些操作可以在 Visual Studio Code 中完成，但还是没有所见即所得的编辑器方便。
- 回想之前，更新频率这么低，相当一部分原因是因为懒得开 VSC 写 markdown 敲命令，一段时间过去，连 hexo 命令都忘了

相比较下：

- wordpress 配置及其简单，很多 VPS 都提供了一键安装服务
- 所见即所得，wordpress 的 gutenberg 编辑器相当强大（不太好用，可能需要适应）
- 可以在任何地方写文章，只要有浏览器就可以

可能是岁数大了，我懒的再去折腾各种配置项敲命令行，现在工作中写代码都越来越少，更别提工作以外。

接下来会慢慢的把原来博客的文章迁移到这里。一些比较中二的文章就不再迁移，现在自己看都觉的二。