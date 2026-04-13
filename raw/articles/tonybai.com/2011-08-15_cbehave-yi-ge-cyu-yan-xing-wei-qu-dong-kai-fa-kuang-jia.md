---
title: CBehave – 一个C语言行为驱动开发框架
url: https://tonybai.com/2011/08/15/cbehave-a-bdd-framework-for-c/
published: '2011-08-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# CBehave – 一个C语言行为驱动开发框架

[Behaviour-Driven Development](http://behaviour-driven.org/)，即行为驱动开发在业界早已不是什么新鲜玩意了。我之前也略有了解，不过一直没有"深入钻研"。直到今年年初InfoQ的几篇有关BDD的文章才让我对BDD有了更多的认识。与[TDD](http://en.wikipedia.org/wiki/Test-driven_development)一样，C语言在BDD领域依旧是一个"后进分子"，在多数主流语言(Java，C#，Ruby等)都已经拥有比较成熟的BDD框架(如[JBehave](http://jbehave.org/)、[SpecFlow](http://specflow.org/)和[Cucumber](http://cukes.info/))的今天，C语言却似乎仅有一款BDD框架-[CSpec](https://github.com/arnaudbrejeon/cspec)可用。于是年初的时候我就把设计和实现一个用于C语言的行为驱动开发框架加入到我今年的ToDoList中了。

在确定好目标的同时，我也给这款框架命名为[CBehave](http://code.google.com/p/cbehave)(模仿JBehave)，并在Google Code上建立了CBehave的托管项目。但人的时间和精力总是有限的，直到8月中旬我才开始着手进行这个框架的设计和实现。设计和实现一款给程序员使用的工具，这本身就是一件让人兴奋的事情。我先是通过DanNorth的博文"[Introducing BDD](http://dannorth.net/introducing-bdd/)"(其中译版在[这里](http://tonybai.com/2011/08/10/introducing-bdd/))了解了BDD的"诞生历程"，然后又广泛地了解了一下其他语言的BDD框架。对于CSpec这一目前唯一的C语言BDD框架，我并不想给予过多评价，不过总体来说和其他语言的BDD框架相比，CSpec有些简陋，应该说还无法很好的支持BDD中一些核心思想的表达，并且目前它还不支持[Mock](http://tonybai.com/2008/04/12/mock-test-in-c-unit-test/)。这些都坚定了我重新实现一个C语言BDD框架的决心，起码我不完全是"重新发明轮子"^_^。

作为后来者，CBehave的设计参考了诸多现有的主流BDD框架，其中直接灵感来源于Cucumber，不过由于C语言静态编译语言的本质，CBehave与Cucumber在大多地方也只是形似而已。作为一篇CBehave的介绍性文章，这里列举一些CBehave的主要特点：

首先，CBehave借鉴Cucumber的设计采用Feature + Scenario结合的方式来描述功能需求(DanNorth: 需求也是行为)，并且在每个Scenario内部采用BDD的经典的GIVEN-WHEN-THEN结构描述行为的验收标准(acceptance criteria)。

这里给出一个总体的行为描述模板：

FEATURE #1

SCENARIO #1

GIVEN

… …

WHEN

… …

THEN

… …

SCENARIO #2

GIVEN

… …

WHEN

… …

THEN

… …

… …

FEATURE #2

… …

FEATURE #n

原则上FEATURE之间是相互隔离的；FEATURE内部的多个Scenario之间在代码定义和执行时也是相互隔离，互不干扰的。这是一个使用该框架的基本约束。不过这就好比建议性锁，全靠使用时的自觉，否则很容易造成框架运行出错。

下面是一个真实的使用CBehave对strstr函数进行测试的例子(代码片断，完整例子参见源码cbehave/src/example/string_test.c)：

FEATURE(1, "strstr")

SCENARIO("The strstr finds the first occurrence of the substring in the source string")

GIVEN("A source string: [Lionel Messi is a great football player]")

char *str = "Lionel Messi is a great football player";

GIVEN_END

WHEN("we use strstr to find the first occurrence of [football]")

char *p = strstr(str, "football");

WHEN_END

THEN("We should get the string: [football player]")

SHOULD_STR_EQUAL(p, "football player");

THEN_END

SCENARIO_END

SCENARIO("If strstr could not find the first occurrence of the substring, it will return NULL")

GIVEN("A source string: FC Barcelona is a great football club.")

char *str = "FC Barcelona is a great football club";

GIVEN_END

WHEN("we use strstr to find the first occurrence of [AC Milan]")

char *p = strstr(buf, "AC Milan");

WHEN_END

THEN("We should get no string but a NULL")

SHOULD_STR_EQUAL(p, NULL);

THEN_END

SCENARIO_END

FEATURE_END

int main() {

cbehave_feature strstr_features[] = {

{feature_idx(1)},

};

return cbehave_runner("Strstr Features are as belows:", strstr_features);

}

编译运行这个测试，我们会得到如下结果(节选)：

Strstr Features are as belows:

Feature: strstr

Scenario: The strstr finds the first occurrence of the substring in the source string

Given: A source string: Lionel Messi is a great football player

When: we use strstr to find the first occurrence of [football]

Then: We should get the string: [football player]

Scenario: If strstr could not find the first occurrence of the substring, it will return NULL.

Given: A source string: FC Barcelona is a great football club.

When: we use strstr to find the first occurrence of [AC Milan]

Then: We should get no string but a NULL

Summary:

total features: [1]

failed features: [0]

total scenarios: [2]

failed scenarios: [0]

CBehave将strstr的行为原汁原味地输出到最终的测试结果中，与xUnit等框架相比，这确是一个进步，我们在获知测试结果的同时，还依稀中看到了这个特性的需求描述，前提是你要给出一个很好很精确的描述，但这已经不是框架可以帮助你做的了^_^。另外即使你的测试失败了，你甚至可以不通过错误提示中的源码文件名和行号信息也可以快速定位到错误的位置所在。因为错误周围是有足够的上下文信息的。

其次，CBehave支持mock。CBehave中mock的实现完全参考了我之前设计的单元测试框架[LCUT](http://code.google.com/p/lcut)，下面是一个简单的例子(片断，完整代码参加cbehave/src/example/product_database_test.c)：

FEATURE(1, "Get the total count of employees")

SCENARIO("Get the total count of employees")

GIVEN("The db connection is ready and there are 5 employees in total");

CBEHAVE_RETV_RETURN(connect_to_database, 0×1234);

CBEHAVE_ARG_RETURN(table_row_count, 5);

CBEHAVE_RETV_RETURN(table_row_count, 0);

GIVEN_END

WHEN("We call function: get_total_count_of_employee");

int count = get_total_count_of_employee();

WHEN_END

THEN("The total count of employees we read from db should be 5")

SHOULD_INT_EQUAL(count, 5);

THEN_END

SCENARIO_END

FEATURE_END

最后，CBeahve还支持多种SHOULD_XX宏，并且可根据需要灵活添加。目前已支持整型、字符串以及布尔类型的判定。

关于CBehave的实现历程这里也简单说一下。

首先需要确定CBehave的"长相"，也就是CBehave采用的行为描述模板是啥样子的。这块儿确是花了我不少的时间，查看各种资料以及研究其他框架的设计，最终选择了Feature+Scenario以及用Given-When-Then来描述行为的"文档模板"。

其次，有了"文档模板"后如何将其转换为可执行的代码实体？这块也费了我不少脑细胞。思前想后，最终设计是将Feature转换成一个可运行的实体-函数。另外我在函数中使用{}来物理划分Scenario，{}可以隔离变量的可见性和作用域，已达到多个Scenarios定义和执行互不干扰的目的。

上面的标准文档结果中的一个FEATURE宏展开后的样子大致是这样的：

static void cbehave_feature_n(void *_state) {

cbehave_state _old_state;

cbehave_feature_entry(…, &_old_state, _state);

{

/* Scenario #1 */

int _scenario_state = 0; \

cbehave_scenario_entry(x, _state);

… …

cbehave_scenario_exit(&_scenario_state, _state);

}

{

/* Scenario #2 */

}

… …

{

/* Scenario #n */

}

_feature_over: \

cbehave_feature_exit(…);

}

关于feature函数的命名，我考虑了很长时间，由于从外界输入的信息无法约束，这里我引入了Feature序号，并同时将序号作为Feature函数名的一部分。例如：

FEATURE(10, "fopen features")

展开后的feature函数名就是cbehave_feature_10，这样做对用户也有一定约束，但约束较小，只需CBehave用户保证各个Feature的序号不同即可。

在使用CBehave时，很可能出现另外一个问题:那就是测试代码在GIVEN或WHEN区段中依赖的一些资源申请或其他代码的初始化可能失败或出现异常。遇到这种情况时，用户多选择return或exit。但一旦用户这样做，CBehave就无法统计和输出测试失败情况或统计的不够准确了。为了尽量保证CBehave统计的精确性，CBehave提供了一个宏FEATURE_RETURN供用户使用。FEATURE_RETURN将控制权转移到Feature函数的末尾，也就是上面宏展开末尾的哪个_feature_over跳转标识符处，这样Feature有机会把这一错误情况记录下来。另外还可以保证其他Feature测试的继续运行。这里举个简单例子(完整代码参见cbehave/src/example/text_editor_test.c)：

FEATURE(1, "Text Editor – Open Exsited File")

SCENARIO("Open an Exsited File and write something to it")

GIVEN("A file named foo.txt")

FILE *fp = NULL;

char *buf = "Hello Cbehave!";

GIVEN_END

WHEN("we open the file and write something to it")

fp = fopen("foo.txt", "r+");

if (!fp)

FEATURE_RETURN(errno);

WHEN_END

THEN("We should see [Hello Cbehave] has been written into foo.txt")

if (fp)

fclose(fp);

THEN_END

SCENARIO_END

FEATURE_END

例子中如果fopen打开foo.txt失败，代码中调用了FEATURE_RETURN来应对这一情况，而不是直接调用return或exit。

最后，与LCUT不同，Cbehave会尝试运行完所有Feature的测试，而不是遇到测试错误就停止运行。

因为之前有过LCUT[单元测试框架的设计和实现](http://http://tonybai.com/2005/11/08/the-design-and-implementation-of-c-unittest-framework/)经验，这次CBehave框架的设计和实现就相对容易了些。CBehave的设计用了一天时间，上周末两天"百忙"中抽空完成了编码和测试，目前已提供了[cbehave-0.1.0-beta](http://cbehave.googlecode.com/files/cbehave-0.1.0-beta.zip)版供下载体验，欢迎大家提出你的宝贵意见和建议^_^，更多关于CBehave使用方面的细节请参考CBehave用户指南([http://code.google.com/p/cbehave/wiki/CBehave_User_Guide_cn](http://code.google.com/p/cbehave/wiki/CBehave_User_Guide_cn))。

BTW，我并不是一个纯粹的TDDers。我个人认为完全采用TDD或是BDD还是有一定局限的。是否采用这些方式进行开发还要视产品(或项目)的时间、质量、人员能力等诸多制约因素而定。个人推断国内的C程序员多普遍缺乏采用框架进行单元测试的意识，BDD或TDD的推广还是任重道远的。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

不错啊！如果可以参考一下Cucumber的实现，把feature和step的实现分开，会更漂亮的。