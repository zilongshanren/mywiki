---
title: 刚刚，2025图灵奖揭晓！面对即将瘫痪的传统密码学，Go 语言的“抗量子”底牌曝光
url: https://tonybai.com/2026/03/19/2025-turing-award-go-quantum-resistant-cryptography/
published: '2026-03-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 刚刚，2025图灵奖揭晓！面对即将瘫痪的传统密码学，Go 语言的“抗量子”底牌曝光

![](../../assets/859e9f28c3769bcf.png)


[本文永久链接](https://tonybai.com/2026/03/19/2025-turing-award-go-quantum-resistant-cryptography) – https://tonybai.com/2026/03/19/2025-turing-award-go-quantum-resistant-cryptography

大家好，我是Tony Bai。

就在昨天（2026 年 3 月 18 日），计算科学界的最高荣誉——ACM A.M. 图灵奖正式揭晓。[2025 年的图灵奖](https://awards.acm.org/about/2025-turing)，颁给了 Charles H. Bennett 和 Gilles Brassard 两位伟大的科学家，以表彰他们在**“量子密码学（Quantum Cryptography）”**和量子信息科学领域的开创性贡献。

或许你会觉得，图灵奖、量子力学、薛定谔的猫……这些高大上的词汇离我们每天 CRUD 的业务代码太遥远了。

但实际上，这场发端于理论物理界的革命，正在引发全球软件工程界一场最高级别的“红色预警”。

早期的图灵奖往往颁发给操作系统、数据库或编程语言的设计者(比如Unix 之父、B 语言（C 语言前身）以及 Go 语言联合设计者的[Ken Thompson](https://tonybai.com/2026/01/05/how-ken-thompson-developed-go-language-at-google))，而这次颁给[量子密码学](https://tonybai.com/2025/05/20/post-quantum-cryptography-in-go)，传递出了一个极其明确的信号：**传统的数字世界护城河，马上就要守不住了。**

今天，借着图灵奖揭晓的热点，我想和大家聊一个极其硬核、且关乎我们所有后端开发者未来饭碗的话题：**当“量子末日（Q-Day）”逼近，作为云原生时代绝对霸主的 Go 语言，手里究竟握着怎样的“抗量子底牌”？**

![](../../assets/3066932bc8ed6e06.png)


## 你的数据，正被黑客“先存后破”

在理解 Go 团队的动作之前，我们必须先弄懂，为什么我们需要“[后量子密码学（PQC）](https://tonybai.com/2025/05/20/post-quantum-cryptography-in-go)”？

目前，我们用来保护 HTTPS 流量、验证 JWT 登录、以及签署 Git 提交的底层基石，绝大多数是 [RSA 或 ECC（椭圆曲线）算法](https://mp.weixin.qq.com/s/RaKUi4HkomyrBJgcgTgiLw) 。这些算法的安全假设，建立在大质数分解和离散对数计算极其困难的数学事实上。

但早在 1994 年，Peter Shor 就提出了著名的 Shor 算法。该算法在数学上证明了：**只要拥有一台足够规模的量子计算机，RSA 和 ECC 算法不仅能被破解，而且破解速度是指数级倍增的！**

你可能会想：“量子计算机离真正商用还早着呢，急什么？”

黑客们可不这么想。现在全球的顶级黑客和某些国家级 APT 组织，正在疯狂执行一种名为 **“Store Now, Decrypt Later”（先收集，后破解，SNDL）** 的战略。

他们把现在截获的、由 RSA/ECC 加密的核心机密数据全部存储在硬盘里。等若干年后量子计算机成熟，他们就能在一瞬间把这些历史机密全部解开。

为了应对这场“降维打击”，美国国家标准与技术研究院（NIST）紧急发布了后量子密码学（PQC）的 FIPS 标准草案。而作为全球云基础设施底层语言的 Go，自然被推到了抗击量子危机的第一线。

## Go 团队的“抗量子”谋略

如果你经常关注 Go 社区，你会发现 Go 核心团队早就确定了引入新密码学算法的策略。在 Go 官方仓库的 Issue #64537（crypto: post-quantum support roadmap）中，现任 Go 安全团队负责人 Roland Shoemaker 和 Go 密码学专家 Filippo Valsorda 明确抛出了 Go 在面对量子危机时的三大铁律：

- 绝对不当小白鼠：Go 标准库只实现那些结构已经绝对稳定、并在业界（如 WebPKI、TLS）被广泛验证的算法。那些还在实验阶段的半成品，一律拒之门外。
- “按需”引入，绝不盲目：PQC 算法分为两类，一类是密钥封装（KEM，用于加密和协商密钥），一类是数字签名（Signature，用于身份认证）。
- “内测”转“公测”机制：任何新的 PQC 算法，Go 都会先在 internal 包中悄悄跑几个版本，等把所有可能的开发者“误用坑”都踩平了，才会暴露为 Public API。

基于这套严谨的哲学，Go 团队打出了他们的第一张底牌：优先解决“先收集后破解”的威胁。

在 Go 1.24 中，Go 已经通过提案 #70122 和 #69985，在底层网络库中悄然集成了 **ML-KEM（即 Kyber 算法）与 X25519 的混合密钥交换机制**。(注：ML-KEM 从 Go 1.23 就以实验特性引入)

这意味着，如果你使用的是最新的 Go 版本构建的 HTTPS 服务，你的连接在建立之初，就已经具备了抵抗未来量子计算机窃听的能力！

密钥交换的问题解决了，那么用来证明身份的**数字签名（Digital Signatures）**呢？这就引出了 Go 团队即将放出的第二张王炸。

## 揭开 crypto/mldsa 的硬核源码

数字签名的重要性不言而喻：微服务之间的 mTLS 认证、固件升级包的防篡改、区块链的交易防伪，全靠它。

就在最近，Filippo 在 Go 官方 GitHub 上正式提交了 [Issue #77626（proposal: crypto/mldsa: new package）](https://github.com/golang/go/issues/77626)，提议在即将到来的 Go 1.27 中，正式向全世界暴露 ML-DSA（NIST FIPS 204 标准）的公有 API。

让我们剥开这层提案，看看顶级大厂架构师是如何设计这套跨时代 API 的。

### 极简的参数集隔离

ML-DSA 并不是一个单一算法，它包含了不同的安全级别。Go 提案非常干净利落地定义了三个常量函数：

```
func MLDSA44() Parameters // 推荐日常使用，安全级别相当于 AES-128
func MLDSA65() Parameters // 相当于 AES-192
func MLDSA87() Parameters // 极高安全级别，相当于 AES-256
```


开发者不需要去记忆复杂的参数结构，只需像拼积木一样调用。

### 拒绝“半展开密钥”，将安全做到极致

如果你看源码，会发现 NewPrivateKey 除了传入 params 参数集外，只需要传入一个极短的 seed（种子字节），而不是业内的“半展开密钥（Semi-expanded keys）”。

为什么？Filippo 在讨论中给出了让人拍案叫绝的解释：

“半展开密钥是一个极其糟糕的格式。它不仅占用空间更大，加载速度更慢，而且

更危险。我们只会支持基于 Seed 的密钥派生。”

这体现了 Go 始终如一的安全哲学：如果一种格式[有被开发者误用的风险](https://tonybai.com/2026/01/18/go-cryptography-principles/)，那就从 API 层面彻底物理隔绝它。

### 巧妙应对“预哈希（External μ）”难题

传统签名时，我们通常先用 SHA256 算个 Hash，再对 Hash 签名。但 ML-DSA 的底层数学机制非常复杂，它要求对 H(H(pubkey) || 0×00 || context || message) 进行极度严苛的处理。

Go 团队没有去破坏原有的 crypto.Signer 接口，而是极其巧妙地发明了一个“虚拟的占位符”：crypto.MLDSAMu。

这个常量虽然属于 Hash 类型，但它不支持被实例化，调用 New() 会直接引发 Panic。它仅仅作为一个“信号标记”传递给 SignerOpts，优雅地实现了向下兼容。

## 为什么我们还不能在 X.509 证书里用它？

看到这里，很多着急的开发者（尤其是一些政企、军工背景的开发团队，正面临 CNSA 2.0 强制要求在 2025 年升级 PQC 的死命令）在 Issue 里疯狂催问：

*“API 都做好了，为什么不顺手把它集成进 crypto/x509 证书解析里？为什么还不让在 TLS 中直接使用 ML-DSA 证书？”*

Filippo 的回答，直接揭露了目前后量子时代最尴尬的一个物理瓶颈，也展现了他作为世界级密码学家的**极致架构克制**：

“如果我们现在就把 ML-DSA-87 塞进 TLS，你知道一个 TLS 握手包会变得多大吗？

足足 19KB！”

大家要知道，传统的 RSA 签名不过几百字节，ECC 签名更是只有几十个字节。我们过去 30 年的互联网协议（如 TCP/IP、TLS），都是建立在“签名数据极小、传输成本几乎为零”的物理假设上的。

如果你用 ML-DSA 给证书签名，证书链上一叠加，一次最普通的 HTTPS 握手，瞬间需要传输几十 KB 的数据。在移动网络弱网环境下，这会导致大规模的丢包、延迟飙升，甚至是全球互联网的“大塞车”。

**为了通过安全审计而罔顾物理性能，这不是高级软件工程，这是在耍流氓。**

Go 团队的判断是：我们有时间去设计更好的协议（比如使用 Merkle Tree 证书），而不是现在急功近利地把数万字节的“肥胖签名”强塞进原本轻巧的 TLS 隧道里。

**这种“不将就”的架构底线，正是 Go 语言最迷人的地方。**

## 小结：在不确定的未来中，拥抱底层逻辑

图灵奖颁给量子密码学，不仅是对 Bennett 和 Brassard 两位科学先驱的最高致敬，更吹响了全球软件工程界系统升级的冲锋号。

从优先落地对抗 SNDL 攻击的 ML-KEM，到极度克制、优雅设计的 crypto/mldsa，再到坚决抵制“19KB 肥胖握手包”的底线坚守。我们看到的是 Go 语言团队对工程效率、安全性与网络物理特性的深度掌控。

资料链接：

- https://awards.acm.org/about/2025-turing
- https://github.com/golang/go/issues/64537
- https://github.com/golang/go/issues/77626

**今日互动探讨**

如果在未来两年，为了抗击量子计算机，我们所有的 HTTPS 请求都要变慢 200 毫秒，甚至服务器内存消耗要翻倍，你觉得这个代价值得吗？在你的业务线里，有面临密码学升级的强制合规要求吗？

欢迎在评论区分享你的看法！

还在为“复制粘贴喂AI”而烦恼？我的新专栏 **《 AI原生开发工作流实战》** 将带你：

- 告别低效，重塑开发范式
- 驾驭AI Agent(Claude Code)，实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

扫描下方二维码，开启你的AI原生开发之旅。

![](../../assets/305ffd23f32ce780.png)


你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论