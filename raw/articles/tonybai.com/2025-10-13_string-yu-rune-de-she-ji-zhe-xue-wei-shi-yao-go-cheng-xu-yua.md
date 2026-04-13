---
title: string 与 rune 的设计哲学：为什么Go 程序员很少为“乱码”烦恼？
url: https://tonybai.com/2025/10/13/string-and-rune-in-go/
published: '2025-10-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# string 与 rune 的设计哲学：为什么Go 程序员很少为“乱码”烦恼？

![](../../assets/f367bee59e37c580.png)


[本文永久链接](https://tonybai.com/2025/10/13/string-and-rune-in-go) – https://tonybai.com/2025/10/13/string-and-rune-in-go

大家好，我是Tony Bai。

“为什么我的字符又乱码了？！”


这是一个在软件开发历史上，曾让无数程序员彻夜难眠的哀嚎。处理文本，是编程中最基础的任务之一，但其背后关于编码 (Encoding) 和字符集 (Character Set) 的水，远比看起来要深。正如 Joel Spolsky 在其[经典文章](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)中疾呼的那样，这是每位软件开发者都必须了解的“绝对最低限度”的知识。

幸运的是，作为 Go 开发者，我们站在了巨人的肩膀上。Go 语言在设计之初，就以一种“独断”而富有远见的方式，为我们解决了大部分历史遗留的编码难题。然而，理解其背后的设计哲学，特别是 string 与 rune 这对“双子星”的共舞，依然是区分一名普通 Gopher 与一名优秀 Gopher 的关键。

本文将带你重温编码的基础，并深入探讨 Go 是如何从语言设计的根源上，让我们得以优雅地驰骋于多语言文本的世界。

![](../../assets/e7aa987414f58103.png)


## 回到本源——计算机不认识“字符”，只认识“比特”

让我们先直面一个最基本、但又常常被遗忘的事实：计算机的世界里没有字母、数字或符号，只有**比特 (bit)**——0 和 1 的序列。计算机所能存储和处理的一切，无论是文本、图片还是声音，最终都必须被翻译成这种二进制形式。为了让这些比特串代表人类可读的文本，我们需要一套**规则**，这套规则就是**编码 (Encoding)**。

我们可以将这个过程拆分为两个核心概念：

-
**字符集 (Character Set)**：一个抽象的符号集合。例如，**ASCII**字符集包含了 128 个字符，包括大小写英文字母、0-9 的数字、以及各种标点和控制符号。你可以把它想象成一本“字典”，里面列出了所有“合法”的字符。 -
**编码 (Encoding)**：一套将字符集中的每个符号，映射为特定比特序列的具体规则。例如，在 ASCII 编码中，这本“字典”规定了字母 A 对应的“页码”是 65，而 A 在计算机中的比特表示就是 65 的二进制形式 01000001。

**乱码问题的根源**，就在于**使用了错误的“字典”和“编码规则”去解读一段比特序列**。想象一下，一段用 Shift-JIS (一种日语编码) 写入的比特流，如果被错误地用 Mac Roman (一种西欧编码) 的“字典”来查找，结果自然是一堆无法理解的“天书”，也就是我们俗称的“乱码”。

## Go 的“独断”——拥抱 Unicode 与 UTF-8

在 Go 诞生之前，软件世界是一片混乱的“编码战国时代”。ASCII 只有 128 个字符，连欧洲语言中常见的 é 或 ü 都无法表示。为了解决这个问题，各种各样的编码方案如雨后春笋般涌现：西欧有 ISO-8859-1，中国大陆有 GB-2312、GBK以及GB18030，中国台湾省有 BIG-5…… 每种编码都定义了自己的字符集和规则，彼此之间互不兼容。

最终，为了“书同文，车同轨”，**Unicode** 应运而生。它旨在创建一个包罗万象的“超级字符集”，为世界上每一种语言的每一个字符都分配一个唯一的数字编号，这个编号被称为**码点 (Code Point)**。

然而，**Unicode 本身并不是一种编码**，它只是一本巨大的“字典”。如何将这些码点（数字）高效地转换为比特序列，则是由 **UTF (Unicode Transformation Format)** 家族的编码方案来完成的，其中最著名的就是 **UTF-8**。

Go 的设计者们，在面对这段混乱的历史时，做出了一个极其重要的、带有“独断”色彩的决定：**将 UTF-8 作为 Go 语言生态的默认和核心编码**。

这个决定，体现在 Go 语言的每一个角落：

**Go 源码文件**被规定必须以**UTF-8**编码保存。- Go 的 string 类型被设计为
**不可变的字节序列**，并且标准库中的绝大多数操作，都**假定并优化**这些字节是合法的 UTF-8 编码。

这与许多早期语言（比如 PHP 等）形成了鲜明对比，在那些语言中，字符串仅仅是“字节袋”，语言本身对其内部编码一无所知，将处理编码的复杂性完全推给了开发者。Go 的这个设计，从源头上为开发者扫清了最大的障碍。

## string 与 rune 的设计哲学——字节与字符的清晰分离

Go 语言为了优雅地处理 Unicode，其核心设计哲学就是**清晰地分离“字节”和“字符”这两个概念**，并通过 string 和 rune 这两个核心类型来体现。理解它们的区别，是掌握 Go 文本处理的关键。

**string**：一个 string 的表示是一个**只读的字节切片 ([]byte)**。它存储的是文本的**UTF-8 编码**后的字节序列。它是数据的**物理表示**。**rune**：rune 是 Go 中用来代表一个**Unicode 码点 (Code Point)**的类型，它是 int32 的一个别名。你可以把它理解为 Go 世界中真正的“字符”。它是文本的**逻辑表示**。

这种底层设计，直接导致了 len() 和 for range 在处理字符串时，那令人“困惑”却又合乎逻辑的不同行为。

### 一个示例，揭示所有秘密

让我们用一个包含中英文的字符串来做个实验，看看 Go 的设计哲学在实践中如何体现：

```
// https://go.dev/play/p/TANnV9NTQi0
package main
import (
"fmt"
"unicode/utf8"
)
func main() {
s := "你好, Go"
// --- len()：返回字节的数量 ---
// 它的操作对象是 string 的物理表示 (bytes)。
// 在 UTF-8 中，一个英文字符占 1 个字节，一个中文字符占 3 个字节。
// 所以，字节总数 = 2*3 (你好) + 1 (,) + 1 ( ) + 2*1 (Go) = 10
fmt.Printf("len(s) -> The number of bytes: %d\n", len(s))
// --- utf8.RuneCountInString()：返回字符（码点）的数量 ---
// 它的操作对象是 string 的逻辑表示 (runes)。
// "你好, Go" 共有 6 个字符（码点）。
fmt.Printf("Rune count -> The number of characters: %d\n", utf8.RuneCountInString(s))
fmt.Println("\n--- Iterating with standard for loop (by byte) ---")
// --- 传统的 for 循环：按字节遍历 ---
// 这会逐一打印出字符串的 10 个字节。对于多字节字符，会产生乱码。
// 这种遍历方式在处理纯 ASCII 时是正确的，但在处理 Unicode 时是错误的。
for i := 0; i < len(s); i++ {
fmt.Printf("%x ", s[i])
}
fmt.Println()
fmt.Println("\n--- Iterating with for range (by rune) ---")
// --- for range 循环：Go 的魔法所在，按 rune 遍历 ---
// for range 会自动解码 UTF-8 序列，每次迭代返回一个 rune 及其起始字节的索引。
// 这是在 Go 中遍历字符串内容的“正确”且地道的方式。
for index, r := range s {
fmt.Printf("index: %d, char: %c, bytes: %d\n", index, r, utf8.RuneLen(r))
}
}
```


**运行该示例输出如下结果：**

```
len(s) -> The number of bytes: 10
Rune count -> The number of characters: 6
--- Iterating with standard for loop (by byte) ---
e4 bd a0 e5 a5 bd 2c 20 47 6f
--- Iterating with for range (by rune) ---
index: 0, char: 你, bytes: 3
index: 3, char: 好, bytes: 3
index: 6, char: ,, bytes: 1
index: 7, char: , bytes: 1
index: 8, char: G, bytes: 1
index: 9, char: o, bytes: 1
```


这个例子清晰地告诉我们 Go 的设计哲学：

**len(s)**给你的是**字节长度**，适用于网络传输、内存分配、缓冲区大小计算等底层、面向物理的场景。**for i := range s**给你的是**字符 (rune)**，适用于所有需要处理文本内容的、面向逻辑的业务场景。

这种对“字节”和“字符”的明确区分，是 Go 程序在处理多语言文本时如此健壮的根本原因。

## Go 开发者的日常：实践中的编码意识

尽管 Go 为我们做了很多，但在与外部世界交互时，编码意识依然不可或缺。

**文件 I/O**：当你从一个文件中 io.Read 时，你读到的是**原始的字节流**。如果这个文件不是 UTF-8 编码的（例如，一个 GBK 编码的 .txt 文件），你必须使用像 golang.org/x/text/encoding 这样的包，将其**显式地转换**为 UTF-8 字符串后，才能在 Go 程序中安全地处理。

```
import (
"golang.org/x/text/encoding/simplifiedchinese"
"golang.org/x/text/transform"
)
// gb_reader 是一个读取 GBK 编码文件的 io.Reader
// utf8_reader 将会是一个在读取时自动转换为 UTF-8 的 io.Reader
utf8_reader := transform.NewReader(gbk_reader, simplifiedchinese.GBK.NewDecoder())
// 从 utf8_reader 中读取的数据现在可以安全地在 Go 中使用了
utf8Bytes, _ := io.ReadAll(utf8_reader)
s := string(utf8Bytes)
```


-
**Web 开发**：在处理 HTTP 请求和响应时，Content-Type 头中的 charset=utf-8 是你与客户端之间的“契约”。Go 的 net/http 库默认会很好地处理 UTF-8，但你需要确保所有与之交互的系统都遵守了这个契约。 -
**数据库交互**：一个经典的“伪正常”陷阱是，应用程序以 UTF-8 方式与数据库通信，但数据库连接或表本身却被错误地设置为 latin1 等编码。由于 latin1 是单字节编码，它可以“吞下”任何字节序列。数据存入时看似正常，应用程序读出时也能正确解析回 UTF-8 字符串。但只要你通过数据库管理工具查看，或者在数据库层面进行排序、搜索，就会立刻看到乱码。**确保你的数据库连接 DSN 中明确指定了 charset=utf8mb4**，是至关重要的最佳实践。

## 小结：站在巨人的肩膀上

Go 语言的设计，让我们不必再像前人那样，在各种编码的泥潭中苦苦挣扎。它通过将 UTF-8 提升为事实标准，并提供 string (字节序列) 和 rune (字符) 这一对强大而清晰的抽象，为我们构建了一个默认安全的文本处理世界。

此外，理解Go中 len() 与 for range在操作 string 类型数据时的区别，不仅仅是掌握一个语言的“奇技淫巧”，更是洞察 Go 语言如何从根本上解决了困扰软件行业数十年的编码难题。这份与生俱来的编码优势，正是 Go 语言简约而不简单的一个最佳例证。

如果想了解更多关于Go string和rune的“秘密”，可以进一步阅读我的《[Go语言进阶课](http://gk.link/a/12yGY)》的05讲。在《[Go语言第一课](http://gk.link/a/10AVZ)》专栏的第13讲中，也有关于码点以及UTF-8编码的更为详细的讲解。

## 参考资料

- What Every Programmer Absolutely, Positively Needs To Know About Encodings And Character Sets To Work With Text – https://kunststube.net/encoding/
- The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!) – https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/

你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


**想系统学习Go，构建扎实的知识体系？**

我的新书《[Go语言第一课](https://book.douban.com/subject/37499496/)》是你的首选。源自2.4万人好评的极客时间专栏，内容全面升级，同步至Go 1.24。首发期有专属五折优惠，不到40元即可入手，扫码即可拥有这本300页的Go语言入门宝典，即刻开启你的Go语言高效学习之旅！

![](../../assets/d3fd3ab3e1fd7a7e.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论