---
title: 开始使用Markdown写Blog
url: https://tonybai.com/2015/09/19/write-blog-in-markdown/
published: '2015-09-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 开始使用Markdown写Blog

近期发了一些带有大量代码的[Go技术文章](http://tonybai.com/2015/09/17/7-things-you-may-not-pay-attation-to-in-go/)，结果文章中的代码样式被大家鄙视了，比如评论中的“不忍直视”、“这代码看得让人难受”等。于是我决定花些时间尝试做些改变。

### 博客系统

目前使用的这个博客系统是放在[DigitalOcean VPS](https://www.digitalocean.com/?refcode=bff6eed92687)的Wordpress 3.2.1。在[迁移到VPS](http://tonybai.com/2014/11/28/migrate-blog-to-digitalocean-vps/)之前，我的博客是一直托管在同事的一个托管主机上的，当初[从blogbus迁移到他的托管WordPress主机](http://tonybai.com/2012/02/29/a-new-departure-of-my-blog-move-from-blogbus-to-wordpress/)时使用的就是WordPress 3.2.1版本，这两年一直未动，目前WordPress版本都4.3.1了。WordPress 3.2.1有很多bug，尤其是其安全漏洞，[今年就被黑过几次](http://tonybai.com/2015/04/12/fix-hacked-blog-site/)，为此在后台将blog纳入git version管理，这样被黑后就可以很容易恢复。但将版本升级到WordPress新版我还是担心的，主要是担心升级失败，尤其是>数据库表变化较大，担心无法恢复。

不过由于历史“负重”太大（900多篇），我很难将WordPress顺利平滑的切换到一些新博客系统，比如golang开发的[hugo](http://gohugo.io/)，[Jekyll](http://jekyllrb.com/)、[Octopress](http://octopress.org/)等，只能继续坚守WordPress。

由于经常在文章里贴代码，也曾尝试过使用一些语法高亮的插件，但目前使用的富文本编辑器CKEditor似乎总是与语法高亮不兼容，试了N多都不好用，尤其是在html编辑器和富文本编辑器切换时高亮>部分代码内容被自动转码，于是放弃。这样在文章中只能暂时用Courier New字体来“高亮”代码部分。

### Crayon Syntax Highlighter

在尝试之初思路主要还是想找到一款与CKEditor兼容的好用的语法高亮插件，在网上找到一个插件组合：*CKEditor + SyntaxHighlighter CKEditor Button + Auto-SyntaxHighlighter*。安装后简单>测试了一下发现的确比之前找的几款插件强。输入代码时只需要点击CKEditor工具栏上的一个Code Button，SyntaxHighlighter CKEditor Button会打开一个源码输入对话框，选择源码的语言种类贴入源码即可，还可以在”高级”tab中设置一些选项，是否带行号等。这个组合最大的好处就是无需切换到html编辑器手工输入html tag。

不过测试一段时间后还是发现了这个插件组合的问题，那就是不支持Go语法。Auto-SyntaxHighlighter内部使用的是syntaxhighligter的js，后者已经停止更新，并且即便是最新版本也不支持golang。我只能[fork一个Auto-SyntaxHighlighter](https://github.com/bigwhite/Auto-SyntaxHighlighter)的repo，并“照猫画虎”的Auto-SyntaxHighlighter增加Go语法文件:shBrushGo-min.js和shBrushGo.js，并修改SyntaxHighlighter CKEditor Button的js文件，增加Go选项。不过try后，发现高亮格式依旧不对，最初以为是我修改的不正确，后来发现即便是用其支持的C/C++代码，高亮格式依旧有问题，我怀疑是与我当前的[theme](https://github.com/pagecho/maupassant)不兼容所致。

在知乎上看到人们都推荐[Crayon Syntax Highlighter](https://github.com/aramk/crayon-syntax-highlighter)这个语法高亮插件，于是想最后再尝试一下。安装后发现Crayon Syntax Highlighter的确强大，我将字体设置为monaco, 字号14，主题：monokai，其渲染出来的高亮代码和我在本地mac上的几乎一模一样。不过小问题还是有的，比如: 行号无法去掉，浮动工具栏不好用等。

Crayon插件的最大的问题还是使用不便：需要切换到html源码editor中手工加入：

`<pre lang:"go"> </pre>`


如果再切换到富文本编辑器后，再切回来，

`<pre> </pre>`


之间的文本就会被转码，这极大增加了使用门槛。在没有理想办法之前，只能将就着用吧。

以上已经让我折腾我几个小时了，凌晨一点，睡。

### Markdown on Save Improved

早上醒来，想到了[Markdown](http://daringfireball.net/projects/markdown/)，也许是最后稻草了。以前一直以为WordPress版本较低，很多Markdown plugin都不支持。但今天先不管那些了，装上试试。我找到了[Markdown on Save Improved](https://wordpress.org/plugins/markdown-on-save-improved/)，这款插件最大的好处就是可以在每篇文章级别上加markdown开启选项。目前该插件已>经停更，并且其作者基于该插件开发了”Jetpack’s Markdown module”，[Jetpack](https://wordpress.org/plugins/jetpack/)太大，对WordPress版本要求也太高，于是我就选择了”Markdown on Save Improved”，满足我使用就可以了。安装插件后，有一个“Markdown on Save Improved Convert to Jetpack”提示，似乎点击一个按钮，就可以将该插件转换为”Jetpack’s Markdown module”，不过我>也不能肯定，因为从表面上看不出来，没有什么变化。

“Markdown on Save Improved”给我的最大惊喜是它居然兼容Crayon Syntax Highlighter，我将Crayon的默认语言设置为go，这样markdown标记的代码块后者渲染后展现出很理想的高亮效果。

```
package main
import "fmt"
func main() {
fmt.Println("Hello, MarkDown and SyntaxHighlighter")
}
```


至于Markdown的预览，可以在[stackedit.io](https://stackedit.io/editor)上来做。

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论