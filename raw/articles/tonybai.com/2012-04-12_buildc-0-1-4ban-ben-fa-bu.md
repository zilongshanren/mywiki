---
title: buildc 0.1.4版本发布
url: https://tonybai.com/2012/04/12/buildc-0-1-4-release/
published: '2012-04-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# buildc 0.1.4版本发布

年后[buildc](http://tonybai.com/2011/12/08/buildc-a-building-assistant-tool-for-c-app/)开始逐渐在产品线的项目里应用了，随之而来的是大家反馈的各种意见和bug。尤其是bug，我都会很认真地应对，也会及时发布相应的版本修复这些bug。[buildc 0.1.4](http://code.google.com/p/buildc)版本就是一个bugfix版本，其修复的bug源于今天上午的一次[持续集成](http://tonybai.com/2012/02/14/install-and-configure-jenkins/)的失败。

上午收到

[Jenkins](http://tonybai.com/2012/02/14/install-and-configure-jenkins/)发送的一个"build failed"的mail，一个[安装包项目](http://tonybai.com/2012/02/10/add-packing-feature-to-buildc/)的[CI](http://en.wikipedia.org/wiki/Continuous_integration)job执行失败了，于是到Jenkins web页面上检查错误原因。这个Job会在两个slave node上执行集成，一个在x86 linux上，一个在x86 solaris上。这次失败是因为x86 linux上的一个配置问题导致的，页面显示x86 solaris那个节点的集成是成功的。我无意间查看了x86 solaris节点集成过程的命令行输出，发现如下内容：Config Make.rules OK!

Failed to execute cmd [make CMODE=64-bit], errno = [512]

Finished: SUCCESS

显然，构建脚本并未真正成功，但

[Jenkins](http://tonybai.com/2012/02/15/intergating-on-multiple-platforms-simultaneously-using-jenkins/)却认为这次集成是OK的，这是怎么回事呢？难道是[Jenkins](http://jenkins-ci.org)有问题？为了弄清原因，我登到那个Solaris节点上，进入到Jenkins slave工作目录下的workspace中，在对应的Job目录下，手工执行了集成脚本，执行结束后，通过"echo $?"查看命令的返回值，居然是"0"，也就是说执行结果是成功的，这怎么可能？明明代码中输出是"errno= [512]"。为了验证问题，我编写了一个测试程序以验证代码执行是否正确：

# testerrno.py

#! /usr/bin/env python

import commands

import sys

def execute(cmd):

o = commands.getstatusoutput(cmd)

if o[0] != 0:

print "Failed to execute cmd [%s], errno = [%d]” % (cmd, o[0])

sys.exit(o[0])

return o

if __name__ == '__main__':

execute('ls -l foo')

由于当前目录下并未有foo文件，因此预期testerrno.py的执行结果应该是失败的，执行过程如下：

$> testerrno.py

Failed to execute cmd [ls -l foo], errno = [512]

$> echo $?

0

从结果中可以看到，居然执行结果返回的真的是0。我将上述代码中的sys.exit(o[0])直接改为了sys.exit(512)，我要看看究竟是怎么回事，结果执行结果又出乎我的意料：

$> testerrno.py

Failed to execute cmd [ls -l foo], errno = [512]

$> echo $?

0

$> testerrno.py

Failed to execute cmd [ls -l foo], errno = [512]

$> echo $?

23

执行后得到的结果为：23。看来我的思路是正确的，那Shell支持的最大errno值究竟是多少呢？经验告诉我很可能是255。于是乎我又分别将返回值硬编码为255和256并执行之，结果当返回值为255时，echo $?的输出为255；当返回值为256时，echo $?的返回值居然变成了0，看来就是这个问题了。关于为何Python获取到的ls -l foo的执行结果为512(commands.getstatusoutput的返回结果)，我没有深究，但如果手工在命令行上执行'ls -l foo'，得到的返回值实际上是2，而不是512。另外我的Shell版本为：GNU bash, version 3.00.16。

如何修复buildc的这个问题呢？我的方法是让command.execute在执行命令出错时返回同一个指定的错误码，目前为errors.py中shell_cmd_exec_failed值。但command.execute会打印commands.getstatusoutput返回结果中的真实错误码值，两不耽误。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论