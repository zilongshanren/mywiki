---
title: 使用Hugo搭建静态站点
url: https://tonybai.com/2015/09/23/intro-of-gohugo/
published: '2015-09-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Hugo搭建静态站点

虽然前一篇Blog宣称自己要[用Markdown开始写Post](http://tonybai.com/2015/09/19/write-blog-in-markdown/)，但实际操作起来还是发现了诸多不兼容问题(插件与主题间、插件与插件间的)，让编写和修改文章变得十分繁琐，于是我研究了一下静态Web站点生成工具[Hugo](http://gohugo.io/)。Hugo是由前[Docker](https://www.docker.com)的重量级员工(2015年8月末从Docker离职)：[Steve Francia](https://github.com/spf13)实现的一个开源静态站点生成工具框架，类似于[Jekyll](http://jekyllrb.com/)、[Octopress](http://octopress.org)或[Hexo](http://hexo.io/)，都是将特定格式(最常见的是Markdown格式)的文本文件转换为静态html文件而生成一个静态站点，多用于个人Blog站点、项目文档(Docker的官方manual Site就是用Hugo生成的)、初创公司站点等。这类工具越来越多的受到程序员等颇具“极客”精神的群体的欢迎，结合github.com等版本控制服务，采用具有简单语法格式但强大表达力的Markdown标记语言，人们可以在很短时间内就构建出一个符合自己需求的静态Web站点。在这些工具中，Hugo算是后起之秀了，它最大的优点就是Fast! 一个中等规模的站点在几分之一秒内就可以生成出来。其次是良好的跨平台特性、配置简单、使用方便等。这一切均源于其良好的基因：采用Go语言实现。Steve Francia除了Hugo平台自身外，还维护了一个[Hugo Theme](https://github.com/spf13/hugoThemes)的Repo，这个Hugo主题库可以帮助Hugo使用者快速找到自己心仪的主题并快速搭建起静态站点。目前国内使用Hugo的人还不多，但感觉其趋势是在逐渐增多。这里写下这篇Post，也算是为大家入个门，引个路吧。

### 一、安装Hugo

[Hugo托管](https://github.com/spf13/hugo/)在github.com上，因此获取Hugo很方面，目前有至少两种方法可以安装Hugo。

#### 1、安装包

对于普通用户（无git、无开发经验）而言，直接下载安装包是最简单的方式。我们可以下载Hugo的[Release版](https://github.com/spf13/hugo/releases)，截至目前为止最新版本是v0.14，可以在[这里](https://github.com/spf13/hugo/releases/tag/v0.14)下载你的平台(支持linux, windows, darwin, netbsd, freebsd和arm等)对应的版本。不过我发现0.14版本似乎有Bug，在我的MacOsX上生成Hugo Docs站点总是panic。

#### 2、源码编译

对于开发者而言，源码编译是最Geek的方式:

```
go get -u -v github.com/spf13/hugo
go build -o hugo main.go
mv hugo $GOPATH/bin
```


在命令行下执行hugo命令，如果得到类似下面结果，则说明你已经成功安装了Hugo：

```
$hugo version
Hugo Static Site Generator v0.15-DEV BuildDate: 2015-09-20T23:53:39+08:00
```


### 二、生成静态站点

#### 1、创建静态站点

我们来创建一个名为”tonybai.com”的静态站点：

```
$hugo new site tonybai.com
$tree
.
└── tonybai.com
├── archetypes
├── config.toml
├── content
├── data
├── layouts
└── static
```


我们看到，通过hugo new site命令，我们建立了tonybai.com站点的后台目录结构。但细心的你会发现：这里的目录都是空的。除了config.toml中可怜的三行内容：

```
baseurl = "http://replace-this-with-your-hugo-site.com/"
languageCode = "en-us"
title = "My New Hugo Site"
```


不过即便目录为空，这也是一个完整的静态站点源文件，我们可以基于这些文件生成我们的站点。

```
$cd tonybai.com
$hugo server
0 draft content
0 future content
0 pages created
0 paginator pages created
0 tags created
0 categories created
in 6 ms
Serving pages from /Users/tony/test/hugotest/tonybai.com/public
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```


上面的hugo命令在将repo转换为静态Site文件放入public目录：

```
├── public
│ ├── 404.html
│ ├── index.html
│ ├── index.xml
│ └── sitemap.xml
```


之后Hugo启动了一个server作为该Site的Web Server。通过浏览器访问http://localhost:1313，你将看到一个完全空白的站点首页。虽然这个站点没啥实用价值（一片空白），但这却是一个良好的起点。

#### 2、添加Theme

添加了Theme后的站点才有血有肉，丰富多彩。

添加Theme的步骤如下，我们以Hyde Theme为例：

首先创建themes目录，并下载Hyde Theme文件：

```
$ mkdir themes
$ cd themes
$ git clone https://github.com/spf13/hyde.git
```


接下来，我们需要对Site进行一些配置，tonybai.com/config.toml是Site的顶层配置文件，配置后的config.toml文件如下：

```
baseurl = "http://tonybai.com/"
languageCode = "en-us"
title = "Tony Bai"
theme = "hyde"
[params]
description = "这里是Tony Bai的个人博客"
themeColor = "theme-base-08" # for hyde theme
```


其中：

theme = “hyde” 指定站点使用Hyde主题；

themeColor = “theme-base-08″ 指定了站点的主题颜色（默认是黑色的，这里改成一种红色）

在tonybai.com目录下重新执行hugo server，并打开浏览器查看站点首页，你会发现视野里有内容了：

![站点截图1](../../assets/8370bd0e82ba3491.jpg)


#### 3、第一个Post

结构和样式有了，我们还没有内容。我们来创建站点的第一个Post：

```
$hugo new welcome.md
/Users/tony/Test/hugotest/tonybai.com/content/welcome.md created
```


hugo在content下创建welcome.md文件，我们编写一些文件内容：

```
+++
Categories = ["Development", "GoLang"]
Description = ""
Tags = ["Development", "golang"]
date = "2015-09-23T16:30:37+08:00"
menu = "main"
title = "你好，Hugo"
+++
这是使用Hugo创建的站点中的第一篇文章。
```


保存后，重新执行hugo server命令，打开浏览器，你将看到下面的情形：

![站点截图2](../../assets/625c925d0b5063f7.jpg)


至此，如果你是极简主义者，你对其他没有任何要求，你就可以用这个站点写Post了。

### 三、调试与部署站点

#### 1、调试站点

采用Hugo的静态站点在编辑文章、调试站点时十分方便，你要做的就是编辑文本，保存后，打开浏览器看渲染后的结果。不过反复执行hugo server命令还是有些烦，hugo早想到了这一点，hugo提供了:

`-w, --watch[=false]`


执行hugo server命令时加上-w选项，hugo就可以自动检测本地站点文件的变更，并自动执行md -> html转换。这样刷新浏览器页面就可以看到你修改后的结果了：

```
$hugo server -w
0 draft content
0 future content
1 pages created
0 paginator pages created
2 tags created
2 categories created
in 16 ms
Watching for changes in /Users/tony/test/hugotest/tonybai.com/{data,content,layouts,static,themes/hyde}
Serving pages from /Users/tony/test/hugotest/tonybai.com/public
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```


通过hugo server -w的输出日志来看，hugo可以自动检测data,content,layouts,static,themes/hyde目录下的变更，但站点顶层config.toml的改动无法被检测，还需要重启hugo server。

#### 2、部署站点

和Jekyll类似，使用hugo的静态站点可以部署到github page中，不过这里不详细描述这种方法，可以看[官方文档](http://gohugo.io/tutorials/github-pages-blog/)

如果是在vps下部署，那么hugo转换后的public文件夹可以被直接用于部署到像nginx、apache、[caddy](http://tonybai.com/2015/06/04/caddy-a-web-server-in-go/)这样的Web Server下面。

当然hugo本身也可以作为一个Web server来支撑你的静态站点，就像上面提到的，你可以在你的站点目录(比如上面的”tonybai.com”)下执行：

```
$sudo hugo server --bind="0.0.0.0" -v -w -p 80 -b http://tonybai.com
```


如果无法使用80端口（比如通过apache2反向代理），那么需要加上–appendPort=false，否则转换后的public下面的url地址都会带上你的hugo端口（1313）：

```
$hugo server -v -w -p 1313 -b http://tonybai.com --appendPort=false
```


### 四、配置和维护站点

大多数人不会止步于上面那个仅仅能写Post的站点，配置分类、标签；修改字体样式；添加评论功能；增加统计代码；增加代码高亮(程序员最爱)；甚至定制主题是Geek们最喜欢折腾的事情，这里无法全表，列举几个常见的配置和维护方法，还是已hyde主题为例。

#### 1、配置分类、标签

在浏览器中输入：http://localhost:1313/categories/或http://localhost:1313/tags，你会看到站点输出了一个类似目录列表似的页面：

```
development/
golang/
```


development和golang从何而来呢？

隐藏得再深，也要给它揪出来：

```
tonybai.com/themes/hyde/archetypes/default.md
+++
Description = ""
Tags = ["Development", "golang"]
Categories = ["Development", "GoLang"]
menu = "main"
+++
```


由于我们使用了hyde theme，所以我们只需看themes/hyde下面的目录结构即可，tonybai.com下面的除content之外的其他layout, data等可忽略不计。在hyde/archetypes下存放着这个主题下文章的默认分类和tags集合。这个default的作用是每次new post后，hugo会将default中的tags和categories自动copy到Post头中的tags和categories中。

每个Post的分类和tag在post自身的.md文件头中指定，见Categories和Tags两个配置项：

```
tonybai.com/content/welcome.md
+++
Categories = ["Development", "GoLang"]
Description = ""
Tags = ["Development", "golang"]
date = "2015-09-23T16:30:37+08:00"
menu = "main"
title = "你好，Hugo"
+++
```


你可以根据需要在你的post md文件中灵活增删你的tags和categories，不局限于default.md中的那些已知项。

#### 2、修改字体样式

hyde主题的字体样式在tonybai.com/themes/hyde/layouts/partials/head.html中指定：

```
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=PT+Sans:400,400italic,700|Abril+Fatface">
```


由于googleapis在国内无法访问，因此要么注释掉这行（使用浏览器默认字体样式），要么将其换为其他字体公共服务，比如：

```
<link rel="stylesheet" href="http://fonts.useso.com/css?family=PT+Sans:400,400italic,700|Abril+Fatface">
```


字体的设置在tonybai.com/themes/hyde/static/css下的各个css文件中，谨慎调整。

#### 3、添加评论功能

Hugo没有内置评论功能，要增加评论功能需要集成第三方评论服务，比如国外最流行的[Disqus](https://disqus.com)。hyde主题内置了disqus评论插件，不过需要你按如下操作配置一下，否则页面下方的disqus插件总是显示无法连接。

##### 获取disqusShortname

这里用disqus主账号不行，需要用主账号login后：*add a newsite to disqus*，比如加入tonybaicom.disqus.com，这样你的disqusShortname就为：tonybaicom；

##### 配置disqusShortname

在tonybai.com/config.toml中配置disqusShortname:

```
[params]
disqusShortname = "tonybaicom"
```


如果你要使用国内的评论服务，比如：[多说](http://duoshuo.com/)，你可以参考tonybai.com/themes/hyde/layouts/partials/disqus.html，用多说提供的install code替换disqus的code，形成duoshuo.html：

```
<!-- 多说评论框 start -->
<div class="ds-thread" data-thread-key="{{ .URL }}" data-title="{{ .Title }}" data-url="{{ .Permalink }}"></div>
<!-- 多说评论框 end -->
<!-- 多说公共JS代码 start (一个网页只需插入一次) -->
<script type="text/javascript">
var duoshuoQuery = {short_name:"{{.Site.Params.duoshuoShortname}}"};
(function() {
var ds = document.createElement('script');
ds.type = 'text/javascript';ds.async = true;
ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
ds.charset = 'UTF-8';
(document.getElementsByTagName('head')[0]
|| document.getElementsByTagName('body')[0]).appendChild(ds);
})();
</script>
<!-- 多说公共JS代码 end -->
```


再在tonybai.com/themes/hyde/layouts/_default/single.html中替换下面的代码：

```
{{ if and (isset .Site.Params "disqusShortname") (ne .Site.Params.disqusShortname "") }}
<h2>Comments</h2>
{{ partial "disqus" . }}
{{ end }}
```


为类似下面的代码：

```
{{ if and (isset .Site.Params "duoshuoShortname") (ne .Site.Params.duoshuoShortname"") }}
<h2>Comments</h2>
{{ partial "duoshuo" . }}
{{ end }}
```


注意：一旦用上面多说代码，config.toml中就需要配置duoshuoShortname了：

```
[params]
duoshuoShortname = "tonybaicom"
```


#### 4、代码高亮

Hugo官方说明中采用Pygments来进行[代码高亮](http://gohugo.io/extras/highlighting/)的支持，在部署机上安装Pygments，个人觉得这个方法不好。于是换另一外一种js代码法，即采用[highlightjs](http://highlightjs.org)的方法支持代码高亮。

highlightjs同样很强大，支持135种语言（关键是支持Golang）和60多种样式（有我喜爱的github样式和monokai_sublime样式），但不支持linenumber。

我们首先将highlightjs下载到本地:

```
tonybai.com/themes/hyde/static/css/highlight.js/8.8.0/styles/github.min.css
tonybai.com/themes/hyde/static/js/highlight.js/8.8.0/highlight.min.js
```


然后在tonybai.com/themes/hyde/layouts/partials/head.html添加如下代码:

```
<!-- Highlight.js and css -->
<script src="{{ .Site.BaseURL }}js/highlight.js/8.8.0/highlight.min.js"></script>
<link rel="stylesheet" href="{{ .Site.BaseURL }}css/highlight.js/8.8.0/styles/github.min.css">
<script>hljs.initHighlightingOnLoad();</script>
```


highlightjs会自动检测语言类型，并使用github样式。

#### 5、统计代码

提供统计服务的站点，比如statcounter.com一般都会提供安装代码（js）的，将那段代码copy到tonybai.com/themes/hyde/layouts/partials/head.html中即可。

### 四、进阶

#### 1、index.html、single.html和list.html

站点的首页模板在themes/hyde/layouts/index.html中。除首页外，其他Post或叫Page，都被Hugo抽象为两类：单体页面和列表页面，对应这两种页面的默认模板都在themes/hyde/layouts/_default中，分别对应着single.html和list.html。

我们之前通过hugo new welcome.md创建的Post使用的是single.html模板，而查看tags或categories的页面默认采用的是list.html，比如查看tonybai.com/categories/golang，你会在浏览器中看到分类在golang这一类的所有Post列表。

#### 2、type和section

我们执行如下两个命令：

```
$hugo new post/firstpost.md
tonybai.com/content/post/firstpost.md created
$hugo new post/secondpost.md
tonybai.com/content/post/secondpost.md created
```


创建后我们可以看到站点的源文件结构变成了：

```
... ...
├── archetypes
├── config.toml
├── content
│ ├── post
│ │ ├── firstpost.md
│ │ └── secondpost.md
│ └── welcome.md
... ...
```


hugo中源码文件的布局影响着最终生成的html文件的结构布局。有些时候我们的站点可能会分成若干个部分，每部分通过目录隔离开，比如这里content下的post目录，这样hugo转换后，firstpost.html和secondpost.html也会在public的post目录下。这里的“post”被称为一个section。

hugo会为每个section自动生成index.html页，采用的是index.html模板。

至于是否采用的是hyde/layouts/_default下的list.html，这要看host的匹配order，官方给出的是：

```
/layouts/section/SECTION.html
/layouts/_default/section.html
/layouts/_default/list.html
/themes/THEME/layouts/section/SECTION.html
/themes/THEME/layouts/_default/section.html
/themes/THEME/layouts/_default/list.html
这个例子中THEME=hyde, SECTION=post
```


在本例子中，/layouts/下是空的，不予考虑。/themes/hyde/layouts下没有建立section/post.html模板，/themes/hyde/layouts/_default/section.html也不存在，因此用的是_default/list.html。

hugo官方建议静态站点源码文件按section组织，每个section使用相应(同名）的type，这样section下面的.md就会自动使用响应type的meta data。

当我们hugo new post/firstpost.md时，hugo会到archetypes下找是否有post.md文件，如果有则使用post.md文件的categories和tags来初始化content/post/firstpost.md的元数据，如果没有post.md，则使用archetypes/default.md的。

#### 3、模板语言

Hugo使用Golang的模板语法，表达能力很强大；配合Hugo predefined的变量或自定义变量，你可以玩转模板。关于模板内容较多，这里不赘述，需要时查看[官方详细的manual](http://gohugo.io/templates/go-templates/)。

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

好文章，希望Hugo能继续赶超hexo

[悼念乔布斯] 谢谢，用到了~~~~~~~~~~~~~~~~~~~~

谢谢，用到了~~~~~~~~~~~~~~~~~~~~

谢谢，用到了~~~~~~~~~~~~~~~~~~~~

写得好！可是为啥你还在用wordpress呢？

这个原因很复杂。记得当时应该是没找到合适的theme。后来blog文章日益增多，就懒得迁移了。:)

首页能把文章加入 阅读更多 功能么。。。 直接全铺出来，太影响阅读体验了~ 还有，博客带宽多少啊。。 打开慢死了。。。 继续求golang好文章~

使用 .Summary 默认显示前 70 个字符。

hello. 怎么设置这个.Summary 来更改默认显示字符的数量？

ok 解决了 。在文章需要切断的地方 直接添加

路过。。。这是一个非常勤快的程序员，鉴定完毕

非常感谢，这篇文章也让我用上了hugo，博主用心了。

heighlightjs 如何把代码字体设置成Monaco

试试在head.html中加入：

link rel=”stylesheet” href=”{{ .Site.BaseURL }}css/highlight.js/8.8.0/styles/monokai_sublime.min.css”

其中monokai_sublime.min.css要从highlight.js官方下载。

[给力] 不错，支持一下！

感谢，试用中。。。

为什么我按你的修改用不了多说！也上不了语法高亮！是hugo更新过了吗

文章有错误，误导啊！params下的参数都会自动转小写，浪费我时间。

怎么在博文中插入图片？

Markdown格式的文件插入图片都是这样的吧：![图片描述](image_url)，例如：![我的小苹果](http://tonybai.com/demo/my-apple.jpg)

Dear bigwhite :感谢你的回复，我刚刚学习HUGO很多地方都有些不明白，我想问下，当你搭建完后，建立第一个POST页面后，网页是不显示的，白色的，也就是说关健代码还在于“主题”中，主题起到了关健转换作用，我就想了解下，转换的原理，想一步步自已写，页面丑点没关系，主要是想了解原理。请给予指点下，感谢

这方面可能没法继续帮助你了。我当时也只是一个入门级用户。hugo好久没有使用了。建议去看看gohugo的官方doc吧。

东网好像在东大隔壁吧? 路过。

嗯。东大和东网是邻居。隔着一条小马路。

主页出不来。。。。不知道怎么解决。。。。

有没想过用Travis CI 部署hugo

请问你的评论功能用的什么插件？

Hugo内置支持的评论系统是disqus。之前实验hugo时用的是国内的duoshuo，不过duoshuo已经关站了。好久不用hugo了。我看目前hugo支持的comments插件也很多啊。官方manual上提到的就有：Static Man、txtpen、IntenseDebate、Graph Comment、Muut、isso (Self-hosted, Python)。第三方的服务总是不靠谱。如果有vps，建议还是选择self-hosted的吧，比如：isso。

为什么有的皮肤用不成诶…会出现大段的提示；

官网上的那个流程走过之后本地有皮肤，但是推到hub上面就没有皮肤了，会变成几行字放在那里….

有什么比较系统化各个部分都会教学的么，做博客已经用了我快整个周末的时间了…