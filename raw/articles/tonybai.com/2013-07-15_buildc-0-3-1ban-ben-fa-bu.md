---
title: buildc 0.3.1版本发布
url: https://tonybai.com/2013/07/15/buildc-0-3-1-release/
published: '2013-07-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# buildc 0.3.1版本发布

随着[buildc](http://code.google.com/p/buildc)在内部应用的深入，buildc逐渐进入了以内部需求和问题为主要驱动力的演化模式。我们内部的C应用多是后端服务类应用，个人 觉得具有一定代表性。[buildc](http://tonybai.com/2011/12/08/buildc-a-building-assistant-tool-for-c-app/)最初就是为了针对这类C应用而设计的。因此我们内部的需求和问题应该也同样具有一定代表性，而这种演化模式在一 段时间范围内还是有意义的。

[buildc 0.3.1版本](https://buildc.googlecode.com/files/buildc-0.3.1.tar.gz)修正了上一版本的若干bug，并增加了两个新功能。

*** 提高容错能力**

buildc对第三方库的组织结构有着严格的要求，一般是：

package_name/

version/

CPU_MODE_OS/

include/

lib/

一般来说，第三方库会由组织内特定人员进行管理和维护，第三方库服务器上的目录结构不会出现组织错误的情况。但[buildc 0.3.0](http://tonybai.com/2013/05/11/buildc-0-3-0-release/)还是遇到特例了：当某个package的第三级目录为空时，buildc 0.3.0版本会抛出异常。为此，buildc 0.3.1增加了对这块逻辑的容错处理：

1. 如果目录是空目录，直接略过。

2. 如果目录存在合法的目录，cpu_mode_os，加入.buildc.repository中

3. 如果目录中存在合法的目录和不合法的目录，略过不合法的目录。

*** 支持命令行变量**

有些项目针对不同客户有不同的功能版本，但代码是一份，针对不同客户的Release版本用一些特定的宏开关控制，而这些功能开关需要在编译构建 期指定。比如最初版本的buildc.cfg中的片段如下：

custom_defs = ['-std=gnu99', '-DLOGLEVEL=1', '-DUSE_NM']

后A省的客户希望LOGLEVEL用2级，不需要NM(网管)功能，而B省的客户希望LOGLEVEL用2级同时也使用NM功能，那我们的 custom_defs就需要有多种配置了，例如：

if province == "A":

custom_defs = ['-std=gnu99', '-DLOGLEVEL=2']

elif provice == "B"

custom_defs = ['-std=gnu99', '-DLOGLEVEL=2', '-DUSE_NM']

else:

custom_defs = ['-std=gnu99', '-DLOGLEVEL=1', '-DUSE_NM']

province这个变量可以定义在buildc.cfg中，但每次针对不同省份Release时，需要手工修改province变量的值，这样 十分麻烦。因此我们想到是否可以让buildc像Make那样支持[命令行变量](http://tonybai.com/2011/05/19/use-command-line-vars-of-make/)呢，就像这样：

buildc config make province="B"

于是乎buildc 0.3.1版本就实现了这个功能，你可以在buildc config make或buildc pack中使用buildc的命令行变量，命令行变量支持var=value形式，其中value支持如下几种值：

var=1

var=on

var="on"

对于var=on，在buildc内部会将var=on转化为var="on"，否则python会提示找不到on的定义。

*** 支持指定项目配置文件（buildc.cfg)**

当功能开关变得很多时，我们往往很难记住那么多[命令行变量](http://tonybai.com/2013/07/09/an-implementation-of-python-commandline-variables/)，我们可能就会为每个项目保存多个项目构建的配置文件，比如 buildc_for_liaoning.cfg、buildc_for_beijing.cfg等。而以前的buildc只默认支持 buildc.cfg这样一种配置文件，无法支持这类需求，因此buildc 0.3.1增加了指定项目配置文件功能。

如果你要为A省客户发布，你可以敲入buildc config make –config=PATH_OF_CONFIG_FILE，buildc就会加载你指定的配置文件了，而不是默认的buildc.cfg。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论