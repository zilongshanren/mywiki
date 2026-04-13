---
title: htmx：Gopher走向全栈的完美搭档？
url: https://tonybai.com/2024/09/20/htmx-gopher-perfect-partner-for-full-stack/
published: '2024-09-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# htmx：Gopher走向全栈的完美搭档？

![](../../assets/5104ec9ead8fc74d.png)


[本文永久链接](https://tonybai.com/2024/09/20/htmx-gopher-perfect-partner-for-full-stack) – https://tonybai.com/2024/09/20/htmx-gopher-perfect-partner-for-full-stack

在传统的Web开发领域，前端和后端开发通常被明确划分。前端主要负责用户界面的交互和视觉呈现，运用HTML、CSS和JavaScript等技术；后端则专注于服务器逻辑、数据库管理和核心功能实现，常用Go、Java、PHP、Ruby等语言。

然而，随着技术的不断演进和开发流程的优化，全栈开发逐渐成为一种趋势。全栈开发者能够在项目的不同阶段灵活转换角色，有效降低沟通成本和缩短开发周期。他们对系统的整体架构和工作原理有更深入的理解，从而能更高效地解决问题。此外，全栈技能也使得开发者在就业市场上更具竞争力，能够承担更多样化的职责。

尽管如此，对于许多专注后端的工程师（包括众多Gopher）来说，前端开发仍然是一个不小的挑战。它不仅要求熟悉JavaScript等语言，还需要理解复杂的前端框架和工具链。这使得不少后端开发者在面对全栈开发时感到力不从心。

幸运的是，技术的进步为我们提供了更简单、高效的开发途径。Go语言以其简洁和高效著称，而htmx库则通过HTML属性实现丰富的前端交互。将两者结合，开发者可以在无需深入学习JavaScript的情况下，轻松实现全栈开发。这种组合不仅能够显著提升开发效率，还能充分利用服务器端渲染（SSR）的优势，在性能和用户体验方面取得显著提升。

那么，htmx是否真的是Gopher走向全栈的完美搭档呢？在本文中，我们就将探讨一下这个问题，介绍一下htmx的核心理念和工作原理，并结合代码示例和使用场景，详细分析Go和htmx如何协同工作。至于Go+htmx究竟有多能打，相信在本文最后，你会得出自己的评价！

## 1. htmx：为简化前端开发而生

传统的前端开发通常依赖于JavaScript框架，例如React、Vue或Angular。这些框架虽然功能强大，但往往伴随着高昂的学习成本和复杂的开发流程。对于那些主要从事后端开发的程序员来说，学习和掌握这些框架不仅需要花费大量时间，还需要深入理解前端生态系统中的各种概念和工具链。这种学习曲线和开发复杂性成为了许多后端开发者的阻碍，同时也成为了阻碍Go开发者迈向全栈的绊脚石。

htmx的诞生正是为了简化前端开发，特别是对于那些不愿意或没有时间深入学习JavaScript的开发者。

htmx的核心理念是通过扩展HTML，使其具备更强大的功能，从而减少对JavaScript的依赖。它遵循了”HTML优先”的设计原则，允许开发者直接在HTML元素中添加特殊的属性来定义与服务器交互的行为，比如动态加载、表单处理、局部刷新等，从而实现动态交互，而无需编写任何JavaScript代码。可以说，htmx的出现为后端开发者(包括Gopher)提供了一种新的选择，使得Web应用的开发变得更加直观和简便。

不过，htmx自身却是一个轻量级的JavaScript库，这与Go的设计哲学有些“异曲同工”，即**简单留给大家，复杂留给自己**。作为js库，它提供了一组简洁而强大的API，通过设置HTML属性，开发者就可以实现多种交互功能。以下是htmx的一些核心特性：

- 请求类型（hx-get、hx-post、hx-put和hx-delete）

通过指定请求类型，htmx可以在用户触发事件时向服务器发送请求，并处理响应。

- 目标更新（hx-target）

支持指定服务器响应数据要插入的DOM元素，支持部分页面更新而无需刷新整个页面。

- 触发条件（hx-trigger）

支持定义请求触发的条件，例如点击、鼠标悬停、表单提交等事件。

- 交换方式（hx-swap）

支持定义响应内容插入DOM的方式，可以选择替换、插入、删除等操作。

这些API的设计目标是让开发者能够通过声明式的方式来实现前端逻辑，而不必依赖JavaScript代码，以简化开发过程。

由于几乎无需后端开发者写JavaScript，HTMX很容易被认为是**SSR（服务器端渲染）**的一种实现。它们看似很相似，但它们的思路并不完全一致。SSR的渲染过程是在服务器上完成的，服务器生成整个HTML页面的内容，并将其发送给客户端。客户端接收到完整的HTML直接展示给用户。这也使得SSR通常可以提供更快的初始加载体验，因为用户可以立即看到页面内容，而不必等待JavaScript加载和执行。此外，由于HTML内容在服务器上渲染，搜索引擎更容易抓取和索引内容。

而HTMX的大部分渲染也是在服务端完成的，但它支持在客户端通过AJAX请求动态更新页面的某些部分，而不需要重新加载整个页面，只是它是通过简单的HTML属性(外加自身js)实现这些功能的，而无需用户手工写JavaScript实现。HTMX还使得页面能够更具交互性，用户可以在不离开当前页面的情况下与应用程序进行交互。

因此，htmx可以视为一种结合SSR和**局部CSR(客户端渲染)**的技术，它让你通过服务器端渲染HTML，同时在客户端实现灵活的动态交互功能。这使得开发者能够在SSR提供的性能优势和SEO友好性基础上，提升用户体验而不必依赖完整的客户端框架。

虽然保留了CSR，但与传统的JavaScript框架（如 React、Vue、Angular）相比，htmx非常轻量，体积非常小，以撰写本文时的[最新2.0.2版本htmx](https://unpkg.com/browse/htmx.org@2.0.2/dist/)为例，它的js包大小如下，压缩版才10几k：

![](../../assets/ac7e513738969308.png)


此外，传统框架虽然功能强大，但往往需要复杂的配置和较高的学习成本，尤其对于习惯后端开发的开发者来说，更是如此。而使用HTMX，只需掌握HTML和少量的htmx API即可开始开发，适合后端开发者快速上手。

说了这么多htmx的优点，那基于htmx的开发究竟是怎样的呢？下面我们就以htmx的几个核心特性为例，看看如何基于htmx开发简单web应用。

## 2. htmx的基本用法

在前面我们了解了htmx的几个核心特性，包括请求类型、目标更新等。下面我们就针对这些核心特性，举几个例子，大家初步了解一下基于htmx的开发web应用的流程。

我们先从请求类型开始，了解一下基于htmx如何向后端发起POST/GET/PUT/DELETE等请求。

### 2.1 示例1：请求类型

在这第一个示例中，我们使用Go语言创建一个简单的服务器，并使用htmx在前端实现不同类型的请求。下面是我们定义的html模板，其中包含了htmx的自定义属性：

```
// go-htmx/demo1/index.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HTMX Go Example</title>
<script src="https://unpkg.com/htmx.org@2.0.2"></script>
<style>
.row {
margin-bottom: 10px;
}
button {
width: 120px;
margin-right: 10px;
}
.result {
display: inline-block;
width: 300px;
border: 1px solid #ccc;
padding: 5px;
min-height: 20px;
}
</style>
</head>
<body>
<h1>HTMX Request Types Demo</h1>
<div class="row">
<button hx-get="/api/get" hx-target="#get-result">GET Request</button>
<span id="get-result" class="result"></span>
</div>
<div class="row">
<button hx-post="/api/post" hx-target="#post-result">POST Request</button>
<span id="post-result" class="result"></span>
</div>
<div class="row">
<button hx-put="/api/put" hx-target="#put-result">PUT Request</button>
<span id="put-result" class="result"></span>
</div>
<div class="row">
<button hx-delete="/api/delete" hx-target="#delete-result">DELETE Request</button>
<span id="delete-result" class="result"></span>
</div>
</body>
</html>
```


在这个HTML模板文件中包含了四个按钮，每个按钮对应一种http请求类型（GET、POST、PUT、DELETE），具体的实现方式是每个按钮都使用了相应的htmx属性（hx-get、hx-post、hx-put、hx-delete）来指定请求类型和目标URL。此外，所有按钮都使用了hx-target来设置服务器的响应将被显示的元素id。以get请求button为例，响应的值将被放到id为get-result的span中。

对应的Go后端程序就非常简单了，下面是代码摘录：

```
// go-htmx/demo1/main.go
package main
import (
"fmt"
"net/http"
"os"
"path/filepath"
)
func main() {
http.HandleFunc("/", handleIndex)
http.HandleFunc("/api/get", handleGet)
http.HandleFunc("/api/post", handlePost)
http.HandleFunc("/api/put", handlePut)
http.HandleFunc("/api/delete", handleDelete)
fmt.Println("Server is running on http://localhost:8080")
http.ListenAndServe(":8080", nil)
}
func handleIndex(w http.ResponseWriter, r *http.Request) {
currentDir, _ := os.Getwd()
filePath := filepath.Join(currentDir, "index.html")
http.ServeFile(w, r, filePath)
}
func handleGet(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "Received a GET request")
}
func handlePost(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "Received a POST request")
}
func handlePut(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "Received a PUT request")
}
func handleDelete(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "Received a DELETE request")
}
```


运行该server后，用浏览器打开localhost:8080，我们将看到下面页面：

![](../../assets/7757af8b49be98a4.png)


逐一点击各个Button，htmx会将从服务器收到的响应内容放入对应的span中：

![](../../assets/ae9794d43b838322.png)


### 2.2 示例2：触发条件

在这个示例2中，我们将基于htmx实现对各种触发条件的响应与处理，htmx提供了hx-trigger属性来应对这些不同的事件触发，包括点击、鼠标悬停和表单提交等。我们看下面html模板代码：

```
// go-htmx/demo2/index.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HTMX Trigger Demo</title>
<script src="https://unpkg.com/htmx.org@2.0.2"></script>
<style>
.demo-section {
margin-bottom: 20px;
padding: 10px;
border: 1px solid #ccc;
}
.result {
margin-top: 10px;
padding: 5px;
background-color: #f0f0f0;
min-height: 20px;
}
</style>
</head>
<body>
<h1>HTMX Trigger Demo</h1>
<div class="demo-section">
<h2>Click Trigger</h2>
<button hx-get="/api/click" hx-trigger="click" hx-target="#click-result">
Click me
</button>
<div id="click-result" class="result"></div>
</div>
<div class="demo-section">
<h2>Hover Trigger</h2>
<div hx-get="/api/hover" hx-trigger="mouseenter" hx-target="#hover-result" style="display: inline-block; padding: 10px; background-color: #e0e0e0;">
Hover over me
</div>
<div id="hover-result" class="result"></div>
</div>
<div class="demo-section">
<h2>Form Submit Trigger</h2>
<form hx-post="/api/submit" hx-trigger="submit" hx-target="#form-result">
<input type="text" name="message" placeholder="Enter a message">
<button type="submit">Submit</button>
</form>
<div id="form-result" class="result"></div>
</div>
<div class="demo-section">
<h2>Custom Delay Trigger</h2>
<input type="text" name="search"
hx-get="/api/search"
hx-trigger="keyup changed delay:500ms"
hx-target="#search-result"
placeholder="Type to search...">
<div id="search-result" class="result"></div>
</div>
</body>
</html>
```


通过模板代码，我们可以看到hx-trigger 的多种用法：

- 点击触发（Click Trigger）：使用 hx-trigger=”click”，当按钮被点击时触发请求。
- 悬停触发（Hover Trigger）：使用 hx-trigger=”mouseenter”，当鼠标悬停在元素上时触发请求。
- 表单提交触发（Form Submit Trigger）：使用 hx-trigger=”submit”，当表单提交时触发请求。
- 自定义延迟触发（Custom Delay Trigger）：使用 hx-trigger=”keyup changed delay:500ms”，在输入框中输入时，等待500毫秒后触发请求。这对于实现搜索建议等功能很有用。

下面是该示例的后端go代码，逻辑非常简单，针对每个事件调用，简单返回一个字符串：

```
// go-htmx/demo2/main.go
... ...
func main() {
http.HandleFunc("/", handleIndex)
http.HandleFunc("/api/click", handleClick)
http.HandleFunc("/api/hover", handleHover)
http.HandleFunc("/api/submit", handleSubmit)
http.HandleFunc("/api/search", handleSearch)
fmt.Println("Server is running on http://localhost:8080")
http.ListenAndServe(":8080", nil)
}
func handleIndex(w http.ResponseWriter, r *http.Request) {
currentDir, _ := os.Getwd()
filePath := filepath.Join(currentDir, "index.html")
http.ServeFile(w, r, filePath)
}
func handleClick(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "Button was clicked!")
}
func handleHover(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "You hovered over the element!")
}
func handleSubmit(w http.ResponseWriter, r *http.Request) {
message := r.FormValue("message")
fmt.Fprintf(w, "Form submitted with message: %s", message)
}
func handleSearch(w http.ResponseWriter, r *http.Request) {
query := r.URL.Query().Get("search")
fmt.Fprintf(w, "Searching for: %s", query)
}
```


运行该server后，用浏览器打开localhost:8080，我们将看到下面页面：

![](../../assets/5de54e1d93a8d1e9.png)


接下来，我们可以尝试点击按钮、悬停在元素上、提交表单和在搜索框中输入，看看每个操作如何触发HTMX 请求并更新页面的相应部分，下面是触发后的结果：

![](../../assets/efb37abcd1b19887.png)


### 2.3 示例3：交换方式

在示例3中，我们将展示如何使用htmx的hx-swap属性实现不同的内容更新方式，包括替换、插入和删除操作，其中还包含多种替换方式。下面是html模板：

```
// go-htmx/demo3/index.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HTMX Swap Demo - All Attributes</title>
<script src="https://unpkg.com/htmx.org@2.0.2"></script>
<style>
.demo-section {
margin-bottom: 20px;
padding: 10px;
border: 1px solid #ccc;
}
.content-box {
margin-top: 10px;
padding: 10px;
border: 1px solid #ddd;
min-height: 50px;
}
.item {
margin: 5px 0;
padding: 5px;
background-color: #f0f0f0;
}
</style>
</head>
<body>
<h1>HTMX Swap Demo - All Attributes</h1>
<div class="demo-section">
<h2>innerHTML (Default)</h2>
<button hx-get="/api/swap/inner" hx-target="#inner-content">
Swap innerHTML
</button>
<div id="inner-content" class="content-box">
<p>This is the original content. The entire inner HTML will be replaced.</p>
</div>
</div>
<div class="demo-section">
<h2>outerHTML</h2>
<button hx-get="/api/swap/outer" hx-target="#outer-content" hx-swap="outerHTML">
Swap outerHTML
</button>
<div id="outer-content" class="content-box">
<p>This entire div will be replaced, including its container.</p>
</div>
</div>
<div class="demo-section">
<h2>textContent</h2>
<button hx-get="/api/swap/text" hx-target="#text-content" hx-swap="textContent">
Swap textContent
</button>
<div id="text-content" class="content-box">
<p>This <strong>text</strong> will be replaced, but HTML tags will be treated as plain text.</p>
</div>
</div>
<div class="demo-section">
<h2>beforebegin</h2>
<button hx-get="/api/swap/before" hx-target="#before-content" hx-swap="beforebegin">
Insert before
</button>
<div id="before-content" class="content-box">
<p>New content will be inserted before this div.</p>
</div>
</div>
<div class="demo-section">
<h2>afterbegin</h2>
<button hx-get="/api/swap/afterbegin" hx-target="#afterbegin-content" hx-swap="afterbegin">
Insert at beginning
</button>
<div id="afterbegin-content" class="content-box">
<p>New content will be inserted at the beginning of this div, before this paragraph.</p>
</div>
</div>
<div class="demo-section">
<h2>beforeend</h2>
<button hx-get="/api/swap/beforeend" hx-target="#beforeend-content" hx-swap="beforeend">
Insert at end
</button>
<div id="beforeend-content" class="content-box">
<p>New content will be inserted at the end of this div, after this paragraph.</p>
</div>
</div>
<div class="demo-section">
<h2>afterend</h2>
<button hx-get="/api/swap/after" hx-target="#after-content" hx-swap="afterend">
Insert after
</button>
<div id="after-content" class="content-box">
<p>New content will be inserted after this div.</p>
</div>
</div>
<div class="demo-section">
<h2>delete</h2>
<button hx-get="/api/swap/delete" hx-target="#delete-content" hx-swap="delete">
Delete content
</button>
<div id="delete-content" class="content-box">
<p>This content will be deleted when the button is clicked.</p>
</div>
</div>
</body>
</html>
```


这个示例略复杂，它涵盖了hx-swap的所有属性：

- innerHTML（默认）：替换目标元素的内部HTML。
- outerHTML：用响应替换整个目标元素。
- textContent：替换目标元素的文本内容，不解析HTML。
- beforebegin：在目标元素之前插入响应。
- afterbegin：在目标元素的第一个子元素之前插入响应。
- beforeend：在目标元素的最后一个子元素之后插入响应。
- afterend：在目标元素之后插入响应。
- delete：删除目标元素，忽略响应内容。

为了配合这个演示，我们编写了一个简单的go后端程序：

```
// go-htmx/demo3/main.go
... ...
func main() {
http.HandleFunc("/", handleIndex)
http.HandleFunc("/api/swap/inner", handleInner)
http.HandleFunc("/api/swap/outer", handleOuter)
http.HandleFunc("/api/swap/text", handleText)
http.HandleFunc("/api/swap/before", handleBefore)
http.HandleFunc("/api/swap/afterbegin", handleAfterBegin)
http.HandleFunc("/api/swap/beforeend", handleBeforeEnd)
http.HandleFunc("/api/swap/after", handleAfter)
http.HandleFunc("/api/swap/delete", handleDelete)
fmt.Println("Server is running on http://localhost:8080")
http.ListenAndServe(":8080", nil)
}
func handleIndex(w http.ResponseWriter, r *http.Request) {
currentDir, _ := os.Getwd()
filePath := filepath.Join(currentDir, "index.html")
http.ServeFile(w, r, filePath)
}
func handleInner(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "<p>This content replaced the inner HTML at %s</p>", time.Now().Format(time.RFC1123))
}
func handleOuter(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "<div id=\"outer-content\" class=\"content-box\"><p>This div replaced the entire outer HTML at %s</p></div>", time.Now().Format(time.RFC1123))
}
func handleText(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "This replaced the text content at %s. <strong>HTML tags</strong> are not parsed.", time.Now().Format(time.RFC1123))
}
func handleBefore(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "<p class=\"item\">This content was inserted before the target div at %s</p>", time.Now().Format(time.RFC1123))
}
func handleAfterBegin(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "<p class=\"item\">This content was inserted at the beginning of the target div at %s</p>", time.Now().Format(time.RFC1123))
}
func handleBeforeEnd(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "<p class=\"item\">This content was inserted at the end of the target div at %s</p>", time.Now().Format(time.RFC1123))
}
func handleAfter(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "<p class=\"item\">This content was inserted after the target div at %s</p>", time.Now().Format(time.RFC1123))
}
func handleDelete(w http.ResponseWriter, r *http.Request) {
// For delete, we don't need to send any content back
w.WriteHeader(http.StatusOK)
}
```


运行该server后，用浏览器打开localhost:8080，你应该能看到一个包含八个不同部分的页面，每个部分演示了hx-swap的一种属性。你可以点击每个部分的按钮，观察内容如何以不同的方式更新或变化。这个综合示例展示了hx-swap的强大功能和灵活性，让你可以精确控制如何更新页面的不同部分。下面是你可以看到的效果呈现：

![](../../assets/77567e4897d0416a.png)


![](../../assets/d498b9bd871bc4b5.png)


![](../../assets/67b80dd69df2defe.png)


以上就是htmx核心属性的用法，基于这些核心属性，我们可以实现更多更为复杂和高级的场景功能。在下一节，我们会举两个复杂一些的示例，供大家参考。

## 3. 高级用法

### 3.1 基于token的身份认证

在使用HTMX作为前端与后端进行交互时，通常会涉及到[用户身份认证](https://tonybai.com/2023/10/23/understand-go-web-authn-by-example/)及[鉴权](https://tonybai.com/2023/11/04/understand-go-web-authz-by-example)，其中一个常见场景是通过前端获取的Token（如JWT）去访问后端的受保护的API。下面我们看看使用HTMX该如何实现这一常见功能。

下面是网站首页的html模板，包含用户登录的Form：

```
// go-htmx/demo4/index.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HTMX Auth Example - Login</title>
<script src="https://unpkg.com/htmx.org@2.0.2"></script>
<script>
htmx.on('htmx:afterRequest', function(event) {
if (event.detail.elt.id === 'login-form') {
var xhr = event.detail.xhr;
if (xhr.status === 200) {
var response = JSON.parse(xhr.responseText);
if (response.success) {
localStorage.setItem('auth_token', response.token);
window.location.href = response.redirect;
} else {
document.getElementById('message').innerText = response.message;
}
} else {
document.getElementById('message').innerText = "An error occurred. Please try again.";
}
}
});
</script>
</head>
<body>
<h1>HTMX Auth Example - Login</h1>
<form id="login-form" hx-post="/login" hx-target="#message">
<label for="username">Username:</label>
<input type="text" id="username" name="username" required><br><br>
<label for="password">Password:</label>
<input type="password" id="password" name="password" required><br><br>
<button type="submit">Login</button>
</form>
<div id="message"></div>
</body>
</html>
```


这个代码片段结合了HTMX和JavaScript，处理登录表单的提交，以及登录成功后将令牌（Token）存储到浏览器的本地存储中，并在登录成功后重定向到dashboard页面。

这段代码监听了HTMX的htmx:afterRequest事件。此事件在HTMX请求完成（即请求已经发出并接收到响应）后触发，event.detail.elt表示触发事件的元素。代码检查该元素的id是否为login-form，确认这次请求来自登录表单。如果是其他表单或元素触发的请求，它将忽略。如果服务器的身份验证成功，它以json格式返回token和重定向地址，前端会解析响应，并将Token存储到本地存储，然后自动跳转到登录后的dashboard页面。

下面是dashboard页面的html模板：

```
// go-htmx/demo4/dashboard.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HTMX Auth Example - Dashboard</title>
<script src="https://unpkg.com/htmx.org@2.0.2"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
htmx.on('htmx:configRequest', function(event) {
var token = localStorage.getItem('auth_token');
if (token) {
event.detail.headers['Authorization'] = 'Bearer ' + token;
}
});
});
</script>
</head>
<body>
<h1>Welcome to Your Dashboard</h1>
<button hx-get="/protected" hx-target="#protected-content">Access Protected Content</button>
<div id="protected-content"></div>
</body>
</html>
```


这段代码最值得关注的地方就是在后续发出的Request中自动加入之前获取到的token。这里是使用了htmx:configRequest事件实现的。监听HTMX的htmx:configRequest事件，该事件在HTMX发出请求之前触发，它允许你修改即将发出的请求。这里的configRequest的处理逻辑是：如果Token存在，将它添加到即将发出的请求的Authorization头中，并格式化为标准的Bearer Token形式（即 “Authorization: Bearer your_token_here”）。这样，后端在处理请求时可以从请求头中提取出Token，用于验证用户身份。

整个示例的后端go程序如下：

```
// go-htmx/demo4/main.go
package main
import (
"encoding/json"
"fmt"
"html/template"
"net/http"
"strings"
"sync"
"github.com/google/uuid"
)
var (
tokens = make(map[string]bool)
tokensMu sync.Mutex
)
type LoginResponse struct {
Success bool `json:"success"`
Token string `json:"token,omitempty"`
Message string `json:"message"`
Redirect string `json:"redirect,omitempty"`
}
func main() {
http.HandleFunc("/", indexHandler)
http.HandleFunc("/login", loginHandler)
http.HandleFunc("/dashboard", dashboardHandler)
http.HandleFunc("/protected", protectedHandler)
fmt.Println("Server is running on http://localhost:8080")
http.ListenAndServe(":8080", nil)
}
func indexHandler(w http.ResponseWriter, r *http.Request) {
if r.URL.Path != "/" {
http.NotFound(w, r)
return
}
http.ServeFile(w, r, "index.html")
}
func loginHandler(w http.ResponseWriter, r *http.Request) {
if r.Method != http.MethodPost {
http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
return
}
username := r.FormValue("username")
password := r.FormValue("password")
response := LoginResponse{}
if username == "admin" && password == "password" {
token := uuid.New().String()
tokensMu.Lock()
tokens[token] = true
tokensMu.Unlock()
response.Success = true
response.Token = token
response.Message = "Login successful"
response.Redirect = "/dashboard"
} else {
response.Success = false
response.Message = "Login failed. Please check your credentials and try again."
}
w.Header().Set("Content-Type", "application/json")
json.NewEncoder(w).Encode(response)
}
func dashboardHandler(w http.ResponseWriter, r *http.Request) {
tmpl, err := template.ParseFiles("dashboard.html")
if err != nil {
http.Error(w, err.Error(), http.StatusInternalServerError)
return
}
tmpl.Execute(w, nil)
}
func protectedHandler(w http.ResponseWriter, r *http.Request) {
authHeader := r.Header.Get("Authorization")
if authHeader == "" || !strings.HasPrefix(authHeader, "Bearer ") {
http.Error(w, "Unauthorized", http.StatusUnauthorized)
return
}
token := strings.TrimPrefix(authHeader, "Bearer ")
tokensMu.Lock()
valid := tokens[token]
tokensMu.Unlock()
if !valid {
http.Error(w, "Invalid token", http.StatusUnauthorized)
return
}
fmt.Fprintf(w, `<div>
<h2>Protected Content</h2>
<p>This is sensitive information only for authenticated users.</p>
<p>Your token: %s</p>
</div>`, token)
}
```


注：这里仅是示例，因此只是用了一个uuid作为token，没有使用通用的jwt。


运行程序，登录并在Dashboard中点击访问protected data，我们会看到下面图中呈现的效果：

![](../../assets/f871564eff343d57.png)


下面我们再来看一个略复杂一些的示例，这次我们基于htmx来实现SSE(Server-Sent Event)，即服务端事件。

### 3.2 SSE

Server-Sent Events (SSE) 是一种轻量级的实时通信技术，允许服务器通过HTTP协议持续向客户端推送更新数据。与[WebSocket](https://tonybai.com/2019/09/28/how-to-build-websockets-in-go)不同，SSE是单向通信，服务器可以推送数据到客户端，但客户端无法通过同一连接向服务器发送数据。这种机制非常适合需要频繁更新数据但对双向通信要求不高的场景，如股票价格、新闻推送、社交媒体通知等。

htmx对SSE的支持是通过扩展包实现的，下面就是本示例的index.html模板代码：

```
// go-htmx/demo5/index.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HTMX SSE Notifications</title>
<script src="https://unpkg.com/htmx.org@1.9.6"></script>
<script src="https://unpkg.com/htmx.org/dist/ext/sse.js"></script>
</head>
<body>
<h1>实时通知</h1>
<div hx-ext="sse" sse-connect="/events" sse-swap="message">
<ul id="notifications">
<!-- 通知将在这里动态添加 -->
</ul>
</div>
<script>
htmx.on("htmx:sseMessage", function(event) {
var ul = document.getElementById("notifications");
var li = document.createElement("li");
li.innerHTML = event.detail.message;
ul.insertBefore(li, ul.firstChild);
});
</script>
</body>
</html>
```


这个代码片段通过HTMX和Server-Sent Events (SSE) 实现了实时通知的功能。它会动态将服务器端发送的通知添加到页面的通知列表中。具体来说：

- hx-ext=”sse”：启用了HTMX的SSE扩展，用于处理 Server-Sent Events（服务器发送事件），使得浏览器可以保持与服务器的长连接，实时接收更新。
- sse-connect=”/events”：指定了SSE连接的URL。浏览器会向/events这个路径发起SSE连接，服务器可以通过这个连接持续向客户端推送消息。
- sse-swap=”message”：指示HTMX在收到SSE消息时触发事件处理，消息内容将使用JavaScript进行处理而不是自动更新HTML。
- htmx.on(“htmx:sseMessage”, function(event))：监听HTMX的htmx:sseMessage事件，每当服务器通过SSE推送新消息时，该事件会触发。event.detail.message包含从服务器接收到的消息内容。
- var ul = document.getElementById(“notifications”);：获取页面上ID为notifications的\<ul>元素，表示存放通知的容器。收到的通知通过htmx:sseMessage事件处理，将消息动态添加到通知列表中，并显示在网页上。

下面是示例对应的Go后端程序：

```
// go-htmx/demo5/main.go
func main() {
http.HandleFunc("/", serveHTML)
http.HandleFunc("/events", handleSSE)
fmt.Println("Server starting on http://localhost:8080")
log.Fatal(http.ListenAndServe(":8080", nil))
}
func serveHTML(w http.ResponseWriter, r *http.Request) {
http.ServeFile(w, r, "index.html")
}
func handleSSE(w http.ResponseWriter, r *http.Request) {
w.Header().Set("Content-Type", "text/event-stream")
w.Header().Set("Cache-Control", "no-cache")
w.Header().Set("Connection", "keep-alive")
flusher, ok := w.(http.Flusher)
if !ok {
http.Error(w, "Streaming unsupported!", http.StatusInternalServerError)
return
}
notificationCount := 1
for {
notification := fmt.Sprintf("新通知 #%d: %s", notificationCount, time.Now().Format("15:04:05"))
fmt.Fprintf(w, "data: <li>%s</li>\n\n", notification)
flusher.Flush()
notificationCount++
time.Sleep(3 * time.Second)
if r.Context().Err() != nil {
return
}
}
}
```


运行程序，打开浏览器访问localhost:8080，在加载的页面中会自动建立sse连接，页面上的通知消息区便会如下面这样每3秒一变化：

![](../../assets/589105c75fdc1944.png)


不过这个示例的程序有个“瑕疵”，那就是如果将htmx的版本从1.9.6换作最新的2.0.2，那么示例就将不工作了，翻看了一下htmx文档，应该是sseMessage这个htmx扩展属性被删除了。

如果要让示例更具通用性，可以将index.html换成下面的代码：

```
// go-htmx/demo6/index.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HTMX SSE Notifications</title>
<script src="https://unpkg.com/htmx.org@2.0.2"></script>
<style>
#notification {
padding: 10px;
border: 1px solid #ccc;
background-color: #f8f8f8;
margin-top: 20px;
}
</style>
</head>
<body>
<h1>实时通知</h1>
<div id="notification-container">
<div id="notification">等待通知...</div>
</div>
<script>
document.body.addEventListener('htmx:load', function() {
var notificationDiv = document.getElementById('notification');
var evtSource = new EventSource("/events");
evtSource.onmessage = function(event) {
notificationDiv.textContent = event.data;
};
evtSource.onerror = function(err) {
console.error("EventSource failed:", err);
};
});
</script>
</body>
</html>
```


当然这个代码更多使用js来实现事件的处理。

## 4. 小结

本文探讨了Go与htmx这一全栈组合的简洁优势。对于后端开发者而言，这一组合提供了一种无需深入掌握前端技术即可开发现代Web应用的高效途径。

然而，从两个高级示例中可以看出，**JavaScript代码仍难以完全避免**，虽然数量不多，但在稍复杂的场景下依然不可或缺。

因此，htmx目前更多被中小型团队或个人开发者所青睐。这类开发者通常没有专职的前端人员，但希望快速构建并部署功能完善的Web应用。

综上所述，在我这个对前端开发了解甚少的Go开发者看来，Go与htmx的组合的确降低了开发门槛，同时提供了性能和SEO优势，使其成为现代Web开发中值得推荐的技术栈之一。不过，对于复杂的Web应用，开发者可能需要结合htmx和JavaScript，或更可能直接采用vue、react或angular等框架。

目前Go社区对htmx的支持也越来越多，比如[html模板引擎templ](https://templ.guide)可以用于生成htmx模板，当然也有专有的htmx框架，比如：[ghtmx](https://gitlab.com/go-htmx/go-htmx)、[pagoda](https://github.com/mikestefanello/pagoda)、[go-htmx](https://github.com/donseba/go-htmx)等。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go-htmx)下载。

## 5. 参考资料

[htmx.org](https://htmx.org/)– https://htmx.org/[htmx sucks](https://htmx.org/essays/htmx-sucks/)– https://htmx.org/essays/htmx-sucks/[《HYPERMEDIA SYSTEMS》](https://hypermedia.systems/book/contents/)– https://hypermedia.systems/book/contents/

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