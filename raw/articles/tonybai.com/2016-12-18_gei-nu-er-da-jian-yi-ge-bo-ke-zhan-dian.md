---
title: 给女儿搭建一个博客站点
url: https://tonybai.com/2016/12/18/build-a-blog-website-for-my-daughter/
published: '2016-12-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 给女儿搭建一个博客站点

时光荏苒。转眼间女儿已经成为一名小学生了，依稀还记得当年[果果呱呱坠地](http://tonybai.com/2010/05/11/now-i-am-a-father/)的情景，独自回味，感慨万千。

[果果3岁](http://tonybai.com/2013/05/18/daughter-is-3-years-old/)前，都是我来[记录她的生活点滴和成长历程](http://tonybai.com/tag/女儿)，那个时候她是我们生活舞台的主角。3岁后，果果学会了说话，上了幼儿园，开始学习各种知识、技能以及各种才艺。尤其是在幼儿园中班之后，她学会了写字、组词、造句和写日记，果果完全可以自己用文字来表达自己了! 我觉得是时候让她自己来记录她的成长历程了，我和她妈妈只是辅助和指导就好了。这种想法日益迫切，尤其是果果今年上了小学后，果果的成长更快了。我觉得迫切需要给她一个平台去表达她自己和记录她的成长。传统手段不能满足需求，于是我就想到给她搭建了一个博客站点，辅助她用网络文字、图片的形式记录自6岁上学之后的成长历程。于是这个周末就花了些时间，给女儿搭了一个博客站点。

下面以“流水账”的形式，记录一下这个站点的搭建过程，也许能给和我有同样需求的家长们带来一些帮助^_^。

### 一、选型和准备工作

博客站点，我首选静态页面的。静态页面，又要快速搭建，我首选[github page](https://pages.github.com/)。github page一般情况下在国内访问相对较为稳定，访问速度也不错，ping延迟一般在100多ms，比我独立购买的[Digital Ocean的主机](https://www.digitalocean.com/?refcode=bff6eed92687)的延迟低很多。还有另外一个原因就是市面上几乎所有主流静态页面生成工具都对github pages有着不错的支持。由于采用静态页面，即便将来[迁移到VPS](http://tonybai.com/2014/11/28/migrate-blog-to-digitalocean-vps/)，也几乎是无缝的。于是给果果在github上申请了[账号](https://github.com/baisibei)。

用与搭建博客、个人站点的静态页面生成工具很多，比如：[jekyll](http://jekyllrb.com/)、[octopress](http://octopress.org/)、[hexo](https://hexo.io/)以及[hugo](http://gohugo.io/)，用哪个呢？作为[Gopher](http://tonybai.com/tag/golang)，我首选[hugo](https://github.com/spf13/hugo)。接下来，我们来看看用hugo是否能搭建出满足我们需求的基于github page的博客站点吧。

hugo的安装参考hugo github主页上的说明即可。由于hugo import了很多第三方package，有些package可能在墙外，因此配置上加速器是更好的、更快的^_^。

### 二、基于hugo搭建博客站点

去年曾写过一篇《使用Hugo搭建静态站点(http://tonybai.com/2015/09/23/intro-of-gohugo/)》，讲述如何通过[hugo](https://github.com/spf13/hugo)这个[golang](http://tonybai.com/tag/golang)开发的工具搭建一个属于自己的静态站点（static websites)。不过那篇文章并没有谈到hugo如何与github page结合。

hugo官方文档中，对[如何使用hugo创建基于github page站点](https://gohugo.io/tutorials/github-pages-blog/)有着较为详尽的描述，这是由一位名为[Spencer Lyon](https://github.com/spencerlyon2/)的外国开发者贡献的文章，并且Spencer Lyon给出hugo github page的工程template： [hugo-gh-blog](http://spencerlyon2.github.io/hugo_gh_blog)。我这里就直接使用了该工程模板，并基于hugo_gh_blog做一些定制化修改，比如“汉化”之类的。

下面是详细的步骤：

#### 1、clone hugo_gh_blog

我们首先将Spencer Lyon的hugo_gh_blog代码库clone到本地，这是我们博客搭建的基础：

```
$mkdir GuoGuoBlog
$cd GuoGuoBlog
$git clone https://github.com/spencerlyon2/hugo_gh_blog.git
Cloning into 'hugo_gh_blog'...
remote: Counting objects: 489, done.
remote: Total 489 (delta 0), reused 0 (delta 0), pack-reused 489
Receiving objects: 100% (489/489), 84.50 KiB | 24.00 KiB/s, done.
Resolving deltas: 100% (232/232), done.
Checking connectivity... done.
$cd hugo_gh_blog/
$ls
LICENSE README.md config.yaml content/ deploy.sh* static/ themes/
```


#### 2、编辑config.yaml和本地调试

进入hugo_gh_blog目录，编辑config.yaml，设置站点的一些元数据：

```
---
contentdir: "content"
layoutdir: "layouts"
publishdir: "public"
indexes:
category: "categories"
baseurl: "http://baisibei.github.io"
title: "果果的成长历程"
canonifyurls: true
theme: "Lanyon"
...
```


接下来，我们来生成我们的静态博客页面：

```
$hugo
0 draft content
0 future content
2 pages created
0 paginator pages created
2 categories created
in 48 ms
```


hugo将创建public目录，并将生成的页面放入该目录：

```
$ls public
404.html categories/ css/ favicon.ico img/ index.html index.xml posts/ sitemap.xml
```


public/index.html就是站点首页。

我们在本地可以启动hugo server，并查看生成的站点情况：

```
$hugo server -t Lanyon
0 draft content
0 future content
2 pages created
0 paginator pages created
2 categories created
in 54 ms
Serving pages from /Users/tony/GuoGuoBlog/hugo_gh_blog/public
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
```


打开浏览器，输入localhost:1313。不出意外，你就可以看到类似下面的站点：

![img{512x368}](../../assets/8fa78f8495410a68.png)


#### 3、创建github page repository

默认情况，github账号xxxx对应的github page repository是xxxx.github.io。于是我在女儿的github账号下创建public repository：baisibei.github.io。

接下来，我们需要将上步中生成的静态页面push到baisibei.github.io这个repository中。在本地进入到hugo_gh_blog/public目录下，执行：

```
$git init
$git add -A
$git commit -m"initial commit" .
$git remote add origin https//github.com/baisibei.github.io.git
$git push -u origin master
```


如果你是用自己的github账号替孩子提交，那么请在该repository下设置collaborator。

push一旦成功后，你就可以直接访问：https://xxxx.github.io查看站点页面了。我这里要访问的是baisibei.github.io。

#### 4、样式问题

问题出现了。在本地样式良好的首页，一旦push到github page上，再用浏览器（chrome）打开，我发现样式全部丢失了，首页被render为“全文字”版本。我一开始怀疑css文件路径不对或无法访问到某个css文件，通过“显示网页源代码”，单独试着访问所有css文件，发现这些文件都是可访问的。还有一个现象是：通过mac safari浏览器、手机上的ucweb、微信内置浏览器浏览，均没有样式问题，显示一切正常(Firefox、IE也均有问题)。将hugo_gh_blog放在我的VPS上，并用hugo作为web server，任何浏览器访问都是没有问题的。

针对这个问题，谷歌和度娘了半天，也没有解决掉。于是我有了换工具的想法。在搜索其他工具资料的过程中，我发现了基于hexo的[maupassant theme](https://github.com/tufu9441/maupassant-hexo)！没错，就是那个和我目前博客同源的主题：maupassant。这个主题采用响应式的设计，对不同屏幕的访问均有很好的适配。

之前我的博客为了适应智能终端的浏览，采用了WPtouch插件，效果差强人意。这次我特地停用了该插件，直接用手机访问我的博客，发现maupassant的显示效果是棒棒的。于是下一步，我将hugo更换为[hexo](https://hexo.io)，主题由Lanyon更换为maupassant。

hugo_gh_blog和baisibei.github.io依然保留在github.com上，后者的名字被rename为baisibei.github.io.using.hugo。

### 三、基于hexo搭建博客站点

#### 1、安装hexo相关工具

第一次用hexo，安装hexo过程需要一些耐心：

```
$npm install hexo-cli -g
{耐心的等待... ...}
$which hexo
/usr/local/bin/hexo
$hexo -v
hexo-cli: 1.0.2
os: Darwin 13.1.0 darwin x64
http_parser: 2.7.0
node: 6.9.1
v8: 5.1.281.84
uv: 1.9.1
zlib: 1.2.8
ares: 1.10.1-DEV
icu: 57.1
modules: 48
openssl: 1.0.2j
```


#### 2、创建blog

使用hexo init在本地创建blog repository目录：

```
$hexo init hexo_gh_blog
{耐心等待...}
... ...
INFO Start blogging with Hexo!
```


进入hexo_gh_blog目录：

```
$cd hexo_gh_blog
$ls
_config.yml node_modules/ package.json scaffolds/ source/ themes/
```


没完，我们还需要install一下相关的依赖：

```
$npm install
{耐心等待....}
```


通过”hexo g”命令生成blog文件：

```
$hexo g
INFO Start processing
INFO Files loaded in 270 ms
INFO Generated: index.html
INFO Generated: archives/index.html
INFO Generated: fancybox/blank.gif
INFO Generated: fancybox/jquery.fancybox.css
INFO Generated: fancybox/fancybox_sprite.png
INFO Generated: fancybox/fancybox_loading.gif
INFO Generated: fancybox/fancybox_overlay.png
INFO Generated: fancybox/fancybox_loading@2x.gif
INFO Generated: fancybox/jquery.fancybox.pack.js
INFO Generated: fancybox/jquery.fancybox.js
INFO Generated: fancybox/fancybox_sprite@2x.png
INFO Generated: archives/2016/12/index.html
INFO Generated: css/fonts/fontawesome-webfont.eot
INFO Generated: css/fonts/fontawesome-webfont.svg
INFO Generated: css/style.css
INFO Generated: css/fonts/fontawesome-webfont.ttf
INFO Generated: fancybox/helpers/fancybox_buttons.png
INFO Generated: css/fonts/FontAwesome.otf
INFO Generated: js/script.js
INFO Generated: fancybox/helpers/jquery.fancybox-buttons.css
INFO Generated: archives/2016/index.html
INFO Generated: css/fonts/fontawesome-webfont.woff
INFO Generated: fancybox/helpers/jquery.fancybox-media.js
INFO Generated: fancybox/helpers/jquery.fancybox-buttons.js
INFO Generated: fancybox/helpers/jquery.fancybox-thumbs.css
INFO Generated: fancybox/helpers/jquery.fancybox-thumbs.js
INFO Generated: css/images/banner.jpg
INFO Generated: 2016/12/16/hello-world/index.html
INFO 28 files generated in 867 ms
$ls
_config.yml db.json node_modules/ package.json public/ scaffolds/ source/ themes/
```


和hugo命令类似，hexo g也创建了public目录，并将站点的静态文件生成在这个目录下面。

通过hexo s可以启动一个web server，在本地查看生成的静态站点：

```
$hexo s
INFO Start processing
INFO Hexo is running at http://localhost:4000/. Press Ctrl+C to st
```


hexo自带的landscape theme真的是不咋好看。

#### 3、更换主题为maupassant

先清理一下生成文件，再clone maupassant主题：

```
$hexo clean
INFO Deleted database.
INFO Deleted public folder.
$git clone https://github.com/tufu9441/maupassant-hexo themes/maupassant
Cloning into 'themes/maupassant'...
remote: Counting objects: 1310, done.
remote: Total 1310 (delta 0), reused 0 (delta 0), pack-reused 1309
Receiving objects: 100% (1310/1310), 562.88 KiB | 382.00 KiB/s, done.
Resolving deltas: 100% (747/747), done.
Checking connectivity... done.
$ls themes/
landscape/ maupassant/
```


编辑hexo_gh_blog/_config.yml文件，修改theme为：maupassant

```
//_config.xml
theme: landscape
=>
theme: maupassant
```


重新生成站点静态文件之前，我们还需要安装下面两个工具，否则hexo生成出来的静态页面也是不可用的：

```
$ npm install hexo-renderer-jade --save
$ npm install hexo-renderer-sass --save
```


hexo g和hexo s后，你就可以在本地：localhost:4000地址上看到生成的静态页面了：

![img{512x368}](../../assets/81b715bee406cfdc.png)


仿效上面章节中的步骤，将public目录push到baisibei.github.io repository中，看看我们上传后的站点通过公网访问是否还有“失真”现象，结果：一切正常。

#### 4、定制站点

##### a) 定制hexo_gh_blog/_config.yml

这个_config.xml中的配置都是站点全局范畴的，这里仅我将我修改过的一些定制属性贴出来：

```
# Site
title: Amy Bai
subtitle: 果果的成长历程
description: 记录一个小女孩儿在学习、生活、家庭、情感方面的成长经历
author: Amy Bai
language: zh-CN
timezone: Asia/Shanghai
since: 2016
avatar: https://avatars0.githubusercontent.com/u/24524343?v=3&s=400
# URL
## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
url: http://daughter.tonybai.com
```


默认情况下，maupassant主题的menu中包含rss菜单项（站点的订阅feed），对应的访问路径是/atom.xml，但要生成atom.xml，需要安装另外两个plugins：hexo-generator-feed和hexo-generator-sitemap：

```
在_config.xml中添加：
plugins:
- hexo-generator-feed
- hexo-generator-sitemap
安装这两个插件；
$npm install hexo-generator-feed --save
hexo-site@0.0.0 /Users/tony/GuoGuoblog/hexo_gh_blog
└── hexo-generator-feed@1.2.0
$npm install hexo-generator-sitemap --save
hexo-site@0.0.0 /Users/tony/GuoGuoblog/hexo_gh_blog
└── hexo-generator-sitemap@1.1.2
```


安装后，执行hexo g，会看到atom.xml的生成。不过由于hexo版本似乎与feed插件有兼容性问题，当执行hexo s时，命令报错。我暂时在_config.xml中先注释掉这两个插件，待后期看是否能解决，不过这不影响站点的主要功能。

##### b) about页面

在maupassant主题的menu中默认还包含了about菜单项，但在生成的站点静态页面中点击about菜单项，将返回失败页面。如何给站点添加about页面呢？

在hexo_gh_blog/source下创建about目录，进入about目录，创建index.md文件，内容诸如：

```
---
title: 关于我
---
我是Amy Bai，小名果果。
```


这样hexo g和hexo s后，你就有about页面可供访问了。

#### 5、写post

hexo通过hexo new 命令来创建一篇post，我更喜欢简单粗暴，直接再hexo_gh_blog/source/_post创建一个xxx.md文件，这就是一篇post。post内的markdown格式和很多工具都是类似的：

```
以initial-post.md为例：
---
title: "第一篇（待写）"
date: "2016-12-15"
description: "第一篇博文，敬请期待^O^"
categories:
- "日记"
- "感悟"
---
## 标题一
第一篇文章，敬请期待
### 子标题
## 小结
^O^
```


hexo按md文件头中的date对post进行排序。title就是显示在文章中的标题。description是文章摘要。默认情况下，maupassant主题在首页只是展示文章摘要而不是全文。

### 四、域名绑定

还没有申请顶级域名下的二级域名，目前打算绑定daughter.tonybai.com这个子域名。怎么做呢？

在public目录下，创建CNAME文件，文件内容：daughter.tonybai.com。然后将文件Push到github上去。

在你的域名管理站点，创建”daughter.tonybai.com”子域名，并将其CNAME值设置为”baisibei.github.io”。生效后，打开浏览器，访问”daughter.tonybai.com”，你就可以看到你刚刚生成的新站点了。

### 五、小结

站点搭建好了！用各种终端访问，感觉效果还不错。post发布也很方便，如果你想自动发布，定义一下hexo deploy即可。我个人习惯手动提交，也就没这个步骤了。

接下来，把内容创作的任务就交给果果了^_^。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

正在学习做博客，就翻到了采用同样主题的博客，你的女儿好可爱n(*≧▽≦*)n现在我只能对博客内容进行丰满，还要继续学习对主题的优化和修改，希望能向你学习。

给女儿点赞，好可爱+1