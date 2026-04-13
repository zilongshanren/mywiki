---
title: 关于在线代码评审的几点考量
url: https://tonybai.com/2010/12/18/thoughts-on-online-coding-review/
published: '2010-12-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 关于在线代码评审的几点考量

记得上次折腾[Review Board](http://tonybai.com/2009/09/19/review-board-installation-and-configuration/)这个在线代码评审工具还是在一年前，那时的[Review Board](http://www.reviewboard.org)版本是1.0.3；这周部门的一位同事也在折腾Review Board，不过现在的版本已经升级到了1.5.1了。新版Review Board显然修正了许多旧版本中[存在的问题](http://tonybai.com/2009/10/05/chinese-support-for-review-board/)，另外无法支持ssl邮件端口的问题也被我这位同事通过更换django源文件的方式搞定了。Review Board好用了，下一步需要关注的就是怎样才能用好Review Board的问题了。

一般认为[代码评审](http://tonybai.com/2006/05/31/code-review-is-necessary/)是一项优秀的软件开发实践，它可以将很多隐患和bug消灭在萌芽阶段。其实践形式大致有代码走查、代码审查和结对编程（每时每刻都在做代码评审）这三种。一般来说读懂别人的代码可能比自己亲自编写代码花费的时间还要长，而且更为困难，所以除了结对编程之外，代码走查和审查都是低效的，多数情况下都是高投入低产出的，引入在线评审恰恰是对这些低效代码评审形式的一个有效补充，另外在线评审更适合异地团队和开源项目。

那么什么情况下适合发起在线Code Review Request呢？可考虑下面几种情况：

- 新增的关键功能代码的评审

- 系统改善或优化代码的评审

- bugfix代码的评审

- 一些试验性代码的可行性评审

创建一个新的Review request时应考虑注意以下几点：

- 精确描述review request，提供此次评审的重要关注点；

- 每个review request要有针对性，选择合适的评审人，不要泛泛的发给所有人；

- 明确此次评审的截止时间点；

- 每个review request所包含的待评审代码的行数最好不要超过50行，以30行以内为佳。如果你的request中包含了上千行的代码，我想是没人会去真正评审你的代码的。

在项目编码高峰期，切忌发起大量在线Review request，那样的话，大家都会"淹没"在诸多Requests中，评审质量会严重下降，评审人的热情也会受到打击^_^。这个时候我们可以考虑结合其他评审方式，如采用结对和走查。另外对于一些遗留的维护项目，由于代码历史较为"悠久"，相关干系人较多，无法确认的因素也较多，可通过在线评审方式将review request发给相关干系人，以获得全面的评审，避免死角。

以上是目前关于在线代码评审的一些考量，这里记之以备忘。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 仅有 1 条评论