---
title: Go开发者的密码学导航：crypto库使用指南
url: https://tonybai.com/2024/10/19/go-crypto-package-design-deep-dive/
published: '2024-10-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go开发者的密码学导航：crypto库使用指南

![](../../assets/049729100687c5bb.png)


[本文永久链接](https://tonybai.com/2024/10/19/go-crypto-package-design-deep-dive) – https://tonybai.com/2024/10/19/go-crypto-package-design-deep-dive

Go号称“开箱即用”，这与其标准库的丰富功能和高质量是分不开的。而在Go标准库中，crypto库(包括crypto包、crypto目录下相关包以及golang.org/x/crypto下的补充包)又是Go社区最值得称道的Go库之一。

crypto库由Go核心团队维护，确保了最高级别的安全标准和及时的漏洞修复，为开发者提供了可靠的安全保障。crypto还涵盖了从基础的对称加密到复杂的非对称加密，以及各种哈希函数和数字签名算法等广泛的加解密算法支持，以满足Go开发者的各种需求为目的，而不是与其他密码学工具包竞争。此外，crypto库还经过精心优化，能够在不同硬件平台上尽可能地保证高效的执行性能。值得一提的是，crypto库还提供了统一的API设计，使得不同加密算法的使用方式保持一致，也降低了开发者的学习成本。

可以说[Go crypto库](https://pkg.go.dev/crypto)是**Go生态中密码学功能的核心**，它为Go开发者提供了一套全面、安全、**保持现代化**、**提供安全默认值**且**易于使用**的密码学工具，使得在Go应用程序中实现各种密码学功能需求时变得简单而可靠。

不过要理解并得心应手的使用crypto库中的相关密码学包仍然并非易事，这是因为密码学涉及数学、密码分析、计算机安全等多个学科，概念多，算法也十分复杂，而大多程序员对密码学的了解又多停留在使用层面，缺乏对其原理和底层机制的深入认知，甚至连每个包的用途都不甚了解。这导致很多开发者浏览了crypto相关包之后，甚至不知道该使用哪个包。

所以在这篇文章中，我想为Go开发者建立一张crypto库的“地图”，这张“地图”将帮助我们从宏观角度理解crypto库的结构，帮助大家快速精准选择正确的包。并且通过对crypto相关包设计的理解，轻松掌握crypto相关包的使用模式。

注：Go标准库crypto库的第一任负责人是

[Adam Langley(agl)]，他开创了Go crypto库，他在招募和培养了[Filippo Valsorda]后离开了Go项目，后者成为了Go crypto的负责人。Filippo在Go项目工作若干年后，把负责人交给了[Roland Shoemaker]，即现任Go团队安全组的负责人。当然Shoemaker也是Filippo招募到Go团队中的。

下面我们首先来看看Go crypto库的“整体架构”。

## 1. 标准库crypto与golang.org/x/crypto

Go的密码学功能(即我们统一称的crypto库)分为两个主要部分：**标准库的crypto相关包和扩展库golang.org/x/crypto**。这种分离设计有其特定的目的和优势：

Go标准库的crypto相关包，包含了最基础、最稳定和使用最广泛的密码学算法。这些算法实现经过Go团队的严格审查，保证了长期稳定性和向后兼容性。同时，这些包是随Go安装包分发的，使用时再无需引入额外的依赖。

而golang.org/x/crypto则号称是Go标准库crypto相关包的补充库，虽然它同样由Go团队维护，但由于不是标准库，它可以包含更多实验性或较新的密码学算法及实现，并可以更快速的迭代和更新。这样它也可以成为Go标准库中一些crypto相关包的“孵化器”，就像当年golang.org/x/net/context提升为[标准库context](https://tonybai.com/2022/11/08/understand-go-context-by-example)一样。

同时golang.org/x/crypto也是Go标准库依赖的为数极少的外部包之一。比如，下面是[Go 1.23.0](https://tonybai.com/2024/08/19/some-changes-in-go-1-23/)标准库go.mod文件的内容：

```
module std
go 1.23
require (
golang.org/x/crypto v0.23.1-0.20240603234054-0b431c7de36a
golang.org/x/net v0.25.1-0.20240603202750-6249541f2a6c
)
require (
golang.org/x/sys v0.22.0 // indirect
golang.org/x/text v0.16.0 // indirect
)
```


我们看到Go标准库依赖特定版本的golang.org/x/crypto模块。

与标准库不同的是，如果你要使用golang.org/x/crypto模块中的密码学包，**你就需要单独引入项目依赖**。此外，golang.org/x 下的包通常被视为实验性或扩展包，因此它们并不严格遵循[Go1兼容性承诺](https://go.dev/doc/go1compat)。换句话说，这些包在API稳定性上没有与标准库相同的保证，可能会有非向后兼容的更改。

综上，我们看到Go标准库crypto与golang.org/x/crypto的这种分离策略，允许Go团队在保持标准库稳定性的同时，也能够灵活地引入新的密码学算法和技术。

接下来，我们来看看crypto库的整体结构设计原则，这些原则对理解整个crypto库大有裨益。

## 2. 整体结构设计原则

Go的crypto库整体上的结构设计遵循了几个原则：

### 2.1 统一接口和类型抽象

首先是**统一接口和类型抽象**，这在最顶层的crypto包中就能充分体现。

crypto包定义了一个Hash类型和一个创建具体哈希实现的方法。这个设计允许统一管理不同的哈希算法，同时保持了良好的可扩展性：

```
// $GOROOT/src/crypto/crypto.go
type Hash uint
// New returns a new hash.Hash calculating the given hash function. New panics
// if the hash function is not linked into the binary.
func (h Hash) New() hash.Hash {
if h > 0 && h < maxHash {
f := hashes[h]
if f != nil {
return f()
}
}
panic("crypto: requested hash function #" + strconv.Itoa(int(h)) + " is unavailable")
}
// HashFunc simply returns the value of h so that [Hash] implements [SignerOpts].
func (h Hash) HashFunc() Hash {
return h
}
// RegisterHash registers a function that returns a new instance of the given
// hash function. This is intended to be called from the init function in
// packages that implement hash functions.
func RegisterHash(h Hash, f func() hash.Hash) {
if h >= maxHash {
panic("crypto: RegisterHash of unknown hash function")
}
hashes[h] = f
}
var hashes = make([]func() hash.Hash, maxHash)
```


Hash类型作为一个统一的标识符，用于表示不同的哈希算法。New方法则“像一个工厂方法”，用于创建具体的哈希实现。新的哈希算法可以很容易地添加到这个系统中，只需定义一个新的常量并提供相应的实现，并将实现通过RegisterHash注册到hashes中即可。下面是一个使用sha256算法的示例(仅做演示，并非惯例写法)：

```
package main
import (
"crypto"
_ "crypto/sha256" // register h256 to hashes
)
func main() {
ht := crypto.SHA256
h := ht.New()
h.Write([]byte("hello world"))
sum := h.Sum(nil)
println(sum)
}
```


注：也许是早期标准库的设计问题，hash接口目前没有放到crypto下面，而是在标准库顶层目录下。crypto库中的hash实现通过New方法返回真正的hash.Hash实现。


crypto包还定义了几个关键接口，这些接口被各个子包实现，从而实现了高度的可扩展性和互操作性，比如下面的Signer、SignerOpts、Decrypter接口：

```
// Signer is an interface for an opaque private key that can be used for
// signing operations. For example, an RSA key kept in a hardware module.
type Signer interface {
Public() PublicKey
Sign(rand io.Reader, digest []byte, opts SignerOpts) (signature []byte, err error)
}
// SignerOpts contains options for signing with a [Signer].
type SignerOpts interface {
HashFunc() Hash
}
// Decrypter is an interface for an opaque private key that can be used for
// asymmetric decryption operations. An example would be an RSA key
// kept in a hardware module.
type Decrypter interface {
Public() PublicKey
Decrypt(rand io.Reader, msg []byte, opts DecrypterOpts) (plaintext []byte, err error)
}
```


以Signer接口为例，这个Signer接口为不同的签名算法（如RSA、ECDSA、Ed25519等）提供了一个统一的抽象。下面是一个使用统一Signer接口但不同Signer实现的示例：

```
func signData(signer crypto.Signer, data []byte) ([]byte, error) {
hash := crypto.SHA256
h := hash.New()
h.Write(data)
digest := h.Sum(nil)
return signer.Sign(rand.Reader, digest, hash)
}
func main() {
rsaKey, _ := rsa.GenerateKey(rand.Reader, 2048)
signature, _ := signData(rsaKey, []byte("Hello, World!"))
println(signature)
ecdsaKey, _ := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
signature, _ = signData(ecdsaKey, []byte("Hello, World!"))
println(signature)
}
```


在这个例子中，我们看到了如何使用相同的signData函数来处理不同类型的签名算法，这体现了统一接口带来的灵活性和一致性。

在crypto目录下的各个子包中，上述原则也有很好的体现，比如cipher包就定义了Block、Stream等接口，然后aes、des等对称加密包也都提供了创建实现了这些接口的类型的函数，比如aes.NewCipher以及des.NewCipher等。

### 2.2 模块化

每个子包专注于特定的功能，这种模块化设计使得每个包都相对独立，便于维护和使用。以aes包和des包为例：

```
// crypto/aes/cipher.go
func NewCipher(key []byte) (cipher.Block, error) {
// AES specific implementation
}
// crypto/des/cipher.go
func NewCipher(key []byte) (cipher.Block, error) {
// DES specific implementation
}
```


这两个包都实现了相同的NewCipher函数，但内部实现完全不同，专注于各自的加密算法。

### 2.3 易用性与灵活性的平衡

Go crypto库中的很多包既提供了可以满足大多数常见用例的需求、易用性很好的高级API，同时也提供了更灵活的低级API，允许开发者在需要时进行更精细的控制或自定义实现。

让我们以SHA256哈希函数为例来说明这一点：

```
// 高级API
func highLevelAPI(data []byte) [32]byte {
return sha256.Sum256(data)
}
// 低级API
func lowLevelAPI(data []byte) [32]byte {
h := sha256.New()
h.Write(data)
return *(*[32]byte)(h.Sum(nil))
}
func main() {
fmt.Println(lowLevelAPI([]byte("hello world")))
fmt.Println(highLevelAPI([]byte("hello world")))
}
```


在这个例子中，sha256.Sum256是高级API，而lowLevelAPI中使用的那套逻辑则是对低级API的组合以实现Sum256功能。

### 2.4 可扩展性

基于“统一接口和类型抽象”原则设计的crypto库可以让用户轻松地集成自己的实现或第三方库，这种可扩展性便于我们添加新的算法或功能，而不影响现有结构。 比如，我们可以像这下面这样实现自定义的cipher.Block：

```
type MyCustomCipher struct {
// ...
}
func (c *MyCustomCipher) BlockSize() int {
// ...
}
func (c *MyCustomCipher) Encrypt(dst, src []byte) {
// ...
}
func (c *MyCustomCipher) Decrypt(dst, src []byte) {
// ...
}
```


之后，这个自定义的cipher.Block实现便可以直接用在标准库提供的分组密码模式中。

作为crypto库的扩展和实验库，golang.org/x/crypto也遵循了与标准库crypto相关包一致的设计原则，这里就不举例说明了。

有了上述对crypto库的整体设计原则的认知后，我们再来看一下Go标准库crypto目录下的子包结构，了解了这个结果，**你就会像拥有了crypto库的“导航”**，可以顺利方便地找到你想要的密码学包了。

## 3. 子包结构概览

众所周知，Go标准库crypto目录下不仅有crypto包，还有众多种类的密码学包，下面这张示意图对这些包进行了简单分类：

![](../../assets/f27d3330e620b98c.png)


下面我会按照图中的类别对各个包做简单介绍，包括功能、用途、简单的示例以及是否推荐使用。密码学一直在发展，很多算法因为不再“牢不可破”而逐渐不再被推荐使用。但Go为了保证Go1兼容性，这些包依赖留在了Go标准库中。

我们自上而下，先从哈希函数开始。

### 3.1 哈希函数

#### 3.1.1 md5

- 功能：实现MD5哈希算法
- 用途：生成数据的128位哈希值
- 示例：

```
import "crypto/md5"
hash := md5.Sum([]byte("hello world"))
```


- 使用建议：不推荐用于安全相关用途，因为MD5已被证明不够安全。

#### 3.1.2 sha1

- 功能：实现SHA-1哈希算法
- 用途：生成数据的160位哈希值
- 示例：

```
import "crypto/sha1"
hash := sha1.Sum([]byte("hello world"))
```


- 使用建议：不推荐用于安全相关用途，因为SHA-1已被证明存在碰撞风险。

#### 3.1.3 sha256

- 功能：实现SHA-256哈希算法
- 用途：生成数据的256位哈希值
- 示例：

```
import "crypto/sha256"
hash := sha256.Sum256([]byte("hello world"))
```


- 使用建议：推荐使用，安全性高。

#### 3.1.4 sha512

- 功能：实现SHA-512哈希算法
- 用途：生成数据的512位哈希值
- 示例：

```
import "crypto/sha512"
hash := sha512.Sum512([]byte("hello world"))
```


- 使用建议：推荐使用，安全性很高。

### 3.2 加密和解密

#### 3.2.1 aes

- 功能：实现AES(Advanced Encryption Standard)对称加密算法
- 用途：数据对称加密和解密
- 示例：

```
import "crypto/aes"
key := []byte("example key 1234") // 16字节的key
block, _ := aes.NewCipher(key)
```


- 使用建议：推荐使用，是目前最广泛使用的对称加密算法。

#### 3.2.2 des

- 功能：实现DES(Data Encryption Standard)和Triple DES加密算法
- 用途：数据对称加密和解密
- 示例：

```
import "crypto/des"
key := []byte("example!") // 8字节的key
block, _ := des.NewCipher(key)
```


- 使用建议：不推荐使用DES，密钥长度不足(DES使用56位密钥，实际上是64位，但其中8位是奇偶校验位，不用于加密)，容易被暴力破解。推荐使用AES；Triple DES在某些遗留系统中仍在使用。

#### 3.2.3 rc4

- 功能：实现RC4(Rivest Cipher 4)流加密算法
- 用途：流数据的加密和解密
- 示例：

```
import "crypto/rc4"
key := []byte("secret key")
cipher, _ := rc4.NewCipher(key)
```


- 使用建议：不推荐使用，因为RC4已被证明存在安全漏洞。由于这些已知的安全问题，RC4已经被许多现代加密协议和应用所弃用。例如，TLS（Transport Layer Security）协议已经移除了对RC4的支持。

#### 3.2.4 cipher

- 功能：定义了块加密的通用接口
- 用途：为其他加密算法提供通用的加密和解密方法
- 示例：

```
import "crypto/cipher"
// 使用AES-GCM模式
block, _ := aes.NewCipher(key)
aesgcm, _ := cipher.NewGCM(block)
```


- 使用建议：推荐使用，特别是GCM等认证加密模式。

### 3.3 签名和验证

#### 3.3.1 dsa

- 功能：实现数字签名算法（DSA, Digital Signature Algorithm）
- 用途：生成和验证数字签名
- 示例：

```
import "crypto/dsa"
var privateKey dsa.PrivateKey
dsa.GenerateKey(&privateKey, rand.Reader)
```


- 使用建议：目前的趋势是DSA在许多应用中不再被推荐使用。DSA的安全性高度依赖于密钥长度。随着计算能力的提升，较短的DSA密钥长度（例如1024位）已经不再被认为是安全的。NIST建议使用更长的密钥长度（例如2048位或更长），但这会增加计算复杂性和资源消耗。ECDSA使用椭圆曲线密码学，可以在更短的密钥长度下提供相同级别的安全性。

#### 3.3.2 ecdsa

- 功能：实现椭圆曲线数字签名算法（ECDSA, Elliptic Curve Digital Signature Algorithm）
- 用途：生成和验证数字签名
- 示例：

```
import "crypto/ecdsa"
privateKey, _ := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
```


- 使用建议：强烈推荐使用，安全性高且效率好。

#### 3.3.3 ed25519

- 功能：实现Ed25519签名算法(Edwards-curve Digital Signature Algorithm with Curve25519)
- 用途：生成和验证数字签名
- 示例：

```
import "crypto/ed25519"
publicKey, privateKey, _ := ed25519.GenerateKey(rand.Reader)
```


- 使用建议：强烈推荐使用，安全性高且性能优秀。Ed25519提供了比传统ECDSA更高的安全性和性能，同时减少了某些类型的实现风险。因此，在选择数字签名算法时，Ed25519是一个非常有吸引力的选项，尤其是在需要高性能和强安全保障的应用中。

#### 3.3.4 rsa

- 功能：实现RSA(Rivest–Shamir–Adleman)加密和签名算法
- 用途：非对称加密、数字签名
- 示例：

```
import "crypto/rsa"
privateKey, _ := rsa.GenerateKey(rand.Reader, 2048)
```


- 使用建议：关于是否推荐使用RSA，这取决于具体的应用场景和安全需求。RSA在许多应用中仍然被广泛使用，尤其是在需要公钥加密和数字签名的场景。它是一个经过时间考验的算法，有着良好的安全记录。随着计算能力的提升，特别是量子计算的发展，RSA的安全性可能会受到威胁。此外，对于某些高性能或资源受限的环境，RSA可能不如其他算法（如椭圆曲线加密算法，如ECDSA或Ed25519）高效。尤其是签名，ECDSA或Ed25519可能是更好的选择。

### 3.4 密钥交换

#### 3.4.1 ecdh

- 功能：实现椭圆曲线Diffie-Hellman密钥交换(Elliptic Curve Diffie-Hellman)
- 用途：安全地在不安全的通道上协商共享密钥
- 示例：

```
import "crypto/ecdh"
curve := ecdh.P256()
privateKey, _ := curve.GenerateKey(rand.Reader)
```


- 使用建议：ECDH是一个强大且高效的密钥交换协议，在许多现代安全通信中被推荐使用，是现代密钥交换的首选方法。

### 3.5 安全随机数生成

#### 3.5.1 rand

- 功能：提供加密安全的随机数生成器
- 用途：生成密钥、随机填充等
- 示例：

```
import "crypto/rand"
randomBytes := make([]byte, 32)
rand.Read(randomBytes)
```


- 使用建议：强烈推荐使用，不要使用math/rand包(包括math/rand/v2)生成密码学相关的随机数(这些随机数是伪随机)。

### 3.6 证书和协议

#### 3.6.1 tls

- 功能：实现传输层安全（TLS, Transport Layer Security）协议
- 用途：安全网络通信
- 示例：

```
import "crypto/tls"
config := &tls.Config{MinVersion: tls.VersionTLS12}
```


- 使用建议：强烈推荐使用，是保护网络通信的标准方法。

#### 3.6.2 x509

- 功能：实现X.509公钥基础设施标准
- 用途：处理数字证书、证书签名请求（CSR）等
- 示例：

```
import "crypto/x509"
cert, _ := x509.ParseCertificate(certDER)
```


- 使用建议：推荐使用，是处理数字证书的标准方法。

### 3.7. 辅助功能

#### 3.7.1 elliptic

- 功能：实现几个标准的椭圆曲线
- 用途：为ECDSA和ECDH提供基础
- 示例：

```
import "crypto/elliptic"
curve := elliptic.P256()
```


- 使用建议：推荐使用，但通常不直接使用，而是通过ecdsa或ecdh包间接使用。

#### 3.7.2 hmac

- 功能：实现密钥散列消息认证码（HMAC, Hash-based Message Authentication Code）
- 用途：消息完整性验证
- 示例：

```
import "crypto/hmac"
h := hmac.New(sha256.New, []byte("secret key"))
h.Write([]byte("message"))
```


- 使用建议：推荐使用，是保护数据完整性和消息认证的标准方法。

#### 3.7.3 subtle

- 功能：提供一些用于实现加密功能的常用但容易出错的操作
- 用途：比较、常量时间操作等
- 示例：

```
import "crypto/subtle"
equal := subtle.ConstantTimeCompare([]byte("a"), []byte("b"))
```


- 使用建议：推荐在需要时使用，有助于防止时序攻击。

结合上面两节，我们看到crypto库的内部依赖结构设计得非常巧妙，以最小化耦合。大多数子包依赖于crypto基础包中定义的接口和类型。crypto/subtle包提供了一些底层的辅助函数，被多个其他包使用。每个加密算法包（如crypto/aes，crypto/rsa）通常是独立的，减少了包间的直接依赖。一些高级功能包（如crypto/tls）会依赖多个基础算法包。大多数需要随机性的包都依赖crypto/rand作为安全随机源。

此外，crypto库与其他Go标准库可紧密集成，包括：

- 与io包集成：使用io.Reader和io.Writer接口，便于流式处理和与其他I/O操作集成。
- 与encoding相关包集成：比如与encoding/pem和encoding/asn1包配合，用于处理密钥和证书的编码。
- 与hash包集成：加密哈希函数实现了hash.Hash接口，保持一致性。
- 与net包集成：如crypto/tls包与net包紧密集成，提供安全的网络通信。

接下来，再来看看golang.org/x/crypto扩展库，我们同样借鉴上面的分类和介绍方法，看看crypto扩展库中都有哪些有价值的实用密码学包。

## 4 golang.org/x/crypto扩展库

我们还是从哈希函数开始介绍。

### 4.1 哈希函数

#### 4.1.1 blake2b和blake2s

- 功能：实现BLAKE2b和BLAKE2s哈希函数。BLAKE2是一种加密哈希函数，由Jean-Philippe Aumasson、Samuel Neves、Zooko Wilcox-O’Hearn和Christian Winnerlein设计，旨在替代MD5和SHA-1等旧的哈希函数。BLAKE2有两种主要变体：BLAKE2b和BLAKE2s。
- 用途：生成高速、安全的哈希值。
- 示例：

```
import "golang.org/x/crypto/blake2b"
hash := blake2b.Sum256([]byte("hello world"))
```


- 使用建议：推荐使用，BLAKE2提供了比MD5和SHA-1更高的安全性，同时保持与SHA-2和SHA-3相当的强度，安全性高且速度快。

#### 4.1.2 md4

- 功能：实现MD4(Message Digest Algorithm 4)哈希算法
- 用途：生成128位哈希值
- 示例：

```
import "golang.org/x/crypto/md4"
h := md4.New()
h.Write([]byte("hello world"))
hash := h.Sum(nil)
```


- 使用建议：不推荐用于安全相关用途，MD4已被证明不安全，容易受到碰撞攻击和其他类型的攻击。已经被更安全的哈希函数所取代，如SHA-2和SHA-3等。

#### 4.1.3 ripemd160

- 功能：实现RIPEMD-160(RACE Integrity Primitives Evaluation Message Digest 160)哈希算法。
- 用途：生成160位哈希值
- 示例：

```
import "golang.org/x/crypto/ripemd160"
h := ripemd160.New()
h.Write([]byte("hello world"))
hash := h.Sum(nil)
```


- 使用建议：RIPEMD-160提供了比MD5和SHA-1更高的安全性，尽管它不像SHA-2和SHA-3那样被广泛研究和使用。但它仍然在某些特定场景（如比特币地址生成）中使用，但一般情况下推荐使用更现代的哈希函数(如SHA-256和SHA-512)。

#### 4.1.4 sha3

- 功能：实现SHA-3(Secure Hash Algorithm 3)哈希算法族。SHA-3是由美国国家标准与技术研究院（NIST）在2015年发布的一种加密哈希函数，作为SHA-2的后继者。SHA-3的设计基于Keccak算法，由Guido Bertoni、Joan Daemen、Michaël Peeters和Gilles Van Assche开发。
- 用途：生成不同长度的哈希值。SHA-3包括多种变体，如SHA3-224、SHA3-256、SHA3-384和SHA3-512，分别生成224位、256位、384位和512位的哈希值。
- 示例：

```
import "golang.org/x/crypto/sha3"
hash := sha3.Sum256([]byte("hello world"))
```


- 使用建议：强烈推荐使用，是最新的NIST标准哈希函数。

### 4.2 加密和解密

#### 4.2.1 blowfish

- 功能：实现Blowfish(设计者Bruce Schneier)加密算法
- 用途：数据的对称加密和解密
- 示例：

```
import "golang.org/x/crypto/blowfish"
cipher, _ := blowfish.NewCipher([]byte("key"))
```


- 使用建议：不推荐用于新系统，其密钥长度上限为448位，不如更现代的算法安全，建议使用AES。

#### 4.2.2 cast5

- 功能：实现CAST5（又名CAST-128）加密算法
- 用途：数据对称加密和解密
- 示例：

```
import "golang.org/x/crypto/cast5"
cipher, _ := cast5.NewCipher([]byte("16-byte key"))
```


- 使用建议：不推荐用于新系统，建议使用AES。

#### 4.2.3 chacha20

- 功能：实现ChaCha20流加密算法(ChaCha20 stream cipher)
- 用途：流数据的对称加密和解密
- 示例：

```
import "golang.org/x/crypto/chacha20"
cipher, _ := chacha20.NewUnauthenticatedCipher(key, nonce)
```


- 使用建议：推荐使用，特别是在移动设备上性能优于AES。它被广泛用于各种安全协议和应用中，包括TLS（Transport Layer Security）、SSH（Secure Shell）和QUIC（Quick UDP Internet Connections）等。

#### 4.2.4 salsa20

- 功能：实现Salsa20流加密算法(Salsa20 stream cipher)
- 用途：流数据的对称加密和解密
- 示例：

```
import "golang.org/x/crypto/salsa20"
salsa20.XORKeyStream(dst, src, nonce, key)
```


- 使用建议：推荐使用，但ChaCha20可能因其性能优势和更广泛的标准支持而成为更受欢迎的选择。

#### 4.2.4 tea

- 功能：实现TEA（Tiny Encryption Algorithm）加密算法
- 用途：轻量级数据加密
- 示例：

```
import "golang.org/x/crypto/tea"
cipher, _ := tea.NewCipher([]byte("16-byte key"))
```


- 使用建议：尽管TEA算法在过去被认为是安全的，但它已经出现了一些已知的安全漏洞，如密钥相关攻击和差分攻击。因此，TEA算法可能不适合需要高安全性的应用。不推荐将它用于新系统，建议使用AES。

#### 4.2.5 twofish

- 功能：实现Twofish(Twofish block cipher)加密算法
- 用途：数据对称加密和解密
- 示例：

```
import "golang.org/x/crypto/twofish"
cipher, _ := twofish.NewCipher([]byte("16, 24, or 32 byte key"))
```


- 使用建议：不推荐将它用于新系统，建议使用AES。

#### 4.2.6 xtea

- 功能：实现XTEA(eXtended Tiny Encryption Algorithm)加密算法
- 用途：轻量级对称数据加密
- 示例：

```
import "golang.org/x/crypto/xtea"
cipher, _ := xtea.NewCipher([]byte("16-byte key"))
```


- 使用建议：尽管XTEA修复了TEA的一些安全漏洞，但它仍然可能存在其他安全问题，特别是在面对现代计算能力和攻击技术时。因此，不推荐用于新系统，建议使用AES。

#### 4.2.7 xts

- 功能：实现XTS (XEX-based tweaked-codebook mode with ciphertext stealing) 模式
- 用途：是一种块加密的标准操作模式，主要用于全磁盘加密
- 示例：

```
import "golang.org/x/crypto/xts"
cipher, _ := xts.NewCipher(aes.NewCipher, []byte("32-byte key"))
```


- 使用建议：在全磁盘加密场景，即需要对存储设备进行加密的应用中推荐使用。

### 4.3 认证加密

#### 4.3.1 chacha20poly1305

- 功能：实现ChaCha20-Poly1305(ChaCha20流加密算法和Poly1305消息认证码) AEAD（认证加密与关联数据）。
- 用途：提供加密和认证的组合
- 示例：

```
import "golang.org/x/crypto/chacha20poly1305"
aead, _ := chacha20poly1305.New(key)
```


- 使用建议：ChaCha20-Poly1305是一个高效且安全的组合加密算法，在许多现代安全应用中被推荐使用。这里也强烈推荐使用，提供了高安全性和高性能。

### 4.4 密钥派生和密码哈希

#### 4.4.1 argon2

- 功能：实现Argon2(Argon2 memory-hard key derivation function)密码哈希算法
- 用途：安全地存储密码
- 示例：

```
import "golang.org/x/crypto/argon2"
hash := argon2.IDKey([]byte("password"), salt, 1, 64*1024, 4, 32)
```


- 使用建议：强烈推荐使用，是最新的密码哈希标准。

#### 4.4.2 bcrypt

- 功能：实现bcrypt(Blowfish-based password hashing function)密码哈希算法
- 用途：安全地存储密码
- 示例：

```
import "golang.org/x/crypto/bcrypt"
hash, _ := bcrypt.GenerateFromPassword([]byte("password"), bcrypt.DefaultCost)
```


- 使用建议：推荐使用，广泛应用于
[密码存储](https://tonybai.com/2023/10/25/understand-password-storage-of-web-app-by-example/)。

#### 4.4.3 hkdf

- 功能：实现HMAC-based Key Derivation Function (HKDF)
- 用途：HKDF是基于HMAC（Hash-based Message Authentication Code）的一种变体，专门用于从较短的输入密钥材料（如共享密钥或密码）派生出更长的、安全的密钥。
- 示例：

```
import "golang.org/x/crypto/hkdf"
hkdf := hkdf.New(sha256.New, secret, salt, info)
```


- 使用建议：推荐使用，是标准的密钥派生函数。

#### 4.4.4 pbkdf2

- 功能：实现PBKDF2（Password-Based Key Derivation Function 2, 基于密码的密钥派生函数2）
- 用途：从密码派生密钥
- 示例：

```
import "golang.org/x/crypto/pbkdf2"
dk := pbkdf2.Key([]byte("password"), salt, 4096, 32, sha1.New)
```


- 使用建议：对于需要高安全性和抵抗暴力破解攻击的应用，PBKDF2是一个很好的选择。然而，对于更现代的应用，特别是那些对安全性有极高要求的应用，可能更推荐使用更现代的密码哈希算法，如Argon2。

#### 4.4.5 scrypt

- 功能：实现scrypt(Scrypt key derivation function)密钥派生函数
- 用途：从密码派生密钥，特别适合抵抗硬件暴力破解
- 示例：

```
import "golang.org/x/crypto/scrypt"
dk, _ := scrypt.Key([]byte("password"), salt, 32768, 8, 1, 32)
```


- 使用建议：推荐使用，特别是在需要
[抵抗硬件攻击或并行计算攻击的场景](https://tonybai.com/2023/10/25/understand-password-storage-of-web-app-by-example/)。

### 4.5 公钥密码学

#### 4.5.1 bn256

- 功能：实现256位Barreto-Naehrig曲线
- 用途：支持双线性对运算，用于某些高级密码协议
- 示例：

```
import "golang.org/x/crypto/bn256"
g1 := new(bn256.G1).ScalarBaseMult(k)
```


- 使用建议：该包已作废并冻结，不推荐使用。github.com/cloudflare/bn256有更完整的实现，但对于新的应用，特别是那些对安全性有极高要求的应用，不推荐使用bn256。

#### 4.5.2 nacl

- 功能：提供NaCl（Networking and Cryptography library）的Go实现
- 用途：NaCl主要用于需要高效加密和安全通信的应用。它提供了各种加密原语，包括对称加密、公钥加密、哈希函数、消息认证码（MAC）和密钥协商协议等。
- 示例：

```
import "golang.org/x/crypto/nacl/box"
publicKey, privateKey, _ := box.GenerateKey(rand.Reader)
```


- 使用建议：推荐使用，提供了易用的高级加密接口

### 4.6 协议和标准

#### 4.6.1 acme

- 功能：实现ACME（Automatic Certificate Management Environment）协议，该协议旨在自动化证书的颁发、更新和管理。它允许服务器自动请求和接收TLS/SSL证书，而无需人工干预。
- 用途：自动化证书管理，如Let’s Encrypt
- 示例：使用较复杂，通常通过更高级的库如golang.org/x/crypto/acme/autocert使用，鉴于篇幅，这里就不贴代码了。
- 使用建议：在需要自动化证书管理的场景中推荐使用

#### 4.6.2 ocsp

- 功能：实现在线证书状态协议（OCSP, Online Certificate Status Protocol），该协议提供了一种实时查询数字证书状态的方法。它允许客户端在建立安全连接之前，向证书颁发机构（CA）查询特定证书的有效性。
- 用途：检查X.509数字证书的撤销状态
- 示例：

```
import "golang.org/x/crypto/ocsp"
resp, _ := ocsp.ParseResponse(responseBytes, issuer)
```


- 使用建议：在需要证书状态检查的应用中推荐使用

#### 4.6.3 openpgp

- 功能：实现OpenPGP(Open Pretty Good Privacy)标准。OpenPGP是一种加密标准，旨在提供数据加密和解密、数字签名和数据完整性保护。
- 用途：主要用于保护电子邮件通信、文件存储和数据传输的安全。它支持对称加密、公钥加密、哈希函数和消息认证码（MAC），以及生成和验证数字签名。
- 示例：

```
import "golang.org/x/crypto/openpgp"
entity, _ := openpgp.NewEntity("name", "comment", "email", nil)
```


- 使用建议：OpenPGP是一个强大、灵活和安全的加密标准，被广泛用于各种安全协议和应用中，包括电子邮件加密、文件加密和数据传输加密。在许多现代安全应用中被推荐使用。

#### 4.6.4 otr

- 功能：实现Off-The-Record Messaging (OTR) 离线消息传递协议
- 用途：提供即时通讯场景的端到端加密，确保通信内容只能被预期的接收者阅读，而不会被第三方窃听或篡改。
- 示例：（使用较复杂，通常需要结合具体的即时通讯应用）
- 使用建议：在开发加密即时通讯应用时可以考虑使用

#### 4.6.5 pkcs12

- 功能：实现PKCS#12标准(Public-Key Cryptography Standards #12)，PKCS#12是由RSA Laboratories设计的，旨在定义一种标准格式，用于存储和传输私钥、公钥和证书链。PKCS#12文件通常以.p12或.pfx扩展名结尾。
- 用途：存储和传输服务器证书、中间证书和私钥
- 示例：

```
import "golang.org/x/crypto/pkcs12"
blocks, _ := pkcs12.ToPEM(pfxData, "password")
```


- 使用建议：PKCS#12是一个强大、安全和标准化的密钥和证书存储格式，在需要安全存储和传输加密密钥和证书的应用中被推荐使用。不过该包已经冻结，如需要，可考虑software.sslmate.com/src/go-pkcs12的实现(github.com/SSLMate/go-pkcs12)。

#### 4.6.6 ssh

- 功能：实现SSH客户端和服务器
- 用途：提供安全的远程登录和其他安全网络服务
- 示例：

```
import "golang.org/x/crypto/ssh"
config := &ssh.ClientConfig{User: "user", Auth: []ssh.AuthMethod{ssh.Password("password")}}
```


- 使用建议：强烈推荐用于实现SSH功能

### 4.7 其他

#### 4.7.1 poly1305

- 功能：实现Poly1305消息认证码。Poly1305是一种高速的消息认证码（MAC）算法, 通常与ChaCha20流加密算法结合使用，形成ChaCha20-Poly1305组合，用于提供加密和消息认证的完整解决方案。
- 用途：用于消息认证，确保消息在传输过程中的完整性和真实性，未被篡改。
- 示例：

```
import "golang.org/x/crypto/poly1305"
var key [32]byte
var out [16]byte
poly1305.Sum(&out, msg, &key)
```


- 使用建议：这个包的实现已作废，推荐使用golang.org/x/crypto/chacha20poly1305

## 5. Go密码学库的现状与后续方向

Gotime在2023年末和今年年初对Go密码学库的前负责人Filippo Valsorda和现负责人Roland Shoemaker进行了三期访谈(见参考资料)，通过这三次访谈我们大约可以梳理出Go密码学库的现状与后续方向：

- RSA后端实现的改进，提高了安全性和性能。
- 引入
[godebug机制](https://tonybai.com/2024/10/11/go-evolution-dual-insurance-goexperiment-godebug)，允许在[不破坏兼容性](https://tonybai.com/2023/09/10/understand-go-forward-compatibility-and-toolchain-rule)的情况下逐步引入新的安全改进。 - 正在考虑对一些密码学包进行v2版本的设计，以提供更高级和更易用的API。
- 正在逐步弃用一些不安全的算法，如SHA1和MD5。
- 简化配置选项，减少用户需要做的选择，提供更多默认安全设置。
- 正在将golang.org/x/crypto中的重要包移入标准库，以减少混淆，包括继TLS之后的另外一个重要协议包ssh库。
- 使用BoringSSL的BoGo测试套件来全面测试Go的TLS实现。
- Go密码学库正在实现这些新的
[后量子密码算法](https://en.wikipedia.org/wiki/Post-quantum_cryptography)，但目前还没有完全集成到标准库中。

总的来说，Go密码学库(包括golang.org/x/crypto)正在积极发展和改进，同时也在为后量子密码学时代做准备。虽然后量子算法的完全集成和广泛应用还需要一段时间，但Go团队正在积极跟进这一领域的发展，努力在保持兼容性的同时提升安全性和性能。

## 6. 小结

在这篇文章中，我们对Go生态中密码学功能的核心：Go crypto库(包括标准库crypto相关包以及golang.org/x/crypto相关包)进行了全面的了解，包括两者的关系、整体结构设计原则以及每个库的子包概览。

我们看到：Go crypto库以其安全性、全面性、易用性、高性能以及与Go生态系统的高度集成而著称。它不仅涵盖了广泛的加密算法和协议，还通过统一且直观的API降低了使用门槛。

相信通过上述的了解，大家都已经理解了Go crypto库的架构与设计思想，并建立起了一张crypto库的“地图”。按照这幅图的指示，大家可以根据具体需求，快速找到合适的密码学包，并利用这些包构建安全可靠的Go应用。

## 7. 参考资料

[What’s new in Go’s cryptography libraries: Part 1](https://changelog.com/gotime/295)– https://changelog.com/gotime/295[What’s new in Go’s cryptography libraries: Part 2](https://changelog.com/gotime/298)– https://changelog.com/gotime/298[What’s new in Go’s cryptography libraries: Part 3](https://changelog.com/gotime/313?ref=tonybai.com)– https://changelog.com/gotime/313[Crypto 101: A Brief Tour of Practical Crypto in Golang](https://cyberspy.io/articles/crypto101/)– https://cyberspy.io/articles/crypto101/[Go for Crypto Developers](https://www.youtube.com/watch?v=2r_KMzXB74w)– https://www.youtube.com/watch?v=2r_KMzXB74w

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

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
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论