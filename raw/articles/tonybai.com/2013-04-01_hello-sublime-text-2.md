---
title: Hello，Sublime Text 2
url: https://tonybai.com/2013/04/01/hello-sublime-text-2/
published: '2013-04-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Hello，Sublime Text 2

用惯了[Vim](http://tonybai.com/2008/12/30/in-depth-study-vim/)后，也会有一种尝试新Editor的冲动，这回[Sublime Text 2](http://www.sublimetext.com/2)满足了我的这个需求。据说Sublime Text是目前最火的代码编辑器之一，我周围为数不多的几个比较Geek的同事都已经开始使用Sublime Text 2或用了很长时间了，其官方网站首页的Feature Demo也的确非常地炫。

**安装Sublime Text 2**

我的实验环境[Ubuntu 12.04.1](http://tonybai.com/2012/12/04/upgrade-ubuntu-to-1204-lts/) 32-bit Desktop版，默认Ubuntu Unity桌面，iBus拼音输入法。

Sublime Text 2的安装极其简单，遵循着download（http://www.sublimetext.com/2） -> unzip -> add path -> start and use的经典路线。我下载的Sublime Text 2是2.0.1版本，启动后一切正常。

**安装后目录结构**

安装后的Sublime Text 2的目录结构非常简洁：

$ ls

Icon/ PackageSetup.py Pristine Packages/

lib/ sublime_plugin.py sublime_text*

lib下是自带的Python26环境；Pristine Packages下是各种编程语言的插件包。

在我的环境下Sublime Text 2的用户配置与包环境放在了~/.config/sublime-text-2/下面，

$ ls

Installed Packages/ Packages/ Pristine Packages/ Settings/

这里面最重要的目录就是Packages目录了，这里是Sublime Text 2用第三方包扩展自身Feature的包存储路径。

**安装package control**

package control包之于Sublime Text 2就好比apt工具之于Ubuntu，它是一个方便第三方包安装、卸载和管理的第三方包。在其官网(http://wbond.net/sublime_packages/package_control)上明示了其安装方法：

* 敲入 ctrl + ` 调出命令行窗口

* 在命令行窗口中输入下面的代码，回车执行。

import urllib2,os; pf='Package Control.sublime-package'; ipp=sublime.installed_packages_path(); os. makedirs(ipp) if not os.path.exists(ipp) else None; urllib2.install_opener(urllib2.build_opener(urllib2. ProxyHandler())); open(os.path.join(ipp,pf),'wb').write(urllib2.urlopen('http://sublime.wbond.net/'+pf.replace(' ','%20')).read()); print('Please restart Sublime Text to finish installation')

* 重启Sublime Text 2。

注意：如果需要代理访问外网的话，需要正确设置[http_proxy](http://tonybai.com/2012/11/21/setup-http-proxy-with-squid/)环境变量。

敲入"ctrl + shift + p"可打开命令窗口，输入"Package Control"，你会看到窗口下拉提示中Package Control支持的功能，常用的我们会选择：“Package Control: Install Package”。

**安装中文支持**

中国程序员每每在尝试一种国外程序员新开发的编辑器时，都会遇到[中文字符集编码](http://tonybai.com/2009/09/28/also-talk-about-vim-charset-configuration/)的问题，这次Sublime Text 2也不例外，它原生就不支持中文显示。还好中国程序员是无比聪明的，开发了[ConvertToUTF8](https://github.com/seanliang/ConvertToUTF8)这样的第三方包，让我们可以看到中文并用中文编辑。

最简单的安装ConvertToUTF8的方法就是用Package Control安装，选择Package Control: Install Package后，搜素ConvertToUTF8，找到后，点击即可安装。安装后，你会在~/.config/sublime-text-2/Packages下面看到ConvertToUTF8包目录。

再次启动Sublime Text 2后，打开一个GBK编码的中文文档，居然提示ConvertToUTF8工作不正常。后发现ConvertToUTF8主页上有提示，Python 2.6下的ConvertToUTF8需要一个[Codecs26](https://github.com/seanliang/Codecs26)的Package才能正常运行。下载Codecs26后，解压安装到Packages下面，重新启动Sublime Text 2，Sublime Text 2直接dump core。从Packages目录下将Codecs26删除后，Sublime Text 2恢复正常。

又细致读了ConvertToUTF8作者的README文件，发现master branch上的Codecs26是for 64位版本的，我需要下载x32 branch上的包。的确，下载并安装x32 branch上的Codecs26后，Sublime Text 2启动OK，转换中文OK了。

注意：不要与其他支持GBK转换的包（比如GBK Encoding Support）混用，否则ConvertToUTF8无法works。

**解决中文输入问题**

好不容易能看GBK编码的中文文件了，却发现无法输入中文，无论如何切换输入法和重启输入法，都无法输入中文。网上介绍可通过"Input Helper Package（cd .config/sublime-text-2/Packages; git clone http://github.com/xgenvn/InputHelper.git）"解决问题。问题的确可以解决，不过输入中文时太麻烦了：需要先敲入"ctrl+shift+z"调出中文输入框，再在这个框里输入中文。

网上都说这是iBus输入法与Sublime Text 2的兼容问题，要想解决就要换[fcitx](http://www.fcitx.org)。以前用过fcitx感觉默认输入法比较弱，不过现在fcitx有google pinyin了，体验一定会提高不少。通过下面命令一键安装fcitx：

sudo apt-get install fcitx fcitx-googlepinyin

安装后，在“语言支持”中用fcitx替换掉iBus。在“启动应用程序”中加入：

名称: Fcitx

命令: /usr/bin/fcitx -d

注释t: Fcitx启动

注销再登录后，再打开Sublime Text 2，终于可以输入中文了。

**功能**

用了一遭儿，Sublime Text 2最吸引我的Feature包括：“Goto Anything”和“Multi-Selection”。在一个工程中，通过ctrl + p调出一个输入框，Sublime Text 2首先在文件名级别对你输入的文本进行匹配；待选择好文件后，继续输入@，可看到下拉列表中显示这个文件中所有函数名的名称列表；如果输入的是#，那么下拉列表中将显示该文件中的所有符号。选择某个函数名或符号后，光标将停留在某个符号上，这时我们可以用Multi-Selection这个功能了，如果你要将这个文件中同名符号全选出来，直接Alt+F3即可；如果要选择接下来的N个同名符号，那么敲入N次ctrl + D即可。

不过要想实现[ctags](http://tonybai.com/2009/02/23/solve-some-problems-when-using-cscope/)那种在符号上跳转到符号定义或符号调用者的功能，Sublime Text 2还无法原生支持，可考虑安装Sublime Text 2的Ctags插件实现：直接在Packages目录下git clone https://github.com/SublimeText/CTags.git。之后：

- “ctrl +t, ctrl+ r"会重新生成tags文件(前提：系统内安装了ctags程序)

- "ctrl +t, ctrl + t"会跳到光标所在符号的定义处;

- "ctrl + t, ctrl + b"会跳回上次的位置;

**感受**

Sublime Text 2给我的最大感受就是“快”！你在搜索、切换符号、选择文件列表中文件或符号的同时，整个文件会同步的展现你的屏幕上。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我是编程小白，但是我用sublimeText2. 这东西确实好。我没有感觉到什么中文支持问题嘛，现在手头上用mac，读取和输入中文都很正常。我没有对sublimeText做过什么特殊设置。回头有空去linux上试试来到您博客的原因是因为正在看您的7周7语言，多看上买的。翻译是个辛苦活，没什么钱还常招人骂，我得感谢您一下

想用，但是又不想换输入法。我用的是ibus，用习惯了。