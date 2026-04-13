---
title: 基于Markdown格式的电子书生成工具大比拼：gohugo、mdbook和peach
url: https://tonybai.com/2020/06/27/gohugo-vs-mdbook-vs-peach/
published: '2020-06-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 基于Markdown格式的电子书生成工具大比拼：gohugo、mdbook和peach

基于[Markdown格式](http://en.wikipedia.org/wiki/Markdown)文件[写博客已经很多年了](https://tonybai.com/2015/09/19/write-blog-in-markdown/)，一直使用的是Wordpress的markdown插件，由于各种遗留原因，一直没有转换到直接使用静态站点的方式。博客文章之间一般来说多是独立篇章，少有关联，即便是写一个系列文章，数量也不会太多。因此，用博客形式来组织书籍章节是不大合适的。“术业有专攻”，我们还得寻找专门用来制作电子书的工具或平台，并且要支持本地安装，支持基于Markdown格式的源数据文件。

专门用于制作电子书类文档的知名工具包括：[gitbook](https://www.gitbook.com/)和[Read the Docs](https://readthedocs.org/)。不过前者的[开源版本](https://github.com/GitbookIO/gitbook)2018年末就[不更新了](https://legacy.gitbook.com/)，而**Read the Docs**则比较老，还需要多个工具配合。我个人倾向于单个二进制文件搞定一切。于是我找到了三个候选：[gohugo](https://gohugo.io/)、[mdbook](https://github.com/rust-lang/mdBook)和[peach](https://github.com/peachdocs/peach)，这三个候选部署时都只有一个二进制文件。[gohugo](https://tonybai.com/2015/09/23/intro-of-gohugo/)和peach是[Go语言](https://tonybai.com/tag/go)实现的，而mdbook则是用[Rust语言](https://www.rust-lang.org/)实现的。下面我们就来简单对比一下这三个基于Markdown格式的电子书制作工具。

## 1. mdbook

mdbook是模仿gitbook样式的从markdown文件生成电子书的工具和静态站点服务，它仅聚焦于“电子书制作和站点服务”。如果不是类似gitbook风格的其他类静态内容服务，那么它并不适合。因此，该工具采用了惯例优先原则(convention over configuration)，使得使用时我们无需做太多的配置即可生成一个**像模像样**的电子书站点。

由于是rust实现的，mdbook本地部署时只需一个二进制文件，我们直接从它的github release上下载对应os平台的release文件（这里是macos的0.4.0版本）：

```
wget -c https://github.com/rust-lang/mdBook/releases/download/v0.4.0/mdbook-v0.4.0-x86_64-apple-darwin.tar.gz
```


解压后，将mdbook所在路径添加到**PATH**环境变量中：

```
$tar zxvf mdbook-v0.4.0-x86_64-apple-darwin.tar.gz
x mdbook
$ls
mdbook* mdbook-v0.4.0-x86_64-apple-darwin.tar.gz
$mdbook -help
mdbook v0.4.0
Mathieu David <mathieudavid@mathieudavid.org>
Creates a book from markdown files
USAGE:
mdbook [SUBCOMMAND]
FLAGS:
-h, --help Prints help information
-V, --version Prints version information
SUBCOMMANDS:
build Builds a book from its markdown files
clean Deletes a built book
help Prints this message or the help of the given subcommand(s)
init Creates the boilerplate structure and files for a new book
serve Serves a book at http://localhost:3000, and rebuilds it on changes
test Tests that a book's Rust code samples compile
watch Watches a book's files and rebuilds it on changes
For more information about a specific command, try `mdbook <command> --help`
The source code for mdBook is available at: https://github.com/rust-lang/mdBook
```


接下来，我们就使用**mdbook init**命令创建一个电子书工程：

```
$mdbook init go-ml
Do you want a .gitignore to be created? (y/n)
y
What title would you like to give the book?
go machine learning
2020-06-27 15:58:03 [INFO] (mdbook::book::init): Creating a new book with stub content
All done, no errors...
```


我们看到**mdbook init**生成了一个目录，目录布局如下：

```
➜ /Users/tonybai/MyEbook/mdbook git:(master) ✗ $tree
.
└── go-ml
├── book
├── book.toml
└── src
├── SUMMARY.md
└── chapter_1.md
3 directories, 3 files
```


接下来，我们直接运行**mdbook serve**即启动了一个服务，用于访问该电子书：

```
➜ /Users/tonybai/MyEbook/mdbook git:(master) ✗ $mdbook serve go-ml
2020-06-27 16:06:56 [INFO] (mdbook::book): Book building has started
2020-06-27 16:06:56 [INFO] (mdbook::book): Running the html backend
2020-06-27 16:06:56 [INFO] (mdbook::cmd::serve): Serving on: http://localhost:3000
2020-06-27 16:06:56 [INFO] (warp::server): listening on http://[::1]:3000
2020-06-27 16:06:56 [INFO] (mdbook::cmd::watch): Listening for changes...
```


我们通过浏览器访问**http://localhost:3000**，可以看到如下页面：

![img{512x368}](../../assets/6ab913ada6d3df7e.png)


我们看到：我们没有做任何配置就生成了一个和gitbook样式差不多的电子书服务站点。该站点还支持选择页面显示模式（截图中使用的是默认的Light模式）、支持查询等。

如果我们要增加新章节、编排章节标题缩进，只需编辑电子书工程下面的**src/SUMMARY.md**：

```
$cat SUMMARY.md
# Summary
- [Chapter 1](./chapter_1.md)
- [Chapter 1.1](./chapter_1_1.md)
- [Chapter 2](./chapter_2.md)
```


这些对于多数人来说已经是足够了的，后续只需关注书籍内容即可，无需对mdbook生成的工程进行什么调整。mdbook会自动探测src目录下的文件变化并根据变化重新生成静态html文件。我们只需刷新页面即可看到最新变化。

## 2. peach

[peach](https://peachdocs.org/docs)是一款由Go语言实现的多语言、实时同步以及全文搜索功能的 Web 文档服务器。它由gogs的作者[无闻](https://github.com/unknwon)打造，该作者的很多开源项目的文档也都是由peach生成和提供文档服务支撑的。

我们可以直接使用**go get**安装peach：

```
$export GONOSUMDB="github.com/russross/blackfriday"
$go get github.com/peachdocs/peach
go: github.com/peachdocs/peach upgrade => v0.9.8
$peach -v
Peach version 0.9.8.0810
```


接下来，我们用peach建立电子书工程：

```
$peach new -target=go-ml.peach
➜ Creating 'go-ml.peach'...
➜ Creating 'templates'...
➜ Creating 'public'...
Do you want to use custom templates?[Y/n] n
✓ Done!
```


我们这里直接使用peach项目自身文档的自定义模板：

下载配置好的自定义模板：

```
$ cd go-ml.peach
$ git clone https://github.com/peachdocs/peach.peach.git custom
Cloning into 'custom'...
remote: Enumerating objects: 62, done.
remote: Total 62 (delta 0), reused 0 (delta 0), pack-reused 62
Unpacking objects: 100% (62/62), done.
Checking connectivity... done.
```


启动web服务：

```
$peach web
intro/
|__ installation
|__ getting_started
|__ roadmap
howto/
|__ documentation
|__ webhook
|__ templates
|__ static_resources
|__ navbar
|__ pages
|__ extension
|__ protect_resources
|__ upgrade
advanced/
|__ config_cheat_sheet
faqs/
intro/
|__ installation
|__ getting_started
|__ roadmap
howto/
|__ documentation
|__ webhook
|__ templates
|__ static_resources
|__ navbar
|__ pages
|__ extension
|__ protect_resources
|__ upgrade
advanced/
|__ config_cheat_sheet
faqs/
[Peach] 20-06-27 10:17:31 [ INFO] Peach 0.9.8.0810
[Peach] 20-06-27 10:17:31 [ INFO] Peach Server Listen on 127.0.0.1:5556
```


我们通过浏览器访问**http://localhost:5556**，可以看到如下页面：

![img{512x368}](../../assets/e640a6f27f234ad5.png)


不过，和mdbook不同，上面peach加载并渲染的文档并不在本地，我们在custom/app.ini中看到如下配置：

```
[docs]
TYPE = remote
TARGET = https://github.com/peachdocs/docs.git
SECRET = peach
```


我们看到当前例子采用了**remote**模式，即使用Github上的仓库peachdocs/docs中的数据(markdown文件）作为源文件进行渲染，而这个仓库的结构如下：

```
$tree -L 2 docs
docs
├── TOC.ini
├── en-US
│ ├── advanced
│ ├── faqs
│ ├── howto
│ └── intro
├── images
│ └── github_webhook.png
└── zh-CN
├── advanced
├── faqs
├── howto
└── intro
11 directories, 2 files
```


TOC.ini文件描述了文档结构布局：

```
$cat TOC.ini
-: intro
-: howto
-: advanced
-: faqs
[intro]
-: README
-: installation
-: getting_started
-: roadmap
[howto]
-: README
-: documentation
-: webhook
-: templates
-: static_resources
-: navbar
-: pages
-: extension
-: protect_resources
-: upgrade
[advanced]
-: README
-: config_cheat_sheet
[faqs]
-: README
```


我们看到，和mdbook相比，peach的门槛稍高一些，需要学习TOC.ini中的特殊配置语法，同时如果要改变peach的默认风格，还要学习peach使用的模板语法(Peach 使用 Go 语言 Pongo2 v3 版本 作为模板引擎，它使用的是 Django HTML 格式)。

## 3. gohugo+git book theme

gohugo是这几年最火的静态站点生成工具。和上面两个工具不同的是：它致力于成为一个通用的静态站点工具，与hexo等目标一致。结合gohugo与git book风格的theme也能实现电子书制作与站点服务。

经过多年发展，gohugo的安装十分方便：在macos上，我们既可以使用go get安装（gohugo支持module），也可以使用brew安装：

```
$brew install hugo
==> Downloading https://mirrors.ustc.edu.cn/homebrew-bottles/bottles/hugo-0.69.2.mojave.bottle.tar.gz
==> Summary
/usr/local/Cellar/hugo/0.69.2: 42 files, 74.3MB
==> `brew cleanup` has not been run in 30 days, running now...
Removing: /usr/local/Cellar/gettext/0.20.1... (1,899 files, 18.5MB)
... ...
$hugo version
Hugo Static Site Generator v0.69.2/extended darwin/amd64 BuildDate: unknown
```


通过**hugo new site**命令，我们来创建一个新的站点：

```
$hugo new site go-machine-learning
Congratulations! Your new Hugo site is created in /Users/tonybai/MyEbook/gohugo/go-machine-learning.
Just a few more steps and you're ready to go:
1. Download a theme into the same-named folder.
Choose a theme from https://themes.gohugo.io/ or
create your own with the "hugo new theme <THEMENAME>" command.
2. Perhaps you want to add some content. You can add single files
with "hugo new <SECTIONNAME>/<FILENAME>.<FORMAT>".
3. Start the built-in live server via "hugo server".
Visit https://gohugo.io/ for quickstart guide and full documentation.
```


下面是生成的站点的初始目录结构：

```
$tree
.
└── go-machine-learning
├── archetypes
│ └── default.md
├── config.toml
├── content
├── data
├── layouts
├── static
└── themes
7 directories, 2 files
```


接下来我们来安装[gitbook theme](https://github.com/alex-shpak/hugo-book)：

```
$cd go-machine-learning
$git submodule add https://github.com/alex-shpak/hugo-book themes/book
Cloning into '/Users/tonybai/MyEbook/gohugo/go-machine-learning/hugo-book'...
remote: Enumerating objects: 3555, done.
Receiving objects: 18% (664/3555), 692.01 KiB | 4.00 KiB/s
... ...
remote: Total 3555 (delta 0), reused 0 (delta 0), pack-reused 3555
Receiving objects: 100% (3555/3555), 5.74 MiB | 5.00 KiB/s, done.
Resolving deltas: 100% (1809/1809), done.
```


我们可以修改一下顶层目录的config.toml，增加**theme=”book”**：

```
baseURL = "http://example.org/"
languageCode = "zh-cn"
title = "Go机器学习"
theme = "book"
```


启动该站点：

```
$hugo server --minify --theme book
| EN
-------------------+-----
Pages | 7
Paginator pages | 0
Non-page files | 0
Static files | 80
Processed images | 0
Aliases | 0
Sitemaps | 1
Cleaned | 0
Built in 26 ms
Watching for changes in /Users/tonybai/MyEbook/gohugo/go-machine-learning/{archetypes,content,data,layouts,static,themes}
Watching for config changes in /Users/tonybai/MyEbook/gohugo/go-machine-learning/config.toml
Environment: "development"
Serving pages from memory
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```


这时由于content目录为空，因此通过浏览器访问: localhost:1313后只能看到只有一个标题的空白页面。

我们将https://github.com/alex-shpak/hugo-book themes/book下面的样例站点的content拷贝到我们的站点中：

```
$cp -R themes/book/exampleSite/content .
$ll content
total 8
drwxr-xr-x 6 tonybai staff 192 6 27 16:36 ./
drwxr-xr-x 12 tonybai staff 384 6 27 16:35 ../
-rw-r--r-- 1 tonybai staff 1165 6 27 16:36 _index.md
drwxr-xr-x 4 tonybai staff 128 6 27 16:36 docs/
drwxr-xr-x 3 tonybai staff 96 6 27 16:36 menu/
drwxr-xr-x 7 tonybai staff 224 6 27 16:36 posts/
```


再次启动hugo server后，我们通过浏览器浏览，可以看到下面页面：

![img{512x368}](../../assets/b9ebe57e71791c30.png)


我们看到这个页面分为三栏，最左侧是站点目录栏，中间是章节内容，右侧显示的是内容中的标题结构。电子书源文件分布在content目录下，该目录的结构如下：

```
$tree -L 2 content
content
├── _index.md
├── docs
│ ├── example
│ └── shortcodes
├── menu
│ └── index.md
└── posts
├── _index.md
├── chapter_1.md
├── creating-a-new-theme.md
├── goisforlovers.md
├── hugoisforlovers.md
└── migrate-from-jekyll.md
5 directories, 8 files
```


-
_index.md是首页布局

-
menu/index.md是左侧栏的布局


其他均为文章内容源文件。如果我们要调整首页布局或左侧栏的书籍结构，我们只需调整上述两个文件即可。

## 4. 小结

我们粗略、快速对mdbook、peach和gohugo工具做了比较，三者部署时都是单二进制文件。

我们的目标是利用工具生成电子书，仅从达到这个目的难易度来看：

-
mdbook是“门槛”最低的，几乎无需配置，就能搭建出一个像模像样的类似gitbook的图书站点；

-
peach门槛较高一些，要配置的东西多一些；

-
gohugo门槛适中，但却最为灵活和强大。如果对gohugo的模板语法十分熟悉，可以定义出一套满足自己风格的电子书浏览页面风格。


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

第三部分的转义符出问题了吗？感觉文章没有完呀？

感谢提醒，已经更新。看来以后发表post后，我自己也一定要细致检查一下。

搜索 mdbook 看到的文章, 写得真好.

不过平时工作使用 pandoc, 推荐也关注下.