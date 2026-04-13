---
title: 使用ssh通过http代理访问bitbucket
url: https://tonybai.com/2012/05/09/ssh-access-bitbucket-via-http-proxy/
published: '2012-05-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用ssh通过http代理访问bitbucket

在很多公司内部，要想访问外部互联网都需要设置代理，我所在公司也是这样，有些时候这种限制真的可以让人骂娘。不过经过几年与代理的"斗争"后，大部分需 要访问外部网络的软件(比如[subversion](http://tonybai.com/2011/03/23/also-talk-about-solving-the-svn-conflicts/)、apt-get、[git](http://tonybai.com/2011/01/20/try-git-svn/)、wgetc、filezilla等)经过设置后还都可以正常工作。不过前些日 子在折腾bitbucket上的源码库时又遇到了代理问题：无论通过https方式还是ssh方式都无法clone [bitbucket](http://bitbucket.org)上的git库。

之所以用bitbucket而不是[github](http://github.com)是因为前者提供免费的private repository，而后者则是收费的。今天又亟需访问bitbucket上的库，于是再次尝试突破代理的限制。

这次想到一个思路：ssh是否可以通过http代理出去呢？Google的结果告诉我：可以！于是眼前一亮，开始折腾。

首先要安装一个名为connect-proxy的链接代理软件：sudo apt-get install connect-proxy，软件不大，瞬间就安装完比。

然后创建~/.ssh/config配置文件(如果之前已经存在该文件，就打开该文件)，将如下配置写入该配置文件：

## ssh access bitbucket.or via HTTP proxy

Host bitbucket.org

ProxyCommand connect -H user@proxy_server:port %h %p

## other sites, do NOT use proxy

Host *

ProxyCommand connect %h %p

这里的配置很清晰，当匹配到bitbucket.org这个host时，ssh经由http proxy访问相应的主机；其他主机，则直接访问。注意connect命令其实就是connect-proxy，通过ls -l命令可以看到/usr/bin/connect -> connect-proxy。保存该配置文件后，尝试clone一个bitbucket上的repository，例如：

$> git clone git@bitbucket.org:lindekleiv/jquery-ui-colorpicker.git

$> ~/proj/opensource$ git clone git@bitbucket.org:lindekleiv/jquery-ui-colorpicker.git

Initialized empty Git repository in /home/tonybai/proj/opensource/jquery-ui-colorpicker/.git/

Enter proxy authentication password for user@proxy_server:

remote: Counting objects: 33, done.

remote: Compressing objects: 100% (32/32), done.

remote: Total 33 (delta 18), reused 0 (delta 0)

Receiving objects: 100% (33/33), 16.04 KiB, done.

Resolving deltas: 100% (18/18), done.

可以看到命令执行后，会提示你输入访问代理的密码。输入正确的密码后，我们可以看到git可以顺利访问到bitbucket上的jquery-ui-colorpicker这个库了。

这里有一点挺让人糟心，那就是每次都得输入访问proxy server的密码，man connect-proxy也没有发现放置http_proxy代理密码的地方，用-h选项也不行。

注意这种用ssh访问的前提是将本地生成的公钥放置在你的bitbucket账户的"SSH keys"中了。

BTW，理论上这种ssh通过http代理的方式对github也同样适用。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论