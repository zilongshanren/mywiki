---
title: 构建无密码认证：passkey入门与Go实现
url: https://tonybai.com/2024/11/01/introduction-to-passkey/
published: '2024-11-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 构建无密码认证：passkey入门与Go实现

![](../../assets/095d75fbf027e17c.png)


[本文永久链接](https://tonybai.com/2024/11/01/introduction-to-passkey) – https://tonybai.com/2024/11/01/introduction-to-passkey

传统的密码认证一直以来都是数字时代的[主流身份验证方式](https://tonybai.com/2023/10/23/understand-go-web-authn-by-example)。然而，用户常常选择易记的弱密码并重复使用，导致账号易受攻击。密码泄露、钓鱼攻击等安全问题层出不穷，超过80%的数据泄露与密码相关。

![](../../assets/47a605f13dc2e0e7.png)



与此同时，频繁的密码管理和忘记密码情况严重影响用户体验。服务商在[安全保存用户密码](https://tonybai.com/2023/11/08/understand-go-web-secret-management-by-example)方面的责任也增加了系统建设和维护的成本。为了应对这些问题，科技行业开始积极探索无密码认证的方法。

无密码认证利用设备生物识别、硬件加密和其他更安全的验证手段，提供了更安全的登录体验。在[Thoughtworks最新一期（第31期）技术雷达文档](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2024/10/tr_technology_radar_vol_31_en.pdf)中，一种名为[passkey](https://fidoalliance.org/passkeys/)的无密码认证技术被列入“试验” 象限，许多读者可能在[github](https://docs.github.com/en/authentication/authenticating-with-a-passkey/signing-in-with-a-passkey)或其他支持passkey的站点和应用中使用过这一技术了。

![](../../assets/d7123f758eeba446.png)


Passkey是[FIDO联盟(Fast IDentity Online)](https://fidoalliance.org/overview/)提出的一种[无密码认证解决方案](https://fidoalliance.org/passkeys/)。FIDO联盟是一个开放的行业协会，其核心使命是**减少世界对密码的依赖**。联盟成员包括众多知名的科技公司和组织，如Google、微软、Apple、Amazon等，致力于定义一套开放、可扩展、可互操作的机制，以降低用户和设备身份验证时对密码的依赖。

Passkey是FIDO联盟的首个无密码身份认证凭据方案，支持用户通过与解锁手机、平板或计算机相同的方式（如生物识别(比如屏幕指纹、面部识别等)、PIN码或图案）登录应用程序和网站。目前许多主流设备、操作系统原生应用、浏览器和站点都支持passkey技术(如下图)，这使得passkey技术在未来的无密码认证认证领域展现出巨大的潜力。

![](../../assets/335012cec7e5c8d2.png)



在这篇文章中，我将对passkey技术进行入门介绍，并通过Go实现一个简单的示例供大家参考。

## 1. passkey的工作原理

通过上面的介绍，我们大致知道了passkey是密码的替代品，一旦使用了passkey，我们登录网站时就无需再输入密码，用于网站对你的身份进行验证的passkey存储在你的设备本地，你顶多只需通过本地设备的生物识别(比如指纹、人脸或图案密码等)进行一次解锁即可。

从技术本质来说，**paaskey就是“免密登录服务器”方案在Web服务和终端App领域的应用**。没错！passkey就是基于非对称加密实现的一种无密码认证技术。下图展示了Bob这个用户登录不同Web服务时使用不同passkey的情景：

![](../../assets/4d4de45fe762411a.png)


如果你熟悉非对称加密的运作原理，你就可以立即get到passkey的工作原理。

注：在《

[Go语言精进之路：从新手到高手的编程思想、方法和技巧]》的第51条“使用net/http包实现安全通信”中有对非对称加密的全面系统讲解以及示例说明。如果你不是很熟悉，可以看一下我的这本书中的内容。

以上图中的Web Service1为例，用户Bob在注册时会在其自己的设备(比如电脑)上创建一对私钥与公钥，比如Bob的bob-ws1-private key和bob-ws1-public key，私钥会保存在Bob的设备上，而并不需要保密的公钥则会发送给Web Service1保存。之后，Web Service1对Bob进行身份验证的时候，只需发送一块数据给Bob设备上的应用(通常是浏览器)，应用会申请使用Bob的私钥，这个过程可能需要bob输入设备的用户密码或使用生物识别（比如指纹）来授权。使用Bob的私钥对这块数据进行签名后，发回Web Service1，后者通过Bob保存在服务器上的公钥对这块签名后的数据进行验签，验签通过，则Bob的身份验证就通过了！当然这只是基本原理，还有很多场景、交互和技术细节，比如支持在网吧等公共计算机上借助个人的其他设备(比如手机)进行基于passkey的的身份验证等，这些需要进一步阅读相关规范。更多原理细节我们也会在接下来的内容中详细说明。

不过，在进一步了解原理之前，我们先来了解一下paaskey与FIDO、webauthn之间的关系。

[FIDO2](https://fidoalliance.org/specifications-overview/)是一个开放的认证标准框架，旨在取代传统密码认证。它包含[WebAuthn](https://www.w3.org/TR/webauthn-1/)（由W3C提供的WebAPI规范）和[CTAP](https://fidoalliance.org/specifications/download/)（客户端到认证器的协议），即客户端设备和外部认证器的通信标准。FIDO2的主要目标是增强网络安全性，支持无需密码的安全登录方式。

WebAuthn是FIDO2的WebAPI组件，定义了应用如何在网页上与浏览器协作，以支持基于公钥的认证方式。它允许浏览器和Web应用访问用户设备上的身份验证器（如指纹传感器或USB密钥），并进行认证交互。WebAuthn作为Web标准，得到了大多数现代浏览器的支持。

Passkey是对FIDO2标准的应用，以实现无密码认证。在技术栈上，Passkey利用WebAuthn和CTAP来构建实际应用体验，从而让用户在支持FIDO2的Web应用中享受无密码登录的便捷。这三者共同实现了现代无密码身份认证的完整生态体系。

下面我们通过一个序列图具体了解一下paaskey的工作原理：

![](../../assets/4d3961706afbd057.png)


上图展示了Passkey的工作流程，包括注册和认证两个主要流程。

在passkey（即基于WebAuthn的非密码认证机制）中，有三个主要的实体：

- 浏览器(客户端)：提供 WebAuthn API
- 服务器(即规范中的依赖方(Relying Party))：验证用户身份
- 认证器(Authenticator)： 生成和存储密钥对（认证器可以是设备内置的，如TouchID、FaceID，或外部硬件如YubiKey）。

我们先来看看**注册流程**。

用户输入用户名并触发注册流程，浏览器向服务器请求注册选项，服务器生成随机挑战（challenge）并创建注册选项。

浏览器调用WebAuthn API(navigator.credentials.create)，操作系统检查可用的认证器，并根据认证器类型调用相应的系统API。 认证器请求用户验证（如需要），系统根据请求的用户验证级别来决定验证方式。验证级别包括无需验证(none)、隐式验证(silent，比如设备已解锁，使用之前的验证结果)以及必须验证（Required）。如果是必须验证，系统会显示验证提示（密码/生物识别/PIN等）。

用户提供身份验证信息后，认证器会生成新的公私钥对，并将私钥安全存储在认证器中，公钥和其他凭证数据(私钥签名后的挑战数据)返回给浏览器。浏览器将公钥和其他凭证发送给服务器，服务器验证凭证(通过公钥验签)并存储公钥，注册完成。

接下来，我们再来看**认证流程**。

当用户输入用户名并触发登录后，浏览器会向服务器请求认证选项，服务器生成新的挑战并返回认证选项。

浏览器调用WebAuthn API (navigator.credentials.get)，认证器使用私钥对挑战进行签名，并返回签名和其他断言数据给浏览器。

浏览器将断言发送给服务器，服务器使用存储的公钥验证签名，认证完成。

我们看到在整个注册和身份验证流程中，用户都无需记忆复杂的密码，机密信息（比如传统的密码）也无需传递给服务器保存，而公钥本身就是随意公开分发的，服务端甚至都无需对其进行任何加密处理。由此可以看到：passkey既提供了更好的安全性，又提供了更好的用户体验，是传统密码认证的理想替代方案之一。

注：使用另一个设备进行身份验证的流程，大家可以自行阅读passkey相关规范了解。


了解了原理之后，我们再来看一个简单的示例，直观地看看如何实现基于passkey的身份认证。

## 2. passkey身份认证示例

我们使用Go实现一个最简单的基于passkey进行注册和身份验证的示例。在这个示例里，我们将使用[webauthn官方推荐的Go包](https://webauthn.io/)：go-webauthn/webauthn来实现服务端对passkey登录的支持。

注：本示例的工作环境为Go 1.23.0、macOS和Edge浏览器。


这个示例的文件布局如下：

```
// intro-to-passkey/demo
$tree -F .
.
├── go.mod
├── go.sum
├── main.go
└── static/
└── index.html
```


首先我们通过一个静态文件服务器提供了前端首页，并注册了4个API端点用于处理Passkey注册和认证：

```
// intro-to-passkey/demo/main.go
func main() {
// 静态文件服务
http.Handle("/", http.FileServer(http.Dir("static")))
// API 路由
http.HandleFunc("/api/register/begin", handleBeginRegistration)
http.HandleFunc("/api/register/finish", handleFinishRegistration)
http.HandleFunc("/api/login/begin", handleBeginLogin)
http.HandleFunc("/api/login/finish", handleFinishLogin)
log.Println("Server running on http://localhost:8080")
log.Fatal(http.ListenAndServe(":8080", nil))
}
```


关键的passkey配置在init函数中：

```
func init() {
var err error
webAuthn, err = webauthn.New(&webauthn.Config{
RPDisplayName: "Passkey Demo", // Relying Party Display Name
RPID: "localhost", // Relying Party ID
RPOrigins: []string{"http://localhost:8080"}, //允许的源
})
if err != nil {
log.Fatal(err)
}
userDB = NewUserDB() // 初始化内存用户数据库
}
```


运行该go程序后，打开localhost:8080，我们将看到下面页面：

![](../../assets/426eff40d56926d6.png)


接下来，我们先来注册一个用户的passkey。在注册输入框中输入”tonybai”，点击“注册”，浏览器会弹出下面对话框，提醒用户将为localhost创建密钥：

![](../../assets/3ed31e0aaa7499ca.png)


点击“继续”，本地os会弹出身份验证对话框：

![](../../assets/ebb5f538b581341a.png)


输入你的os登录密码，便可继续注册过程。如果注册ok，页面会显示下面“注册成功”字样：

![](../../assets/66b763df6e87528b.png)


在服务器后端，上述的注册过程是由两个handler共同完成的，这也是webauthn规范确定的流程，大家可以结合上面的序列图一起看。

首先是处理/api/register/begin的handleBeginRegistration，它的大致逻辑如下：

```
func handleBeginRegistration(w http.ResponseWriter, r *http.Request) {
// 1. 验证用户名是否已存在
if _, exists := userDB.users[data.Username]; exists {
http.Error(w, "User already exists", http.StatusBadRequest)
return
}
// 2. 创建新用户
user := &User{
ID: []byte(data.Username),
Name: data.Username,
DisplayName: data.Username,
}
userDB.users[data.Username] = user
// 3. 生成注册选项和会话数据
options, sessionData, err := webAuthn.BeginRegistration(user)
// 4. 存储会话数据
sessionID := storeSession(sessionData)
http.SetCookie(w, &http.Cookie{
Name: "registration_session",
Value: sessionID,
Path: "/",
MaxAge: 300,
HttpOnly: true,
})
// 5. 返回注册选项给客户端
json.NewEncoder(w).Encode(options)
}
```


注意：这段代码中的session与传统Web应用中用于跟踪用户登录状态的session不同。这种session机制是WebAuthn协议的一部分，用于确保认证流程的安全性：

- 防止重放攻击：每次认证都会生成新的挑战
- 确保认证操作的完整性：开始认证和完成认证必须使用相同的session数据
- 时效性控制：认证过程必须在有限时间内完成(上面示例中的有效期为5分钟)

所以这里的session更像是一个”挑战-响应”认证过程中的临时状态存储，而不是用来维持用户登录状态的传统session。用户的登录状态管理应该是在这个认证系统之上另外实现的，比如使用JWT token或传统的session机制。

handleFinishRegistration用于处理客户端发到/api/register/finish的完成注册请求，它的逻辑大致如下：

```
func handleFinishRegistration(w http.ResponseWriter, r *http.Request) {
// 1. 获取并验证会话
sessionData, ok := getSession(cookie.Value)
if !ok {
http.Error(w, "Invalid session", http.StatusBadRequest)
return
}
// 2. 获取用户信息
username := string(sessionData.UserID)
user := userDB.users[username]
// 3. 验证并完成注册
credential, err := webAuthn.FinishRegistration(user, *sessionData, r)
// 4. 保存凭证
userDB.Lock()
user.Credentials = append(user.Credentials, *credential)
userDB.Unlock()
// 5. 清理会话
delete(sessionStore, cookie.Value)
}
```


注册passkey后，我们就可以来基于passkey进行登录了！服务端会使用passkey对用户进行身份验证。

我们在登录输入框中输入”tonybai”，然后点击”Passkey登录”，本地os会弹出身份验证对话框：

![](../../assets/ebb5f538b581341a.png)


输入os登录密码后，便可继续身份验证过程，如果服务端身份验证ok，页面会显示下面“登录成功”字样：

![](../../assets/887dad3a447e1e97.png)


如果在登录输入框中输入一个未曾注册过的用户名，则服务器会验证失败，页面会显示如下错误：

![](../../assets/4c0c2e7bd8630668.png)


和注册过程一样，上述的验证过程也是由两个handler共同完成的，这也是webauthn规范确定的流程。

首先是处理/api/login/begin的handleBeginLogin，它的大致逻辑如下：

```
func handleBeginLogin(w http.ResponseWriter, r *http.Request) {
// 1. 验证用户是否存在
user, ok := userDB.users[data.Username]
if !ok {
http.Error(w, "User not found", http.StatusNotFound)
return
}
// 2. 生成认证选项和会话数据
options, sessionData, err := webAuthn.BeginLogin(user)
// 3. 存储会话数据
sessionID := storeSession(sessionData)
http.SetCookie(w, &http.Cookie{
Name: "login_session",
Value: sessionID,
Path: "/",
MaxAge: 300,
HttpOnly: true,
})
// 4. 返回认证选项给客户端
json.NewEncoder(w).Encode(options)
}
```


之后，是handleFinishLogin处理的来自客户端到/api/login/finish的请求，以完成登录流程：

```
func handleFinishLogin(w http.ResponseWriter, r *http.Request) {
// 1. 获取并验证会话
sessionData, ok := getSession(cookie.Value)
if !ok {
http.Error(w, "Invalid session", http.StatusBadRequest)
return
}
// 2. 获取用户信息
username := string(sessionData.UserID)
user := userDB.users[username]
// 3. 验证并完成登录
_, err = webAuthn.FinishLogin(user, *sessionData, r)
// 4. 清理会话
delete(sessionStore, cookie.Value)
}
```


我们看到注册和登录都采用两步验证流程，每个流程都包含开始和完成两个步骤，同时使用会话保持认证状态的连续性。

整个示例的前端基本由js代码完成：

```
<!DOCTYPE html>
<html>
<head>
<title>Passkey Demo</title>
<style>
.container {
margin: 20px;
padding: 20px;
border: 1px solid #ccc;
}
.form-group {
margin: 10px 0;
}
#status {
margin-top: 20px;
padding: 10px;
}
.error {
color: red;
}
.success {
color: green;
}
</style>
</head>
<body>
<div class="container">
<h2>注册</h2>
<div class="form-group">
<input type="text" id="registerUsername" placeholder="用户名">
<button onclick="register()">注册 Passkey</button>
</div>
</div>
<div class="container">
<h2>登录</h2>
<div class="form-group">
<input type="text" id="loginUsername" placeholder="用户名">
<button onclick="login()">Passkey 登录</button>
</div>
</div>
<div id="status"></div>
<script>
// 工具函数：将 ArrayBuffer 转换为 Base64URL 字符串
function bufferToBase64URL(buffer) {
const bytes = new Uint8Array(buffer);
let str = '';
for (const byte of bytes) {
str += String.fromCharCode(byte);
}
return btoa(str)
.replace(/\+/g, '-')
.replace(/\//g, '_')
.replace(/=/g, '');
}
// 工具函数：将 Base64URL 字符串转换为 ArrayBuffer
function base64URLToBuffer(base64URL) {
if (!base64URL) {
throw new Error('Empty base64URL string');
}
const base64 = base64URL.replace(/-/g, '+').replace(/_/g, '/');
const padLen = (4 - (base64.length % 4)) % 4;
const padded = base64.padEnd(base64.length + padLen, '=');
const binary = atob(padded);
const buffer = new ArrayBuffer(binary.length);
const bytes = new Uint8Array(buffer);
for (let i = 0; i < binary.length; i++) {
bytes[i] = binary.charCodeAt(i);
}
return buffer;
}
function showStatus(message, isError = false) {
const status = document.getElementById('status');
status.textContent = message;
status.className = isError ? 'error' : 'success';
}
// 开始注册
async function startRegistration(username) {
try {
// 1. 从服务器获取注册选项
const response = await fetch('/api/register/begin', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify({ username }),
});
if (!response.ok) {
throw new Error(`Server error: ${response.status}`);
}
const responseData = await response.json();
// 确保我们使用的是 publicKey 对象
const options = responseData.publicKey;
if (!options) {
throw new Error('Invalid server response: missing publicKey');
}
// 2. 解码 challenge
options.challenge = base64URLToBuffer(options.challenge);
// 3. 解码 user.id
if (options.user && options.user.id) {
options.user.id = base64URLToBuffer(options.user.id);
}
console.log('Processed options:', options); // 调试输出
// 4. 创建凭证
const credential = await navigator.credentials.create({
publicKey: options
});
// 5. 准备发送到服务器的数据
const registrationData = {
id: credential.id,
rawId: bufferToBase64URL(credential.rawId),
type: credential.type,
response: {
attestationObject: bufferToBase64URL(credential.response.attestationObject),
clientDataJSON: bufferToBase64URL(credential.response.clientDataJSON)
}
};
// 6. 发送注册数据到服务器
const finishResponse = await fetch('/api/register/finish', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify(registrationData)
});
if (!finishResponse.ok) {
throw new Error(`Server error: ${finishResponse.status}`);
}
showStatus('注册成功！');
} catch (error) {
console.error('Registration error:', error);
showStatus(`注册失败: ${error.message}`, true);
}
}
// 开始登录
async function startLogin(username) {
try {
// 1. 从服务器获取登录选项
const response = await fetch('/api/login/begin', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify({ username }),
});
if (!response.ok) {
throw new Error(`Server error: ${response.status}`);
}
const responseData = await response.json();
const options = responseData.publicKey;
if (!options) {
throw new Error('Invalid server response: missing publicKey');
}
// 2. 解码 challenge
options.challenge = base64URLToBuffer(options.challenge);
// 3. 解码 allowCredentials
if (options.allowCredentials) {
options.allowCredentials = options.allowCredentials.map(credential => ({
...credential,
id: base64URLToBuffer(credential.id),
}));
}
// 4. 获取凭证
const credential = await navigator.credentials.get({
publicKey: options
});
// 5. 准备发送到服务器的数据
const loginData = {
id: credential.id,
rawId: bufferToBase64URL(credential.rawId),
type: credential.type,
response: {
authenticatorData: bufferToBase64URL(credential.response.authenticatorData),
clientDataJSON: bufferToBase64URL(credential.response.clientDataJSON),
signature: bufferToBase64URL(credential.response.signature),
userHandle: credential.response.userHandle ? bufferToBase64URL(credential.response.userHandle) : null
}
};
// 6. 发送登录数据到服务器
const finishResponse = await fetch('/api/login/finish', {
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify(loginData)
});
if (!finishResponse.ok) {
throw new Error(`Server error: ${finishResponse.status}`);
}
showStatus('登录成功！');
} catch (error) {
console.error('Login error:', error);
showStatus(`登录失败: ${error.message}`, true);
}
}
// 注册按钮处理函数
function register() {
const username = document.getElementById('registerUsername').value;
if (!username) {
showStatus('请输入用户名', true);
return;
}
startRegistration(username);
}
// 登录按钮处理函数
function login() {
const username = document.getElementById('loginUsername').value;
if (!username) {
showStatus('请输入用户名', true);
return;
}
startLogin(username);
}
</script>
</body>
</html>
```


这段代码没有使用任何第三方库或框架，对js略知一二的读者想必也能看个七七八八。

综上，我们看到这个示例实现提供了完整的Passkey认证功能，但需要注意这是一个演示版本。在生产环境中，还需要考虑更多，比如数据的持久化存储、更完善的错误处理等。

## 3. 小结

本文粗略探讨了无密码认证技术中的一种新兴方案——passkey。随着传统密码认证的安全隐患日益严重，passkey作为FIDO联盟提出的解决方案，利用生物识别和硬件加密以及非对称加密等先进技术，为用户提供了更安全、便捷的身份验证体验。

在文中，我还详细介绍了passkey的工作原理，包括注册和登录流程，强调了非对称加密在身份验证中的重要作用。此外，通过一个基于Go语言的示例，我们展示了如何实现passkey的注册和认证功能，帮助读者更好地理解其实际应用。

整体来看，passkey不仅提升了安全性，还改善了用户体验，是未来无密码认证的有力候选方案。随着passkey技术的发展，期待更多应用场景的出现，为用户带来更安全的网络环境。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/intro-to-passkey)下载。

## 4. 参考资料

[passkey.org](https://passkey.org)– https://passkey.org[passkeys.dev](https://passkeys.dev)– https://passkeys.dev[webauthn.guide](https://webauthn.guide/)– https://webauthn.guide/[FIDO alliance](https://fidoalliance.org/)– https://fidoalliance.org/[webauthn.io](https://webauthn.io/)– https://webauthn.io/[WebAuthn 规范](https://www.w3.org/TR/webauthn/)– https://www.w3.org/TR/webauthn/[FIDO2 文档](https://fidoalliance.org/fido2/)– https://fidoalliance.org/fido2/

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

No related posts.

## 评论