---
title: 图解3GPP规范文档组织结构与编号规则
url: https://tonybai.com/2019/07/25/illustrate-3gpp-spec-docs-structure-and-numbering/
published: '2019-07-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 图解3GPP规范文档组织结构与编号规则

[3GPP](https://www.3gpp.org/)组织（3rd Generation Partnership Project）是全球移动通信业标准制定之执牛耳者。其最初的工作范围是为第三代移动通信系统制定全球适用的技术规范(TS，Technical Specification)和技术报告(TR，Technical Report)，确保不同厂商之间实现无缝互操作以及为移动通信提供其所必需的全球规模，从而达成实现GSM由2G网络到3G网络的平滑过渡的要求。随着3GPP组织在全球影响力的逐渐扩大，3GPP也承担起了建立和统一[4G](https://en.wikipedia.org/wiki/4G)、[5G](https://en.wikipedia.org/wiki/5G)标准的重任，从这方面来看，3GPP改名为NGPP(Next/Nth Generation Partnership Project)似乎更加合适:)。

![img{512x368}](../../assets/1f04afa7e563b68c.png)


从1998年成立至今，3GPP组织制定了大量的标准规范，累积起来有数百个标准文档，这给初次接触3GPP规范的朋友出了一道难题：**如何找到我所需要的那个规范文档呢？**

近期因为业务需要在阅读3GPP有关[短信](https://tonybai.com)、[C-V2X](https://en.wikipedia.org/wiki/Cellular_V2X)方面的规范文档，这也是我第一次近距离接触3GPP规范，为了找到自己想要的规范文档，也真实经历了一番周折。于是有了编写这篇博客的想法，希望大家通过这篇文章，可以了解3GPP规范文档的组织结构以及每个文档的编号规则，实现快速精确找到所需规范文档的目的。

## 一. 3GPP规范文档组织结构

通常3GPP规范文档是通过文档编号或文档名称(title)进行查找的，这里推荐一个3GPP文档汇总页面：[“3GPP Specification Release version matrix”](https://www.3gpp.org/DynaReport/SpecReleaseMatrix.htm)，建议将之保存到浏览器书签中。

![img{512x368}](../../assets/64e706f97d2ee1e7.png)


该页面以3GPP规范Release版本的维度将所有已完成且正式发布的文档列在一个页面上，截至笔者编写这篇文章时，最新的Release版本是**Rel-15**。

我们简单看看上面图中各个列的含义：

-
Spec no. – 规范文档编号

-
Title – 规范文档的名称

-
WG – 工作组

-
Ph1 ~ R00 – 适用于早期GSM的规范发布版本

-
Rel-4 ~ Rel-15 – 适用于GSM、3G以及后续新通信技术的规范发布版本


要进一步了解某个规范的详细信息并下载规范文档，可以点击对应的文档编号：

![img{512x368}](../../assets/a0e2bc3223092604.png)


点击后，进入规范的portal页(默认general，以规范21.905为例)：

![img{512x368}](../../assets/0fd040160d9235da.png)


在general页面上，我们能看到对应规范的status、type(TS/TR)、首次发布时间、适用的无线技术(2G/3G/LTE/5G)等。

点击”Versions”标签进入规范的版本历史页面：

![img{512x368}](../../assets/8cc4e5070912723d.png)


在该页面，点击规范对应的版本编号即可下载对应版本的文档(zip格式，解压后为doc/docx文档)。

3GPP还提供了其他多种spec文档的归集方式，比如按照[Release版本](https://www.3gpp.org/releases)、[技术关键字](https://www.3gpp.org/technologies/keywords-acronyms)、[当前Specs状态](https://www.3gpp.org/ftp/Specs/html-info/status-report.htm)查看，也可以在[归档FTP](https://www.3gpp.org/ftp/Specs/archive/)中自行翻找:)。

个人觉得[spec release matrix页面](https://www.3gpp.org/DynaReport/SpecReleaseMatrix.htm)仍然是3GPP入门朋友的最佳入口。

## 二. 3GPP规范文档编号与版本规则

下面我们聚焦到某些具体的规范文档：

-
[《Vocabulary for 3GPP Specifications》](https://www.3gpp.org/DynaReport/21905.htm)：文档编号为**21.905**, 最新Version：15.1.0； -
[《Attachment requirements for Global System for Mobile communications (GSM); Advanced Speech Call Items (GSM-ASCI) Mobile Stations; Access》](https://www.3gpp.org/DynaReport/1368.htm)：文档编号为**13.68**，最新version: 5.0.2;

我们看到每个文档都有两个重要属性信息：[规范文档编号(Specification Number)](https://www.3gpp.org/specifications/specification-numbering)和[版本号(Version)](https://www.3gpp.org/Version-Numbering-Scheme)。我们用一幅图来解释一下文档编号和版本号的用途：

![img{512x368}](../../assets/a8f06dff9b0918f4.png)


从图中我们可以看到：

-
规范文档编号由两部分组成：系列号(series number)和尾号(mantissa，也称为文档号)，两个部分之间用“.”分隔；

-
系列号(series number)是从00开始的两位数字；XX.YY形式是早期规范文档的编号形式，用于00~13系列文档，适用于早期GSM系统(即Rel-4之前的GSM)；而XX.YYY形式是后期，也是当前使用的编号形式，用于41~55系列（仅GSM）和21~38系列(3G及新一代系统)；

-
规范文档编号中的尾号(文档号）没有特别的意义，早期使用两位尾号，现在都使用三位尾号；

-
规范文档的版本号由三位从0开始的数字组成，数字间由“.”分隔；

-
版本号从左到右的第一位是major域，表示该文档所处的主要阶段：

- 0 =不成熟的草案
- 1 =至少完成60％的草案已经提交/将很快提交给负责的TSG以供参考
- 2 =完成至少80％的草案并已提交/将很快提交给负责的TSG批准
- 3或更高=已经由负责的TSG批准并且处于变更控制之下的规范。

-
版本号从左到右的第二位是technical域（技术域），对规范进行技术更改时，技术域字段会递增；

- 版本号从左到右的第三位是editorial域（编辑域）；每次对规范进行非技术性更改时，编辑域字段都会递增，例如，纠正印刷错误。但任何可能会对规范技术规定的解释产生影响的变化都不能被视为编辑域变化。
- 从Rel-4发布开始,3GPP规范的Release和Version有了对应关系。一个规范文档的Version的major域的值将会指示出该规范所适用的 Release，这样达到了Release和Version在某种程度的一致性，方便规范读者查询。

我们还以编号和版本为**21.905 15.1.0**的规范为例，从其编号和版本信息，我们直接可以得到如下结论：

-
该规范术语21系列，适用于3G及新一代系统范畴；

-
该规范已经正式发布，该版本发布于Rel-15；

-
该规范在Rel-15有一次技术性更改。


## 三. 规范文件名规则

最后我们还要了解一个规则，那就是规范文档对应的实体文件的文件名起名规则，规范对应的实体文件的文件名与那规范的文档编号及版本具有一定对应关系。

我们还是用一幅图来形象展示一下文件名规则：

![img{512x368}](../../assets/9f9b47fde7f425fc.png)


从图中我们可以看到：

-
规范文档对应的实体文件名由多部分组成，其中文件名首部是必选的，它由规范编号和尾号组成(中间无分隔)；文件名尾部也是必选的，由规范的版本号组成；中间的part number和sub-part number是可选的。文件名各部分之间由“-”连接；

-
part number和sub-part number都是1或2位数字；

-
文件的尾部对应着规范的版本号，不同的是文件中尾部的版本号中的每个域都是一个有序字符集合[0~9、a~z]中的字符，这个集合中有36个字符按需依次对应着版本号中的0~35，如果版本号中的某个域值超过35，则文件名中的版本号中的每个域都使用两位表示。举例：

-
TR 21.900的版本

**15.1.1**对应文件名21900-f11.zip中的**f11**；（f对应version中的15) -
TS 34.567的版本

**16.36.0**对应文件名34567-163600.zip中的**163600**；(technical域为36,超过35，因此文件名中尾部版本号每个域占用两位)

-

现在如果我们看到一个文件名，即可得到关于规范文档的一些信息，比如：

-
21900-320.zip对应21.900 v3.2.0规范

-
0408-6g0.zip对应的是04.08 v6.16.0规范

-
29998-04-1-100.zip对应的是29.998 part 04 subpart 1 v1.0.0规范

-
29898-133601.zip对应的是29.898 v13.36.1规范


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论