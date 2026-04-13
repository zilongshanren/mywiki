---
title: 那些代码中的“中国式”命名
url: https://tonybai.com/2013/11/06/those-chinese-style-naming-in-code/
published: '2013-11-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 那些代码中的“中国式”命名

10月中旬，有人在[Quora](https://www.quora.com)网站上发起一个调查：“[程序员职业生涯中最难的事是什么？](https://www.quora.com/Software-Engineering/What-is-the-hardest-thing-you-do-as-a-software-engineer)”，调查结果让人实感意外。世界范围内的程序员同胞们普遍认为： “命名是让大家感觉最困难的事情”。对于主流的欧美程序员尚且如此，对于英文非母语的中国程序员来说，苦逼程度可想而知了:(。

虽说中国程序员大多也都学了10年以上的英语了，但能“地道”的表达和书写甚至是选词的程序员们比例却不高。而在编写程序的过程中，给变量、常量以及函数命名即意味着我们要选择恰当地道的词汇或缩写。

事实证明，任何事情经过中国人民的加工，就会呈现出意想不到的效果，于是我们有了[Chinglish](http://en.wikipedia.org/wiki/Chinglish)，有了“中国式”的命名。就此，我特地花了些时间翻阅了下面几个项目组的源码，总结出了一些“中国式”命名的门道，这里也说道说道^_^。

**一、万能的动词**

通过阅读代码中的一些命名，我发现了代码中经常出现的一些动词堪称“万能”，这些动词包括：handle、do、process、check、collect等。无论对象是什么，你只要像如下这么命名，中国程序员基本都能看懂或猜个八九不离十：

process_xx 处理xx

do_yy 做yy

handle_zz 处理zz

check_xx 检查/校验xx

collect_xx 收集xx

**二、标志/类型代言人**

在项目源码文件中，你会变量声明或结果体声明中看到太多的xx_flag或xx_type。xx_flag被大家“公认为”各种标志的代言人了；xx_type也好不到哪去。

route_flag

protocol_flag

msg_flag

session_flag

msg_type

check_type

command_type

session_type

**三、字面意直译式**

比如我们要声明两个变量，一个的意思是“是否打开消息过滤”，另外一个“是否关闭消息过滤”。对于中国人来说，打开/关闭最直接对应的就是open/close，于是就有了这样的变量命名：

is_message_filter_open

is_message_filter_close

其实一般认为更地道的方式应该是：

is_message_filter_on

is_message_filter_off

再举个例子，我们的系统要处理一种中文名为“长短信”的对象，于是直译过来就是：long_sms。但其真正的英文术语应该是[Concatenated SMS](http://en.wikipedia.org/wiki/Concatenated_SMS)。

**四、中文拼音式**

在国内做行业解决方案，不可避免会遇到各种领域词汇，比如我们处理的一种业务称为农信通。估计是开发人员没能找到其对应的英文翻译，于是乎用上了我们的看家本领 – 拼音。

nxt_url 农信通地址

这样的例子是否似曾相识呢！

**五、单词“选秀”**

采用这种方式的程序员应该是更具“责任心”的，至少他/她知道去查查英文词典^_^。

于是乎有了dispense_message、cache_overstock等变量命名。显然他是在字典的单词选秀中随意找到一个“顺眼”的、意思还算相近的单词就挑了出来。显然dispatch 、overflow要比dispense、overstock更地道和准确。

**六、尾声**

以上的“实例”确是从我们项目的代码中“挖掘”出来的，希望只是个案。面对这样的命名bad smell，我们是否有解决方法呢？没有捷径，语言的感觉是要一点点的去找的，个人觉得一个最行之有效的方法就是去看那些英语地道的程序员编写的代码，留 意他们是如何命名的。比如看一些著名欧美程序员的开源项目代码。另外对于行业特定领域，尽量用经过认可的英文翻译结果来命名。

不可否认，英语是编程领域的主流语言，包括中文在内的以其他语言为编码语言的编程语言十分罕见。对于欧美程序员来说，这是天然的优势；而对于其他非欧美国家的程序员，尤其是中国程序员来说，在走向“地道”的路上还要付出很多才行。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

那您觉得农信通是要命名为agricultural_informational_communication吗

agro_infor_comu

这个有正规术语以及缩写。

“这些动词包括：handle、do、process、check、collect等。” 中枪了

为了能一眼看懂，某些地方用拼音很好。

中枪 _(:з」∠)_

认真你就痛苦了。。

之前看到过：little_two, LEFT_KUOHAO, 诸如此类…

还有各种各样的manger

Side_bitch_1Fuck_1