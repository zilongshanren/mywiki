---
title: buildc 0.1.9版本发布
url: https://tonybai.com/2012/07/19/buildc-0-1-9-release/
published: '2012-07-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# buildc 0.1.9版本发布

随着[buildc](http://code.google.com/p/buildc)使用的深入，越来越多的新需求暴露了出来。为了满足这些需求，我们组的小兄弟又对buildc进行了一些改造，这些变化如下：

1、支持将多个子工程打包到一个安装包中

最初[buildc](http://tonybai.com/2012/02/10/add-packing-feature-to-buildc/)的设计思想是为每个子工程单独制作安装包，这样具有很强的灵活性。但在对现有N个工程进行构建脚本改造的过程中发现，有些工程间存在严重 依赖，比如工程A是一个业务级公共库工程，工程B和工程C都依赖工程A构建后生成的静态共享库。而工程A又无法被当成第三方库处理，这给我们的安装包构建 制造了难题。我们的解决方法就是改造安装包工程的setup.cfg文件，让其支持多source。从正规语义上来讲，我们这么做将使得buildc支持 将多个子工程打包到一个安装包中，而间接的作用则是解决了上述有依赖关系的工程安装包制作的问题，虽然看起来不那么美。

修改后，setup.cfg中配置就变成下面这种情况了：

source = [

{

"trunk" : "svn://10.10.15.56:4444/cn/trunk/A",

"binary_prefix" : "fooA"

},

{

"trunk" : "svn://10.10.15.56:4444/cn/trunk/B",

"binary_prefix" : "fooB"

}

]

不过问题并没有彻底解决。A工程的构建结果是一个.a文件，按照原buildc处理流程，该.a文件会被放入安装包中的app目录下，但这不是我们想要 的，.a文件是不应该放入安装包的。与此同时，一些子工程的输出是.so文件，按照最初的规划，这些.so文件应该被放入deps目录，而原buildc 默认都是放在app目录下。为了解决这个问题，我们给source做了"属性扩容" – 增加了一个可选的pack_path字段。

source = [

{

"trunk" : "svn://10.10.15.56:4444/cn/trunk/A",

"binary_prefix" : "fooA"

"pack_path" : ""

},

{

"trunk" : "svn://10.10.15.56:4444/cn/trunk/B",

"binary_prefix" : "fooB"

},

{

"trunk" : "svn://10.10.15.56:4444/cn/trunk/C",

"binary_prefix" : "fooC"

"pack_path" : "deps"

}

]

这个示例中，A工程pack_path的值为""，buildc将忽略A工程的输出文件，B工程没有配置pack_path，则buildc默认将B工程 的输出文件放入app目录；而C工程明确为pack_path赋了值，buildc会将C工程输出文件放入deps目录。

buildc原本支持在命令行输入工程源码库地址(–tag=YOUR_SOURCE_TAG)，现在依旧支持。一旦命令行指定了工程地 址，buildc将不会理睬setup.cfg中source中配置的各个源码库路径，将从命令行指定的工程地址处取得最新源码，但暂无法指定 pack_path，默认会将构建结果放入app目录。

2、打包时自动生成VERSION文件

buildc在执行pack build后，自动在安装包中生成一个VERSION文件。该文件中包含与安装包匹配的平台信息(包括CPU体系、OS类型等)以及构建时的一些版本信 息。该文件除了便于安装包使用人员查看安装包相关版本信息之外，还可以用作安装包在目标平台进行约束检测的依据。如果你的安装包是for x86-64 linux的，那么宕操作人员误将该安装包部署到Solaris 10 for sparc平台时，安装包中的deps_check.py脚本会比对当前平台信息与VERSION文件中携带的信息，发现不匹配，则报错并停止程序的安 装。

3、其他

该版本buildc还提供了一些脚本的详细示例，如env_gen.py、deps_check.py。另外从Make.rules.in模板中去除了硬编码的-D_DEBUG定义。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论