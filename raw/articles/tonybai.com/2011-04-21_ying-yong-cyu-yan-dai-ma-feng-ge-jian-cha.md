---
title: 应用C语言代码风格检查
url: https://tonybai.com/2011/04/21/apply-style-check-to-c-code/
published: '2011-04-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 应用C语言代码风格检查

代码风格（style）一直是一个见仁见智的问题，但是对于一个团队而言，如果能在代码风格上达成一致，显然无论对团队还是对个人来讲都是大有裨益的。

在这方面我们也曾做过努力，包括在团队中引入[astyle](http://tonybai.com/2010/07/29/use-astyle-to-beautify-your-code/)工具，并在astyle的代码美化风格配置上，团队成员也集体达成过一致。但是在开发过程中还是出现了一些问题。最主要的就是对astyle工具使用不足：一些同事总是记得不停地写代码，但却忘记了按约定好的风格要求写代码或按照要求通过工具执行代码美化。

为了尽可能地保证提交到代码库中的代码都是风格良好的（也可以在[代码评审](http://tonybai.com/2011/02/22/code-reviews/)时间接减少评审者提出有关代码风格问题而耗费的工作量），我们将代码风格检查加入到代码构建的关键流程中去，这样可以起到一个提醒大家注意代码风格的作用。与Java等语言相比，C语言的代码风格检查工具相对较少且工具的功能也很有限。我Google了半天才找到一款简单且实用的工具-[c_style_check.py](http://www.cs.caltech.edu/courses/cs11/material/c/mike/misc/c_style_check)。这个检查脚本使用正则式匹配的方法按照你制定的规则对源码文件进行校验，如果发现不符合规则的代码行，则给出提示。另外考虑到我们内部的要求，我对这个脚本也作了一些改造，增加了一些校验规则，并把最新的脚本放到了[这里](https://bigwhite-code.googlecode.com/svn/trunk/style_check_scripts/)。

目前的脚本较为简单，无法检查你的所有风格要求，不过它还是能检查出一些我们想要的不符合风格的地方。比如：不允许使用TAB字符、每行最大长度限制、在常见操作符(比如+,-,*,/,>,<等)两侧要添加空格、在){之间要求添加一个空格以及要求采用C传统注释方式等等。

另外，Google提供了一个强大的按照[Google C++风格](http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml)进行检查的代码检查器 – [cpplint.py](http://google-styleguide.googlecode.com/svn/trunk/cpplint/cpplint.py)。不过尚没有C代码风格检查工具推出，不过cpplint.py这种级别的检查器是我们努力的方向。后续也许会逐步改进[c_style_check.py](https://bigwhite-code.googlecode.com/svn/trunk/style_check_scripts/c_style_check.py)。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论