---
title: 使用squid搭建http代理
url: https://tonybai.com/2012/11/21/setup-http-proxy-with-squid/
published: '2012-11-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用squid搭建http代理

近期在做一些基础设施搭建的过程中，又遭遇到了公司http代理的问题。主要是很多主机上的工具只支持不带身份鉴权信息的http_proxy设置，如只 支持诸如：export http_proxy='http://10.10.1.1:8090'，而不支持export http_proxy='http://tonybai:passwd@10.10.1.1:8090'这种形式的配置。

或是其命令行选项中只提供了proxy_host和proxy_port两个选项，但并不支持携带鉴权信息。而公司内部要访问外部信息还必须通过公司的带 有身份鉴权的代理服务器，总而言之，弄得我十分不爽。于是乎产生一个想法：是否可以搭建一个内部http中间代理，部门内部主机通过不带身份鉴权信息的代 理配置访问该中间代理，而该中间代理将内部的所有http request都转发到公司代理，同时携带配置好的身份验证信息。

对http代理这事，我完全是个小白啊，于是乎Google开来(恰逢最近Google还不给力，原因你懂的)。

最先试用了一下[tinyproxy](https://banu.com/tinyproxy)，这个工具挺小巧简单，在[ubuntu](http://www.ubuntu.com)下通过apt-get 可直接安装，/etc/tinyproxy/tinyproxy.conf的配置也很简单明了。但配置文件中涉及到转发到upstream proxy server的配置行只支持"Upstream host:port"而不支持"Upstream tonybai:passwd@host:port"形式，并且也没有其他地方支持身份鉴权信息的配置。在其官方[bugzilla](http://www.bugzilla.org)上有很多人反映这一情 况，但其最新版本似乎也没有将这个功能加入，十分遗憾！

于是乎打算换一个重量级的代理工具-[nginx](http://nginx.org)。Ubuntu 9.04下默认安装的nginx是0.65版本。nginx功能虽强大，配置倒并不那么“复杂”，但问题在于nginx本身似乎更专注于负载均衡和反向代 理，而满足我这个问题场景的资料甚少。nginx配置命令和变量太多，要想短时间搞清楚这些变量的含义还真是一件困难事。照猫画虎的尝试了几种配 置，也均未能成功。翻阅了国内唯一一本nginx书籍 – 《[实战nginx](http://book.douban.com/subject/4251875/)》，但无奈太厚，翻了三章，索性放下了。换工具！

最传统的开源免费http代理工具莫过于[squid](http://www.squid-cache.org/)了。估计其市场占有率也是名列前茅的。Ubuntu 9.04下默认安装的squid是2.7版本，不算很老，squid官方站至今还提供2.7版本详细的配置文档。但squid默认的配置文件可是超级庞 大，总共有近5k行，虽然绝大部分内容都是被注释掉的。于是乎先用命令过滤出未注释行，这些行是真正生效的配置。

关于squid如何将收到的http request转发到带身份鉴权的上级http proxy server，网上的信息也较少，不过还是让我发现一条。按照这条配置建议做了尝试。/etc/squid/squid.conf的配置摘要如下：

access_log /var/log/squid/access.log squid

debug_options ALL,1

hosts_file /etc/hosts

coredump_dir /var/spool/squid

acl all src all

acl manager proto cache_object

acl localhost src 127.0.0.1/32

acl to_localhost dst 127.0.0.0/8 0.0.0.0/32

acl localnet src 10.0.0.0/8 # RFC1918 possible internal network

acl localnet src 172.16.0.0/12 # RFC1918 possible internal network

acl localnet src 192.168.0.0/16 # RFC1918 possible internal network

http_port 10.10.13.17:3128

http_access allow localnet

http_access allow localhost

http_access deny all

cache_peer proxy.yourcompany.com parent port_of_company_httpproxy 0 no-query default login=user:passwd

never_direct allow localnet

配置后，重启squid(sudo /etc/init.d/squid restart)。将[Chrome](http://www.google.com/chrome)浏览器的代理配置改为该代理，尝试打开"baidu.com"，陷入漫长等待。于是打开squid的访问日志/var /log/squid/access.log，看到如下失败信息：

1353476636.008 0 10.10.13.235 TCP_DENIED/400 1709 GET error:invalid-request – NONE/- text/html

1353476657.337 1 10.10.13.235 TCP_DENIED/400 1709 GET error:invalid-request – NONE/- text/html

1353476691.420 0 10.10.13.235 TCP_DENIED/400 1678 GET error:invalid-request – NONE/- text/htm

居然出错！换成IE浏览器，现象一样，都是这种错误。在/var/log/squid/cache.log中，还能发现下面错误：

2012/11/21 13:43:56| clientTryParseRequest: FD 12 (10.10.13.235:4247) Invalid Request

不断的修改squid.conf配置，不断地修改浏览器代理配置，不断的失败。总是修改浏览器的代理配置让我感觉十分费劲，于是我换用curl工具来测试 该代理。[curl](http://en.wikipedia.org/wiki/CURL)是可以识别http_proxy环境变量的。将http_proxy环境变量改为export http_proxy=http://10.10.13.17:3128，在命令行敲入curl http://baidu.com，居然得到下面结果：

$ curl http://baidu.com

<html>

<meta http-equiv="refresh" content="0;url=http://www.baidu.com/">

</html>

再回到access.log观察，居然看到了下面成功日志：

1353476863.916 0 10.10.13.235 TCP_HIT/200 677 GET http://baidu.com/ – NONE/- text/html

于是又尝试用wget下载外部文件、用[subversion](http://subversion.apache.org)访问外部svn repository、[rvm](https://rvm.io/)安装ruby包均告成功！这不就是我想要的结果吗！居然被我误打误撞到了！虽然到目前为止我仍然不知道为何浏览器发出的http request不能被识别^_^。

Squid这个http代理功能十分强大，本身就是被很多企业作为公司级http代理的工具的。其配置参考足足可以写成一本厚厚的书（市面上已经有这种书），还好我的场景用不到那些稀奇古怪的配置，目前这种状态足矣！

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论