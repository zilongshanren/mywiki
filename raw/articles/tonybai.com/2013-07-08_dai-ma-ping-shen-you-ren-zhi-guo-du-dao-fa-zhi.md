---
title: 代码评审，由人治过渡到“法治”
url: https://tonybai.com/2013/07/08/code-review-from-rule-of-man-to-rule-of-law/
published: '2013-07-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 代码评审，由人治过渡到“法治”

事实证明：有效的[代码评审](http://tonybai.com/2011/02/22/code-reviews/)(Code Review，也有叫代码审查的），对保证代码质量具有十分重要的作用。因此这两年来我一直尝试着在这块不断改进和完善，以期望能形成一套合理、规范、有 效且高效的代码评审流程，这包括引入[在线代码评审系统](http://tonybai.com/2010/12/18/thoughts-on-online-coding-review/)、走查和在线评审结合、规范评审Request的规模与有效性、设立评审专员等，用心不可谓不良苦 ^_^。大家也的确形成了及时提交Code Review Request或组织进行代码走查的良好习惯。不过我还是发现了一些问题。

* 有些组（我对其影响力不足的^_^）依旧没有严格执行代码评审环节，代码屡屡出现低级错误；

* 走查形式的会议评审缺乏全面性，效果好坏与参与者的“状态”直接相关；

* 在线评审环节缺乏“责任制”，常出现的一种情况是：请求大家评审，结果可能却是大家都没有评审。出现"Request Review Miss"的现象。

这让我陷入思考：长期以来我们在代码评审这块过于依赖人的自觉性，理想地认为每个人都能认识到代码评审的重要性，并认真地执行代码评审的流程或充满激情地 参与到其他人发起的代码评审过程中去，但结果事与愿违。这就像党员如何保持纯洁性一样，如果仅仅依靠个人道德/职业水平约束，这事往往是不成的。事实证明 人治在中国社会是会造成各种社会问题的。我们的代码评审环节也是一样，我们不能再期望所有人都能和我站在一条认知和激情水平线上，于是我打算尝试向“法 治”过渡。

"法"，规则制度也，是团队一致认同的可以提升产品质量的规则制度。以此为前提，我要做的就是设立“检查和预防”机构，即以很低的Cost，检查大家是否按“法”完成了代码评审环节，提醒大家要按“法”进行。我采取了几个措施：

**【规范Commit Log ****】**

这是一个前提工作。实现规范的[Commit Log](http://tonybai.com/2013/05/09/also-talk-about-commit-log/)便于后续的检查和监督，同时细化规范的Commit Log信息对代码维护是大有裨益的。在Commit Log中还增加了一些关联信息，方便维护者了解该Commit的背景。初期的模板是这么来确定的：

模板结构：

*TITLE*

*BODY*

*RELATIONSHIPS*

展开后如下：

*[Category] Title content*

*Body content*

*[BUGID] QC#733 | JIRA#766*

*[REVIEWID] RB#767*

*[REVIEWED BY] xx, yy, zz*

*[SIGNOFF BY] xx*

TITLE Category：

– BUGFIX 代码修复

– FEATURE 新功能特性添加

– TASK 诸如代码美化、调整版本号等

– URGENT 紧急提交，对此类commit，可不做review和拦截

BODY Content：

有关此次修改的详细信息说明

RELATIONSHIPS：

– [BUGID] 一般用Bug跟踪系统的ID号

– [REVIEWID] reviewboard上的ID号

– [REVIEWED BY] xx, yy, zz

– [SIGNOFF BY] xx

**【"全覆盖"原则**】

所有变更代码都要发起在线“Code Review Request”，即便是会议走查的代码，会后也要补提“Review Request”。

**【“低保”原则**】

每个Review Request至少选择两名评审负责人，填到"Request"中，这两个人必须对此Request给出评审意见，这是一个评审的**最低保障**了，这总比没有人评审要好。当然了其他人也都可以参与评审。只有这两名评审负责人明确提交"ship it" Comment后，该代码才算是通过评审。

**【关键路径拦截】**

"对不起，若不符合规定，你的工作将无法进行下去"。有了统一的Commit Log模板，我们就可以对大家的代码Commit环节做检查和[拦截](http://tonybai.com/2010/08/07/use-svn-pre-commit-hook/)了。如果代码没有进行评审，无法填写模板中的字段内容，那代码将无法提交到代码库中。如 果虚构Commit log内容，这将是极大的错误，在抽查中一旦发现，后果将是很严重的^_^。

当然这一过程中还有很多细节需要考虑，比如Reviewer的选择不能集中在一个人身上，否则会造成热点；再比如紧急提交代码应该如何处理等等。“法治” 是与一定的“国情”相匹配的，并不是所有的组织都需要进行这么严格且略有死板“法治”手段，依团队内组员的专业能力和认知水平而定。

有些公司开发了自己的统一开发平台，将一系列流程都在一套系统中规范了起来，这当然是更好的“法治”了。但在没有这样的平台的前提下，初步使用上述的几个手段，还是会收获一些改进的。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论