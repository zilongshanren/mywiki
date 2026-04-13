---
title: Gopher Daily改版了
url: https://tonybai.com/2023/08/06/gopherdaily-revamped/
published: '2023-08-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Gopher Daily改版了

![](../../assets/3e288c66d2be8461.png)


[本文永久链接](https://tonybai.com/2023/08/06/gopherdaily-revamped) – https://tonybai.com/2023/08/06/gopherdaily-revamped

已经记不得GopherDaily是何时创建的了，翻了一下[GopherDaily项目](https://github.com/bigwhite/gopherdaily)的commit history，才发现我的这个个人项目是2019年9月创建的，[最初内容组织很粗糙](https://github.com/bigwhite/gopherdaily/blob/master/201909/issue-20190925.txt)，但我的编辑制作的热情很高，基本能坚持**每日一发**，甚至节假日也**不停刊**：

![](../../assets/81c4ab1989c8b887.png)


该项目的初衷就是**为广大Gopher带来新鲜度较高的Go语言技术资料**。项目创建以来得到了很多Gopher的支持，甚至经常收到催刊邮件/私信以及主动report订阅列表问题的情况。

不过近一年多，订阅GopherDaily的Gopher可能会发现：GopherDaily已经做不到“Daily”了！究其原因还是个人精力有限，每刊编辑都要花费很多时间。但个人又不想暂停该项目，怎么办呢？近段时间我就在着手思考**提升GopherDaily制作效率的问题**。

一个可行的方案就是“半自动化”！在这次从“纯人工”到“半自动化”的过程中，顺便对GopherDaily做了一次“改版”。

在这篇文章中，我就来说说结合[大语言模型](https://en.wikipedia.org/wiki/Large_language_model)和Go技术栈实现GopherDaily制作的“半自动化”以及GopherDaily“改版”的历程。

## 1. “半自动化”的制作流程

当前的GopherDaily每刊的制作过程十分费时费力，下面是图示的制作过程：

![](../../assets/9fcf95d73e75bd81.png)


这里面所有步骤都是人工处理，且收集资料、阅读摘要以及选优最为耗时。

那么这些环节中哪些可以自动化呢？收集、摘要、翻译、生成与发布都可以自动化，只有“选优”需要人工干预，下面是改进后的“半自动化”流程：

![](../../assets/8b6ab5911e38997f.png)


我们看到整个过程分为三个阶段：

- 第一阶段(stage1)：自动化的收集资料，并生成第二阶段的输入issue-20230805-stage1.json(以2023年8月5日为例)。
- 第二阶段(stage2)：对输入的issue-20230805-stage1.json中的资料进行选优，删掉不适合或质量不高的资料，当然也可以手工加入一些自动化收集阶段未找到的优秀资料；然后基于选优后的内容生成issue-20230805-stage2.json，作为第三阶段的输入。
- 第三阶段(stage3)：这一阶段也都是自动化的，程序基于第二阶段的输出issue-20230805-stage2.json中内容，逐条生成摘要，并将文章标题和摘要翻译为中文，最后生成两个文件：issue-20230805.html和issue-20230805.md，前者将被发布到
[邮件列表](https://gopherdaily.tonybai.com/subscribe)和[gopherdaily github page](https://gopherdaily.tonybai.com)上，而后者则会被上传到[传统的GopherDaily归档项目](https://github.com/bigwhite/gopherdaily)中。

我个人的目标是将改进后的整个“半自动化”过程缩短在半小时以内，从试运行效果来看，基本达成！

下面我就来简要聊聊各个自动化步骤是如何实现的。

## 2. Go技术资料自动收集

GopherDaily制作效率提升的一个大前提就是可以将最耗时的“资料收集”环节自动化了！而要做到这一点，下面两方面不可或缺：

- 资料源集合
- 针对资料源的最新文章的感知和拉取

### 2.1 资料源的来源

资料源从哪里来呢？答案是以往的GopherDaily issues中！四年来积累了数千篇文章的URL，从这些issue中提取URL并按URL中域名/域名+一级路径的出现次数做个排序，得到GopherDaily改版后的初始资料源集合。虽然这个方案并不完美，但至少可以满足改版后的初始需求，后续还可以对资料源做渐进的手工优化。

提取文本中URL的方法有很多种，常用的一种方法是使用正则表达式，下面是一个从markdown或txt文件中提取url并输出的例子：

```
// extract-url/main.go
package main
import (
"bufio"
"fmt"
"os"
"path/filepath"
"regexp"
)
func main() {
var allURLs []string
err := filepath.Walk("/Users/tonybai/blog/gitee.com/gopherdaily", func(path string, info os.FileInfo, err error) error {
if err != nil {
return err
}
if info.IsDir() {
return nil
}
if filepath.Ext(path) != ".txt" && filepath.Ext(path) != ".md" {
return nil
}
file, err := os.Open(path)
if err != nil {
return err
}
defer file.Close()
scanner := bufio.NewScanner(file)
urlRegex := regexp.MustCompile(`https?://[^\s]+`)
for scanner.Scan() {
urls := urlRegex.FindAllString(scanner.Text(), -1)
allURLs = append(allURLs, urls...)
}
return scanner.Err()
})
if err != nil {
fmt.Println(err)
return
}
for _, url := range allURLs {
fmt.Printf("%s\n", url)
}
fmt.Println(len(allURLs))
}
```


我将提取并分析后得到的URL放入一个临时文件中，因为仅提取URL还不够，要做为资料源，我们需要的是对应站点的feed地址。那么如何提取出站点的feed地址呢？我们看下面这个例子：

```
// extract_rss/main.go
package main
import (
"fmt"
"io/ioutil"
"net/http"
"regexp"
)
var (
rss = regexp.MustCompile(`<link[^>]*type="application/rss\+xml"[^>]*href="([^"]+)"`)
atom = regexp.MustCompile(`<link[^>]*type="application/atom\+xml"[^>]*href="([^"]+)"`)
)
func main() {
var sites = []string{
"http://research.swtch.com",
"https://tonybai.com",
"https://benhoyt.com/writings",
}
for _, url := range sites {
resp, err := http.Get(url)
if err != nil {
fmt.Println("Error fetching URL:", err)
continue
}
defer resp.Body.Close()
body, err := ioutil.ReadAll(resp.Body)
if err != nil {
fmt.Println("Error reading response body:", err)
continue
}
matches := rss.FindAllStringSubmatch(string(body), -1)
if len(matches) == 0 {
matches = atom.FindAllStringSubmatch(string(body), -1)
if len(matches) == 0 {
continue
}
}
fmt.Printf("\"%s\" -> rss: \"%s\"\n", url, matches[0][1])
}
}
```


执行上述程序，我们得到如下结果：

```
"http://research.swtch.com" -> rss: "http://research.swtch.com/feed.atom"
"https://tonybai.com" -> rss: "https://tonybai.com/feed/"
"https://benhoyt.com/writings" -> rss: "/writings/rss.xml"
```


我们看到不同站点的rss地址值着实不同，有些是完整的url地址，有些则是相对于主站点url的路径，这个还需要进一步判断与处理，但这里就不赘述了。

我们将提取和处理后的feed地址放入feeds.toml中作为资料源集合。每天开始制作Gopher Daily时，就从读取这个文件中的资料源开始。

### 2.2 感知和拉取资料源的更新

有了资料源集合后，我们接下来要做的就是定期感知和拉取资料源的最新更新（暂定24小时以内的），再说白点就是拉取资料源的feed数据，解析内容，得到资料源的最新文章信息。针对feed拉取与解析，Go社区有现成的工具，比如[gofeed](https://github.com/mmcdole/gofeed)就是其中功能较为齐全且表现稳定的一个。

下面是使用Gofeed抓取feed地址并获取文章信息的例子：

```
// gofeed/main.go
package main
import (
"fmt"
"github.com/mmcdole/gofeed"
)
func main() {
var feeds = []string{
"https://research.swtch.com/feed.atom",
"https://tonybai.com/feed/",
"https://benhoyt.com/writings/rss.xml",
}
fp := gofeed.NewParser()
for _, feed := range feeds {
feedInfo, err := fp.ParseURL(feed)
if err != nil {
fmt.Printf("parse feed [%s] error: %s\n", feed, err.Error())
continue
}
fmt.Printf("The info of feed url: %s\n", feed)
for _, item := range feedInfo.Items {
fmt.Printf("\t title: %s\n", item.Title)
fmt.Printf("\t link: %s\n", item.Link)
fmt.Printf("\t published: %s\n", item.Published)
}
fmt.Println("")
}
}
```


该程序分别解析三个feed地址，并分别输出得到的文章信息，包括标题、url和发布时间。运行上述程序我们将得到如下结果：

```
$go run main.go
The info of feed url: https://research.swtch.com/feed.atom
title: Coroutines for Go
link: http://research.swtch.com/coro
published: 2023-07-17T14:00:00-04:00
title: Storing Data in Control Flow
link: http://research.swtch.com/pcdata
published: 2023-07-11T14:00:00-04:00
title: Opting In to Transparent Telemetry
link: http://research.swtch.com/telemetry-opt-in
published: 2023-02-24T08:59:00-05:00
title: Use Cases for Transparent Telemetry
link: http://research.swtch.com/telemetry-uses
published: 2023-02-08T08:00:03-05:00
title: The Design of Transparent Telemetry
link: http://research.swtch.com/telemetry-design
published: 2023-02-08T08:00:02-05:00
title: Transparent Telemetry for Open-Source Projects
link: http://research.swtch.com/telemetry-intro
published: 2023-02-08T08:00:01-05:00
title: Transparent Telemetry
link: http://research.swtch.com/telemetry
published: 2023-02-08T08:00:00-05:00
title: The Magic of Sampling, and its Limitations
link: http://research.swtch.com/sample
published: 2023-02-04T12:00:00-05:00
title: Go’s Version Control History
link: http://research.swtch.com/govcs
published: 2022-02-14T10:00:00-05:00
title: What NPM Should Do Today To Stop A New Colors Attack Tomorrow
link: http://research.swtch.com/npm-colors
published: 2022-01-10T11:45:00-05:00
title: Our Software Dependency Problem
link: http://research.swtch.com/deps
published: 2019-01-23T11:00:00-05:00
title: What is Software Engineering?
link: http://research.swtch.com/vgo-eng
published: 2018-05-30T10:00:00-04:00
title: Go and Dogma
link: http://research.swtch.com/dogma
published: 2017-01-09T09:00:00-05:00
title: A Tour of Acme
link: http://research.swtch.com/acme
published: 2012-09-17T11:00:00-04:00
title: Minimal Boolean Formulas
link: http://research.swtch.com/boolean
published: 2011-05-18T00:00:00-04:00
title: Zip Files All The Way Down
link: http://research.swtch.com/zip
published: 2010-03-18T00:00:00-04:00
title: UTF-8: Bits, Bytes, and Benefits
link: http://research.swtch.com/utf8
published: 2010-03-05T00:00:00-05:00
title: Computing History at Bell Labs
link: http://research.swtch.com/bell-labs
published: 2008-04-09T00:00:00-04:00
title: Using Uninitialized Memory for Fun and Profit
link: http://research.swtch.com/sparse
published: 2008-03-14T00:00:00-04:00
title: Play Tic-Tac-Toe with Knuth
link: http://research.swtch.com/tictactoe
published: 2008-01-25T00:00:00-05:00
title: Crabs, the bitmap terror!
link: http://research.swtch.com/crabs
published: 2008-01-09T00:00:00-05:00
The info of feed url: https://tonybai.com/feed/
title: Go语言开发者的Apache Arrow使用指南：读写Parquet文件
link: https://tonybai.com/2023/07/31/a-guide-of-using-apache-arrow-for-gopher-part6/
published: Mon, 31 Jul 2023 13:07:28 +0000
title: Go语言开发者的Apache Arrow使用指南：扩展compute包
link: https://tonybai.com/2023/07/22/a-guide-of-using-apache-arrow-for-gopher-part5/
published: Sat, 22 Jul 2023 13:58:57 +0000
title: 使用testify包辅助Go测试指南
link: https://tonybai.com/2023/07/16/the-guide-of-go-testing-with-testify-package/
published: Sun, 16 Jul 2023 07:09:56 +0000
title: Go语言开发者的Apache Arrow使用指南：数据操作
link: https://tonybai.com/2023/07/13/a-guide-of-using-apache-arrow-for-gopher-part4/
published: Thu, 13 Jul 2023 14:41:25 +0000
title: Go语言开发者的Apache Arrow使用指南：高级数据结构
link: https://tonybai.com/2023/07/08/a-guide-of-using-apache-arrow-for-gopher-part3/
published: Sat, 08 Jul 2023 15:27:54 +0000
title: Apache Arrow：驱动列式分析性能和连接性的提升[译]
link: https://tonybai.com/2023/07/01/arrow-columnar-analytics/
published: Sat, 01 Jul 2023 14:42:29 +0000
title: Go语言开发者的Apache Arrow使用指南：内存管理
link: https://tonybai.com/2023/06/30/a-guide-of-using-apache-arrow-for-gopher-part2/
published: Fri, 30 Jun 2023 14:00:59 +0000
title: Go语言开发者的Apache Arrow使用指南：数据类型
link: https://tonybai.com/2023/06/25/a-guide-of-using-apache-arrow-for-gopher-part1/
published: Sat, 24 Jun 2023 20:43:38 +0000
title: Go语言包设计指南
link: https://tonybai.com/2023/06/18/go-package-design-guide/
published: Sun, 18 Jun 2023 15:03:41 +0000
title: Go GC：了解便利背后的开销
link: https://tonybai.com/2023/06/13/understand-go-gc-overhead-behind-the-convenience/
published: Tue, 13 Jun 2023 14:00:16 +0000
The info of feed url: https://benhoyt.com/writings/rss.xml
title: The proposal to enhance Go's HTTP router
link: https://benhoyt.com/writings/go-servemux-enhancements/
published: Mon, 31 Jul 2023 08:00:00 +1200
title: Scripting with Go: a 400-line Git client that can create a repo and push itself to GitHub
link: https://benhoyt.com/writings/gogit/
published: Sat, 29 Jul 2023 16:30:00 +1200
title: Names should be as short as possible while still being clear
link: https://benhoyt.com/writings/short-names/
published: Mon, 03 Jul 2023 21:00:00 +1200
title: Lookup Tables (Forth Dimensions XIX.3)
link: https://benhoyt.com/writings/forth-lookup-tables/
published: Sat, 01 Jul 2023 22:10:00 +1200
title: For Python packages, file structure != API
link: https://benhoyt.com/writings/python-api-file-structure/
published: Fri, 30 Jun 2023 22:50:00 +1200
title: Designing Pythonic library APIs
link: https://benhoyt.com/writings/python-api-design/
published: Sun, 18 Jun 2023 21:00:00 +1200
title: From Go on EC2 to Fly.io: +fun, −$9/mo
link: https://benhoyt.com/writings/flyio/
published: Mon, 27 Feb 2023 10:00:00 +1300
title: Code coverage for your AWK programs
link: https://benhoyt.com/writings/goawk-coverage/
published: Sat, 10 Dec 2022 13:41:00 +1300
title: I/O is no longer the bottleneck
link: https://benhoyt.com/writings/io-is-no-longer-the-bottleneck/
published: Sat, 26 Nov 2022 22:20:00 +1300
title: microPledge: our startup that (we wish) competed with Kickstarter
link: https://benhoyt.com/writings/micropledge/
published: Mon, 14 Nov 2022 20:00:00 +1200
title: Rob Pike's simple C regex matcher in Go
link: https://benhoyt.com/writings/rob-pike-regex/
published: Fri, 12 Aug 2022 14:00:00 +1200
title: Tools I use to build my website
link: https://benhoyt.com/writings/tools-i-use-to-build-my-website/
published: Tue, 02 Aug 2022 19:00:00 +1200
title: Modernizing AWK, a 45-year old language, by adding CSV support
link: https://benhoyt.com/writings/goawk-csv/
published: Tue, 10 May 2022 09:30:00 +1200
title: Prig: like AWK, but uses Go for "scripting"
link: https://benhoyt.com/writings/prig/
published: Sun, 27 Feb 2022 18:20:00 +0100
title: Go performance from version 1.2 to 1.18
link: https://benhoyt.com/writings/go-version-performance/
published: Fri, 4 Feb 2022 09:30:00 +1300
title: Optimizing GoAWK with a bytecode compiler and virtual machine
link: https://benhoyt.com/writings/goawk-compiler-vm/
published: Thu, 3 Feb 2022 22:25:00 +1300
title: AWKGo, an AWK-to-Go compiler
link: https://benhoyt.com/writings/awkgo/
published: Mon, 22 Nov 2021 00:10:00 +1300
title: Improving the code from the official Go RESTful API tutorial
link: https://benhoyt.com/writings/web-service-stdlib/
published: Wed, 17 Nov 2021 07:00:00 +1300
title: Simple Lists: a tiny to-do list app written the old-school way (server-side Go, no JS)
link: https://benhoyt.com/writings/simple-lists/
published: Mon, 4 Oct 2021 07:30:00 +1300
title: Structural pattern matching in Python 3.10
link: https://benhoyt.com/writings/python-pattern-matching/
published: Mon, 20 Sep 2021 19:30:00 +1200
title: Mugo, a toy compiler for a subset of Go that can compile itself
link: https://benhoyt.com/writings/mugo/
published: Mon, 12 Apr 2021 20:30:00 +1300
title: How to implement a hash table (in C)
link: https://benhoyt.com/writings/hash-table-in-c/
published: Fri, 26 Mar 2021 20:30:00 +1300
title: Performance comparison: counting words in Python, Go, C++, C, AWK, Forth, and Rust
link: https://benhoyt.com/writings/count-words/
published: Mon, 15 Mar 2021 20:30:00 +1300
title: The small web is beautiful
link: https://benhoyt.com/writings/the-small-web-is-beautiful/
published: Tue, 2 Mar 2021 06:50:00 +1300
title: Coming in Go 1.16: ReadDir and DirEntry
link: https://benhoyt.com/writings/go-readdir/
published: Fri, 29 Jan 2021 10:00:00 +1300
title: Fuzzing in Go
link: https://lwn.net/Articles/829242/
published: Tue, 25 Aug 2020 08:00:00 +1200
title: Searching code with Sourcegraph
link: https://lwn.net/Articles/828748/
published: Mon, 17 Aug 2020 08:00:00 +1200
title: Different approaches to HTTP routing in Go
link: https://benhoyt.com/writings/go-routing/
published: Fri, 31 Jul 2020 08:00:00 +1200
title: Go filesystems and file embedding
link: https://lwn.net/Articles/827215/
published: Fri, 31 Jul 2020 00:00:00 +1200
title: The sad, slow-motion death of Do Not Track
link: https://lwn.net/Articles/826575/
published: Wed, 22 Jul 2020 11:00:00 +1200
title: What's new in Lua 5.4
link: https://lwn.net/Articles/826134/
published: Wed, 15 Jul 2020 11:00:00 +1200
title: Hugo: a static-site generator
link: https://lwn.net/Articles/825507/
published: Wed, 8 Jul 2020 11:00:00 +1200
title: Generics for Go
link: https://lwn.net/Articles/824716/
published: Wed, 1 Jul 2020 11:00:00 +1200
title: More alternatives to Google Analytics
link: https://lwn.net/Articles/824294/
published: Wed, 24 Jun 2020 11:00:00 +1200
title: Lightweight Google Analytics alternatives
link: https://lwn.net/Articles/822568/
published: Wed, 17 Jun 2020 11:00:00 +1200
title: An intro to Go for non-Go developers
link: https://benhoyt.com/writings/go-intro/
published: Wed, 10 Jun 2020 23:38:00 +1200
title: ZZT in Go (using a Pascal-to-Go converter)
link: https://benhoyt.com/writings/zzt-in-go/
published: Fri, 29 May 2020 17:25:00 +1200
title: Testing in Go: philosophy and tools
link: https://lwn.net/Articles/821358/
published: Wed, 27 May 2020 12:00:00 +1200
title: The state of the AWK
link: https://lwn.net/Articles/820829/
published: Wed, 20 May 2020 12:00:00 +1200
title: What's coming in Go 1.15
link: https://lwn.net/Articles/820217/
published: Wed, 13 May 2020 12:00:00 +1200
title: Don't try to sanitize input. Escape output.
link: https://benhoyt.com/writings/dont-sanitize-do-escape/
published: Thu, 27 Feb 2020 19:27:00 +1200
title: SEO for Software Engineers
link: https://benhoyt.com/writings/seo-for-software-engineers/
published: Thu, 20 Feb 2020 12:00:00 +1200
```


注：gofeed抓取的item.Description是文章的摘要。但这个摘要不一定可以真实反映文章内容的概要，很多就是文章内容的前N个字而已。


Gopher Daily半自动化改造的另外一个技术课题是对拉取的文章做自动摘要与标题摘要的翻译，下面我们继续来看一下这个课题如何攻破。

注：目前微信公众号的优质文章尚未实现自动拉取，还需手工选优。


## 3. 自动摘要与翻译

对一段文本提取摘要和翻译均属于自然语言处理(NLP)范畴，说实话，Go在这个范畴中并不活跃，很难找到像样的开源算法实现或工具可直接使用。我的解决方案是**借助云平台供应商的NLP API来做**，这里我用的是微软Azure的相关API。

在使用现成的API之前，我们需要抓取特定url上的html页面并提取出要进行摘要的文本。

### 3.1 提取html中的原始文本

我们通过http.Get可以获取到一个文章URL上的html页面的所有内容，但如何提取出主要文本以供后续提取摘要使用呢？每个站点上的html内容都包含了很多额外内容，比如header、footer、分栏、边栏、导航栏等，这些内容对摘要的生成具有一定影响。我们最好能将这些额外内容剔除掉。但html的解析还是十分复杂的，我的解决方案是将html转换为markdown后再提交给摘要API。

[html-to-markdown](https://github.com/JohannesKaufmann/html-to-markdown)是一款不错的转换工具，它最吸引我的是可以删除原HTML中的一些tag，并自定义一些rule。下面的例子就是用html-to-markdown获取文章原始本文的例子：

```
// get-original-text/main.go
package main
import (
"fmt"
"io/ioutil"
"net/http"
md "github.com/JohannesKaufmann/html-to-markdown"
)
func main() {
s, err := getOriginText("http://research.swtch.com/coro")
if err != nil {
panic(err)
}
fmt.Println(s)
}
func getOriginText(url string) (string, error) {
resp, err := http.Get(url)
if err != nil {
return "", err
}
defer resp.Body.Close()
body, _ := ioutil.ReadAll(resp.Body)
converter := md.NewConverter("", true, nil).Remove("header",
"footer", "aside", "table", "nav") //"table" is used to store code
markdown, err := converter.ConvertString(string(body))
if err != nil {
return "", err
}
return markdown, nil
}
```


在这个例子中，我们删除了header、footer、边栏、导航栏等，尽可能的保留主要文本。针对这个例子我就不执行了，大家可以自行执行并查看执行结果。

### 3.2 提取摘要

我们通过[微软Azure提供的摘要提取API](https://learn.microsoft.com/zh-cn/azure/ai-services/language-service/summarization/how-to/document-summarization)进行摘要提取。微软Azure的这个API提供的免费额度，足够我这边制作Gopher Daily使用了。

注：要使用微软Azure提供的各类免费API，需要先注册Azure的账户。目前摘要提取API仅在North Europe, East US, UK South三个region提供，创建API服务时别选错Region了。我这里用的是East US。

注：Azure控制台较为难用，大家要有心理准备:)。


微软这个摘要API十分复杂，下面给出一个用curl调用API的示例。

摘要提取API的使用分为两步。第一步是请求对原始文本进行摘要处理，比如：

```
$curl -i -X POST https://gopherdaily-summarization.cognitiveservices.azure.com/language/analyze-text/jobs?api-version=2022-10-01-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: your_api_key" \
-d \
'
{
"displayName": "Document Abstractive Summarization Task Example",
"analysisInput": {
"documents": [
{
"id": "1",
"language": "en",
"text": "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Azure AI services, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there’s magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code will enable us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pre-trained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
}
]
},
"tasks": [
{
"kind": "AbstractiveSummarization",
"taskName": "Document Abstractive Summarization Task 1",
"parameters": {
"sentenceCount": 1
}
}
]
}
'
```


请求成功后，我们将得到一段应答，应答中包含类似operation-location的一段地址：

```
Operation-Location:[https://gopherdaily-summarization.cognitiveservices.azure.com/language/analyze-text/jobs/66e7e3a1-697c-4fad-864c-d84c647682b4?api-version=2022-10-01-preview]
```


这段地址就是第二步的请求地址，第二步是从这个地址获取摘要后的本文：

```
$curl -X GET https://gopherdaily-summarization.cognitiveservices.azure.com/language/analyze-text/jobs/66e7e3a1-697c-4fad-864c-d84c647682b4\?api-version\=2022-10-01-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: your_api_key"
{"jobId":"66e7e3a1-697c-4fad-864c-d84c647682b4","lastUpdatedDateTime":"2023-07-27T11:09:45Z","createdDateTime":"2023-07-27T11:09:44Z","expirationDateTime":"2023-07-28T11:09:44Z","status":"succeeded","errors":[],"displayName":"Document Abstractive Summarization Task Example","tasks":{"completed":1,"failed":0,"inProgress":0,"total":1,"items":[{"kind":"AbstractiveSummarizationLROResults","taskName":"Document Abstractive Summarization Task 1","lastUpdateDateTime":"2023-07-27T11:09:45.8892126Z","status":"succeeded","results":{"documents":[{"summaries":[{"text":"Microsoft has been working to advance AI beyond existing techniques by taking a more holistic, human-centric approach to learning and understanding, and the Chief Technology Officer of Azure AI services, who enjoys a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text, audio or visual sensory signals, and multilingual, has created XYZ-code, a joint representation to create more powerful AI that can speak, hear, see, and understand humans better.","contexts":[{"offset":0,"length":1619}]}],"id":"1","warnings":[]}],"errors":[],"modelVersion":"latest"}}]}}%
```


大家可以根据请求和应答的JSON结构，结合一些json-to-struct工具自行实现Azure摘要API的Go代码。

### 3.3 翻译

[Azure的翻译API](https://learn.microsoft.com/zh-cn/azure/ai-services/translator/reference/v3-0-reference)相对于摘要API要简单的多。

下面是使用curl演示翻译API的示例：

```
$curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=zh" \
-H "Ocp-Apim-Subscription-Key:your_api_key" \
-H "Ocp-Apim-Subscription-Region:westcentralus" \
-H "Content-Type: application/json" \
-d "[{'Text':'Hello, what is your name?'}]"
[{"detectedLanguage":{"language":"en","score":1.0},"translations":[{"text":"你好，你叫什么名字？","to":"zh-Hans"}]}]%
```


大家可以根据请求和应答的JSON结构，结合一些json-to-struct工具自行实现Azure翻译API的Go代码。

对于源文章是中文的，我们可以无需调用该API进行翻译，下面是一个判断字符串是否为中文的函数：

```
func isChinese(s string) bool {
for _, r := range s {
if unicode.Is(unicode.Scripts["Han"], r) {
return true
}
}
return false
}
```


## 4. 页面样式设计与html生成

这次Gopher Daily改版，我为Gopher Daily提供了[Web版](https://gopherdaily.tonybai.com)和[邮件列表版](https://gopherdaily.tonybai.com/subscribe)，但页面设计是我最不擅长的。好在，和四年前相比，IT技术又有了进一步的发展，以ChatGPT为代表的大语言模型如雨后春笋般层出不穷，我可以借助大模型的帮助来为我设计和实现一个简单的html页面了。下图就是这次改版后的第一版页面：

![](../../assets/9e977a59a42ff673.png)


整个页面分为四大部分：Go、云原生(与Go关系紧密，程序员相关，架构相关的内容也放在这部分)、AI(当今流行)以及热门工具与项目(目前主要是github trending中每天Go项目的top列表中的内容)。

每一部分每个条目都包含文章标题、文章链接和文章的摘要，摘要的增加可以帮助大家更好的预览文章内容。

html和markdown的生成都是基于Go的template技术，template也是借助[claude.ai](https://claude.ai/chats)设计与实现的，这里就不赘述了。

## 5. 服务器选型

以前的Gopher Daily仅是在github上的一个开源项目，大家通过watch来订阅。此外，[Basten Gao](https://github.com/bastengao)维护着一个第三方的[邮件列表](https://gopher-daily.com/)，在此也对Basten Gao对Gopher Daily的长期支持表示感谢。

如今改版后，我原生提供了Gopher Daily的Web版，我需要为Gopher Daily选择服务器。

简单起见，我选用了github page来承载Gopher Daily的Web版。

至于邮件列表的订阅、取消订阅，我则是开发了一个小小的服务，跑在[Digital Ocean的VPS](https://m.do.co/c/bff6eed92687)上。

在选择反向代理web服务器时，我放弃了nginx，选择了同样Go技术栈实现的[Caddy](https://github.com/caddyserver/caddy)。Caddy最大好处就是易上手，且默认自动支持HTTPS，我无需自行用工具向免费证书机构(如 Let’s Encrypt或ZeroSSL)去申请和维护证书。

## 6 小结

这次改版后的Gopher Daily应得上那句话：“麻雀虽小，五脏俱全”：我为此开发了三个工具，一个服务。

当然Gopher Daily还在持续优化，后续也会根据Gopher们的反馈作适当调整。

摘要和翻译目前使用Azure API，后续可能会改造为使用类ChatGPT的API。

此外，[知识星球Gopher部落](https://public.zsxq.com/groups/51284458844544)的星友们依然拥有“先睹为快”的权益。

本文示例代码可以在[这里](https://github.com/bigwhite/experiments/blob/master/gopherdaily-revamped)下载。

[Gopher Daily网页版](https://gopherdaily.tonybai.com)– https://gopherdaily.tonybai.com[Gopher Daily邮件列表订阅](https://gopherdaily.tonybai.com/subscribe)– https://gopherdaily.tonybai.com/subscribe[Gopher Daily项目归档(markdown版本)](https://github.com/bigwhite/gopherdaily)– https://github.com/bigwhite/gopherdaily

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论