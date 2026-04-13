---
title: TB一周萃选[第7期]
url: https://tonybai.com/2018/01/28/7th-issue-of-the-tech-weekly-carefully-chosen-by-tonybai/
published: '2018-01-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# TB一周萃选[第7期]

本文是首发于[个人微信公众号](https://mp.weixin.qq.com/mp/qrcode?scene=10000005&size=102&__biz=MzIyNzM0MDk0Mg==&mid=2247483848&idx=1&sn=a3cd9182a2b2d3716623cc2c43d59f37&send_time=)的文章**“TB一周萃选[第7期]”**的归档。

![img{512x368}](../../assets/e125e43f9878f8d2.jpg)


我看过小马哥(哈维尔·马斯切拉诺)踢球，


你看过小马哥踢球，

他看过小马哥踢球。

我们看过小马哥踢球，

你们看过小马哥踢球，

他们看过小马哥踢球！— 改编自网络资料


都说三九天是一年中最冷的一段时间，但我们这里稍有偏差，就个人赶脚：四九、五九才是我们这里温度的最低点。这一周的感受用一句东北话来说就是**嘎嘎冷**！体感温度近零下30摄氏度：一开车门，好不容易凝聚在身体周遭的“热量”瞬间散失，似乎已经有10多年没有感觉到如此持续的寒冷了。

但巴萨新闻中的一则消息却让作为阿根廷和巴萨双重球迷的我感到了一丝温暖。北京时间本周五凌晨，在[巴萨](https://www.fcbarcelona.com/)主场与西班牙人队的国王杯四分之一决赛前，梦三主力、巴萨后防中坚小马哥携着自己的家人在巴萨队友的列队欢迎下、在诺坎普主场球迷山呼海啸般的欢呼声中走入诺坎普，和大家做着最后的告别。对于一名职业球员来说，这已经算是在俱乐部层面能得到的最高荣誉了。

虽说[梅球王](http://tonybai.com/tag/Messi)是我的最爱，但小马哥也是我十分喜欢和尊敬的一名足球运动员，在他的身上你几乎能够看到一名职业运动员所有的“正能量”标签：高超的专业能力、职业、自律、低调、坚毅、领导力、热爱足球、热爱家庭、没有绯闻等。对于小马哥这样的功勋球员，以“不只是一家俱乐部(Mes que un club)”为使命的巴萨俱乐部也做出了最大的让步，为小马哥设定了较低的转会费，让他可以按照自己的意愿成功转会到中超的华夏幸福。

小马哥将自己职业生涯中最好的七年奉献给了巴萨，对巴萨的贡献可谓是居功至伟！看看小马哥为巴萨赢得的荣誉吧。

![img{512x368}](../../assets/e17bc4841d5ff6b1.jpg)


感谢小马哥，祝福小马哥在后续的职业生涯中一切顺利！在中国生活的快乐！

## 一、一周文章精粹

### 1. Hello, 中国!

由于“众所周知”的原因，大陆地区的Gopher们在访问Go官方站点时十分困难。这一定程度上影响了Go在大陆地区的推广。但Go语言在大陆地区的发展势头让Go team看到了建立大陆地区mirror站的必要性。就在这一周，中国的Gopher们迎来了一个Go官方的好消息，那就是Go语言大陆地区官方网站上线了。网站的地址是https://golang.google.cn，这个网站目前就是Go官方站的mirror，很多深层的链接可能依然指向源站，不过迈出第一步总是好的。

文章链接：[“Hello，中国!”](https://blog.golang.org/hello-china)

### 2. 尚未修复的逃逸分析缺陷(Escape-Analysis Flaws)

[William Kennedy](https://github.com/goinggo)是著名的Go语言培训师，也是[《Go in action》](https://book.douban.com/subject/25858023/)这本书的作者之一，他在[Ardan Labs网站](https://www.ardanlabs.com/)上撰写了许多篇关于Go语言的学习资料。其中最新的一篇“Escape Analysic Flaws”探讨了当前Go compiler(截至到[Go 1.9](http://tonybai.com/2017/07/14/some-changes-in-go-1-9/))中依然存在的[逃逸分析](https://en.wikipedia.org/wiki/Escape_analysis)的缺陷，包括：

- Indirect Assignment
- Indirect Call
- Slice and Map Assignments
- Interfaces
- Unknown

Go实际编码过程中减少在heap上的内存分配是提升性能，减少cost的好方法，通过William的分析，我们也期望能做到尽量避免逃逸的情况，但有些时候做起来很难。因此，让Go compiler自身变得更聪明才是终极解决方法。

### 3. Github用户使用的编程语言排名

国外友人Ben Fredericksont通过对2011以来github的public event数据的分析，得出了关于github上编程语言的使用变化趋势，包括：top ten活跃语言、主流语言的活跃程度变化趋势、2018值得学习的几个热门新语言、几门趋势下降很快的语言、科学计算语言的变化趋势、函数式语言的变化趋势等。

![img{512x368}](../../assets/de819c6769cb1f9d.png)


图：2018值得学习的几个热门新语言

### 4. Nonblocking I/O指南

Go语言的默认的网络I/O编程模型是阻塞I/O，这可以大幅降低应用开发者在处理网络I/O时的心智负担。但这也仅限于“用户层面”，研究过[Go runtime调度](http://tonybai.com/2017/06/23/an-intro-about-goroutine-scheduler/)的gopher都知道，在runtime内部，关于网络I/O的调度实际上是Nonblocking的。imgix的工程师[Cindy Sridharan](http://twitter.com/copyconstruct)曾全面细致总结了对Nonblocking I/O的技术要点的理解，这里推荐给大家。

![img{512x368}](../../assets/a8566d694ca31e93.jpg)


文章链接：[“Nonblocking I/O”](https://medium.com/@copyconstruct/nonblocking-i-o-99948ad7c957)

### 5. 预测：2018年的最佳Linux发行版

[Linux内核](http://tonybai.com/tag/Kernel)已经成为这个星球上使用最为广泛的操作系统内核了，无论是云服务器，还是桌面机，从移动终端到Iot设备，现代人身边10米范围内，一般总能找出一台运行着Linux内核的设备。而对于用户而言，看到的更多是基于Linux内核的各种发行版，比如：Ubuntu、CentOS等。年初JACK WALLEN在linux.com博客上撰文预测了2018年各个领域的最佳Linux发行版，包括从sysadmin、桌面版、server版、便携版、iot版等多个方面。这些预测基于distrowatch.com上各个发行版的人气排名。

文章链接：[“best linux distributions for 2018”](https://www.linux.com/blog/learn/intro-to-linux/2018/1/best-linux-distributions-2018)

### 6. 如何使用Go语言创建基于AWS Lambda的serverless应用

[AWS Lambda宣布支持Go](https://aws.amazon.com/cn/blogs/compute/announcing-go-support-for-aws-lambda/)不久，各路关于如何使用Go在AWS Lambda创建serverless应用的资料便接踵踏来。这里推荐的就是其中的一篇。对于想使用Go在AWS Lambda上“尝鲜”的Gopher们，这是个不错的入门文章。

![img{512x368}](../../assets/351941e4e86640a4.png)


文章链接：[“Serverless Golang API with AWS Lambda”](https://read.acloud.guru/serverless-golang-api-with-aws-lambda-34e442385a6a)

### 7. JavaScript框架终极指南

JavaScript这门语言虽然“颜值”不那么高，但这并不妨碍它抱上浏览器这一“大腿”，并还进军了服务端市场。在这一过程中，JavaScript领域诞生了诸多Framework，最出名的莫过于三巨头：[Angular](https://angular.io/)、[React](https://reactjs.org/)和[Vue.js](https://github.com/vuejs)这三个框架了。除此之外，还有太多我甚至没有听过名字的框架。这里推荐的“JavaScript框架终极指南”一文就是对JavaScript目前的主流框架的状态、优劣势进行详细总结说明的一篇文章，希望能帮助你挑选出最适合你的Js框架。

![img{512x368}](../../assets/8ff22e88f483eebb.png)


文章链接：[“The Ultimate Guide to JavaScript Frameworks”](https://javascriptreport.com/the-ultimate-guide-to-javascript-frameworks)

## 二、一周资料分享

### 1. ROSCon 2017资料

[ROS](http://tonybai.com/2017/08/01/hello-ros/)作为世界上应用最为广泛、最具影响力的开源机器人操作系统，它从2012年开始举办的ROSCon大会就备受关注，2017年ROSCon大会在加拿大温哥华举行。在人工智能、智能驾驶如此“热”的今天，ROS作为很多智能驾驶平台（比如百度的[Apollo](http://tonybai.com/2017/08/15/hello-apollo/)、[tierIV](https://www.tier4.jp/)的[autoware](https://www.autoware.ai/)等）的底层支撑组件自然吸引了自全世界范围内的学者和工程师的眼球和参与。这次大会的topic是干货满满，由于是[ROS2](https://github.com/ros2/ros2)发布正式版前的最后一次大会，因此涉及ROS2的topics十分多，算是为ROS2正式登场预热(注：ROS2在2017.12.10正式发布，代号：Ardent Apalone)。

![img{512x368}](../../assets/87130ee5de7bf0ad.png)


资料分享链接：[“ROSCon 2017资料”](https://roscon.ros.org/2017/)

## 三、一周工具推荐

### 1. carbon：一款源码图片创建和分享的工具

在技术文章写作中，我们会有大量的代码截图的需求，但限于客观原因，截图的质量和风格难于把控。Carbon这个工具就是来帮助解决这个问题的。Carbon是一个在线服务，支持通过将源码文件拖拽到生成框中自动生成代码图片。Carbon支持几乎所有主流语言，并可以自动识别，并且Carbon支持多种风格的代码高亮样式，比如：Monokai、Solarized等。

![img{512x368}](../../assets/8c4b4f65ac96d94a.png)


图：Carbon主页

![img{512x368}](../../assets/5a6fbee70e13c41c.png)


图：Carbon生成的Go源码图片

推荐工具链接：[Carbon](https://carbon.now.sh)

## 四、一周图书推荐

### 1.《Hello World! Second Edition – Computer Programming for Kids and Other Beginners》

都说00后是互联网时代的原住民，那么伴着这轮AI热，我们是否可以大胆地说2020后或2025后是AI时代的原住民呢。这让我仿佛看到了“[超能陆战队](https://movie.douban.com/subject/11026735/)”中男主小宏所使用的IT装备和掌握的编程技能。也许在未来10年后，编程就会像数学、语文一样成为在AI时代的基本技能。而这一切都要从娃娃抓起，从编程基础抓起。Sande父子合作编写的这本《Hello World》图文并茂地将孩子带入二进制的程序世界，孩子将在轻松惬意的氛围中学习基础的编程概念：如内存、循环、输入和输出、数据结构和图形用户界面等。对于如今智力水平普遍较高的孩子们来说，这些内容就像小游戏般容易掌握。书中使用的教学语言是[Python](http://tonybai.com/tag/python)，别忘了目前的Python可是AI时代的top3语言，并是AI第一语言的强有力的竞争者。

很多人说：当前儿童编程的第一语言是MIT的[Scratch](https://scratch.mit.edu/)，我不能否认这一点，Scratch就是为Kids们所创造的，它是MIT继[Seymour Papert教授](https://en.wikipedia.org/wiki/Seymour_Papert)在创建[LOGO语言](https://turtleacademy.com/)、探索儿童编程教育后的又一杰作。全图形化的编程教学让孩子们很是喜欢。但我个人觉得如果能结合一些真实代码，尤其是对于中高年级的学生来说，将是大有裨益的。

作为Gopher，我一直在想足够简洁的Go语言也是可以作为儿童编程教学语言的，希望能早日出现一门以Go语言为第一教学语言的儿童编程图书。

![img{512x368}](../../assets/0e2b788678363abf.png)


图书链接：

[《父与子的编程之旅 – 与小卡特一起学Python》](https://book.douban.com/subject/26005639/)

[《Hello World! Second Edition – Computer Programming for Kids and Other Beginners》](https://www.manning.com/books/hello-world-second-edition)

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：http://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/71dbd0d64d261ba9.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论