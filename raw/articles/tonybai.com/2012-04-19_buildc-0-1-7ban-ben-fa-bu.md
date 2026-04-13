---
title: buildc 0.1.7版本发布
url: https://tonybai.com/2012/04/19/buildc-0-1-7-release/
published: '2012-04-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# buildc 0.1.7版本发布

最近针对[buildc](http://code.google.com/p/buildc)又有了一些新想法，于是今天上午又对buildc进行了多处修改，并相继发布了0.1.6版本和0.1.7版本。

* 对buildc cache upgrade的实现进行了修改。

在执行全量更新本地cache前，先对本地cache的情况进行一些检查，并判断是否与当前.buildc.rc中的配置相符。如果两者是一致的，那么只进行update操作；否则则执行真正的upgrade(remove and re-init)。

* 调整了整个buildc源码目录的结构。

原先所有代码都放在build_utils目录下，这次我把代码分为两类：一类是核心逻辑(core)；另外一类则是工具库类(utils)，因此我删除了build_utils目录，同时增加了core和utils两个目录，分别存放不同类别的源文件。

在进行这项改造时遇到了一个小问题，那就是

[Python](http://python.org)模块(比如core模块)中的源文件导入(import)另一个同级别模块(比如utils模块)中的符号的问题。以core模块的core.py为例，core.py中导入了env文件中的符号。原先core.py和env.py在同一个模块(build_utils)下，直接import env即可；但现在core.py和env.py分别放在了core和utils目录下，直接import env就会出现导入错误。这里涉及到了Python的模块搜索路径(sys.path)。默认的sys.path只是包括执行脚本的当前目录以及一些Python相关的安装目录(比如/usr/lib/python2.6、/usr/local/lib/python2.6/dist-packages等)。这样Python解释器无法找到core.py所在目录的上层目录utils下的env.py文件。为此我们需要在sys.path中增加一个路径，即'..'，core.py文件的代码截取如下：import sys

import os

import shutil

sys.path.append('..')

from utils import env

…

这样Python解释器就可以在core.py所在目录的上一层目录下寻找模块了。

* 将samples中的模板文件统一移到了templates中，删除samples目录

最初设计templates目录下只存放Make.rules相关模板文件，当时考虑的是支持多Make.rules模板。但目前只考虑支持一种，至少目前是这样(也许后续会有变化，但不能肯定)，而samples目录下的文件其实也都是各种配置模板，因此将两个目录合二为一。

* 修改buildc init的执行语义

原先buildc init在初始情况下会在$(HOME)目录下创建.buildc.rc以及在当前目录下创建buildc.cfg；.buildc.rc是用户级别的配置；而buildc.cfg是项目级别的配置，放在一个init里显然有些不合适，因此0.1.7版本及以后版本在执行buildc init时只会创建$(HOME)/.buildc.rc。

* 增加buildc config init

对于项目级别的配置bulidc.cfg，我们使用新命令buildc config init来创建，即初始化一个项目级别的配置。

* 用buildc config make替代buildc config-make

顺水推舟，我们去掉了config-make这个command，进而改用buildc config make来生成或重新配置Make.rules文件。

做完以上修改后，感觉buildc看起来和用起来都更舒服些。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论