---
title: 读《How Google Tests Software》
url: https://tonybai.com/2012/07/10/read-how-google-tests-software/
published: '2012-07-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 读《How Google Tests Software》

一直对Google这个牛X公司的内部开发过程很是感兴趣，毕竟像[Google Search Engine](http://www.google.com)、[Google云计算平台](https://appengine.google.com)这些伟大产品都是在这个开发过程下缔造出来的。但也许是Google保密工作做的很好，或许人家不是刻意保密，只是 因为工作太忙或人员太低调，没空派人出来宣讲罢了。外界对Google内部的开发流程知之甚少；知道一些，诸如20%项目，也只是皮毛。

终于有一天，Google的三位工程师冒了出来，为我们带来的了一本名为《[How Google Tests Software](http://book.douban.com/subject/7065508)》的小书。我断断续续用了不到一周时间粗略地浏览了一遍这本书，算是对神秘的Google内部开发过程有了初步的了解了。其中有一些思路 还真是值得我后续深入思考，这里仅列出一些让我心有所触的"点"，与大家共享。

书是从Test角度展开的，但Google的Test与我们所熟知的Test还有不同，包括这个过程的角色设置与职责等。下面是从书中摘录的一些语句(有些地方是我总结后的)和观点，再加上我的一些体会。

1、在Google，Software Testing被称作"Engineering Productivity(工程效率)"，既负责开发和测试工具的开发、发布工程，还负责从单元测试(unit level)到探索性测试(exploratory testing)的全过程。


— 在国内，多数公司的Testers只负责测试过程，而且多从功能测试开始，Unit test是开发人员的责任。大部分公司的开发与测试工具都是开发人员设计和实现的，但也有少部分先进的公司有专职的测试工具开发岗。总体来 说，Google内部的"测试人员"角色是与众不同的。

2、"Quality is a development issue, not a testing issue"、

"At Google, this is exactly our goal: to merge development and testing so that you cannot do one without the other. Build a little and then test it. Build some more and test some more. " 、

"The reason Google can get by with so few dedicated testers is because developers own quality.If a product breaks in the field, the first point of escalation is the developer who created the problem, not the tester who didn't catch it."

"Testing must be an unavoidable aspect of development, and the marriage of development and testing is where quality is achieved."

— 可以看出Google信奉："Developer是质量的owner，是第一责任人；质量应该由开发人员把关；测试是开发过程必不可少的一方面；将开发与 测试融合在一起以获取更高的质量；开发一些，测试一些(迭代的思想)"。而国内多数组织依旧信奉着测试是软件质量的最后保证这一信条，将开发和测试隔离的 很开。


3、Google内部开发测试过程的三个角色：software engineer (SWE) 、software engineer in test (SET)和 test engineer (TE)，Google SWEs are feature developers. Google SETs are test developers. Google TEs are user developers.

— 在Google，似乎没有纯粹的传统意义上的Testers，按照书中所讲，SWE肯定是开发工程师，负责实现产品功能(feature)，而SET，其 实也是开发工程师，用于编写产品的测试Feature，关于测试Feature这个概念很独特，Google认为，产品应该有两种Feature属性，一 种是function feature，一种则是产品的test feature，而SWE和SET则分别focus这两点。SWE和SET共享同一代码库，是开发过程中的Partner。与SWE关注功能 feature不同，SET更加关注产品的可测试性、如何通过测试提升产品质量以及提升测试覆盖率以及产品性能。他们为产品的feature编写测试代 码，从单元测试到后续的各种测试，编写各种工具，并尽量的将测试自动化，提升测试效率。

而TE这个角色则有些类似传统的Testers，但在Google也有不同。在Google，TE更多是从user角度去探索产品，有的TE会编写大量脚 本代码，模拟user使用产品的各种场景；按照书中的说法："TEs are product experts, quality advisers, and analyzers of risk"。

4、One of the key ways Google achieves good results with fewer testers than many companies is that we rarely attempt to ship a large set of features at once.

— 显然Google也倾向于增量的迭代开发，这种模式符合Google内部的role设置，同时，这种role设置也更好地促进了增量迭代开发的顺利高效开展。

5、Build the core of a product and release it the moment it is useful to as large a crowd as feasible, and then get their feedback and iterate. This is what we did with Gmail, a product that kept its beta tag for four years.

Google often builds the minimum useful product as an initial version and then quickly iterates successive versions allowing for internal and user feedback and careful consideration of quality with every small step. Products proceed through canary, development, testing, beta, and release channels before making it to users.

— 这似乎就是Google著名的"Beta"模式，目前很多互联网企业(特别是startup)均效仿之。

6、Instead of distinguishing between code, integration, and system testing, Google uses the language of small, medium, and large tests, emphasizing scope over form.

Small tests cover a single unit of code in a completely faked environment. Medium tests cover multiple and interacting units of code in a faked or real environment. Large tests cover any number of units of code in the actual production environment with real and not faked resources.

The general rule of thumb is to start with a rule of 70/20/10: 70 percent of tests should be small, 20 percent medium,

and 10 percent large.

— Google内部的测试不是按照代码[单元测试](http://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/)、集成测试以及系统测试这些典型的阶段划分的，而是用"small、medium、large、 enormous"这些词汇来描述测试的各个环节，这些词汇也是Google内部的"共同语言"。如何界定这些测试的scope呢？Google内部有一 套共享的测试执行系统，它通过test size来界定不同的test类型。比如：对small tests的要求是每方法(method)的测试执行时间不能超过100ms，如果1分钟仍然执行不完，则将被kill掉。

7、Keeping it simple and uniform is a specific goal of the Google platform: a common Linux distribution for engineering workstations and production deployment machines; a centrally managed set of common, core libraries; a common source,

build, and test infrastructure; a single compiler for each core programming language; language independent, common build specification; and a culture that respects and rewards the maintenance of these shared resources.

— 在Google内部一切都是"整齐划一"的，大大降低了各种人员在熟悉、学习和使用过程中的工作量。可以看出，Google为了提升内部开发效率，真是无 所不用其极啊。另外Google内部这套完整的强大的基础设施工具、库、语言以及流程支撑想必也让大家垂涎三尺吧。

8、There is no set rule at Google for when SETs engage in a project, as there are no set rules for establishing when projects become “real.” A common scenario for new project creation is that some informal 20 percent effort takes a life of its own as an actual Google-branded product. Gmail and Chrome OS are both projects that started out as ideas that were not formally sanctioned by Google but overtime grew into shipping products with teams of developers and testers working on them.

No project gets testing resources as some right of its existence. The onus is on the development teams to solicit help from testers and convince them that their project is exciting and full of potential.

— 这两段话既描述了SETs进入项目的时机，同时也从侧面反映出了Google内部产品的初期形成机制。在这种机制下，一些著名产品诸如Gmail、 Chrome等诞生了。个人很是认同这种自底向上的产品"产生机制"，有利于员工创造力的充分展现。其实退一步来说，我们不一定非要公司明确规定设置 20%个人时间，只是我们在平时工作中主动去发现、去分析、思考和总结，我们一样可以"创造"出一些用于改善我们工作和生活的工具或产品，这些"成果"在 我们的日常工作中使用，逐渐被大家所接受，甚至于发展演化成熟，形成一个可盈利的产品或是贡献给开源社区，不是一样很好么。感觉国内的很多互联网公司里面 的一些同行正在做这些事情。

9、This is the convention at Google: Make the common case fast.

— 这显然已经上升到了哲学的层次，不仅对开发测试过程的效率改进有着指导意义，对软件自身的调优也是一样富有价值。甚至于对我们的日常生活也是有帮助的。

10、Designs that seek to automate everything end-to-end all in one master test suite are generally a mistake. The larger an automation effort is, the harder it is to maintain and the more brittle it becomes as the system evolves. It’s the smaller, more special purpose automation that creates useful infrastructure and that attracts the most SWEs to write tests.

Overinvesting in end-to-end automation often ties you to a product’s specific design.

– 这又是Google内部对[自动化测试](http://tonybai.com/2011/10/31/improving-efficiency-should-not-only-be-a-slogan/)的一种中肯的实用的理解。我们要自动化，但要掌握方法，不要大而全，要小且精，吸引SWE自己去写测试代码。过分追求全闭环的自动化测试会将你与一个产品的细节间建立依赖。

11、Google centers its development process around code reviews. There is far more fanfare about reviewing code than there is about writing it.


These pre-submit rules cover simple things such as adherence to the Google coding style guide and more involved things such as ensuring that every existing test associated with the CL has been executed (the rule is that all tests must pass).

— Google打造了一个以[代码评审](http://tonybai.com/2011/02/22/code-reviews/)为中心的开发过程，建立了一套完整的日常开发流程以及评审流程。并通过一套完整的工具平台在代码提交评审前对代码进行各种自动化检查，让评审过程更加focus关键业务逻辑，而不是语法之类的细节。

12、Test Runtime Requirements

– Each test must be independent from other tests so that tests can be executed in any order.

– Tests must not have any persistent side effects. They must leave their environment exactly in the state when it started.

— 这里点明测试执行的原则：测试case间无依赖，可任意顺序执行；测试执行应遵循"[童子军](http://tonybai.com/2011/04/23/the-boy-scout-rule/)"纪律：测试执行结束后，将环境恢复到测试起始状态。

13、带认证的测试(Test Certified)

— Google内部建立了类似竞赛似的规则，对每个项目的测试水平进行认证，分为几个级别：从TC level1到TC level5。对于每个级别都有明确的指标，甚至是明确的达标数字，比如总测试覆盖率，各种类型(比如small)测试的覆盖率等。在每个项目的首页都会 看到该项目的认证级别。这种规则将促使项目SWE和SET不断地改善测试，来提升测试认证水平，间接地提升了产品的质量。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论