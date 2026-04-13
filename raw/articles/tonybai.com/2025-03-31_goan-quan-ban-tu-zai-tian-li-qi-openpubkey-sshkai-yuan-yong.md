---
title: Go安全版图再添利器：OpenPubkey SSH开源，用SSO彻底改变SSH认证
url: https://tonybai.com/2025/03/31/openpubkey-ssh-open-source/
published: '2025-03-31'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go安全版图再添利器：OpenPubkey SSH开源，用SSO彻底改变SSH认证

![](../../assets/522a2165ddb3bdd0.png)


[本文永久链接](https://tonybai.com/2025/03/31/openpubkey-ssh-open-source) – https://tonybai.com/2025/03/31/openpubkey-ssh-open-source

对于许多开发者和运维工程师而言，管理SSH密钥是一项繁琐且易出错的任务。正如[SSH发明者、芬兰计算机科学家Tatu Ylonen](https://ylonen.org/index.html)所指出的，许多组织中过时授权密钥的数量甚至远超员工人数，这带来了巨大的安全隐患。现在，一个基于Go语言生态的创新项目——[OpenPubkey SSH (OPKSSH)](https://github.com/openpubkey/opkssh)，旨在彻底改变这一现状。近日，随着Cloudflare将[OPKSSH代码](https://github.com/openpubkey/opkssh)捐赠给Linux基金会下的[OpenPubkey项目](https://github.com/openpubkey)并将其开源，开发者们终于可以拥抱一种更便捷、更安全的SSH认证方式：使用熟悉的单点登录(SSO)系统。本文将简要介绍OPKSSH项目及其技术基石OpenPubkey技术。

## 1. 核心看点：OPKSSH 开源与价值解读

OPKSSH (OpenPubkey SSH) 是一个巧妙的工具，它将[OpenID Connect (OIDC)](https://tonybai.com/2023/12/22/understand-oidc-by-example/) 等现代SSO技术与[SSH协议](https://www.ssh.com/academy/ssh)集成起来，其核心目标是**消除手动管理和配置SSH公私钥的需求**，同时**不引入除身份提供商(IdP)之外的任何新的可信第三方**。

此前，虽然底层的[OpenPubkey协议已于2023年成为Linux基金会的开源项目](https://github.com/openpubkey/openpubkey)，但OPKSSH作为BastionZero（现已被Cloudflare收购）的产品，一直是闭源的。Cloudflare的此次捐赠，使得整个OpenPubkey技术栈的关键应用层实现也完全开放，这对于Go社区和整个基础设施安全领域都是一个重要进展。

![](../../assets/c4a0ab2f05ad651e.jpeg)


## 2. OPKSSH解决了什么痛点？

通常，我们在进行远程服务器管理和运维操作时会使用SSH免密登录，即通过生成SSH密钥对并将公钥复制到远程服务器来实现。但这种传统方式的SSH密钥管理存在诸多问题：

**密钥分发与轮换困难**：需要手动将公钥部署到目标服务器，密钥泄露或员工离职后的吊销流程复杂。**长期密钥风险**：长期存在的私钥增加了泄露风险，一旦泄露，影响范围广。**可见性差**：难以清晰追踪谁拥有对哪些服务器的访问权限，公钥本身缺乏身份信息。

这些问题常常困扰企业的IT运维团队和安全管理人员，他们需要确保访问控制的安全性和可管理性，同时降低操作复杂性和人力成本。

那如何解决这些问题呢？OPKSSH带来了新的解决方案。

## 3. OPKSSH如何解决这些问题？

OPKSSH基于[OpenPubkey协议](https://www.bastionzero.com/openpubkey-faq)，带来了革命性的改进：

**使用临时性密钥(Ephemeral Keys)提升安全性**

OPKSSH使用**按需生成的临时SSH密钥对**取代长期密钥。用户通过SSO登录后，OPKSSH自动生成有效期较短（默认为24小时，可配置）的密钥。这大大缩短了密钥泄露的风险窗口。

**通过单点登录(SSO Login)增强易用性**

用户只需运行opkssh login，通过熟悉的IdP (如Google, Azure AD等) 进行SSO认证，即可自动获取所需的SSH密钥。无需手动生成、复制或管理私钥文件，即可在任何安装了opkssh的机器上进行SSH连接。

**通过Identity-based Auth提升可见性与简化管理**

授权不再基于难以管理的公钥列表（比如~/.ssh/known_hosts），而是基于易于理解和审计的用户身份（如Email地址）。管理员只需在服务器配置中指定允许访问的电子邮件地址列表即可。

到这里你可能会问：这么好用的OPKSSH是如何工作的呢？别急，我们下面就来介绍一下OPKSSH的工作原理。

## 4. OPKSSH的工作原理

Cloudflare的文章中有一个很好的介绍Opkssh工作原理的例子和示意图，这里也借用过来：

![](../../assets/76bb9153e597a58d.png)


如图所示，当用户alice@example.com使用OPKSSH登录服务器，这个过程大致如下：

- 用户本地执行命令opkssh login触发OIDC流程，用户向IdP认证。
- OpenPubkey协议介入，在OIDC流程中巧妙地将用户
**临时生成的公钥**与用户的身份信息绑定，生成一个**PK Token**(本质上是一个增强的ID Token，包含了公钥信息并由IdP签名)。 - OPKSSH将此PK Token打包进一个临时的SSH 公钥文件（利用SSH证书的扩展字段）。
- 当用户发起SSH连接时，这个特殊的公钥文件被发送到服务器。
- 服务器配置了AuthorizedKeysCommand指令，调用opkssh verify(OpenPubkey验证器)。
- 验证器检查PK Token的有效性（签名、有效期、颁发者），提取公钥和用户身份(Email)，并根据服务器配置判断该用户是否有权访问。

关键在于，这一切**无需修改现有的SSH客户端或服务器软件本身**，仅需在服务器端sshd_config中添加两行配置即可启用，这个我们在本文后面会详细说明。

OPKSSH的魔力源于其底层的**OpenPubkey**协议。OpenPubkey本身是一个基于Go语言实现的Linux基金会项目 ([github.com/openpubkey/openpubkey](https://github.com/openpubkey/openpubkey))。

OpenPubkey的核心创新在于，它通过一种**客户端修改**的方式，将用户持有的公钥(PKu)与OIDC的ID Token进行了加密绑定，而**无需 OIDC 提供商(OP)作任何修改**。这是通过巧妙利用OIDC流程中的nonce参数实现的。客户端不再生成完全随机的nonce，而是生成一个包含其公钥等信息的**客户端实例声明(cic)**，并将cic的哈希值作为nonce发送给OP。OP在签发ID Token时会包含这个nonce。这样，最终得到的PK Token就同时承载了OP 对用户身份的认证以及用户对其公钥的所有权声明（通过客户端的额外签名防止身份误绑定攻击）。

这一机制将OIDC的认证模型从**持有者认证(Bearer Authentication)** 升级到了**持有证明(Proof-of-Possession, PoP)**。在Bearer模型下，任何窃取到ID Token的人都可以冒充用户；而在PoP模型下，用户需要证明自己持有与PK Token中公钥对应的私钥，从而有效抵御**令牌重放(Token Replay)** 和**令牌泄露(Token Export)** 攻击，安全性显著提高。

OpenPubkey的设计还考虑了可扩展性，例如引入MFA-Cosigner概念，可以进一步增强安全性，甚至在OP本身被攻陷的情况下也能提供保护。关于OpenPubkey协议设计的详细内容，可以参见参考资料中OpenPubkey的论文，这里就不赘述了。

了解了原理之后，下面我们来实际验证一下opkssh通过IdP实现SSO一键登录服务器的效果。

## 5. 使用opkssh实现免密登录服务器

这次验证的环境是这样的：

- 客户端：macOS
- 服务端：Ubuntu 22.04.1 LTS
- IdP：microsoft (注：国内访问microsoft的服务器成功率高)

我们先来看看客户端的操作步骤：

### 5.1 opkssh在客户端的操作

首先在客户端安装opkssh，你可以选择直接下载编译好的opkssh二进制文件：

```
$curl -L https://github.com/openpubkey/opkssh/releases/latest/download/opkssh-osx-amd64 -o opkssh; chmod +x opkssh
```


由于opkssh是纯Go实现的，如果你本地有Go工具链，也可以选择通过源码安装(在国内，可能选择源码安装的速度更快)：

```
$go install github.com/openpubkey/opkssh@latest
```


安装完成后，我们就来进行客户端的IdP认证。输入下面命令：

```
$opkssh login
INFO[0000] Opening browser to http://127.0.0.1:59638/chooser
```


该命令会打开本地浏览器，并展示下面页面：

![](../../assets/59ec8b3ec2c86668.png)


截止到目前，opkssh支持选择Google、Microsoft或Gitlab作为IdP，这里我们选择**Sign in with Microsoft**。

之后浏览器将跳转到下面页面：

![](../../assets/f04d5ad6ed597ada.png)


这里使用我的Microsoft账号进行身份认证，点击“接受”，即完成认证，之后你可以关闭页面！

而命令行也会提示下面信息：

```
INFO[0002] listening on http://127.0.0.1:3000/
INFO[0002] press ctrl+c to stop
Writing opk ssh public key to /Users/tonybai/.ssh/id_ed25519.pub and corresponding secret key to /Users/tonybai/.ssh/id_ed25519Keys generated for identity
Email, sub, issuer, audience:
bigwhite.cn@hotmail.com AAAAAAAAAAAAAAAAAAAAAP5YMhbf2Ufl_eI1PdK12VE https://login.microsoftonline.com/9188040d-6c67-4c5b-b112-36a304b66dad/v2.0 096ce0a3-5e72-4da8-9c86-12924b294a01
```


接下来，我们再来看看服务端要进行的操作与配置。

### 5.2 opkssh在服务端的操作

在要登录的服务器端安装opkssh，由于安装后还要进行一些设置，我建议直接采用opkssh项目提供的安装脚本进行安装：

```
$ wget -qO- "https://raw.githubusercontent.com/openpubkey/opkssh/main/scripts/install-linux.sh" | sudo bash
Detected OS is debian
Created group: opksshuser
Created user: opksshuser with group: opksshuser
Downloading version latest of opkssh from https://github.com/openpubkey/opkssh/releases/latest/download/opkssh-linux-amd64...
opkssh 100%[========================================================>] 16.01M 83.4MB/s in 0.2s
Installed opkssh to /usr/local/bin/opkssh
Configuring opkssh:
Creating sudoers file at /etc/sudoers.d/opkssh...
Adding sudoers rule for opksshuser...
Installation successful! Run 'opkssh' to use it.
```


之后我们需要修改一下服务端的sshd server的配置。SSH服务器支持一个名为AuthorizedKeysCommand的配置参数，该参数允许我们使用自定义程序来确定SSH公钥是否被授权。因此，我们通过对/etc/ssh/sshd_config文件进行以下两行更改，将SSH服务器的配置文件更改为使用OpenPubkey验证程序而不是SSH默认的验证程序：

```
AuthorizedKeysCommand /usr/local/bin/opkssh verify %u %k %t
AuthorizedKeysCommandUser opksshuser
```


然后通过opkssh添加授权的用户，这些用户登录后将具备root用户权限：

```
$opkssh add root bigwhite.cn@hotmail.com microsoft
Successfully added new policy to /etc/opk/auth_id
```


最后重启一下sshd服务：

```
$systemctl daemon-reload
$systemctl status sshd
```


### 5.3 ssh登录验证

注：为了避免使用之前的ssh免密登录，可以在服务端将.ssh/authorized_keys中的公钥删除！


服务端的opkssh命令行被sshd服务调用进行客户端验证时，会在/var/log/opkssh.log中打印相关日志，这也是opkssh起到作用的一个间接证明。

我在客户端依然以原先的ssh登录命令尝试登录服务器：

```
$ssh root@<your_server_ip>
```


我们在服务端opkssh.log中可以看到下面一些输出：

```
2025/03/29 02:57:43 /usr/local/bin/opkssh verify root AAAAKGVjZHNhLXNoYTItbDUQAAABVwZXJtaXQtWDExLWZvcndhcmRpbmcAAAAAAAAAF3Blcm1pdC1hZ2VudC1mb3J3YXJkaW5nAAAAAAAAABZwZXJtaXQtcG9ydC1mb3J3YXJkaW5nAAAAAAAAAApwZXJtaXQtcHR5AAAAAAAAAA5wZXJtaXQtdXNlci1yYwAAAAAAAAAAAAAAaAAAABNlY2RzYS1zaGEyLW5pc3RwMjU2AAAACG5pc3RwMjU2AAAAQQSXO9YZhMPnGkYfnwpFu/HeX29s7q0l4lK5qCgvaeaWh3zBSidDh49Nirsu5Iwh7YVRkKMa5q+hhnJEFAh7FL5LAAAAZAAAABNlY2RzYS1zaGEyLW5pc3RwMjU2AAAASQAAACEAqD5msj3BsQhlpszOJHBoIcmK3Ex/BwyNWKHgp6labScAAAAgULO5naYi9xOmzrShcGiVIprRbdSvdWltioSVKu63h6Y= ecdsa-sha2-nistp256-cert-v01@openssh.com
2025/03/29 02:57:43 Providers loaded: https://accounts.google.com 206584157355-7cbe4s640tvm7naoludob4ut1emii7sf.apps.googleusercontent.com 24h
https://login.microsoftonline.com/9188040d-6c67-4c5b-b112-36a304b66dad/v2.0 096ce0a3-5e72-4da8-9c86-12924b294a01 24h
https://gitlab.com 8d8b7024572c7fd501f64374dec6bba37096783dfcd792b3988104be08cb6923 24h
2025/03/29 02:57:44 warning: failed to load user policy: failed to read user policy file /root/.opk/auth_id: error reading root home policy using command /usr/bin/sudo -n /usr/local/bin/opkssh readhome root got output Failed to read user's home policy file: failed to open /root/.opk/auth_id, open /root/.opk/auth_id: no such file or directory
and err exit status 1
2025/03/29 02:57:44 successfully verified
```


之后，我就成功登录到服务器上了！

## 6.小结

OPKSSH 的开源是 OpenPubkey 项目和 Go 安全生态的重要里程碑。它不仅提供了一个解决 SSH 密钥管理难题的实用方案，也展示了 Go 语言在构建安全、可靠的基础设施工具方面的强大能力。

我们鼓励对安全、身份认证和 Go 开发感兴趣的开发者们：

**试用 OPKSSH**: 在你的开发或测试环境中体验 SSO 登录 SSH 的便捷。**关注 OpenPubkey 项目**: Star GitHub 仓库，了解最新动态。**参与社区贡献**: 通过 Pull Request、Issue 反馈、参与讨论等方式为项目贡献力量。可以在 OpenSSF Slack 的`#openpubkey`

频道找到社区成员，或参加每月一次的社区会议。

随着 OPKSSH 的加入和持续发展，我们期待 OpenPubkey 能够在更多场景下发挥价值，例如代码签名 (Sigstore 集成)、端到端加密通信等，进一步丰富和巩固 Go 语言在云原生和安全领域的基础设施地位。

## 7. 参考资料

[OPKSSH项目](https://github.com/openpubkey/opkssh/)– https://github.com/openpubkey/opkssh[Paper: OpenPubkey: Augmenting OpenID Connect with User held Signing Keys](https://eprint.iacr.org/2023/296)– https://eprint.iacr.org/2023/296[OpenPubkey项目](https://github.com/openpubkey/openpubkey/)– https://github.com/openpubkey/openpubkey/[Open-sourcing OpenPubkey SSH (OPKSSH): integrating single sign-on with SSH](https://blog.cloudflare.com/open-sourcing-openpubkey-ssh-opkssh-integrating-single-sign-on-with-ssh)– https://blog.cloudflare.com/open-sourcing-openpubkey-ssh-opkssh-integrating-single-sign-on-with-ssh[How to Use OpenPubkey to Solve Key Management via SSO](https://www.docker.com/blog/how-to-use-openpubkey-to-solve-key-management-via-sso)– https://www.docker.com/blog/how-to-use-openpubkey-to-solve-key-management-via-sso/[Open Pubkey Frequently Asked Questions](https://www.bastionzero.com/openpubkey-faq)– https://www.bastionzero.com/openpubkey-faq

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Gopher的AI原生应用开发第一课”、“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格6$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论