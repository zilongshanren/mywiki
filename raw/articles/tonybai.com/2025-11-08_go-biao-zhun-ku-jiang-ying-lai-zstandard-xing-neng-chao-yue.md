---
title: Go 标准库将迎来 Zstandard：性能超越 Gzip，让你的应用更快、更省
url: https://tonybai.com/2025/11/08/proposal-zstd/
published: '2025-11-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 标准库将迎来 Zstandard：性能超越 Gzip，让你的应用更快、更省

![](../../assets/01038a19f70fc39b.png)


[本文永久链接](https://tonybai.com/2025/11/08/proposal-zstd) – https://tonybai.com/2025/11/08/proposal-zstd

大家好，我是Tony Bai。

在 Go 的世界里，一项被社区翘首以盼的提案在沉寂一年后，终于迎来了决定性的进展。2024 年，将 Zstandard 压缩算法纳入标准库的提案（[#62513](https://github.com/golang/go/issues/62513)）被正式 **Accept**，但在那之后便鲜有动静。直到最近的 [Go 编译器与运行时会议纪要](https://github.com/golang/go/issues/43930#issuecomment-3487773597)中透露，这项工作将由社区的明星开发者 Klaus Post 主导推进。

这意味着，在未来的 Go 版本中，开发者将能开箱即用地获得一个官方维护、安全可靠且性能卓越的压缩工具。这不仅是对 Go 生态的一次重要补强，更将直接为无数 Go 应用带来性能提升、带宽节约和成本削减，真正实现“更快、更省”的承诺。

同时，这个提案背后曲折的历程——从激烈的技术选型辩论，到精雕细琢的 API 设计，再到因核心团队资源紧张而搁置，最终由社区力量重新激活——本身就是一幅展现 Go 生态演进的生动图景。

在本文中，我们将探讨 Zstandard 脱颖而出的技术优势，剖析其在工业界的成功案例，并揭示 compress/zstd 标准库从提案、API 设计到最终由社区力量重启的完整历程。

![](../../assets/ce05c9c7438fe698.png)


## Zstandard：为何是它，而非其他？

在决定为标准库引入新的压缩算法时，Go 团队面临着众多选择。提案发起者 dsnet 在讨论中进行了一次精彩的“选美”，清晰地阐述了为何 Zstandard (Zstd) 能够脱颖而出：

**Zstandard (Zstd):**由 Facebook (现 Meta) 开发并开源，拥有极佳的压缩/解压速度和出色的压缩比。更重要的是，它有正式的 RFC 规范（[RFC 8878](https://datatracker.ietf.org/doc/html/rfc8878)），这对于标准库实现的“正确性”至关重要。**Brotli:**同样优秀，但在设计上更偏向 Web 静态内容，且其庞大的静态字典（约 120KiB）与 Go 追求小体积静态二进制文件的哲学相悖。**XZ (LZMA):**拥有极高的压缩比，但代价是极其缓慢的压缩和解压速度，不适合通用场景。且缺乏正式的、明确的规范。**Snappy / LZ4:**追求极致的速度，但在压缩比上做出了巨大牺牲，应用场景相对小众。

Zstd 巧妙地结合了 LZ77 算法和一种名为 ANS (Asymmetric Numeral Systems) 的现代熵编码技术，在性能、压缩比和资源消耗之间取得了近乎完美的平衡，使其成为替代 Gzip 的“天选之子”。

注：截至Go 1.25.3版本，Go compress目录下提供了多种压缩算法的实现：bzip2实现了Burrows-Wheeler变换及霍夫曼编码；flate提供了DEFLATE算法核心，结合了LZ77和霍夫曼编码；gzip和zlib则分别将DEFLATE算法封装为gzip文件格式和zlib数据流格式；lzw实现了Lempel-Ziv-Welch算法。这些包共同为Go语言提供了多样化的数据压缩与解压缩能力。

注：Zstandard最新RFC规范为

[RFC 9659]。

## 工业界验证：Discord 与 Cloudflare 的性能飞跃

理论上的优势必须经过实践的检验。Zstd 在工业界的应用早已硕果累累。

-
[**Discord 的 40% 带宽削减](https://discord.com/blog/how-discord-reduced-websocket-traffic-by-40-percent)：** 通讯巨头 Discord 在将其实时网关的压缩算法从 zlib (Gzip) 迁移到**流式 Zstandard**后，获得了惊人的收益。对于核心的 MESSAGE_CREATE 事件，压缩时间缩短了一半以上，负载体积也显著减小。这直接转化为更低的服务端 CPU 占用和客户端带宽节省，最终实现了**整体 Websocket 流量降低 40%**的壮举。 -
[**Cloudflare 的容器镜像加速](https://blog.cloudflare.com/container-platform-preview)：** 在其全球容器平台上，Cloudflare 需要快速分发巨大的 AI 模型镜像（常超过 15GB）。通过将镜像层压缩算法从 Gzip 更换为 Zstd，**一个 30GB 镜像的拉取时间从 8 分钟骤降至 4 分钟**，速度翻倍，极大地提升了全球调度的灵活性和响应速度。

这些案例雄辩地证明，Zstd 是为现代高吞吐量、低延迟应用而生的。

## API 设计的艺术：一场关于简洁、安全与未来的辩论

将新包引入标准库，API 的设计是重中之重。#62513 的讨论串完整记录了 compress/zstd API 从雏形到最终形态的演进过程。

### 核心原则：安全与一致性

提案伊始，就确立了两大基石：

**安全优先：**标准库实现必须是**纯 Go**版本，不使用 unsafe 或汇编。dsnet 强调：“Go 社区调查一致显示，安全性比性能更重要。” 这意味着标准库版本追求的是可审查性、可维护性和跨平台的一致性，而非极致的性能。**API 一致性：**新 API 应与 compress/gzip、compress/flate 等现有包保持风格统一，降低开发者的学习和迁移成本。

### 社区的声音：Klaus Post 的关键输入

在讨论中，github.com/klauspost/compress 系列库的作者 **Klaus Post** 扮演了关键角色。他的库是 Go 社区公认的最高性能压缩实现，其丰富的实战经验为标准库的设计提供了宝贵视角。

Klaus 指出，他自己的库 API 相对复杂，是因为支持多线程、异步等高级特性。他赞同标准库应剥离这些复杂性，提供一个完全同步的、线程安全的 API。同时，他也对字典（Dictionary）功能的 API 设计提出了深刻见解，强调了字典预处理的开销问题，这直接影响了后续 API 的设计。

### 最终定稿的 API

经过多轮讨论，由 Russ Cox (rsc) 总结并最终被接受的 API 形态如下(并非最终版)：

```
package zstd
const (
NoCompression = 0
BestSpeed = 1
BestCompression = 9
DefaultCompression = -1
)
type Dict struct { /* ... */ }
func ParseDict(enc []byte) (*Dict, error)
// ... 可能还包含 Marshal/Unmarshal 方法
type Reader struct { /* ... unexported fields ... */ }
func NewReader(r io.Reader) (*Reader, error)
func (z *Reader) Reset(r io.Reader) error
func (z *Reader) AddDict(*Dict)
func (z *Reader) SetRawDict([]byte)
func (z *Reader) Read(p []byte) (int, error)
func (z *Reader) Close() error
type Writer struct { /* ... unexported fields ... */ }
func NewWriter(w io.Writer) *Writer
func (z *Writer) Reset(w io.Writer)
func (z *Writer) SetLevel(int) error
func (z *Writer) AddDict(*Dict)
func (z *Writer) SetRawDict([]byte)
func (z *Writer) Write([]byte) (int, error)
func (z *Writer) Flush() error
func (z *Writer) Close() error
```


这个设计体现了 Go 标准库的哲学：

**Setter 模式：**采用 SetLevel、AddDict 等方法进行配置，而不是更复杂的构造函数重载或函数式选项，兼顾了灵活性和简洁性。**独立的 Dict 类型：**将字典抽象为 Dict 类型，通过 ParseDict 进行预处理。这解决了 Klaus 提出的“重复解析字典开销大”的问题，允许用户一次解析，多次复用。**错误处理：**关键配置（如 SetLevel、ParseDict）返回 error，增强了 API 的健壮性。

## 漫长的等待与社区英雄的登场

提案于 2024 年被接受，为何直到 2025 年底才真正启动？这背后反映了 Go 核心团队面临的现实挑战。Go 团队规模精简，核心成员的精力需要分配给语言、编译器、运行时等更高优先级的任务。提案发起者 dsnet 也深度参与了 json/v2 等重大项目，无暇分身。

在此期间，Klaus Post 主动请缨，表示愿意贡献一个精简版的、符合标准库要求的实现。然而，这个提议在当时并未得到明确的推进信号。

转机出现在 [2025 年 11 月的 Go 团队内部会议](https://github.com/golang/go/issues/43930#issuecomment-3487773597)。纪要显示，团队终于有带宽来审查社区对 compress/flate 和 compress/zstd 的贡献。会议明确提到：“很高兴有社区审查。我们能去问问 k8s 的人吗？”（意指寻求更多社区的反馈和测试）。这标志着官方正式为 Klaus Post 的贡献打开了大门。随后Klaus Post也给出了自己的贡献时间表，大约在2026年Q1提交第一版实现给Go团队审查。

## 小结：一次迟到但意义非凡的升级

compress/zstd 的加入，对 Go 生态而言，是一次迟到但意义非凡的升级。它不仅仅是增加了一个功能包，更是一次：

**技术的现代化：**用一个在性能和效率上全面超越 Gzip 的现代算法，武装 Go 的标准库。**生态的成熟：**将社区经过千锤百炼的最佳实践，以安全、稳健的方式融入官方标准。**模式的探索：**展示了在核心团队资源有限的情况下，如何通过与社区领袖的协作，共同推动语言生态向前发展。

对于广大 Go 开发者来说，未来已来。不久之后（或许在 Go 1.27），我们将能以最简单、最 Go-like 的方式，为我们的应用插上 Zstandard 的翅膀，轻松实现性能提升与成本节约。这无疑是 Go 社区协作精神的又一次伟大胜利。

## 参考资料

- https://github.com/golang/go/issues/62513
- https://blog.cloudflare.com/container-platform-preview
- https://discord.com/blog/how-discord-reduced-websocket-traffic-by-40-percent
- https://www.rfc-editor.org/rfc/rfc8878

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

大哥，感谢你的博客让我经常知道 golang 最新的进展， 很棒。

[手动抱拳]