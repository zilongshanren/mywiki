---
title: GopherChina2016后记
url: https://tonybai.com/2016/04/18/my-experience-of-gopherchina2016/
published: '2016-04-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# GopherChina2016后记

4月17日晚22:51，伴随着D7次动车缓缓驶入沈阳北站，拖着疲惫的身体和些许兴奋的我，结束了两天的[GopherChina 2016](http://www.gopherchina.org/)之旅。

### 一、GopherChina大会

[GopherChina大会](http://www.gopherchina.org/)是中国大陆地区[Golang](http://tonybai.com/tag/golang)语言推广第一品牌。[2015年](https://github.com/gopherchina/conference/tree/master/2015)在上海成功了举办了第一届大会；[2016年](https://github.com/gopherchina/conference/tree/master/2016)，大会发起人[astaxie](http://weibo.com/p/1005051889019865)为充分照顾帝都（及周边）Gophers们的情绪^_^，将GopherChina 2016搬到了北京举行。

这是我第一次参加GopherChina大会，也是由于“第一次”，心里有种莫名的小兴奋。

第一天会议，8:30来到亚洲大酒店。虽然酒店外面人员密度稀疏，但主会场入口处却是接踵摩肩，人山人海：注册、领“Gopher战斗服”、收集卡片印章，场面好不热闹，不过主会场内部倒是一片井然有序之气象。会场内主屏幕上循环播放着这次大会几大赞助商的宣传视频：[七牛](http://www.qiniu.com/)、[Daocloud](https://www.daocloud.io/)和[Grabtaxi](http://www.grab.com/)等。作为Gopher，首先应该感谢这些金主，没有他们的”金元”，谢大也难为无米之炊不是。

![img{512x368}](../../assets/61818c414bf45873.jpg)


### 二、Topic主观短评

大会的日程很紧张，Topic较多，能全神贯注的聆听每个Topic基本很难。开始还好，后来只能重点听听自己感兴趣的了，第二天的时光尤甚。相信坚持听完两天的topic的Gopher们都或多或少有疲惫之感。下面就自己的感受，用短短一两句话，主观短评一下各个Topic：

#### 第一天

[陈辉](https://github.com/huichen)的“Go 人工智能”：

话题挺“唬人”^_^，实质则是陈总个人的opensource project show，从“悟空”到“弥勒佛”一应俱全。并且鉴于陈总的Facebook、Google和Alibaba的从业经历，他的开源项目应该值得学习一番。

[刘奇](https://github.com/ngaut)的“Go在分布式数据库中的应用”：

刘总依旧幽默风趣，这次除了带来了TiDB外，还带来了砸场子的用[Rust](https://www.rust-lang.org/)实现的TiKv，为晚上在技术Party上撕逼打下了伏笔^_^。

李炳毅的“Go在百度BFE的应用”：

“车轮大战、车轮大战、车轮大战”，重要的事情说三遍！不过这仅是go在baidu特定场景应用下的tradeoff。个人倒是不建议关掉默认GC。

[毛剑](https://github.com/terry-mao)的“Go在数据存储上面的应用”：

基于FaceBook的Haystack paper，为[B站](http://www.bilibili.com/)造的一个轮子，细致入微。其中的设计考量值得同样在做分布式文件系统的朋友们借鉴和参考。

[Marcel van Lohuizen](https://github.com/mpvl)的”I18n and L10n for Go using x/text”：

Marcel也是今年[GopherCon2016](https://www.gophercon.com)的speaker，这次来到GopherChina讲解x/text也是让我们先睹为快了。Marcel 对x/text进行了详尽的分类讲解，以及给出当前状态、todo 以及 plan。内容结构很有外国speaker共同具备的那些特点。

[米嘉](https://github.com/mijia) 的”Go build web”：

对Go web dev进行了庖丁解牛，Go味儿十足。现场的很多web dev都反映很有赶脚。

[邓洪超](https://github.com/hongchaodeng) 的“Go在分布式系统的性能调试和优化”：

来自CoreOS的邓洪超很萌，演讲很有激情。但也许是外语说惯了，中文反倒不那么利落了。不过整体效果依旧不错。

[沈晟](https://github.com/tomasen)的”Golang在移动客户端开发中的应用”：

心动网络(前verycd)的沈总讲解了心动网络将[gomobile](https://github.com/golang/mobile) 用于游戏客户端client library的例子。记不得沈总是否说过心动网络已经在正式产品中使用gomobile了，不过无论这样，这种“敢为天下先”的气魄还是值得赞颂的^_^。

#### 技术Party

晚上大约80多人聚集在二楼会议厅举行GopherChina技术Party，Party上，PingCAP的刘奇引发Rust vs. Golang的重度pk。由于高铁晚点而迟到的七牛CEO[许式伟](https://github.com/xushiwei)也再次站出来成为golang的捍卫者。pk从语言特性延伸到社区文化，“民主集中制”的精英文化主导的Golang社区与纯粹美式民主的Rust社区到底孰好孰坏，大家也是众说纷纭，见仁见智。外国友人“马尾辫”(Marcel)和大胡子(Dave Cheney)也参与了论战，不过他们自然是站在Golang一方。之后大家在[Docker](http://tonybai.com/tag/docker)话题上又燃战火，人们就Docker究竟能给企业和开发者带来何种好处进行了深入PK。

#### 第二天

[Dave Cheney](http://dave.cheney.net/)的”Writing High Performance Go”：

Dave Cheney不愧为Go语言的知名布道师，这个topic“编程哲学”与实践并存，干货满满，估计事后消化也需要很长时间。值得一提的是本次大会只有Dave的slide是采用Go team常用的[.slide格式文件](http://tonybai.com/2015/08/22/how-to-view-golang-tech-slide/)制作的，赶脚非常go native。

吴小伟的“Go在阿里云CDN系统的应用”：

围绕Go在阿里CDN的应用，看得出Go用的还是蛮多的。印象深刻的一个观点：老板决定语言！

许式伟的“谈谈服务治理”：

大家似乎都想知道国内第一家采用golang技术栈实现的七牛，内部到底是如何使用go的，但许总就是不能让我们如愿哈。

孙宏亮的”Go在分布式docker里面的应用”：

赞助商Daocloud的技术和产品展示，可以看到Daocloud内部的一些架构设计和实现，值得参考。

高步双的“Go在小米商城运维平台的应用与实践”：

由于困了，听这个speak时很迷糊，无感。

赵畅的“Golang项目的测试，持续集成以及部署策略”：

我也是第一次听说Grab这家公司。不过赵畅这个speak我很喜欢，把公司技术栈的变迁讲的很生动，关于golang的实践和一些数据正是我们需要的。

孙建良的“Go在网易广域网上传加速系统中的应用”：

不知为何，slide的首页标题居然是：Go&网易云对象存储服务。原以为标题发生了切换，但没过几页，又回到了“广域网上传加速系统”，这两者似乎也没啥联系啊。也许是我没听完提前离场赶火车的缘故吧。

### 三、会后

谢大组织的这次GopherChina2016非常成功，表现为几点：

- 参会者众多，会场爆满，还有不辞辛苦，站着聆听的gopher。
- 多数Speaker表现优异，达到了Gopher传道的目的。
- 技术Party气氛热烈，论战持久，让Gopher收获满满。
- 硬件以及组织到位，会场井然有序。
- 这次Gopher战斗服非常棒，材质很好。
- 会场的水、水果、奖品、party前自助餐也很给力。

这里对谢大也表示大大的感谢！

个人也有一些小建议：

- 多些场上互动，尤其是下午场，易困倦。如果此次能将daocloud的抽奖环节挪到主会场，全员参与，想必更能活跃气氛，为大家提神^_^。
- 从GopherChina大会品牌角度出发，如果能统一讲师slide模板会更好，如果都能使用go team那种native的.slide文件格式就更Go味道十足了。
- 希望类似GopherCon大会那样，增加open keynote(语言历史，当前，未来plan)和close keynote(社区文化推广)两个环节。

另外我觉得应该对讲师slide内容做一些审核，考虑像gopherchina这样的围绕一门编程语言的conference，到底什么话题才是最佳的呢？当前借着Go之名，实则讲解某一行业领域系统架构的内容似乎多了一些。针对语言本身、语言标准库、语言工具和语言最佳实践的内容略少了一些。

如果要谈语言应用，那个人认为至少如下几个方面应该提及：

- 使用什么go版本
- 版本切换时的差异（内存、cpu、GC延迟、吞吐）和坑
- 用Go开发了哪些服务？为何？为何其他服务不用Go开发，理由。
- 遇到问题/坑，如何解决
- 组织内Go的最佳实践

各位讲师的slide后续还得慢慢消化，另外感谢[极客学院](http://www.jikexueyuan.com/)展台工作人员的拍照服务^_^：

![img{512x368}](../../assets/0eae79a763a1b30c.jpg)


© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

赞一个大白细致的介绍和思考，寥寥数语让没参加会议的我也能体验到嘉宾的特点。学习会议ppt…

关于沈老板的那个topic, 我认为应该还是属于实验状态

比以往的各种会质量高很多

tidb 用来替换mysql感觉还有很远的路要走

忘记和你一起合影了，太忙了

嗯，下次再有机会一定和谢大合个影。

第二天下午直接溜班睡大觉去了[哈哈]

文本选中颜色为什么是白的？好不习惯[委屈]

@bigwhite，读了你的一些文章，有广度又有深度，留个联系方式吧。

谢谢，各种联系方式在我的blog主页右侧边栏有哦。

虽然作为一个大学里的Gopher没有到场，但是博主的精彩陈述，还是缓解了我没去现场的遗憾

去现场体验更佳:) 明年有机会建议去现场。