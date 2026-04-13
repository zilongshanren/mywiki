---
title: 通过实例理解Go Web身份认证的几种方式
url: https://tonybai.com/2023/10/23/understand-go-web-authn-by-example/
published: '2023-10-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解Go Web身份认证的几种方式

![](../../assets/1bef50b428a7b138.png)


[本文永久链接](https://tonybai.com/2023/10/23/understand-go-web-authn-by-example) – https://tonybai.com/2023/10/23/understand-go-web-authn-by-example

在[2023年Q1 Go官方用户调查报告](https://go.dev/blog/survey2023-q1-results)中，API/RPC services、Websites/web services都位于使用Go开发的应用类别的头部(如下图)：

![](../../assets/472e47474cb55999.png)


我个人使用Go开发已很多年，但一直从事底层基础设施、分布式中间件等方向，Web应用开发领域涉及较少，像Web应用领域常见的CRUD更是少有涉猎，不能不说是一种“遗憾”^_^。未来一段时间，团队会接触到Web应用的开发，我打算对Go Web应用开发的重点环节做一个快速系统的梳理。

而身份认证(Authentication，简称AuthN)是Web应用开发中一个关键的环节，也是首个环节，它负责验证用户身份，让用户可以以认证过的身份访问系统中的资源和信息。

Go语言作为一门优秀的Web开发语言，提供了丰富的机制来实现Web应用的用户身份认证。在这篇文章中，我就通过Go示例和大家一起探讨一下当前Web应用开发中几种常见的主流身份认证方式，帮助自己和各位读者**迈出Web应用开发修炼之路的第一步**。

## 1. 身份认证简介

### 1.1 身份认证解决的问题

身份认证不局限于Web应用，各种系统都会有身份认证，但本文我们聚焦Web应用领域的身份认证技术。

几乎所有Web应用的安全性都是从身份认证开始的，身份认证是验证用户身份真实性的过程，是我们首先要部署的策略。位于下游的安全控制，如授权(Authorization, AuthZ)、审计日志(Audit log)等，几乎都需要用户的身份。

身份认证的英文是Authentication，简写为AuthN，大家不要将之与授权Authorization(AuthZ)混淆(在后续系列文章中会继续探讨AuthZ相关的内容)，他们所要解决的问题相似，但有不同，也有先后。通常先AuthN，再AuthZ。我们可以用下面的比喻来形象地解释二者的联系与差异:

- AuthN就像是进入公司大楼的安检，负责检查员工的身份是否合法，是否具有进入公司的资格，
**它解决的是验证员工身份的问题**。 - AuthZ更像是公司内部的权限管理，某个员工进入了公司后(AuthN后)想访问一些重要资料，这时还需要确认该员工是否有相应的访问权限。它解决的是授权访问控制的问题。

简单来说，**AuthN是验证你是谁**，authZ是验证你有哪些权限。AuthN解决认证问题，AuthZ解决授权问题，这两个都重要，AuthN解决外部的安全问题，authZ解决内部的安全与合规问题。

### 1.2 身份认证的三要素

身份认证需要被认证方提供一些身份信息输入，这些代表身份信息的输入被称为身份认证要素（authentication factor）。这些要素有很多，大致可分为三类：

- 你知道的东西(What you know)

即基于被认证方知道的特定信息来验证身份，最常见的如密码等。

- 你拥有的东西(What you have)

基于被认证方所拥有的特定物件来验证身份，最常见的利用数字证书、令牌卡等。N年前，在移动端应用还没有发展起来时，一些人在银行办理电子银行业务时会拿到一个U盾(又称为USBKey)，其中存放着用于用户身份识别的数字证书，这个U盾就属于此类要素。

上面比喻中进入大楼时使用的员工卡也属于这类要素。

- 你本身就具有的(What you are)

即基于被认证方所拥有的生物特征要素(biometric factor)来验证身份，最常见的人脸识别、指纹/声纹/虹膜识别和解锁等。理论上来说，具备个人生物特征的身份认证标志具有不可仿冒性、唯一性。

如果上面比喻中的大楼已经开启了人脸识别功能，那么基于人脸识别的认证就属于这类要素的认证。

通常我们会基于单个要素设计身份认证方案，一旦使用两个或两个以上不同类的要素，就可以被称为** 双因素认证(2FA)**或

**多因素认证(MFA)**了。不过，2FA和MFA都比较复杂，不再本篇文章讨论范围之内。

基于上述要素，我们就可以设计和实现各种适合不同类别Web应用或API服务的身份认证方法了。Web应用和API服务都需要身份认证，它们有什么差异呢？这些差异是否会对身份认证方案产生影响呢？我们接下来看一下。

### 1.3 Web应用身份认证 vs. API服务身份认证

Web应用和API服务主要有以下几点区别:

- 交互方式不同

Web应用是浏览器与服务器之间的交互，用户通过浏览器访问Web应用。而API服务是程序/应用与服务器之间的交互，通过API请求获取数据或执行操作。

- 返回数据格式不同

Web应用通常会返回html/js/css等浏览器可解析执行的代码，而API服务通常返回结构化数据，常见的如JSON或XML等。

- 使用场景不同

Web应用主要面向人类用户的使用，用户通过浏览器进行操作。而API服务主要被其他程序调用，为程序之间提供接口与数据支撑。

- 状态管理不同

Web应用在服务端保存会话状态，浏览器通过cookie等保存用户状态。而API服务通常是无状态的，每次请求都需要携带用于身份认证的信息，比如访问令牌或API Key等。

- 安全方面的关注点不同

Web应用更关注[XSS](https://owasp.org/www-community/attacks/xss/)、[CSRF](https://owasp.org/www-community/attacks/csrf)等输入验证安全，而API服务更关注身份认证(authN)、授权(authZ)、准入(admission)、限流等访问控制安全。

总之，Web应用注重界面的展示和用户交互；而API服务注重数据和服务的提供，它们有不同的使用场景、交互方式和安全关注点。

Web应用和API服务的这些差异也导致了Web应用和API服务适合使用的身份认证方案上会有所不同。但**前后端分离架构的出现和普及**，让前后端责任分离：前端专注于视图和交互，后端专注数据和业务，并且前后端通过标准化的API接口进行数据交互。这可以让后端提供统一的认证接口，不同的前端可以共享。像基于Token这样的无状态易理解的身份验证机制逐渐成为主流。也就是说，架构模式的变化，使得Web应用和API服务在身份验证(authN)方案上出现了一些融合的现象，因此在身份认证方法上，Web应用和API服务也存在一些交集。

下面维韦恩图列出了三类身份认证方法，包括仅适用于Web应用的、仅适用于API服务的以及两者都适用的：

![](../../assets/113f6573d9644a0b.png)


本文聚焦Web应用的身份认证方式，接下来会重点说说上图中绿色背景色的几种身份认证方式。

## 2. 安全信道是身份认证的前提和基础

在对具体的Web身份认证方式进行说明之前，我们先来了解一下身份认证的前提和基础 – **安全信道**。

在Web应用身份认证的过程中，无论采用何种认证方式，用户的身份要素信息(用户名/密码、token、生物特征信息)都要传递给服务器，这时候如果传递此类信息的通信信道不安全，这些重要的认证要素信息就很容易被中间人截取、破解、篡改并被冒充，从而获得Web应用的使用权。从服务端角度来看，如果没有安全信道，服务器身份也容易被伪装，导致用户连接到“冒牌服务器”并导致严重后果。因此，没有建立在安全信道上的身份认证是不安全，不具备实际应用价值的，甚至是完全没有意义的。

此外，安全信道不仅对登录阶段的身份认证环节有重要意义，在用户已登录并访问Web应用其他功能页面时，安全通道也可以对数据的传输以及类似访问令牌或Cookie数据的传输起到加密和保护作用。

在Web应用领域，最常用的安全信道建立方式是基于HTTPS(HTTP over TLS)或直接建立在TLS之上的自定义通信，TLS利用证书对通信进行加密、验证服务器身份（甚至是客户端身份的验证），保障信息的机密性和完整性。各大安全规范和标准如[PCI DSS(Payment Card Industry Data Security Standard)](https://www.pcisecuritystandards.org/)、[OWASP](https://owasp.org)也强制要求使用HTTPS保障认证安全。

基于安全信道，我们还可以**实施第一波的身份认证**，这就是我们通常所说的**基于HTTPS(或TLS)的双向身份认证**。

注：在我的

[《Go语言精进之路vol2》]一书中，对TLS的机制以及[基于Go标准库的TLS的双向认证]有系统全面的说明，欢迎各位童鞋阅读反馈。

这种认证方式采用的是身份认证要素中的第二类要素：What you have。客户端带着归属于自己的专有证书去服务端做身份验证。如果client证书通过服务端的验签后，便可允许client进入“大楼”。

下面是一个基于TLS证书做身份认证的客户端与服务端交互的示意图：

![](../../assets/496dd812ac7e8a7e.png)


我们先看看对应上述示意图中的客户端的代码：

```
// authn-examples/tls-authn/client/main.go
func main() {
// 1. 读取客户端证书文件
clientCert, err := tls.LoadX509KeyPair("client-cert.pem", "client-key.pem")
if err != nil {
log.Fatal(err)
}
// 2. 读取中间CA证书文件
caCert, err := os.ReadFile("inter-cert.pem")
if err != nil {
log.Fatal(err)
}
certPool := x509.NewCertPool()
certPool.AppendCertsFromPEM(caCert)
// 3. 发送请求
client := &http.Client{
Transport: &http.Transport{
TLSClientConfig: &tls.Config{
Certificates: []tls.Certificate{clientCert},
RootCAs: certPool,
},
},
}
req, err := http.NewRequest("GET", "https://server.com:8443", nil)
if err != nil {
log.Fatal(err)
}
resp, err := client.Do(req)
if err != nil {
log.Fatal(err)
}
// 4. 打印响应信息
fmt.Println("Response Status:", resp.Status)
// fmt.Println("Response Headers:", resp.Header)
body, _ := io.ReadAll(resp.Body)
fmt.Println("Response Body:", string(body))
}
```


客户端加载client-cert.pem作为后续与服务端通信的身份凭证，加载inter-cert.pem用于校验服务端在tls握手过程发来的服务端证书(server-cert.pem)，避免连接到“冒牌站点”。通过验证后，客户端向服务端发起Get请求并输出响应的内容。

下面是服务端的代码：

```
// authn-examples/tls-authn/server/main.go
func main() {
var validClients = map[string]struct{}{
"client.com": struct{}{},
}
// 1. 加载证书文件
cert, err := tls.LoadX509KeyPair("server-cert.pem", "server-key.pem")
if err != nil {
log.Fatal(err)
}
caCert, err := os.ReadFile("inter-cert.pem")
if err != nil {
log.Fatal(err)
}
certPool := x509.NewCertPool()
certPool.AppendCertsFromPEM(caCert)
// 2. 配置TLS
tlsConfig := &tls.Config{
Certificates: []tls.Certificate{cert},
ClientAuth: tls.RequireAndVerifyClientCert, // will trigger the invoke of VerifyPeerCertificate
ClientCAs: certPool,
}
// tls.Config设置
tlsConfig.VerifyPeerCertificate = func(rawCerts [][]byte, verifiedChains [][]*x509.Certificate) error {
// 获取客户端证书
cert := verifiedChains[0][0]
// 提取CN作为客户端标识
clientID := cert.Subject.CommonName
fmt.Println(clientID)
_, ok := validClients[clientID]
if !ok {
return errors.New("invalid client id")
}
return nil
}
// 添加处理器
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
w.Write([]byte("Hello World!"))
})
// 3. 创建服务器
srv := &http.Server{
Addr: ":8443",
TLSConfig: tlsConfig,
}
// 4. 启动服务器
err = srv.ListenAndServeTLS("", "")
if err != nil {
log.Fatal(err)
}
}
```


注：在你的实验环境中，需要在/etc/hosts文件中添加server.com的映射ip为127.0.0.1。


服务端代码也不复杂，比较“套路化”：加载服务端证书和中间CA证书(用于验签client端的证书)，这里将tls.Config.ClientAuth设置为RequireAndVerifyClientCert，这会触发服务端对客户端证书的验签，同时在tlsConfig.VerifyPeerCertificate不为nil的情况下，触发对tlsConfig.VerifyPeerCertificate的函数的调用，在示例代码中，我们为tlsConfig.VerifyPeerCertificate赋值了一个匿名函数实现，在这个函数中，我们提取了客户端证书中的客户端标识CN，并查看其是否在可信任的客户端ID表中。

在这个示例中，这个tlsConfig.VerifyPeerCertificate执行的验证有些多余，但我们在实际代码中可以使用tlsConfig.VerifyPeerCertificate来设置黑名单，拦截那些尚未过期、但可以验签通过的客户端，实现一种**客户端证书过期前的作废机制**。

此外，上述示例中客户端、服务端以及中间CA证书的制作代码与[《Go TLS服务端绑定证书的几种方式》](https://tonybai.com/2023/10/13/multiple-ways-to-bind-certificates-on-go-tls-server-side)一文中的证书制作很类似，大家可以直接参考本文示例代码中的tls-authn/make-certs下面的代码，这里就不赘述了。

通过这种基于安全信道的身份验证方式，客户端证书可以强制认证用户，理论上不需要额外再用用户名密码。认证之后客户端在这个TLS连接上发送的所有信息都将绑定其身份。

不过通过颁发客户端专用证书的方式仅适合一些像网络银行之类的专有业务，大多数Web应用会与客户端间建立安全信道，但不会采用客户端证书来认证用户身份，在这样的情况下，下面要说的这些身份认证方式就可以发挥作用了。

我们先来看一下最传统的基于密码的认证。

## 3. 基于密码的认证

基于密码的认证属于基于第一类身份认证要素：你知道的东西(What you know)的认证方式，这类认证也是Web应用中最经典、最常见的认证方式。我们先从基于传统表单承载用户名/密码说起。

### 3.1. 基于用户名+密码的认证(传统表单方式)

这是最常见的Web应用认证方式：用户通过提交包含用户名和密码的表单(Form)，服务端Web应用进行验证。下面使用这种方式的客户端与服务单的交互示意图：

![](../../assets/fc25b04a21254740.png)


接下来，我们看看对应上述示意图的实现代码。我们先建立一个html文件，该文件非常简单，就是一个可输入用户名和密码的表单，点击登录按钮将表单信息发送到服务端：

```
// authn-examples/password/classic/login.html
<!DOCTYPE html>
<html>
<head>
<title>登录</title>
</head>
<body>
<form action="http://server.com:8080/login" method="post">
<label>用户名:</label>
<input type="text" name="username"/>
<label>密码:</label>
<input type="password" name="password"/>
<button type="submit">登录</button>
</form>
</body>
</html>
```


发送的HTTP Post请求的包体(Body)中会包含页面输入的username和password的值，形式如下：

```
username=admin&password=123456
```


而我们的服务端的代码如下：

```
// authn-examples/password/classic/main.go
func main() {
http.HandleFunc("/login", login)
http.ListenAndServe(":8080", nil)
}
func login(w http.ResponseWriter, r *http.Request) {
username := r.FormValue("username")
password := r.FormValue("password")
if isValidUser(username, password) {
w.Write([]byte("Welcome!"))
return
}
http.Error(w, "Invalid username or password", http.StatusUnauthorized) // 401
}
var credentials = map[string]string{
"admin": "123456",
}
func isValidUser(username, password string) bool {
// 验证用户名密码
v, ok := credentials[username]
if !ok {
return false
}
if v != password {
return false
}
return true
}
```


服务端通过Request的FormValue方法获得username和password的值，并与credentials存储的合法用户信息比对(当然这只是演示代码中的临时手段，生产中不要这么存储用户信息)，比对成功，返回”Welcome”应答；比对失败，返回401 Unauthorized错误。

注：包括本示例在内的后续所有示例的客户端和服务端都在非安全信道上通信，目的是简化示例代码的编写。大家在生产环境务必建立安全信道后再做后续的身份验证。


基于传统的表单用户名和密码可以作为Web应用服务端身份验证的方案，但问题来了：服务端认证成功后，用户后续向Web应用服务端发起的请求是否还要继续带上用户和密码信息呢？如果不带上用户和密码信息，服务端又如何验证这些请求是来自之前已经认证成功后的用户；如果后续每个请求都带上以Form形式承载的用户名和密码，使用起来又非常不方便，还影响后续请求的正常数据的传输(对Body数据有侵入)。

于是便有了Session(会话)机制，它可以被认为是基于经典的用户名密码(表单承载)认证方式的“延续”，使得密码认证的成果不再局限在缺乏连续性的单一请求级别上，而是**扩展到后续的一段时间内或一系列与Web应用的互操作过程中**，变成了连续、持久的登录会话。

接下来，我们就来简单看看基于Session的后续认证方式是如何工作的。

### 3.2 使用Session：有状态的认证方式

基于Session的认证方式是一种有状态的方案，服务端会为每个身份认证成功的用户建立并保存相关session信息，同时服务端也会要求客户端在浏览器侧持久化与该Session有关少量信息，通常客户端会通过开启Cookie的方式来保存与用户Session相关的信息。

服务端保存Session有多种方式，可以在进程内存中、文件中、数据库、缓存(Redis)等，不同方式各有优缺点，比如将Session保存在内存中，最大的好处就是实现简单且速度快，但由于不能持久化，服务实例重启后就会丢失，此外当服务端有多副本时，session信息无法在多实例共享；使用关系数据库来保存session，可以方便持久化，也方便与服务端多实例用户数据共享，但数据库交互成本较大；而使用缓存(Redis)存储session信息是目前比较主流的方式，简单、安全、快速，还可以很好地适合分布式环境下session的共享。

下面是一个常见的基于cookie实现的session机制的客户端与服务端的交互示意图：

![](../../assets/077db2c5b64f5167.png)


这里也给出上述示意图的一个参考实现示例（代码仅用作演示，很多值设置并不规范和安全，不要用于生产）。

session机制的开启从用户登录开始，这个示例里的login.html与上一个示例是一样的：

```
// authn-examples/password/session/login.html
<!DOCTYPE html>
<html>
<head>
<title>登录</title>
</head>
<body>
<form action="http://server.com:8080/login" method="post">
<label>用户名:</label>
<input type="text" name="username"/>
<label>密码:</label>
<input type="password" name="password"/>
<button type="submit">登录</button>
</form>
</body>
</html>
```


服务端负责的login Handler代码如下：

```
// authn-examples/password/session/main.go
var store = sessions.NewCookieStore([]byte("session-key"))
func main() {
http.HandleFunc("/login", login)
http.HandleFunc("/calc", calc)
http.HandleFunc("/calcAdd", calcAdd)
http.ListenAndServe(":8080", nil)
}
var credentials = map[string]string{
"admin": "123456",
"test": "654321",
}
func isValid(username, password string) bool {
// 验证用户名密码
v, ok := credentials[username]
if !ok {
return false
}
if v != password {
return false
}
return true
}
func base64Encode(src string) string {
encoded := base64.StdEncoding.EncodeToString([]byte(src))
return encoded
}
func base64Decode(encoded string) string {
decoded, _ := base64.StdEncoding.DecodeString(encoded)
return string(decoded)
}
func randomStr() string {
// 生成随机数
rand.Seed(time.Now().UnixNano())
random := rand.Intn(100000)
// 格式化为05位字符串
str := fmt.Sprintf("%05d", random)
return str
}
func login(w http.ResponseWriter, r *http.Request) {
username := r.FormValue("username")
password := r.FormValue("password")
if isValid(username, password) {
session, err := store.Get(r, "server.com_"+username)
if err != nil {
fmt.Println("get session from session store error:", err)
http.Error(w, "Internal error", http.StatusInternalServerError)
}
// 设置session数据
random := randomStr()
usernameB64 := base64Encode(username + "-" + random)
session.Values["random"] = random
session.Save(r, w)
// 设置cookie
cookie := http.Cookie{Name: "server.com-session", Value: usernameB64}
http.SetCookie(w, &cookie)
// 登录成功,跳转到calc页面
http.Redirect(w, r, "/calc", http.StatusSeeOther)
} else {
http.Error(w, "Invalid username or password", http.StatusUnauthorized) // 401
}
}
```


我们使用了gorilla/sessions这个Go社区广泛使用的session库来实现服务端session的相关操作。以admin用户登录为例，当用户名和密码认证成功后，我们在session store中创建一个新的session：server.com_admin。然后生成一个随机数，将随机数存储在该session的名为”random”的key的下面。之后，让客户端设置cookie，name为server.com-session。值为username和random按特定格式组合后的base64编码值。

登录成功后，浏览器会跳到calc页面，这里我们输入两个整数，并点击”calc”按钮提交，提交动作会发送请求到calcAdd Handler中：

```
// authn-examples/password/session/main.go
func calcAdd(w http.ResponseWriter, r *http.Request) {
// 1. 获取Cookie中的Session
cookie, err := r.Cookie("server.com-session")
if err != nil {
http.Error(w, "找不到cookie，请重新登录", 401)
return
}
fmt.Printf("found cookie: %#v\n", cookie)
// 2. 获取Session对象
usernameB64 := cookie.Value
usernameWithRandom := base64Decode(usernameB64)
ss := strings.Split(usernameWithRandom, "-")
username := ss[0]
random := ss[1]
session, err := store.Get(r, "server.com_"+username)
if err != nil {
http.Error(w, "找不到session, 请重新登录", 401)
return
}
randomInSs := session.Values["random"]
if random != randomInSs {
http.Error(w, "session中信息不匹配, 请重新登录", 401)
return
}
// 3. 转换为整型参数
a, err := strconv.Atoi(r.FormValue("a"))
if err != nil {
http.Error(w, "参数错误", 400)
return
}
b, err := strconv.Atoi(r.FormValue("b"))
if err != nil {
http.Error(w, "参数错误", 400)
return
}
// 4. 计算并返回结果
result := a + b
w.Write([]byte(fmt.Sprintf("%d", result)))
}
```


calcAdd Handler会提取Cookie “server.com-session”中的值，根据值信息查找服务端本地是否存储了对应的session，并校验与session中存储的随机码是否一致。验证通过后，直接返回结算结果；否则提醒客户端重新登录。

前面说过，session是一种有状态的辅助身份认证机制，需要客户端和服务端的配合完成，一旦客户端禁用了Cookie机制，上述的示例实现就失效了。当然有读者会说，Session可以不基于Cookie来实现，可以用URL重写、隐藏表单字段、将Session ID放入URL路径等方式来实现，客户端也可以用LocalStorage等前端存储机制来替代Cookie。但无论哪种实现，这种有状态机制带来的复杂性都不低，并且在分布式环境中需要session共享和同步机制，影响了scaling。

随着微服务架构的广泛使用，无需在服务端存储额外信息、天然支持后端服务分布式多实例的无状态的连续身份认证机制受到了更多的青睐。

其实基于HTTP的无状态认证机制早已有之，最常见的莫过于Basic Auth了，接下来，我们就从Basic Auth开始，说几种无状态身份认证机制。

### 3.3 Basic Auth：最早的无状态认证方式

Basic Auth是HTTP最原始的身份验证方式，在HTTP1.0规范中就已存在，其原因是HTTP是无状态协议，每次请求都需要进行身份验证才能访问受保护资源。

Basic Auth的原理也十分简单，客户端与服务端的交互如下图：

![](https://tonybai.com/wp-content/uploads/understand-go-web-authn-by-example-7.png)


Basic Auth通过在客户端的请求报文中添加HTTP Authorization Header的形式向服务器端发送认证凭据。HTTP Authorization Header的构建通常分两步。

- 将“username:password”的组合字符串进行Base64编码，编码值记作b64Token。
- 将Authorization: Basic b64Token作为HTTP header的一个字段发送给服务器端。

服务端收到请请求后提取出Authorization字段并做Base64解码，得到username和password，然后与存储的信息作比对进行客户端身份认证。

我们来看一个与上图对应的示例的代码，先看客户端：

```
// authn-examples/password/basic/client/main.go
func main() {
client := &http.Client{}
req, _ := http.NewRequest("POST", "http://server.com:8080/", nil)
// 发送默认请求
response, err := client.Do(req)
if err != nil {
fmt.Println(err)
return
}
// 解析响应头
authHeader := response.Header.Get("WWW-Authenticate")
loginReq, _ := http.NewRequest("POST", "http://server.com:8080/login", nil)
username := "admin"
password := "123456"
// 判断认证类型
if !strings.Contains(authHeader, "Basic") {
// 不支持的认证类型
fmt.Println("Unsupported authentication type:", authHeader)
return
}
// 使用Basic Auth, 添加Basic Auth头
loginReq.SetBasicAuth(username, password)
response, err = client.Do(loginReq)
// 打印响应状态
fmt.Println(response.StatusCode)
// 打印响应包体
defer response.Body.Close()
body, err := io.ReadAll(response.Body)
if err != nil {
fmt.Println(err)
return
}
fmt.Println(string(body))
}
```


客户端的代码比较简单，并且流程与图中的交互流程是完全一样的。而服务端就是一个简单的http server，对来自客户端的带有basic auth的请求进行身份认证：

```
// authn-examples/password/basic/server/main.go
func main() {
// 创建一个基本的HTTP服务器
mux := http.NewServeMux()
username := "admin"
password := "123456"
// 针对/的handler
mux.HandleFunc("/", func(w http.ResponseWriter, req *http.Request) {
// 返回401 Unauthorized响应
w.Header().Set("WWW-Authenticate", "Basic realm=\"server.com\"")
w.WriteHeader(http.StatusUnauthorized)
})
// login handler
mux.HandleFunc("/login", func(w http.ResponseWriter, req *http.Request) {
// 从请求头中获取Basic Auth认证信息
user, pass, ok := req.BasicAuth()
if !ok {
// 认证失败
w.WriteHeader(http.StatusUnauthorized)
return
}
// 验证用户名密码
if user == username && pass == password {
// 认证成功
w.WriteHeader(http.StatusOK)
w.Write([]byte("Welcome to the protected resource!"))
} else {
// 认证失败
http.Error(w, "Invalid username or password", http.StatusUnauthorized)
}
})
// 监听8080端口
err := http.ListenAndServe(":8080", mux)
if err != nil {
log.Fatal(err)
}
}
```


采用Basic Auth身份认证方案的客户端在每个请求中都要在Header中加上Basic Auth形式的身份信息，但服务端无需像Session那样存储任何额外的信息。

不过很显然，Basic Auth这种采用明文传输身份信息的方式在安全性方面饱受诟病，为了避免在Header传输明文的安全问题，RFC 2617(以及后续更新版RFC 7616)定义了HTTP Digest身份认证方式。Digest访问认证不再明文传输密码，而是传递用hash算法处理后密码摘要，相对Basic Auth验证安全性更高。接下来，我们就来看看HTTP Digest认证方式。

### 3.4 基于HTTP Digest认证

Digest是一种HTTP摘要认证，你可以把它看作是Basic Auth的改良版本，针对Base64明文发送的风险，Digest认证把用户名和密码加盐（一个被称为Nonce的随机值作为盐值）后，再通过MD5/SHA等哈希算法取摘要放到请求的Header中发送出去。Digest的认证过程如下图：

![](https://tonybai.com/wp-content/uploads/understand-go-web-authn-by-example-8.png)


相对于Basic Auth，Digest Auth的一些值的生成过程还是略复杂的，这里给出一个示例性质的代码示例，可能不完全符合Digest规范，大家通过示例理解Digest的认证过程就可以了。

注：如要使用符合RFC 7616的Digest规范（或老版RFC 2617规范)，可以找一些第三方包，比如https://github.com/abbot/go-http-auth（只满足RFC 2617）。


```
// authn-examples/password/digest/client/main.go
func main() {
client := &http.Client{}
req, _ := http.NewRequest("POST", "http://server.com:8080/", nil)
// 发送默认请求
response, err := client.Do(req)
if err != nil {
fmt.Println(err)
return
}
// 解析响应头
authHeader := response.Header.Get("WWW-Authenticate")
loginReq, _ := http.NewRequest("POST", "http://server.com:8080/login", nil)
username := "admin"
password := "123456"
// 判断认证类型
if !strings.Contains(authHeader, "Digest") {
// 不支持的认证类型
fmt.Println("Unsupported authentication type:", authHeader)
return
}
// 使用Digest Auth
//随机数
cnonce := GenNonce()
//生成HA1
ha1 := GetHA1(username, password, cnonce)
//构建Authorization头
auth := "Digest username=\"" + username + "\", nonce=\"" + cnonce + "\", algorithm=MD5, response=\"" + GetResponse(ha1, cnonce) + "\""
loginReq.Header.Set("Authorization", auth)
response, err = client.Do(loginReq)
// 打印响应状态
fmt.Println(response.StatusCode)
// 打印响应包体
defer response.Body.Close()
body, err := io.ReadAll(response.Body)
if err != nil {
fmt.Println(err)
return
}
fmt.Println(string(body))
}
// 生成随机数
func GenNonce() string {
h := md5.New()
io.WriteString(h, fmt.Sprint(rand.Int()))
return hex.EncodeToString(h.Sum(nil))
}
// 根据用户名密码和随机数生成HA1
func GetHA1(username, password, cnonce string) string {
h := md5.New()
io.WriteString(h, username+":"+cnonce+":"+password)
return hex.EncodeToString(h.Sum(nil))
}
// 根据HA1,随机数生成response
func GetResponse(ha1, cnonce string) string {
h := md5.New()
io.WriteString(h, strings.ToUpper("md5")+":"+ha1+":"+cnonce+"::"+strings.ToUpper("md5"))
return hex.EncodeToString(h.Sum(nil))
}
```


客户端使用username、password和随机数生成摘要以及一个response码，并通过请求的头Authorization字段发给服务端。

服务端解析Authorization字段中的各个值，然后采用同样的算法算出一个新response，与请求中的response比对，如果一致，则认为认证成功：

```
// authn-examples/password/digest/server/main.go
func main() {
mux := http.NewServeMux()
password := "123456"
// 针对/的handler
mux.HandleFunc("/", func(w http.ResponseWriter, req *http.Request) {
// 返回401 Unauthorized响应
w.Header().Set("WWW-Authenticate", "Digest realm=\"server.com\"")
w.WriteHeader(http.StatusUnauthorized)
})
// login handler
mux.HandleFunc("/login", func(w http.ResponseWriter, req *http.Request) {
fmt.Println(req.Header)
//验证参数
if Verify(req, password) {
fmt.Fprintln(w, "Verify Success!")
} else {
w.WriteHeader(401)
fmt.Fprintln(w, "Verify Failed!")
}
})
// 监听8080端口
err := http.ListenAndServe(":8080", mux)
if err != nil {
log.Fatal(err)
}
}
func Verify(r *http.Request, password string) bool {
auth := r.Header.Get("Authorization")
params := strings.Split(auth, ",")
var username, cnonce, response string
for _, p := range params {
p := strings.Trim(p, " ")
kv := strings.Split(p, "=")
if kv[0] == "Digest username" {
username = strings.Trim(kv[1], "\"")
}
if kv[0] == "nonce" {
cnonce = strings.Trim(kv[1], "\"")
}
if kv[0] == "response" {
response = strings.Trim(kv[1], "\"")
}
}
if username == "" {
return false
}
//根据用户名密码及随机数生成HA1
ha1 := GetHA1(username, password, cnonce)
//自己生成response与请求中response对比
return response == GetResponse(ha1, cnonce)
}
```


虽然实现了无状态，安全性也高于Basic Auth，但Digest方式的用户体验依然有限：每次向服务端发送请求，客户端都要进行一次复杂计算，服务端也要再做一次相同的验算和比对。

那么是否有一种体验更为良好的无状态身份认证方式呢？我们接下来看看基于Token的认证方式。

## 4. 无状态：基于Token的认证

基于Token的认证方式的备受青睐得益于Web领域前后端分离架构的发展以及微服务架构的流行，在API调用和网站间需要轻量级的认证机制来传递用户信息。Token认证机制正好满足这一需求，而[JWT(JSON Web Token)](https://jwt.io)是目前Token格式标准中使用最广的一种。

### 4.1 JWT原理

JWT由头部(Header)、载荷(Payload)和签名(Signature)三部分组成，三部分之间用圆点连接，其形式如下：

```
xxxxx.yyyyy.zzzzz
```


一个真实的JWT token的例子如下面来自[jwt.io](https://jwt.io/)站点的截图)：

![](../../assets/c2685a37ddd4cfe7.png)


JWT token的生成过程也非常清晰，下图展示了上述截图中jwt token的生成过程：

![](../../assets/d9729d7ac46107e3.png)


如果你不想依赖第三方库，也可以自己实现生成token的函数，下面是一个示例：

```
// authn-examples/jwt/scratch/main.go
package main
import (
"crypto/hmac"
"crypto/sha256"
"encoding/base64"
"encoding/json"
"fmt"
)
type Header struct {
Alg string `json:"alg"`
Typ string `json:"typ"`
}
type Claims struct {
Sub string `json:"sub"`
Name string `json:"name"`
Iat int64 `json:"iat"`
}
// GenerateToken：不依赖第三方库的JWT生成实现
func GenerateToken(claims *Claims, key string) (string, error) {
header, _ := json.Marshal(Header{
Alg: "HS256",
Typ: "JWT",
})
// 序列化Payload
payload, err := json.Marshal(claims)
if err != nil {
return "", err
}
// 拼接成JWT字符串
headerEncoded := base64.RawURLEncoding.EncodeToString(header)
payloadEncoded := base64.RawURLEncoding.EncodeToString([]byte(payload))
encodedToSign := headerEncoded + "." + payloadEncoded
// 使用HMAC+SHA256签名
hash := hmac.New(sha256.New, []byte(key))
hash.Write([]byte(encodedToSign))
sig := hash.Sum(nil)
sigEncoded := base64.RawURLEncoding.EncodeToString(sig)
var token string
token += headerEncoded
token += "."
token += payloadEncoded
token += "."
token += sigEncoded
return token, nil
}
func main() {
var claims = &Claims{
Sub: "1234567890",
Name: "John Doe",
Iat: 1516239022,
}
result, _ := GenerateToken(claims, "iamtonybai")
fmt.Println(result)
}
```


对照着上面图示的流程，理解这个示例非常容易。当然jwt.io官方也维护了一个使用简单且灵活性更好的Go module：[golang-jwt/jwt](https://github.com/golang-jwt/jwt)，用这个go module生成上述token的示例代码如下：

```
// authn-examples/jwt/golang-jwt/main.go
import (
"fmt"
"time"
jwt "github.com/golang-jwt/jwt/v5"
)
type MyCustomClaims struct {
Sub string `json:"sub"`
Name string `json:"name"`
jwt.RegisteredClaims // use its Subject and IssuedAt
}
func main() {
mySigningKey := []byte("iamtonybai")
// Create claims with multiple fields populated
claims := MyCustomClaims{
Name: "John Doe",
Sub: "1234567890",
RegisteredClaims: jwt.RegisteredClaims{
IssuedAt: jwt.NewNumericDate(time.Unix(1516239022, 0)), // 1516239022
},
}
token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
ss, _ := token.SignedString(mySigningKey)
fmt.Println(ss)
_, err := verifyToken(ss, "iamtonybai")
if err != nil {
fmt.Println("invalid token:", err)
return
}
fmt.Println("valid token")
}
```


这段代码中还包含了一个对jwt token验证合法性的函数verifyToken，服务端每次收到客户端请求中携带的token时，都可以使用verifyToken来验证token是否合法，下面是verifyToken的实现逻辑：

```
// authn-examples/jwt/golang-jwt/main.go
// verifyToken 验证JWT函数
func verifyToken(tokenString, key string) (*jwt.Token, error) {
// 解析Token
token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
return []byte(key), nil
})
if err != nil {
return nil, err
}
// 验证签名
if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
return nil, jwt.ErrSignatureInvalid
}
return token, nil
}
```


服务端验证token的逻辑是先解析token，得到header、payload对应的base64UrlEncoded后的结果，然后用key重新生成签名，对比生成的签名与token携带的签名是否一致。

那么在Web应用中如何实现基于jwt token的身份认证呢？我们继续往下看。

### 4.2 使用JWT token做身份认证

在前面讲解Basic Auth、Digest Auth时，Basic Auth、Digest等服务端认证方式利用了HTTP Header的Authorization字段，基于JWT token的认证也是基于Authorization字段，只不过前缀从Basic、Digest换成了**Bearer**：

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2OTc4NjE5MzIsInVzZXJuYW1lIjoiYWRtaW4ifQ.go6NhfmYPZbtHEuJ1oULG890neo0yVdtFJwfAvHhxyE
```


基于JWT token的身份认证方式的客户端与服务端的交互流程如下图：

![](../../assets/e8e2dc940958ca8f.png)


在这幅示意图中，客户端先用basic auth方式登录服务端，服务端验证通过后，在登录应答中写入一个jwt token作为后续客户端访问服务端其他功能的依据。客户端从登录应答的包体中解析出jwt token后，可以将该token存放在LocalStorage中，然后在后续的发向该服务端的所有请求中都带上这个jwt token。服务端对这些请求都会校验其携带的jwt token，只有验证通过的请求才能被正确处理。

下面来看看对应示意图的示例源码，先来看一下客户端：

```
// authn-examples/jwt-authn/client/main.go
func main() {
client := &http.Client{}
req, _ := http.NewRequest("POST", "http://server.com:8080/", nil)
// 发送默认请求
response, err := client.Do(req)
if err != nil {
fmt.Println(err)
return
}
// 解析响应头
authHeader := response.Header.Get("WWW-Authenticate")
loginReq, _ := http.NewRequest("POST", "http://server.com:8080/login", nil)
username := "admin"
password := "123456"
// 判断认证类型
if !strings.Contains(authHeader, "Basic") {
// 不支持的认证类型
fmt.Println("Unsupported authentication type:", authHeader)
return
}
// 使用Basic Auth, 添加Basic Auth头
loginReq.SetBasicAuth(username, password)
response, err = client.Do(loginReq)
fmt.Println(response.StatusCode)
// 从响应包体中获取服务端分配的jwt token
defer response.Body.Close()
body, err := io.ReadAll(response.Body)
if err != nil {
fmt.Println(err)
return
}
token := string(body)
fmt.Println("token=", token)
// 基于token访问服务端其他功能
apiReq, _ := http.NewRequest("POST", "http://server.com:8080/calc", nil)
apiReq.Header.Set("Authorization", "Bearer "+token)
response, err = client.Do(apiReq)
fmt.Println(response.StatusCode)
defer response.Body.Close()
body, err = io.ReadAll(response.Body)
if err != nil {
fmt.Println(err)
return
}
fmt.Println(string(body))
}
```


客户端的操作流程与示意图一样，先用basic auth登录server，通过验证后，拿到服务端生成的token。后续到该服务端的所有请求只需在Header中带上token即可。

服务端的代码如下：

```
// authn-examples/jwt-authn/server/main.go
func main() {
// 创建一个基本的HTTP服务器
mux := http.NewServeMux()
username := "admin"
password := "123456"
key := "iamtonybai"
// 针对/的handler
mux.HandleFunc("/", func(w http.ResponseWriter, req *http.Request) {
// 返回401 Unauthorized响应
w.Header().Set("WWW-Authenticate", "Basic realm=\"server.com\"")
w.WriteHeader(http.StatusUnauthorized)
})
// login handler
mux.HandleFunc("/login", func(w http.ResponseWriter, req *http.Request) {
// 从请求头中获取Basic Auth认证信息
user, pass, ok := req.BasicAuth()
if !ok {
// 认证失败
w.WriteHeader(http.StatusUnauthorized)
return
}
// 验证用户名密码
if user == username && pass == password {
// 认证成功，生成token
token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
"username": username,
"iat": jwt.NewNumericDate(time.Now().Add(time.Hour * 24)),
})
signedToken, _ := token.SignedString([]byte(key))
w.Write([]byte(signedToken))
} else {
// 认证失败
http.Error(w, "Invalid username or password", http.StatusUnauthorized)
}
})
// calc handler
mux.HandleFunc("/calc", func(w http.ResponseWriter, req *http.Request) {
// 读取并校验jwt token
token := req.Header.Get("Authorization")[len("Bearer "):]
fmt.Println(token)
if _, err := verifyToken(token, key); err != nil {
// 认证失败
http.Error(w, "Invalid token", http.StatusUnauthorized)
return
}
w.Write([]byte("invoke calc ok"))
})
// 监听8080端口
err := http.ListenAndServe(":8080", mux)
if err != nil {
log.Fatal(err)
}
}
```


我们看到，除了在login handler中使用basic auth做用户密码验证外，其他功能handler(如calc)中都使用token进行身份验证。

与传统会话式(session)认证相比，JWT是无状态的，更适用于分布式微服务架构。与Basic auth和digest相比，jwt在使用体验上又领先一筹。凭借其无需在服务端保存会话状态、天生适合分布式架构、令牌内容可以自定义扩展等优势，现阶段，jwt已广泛应用于以下场合：

- 前后端分离的Web应用和API认证
- 跨域单点登录(SSO)
- 微服务架构下服务间认证
- 无状态和移动应用认证

不过JWT认证方式也有不足，比如：客户端要承担令牌存储成本、如果令牌泄露未及时失效可能被滥用等。

讲到这里，从基本的用户名密码认证，到加上密码散列的Digest认证，再到应用会话管理的Session认证，以及基于令牌的JWT认证，我们见证了认证机制的不断进步和发展。

这些方法主要依赖账号密码这单一要素，提供了不同程度的安全性。但是随着互联网的快速发展，开发人员也在考虑改善用户名密码这种方式的使用体验，一些一次性密码认证方式便走入了我们的生活。接下来我们就来简单说一下一次性密码验证。

## 5. 基于一次性密码验证

一次性密码（One Time Password, OTP）是一种只能使用一次的密码，它在使用后立即失效。OTP生成密码的算法基于时间，在很短的时间内(一般分钟内或更短时间内)只能使用一次；每次验证都需要生成和输入新的密码，不能重复使用。

一次性密码的优势主要有以下几点：

- 安全性高：一次性密码只能使用一次，因此即使攻击者获得了密码，也无法重复使用。
- 易用性强：一次性密码通常是数字或字母组成的短语，易于记忆和输入。
- 成本低：一次性密码的生成和验证成本相对较低。

信息论已经从理论上证明了：一次性密码本是无条件安全的，在理论上是无法破译的。不过现实中，还没有一种理想的一次性密码，大多数一次性密码还处于身份认证的辅助地位，多作为第二要素。

短信验证码就是一种我们生活中常见的一次性密码，它是利用移动运营商的短信通道传输的一次性密码。短信验证码通常由6位数字组成，有效期为几分钟，并且只能使用一次，通过短信发送给用户，非常方便用户使用，用户无需有记住密码的烦恼。

短信验证码的工作流程如下：

- 客户端发起认证请求，如登录或注册；
- 服务器生成6位随机数字作为验证码，通过文本短信发送到用户注册的手机号；
- 用户接收短信并输入验证码进行验证；
- 服务器通过时间戳验证此验证码是否有效(一般在5分钟内)。
- 验证码只能使用一次，服务器会将此条记录标记为使用。

短信验证码的优势是**方便快捷**。目前国内大多数主流Web应用都支持手机验证码登录。短信验证码通常用于以下场景：

- 用户注册
- 用户登录
- 支付或交易
- 辅助密码找回等

不过手机验证码这种一次性密码的安全性相对较低，因为短信可以被截获，攻击者可以通过截获短信来获取验证码。

除短信验证码外，还有其他常见的OTP实现形式:

- 手机应用软件OTP：使用专门的手机APP软件生成OTP码，如Google Authenticator、Microsoft Authenticator等。
- 电子邮件OTP：类似短信验证码，但通过邮件发送6-8位数字验证码到用户注册的邮箱。
- 语音验证码OTP：服务端调用第三方语音平台，使用文本到语音功能给用户自动拨打认证电话，提示验证码。

总体来说，OTP越来越多地被用到用户身份认证上来，随着以后技术的进步，其应用的广度和深度会进一步扩大，安全性也会得到进一步提升。基于传统密码的认证方式早晚会被扔到历史的旧物箱中。一些大厂，如Google都在研究替代传统密码的技术，比如[Passkey](https://blog.google/technology/safety-security/the-beginning-of-the-end-of-the-password/)等，一些Web标准组织也在做无密码认证的规范，比如[WebAuthn](https://webauthn.guide)等。

## 6. 小结

就写到这里吧，篇幅有些长了，关于OAuth、OpenID等身份认证技术就不在这里写了，后续找机会单独梳理。

本文我们介绍了多种Web应用的身份认证技术方案，各种认证技术会依据对安全性、使用性和扩展性的不同需求而存在和发展。了解每种技术的原理和优劣势，可帮助我们更好地选择适合的方案。

首次梳理这么多Web应用身份认证的资料，可能有些描述并不完全正确，欢迎指正。在撰写本文时，大语言模型帮助编写部分文字素材和代码。

本文示例所涉及的Go源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/authn-examples)下载。

## 7. 参考资料

[《API安全实战》](https://book.douban.com/subject/36039150/)– https://book.douban.com/subject/36039150/[《API安全技术与实战》](https://book.douban.com/subject/35429043/)– https://book.douban.com/subject/35429043/[《深入浅出密码学》](https://book.douban.com/subject/36179106/)– https://book.douban.com/subject/36179106/[Web Authentication Methods Compared](https://testdriven.io/blog/web-authentication-methods)– https://testdriven.io/blog/web-authentication-methods/[认证：系统如何正确分辨操作用户的真实身份？](https://time.geekbang.org/column/article/329954)– https://time.geekbang.org/column/article/329954[如何实现零信任网络下安全的服务访问？](https://time.geekbang.org/column/article/345593)– https://time.geekbang.org/column/article/345593[凭证：系统如何保证与用户之间的承诺是准确完整且不可抵赖的？](https://time.geekbang.org/column/article/333272)– https://time.geekbang.org/column/article/333272[谷歌正推出Passkey，密码将成历史](https://blog.google/technology/safety-security/the-beginning-of-the-end-of-the-password/)– https://blog.google/technology/safety-security/the-beginning-of-the-end-of-the-password/[What is authentication?](https://www.microsoft.com/zh-cn/security/business/security-101/what-is-authentication)– https://www.microsoft.com/zh-cn/security/business/security-101/what-is-authentication[Authentication(wikipedia)](https://en.wikipedia.org/wiki/Authentication.html)– https://en.wikipedia.org/wiki/Authentication.html[RFC 7617: The ‘Basic’ HTTP Authentication Scheme](https://datatracker.ietf.org/doc/html/rfc7617)– https://datatracker.ietf.org/doc/html/rfc7617[RFC 7616: HTTP Digest Access Authentication](https://datatracker.ietf.org/doc/html/rfc7616)– https://datatracker.ietf.org/doc/html/rfc7616[RFC 7519: JSON Web Token(JWT)](https://datatracker.ietf.org/doc/html/rfc7519)– https://datatracker.ietf.org/doc/html/rfc7519[Introduction to JSON Web Tokens](https://jwt.io/introduction)– https://jwt.io/introduction

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