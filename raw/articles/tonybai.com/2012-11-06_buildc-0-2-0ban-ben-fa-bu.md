---
title: buildc 0.2.0版本发布
url: https://tonybai.com/2012/11/06/buildc-0-2-0-release/
published: '2012-11-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# buildc 0.2.0版本发布

[buildc](http://code.google.com/p/buildc/)的演进先后经历了[构建管理](http://tonybai.com/2011/12/08/buildc-a-building-assistant-tool-for-c-app/)和[安装包工程管理](http://tonybai.com/2012/02/10/add-packing-feature-to-buildc/)两个阶段。其中buildc的构建管理功能在项目中应用较早，目前相对稳定可靠。但其支持的安装包工程是直到最近才被大家所正式使用的。不出意料，大家在使用过程发现了一些问题，于是我们也是边用边改。

目前一个setup工程一般具有类似如下源码组织结构：

distributions/

setup.cfg

src/

– README

– app/

– conf/

– deps/

– layout.cfg

– others/

– scripts/

– setup.py

按照最初的设计，deps目录下会存放一些目标程序运行时依赖的库、工具等。但就一些细节并未考虑清楚，比如如果一个程序需要在两个平台（linux和solaris）上运行，那deps下的依赖库应该如何存放？

就这个问题一线的人员在设计setup工程时采用的策略是将某个库的所有平台版本都手工放到deps下，以instantclient这个oracle的客户端库来说，就形成了如下结构：

deps/

– instantclient/

– 10.2.0.5.0/

– x86_64_linux/

– lib/

– x86_64_solaris/

– lib/

这样一来安装包制作完后size非常的大，不便于存储和传输。另外手工copy依赖库显然不够专业。打包过程是buildc来完成的，而buildc是拥 有全部依赖库的存储位置、版本等信息的。于是我们就这个问题做了改进，让[buildc 0.2.0](http://buildc.googlecode.com/files/buildc-0.2.0.tar.gz)支持将依赖的第三方库根据目标程序运行平台类别自动打包到最终的安装包中。

也就是说，如果你是为x86-64 linux平台做的安装包，最终安装包中的目录结构会是：

deps/

– instantclient/

– 10.2.0.5.0/

– x86_64_linux/

– lib/

而这一切仅需通过配置完成。在setup工程顶层目录的setup.cfg文件中，我们增加了一个新配置项，用于描述目标程序运行时依赖哪些第三方库，这些库将被打包到安装包中，并部署到目标主机上去。

配置的格式如下：

dependences = [

("instantclient", "10.2.0.5.0", ["libclntsh.so", "libclntsh.so.10.1", "libnnz10.so"]), # 打包指定的库文件

#("instantclient", "10.2.0.5.0", []), # 打包instantclient/10.2.0.5.0下所有的库文件

#("instantclient", "10.2.0.5.0"), # 打包instantclient/10.2.0.5.0下所有的库文件

]

通过例子可以看出dependences中的元素支持三种形式配置，可以指定打包的库文件，也可以将库目录整体打包。

BTW，buildc自从发布以来一直没有user guide，好消息是项目组的小兄弟wtz1989227已经在wiki上建立了[buildc_user_guide](http://code.google.com/p/buildc/wiki/buildc_user_guide)页面，后续他会逐步完善这个guide的。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论