---
title: 通过实例理解Web应用的机密管理
url: https://tonybai.com/2023/11/08/understand-go-web-secret-management-by-example/
published: '2023-11-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解Web应用的机密管理

![](../../assets/4c134ba37485e870.png)


[本文永久链接](https://tonybai.com/2023/11/08/understand-go-web-secret-management-by-example) – https://tonybai.com/2023/11/08/understand-go-web-secret-management-by-example

如果你是一个Web应用系统的开发人员，你的日常大概率是“乐此不疲”地做着[CRUD](https://www.codecademy.com/article/what-is-crud)的活儿，很少接触到安全方面的内容。如果这时有人和你提到“机密(信息)管理(secret management)”，你大概率会说：那是啥？和我有关系吗？

你只是大多应用系统开发人员中的一个**典型代表**。现阶段，很多开发人员，尤其是业务应用开发人员在工作中较少甚至没有接触过专门的机密管理系统，在系统设计时也较少考虑到机密管理方面的要求，精力仍主要集中在保证系统功能的正确性、性能等方面。这种对安全的重视程度不够，不了解机密管理的现象较为普遍，下面是一些常见的表现：

- 明文存储密码、密钥等敏感数据

很多项目依然直接将用户密码、数据库连接密码、第三方服务密钥等信息明文写在代码或配置文件中，存在被攻击者直接获取的风险。

- 硬编码密钥与密码

重复地在代码中多次硬编码密码、密钥等机密信息，导致不能统一变更及管理。

- 使用弱密码、未定期更换

使用常见的弱密码，或使用默认或长期不变更的密码，很容易被猜测或破解。

- 不同环境复用同一密钥

开发、测试、生产环境复用同一密钥，一旦泄露将影响所有环境。

- 明文传输密码

HTTP传输中明文传递密码，导致可被嗅探截获。

- 日志中输出明文密码

调试日志中直接输出数据库密码等敏感信息，可能被利用。

- 缺乏访问控制和审计机制

密钥等资源无访问控制，且操作不被审计，难以追踪。

这些现象的普遍存在表明当前对于机密管理的重要性认知还有待提高，尤其是在当前互联网/移动互联网安全形势日益严峻的情况下，开发人员在系统开发的每个环节都应该意识到机密管理的重要性，并将机密管理纳入开发流程的各个阶段，这可以帮助大家构建出更可靠、安全的系统。

在这篇文章中，我就和大家一起来了解一下什么是机密管理，日常进行Web应用开发过程中该如何集成机密管理来保证机密信息在存储、传输、使用过程中的安全，最后，通过实例的方式来剖析Web应用是如何对一些典型的机密信息进行机密管理的。

## 1. 认识机密管理

在IT领域，机密管理是一种网络安全最佳实践，用于持续地、自动化地管理和保护数字身份验证凭证(如密码、密钥、API令牌等机密信息)，确保这些机密信息只能被经过授权的实体在严格的访问控制下使用。

机密管理拥有一套自己的核心管理措施，包括：

- 从代码、配置文件和其他未经受保护的区域中删除明文机密信息，将机密信息与代码/配置隔离存储;
- 执行最小特权(Least Privilege)原则，即设计访问控制时，用户和程序只会被授予执行其任务所需的最小/最低权限；
- 执行严格的访问控制(尤其是要对所有非人类凭证的访问请求进行验证)，并对所有访问进行跟踪和全面审计；
- 定期对机密信息(secrets)和凭证(credentials)进行轮转(rotate)；
- 自动管理机密信息的全生命周期，例如存储、分发、轮转等，并应用一致的访问策略；
- … …

机密管理涉及要管理的机密信息的类型包括(但不限于)：

- 用户密码或自动生成的密码
- API和其他应用程序的密钥(Key)/凭证（包括容器内的密钥/凭证）
- SSH密钥
- 数据库和其他system-to-system的密码
- 用于安全通信、传输和接收数据的私人证书（TLS、SSL 等）
- RSA和其他一次性密码设备

综合上面信息，我们看到机密管理不仅有一套严格的管理措施，而且要管理的机密信息的类型也是很多，并且随着软件系统复杂性的增加，云原生应用兴起，需要管理的机密类型和数量激增，不仅包括传统的密码和密钥，还有云平台的访问证书、微服务间的通信令牌等；管理难度也会大大提高。远程访问和云部署使得传统的边界安全防护变得困难。机密信息传输和存储的渠道更多，风险也上升。高速迭代的软件交付流程和自动化部署，也要求机密管理能同步地快速响应和自动化，机密管理面临着越来越大的挑战。面对这些挑战，业界迫切需要引入自动化、智能化和专业化的**机密管理系统**来应对。

## 2. 机密管理系统

机密管理系统是一套专业的用于集中存储、管理、控制和监控机密信息的安全解决方案。机密管理系统的发展经历了一个从分散到集中、从静态到动态、从本地到云端、从加密到访问控制、从人工操作到DevOps自动集成的发展历程，这个历程大致可分为如下几个阶段：

- 文件加密阶段

早期开发人员通过对文档和配置文件进行加密来保护机密信息，代表技术是PGP等加密软件。但很显然，这种方式操作不便，不支持访问控制等高级功能。

- 自建解决方案阶段

企业开始自研一些机密管理解决方案(包括基于一些像[KeePass](https://keepass.info)这样的开源项目)，但功能有限，更多是局限于满足企业自己的需求，很少支持跨平台和集中管理等功能。

- 开源机密管理项目

随着云计算时代的到来，开源社区推出了支持云和容器的自动化机密管理项目，例如：[Vault](https://github.com/hashicorp/vault/)、[Keywhiz](https://github.com/square/keywhiz)等，这些项目的一些公同的功能特性包括：轻量化实现、支持访问控制、提供机密信息版本控制、提供审计功能、提供API便于应用集成、支持与 CI/CD 工具集成、支持Docker、Kubernetes等容器平台等。这一时期的开源机密管理系统大大简化了机密管理流程，为随后的云原生机密管理平台的发展奠定了基础。

注：Keywhiz目前2023年9月宣布不再开发，建议使用Hashicorp Vault。


- 云原生机密管理平台

在开源机密管理项目的基础之上，这些开源项目背后的开发商以及一些专业的公有云提供商开始面向云原生应用和DevOps，以SaaS形式提供专业的机密管理服务和全面的机密管理解决方案，如[Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault/)、[Google Secret Manager](https://cloud.google.com/secret-manager)、[AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)、HashiCorp Vault等。

我们看到：专业的机密系统发展到今天的水平，其过程不是一蹴而就的。正是基于历史经验的积累和总结，现代机密管理平台才演化出了面向云原生架构、支持DevOps、细粒度访问控制、机密信息的动态化以及生命周期的自动化管理等先进功能特性。

在上面的优秀的云原生机密管理系统中，HashiCorp Vault是唯一开源且可以私有化部署在企业内部的。[HashiCorp公司于2015年发布并开源了Vault](https://www.hashicorp.com/blog/vault-announcement)，经过多年发展，Vault已经发展成为一款功能强大的企业级机密管理系统，并被广泛视为云原生领域的首选解决方案。

对于普通Web应用开发者而言，**既要有机密管理的意识，又要有机密管理的实现手段**。HashiCorp Vault的设计目标之一就是将机密管理下沉到平台层面，让应用开发者能够专注于应用程序的开发而无需过多关注机密的管理和保护。

作为Web应用开发者，基于Vault实现Web应用的机密管理是一条非常可行的机密管理方案。通过与Vault的集成，Web应用开发者可以利用Vault提供的丰富功能来处理各种机密管理需求和场景。开发者只需要学习如何使用Vault的API或客户端库与Vault进行交互，就能轻松地访问和管理机密数据，实现机密信息(如数据库凭据、API 密钥等)获取、动态机密信息生成、访问控制、审计和监控等机密管理功能，并且可以减少机密管理的开发和维护的复杂性。

接下来，我就和大家一起简要的了解一下Hashicorp的Vault。

## 3. 认识Vault

### 3.1 Vault的架构

如果对Hashicorp这家公司很熟悉，你肯定知道Hashicorp大部分产品(和开源项目)都是由Go开发的，包括[consul](https://tonybai.com/2018/09/10/setup-service-discovery-and-load-balance-based-on-consul/)、[nomad](https://tonybai.com/2019/03/30/cluster-management-and-microservice-deployment-and-scheduled-by-nomad/)、[terraform](https://github.com/hashicorp/terraform)以及[vagrant](https://github.com/hashicorp/vagrant)([vagrant的新版本将切换到go实现](https://discuss.hashicorp.com/t/status-of-vagrant-go/42562))等。

Vault这款优秀的机密管理软件系统继承了Hashicorp的开发基因，也是由Go语言开发的。从2015年至今，Vault已经演化为一个功能强大，但相对也比较复杂的系统，下面是[Hashicorp官方架构文档](https://developer.hashicorp.com/vault/docs/internals/architecture)中的一个关于Vault的high level的结构示意图：

![](../../assets/bee30784395ddd9a.png)


从整体架构设计思路来看，vault支持：

- 高可用性

Vault的架构设计允许部署多个Vault服务器以实现高可用性和容错性，在[高可用集群部署模式](https://developer.hashicorp.com/vault/docs/internals/high-availability)下，多个vault服务器共享存储后端，并且每个vault服务器可能是两个状态：active和standby。任意时刻集群都只有一个实例处于active状态，所有standby实例都处于热备用状态(hot standby)。只有处于active状态的服务器会处理所有请求；standby服务器会将所有请求重定向到活动Vault服务器，这点与consul的设计是一致的。如果active服务器被sealed、发生故障或失去网络连接，则standby Vault服务器中的一个将成为active实例。

这里有人可能会问：如果只有一个active实例，那么在访问量增大的时候，active实例便会成为热点或性能瓶颈！没错，这是vault开源版本的约束。这个约束在vault的企业付费版中被取消，在付费版中，standby服务器可以接收只读请求，所有只读请求会均衡分担到各个standby实例上，如果standby实例收到写请求，它会将写请求转发给active实例处理。

- 封存和解封

说高可用性时，我们提到了vault服务器实例的sealed(封存)状态。启动Vault服务器时，它会处于sealed状态。在这种状态下，Vault仅知道访问物理存储的位置和方式，但不知道如何解密存储中数据。在unseal(解封)之前，该vault服务器几乎无法做任何操作。在对处于sealed状态的Vault实例进行任何操作之前，必须对其进行解封(unseal)。

解封操作需要提供**解封密钥(unseal keys)**。有人注意到了，我用了unseal keys，而不是unseal key，因为解封密钥是由一种名为[Shamir’s Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing)的算法分解保存和汇集生成的。Shamir’s Secret Sharing（Shamir的机密分享算法）是一种密码学算法，用于将机密数据(在本文中指的就是“unseal key”)分割成多个部分，称为shares。这些share可以被分发给不同的人，如下图所示：

![](../../assets/c4cee49de65342a9.png)


而只有当足够数量的share被汇集时，才能恢复出原始的机密数据(unseal key)，并用恢复出的机密数据进行下一步操作(如下图所示，下图来自Hashicorp官方文档)：

![](../../assets/7980364aac84e01a.png)


在这幅图中，当汇集一定个数的unseal keys’share后，vault就能够重构解封密钥(“unseal key”)，然后用它来解密得到根密钥(root key，也称为master key)，根密钥再被用来解密得到加密密钥(Encryption key)用于保护所有vault的数据，即这个Encryption key就是后续参与机密数据加解密的密钥。

注：实际生产部署时，究竟要如何对Vault Server进行unseal，

[HashiCorp提供了一些unseal pattern]供大家参考。

- 加密层

前面架构图中左侧南北横贯多层的部分是Vault的加密层，被称为**barrier**，负责对Vault数据进行加密和解密，确保数据在存储和传输过程中的机密性和完整性。Vault服务器启动时，会将数据写入存储后端。由于存储后端位于barrier之外，被视为不可信的(与零信任网络理念一致)，因此Vault会在将数据发送到存储后端之前对其进行加密。这种机制确保了即便恶意攻击者试获取了对存储后端的访问权限，其拿到的数据仍然保持加密状态。

- 认证和授权

如下图(来自Hashicorp官方文档)，当客户端首次连接到Vault时，需要进行身份验证。Vault提供可配置的认证方法，并在身份验证机制上提供灵活性。操作员可以使用用户名/密码等机制进行身份验证，而应用程序可以使用公钥/私钥或令牌进行身份验证。 Core（核心）负责管理请求的流程，包括流经哪个身份验证方法来确定请求是否有效，并得到关联策略的列表，执行访问控制规则（ACLs），确保审计日志记录，并将请求路由到相应的机密引擎进行处理。

![](../../assets/56bc7a58c1e7175b.png)


- 策略管理

策略是一组命名的访问控制规则。Vault内置了一些策略，如”root”策略，允许对所有资源的访问。用户可以创建任意数量的命名策略，并对路径进行细粒度的控制。除非通过策略明确授权，否则不允许进行操作。

- 机密引擎

Vault使用机密引擎来生成和管理动态机密数据，如临时凭据、API密钥等。机密引擎的类型可以是静态的，如数据库凭据，也可以是动态的，如 AWS IAM凭据。机密引擎根据配置的规则和策略生成和提供机密数据。

- 审计和日志记录

Vault记录请求和响应的审计日志，并有Audit Broker(审计代理)将其分发到配置的审计设备(audit device)。审计日志用于监控和审计对Vault的访问和操作。

- Expiration Manager（租期管理）

Vault由Expiration Mgr管理令牌和机密数据的过期，自动回收已过期的客户端令牌和机密数据。

- Token Store（令牌存储）

Token Store生成和管理客户端令牌，用于进行后续的请求操作。令牌类似于网站登录时发送的 cookie，用于验证客户端的身份和授权。

以上是Vault的主要架构设计思路和各部分的功能范围。Vault的架构保证了安全性、高可用性和可扩展性，使用户能够安全地管理和保护机密信息。

### 3.2 Vault的安全模型

Vault是做机密信息管理的，其自身安全模型是否完善直接关系到应用系统的安全。Vault官方也十分重视这点，在[官方文档中也对其安全模型做了说明](https://developer.hashicorp.com/vault/docs/internals/security)，这里梳理一下。

Vault的安全模型旨在提供数据的机密性、完整性、可用性、可追溯性和认证性。以下是Vault安全模型的几个设计要点：

- 通信安全

Vault要求客户端与服务器之间的通信通过TLS建立安全通道，以确保通信的机密性和完整性。此外，Vault服务器之间的集群通信也使用相互认证的TLS，以保护数据在传输过程中的机密性和完整性。

- 身份验证和授权

前面说架构时提及过：所有客户端请求必须经过适当的身份验证和授权。当客户端首次进行身份验证时，Vault使用认证方法验证客户端的身份，并返回与其关联的ACL策略列表。每个请求都需要提供有效的客户端令牌，Vault根据令牌验证其有效性，并生成基于关联策略的访问控制列表（ACL）。

- 数据安全

Vault对于存储在后端的数据，以及在传输过程中的数据，都要求保证安全。Vault使用256位的高级加密标准（AES）密码和96位随机数作为加密密钥，对离开Vault的所有数据进行加密。同时，在解密过程中验证Galios Counter Mode（GCM）的认证标签，以检测任何篡改。

- 内部威胁保护

Vault关注内部攻击威胁，即已经获得某种程度Vault访问权限的攻击者企图获取未经授权的机密信息。Vault在客户端进行身份验证时，使用事先配置的关联策略列表来生成客户端令牌，并使用严格的默认拒绝策略来进行访问控制。每个策略指定对Vault中路径的访问级别，最终的访问权限由所有关联策略中最高级别的权限决定。

- 密钥管理

Vault使用Shamir’s Secret Sharing技术来实现密钥的管理和保护unseal key，本质上也是对Root key和Encryption key的保护。只有在提供足够数量的share时，才能恢复unseal密钥，这样可以避免对单个持有者的绝对信任，同时也不需要存储完整的加密密钥。

但需要注意的是，Vault的安全模型并不涵盖所有可能的威胁和攻击，例如对存储后端的完全控制、存储后端中存在的秘密信息的泄露、运行中的Vault实例内存分析等。此外，Vault还依赖于外部系统或服务的安全性，如果这些外部系统存在漏洞或受到攻击，可能会导致Vault中数据的机密性或完整性受到威胁。

说了这么多Vault，Vault究竟长什么样？应该如何用呢？接下来我们简单介绍一下Vault的安装和使用，也是为后续的实例部分做个铺垫。

### 3.3 Vault的安装

[Vault支持多种形式的安装部署](https://developer.hashicorp.com/vault/docs/install)，包括基于预编译好的二进制文件(precompiled binary)、基于容器或包管理器等，你甚至可以自己基于源码编译。

我这里使用的是Precompiled binary方式，将Vault直接部署在我的开发环境下，一台MacBook Pro上。

Precompiled binary下载后就是一个可执行文件，把它放到特定路径下，并在PATH环境变量中将这个路径加入进来，环境变量生效后，你就可以在任意路径下使用vault命令了。

下面的命令打印了下载的vault的版本：

```
$vault -v
Vault v1.15.1 (b94e275f25ccd9011146d14c00ea9e49fd5032dc), built 2023-10-20T19:16:11Z
```


通过-h命令行参数，可以查看vault的命令帮助信息：

```
$vault -h
Usage: vault <command> [args]
Common commands:
read Read data and retrieves secrets
write Write data, configuration, and secrets
delete Delete secrets and configuration
list List data or secrets
login Authenticate locally
agent Start a Vault agent
server Start a Vault server
status Print seal and HA status
unwrap Unwrap a wrapped secret
Other commands:
audit Interact with audit devices
auth Interact with auth methods
debug Runs the debug command
events
kv Interact with Vault's Key-Value storage
lease Interact with leases
monitor Stream log messages from a Vault server
namespace Interact with namespaces
operator Perform operator-specific tasks
patch Patch data, configuration, and secrets
path-help Retrieve API help for paths
pki Interact with Vault's PKI Secrets Engine
plugin Interact with Vault plugins and catalog
policy Interact with policies
print Prints runtime configurations
proxy Start a Vault Proxy
secrets Interact with secrets engines
ssh Initiate an SSH session
token Interact with tokens
transform Interact with Vault's Transform Secrets Engine
transit Interact with Vault's Transit Secrets Engine
version-history Prints the version history of the target Vault server
```


注：Vault继承了Hashicorp产品的一贯风格，即将所有功能放到一个程序中，各个功能通过subcommand的形式提供，比如vault server、vault agent、vault proxy等。如果你了解consul，你会发现consul就是这样的。


### 3.4 Vault的启动(dev模式)

生产环境的Vault部署、配置、启动以及unseal过程还是蛮复杂的，[HashiCorp给了一些参考集群架构](https://developer.hashicorp.com/vault/tutorials/day-one-consul/multi-cluster-architecture)，这些可以交给运维同学去琢磨。

对于开发人员而言，日常将应用与Vault集成实现机密管理的时候，只需在本机或远程开发机上启动dev模式的Vault实例即可，这里我们也基于dev模式来启动一个单实例的Vault：

```
$vault server -dev
==> Vault server configuration:
Administrative Namespace:
Api Address: http://127.0.0.1:8200
Cgo: disabled
Cluster Address: https://127.0.0.1:8201
Environment Variables: Apple_PubSub_Socket_Render, CLASSPATH, CLISH_PATH, ETCDCTL_API, GITEA_WORK_DIR, GODEBUG, GONOPROXY, GONOSUMDB, GOPATH, GOPRIVATE, GOPROXY, GOROOT, GOSUMDB, HOME, HOMEBREW_BOTTLE_DOMAIN, LANG, LC_CTYPE, LESS, LOGNAME, LSCOLORS, MML_HOME, NVM_BIN, NVM_CD_FLAGS, NVM_DIR, OLDPWD, OPENCV_PATH, PAGER, PATH, PWD, PYTHONPATH, RUSTUP_DIST_SERVER, RUSTUP_UPDATE_ROOT, SHELL, SHLVL, SSH_AUTH_SOCK, TERM, TERM_PROGRAM, TERM_PROGRAM_VERSION, TERM_SESSION_ID, TMPDIR, USER, XPC_FLAGS, XPC_SERVICE_NAME, ZSH, _
Go Version: go1.21.3
Listener 1: tcp (addr: "127.0.0.1:8200", cluster address: "127.0.0.1:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
Log Level:
Mlock: supported: false, enabled: false
Recovery Mode: false
Storage: inmem
Version: Vault v1.15.1, built 2023-10-20T19:16:11Z
Version Sha: b94e275f25ccd9011146d14c00ea9e49fd5032dc
==> Vault server started! Log data will stream in below:
2023-11-06T10:25:37.723+0800 [INFO] proxy environment: http_proxy="" https_proxy="" no_proxy=""
2023-11-06T10:25:37.727+0800 [INFO] incrementing seal generation: generation=1
2023-11-06T10:25:37.727+0800 [WARN] no `api_addr` value specified in config or in VAULT_API_ADDR; falling back to detection if possible, but this value should be manually set
2023-11-06T10:25:37.733+0800 [INFO] core: Initializing version history cache for core
2023-11-06T10:25:37.734+0800 [INFO] events: Starting event system
2023-11-06T10:25:37.736+0800 [INFO] core: security barrier not initialized
2023-11-06T10:25:37.737+0800 [INFO] core: security barrier initialized: stored=1 shares=1 threshold=1
2023-11-06T10:25:37.744+0800 [INFO] core: post-unseal setup starting
2023-11-06T10:25:37.758+0800 [INFO] core: loaded wrapping token key
2023-11-06T10:25:37.758+0800 [INFO] core: successfully setup plugin runtime catalog
2023-11-06T10:25:37.758+0800 [INFO] core: successfully setup plugin catalog: plugin-directory=""
2023-11-06T10:25:37.760+0800 [INFO] core: no mounts; adding default mount table
2023-11-06T10:25:37.765+0800 [INFO] core: successfully mounted: type=cubbyhole version="v1.15.1+builtin.vault" path=cubbyhole/ namespace="ID: root. Path: "
2023-11-06T10:25:37.774+0800 [INFO] core: successfully mounted: type=system version="v1.15.1+builtin.vault" path=sys/ namespace="ID: root. Path: "
2023-11-06T10:25:37.777+0800 [INFO] core: successfully mounted: type=identity version="v1.15.1+builtin.vault" path=identity/ namespace="ID: root. Path: "
2023-11-06T10:25:37.783+0800 [INFO] core: successfully mounted: type=token version="v1.15.1+builtin.vault" path=token/ namespace="ID: root. Path: "
2023-11-06T10:25:37.785+0800 [INFO] rollback: Starting the rollback manager with 256 workers
2023-11-06T10:25:37.787+0800 [INFO] rollback: starting rollback manager
2023-11-06T10:25:37.789+0800 [INFO] core: restoring leases
2023-11-06T10:25:37.791+0800 [INFO] identity: entities restored
2023-11-06T10:25:37.791+0800 [INFO] identity: groups restored
2023-11-06T10:25:37.791+0800 [INFO] expiration: lease restore complete
2023-11-06T10:25:37.793+0800 [INFO] core: Recorded vault version: vault version=1.15.1 upgrade time="2023-11-06 02:25:37.793171 +0000 UTC" build date=2023-10-20T19:16:11Z
2023-11-06T22:25:38.367+0800 [INFO] core: post-unseal setup complete
2023-11-06T22:25:38.368+0800 [INFO] core: root token generated
2023-11-06T22:25:38.368+0800 [INFO] core: pre-seal teardown starting
2023-11-06T22:25:38.369+0800 [INFO] rollback: stopping rollback manager
2023-11-06T22:25:38.369+0800 [INFO] core: pre-seal teardown complete
2023-11-06T22:25:38.370+0800 [INFO] core.cluster-listener.tcp: starting listener: listener_address=127.0.0.1:8201
2023-11-06T22:25:38.370+0800 [INFO] core.cluster-listener: serving cluster requests: cluster_listen_address=127.0.0.1:8201
2023-11-06T22:25:38.371+0800 [INFO] core: post-unseal setup starting
2023-11-06T22:25:38.371+0800 [INFO] core: loaded wrapping token key
2023-11-06T22:25:38.371+0800 [INFO] core: successfully setup plugin runtime catalog
2023-11-06T22:25:38.371+0800 [INFO] core: successfully setup plugin catalog: plugin-directory=""
2023-11-06T22:25:38.372+0800 [INFO] core: successfully mounted: type=system version="v1.15.1+builtin.vault" path=sys/ namespace="ID: root. Path: "
2023-11-06T22:25:38.372+0800 [INFO] core: successfully mounted: type=identity version="v1.15.1+builtin.vault" path=identity/ namespace="ID: root. Path: "
2023-11-06T22:25:38.372+0800 [INFO] core: successfully mounted: type=cubbyhole version="v1.15.1+builtin.vault" path=cubbyhole/ namespace="ID: root. Path: "
2023-11-06T22:25:38.373+0800 [INFO] core: successfully mounted: type=token version="v1.15.1+builtin.vault" path=token/ namespace="ID: root. Path: "
2023-11-06T22:25:38.373+0800 [INFO] rollback: Starting the rollback manager with 256 workers
2023-11-06T22:25:38.373+0800 [INFO] rollback: starting rollback manager
2023-11-06T22:25:38.374+0800 [INFO] core: restoring leases
2023-11-06T22:25:38.374+0800 [INFO] expiration: lease restore complete
2023-11-06T22:25:38.374+0800 [INFO] identity: entities restored
2023-11-06T22:25:38.374+0800 [INFO] identity: groups restored
2023-11-06T22:25:38.374+0800 [INFO] core: post-unseal setup complete
2023-11-06T22:25:38.374+0800 [INFO] core: vault is unsealed
2023-11-06T22:25:38.386+0800 [INFO] core: successful mount: namespace="" path=secret/ type=kv version=""
WARNING! dev mode is enabled! In this mode, Vault runs entirely in-memory
and starts unsealed with a single unseal key. The root token is already
authenticated to the CLI, so you can immediately begin using Vault.
You may need to set the following environment variables:
$ export VAULT_ADDR='http://127.0.0.1:8200'
The unseal key and root token are displayed below in case you want to
seal/unseal the Vault or re-authenticate.
Unseal Key: KiF1ohtchsOjr4IvzHY38/OAPOqS1/rARczTFG6Ull8=
Root Token: hvs.9QOJsa7zlwHO8ieW15CXXoOp
Development mode should NOT be used in production installations!
```


我们看到dev模式下，Vault server是自动unseal的，并打印出了Unseal Key和Root Token，而且显式地告诉你：所有机密数据都是存储在内存中的，**不要将这个模式用于生产环境**。

前面说过，vault程序继承了Hashicorp产品的基因，它既可以用来启动server，其自身也是一个命令行程序，我们可以用vault命令查看启动的server的状态：

```
$vault status
Error checking seal status: Get "https://127.0.0.1:8200/v1/sys/seal-status": http: server gave HTTP response to HTTPS client
```


我们看到：获取vault server状态的命令执行失败，因为我们并没有开启vault server的https端口，仅使用了http端口。我们设置一下环境变量后，再执行status命令：

```
$export VAULT_ADDR='http://127.0.0.1:8200' // 设置vault server addr为http非安全方式
$vault status
Key Value
--- -----
Seal Type shamir
Initialized true
Sealed false
Total Shares 1
Threshold 1
Version 1.15.1
Build Date 2023-10-20T19:16:11Z
Storage Type inmem
Cluster Name vault-cluster-23f54192
Cluster ID a86c14e2-b88c-5391-e8b4-0b1b9e9a9aaf
HA Enabled false
```


接下来，我们试着向Vault写入一个机密信息。Vault支持多种secret engine，比如：[Key/Value secrets engine](https://developer.hashicorp.com/vault/tutorials/secrets-management/static-secrets)、[Versioned Key/value secrets engine(k/v引擎的v2版本)](https://developer.hashicorp.com/vault/tutorials/secrets-management/versioned-kv)、[LDAP secrets engine](https://developer.hashicorp.com/vault/tutorials/secrets-management/openldap)、[Azure secrets engine](https://developer.hashicorp.com/vault/tutorials/secrets-management/azure-secrets)等，其中K/V引擎以及带版本的K/V引擎是最常用的。

注：Vault还支持开发者

[自定义secret engine]。

我们尝试使用kv子命令向vault中写入一个key/value，放到secret路径下(在dev模式下，secret路径下自动开启v2版本引擎)，key为hello，值为foo=world：

```
$vault kv put -mount=secret hello foo=world
Error making API request.
URL: GET http://127.0.0.1:8200/v1/sys/internal/ui/mounts/secret
Code: 403. Errors:
* permission denied
```


我们看到命令执行失败，提示没有权限。vault server要求每个访问请求都必须带上token，我们可以使用vault server启动时打印的root token，可以使用环境变量的方式将token注入：

```
export VAULT_TOKEN="hvs.9QOJsa7zlwHO8ieW15CXXoOp"
```


也可以执行下面命令并输入root token完成登录：

```
$vault login
Token (will be hidden):
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.
Key Value
--- -----
token hvs.9QOJsa7zlwHO8ieW15CXXoOp
token_accessor 170OHOscEZjfl8fSa8aVpNkZ
token_duration ∞
token_renewable false
token_policies ["root"]
identity_policies []
policies ["root"]
```


之后，root token就被放置在“~/.vault-token”中了：

```
$cat ~/.vault-token
hvs.9QOJsa7zlwHO8ieW15CXXoOp
```


注：我们通常不会使用root token，而是会

[利用vault token命令生成新token]作为vault cli访问vault server的token。

现在我们重新执行一下kv put命令：

```
$vault kv put -mount=secret hello foo=world
== Secret Path ==
secret/data/hello
======= Metadata =======
Key Value
--- -----
created_time 2023-11-06T03:01:25.968883Z
custom_metadata <nil>
deletion_time n/a
destroyed false
version 2
```


kv创建成功，路径secret/data/hello(注：vault会默认在mount的路径secret下创建data路径)。vault server在将value值存储在backend storage(这里是memory)前，会用Encryption Key对内容进行加密。如果你多执行几次这个命令，你会发现输出信息中的version的数值会递增，这个数值表示设置的值的版本。

我们可以用kv get获取刚才写入的kv值，vault会将数据从backend storage中读取出来并解密：

```
$vault kv get -mount=secret hello
== Secret Path ==
secret/data/hello
======= Metadata =======
Key Value
--- -----
created_time 2023-11-06T03:01:25.968883Z
custom_metadata <nil>
deletion_time n/a
destroyed false
version 2
=== Data ===
Key Value
--- -----
foo world
```


我们还可以通过delete删除刚刚建立的kv值(为后面的基本场景示例做铺垫)：

```
$vault kv delete secret/foo
Success! Data deleted (if it existed) at: secret/data/foo
$vault kv get secret/foo
No value found at secret/data/foo
```


到这里我们看到，一旦vault安装完毕后，基本使用场景还是蛮简单的，但也仅限于基本使用场景^_^。下面我们再来看看如何通过代码来实现这些基本功能场景。

### 3.5 使用client SDK与Vault交互

[Vault支持各种主流语言的client SDK](https://developer.hashicorp.com/vault/api-docs/libraries)，其中Vault官方维护了三个：Go、Ruby和C#，其他语言的SDK则是由社区维护。

我们用Go Client SDK来编写一个设置kv和获取kv值的小程序，如下面代码所示：

```
// secret-management-examples/basic/main.go
package main
import (
"context"
"fmt"
"github.com/hashicorp/vault/api"
)
func main() {
// 创建一个新的Vault客户端
client, err := api.NewClient(api.DefaultConfig())
if err != nil {
fmt.Println("无法创建Vault客户端:", err)
return
}
// 设置Vault服务器的地址
client.SetAddress("http://localhost:8200/")
// 设置Vault的访问令牌（如果需要认证）
client.SetToken("hvs.9QOJsa7zlwHO8ieW15CXXoOp")
// 设置要写入的机密信息
secretData := map[string]interface{}{
"foo": "bar",
}
kv2 := client.KVv2("secret") // mount "secret"
// 写入机密信息到Vault的secret/data/{key}路径下
key := "hello"
_, err = kv2.Put(context.Background(), key, secretData)
if err != nil {
fmt.Println("无法写入机密信息:", err)
return
}
// 读取Vault的secret/data/{key}路径下的机密信息
secret, err := kv2.Get(context.Background(), key)
if err != nil {
fmt.Println("无法读取机密信息:", err)
return
}
// 打印读取到的值
fmt.Println("读取到的值:", secret.Data)
}
```


我们看到：默认创建的api.Client操作的都是v1版本的数据，这里通过KVv2方法将其转换为可以操作v2版本数据的client，之后put和get就可以如预期正常工作了！

下面是其运行结果：

```
$go run main.go
读取到的值: map[foo:bar]
```


有了基础场景做铺垫，接下来我们就进入实例环节，看看应用是如何基于Vault应对一些常见的机密管理场景的。

## 4. 常见的机密管理场景

Vault支持对多种机密信息的管理，包括应用访问外部服务或资源所需的用户名/密码、API密钥或访问令牌(token)，应用程序的配置中的机密配置信息，比如数据库连接字符串、加密密钥等，以及私钥、证书等加密相关的机密信息等。这里我们就分别来看看应用与Vault集成并获取这些机密信息的场景，不过在这之前，我们首先需要先来了解一下应用本身与Vault是如何集成的。

### 4.1 应用通过Vault身份认证和授权的方法

在3.5小节的基本场景示例中，我们的client使用了[一个长期有效的token](https://developer.hashicorp.com/vault/docs/auth/token)通过了Vault的身份认证和授权环节，拥有了操作Vault数据的权限。

token auth方法也是dev模式下Vault server实例支持的唯一auth method，我们可以通过auth list命令查看vault server当前支持的auth方法集合：

```
$vault auth list
Path Type Accessor Description Version
---- ---- -------- ----------- -------
token/ token auth_token_6f9cc41c token based credentials n/a
```


不过，基于token来实现app与Vault的集成并非Vault官方推荐的在生产环境使用的[auth方式](https://developer.hashicorp.com/vault/docs/auth)，理由也很明显：这种方式涉及手动创建一个长期有效的令牌，这有悖于最佳实践，并存在安全风险。

除了Token auth method，Vault还支持[AppRole](https://developer.hashicorp.com/vault/docs/auth/approle)、[JWT/OIDC](https://developer.hashicorp.com/vault/docs/auth/jwt)、[TLS证书](https://developer.hashicorp.com/vault/docs/auth/cert)以及[User/Password](https://developer.hashicorp.com/vault/docs/auth/userpass)等[多种auth method](https://developer.hashicorp.com/vault/docs/auth)，这些auth method的共同之处在于通过身份认证后，Vault可自动创建**短期令牌**供客户端使用，无需定期手动生成新令牌，短期令牌可以减少令牌泄露的风险，因为短期令牌在一定时间后会自动失效，并需要重新进行身份认证。

简单起见，我这里就用User/Password method作为实例演示一下应用通过Vault的身份认证和授权。

我们先来开启(enable)基于User/Password的auth method：

```
$vault auth enable userpass
Success! Enabled userpass auth method at: userpass/
```


该命令默认将会启用auth/userpass路径，之后通过auth list查看，就能在list中看到新增的userpass auth method了：

```
$vault auth list
Path Type Accessor Description Version
---- ---- -------- ----------- -------
token/ token auth_token_6f9cc41c token based credentials n/a
userpass/ userpass auth_userpass_b5b6e974 n/a n/a
```


接下来，我们在vault服务实例中建立一个新的user：

```
$vault write auth/userpass/users/tonybai password=ilovegolang
Success! Data written to: auth/userpass/users/tonybai
$vault read auth/userpass/users/tonybai
Key Value
--- -----
token_bound_cidrs []
token_explicit_max_ttl 0s
token_max_ttl 0s
token_no_default_policy false
token_num_uses 0
token_period 0s
token_policies [default]
token_ttl 0s
token_type default
```


下面是示例代码：

```
// secret-management-examples/auth_user_password/main.go
package main
import (
"context"
"fmt"
"github.com/hashicorp/vault/api"
auth "github.com/hashicorp/vault/api/auth/userpass"
)
func main() {
user := "tonybai"
pass := "ilovegolang"
// 创建Vault API客户端
client, err := api.NewClient(api.DefaultConfig())
if err != nil {
fmt.Printf("无法创建Vault客户端: %v\n", err)
return
}
// 设置 Vault 地址
client.SetAddress("http://localhost:8200")
// client登录vault服务器获取临时访问令牌
userpassAuth, err := auth.NewUserpassAuth(user, &auth.Password{FromString: pass})
if err != nil {
fmt.Errorf("无法初始化userpass auth method: %w", err)
return
}
secret, err := client.Auth().Login(context.Background(), userpassAuth)
if err != nil {
fmt.Errorf("登录Vault失败: %w", err)
return
}
if secret == nil {
fmt.Printf("登录后没有secret信息返回: %v\n", err)
return
}
fmt.Printf("登录Vault成功\n")
token := secret.Auth.ClientToken
// 设置临时访问令牌
client.SetToken(token)
kv2 := client.KVv2("secret") // mount "secret"
// 读取Vault的secret/data/{key}路径下的机密信息
data, err := kv2.Get(context.Background(), "hello")
if err != nil {
fmt.Println("无法读取机密信息:", err)
return
}
// 打印读取到的值
fmt.Println("读取到的值:", data.Data)
}
```


如果你在Vault的GO SDK中没有找到对user/password auth method的直接支持，你也可以参考[user/password auth method的API文档](https://developer.hashicorp.com/vault/api-docs/auth/userpass)自行实现登录Vault并读取特定机密信息，代码如下(与上面代码功能是等价的)：

```
// secret-management-examples/auth_user_password_self_impl/main.go
func clientAuth(vaultAddr, user, pass string) (*api.Secret, error) {
payload := fmt.Sprintf(`{"password": "%s"}`, pass)
req, err := http.NewRequest("POST", vaultAddr+"/v1/auth/userpass/login/"+user, strings.NewReader(payload))
if err != nil {
return nil, err
}
resp, err := http.DefaultClient.Do(req)
if err != nil {
return nil, err
}
defer resp.Body.Close()
body, err := io.ReadAll(resp.Body)
if err != nil {
return nil, err
}
if resp.StatusCode != http.StatusOK {
return nil, errors.New(string(body))
}
return api.ParseSecret(bytes.NewReader(body))
}
func main() {
vaultAddr := "http://localhost:8200"
user := "tonybai"
pass := "ilovegolang"
// client登录vault服务器获取临时访问令牌
secret, err := clientAuth(vaultAddr, user, pass)
if err != nil {
fmt.Printf("登录Vault失败: %v\n", err)
return
}
fmt.Printf("登录Vault成功\n")
// 创建Vault API客户端
client, err := api.NewClient(api.DefaultConfig())
if err != nil {
fmt.Printf("无法创建Vault客户端: %v\n", err)
return
}
// 设置 Vault 地址
client.SetAddress("http://localhost:8200")
token := secret.Auth.ClientToken
// 设置临时访问令牌
client.SetToken(token)
kv2 := client.KVv2("secret") // mount "secret"
// 读取Vault的secret/data/{key}路径下的机密信息
data, err := kv2.Get(context.Background(), "hello")
if err != nil {
fmt.Println("无法读取机密信息:", err)
return
}
// 打印读取到的值
fmt.Println("读取到的值:", data.Data)
}
```


我们运行一下上述两个示例代码之一：

```
$go run main.go
登录Vault成功
无法读取机密信息: error encountered while reading secret at secret/data/hello: Error making API request.
URL: GET http://localhost:8200/v1/secret/data/hello
Code: 403. Errors:
* 1 error occurred:
* permission denied
```


通过错误信息来看，“tonybai”这个user没有权限读取secret/data/hello下的机密信息！那么怎么给这个用户加上secret/data/hello的读取权限呢？Vault通过policy来管理权限，如果某个user具有某个policy的绑定，那么该user就拥有该policy设定的权限，这有点像RBAC的思路，只是没有引入role的概念! 我们先来添加一个拥有secret/data/hello读权限的policy：

```
$vault policy write my-policy -<<EOF
# Allow "read" permission on "secret/data/*" secrets
path "secret/data/*" {
capabilities = ["read"]
}
EOF
Success! Uploaded policy: my-policy
```


接下来重写user的属性数据，将my-policy赋给”tonybai”这个user：

```
$vault write auth/userpass/users/tonybai password=ilovegolang token_policies=my-policy
Success! Data written to: auth/userpass/users/tonybai
$vault read auth/userpass/users/tonybai
Key Value
--- -----
token_bound_cidrs []
token_explicit_max_ttl 0s
token_max_ttl 0s
token_no_default_policy false
token_num_uses 0
token_period 0s
token_policies [my-policy]
token_ttl 0s
token_type default
```


完成上述设置后，我们再来运行一下基于user/password auth method的程序：

```
$go run main.go
登录Vault成功
读取到的值: map[foo:bar]
```


这次程序成功登录Vault并成功读取了secret/data/hello下面的机密数据。

这里我们除了设置了token_policies，其他属性都保持了默认值，这样我们拿到的临时token其实并不“临时”，我们可以一直使用。下面我们通过设置token_ttl来指定每个临时token的最大有效时间：

```
$vault write auth/userpass/users/tonybai password=ilovegolang token_policies=my-policy token_ttl=5s
Success! Data written to: auth/userpass/users/tonybai
$vault read auth/userpass/users/tonybai
Key Value
--- -----
token_bound_cidrs []
token_explicit_max_ttl 0s
token_max_ttl 0s
token_no_default_policy false
token_num_uses 0
token_period 0s
token_policies [my-policy]
token_ttl 5s
token_type default
```


我们改写一下程序，让程序每隔1秒用临时token获取一下机密信息并输出：

```
// secret-management-examples/auth_user_password_renewal/main.go (临时版本)
for {
// 每个一秒读取一次Vault的secret/data/{key}路径下的机密信息
data, err := kv2.Get(context.Background(), "hello")
if err != nil {
fmt.Println("无法读取机密信息:", err)
return
}
// 打印读取到的值
log.Println("读取到的值:", data.Data)
time.Sleep(time.Second)
}
```


我们运行这个程序将得到如下结果：

```
$go run main.go
登录Vault成功
2023/11/06 05:24:17 读取到的值: map[foo:bar]
2023/11/06 05:24:18 读取到的值: map[foo:bar]
2023/11/06 05:24:19 读取到的值: map[foo:bar]
2023/11/06 05:24:20 读取到的值: map[foo:bar]
2023/11/06 05:24:21 读取到的值: map[foo:bar]
无法读取机密信息: error encountered while reading secret at secret/data/hello: Error making API request.
URL: GET http://localhost:8200/v1/secret/data/hello
Code: 403. Errors:
* permission denied
```


我们看到如果token过期，而我们的程序又没有[对token进行续期(renewal)](https://developer.hashicorp.com/vault/docs/concepts/lease#lease-durations-and-renewal)，程序后续对Vault中机密数据的访问将以”permission denied”的失败而告终。下面我们就来为程序加上token续期，Vault SDK提供了LifetimeWatcher来辅助token续期工作，下面就是利用LifetimeWatcher进行token续期的示例：

```
// secret-management-examples/auth_user_password_renewal/main.go
package main
import (
"context"
"fmt"
"log"
"time"
"github.com/hashicorp/vault/api"
auth "github.com/hashicorp/vault/api/auth/userpass"
)
func main() {
user := "tonybai"
pass := "ilovegolang"
// 创建Vault API客户端
client, err := api.NewClient(api.DefaultConfig())
if err != nil {
fmt.Printf("无法创建Vault客户端: %v\n", err)
return
}
// 设置 Vault 地址
client.SetAddress("http://localhost:8200")
// client登录vault服务器获取临时访问令牌
userpassAuth, err := auth.NewUserpassAuth(user, &auth.Password{FromString: pass})
if err != nil {
fmt.Errorf("无法初始化userpass auth method: %w", err)
return
}
secret, err := client.Auth().Login(context.Background(), userpassAuth)
if err != nil {
fmt.Errorf("登录Vault失败: %w", err)
return
}
if secret == nil {
fmt.Printf("登录后没有secret信息返回: %v\n", err)
return
}
fmt.Printf("登录Vault成功\n")
token := secret.Auth.ClientToken
// 设置临时访问令牌
client.SetToken(token)
// 设置renewel watcher
watcher, err := client.NewLifetimeWatcher(&api.LifetimeWatcherInput{
Secret: secret,
})
go watcher.Start()
defer watcher.Stop()
kv2 := client.KVv2("secret") // mount "secret"
ticker := time.NewTicker(time.Second)
for {
select {
case err := <-watcher.DoneCh():
if err != nil {
log.Printf("Failed to renew token: %v. Re-attempting login.", err)
return
}
// This occurs once the token has reached max TTL.
log.Printf("Token can no longer be renewed. Re-attempting login.")
return
case renewal := <-watcher.RenewCh():
// Renewal is now over
log.Printf("Successfully renewed: %#v", renewal)
case <-ticker.C:
// 每个一秒读取一次Vault的secret/data/{key}路径下的机密信息
data, err := kv2.Get(context.Background(), "hello")
if err != nil {
fmt.Println("无法读取机密信息:", err)
continue
}
// 打印读取到的值
log.Println("读取到的值:", data.Data)
}
}
}
```


运行上述示例(此时token_ttl为5s)：

```
$go run main.go
登录Vault成功
2023/11/06 05:17:42 Successfully renewed: &api.RenewOutput{RenewedAt:time.Date(2023, time.November, 7, 14, 17, 42, 233750000, time.UTC), Secret:(*api.Secret)(0xc000114a80)}
2023/11/06 05:17:43 读取到的值: map[foo:bar]
2023/11/06 05:17:44 读取到的值: map[foo:bar]
2023/11/06 05:17:45 读取到的值: map[foo:bar]
2023/11/06 05:17:45 Successfully renewed: &api.RenewOutput{RenewedAt:time.Date(2023, time.November, 7, 14, 17, 45, 841374000, time.UTC), Secret:(*api.Secret)(0xc0002827e0)}
2023/11/06 05:17:46 读取到的值: map[foo:bar]
2023/11/06 05:17:47 读取到的值: map[foo:bar]
2023/11/06 05:17:48 读取到的值: map[foo:bar]
2023/11/06 05:17:49 读取到的值: map[foo:bar]
2023/11/06 05:17:49 Successfully renewed: &api.RenewOutput{RenewedAt:time.Date(2023, time.November, 7, 14, 17, 49, 443211000, time.UTC), Secret:(*api.Secret)(0xc0002831a0)}
2023/11/06 05:17:50 读取到的值: map[foo:bar]
2023/11/06 05:17:51 读取到的值: map[foo:bar]
2023/11/06 05:17:52 读取到的值: map[foo:bar]
2023/11/06 05:17:53 Successfully renewed: &api.RenewOutput{RenewedAt:time.Date(2023, time.November, 7, 14, 17, 53, 46880000, time.UTC), Secret:(*api.Secret)(0xc000115a40)}
2023/11/06 05:17:53 读取到的值: map[foo:bar]
2023/11/06 05:17:54 读取到的值: map[foo:bar]
... ...
```


我们看到，在token过期之前，LifetimeWatcher帮助Client完成了续期请求。LifetimeWatcher运行在一个单独的goroutine中，通过channel与main goroutine通信。Vault默认token_max_ttl的值为32天，即便你没有设置其值，当token续期到32天时，就无法再renew了，此时watcher.DoneCh会返回事件，这是让你重新login的信号，示例中只给出了注释，并未重新login，大家注意一下。出于安全考虑，可以将token_max_ttl设置为一个合理的值，使其起到应有的安全作用。

通过这个示例我们看到，只要通过Vault的身份认证和授权，我们就能安全地存储和使用机密信息了。那么如何保证应用在与Vault进行身份认证和授权时所使用的凭据的安全呢？比如上面程序里所需的user和password。这个感觉又回到“先有鸡还是先有蛋”的问题了！实际在生产环境，我们可以依赖IaaS层或公有云的安全措施来保证，比如通过环境变量在运行时注入user和password；再比如利用公有云提供的KMS(key management system)或HSM(Hardware Security Module)服务来保证user和password安全。

### 4.2 静态secret

将静态secret作为机密信息保存和管理，是Vault非常常见的应用。secret可以存在很长时间不变，或可能很少改变。Vault可以使用它的加密屏障(barrier)存储这些secret，应用程序运行时可以向Vault请求读取这些secret来使用。

Vault的versioned secrets engine支持你以安全的方式存储和管理secret，同时还提供secret的版本控制能力。你可以使用不同版本的secret进行应用程序升级或回滚，也可以在需要时轻松地恢复旧版本secret。引擎还可以记录secret每个版本的修改人和修改时间。

关于静态secret的管理和使用，可以参见3.5中的基本场景，这里就不赘述了。

### 4.3 动态secret

有静态、长有效期的静态secret，就会有对应的动态secret。和静态secret相比，动态secret安全性高，每个动态secret的有效期都较短，并且一旦泄露可以马上撤销，同时动态secret也便于轮换，定期自动过期无需中断业务。

Vault提供了对多种针对不同系统的动态secret管理能力，包括数据库访问凭据、Active Directory账号, SSH keys和PKI certificates ，Vault针对不同系统提供了不同的secret engine。

Vault官方举了一个有关[使用Database Secrets Engine实现数据库动态secret](https://developer.hashicorp.com/vault/tutorials/db-credentials/database-secrets)的示例，

鉴于篇幅，这里也不细说了。

### 4.4 其他场景

根据[Vault官方文档对Vault应用场景的描述](https://developer.hashicorp.com/vault/docs/use-cases)，除了静态和动态secret类机密信息，Vault可以处理以下类型的机密信息：

- 数据加密类(Data encryption)机密信息

Vault支持将数据加密服务外包给Vault，应用只需关注数据的加密与解密，Vault负责核心密钥和加密管理。Vault还支持对数据进行传输加密与存储加密。

- 身份识别类(Identity-Based access)机密信息

Vault支持从不同身份验证系统整合用户身份，实现统一的ACL系统，管理对系统和应用的访问。

- 加密密钥类(Key management)机密信息

Vault支持对云提供商密钥的生命周期管理，例如管理AWS KMS或GCP云密钥。

鉴于篇幅和实验环境有限，这里就针对每种情况做详细示例说明了，大家可以根据自己的需求，针对具体的某个场景做专题性的研究。

## 5. 小结

本文首先介绍了机密管理的概念，阐述了在现代Web应用开发中，为何需要重视机密管理。

接着，文中概述了专用于实现机密管理的机密管理系统的发展历程，以及从功能上逐步演化出的云原生机密管理系统的特征。

文章以业内知名的开源机密管理系统HashiCorp Vault为例，全面系统地介绍了它的架构设计、安全模型、使用方法，并详细阐释了应用程序如何通过与Vault API/SDK的集成，实现对各类机密信息的安全存储、动态生成、访问控制、审计等功能。

最后，文章用代码实例详细演示了基于Vault的几个典型机密管理场景，如不同类型机密信息的读写操作，以及不同认证方式的集成等。

这是个”每个人都应该重视安全的时代”，安全需要每个环节的参与，一处薄弱，就会导致“处处薄弱”。我相信本文的内容能有助于让大家对机密管理的概念、重要性及具体实现方法有更深入的理解。

本文涉及的代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/secret-management-examples)下载。

注：Vault项目还提供了Vault Agent和Vault Proxy，旨在为应用提供更可扩展、更简单的方式来集成Vault，消除应用程序采用Vault的初期障碍。Vault Agent可以获取secrets并将它们提供给应用程序，Vault Proxy可以在Vault和应用程序之间充当代理，可选地简化认证过程并缓存请求。有兴趣的童鞋可以参考

[Vault Agent和Proxy的官方文档]。

## 6. 参考资料

[Comparative Analysis of Cryptographic Key Management Systems](https://arxiv.org/abs/2109.09905)– https://arxiv.org/abs/2109.09905[What are the Practices for Secret Management in Software Artifacts?](https://arxiv.org/abs/2208.11280)– https://arxiv.org/abs/2208.11280[Shamir’s secret sharing](https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing)– https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing[HashiCorp Vault](https://www.hashicorp.com/blog/vault-announcement)– https://www.hashicorp.com/blog/vault-announcement[Vault Architecture](https://developer.hashicorp.com/vault/docs/internals/architecture)– https://developer.hashicorp.com/vault/docs/internals/architecture[External Secrets](https://github.com/external-secrets/external-secrets)– https://github.com/external-secrets/external-secrets[5 best practices for secrets management](https://www.hashicorp.com/resources/5-best-practices-for-secrets-management)– https://www.hashicorp.com/resources/5-best-practices-for-secrets-management[Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)– https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html[Secret Management](https://www.imperva.com/learn/data-security/secret-management/)– https://www.imperva.com/learn/data-security/secret-management/[Best practices for secrets management in Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/secrets/secrets-best-practices)– https://learn.microsoft.com/en-us/azure/key-vault/secrets/secrets-best-practices[Glossary: Secrets Management](https://www.beyondtrust.com/resources/glossary/secrets-management)– https://www.beyondtrust.com/resources/glossary/secrets-management

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