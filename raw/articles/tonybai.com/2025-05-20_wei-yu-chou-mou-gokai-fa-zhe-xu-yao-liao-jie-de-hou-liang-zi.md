---
title: 未雨绸缪：Go开发者需要了解的后量子密码学与实现现状
url: https://tonybai.com/2025/05/20/post-quantum-cryptography-in-go/
published: '2025-05-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 未雨绸缪：Go开发者需要了解的后量子密码学与实现现状

![](../../assets/59c2c50caa183162.png)


[本文永久链接](https://tonybai.com/2025/05/20/post-quantum-cryptography-in-go) – https://tonybai.com/2025/05/20/post-quantum-cryptography-in-go

大家好，我是 Tony Bai。

在我们享受数字时代便利的同时，信息安全始终是悬在我们头顶的达摩克利斯之剑。而这把剑，正面临着来自未来的一个巨大挑战——**量子计算机**。一旦实用化的大规模量子计算机问世，我们当前广泛依赖的许多经典密码体系（如 RSA、椭圆曲线密码 ECC）可能在瞬间土崩瓦解。

这不是科幻电影，而是密码学界和全球科技巨头都在严肃对待的现实威胁。正因如此，“后量子密码学” (Post-Quantum Cryptography, 以下简称PQC) 应运而生，旨在研发能够抵御量子计算机攻击的新一代密码算法。

作为 Go 开发者，我们或许觉得量子计算机还很遥远，但“现在记录数据，未来量子破解”的风险已然存在。更重要的是，Go 语言作为一门以简洁、高效和安全著称的现代编程语言，其核心团队早已在为这个“后量子时代”积极布局。**随着 Go 1.24 的发布，这一布局取得了实质性的进展：备受期待的 crypto/mlkem 包正式加入标准库！**

那么，PQC 究竟是什么？crypto/mlkem 包为我们带来了什么？Go 语言在 PQC 的浪潮中又将扮演怎样的角色？今天，就让我们一起“未雨绸缪”，深入了解 PQC 及其在 Go 中的最新进展。

![](../../assets/ab2d7a5176ba4b48.png)


## 量子风暴将至：为何我们需要 PQC？

想象一下，你用 RSA 加密了公司的核心商业机密，或者用 ECDSA 签名了重要的合同。这些操作的安全性，都依赖于经典计算机难以在有效时间内解决某些数学难题（如大数分解、离散对数）。

然而，量子计算机一旦足够强大，[Shor 算法](https://tonybai.com/2024/12/11/simulate-quantum-computing-in-go)就能在多项式时间内攻破这些难题。这意味着：

**加密通讯不再私密：**HTTPS、VPN 等都可能被破解。**数字签名不再可信：**软件更新、代码签名、身份认证都可能被伪造。**历史数据面临风险：**黑客现在就可以截获并存储加密数据，等待未来用量子计算机解密。对于需要长期保密的医疗记录、金融数据、国家机密等，这无疑是巨大威胁。

这就是我们迫切需要 PQC 的原因：**寻找并标准化那些即使是量子计算机也难以破解的新密码算法。**

## PQC 的曙光：NIST 标准化与主流算法

幸运的是，我们并非束手无策。在应对后量子密码学（PQC）的挑战时，美国国家标准与技术研究院（NIST）自2016年启动了PQ算法的标准化进程，旨在筛选和确立新一代的密码算法。经过多轮评审，几种优胜算法逐渐浮出水面，为未来的安全通信提供了希望。

首先，在密钥封装/交换机制（KEM – Key Encapsulation Mechanism)方面，基于格密码学（Lattice-based cryptography）的ML-KEM被选为主要的KEM标准（FIPS 203）。这一算法的优势在于，某些实现的性能甚至超过了我们熟知的X25519密钥交换算法，为其广泛应用奠定了基础。

简单来说，KEM的工作原理可以类比于使用一个特殊的“量子安全信封”——公钥，将对称密钥（例如AES密钥）封装后发送给对方。接收方使用对应的“量子安全钥匙”——私钥，打开信封取出密钥，随后双方便可借助这个对称密钥进行安全的通信。

在数字签名方面，ML-DSA基于Dilithium算法，同样属于格密码学的范畴。该算法被选为主要的数字签名标准（FIPS 204），用于验证信息的来源及完整性。这为数字通信的安全性提供了重要保障。

通过这些新兴的密码算法，NIST为抵御未来的量子攻击奠定了坚实的基础，展现了在后量子时代中应对安全挑战的希望。

**PQC 算法的挑战：更大的“块头”**

虽然 PQC 算法带来了量子抵抗性，但也普遍面临一个挑战：**密钥和签名的尺寸通常比经典算法大得多。** 这可能会对网络带宽、存储空间（尤其是 X.509 证书）以及资源受限设备带来一定压力。

**现有算法与 PQC 替换畅想 (简表):**

![](../../assets/2016a06270eaee6c.png)


注意：上表为简化对应，实际替换过程会更复杂。


## Go语言与PQC：Go 1.24 迎来 crypto/mlkem

Go 语言以其强大的 crypto 标准库和对安全性的重视而闻名。面对 PQC 的浪潮，Go 核心团队自然不会缺席。他们的策略是**谨慎、务实且前瞻**。

### Go 密码学库的坚实基础

在讨论 PQC 之前，值得一提的是 Go 现有密码学库的优秀设计：

**简洁易用：**尽量减少复杂性，提供安全的默认值，降低开发者误用风险。**持续现代化：**如对 RSA 后端的优化、新增 crypto/ecdh 包简化密钥交换、通过 godebug 机制平滑引入安全改进等。**golang.org/x/crypto：**作为标准库的扩展和试验田，引入 ChaCha20、Argon2 等高级算法。

在 crypto/mlkem 正式发布之前，Go 团队已在早期版本（如 Go 1.23）中进行了内部实现和集成工作。这些工作为标准库的最终引入奠定了基础，尤其是在 crypto/tls 包中探索对后量子密钥交换的支持。

### Go 1.24：crypto/mlkem 包正式发布！

**激动人心的时刻终于到来！Go 1.24 版本正式将 crypto/mlkem 包引入标准库。** 这一里程碑事件由 Go 核心开发者 FiloSottile（Filippo Valsorda）在 [Go Issue #70122](https://github.com/golang/go/issues/70122) 中提议并推动实现。

crypto/mlkem 包实现了 FIPS 203 标准中定义的 ML-KEM 算法，目前支持以下两个参数集：

**ML-KEM-768:**这是在大多数场景中推荐使用的参数集，提供了足够的后量子安全性。**ML-KEM-1024:**主要用于满足 CNSA 2.0 等特定规范的要求。

Go 团队暂时未包含 ML-KEM-512，因为它在实际部署中较为罕见。这一选择与 BoringSSL 等其他主流密码库的实现保持一致。

下面是crypto/mlkem 包 API的一些设计考量：

**类型安全：**为 ML-KEM-768 和 ML-KEM-1024 提供了独立的类型（如 mlkem.DecapsulationKey768 和 mlkem.EncapsulationKey768），避免了因参数集不同导致数据结构大小不匹配的问题。虽然数字后缀在 godoc 中的排序可能不理想，但这是为了类型清晰和性能考虑的权衡。**种子作为解封装密钥：**解封装密钥（私钥）支持以 64 字节的种子（”d || z” 形式）进行创建和表示。这种格式与 IETF 的方向一致，有助于标准化和互操作性。**简洁的核心操作：**API 围绕密钥生成 (GenerateKey)、密钥解析 (NewDecapsulationKey/NewEncapsulationKey)、密钥字节化 (Bytes)、封装 (Encapsulate) 和解封装 (Decapsulate) 这几个核心 KEM 操作展开。

### crypto/mlkem 使用示例

下面是一个演示如何使用 crypto/mlkem 包进行密钥封装和解封装的基本流程：

```
package main
import (
"bytes"
"crypto/mlkem"
"fmt"
"log"
)
func main() {
// === 场景：Alice 希望与 Bob 安全地共享一个密钥 ===
// --- Alice 的操作 ---
// 1. Alice 生成一个 ML-KEM-768 私钥 (DecapsulationKey)。
// GenerateKey768 返回 (*DecapsulationKey768, error)。
privateKeyAlice, err := mlkem.GenerateKey768()
if err != nil {
log.Fatalf("Alice: Failed to generate ML-KEM-768 decapsulation key: %v", err)
}
// 2. 从私钥获取对应的公钥 (EncapsulationKey)。
publicKeyAlice := privateKeyAlice.EncapsulationKey()
// 3. Alice 将她的公钥序列化为字节串，以便发送给 Bob。
publicKeyAliceBytes := publicKeyAlice.Bytes()
fmt.Printf("Alice's Public Key (ML-KEM-768, %d bytes): %x...\n", len(publicKeyAliceBytes), publicKeyAliceBytes[:16])
// --- Bob 的操作 ---
// Bob 接收到 Alice 的公钥字节串 publicKeyAliceBytes
// 4. Bob 根据接收到的字节串创建一个公钥实例。
// NewEncapsulationKey768 返回 (*EncapsulationKey768, error)。
publicKeyReceivedByBob, err := mlkem.NewEncapsulationKey768(publicKeyAliceBytes)
if err != nil {
log.Fatalf("Bob: Failed to parse Alice's public key: %v", err)
}
// 5. Bob 使用 Alice 的公钥来封装一个新的共享密钥。
// Encapsulate 返回 (sharedKey []byte, ciphertext []byte)，不返回 error。
sharedKeyForBob, ciphertextForAlice := publicKeyReceivedByBob.Encapsulate()
fmt.Printf("Bob: Generated Shared Key (ML-KEM-768, %d bytes): %x\n", len(sharedKeyForBob), sharedKeyForBob)
fmt.Printf("Bob: Generated Ciphertext for Alice (%d bytes): %x...\n", len(ciphertextForAlice), ciphertextForAlice[:16])
// --- Alice 的操作 ---
// Alice 接收到 Bob 发送过来的密文 ciphertextForAlice
// 6. Alice 使用她的私钥和收到的密文来解封装，得到共享密钥。
// Decapsulate 返回 (sharedKey []byte, error)。
sharedKeyForAlice, err := privateKeyAlice.Decapsulate(ciphertextForAlice)
if err != nil {
// 如果密文无效或已被篡改，Decapsulate 会返回错误。
log.Fatalf("Alice: Failed to decapsulate shared key: %v", err)
}
fmt.Printf("Alice: Decapsulated Shared Key (ML-KEM-768, %d bytes): %x\n", len(sharedKeyForAlice), sharedKeyForAlice)
// --- 验证 ---
// 7. 验证 Alice 和 Bob 得到的共享密钥是否一致。
if bytes.Equal(sharedKeyForAlice, sharedKeyForBob) {
fmt.Println("\nSuccess! Alice and Bob now share the same secret key using ML-KEM-768.")
} else {
// 这通常不应该发生，如果 Decapsulate 成功且数据未被篡改。
fmt.Println("\nError! Shared keys do NOT match. This is unexpected.")
}
// 简单演示 ML-KEM-1024 的密钥生成 (API 结构类似)
dk1024, err := mlkem.GenerateKey1024()
if err != nil {
log.Fatalf("Failed to generate ML-KEM-1024 decapsulation key: %v", err)
}
_ = dk1024.EncapsulationKey() // 获取公钥
fmt.Println("\nSuccessfully demonstrated ML-KEM-1024 key generation as well.")
// 打印一些常量信息
fmt.Printf("\nML-KEM Constants:\n")
fmt.Printf(" SharedKeySize: %d bytes\n", mlkem.SharedKeySize)
fmt.Printf(" SeedSize: %d bytes\n", mlkem.SeedSize)
fmt.Printf(" CiphertextSize768: %d bytes\n", mlkem.CiphertextSize768)
fmt.Printf(" EncapsulationKeySize768: %d bytes\n", mlkem.EncapsulationKeySize768)
fmt.Printf(" CiphertextSize1024: %d bytes\n", mlkem.CiphertextSize1024)
fmt.Printf(" EncapsulationKeySize1024: %d bytes\n", mlkem.EncapsulationKeySize1024)
}
```


使用Go 1.24+版本运行上述代码，可以得到类似如下输出结果：

```
Alice's Public Key (ML-KEM-768, 1184 bytes): f880089a159c9ba338a684c70e10bdee...
Bob: Generated Shared Key (ML-KEM-768, 32 bytes): bf7a9749d29a56c831edfda00aaa4d7034e82f744cacf9b8a377e79a20febb1f
Bob: Generated Ciphertext for Alice (1088 bytes): 9afe9f9d36a581a5d7e47b7913c65886...
Alice: Decapsulated Shared Key (ML-KEM-768, 32 bytes): bf7a9749d29a56c831edfda00aaa4d7034e82f744cacf9b8a377e79a20febb1f
Success! Alice and Bob now share the same secret key using ML-KEM-768.
Successfully demonstrated ML-KEM-1024 key generation as well.
ML-KEM Constants:
SharedKeySize: 32 bytes
SeedSize: 64 bytes
CiphertextSize768: 1088 bytes
EncapsulationKeySize768: 1184 bytes
CiphertextSize1024: 1568 bytes
EncapsulationKeySize1024: 1568 bytes
```


上述代码仅为了展示 crypto/mlkem 包的核心用法。实际应用中，公钥和密文的传输需要通过网络等信道。

crypto/mlkem 包的加入，使得 Go 开发者可以直接在应用层使用标准化的后量子密钥封装机制，为构建面向未来的安全应用提供了坚实的基础。

### crypto/tls 的 PQC 集成：Go 1.24 默认启用，让 HTTPS 更“抗量子”

对于大多数 Go 开发者而言，直接使用底层的 crypto/mlkem 包可能不是最常见的场景。更令人振奋的是，Go 团队已将后量子密码能力无缝集成到了我们日常使用的 crypto/tls 包中！

**根据 Go 1.24 的发布说明，crypto/tls 包现在默认支持并启用了新的后量子混合密钥交换机制 X25519MLKEM768。**

这意味着什么呢？

**默认的后量子保护：**当你的 Go 1.24+ 应用程序使用 crypto/tls（例如，作为 HTTPS 服务器或客户端），并且 tls.Config 中的 CurvePreferences 字段未被显式设置（保持为 nil）时，TLS 握手将**自动尝试使用 X25519MLKEM768 进行密钥交换**。**混合机制的优势：**X25519MLKEM768 是一种**混合 (hybrid)**密钥交换方案。它巧妙地将经过广泛验证的经典椭圆曲线算法 X25519 与后量子安全的 ML-KEM-768 结合起来。这样做的好处是：**经典安全：**即使 ML-KEM-768 未来被发现存在未知的弱点（尽管可能性很小），X25519 依然能提供经典的安全性。**量子抵抗：**面对量子计算机的威胁，ML-KEM-768 部分提供了后量子保护。


这种“两全其美”的设计是当前 PQC 过渡阶段推荐的主流方案。

**开发者体验的极致简化：**大部分情况下，开发者**无需修改现有代码**即可获得这种增强的安全性。Go 语言的哲学再次体现——将复杂性封装起来，提供安全且易用的默认行为。

**如何控制这一行为？**

虽然默认启用是推荐的，但 Go 团队也考虑到了现实世界中的兼容性问题。在某些情况下，一些老旧或有缺陷的 TLS 服务器可能无法正确处理 X25519MLKEM768 握手过程中可能产生的较大记录 (TLS record)，导致握手超时失败。

因此，Go 1.24 提供了禁用此默认行为的选项：

**通过 tls.Config.CurvePreferences：**

你可以显式设置 CurvePreferences 字段，只包含你希望支持的经典密钥交换机制，从而排除 X25519MLKEM768。

```
// 示例：显式设置，不包含 X25519MLKEM768
config := &tls.Config{
Certificates: []tls.Certificate{cert},
CurvePreferences: []tls.CurveID{tls.X25519, tls.CurveP256}, // 明确指定经典曲线
}
```


**通过 GODEBUG 环境变量：**

可以在运行时通过设置环境变量 GODEBUG=tlsmlkem=0 来全局禁用 X25519MLKEM768 的默认启用。

**概念性代码示例（体现 Go 1.24 默认行为）：**

```
package main
import (
"crypto/tls"
"log"
"net/http"
)
func helloServer(w http.ResponseWriter, req *http.Request) {
w.Header().Set("Content-Type", "text/plain")
w.Write([]byte("This is an example server with Go 1.24 TLS.\n"))
// Go 1.24 crypto/tls 默认会尝试 X25519MLKEM768 密钥交换
// 如果客户端也支持，连接将具备后量子安全性！
}
func main() {
// 加载证书和私钥 (此处省略具体加载过程)
cert, err := tls.LoadX509KeyPair("server.crt", "server.key")
if err != nil {
log.Fatalf("server: loadkeys: %s", err)
}
// 服务器配置
// 在 Go 1.24+ 中，如果 CurvePreferences 为 nil (默认)，
// X25519MLKEM768 将被默认启用。
config := &tls.Config{
Certificates: []tls.Certificate{cert},
// CurvePreferences: nil, // 默认即启用 X25519MLKEM768
}
http.HandleFunc("/hello", helloServer)
server := &http.Server{
Addr: ":8443",
TLSConfig: config,
}
log.Println("Starting server on https://localhost:8443/hello")
log.Fatal(server.ListenAndServeTLS("", "")) // 使用空字符串让其加载 config 中的证书
}
// 客户端示例 (概念)
// clientConfig := &tls.Config{
// InsecureSkipVerify: true, // 仅用于测试，生产环境不要用
// CurvePreferences: nil, // 客户端也会默认尝试 X25519MLKEM768
// }
// conn, err := tls.Dial("tcp", "localhost:8443", clientConfig)
// if err != nil {
// log.Fatalf("client: dial: %s", err)
// }
// defer conn.Close()
// log.Println("client: connected to: ", conn.RemoteAddr())
```


**重要提示：** Go 1.24 还**移除了对实验性 X25519Kyber768Draft00 密钥交换的支持**，完全转向了标准化的 X25519MLKEM768。

crypto/tls 中这一默认的后量子安全增强，是 Go 语言在 PQC 时代向前迈出的坚实一步，极大地降低了开发者应用 PQC 的门槛。

开发者可能只需要更新 Go 版本，或者做少量配置，就能让应用具备初步的后量子防护能力，而无需深入了解 ML-KEM 的复杂细节。这正是 Go 追求简洁易用哲学的体现。

对于 SSH 协议，Go 团队计划密切关注 OpenSSH 的发展。一旦 OpenSSH 支持 NIST 选定的 ML-KEM 标准（目前 OpenSSH 使用的是 NTRU，非 NIST 主选），Go 团队也将在 crypto/ssh 包中添加相应支持，以确保互操作性。

## Go 与 PQC：机遇、挑战及开发者行动

Go 语言正积极拥抱后量子密码学 (PQC) 时代，Go 1.24 将 crypto/mlkem 纳入标准库并通过 crypto/tls 默认启用 X25519MLKEM768 混合密钥交换，这为 Go 开发者带来了技术领先和安全增强的机遇，但也伴随着 API 演进、行业经验不足及资源消耗等挑战。Go 社区正通过提供清晰文档和推动实践来赋能开发者，共同塑造一个更安全的数字未来。

面对这一变革，Go 开发者应积极学习 crypto/mlkem 的 API 和 crypto/tls 的 PQC 集成机制，理解其默认行为及控制方式。对于需要长期数据保密性的项目，应审慎评估并开始应用这些新特性，同时关注 Go 在 PQC 领域的后续发展，并参与社区交流，为应用的未来安全做好规划。Go 1.24 已为我们迈向后量子安全提供了坚实的工具。

## 小结：为量子未来，Go 已在路上

后量子密码学不再是遥不可及的未来概念，而是关乎我们数字世界长期安全的关键一步。Go 语言凭借其在密码学领域的深厚积累和前瞻性布局，正稳步迈向这个新时代。

Go 1.24 中 crypto/mlkem 包的正式发布，是 Go 在 PQC 领域的一个重要里程碑。它为开发者提供了直接、标准化的工具来应对量子计算的潜在威胁。结合未来在 crypto/tls 和 crypto/ssh 等包中的 PQC 集成，Go 团队正努力为开发者提供安全、易用且高效的后量子密码解决方案。

这不仅是一场技术升级，更是 Go 社区共同承担的责任。通过学习、关注、参与和实践，我们可以与 Go 一道，为构建一个能抵御未来量子威胁的、更安全的数字世界贡献力量。让我们一起期待 Go 在后量子时代的精彩表现！

## 参考资料

[crypto/mlkem: new package #70122](https://github.com/golang/go/issues/70122)– https://github.com/golang/go/issues/70122[NIST Releases First 3 Finalized Post-Quantum Encryption Standards](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)– https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards[Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)– https://csrc.nist.gov/projects/post-quantum-cryptography[Post-quantum cryptography](https://en.wikipedia.org/wiki/Post-quantum_cryptography)– https://en.wikipedia.org/wiki/Post-quantum_cryptography[Towards Post-Quantum Cryptography in TLS](https://blog.cloudflare.com/towards-post-quantum-cryptography-in-tls/)– https://blog.cloudflare.com/towards-post-quantum-cryptography-in-tls/[KEMS AND POST-QUANTUM AGE](https://words.filippo.io/dispatches/post-quantum-age/)– https://words.filippo.io/dispatches/post-quantum-age/[POST-QUANTUM CRYPTOGRAPHY FOR THE GO ECOSYSTEM](https://words.filippo.io/dispatches/mlkem768/)– https://words.filippo.io/dispatches/mlkem768/[What’s new in Go’s cryptography libraries: Part 1](https://changelog.com/gotime/295?ref=tonybai.com)– https://changelog.com/gotime/295[What’s new in Go’s cryptography libraries: Part 2](https://changelog.com/gotime/298?ref=tonybai.com)– https://changelog.com/gotime/298[What’s new in Go’s cryptography libraries: Part 3](https://changelog.com/gotime/313?ref=tonybai.com)– https://changelog.com/gotime/313[Post Quantum Cryptography Web Server in Go 1.23](https://medium.com/cyberark-engineering/a-post-quantum-cryptography-web-server-in-go-1-23-9f7e98db7b39)– https://medium.com/cyberark-engineering/a-post-quantum-cryptography-web-server-in-go-1-23-9f7e98db7b39

**感谢阅读！**

如果这篇文章让你对后量子密码学和 Go 的未来有所了解，请帮忙**转发** ，让更多 Gopher 关注这一重要趋势！

**深入探讨，加入我们！**

对后量子密码学的技术细节、Go 的具体实现进展、或如何在你的应用中规划 PQC 过渡感兴趣？欢迎加入我的知识星球 **“Go & AI 精进营”**！

在那里，我们可以：

- 跟踪 PQC 在 Go 及其他主流语言中的最新动态。
- 讨论 PQC API 设计的最佳实践。
- 分享学习 PQC 和密码学的心得体会。

欢迎扫描下方二维码加入星球，共同探索安全技术的未来！

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

那么，贵站准备什么时候启动后量子密钥交换支持？在当下（2025.10.5），贵站可还是默认在用 TLSv1.2 + RSA 证书啊

我这里用的是wordpress，并且比较老的版本。基于let’s encrypt的certbot定期更换证书。

如果是我自己开发的博客系统，自然会尽快升级到tls 1.3+更安全密钥加持的证书了。

还有就是，没有太多空闲时间折腾了:(。