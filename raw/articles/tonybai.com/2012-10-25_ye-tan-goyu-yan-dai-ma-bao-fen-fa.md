---
title: 也谈Go语言代码包分发
url: https://tonybai.com/2012/10/25/go-package-distributing/
published: '2012-10-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈Go语言代码包分发

[Go语言](http://golang.org)目前(截至1.0.2版本)尚不支持直接链接.a文件(这里的.a文件指的不是传统静态共享库，而是对golang的非main包build后的产物)。这样一来Go的第三方库包或组织内部的公共代码库包只能以源码的形式分发了。

Go提供了get命令用于获取他人分发的代码包。我们通过get命令既可以获取一些知名代码托管站点上的代码，也可以获取组织内部版本控制服务器上的公共代码。

Go get支持的托管站点包括github、google code、BitBucket以及Launchpad，针对这类情况，我们可以得到“特殊”语法的照顾：

go get github.com/bmizerany/assert

go get bitbucket.org/bmizerany/assert

go get code.google.com/p/assert

go get launchpad.net/assert

由于Go已经“内置”了github、google code等的版本控制工具类型，因此我们无需再做任何额外指定，只需用代码的url（去掉http://）即可。

执行get后，代码会被下载到GOPATH环境变量配置中的第一个路径下的src目录下面。例如：我们的GOPATH=/home/tonybai /goworkspace1:/home/tonybai/goworkspace2，执行go get github.com/bmizerany/assert后，我们将在/home/tonybai/goworkspace1下看到github.com 目录，而assert包在本地的完整路径就是/home/tonybai/goworkspace1/github.com/bmizerany /assert。这样我们在代码中直接import "github.com/bmizerany/assert"即可使用assert这个第三方包了。

在组织内部我们也会有自己的私有公共代码库，一份代码库可能被多个项目所使用。在每个项目中都保存一份公共库代码显然是不利于后续版本升级维护的，这样就需要各个项目统一从同一个地方获取或更新公共库代码。这种情况我们同样可以用go get命令来做。

假设内部使用subversion作为版本控制工具，公共库架设在10.10.12.13/svn0/share/golib。这时我们不能简单地的通 过"go get 10.10.12.13/svn0/share/golib"来获取到代码，我们需要告诉get我们采用哪种版本控制工具，而这种信息的传递是通过在库名称后面加上后缀的方式进行的。比如：

go get "10.10.12.13/svn0/share/golib.svn"

这样在/home/tonybai/goworkspace1下就会出现10.10.12.13/svn0/share/golib.svn目录结构。我 们在代码中可以直接import对应的包，比如import "10.10.12.13/svn0/share/golib.svn/assert"。

通过对get命令特性的了解，我们也可以确定分发的代码包到底应该如何组织。从上面的例子我们可以看出我们分发的代码包结构不需很复杂，直接在库的 repository下建立包目录即可，比如上面例子中库repository为golib，assert就是直接建立在下面的目录，同时也是包名。

go get可自动识别http_proxy环境变量，这样Go也可以通过代理获取外部代码包。

使用外部代码包的项目可以通过go get -u url来更新代码包版本为最新版本。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

学习啦，哈哈