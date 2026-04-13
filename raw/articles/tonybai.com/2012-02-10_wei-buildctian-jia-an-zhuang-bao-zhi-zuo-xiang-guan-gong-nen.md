---
title: 为buildc添加安装包制作相关功能
url: https://tonybai.com/2012/02/10/add-packing-feature-to-buildc/
published: '2012-02-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 为buildc添加安装包制作相关功能

在"[也谈C应用安装包制作与部署](http://tonybai.com/2012/02/01/also-talk-about-c-app-install-package-making-and-deploying/)"一文中，我提到了为每一个源码工程建立单独的安装包制作工程(setup project)的想法，这两天我就一直在折腾这件事儿^_^。

最初我并没有想去搞一个通用的安装包制作工具，只是为一个现有的源码工程建立了一个试验性质的安装包工程，并实现了其构建脚本(build.py)。但之后考虑到各个项目都要建立一个对应的安装包工程，安装包工程的构建脚本build.py势必会沦落成被copy来copy去的下场，这显然不是一个很好的解决问题的办法。那是否需要再单独设计和实现一个安装包制作工具呢？工具多了，大家用起来肯定会很烦，不能自找没趣^_^。要知道为程序员编写工具可是一件很困难、很头疼，需要你很谨慎的事情。现在我们已经有了源码工程构建工具[buildc](http://tonybai.com/2011/12/08/buildc-a-building-assistant-tool-for-c-app/)，我前几天还为buildc添加了[安装脚本](http://tonybai.com/2012/02/07/add-setup-script-for-buildc/)，并用之改造了一个真实的工程，并给大家做了讲解，可以说大家对[buildc](http://code.google.com/p/buildc/)算是接受了。

那把安装包制作功能集成到buildc中呢？一个大胆的想法油然而生。这样做似乎扩展了原buildc的设计意图：不仅可以做源码工程的构建辅助工具，还可以用于辅助生成安装包制作工程并制作安装包，并且这样做也最大限度迎合了组织内部大家的需求，避免了日后被狠狠地拍板砖^_^。

之前的试验安装包工程的构建脚本已经实现，现在只需将其功能移植到buildc中即可。在"[也谈C应用安装包制作与部署](http://tonybai.com/2012/02/01/also-talk-about-c-app-install-package-making-and-deploying/)"一文中我提到了一个示例安装包工程的组织方式，其实这里的buildc所实现的安装包制作功能也是以这个安装包工程的组织方式作为前提的，不过这里又略做了些改动，示例如下：

setup_project/

– setup.cfg

– distributions/

– cn-foo-2.14.0.0-x86-linux-64bit.tar.gz

– src/

– setup.py*

– README

– app/

– env/

– conf/

– log/

– bin/

…

– deps/

– libs/

– tools/

– scripts/

– deps_check.sh

– others/

也就是说，buildc生成的C应用安装包工程目录组织方式就是这样的；反过来说只有这个模样的安装包工程才能使用buildc进行安装包构建。我为buildc添加了一个Command "pack"用于安装包工程相关操作，这个命令的使用方式如下：

一、安装包工程的创建

在任意路径下执行buildc pack create –project=YOUR_SETUP_PROJECT_NAME，你即可在当前目录下看到一个empty安装包工程：

$> buildc pack create –project=foo_setup

Setup project [foo_setup] create OK!

$> cd foo_setup

$> ls

distributions/ setup.cfg src/

$> cd src; ls

$> app/ deps/ env/ others/ README scripts/ setup.py*

二、配置安装包工程

在生成的安装包工程下面有一个配置文件setup.cfg，在使用buildc进行安装包构建之前，务必先进行该文件的配置，其内容示例如下：

distribution = {

"packname" : "cn-foo",

"version" : "2.14.0.1",

}

source = {

"trunk" : "svn://10.10.15.56:4444/cn/trunk/foo",

"binary_prefix" : "cn-foo"

}

其中：

distribution['packname'] – 最终安装包的名字前缀

distribution['version'] – 最终安装包的版本号

source['trunk'] – 该安装包工程所对应的源码工程的svn url

source['binary_prefix'] – 源码工程构建后所生成的二进制可执行文件的名字前缀

三、构建安装包

在已经配置好的安装包工程中，使用buildc pack build命令即可以进行安装包的制作，例如：

$> buildc pack build

Clean [.build] OK!

Clean [.package] OK!

Clean [./src/app] OK!

Clean [./distributions] OK!

Package distribution clean OK!

Create dir [.build] OK!

Export [svn://10.10.15.56:4444/cn/trunk/foo] OK!

Cd /home/tonybai/proj/foo_setup/.build/foo

Config Make.rules OK!

Make Ok!

Copy binary file to [/home/tonybai/proj/foo_setup/src/app] Ok!

Cd /home/tonybai/proj/foo_setup

Del [.build] OK!

Build source [svn://10.10.15.56:4444/cn/trunk/foo] OK!

Create dir [.package] OK!

Cd /home/tonybai/proj/foo_setup/.package

Generate cn-foo-2.14.0.1-x86-linux-64bit.tar OK!

Zip cn-foo-2.14.0.1-x86-linux-64bit.tar OK!

Cd /home/tonybai/proj/foo_setup

Del [.package] OK!

Make target [cn-foo-2.14.0.1-x86-linux-64bit.tar.gz] OK!

构建成功后，你会在distributions目录下看到最终的安装包。如果在buildc命令行中没有指定–tag=YOUR_SOURCE_TAG，buildc会使用setup.cfg中source['trunk']中的配置检出trunk代码并构建；如果指定了SOURCE TAG，那么buildc就会使用tag中提供的source svn url检出代码并构建，例如下面的命令将检出foo-2.14.0.2标签的代码并构建可执行程序：

$> bulidc pack build –tag=svn://10.10.15.56:4444/cn/tags/foo-2.14.0.2

四、清理安装包工程

在工程目录下，使用buildc pack clean命令可以对安装包工程进行清理：

$> buildc pack clean

Clean [.build] OK!

Clean [.package] OK!

Clean [./src/app] OK!

Clean [./distributions] OK!

Package distribution clean OK!

五、上传安装包文件

在制作完安装包后，我们一般会将其上传到一个指定的发布服务器上去。buildc提供了上传安装包的功能。使用buildc pack upload –host=HOST –user=USERNAME –passwd=PASSWD –dir=REMOTEDIR –port=FTP_PORT命令我们可以将构建完毕的安装包文件上传到远程服务器上面，例如：

$> buildc pack upload –host=10.10.1.191 –user=tony –passwd=tony –dir=dist

Cd distributions

Upload [cn-foo-2.14.0.0-x86-linux-64bit.tar.gz] OK!

BTW，在编写和使用buildc的过程中，我真实地体会到了用脚本语言源文件作为配置文件的强大，与典型的.ini或.xml等类型配置文件相比，其灵活性过之尤甚，特别是在配置文件中嵌入一些代码就可以改变配置行为，并且脚本语言提供的丰富且强大的数据结构可以充分满足你对配置文件数据组织的需求。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论