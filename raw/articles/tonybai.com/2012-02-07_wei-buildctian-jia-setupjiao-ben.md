---
title: 为buildc添加setup脚本
url: https://tonybai.com/2012/02/07/add-setup-script-for-buildc/
published: '2012-02-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 为buildc添加setup脚本

[buildc](http://code.google.com/p/buildc)在发布0.1.0版时并没有做好安装脚本，当时的建议是直接下载0.1.0的源码包或[svn](http://tonybai.com/tag/Subversion) export/checkout源码包，并手工将[buildc](http://tonybai.com/2011/12/08/buildc-a-building-assistant-tool-for-c-app/)目录位置加入到用户的PATH环境变量中。近期buildc计划正式投入到项目中使用，为了方便大家安装以及以后的统一升级维护，我花了些时间给buildc加上了setup脚本。

[Python](http://python.org)有标准的程序分发方案，不过我对这些了解不多。buildc本身很简单，我觉得没有必要把安装做得很复杂，所以就自己动手编写了一个setup.py，不到100行，用于安装buildc。

Python的标准安装脚本也叫setup.py，我这里也借鉴了这个名字。有了setup.py，buildc的安装就简单多了：

* 下载buildc Release包(当前最新是buildc-0.1.1)

* 解压发布包，在发布包路径下，执行setup.py install [--prefix=YOUR_INSTALL_PATH]

setup.py默认将buildc安装到/usr/share/buildc下面，并在/usr/bin下建立一个到/usr/share/buildc/buildc脚本的符号链接(symbol link)，当然这种安装是需要root权限的，但一旦安装好，host上的所有用户就都可以使用buildc了，日后统一升级buildc也十分方便；如果你不想在默认路径下安装，可以通过–prefix=XXX指定你自己的安装路径，这种情景下，setup.py不会建立什么符号链接，需要你手动将你的安装路径加入到你的PATH环境变量中，以便后续使用。

卸载buildc也十分方便，执行一条"setup.py uninstall [--prefix=YOUR_INSTALL_PATH]即可。

setup.py的安装原理很简单，就是利用shutil包的copytree将buildc目录复制到指定目录下。shutil的copytree在Python 2.6以后版本中支持ignore参数，可以有选择的将buildc目录下的文件和目录复制到目标目录，比如.pyc文件或.svn目录本不应该出现在目标目录下，我们就可以通过ignore参数指定一个ignore_patterns来过滤掉这些文件或目录：

shutil.copytree(package_root, install_root, ignore = shutil.ignore_patterns('*.pyc', '.svn'))

但在Python 2.6版本之前，ignore参数是不被支持的，所以这里也留下缺憾，那就是如果你使用svn checkout方式下载源码包，安装的时候.svn等目录也会被安装到目标目录下，看起来别扭，但不影响您对buildc的使用。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论