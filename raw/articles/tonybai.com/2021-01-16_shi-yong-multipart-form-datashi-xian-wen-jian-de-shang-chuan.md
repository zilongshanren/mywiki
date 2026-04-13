---
title: 使用multipart/form-data实现文件的上传与下载
url: https://tonybai.com/2021/01/16/upload-and-download-file-using-multipart-form-over-http/
published: '2021-01-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用multipart/form-data实现文件的上传与下载

![img{512x368}](../../assets/5cb8ebb2b3a0055a.png)


### 1. Form简介

[ Form(中文译为表单)](https://www.w3.org/TR/html401/interact/forms.html)，是HTML标记语言中的重要语法元素。一个Form不仅包含正常的文本内容、标记等，还包含被称为控件的特殊元素。用户通常通过修改控件（比如：输入文本、选择菜单项等）来“完成”表单，然后将表单数据以HTTP Get或Post请求的形式提交（submit）给Web服务器。

很多初学者总是混淆HTML和HTTP。其实，http通常作为html传输的承载体，打个比方，html就像乘客，http就像出租车，将乘客从一个地方运输到另外一个地方。但显然http这辆出租车可不仅仅只拉html这一个乘客，很多格式均可作为http这辆出租车的乘客，比如json(over http)、xml(over http)。


在一个HTML文档中，一个表单的标准格式如下：

```
<form action="http://localhost:8080/repositories" method="get">
<input type="text" name="language" value="go" />
<input type="text" name="since" value="monthly" />
<input type="submit" />
</form>
```


这样的一个Form被加载到浏览器中后会呈现为一个表单的样式，当在两个文本框中分别输入文本(或以默认的文本作为输入)后，点击“提交(submit)”，浏览器会向http://localhost:8080发出一个HTTP请求，由于Form的method属性为get，因此该HTTP请求会将表单的输入文本作为查询字符串参数(Query String Parameter，在这里即是**?language=go&since=monthly**)。服务器端处理完该请求后，会返回一个HTTP承载的应答，该应答被浏览器接收后会按特定样式呈现在浏览器窗口中。上述这个过程可以用总结为下面这幅示意图：

![img{512x368}](../../assets/e104a149db3647fe.png)


Form中的method也可以使用post，就像下面这样：

```
<form action="http://localhost:8080/repositories" method="post">
<input type="text" name="language" value="go" />
<input type="text" name="since" value="monthly" />
<input type="submit" />
</form>
```


改为post的Form表单在点击提交后发出的http请求与method=get时的请求有何不同呢？不同之处就在于在method=post的情况下，表单的参数不会再以查询字符串参数的形式放在请求的URL中，而是会被写入HTTP的BODY中。我们也将这一过程用一幅示意图的形式总结一下：

![img{512x368}](../../assets/a7e83cc07dea563f.png)


由于表单参数被放置在HTTP Body中传输(body中的数据为：**language=go&since=monthly**)，因此在该HTTP请求的headers中我们会发现新增一个header字段：**Content-Type**，在这里例子中，它的值为**application/x-www-form-urlencoded**。我们可以在Form中使用**enctype**属性改变Form传输数据的内容编码类型，该属性的默认值就是**application/x-www-form-urlencoded**(即key1=value1&key2=value2&…的形式)。enctype的其它可选值还包括：

- text/plain
- multipart/form-data

采用method=get的Form的表单参数以查询字符串参数的形式放入http请求，这使得其应用场景相对局限，比如：

- 当参数值很多，参数值很长时，可能会超出URL最大长度限制；
- 传递敏感数据时，参数值以明文放在HTTP请求头是不安全的；
- 无法胜任传递二进制数据(比如一个文件内容)的情形。

因此，在面对上述这些情形时，method=post的表单更有优势。当enctype为不同值时，method=post的表单在http Body中传输的数据形式如下图：

![img{512x368}](../../assets/93b41a73684f5be6.png)


我们看到：enctype=application/x-www-urlencoded时，Body中的数据呈现为key1=value1&key2=value2&…的形式，好似URL的查询字符串参数的组合呈现形式；当enctype=text/plain时，这种编码格式也称为raw，即将数据内容原封不动的放入Body中传输，保持数据的原先的编码方式(通常为utf-8)；而当enctype=multipart/form-data时，HTTP Body中的数据以多段(part)的形式呈现，段与段之间使用指定的随机字符串分隔，该随机字符串也会随着HTTP Post请求一并传给服务端(放在Header中的Content-Type的值中，与multipart/form-data使用分号相隔)，如：

```
Content-Type: multipart/form-data; boundary=--------------------------399501358433894470769897
```


我们来看一个稍微复杂些的enctype=multipart/form-data的例子的示意图：

![img{512x368}](../../assets/4f7cd043da9c6e10.png)


我们用Postman模拟了一个包含5个分段(part)的Post请求，其中包含两个文本分段(text)和三个文件分段，并且这三个文件是不同格式的文件，分别是txt，png和json。针对文件分段，Postman使用每个分段中的Content-Type来指明这个分段的数据内容类型。当服务端接收到这些数据时，根据分段Content-Type的指示，便可以有针对性的对分段数据进行解析了。文件分段的默认Content-Type为text/plain；对于无法识别的文件类型（比如：没有扩展名），文件分段的Content-Type通常会设置为**application/octet-stream**。

通过Form上传文件是[RFC1867规范](https://www.ietf.org/rfc/rfc1867.txt)赋予html的一种能力，并且该能力已被证明非常有用，并被广泛使用，**甚至**我们可以直接将multipart/form-data作为HTTP Post body的一种数据承载协议在两个端之间传输文件数据。

### 2. 支持以multipart/form-data格式上传文件的Go服务器

http.Request提供了ParseMultipartForm的方法对以multipart/form-data格式传输的数据进行解析，解析即是将数据映射为Request结构的MultipartForm字段的过程：

```
// $GOROOT/src/net/http/request.go
type Request struct {
... ...
// MultipartForm is the parsed multipart form, including file uploads.
// This field is only available after ParseMultipartForm is called.
// The HTTP client ignores MultipartForm and uses Body instead.
MultipartForm *multipart.Form
... ...
}
```


multipart.Form代表了一个解析后的multipart/form-data的Body，其结构如下:

```
// $GOROOT/src/mime/multipart/formdata.go
// Form is a parsed multipart form.
// Its File parts are stored either in memory or on disk,
// and are accessible via the *FileHeader's Open method.
// Its Value parts are stored as strings.
// Both are keyed by field name.
type Form struct {
Value map[string][]string
File map[string][]*FileHeader
}
```


我们看到这个Form结构由两个map组成，一个map中存放了所有的value part(就像前面的name、age)，另外一个map存放了所有的file part(就像前面的part1.txt、part2.png和part3.json)。value part集合没什么可说的，map的key就是每个值分段中的”name”； 我们的重点在file part上。每个file part对应一组FileHeader，FileHeader的结构如下：

```
// $GOROOT/src/mime/multipart/formdata.go
type FileHeader struct {
Filename string
Header textproto.MIMEHeader
Size int64
content []byte
tmpfile string
}
```


每个file part的FileHeader包含五个字段：

- Filename – 上传文件的原始文件名
- Size – 上传文件的大小（单位：字节）
- content – 内存中存储的上传文件的（部分或全部）数据内容
- tmpfile – 在服务器本地的临时文件中存储的部分上传文件的数据内容(如果上传的文件大小大于传给ParseMultipartForm的参数maxMemory，剩余部分存储在临时文件中)
- Header – file part的header内容，它亦是一个map，其结构如下：

```
// $GOROOT/src/net/textproto/header.go
// A MIMEHeader represents a MIME-style header mapping
// keys to sets of values.
type MIMEHeader map[string][]string
```


我们可以将ParseMultipartForm方法实现的数据映射过程表述为下面这张示意图，这样看起来更为直观：

![img{512x368}](../../assets/827a69b79b843063.png)


有了上述对通过multipart/form-data格式上传文件的原理的拆解，我们就可以很容易地利用Go http包实现一个简单的支持以multipart/form-data格式上传文件的Go服务器：

```
// github.com/bigwhite/experiments/multipart-formdata/server/file_server1.go
package main
import (
"fmt"
"io"
"net/http"
"os"
)
const uploadPath = "./upload"
func handleUploadFile(w http.ResponseWriter, r *http.Request) {
r.ParseMultipartForm(100)
mForm := r.MultipartForm
for k, _ := range mForm.File {
// k is the key of file part
file, fileHeader, err := r.FormFile(k)
if err != nil {
fmt.Println("inovke FormFile error:", err)
return
}
defer file.Close()
fmt.Printf("the uploaded file: name[%s], size[%d], header[%#v]\n",
fileHeader.Filename, fileHeader.Size, fileHeader.Header)
// store uploaded file into local path
localFileName := uploadPath + "/" + fileHeader.Filename
out, err := os.Create(localFileName)
if err != nil {
fmt.Printf("failed to open the file %s for writing", localFileName)
return
}
defer out.Close()
_, err = io.Copy(out, file)
if err != nil {
fmt.Printf("copy file err:%s\n", err)
return
}
fmt.Printf("file %s uploaded ok\n", fileHeader.Filename)
}
}
func main() {
http.HandleFunc("/upload", handleUploadFile)
http.ListenAndServe(":8080", nil)
}
```


我们可以用Postman或下面curl命令向上述文件服务器同时上传两个文件part1.txt和part3.json：

```
curl --location --request POST ':8080/upload' \
--form 'name="tony bai"' \
--form 'age="23"' \
--form 'file1=@"/your_local_path/part1.txt"' \
--form 'file3=@"/your_local_path/part3.json"'
```


文件上传服务器的运行输出日志如下：

```
$go run file_server1.go
the uploaded file: name[part3.json], size[130], header[textproto.MIMEHeader{"Content-Disposition":[]string{"form-data; name=\"file3\"; filename=\"part3.json\""}, "Content-Type":[]string{"application/json"}}]
file part3.json uploaded ok
the uploaded file: name[part1.txt], size[15], header[textproto.MIMEHeader{"Content-Disposition":[]string{"form-data; name=\"file1\"; filename=\"part1.txt\""}, "Content-Type":[]string{"text/plain"}}]
file part1.txt uploaded ok
```


之后我们可以看到：文件上传服务器成功地将接收到的part1.txt和part3.json存储到了当前路径下的upload目录中了！

### 3. 支持以multipart/form-data格式上传文件的Go客户端

前面进行文件上传的客户端要么是浏览器，要么是Postman，要么是curl，如果我们自己构要造一个支持以multipart/form-data格式上传文件的客户端，应该如何做呢？我们需要按照multipart/form-data的格式构造HTTP请求的包体(Body)，还好通过Go标准库提供的mime/multipart包，我们可以很容易地构建出满足要求的包体：

```
// github.com/bigwhite/experiments/multipart-formdata/client/client1.go
... ...
var (
filePath string
addr string
)
func init() {
flag.StringVar(&filePath, "file", "", "the file to upload")
flag.StringVar(&addr, "addr", "localhost:8080", "the addr of file server")
flag.Parse()
}
func main() {
if filePath == "" {
fmt.Println("file must not be empty")
return
}
err := doUpload(addr, filePath)
if err != nil {
fmt.Printf("upload file [%s] error: %s", filePath, err)
return
}
fmt.Printf("upload file [%s] ok\n", filePath)
}
func createReqBody(filePath string) (string, io.Reader, error) {
var err error
buf := new(bytes.Buffer)
bw := multipart.NewWriter(buf) // body writer
f, err := os.Open(filePath)
if err != nil {
return "", nil, err
}
defer f.Close()
// text part1
p1w, _ := bw.CreateFormField("name")
p1w.Write([]byte("Tony Bai"))
// text part2
p2w, _ := bw.CreateFormField("age")
p2w.Write([]byte("15"))
// file part1
_, fileName := filepath.Split(filePath)
fw1, _ := bw.CreateFormFile("file1", fileName)
io.Copy(fw1, f)
bw.Close() //write the tail boundry
return bw.FormDataContentType(), buf, nil
}
func doUpload(addr, filePath string) error {
// create body
contType, reader, err := createReqBody(filePath)
if err != nil {
return err
}
url := fmt.Sprintf("http://%s/upload", addr)
req, err := http.NewRequest("POST", url, reader)
// add headers
req.Header.Add("Content-Type", contType)
client := &http.Client{}
resp, err := client.Do(req)
if err != nil {
fmt.Println("request send error:", err)
return err
}
resp.Body.Close()
return nil
}
```


显然上面这个client端的代码的核心是createReqBody函数：

- 该client在body中创建了三个分段，前两个分段仅仅是我为了演示如何创建text part而故意加入的，真正的上传文件客户端是不需要创建这两个分段(part)的；
- createReqBody使用bytes.Buffer作为http body的临时存储；
- 构建完body内容后，不要忘记调用multipart.Writer的Close方法以写入结尾的boundary标记。

我们使用这个客户端向前面的支持以multipart/form-data格式上传文件的服务器上传一个文件：

```
// 客户端
$go run client1.go -file hello.txt
upload file [hello.txt] ok
// 服务端
$go run file_server1.go
http request: http.Request{Method:"POST", URL:(*url.URL)(0xc00016e100), Proto:"HTTP/1.1", ProtoMajor:1, ProtoMinor:1, Header:http.Header{"Accept-Encoding":[]string{"gzip"}, "Content-Length":[]string{"492"}, "Content-Type":[]string{"multipart/form-data; boundary=b55090594eaa1aaac1abad1d89a77ae689130d79d6f66af82590036bd8ba"}, "User-Agent":[]string{"Go-http-client/1.1"}}, Body:(*http.body)(0xc000146380), GetBody:(func() (io.ReadCloser, error))(nil), ContentLength:492, TransferEncoding:[]string(nil), Close:false, Host:"localhost:8080", Form:url.Values{"age":[]string{"15"}, "name":[]string{"Tony Bai"}}, PostForm:url.Values{"age":[]string{"15"}, "name":[]string{"Tony Bai"}}, MultipartForm:(*multipart.Form)(0xc000110d50), Trailer:http.Header(nil), RemoteAddr:"[::1]:58569", RequestURI:"/upload", TLS:(*tls.ConnectionState)(nil), Cancel:(<-chan struct {})(nil), Response:(*http.Response)(nil), ctx:(*context.cancelCtx)(0xc0001463c0)}
the uploaded file: name[hello.txt], size[15], header[textproto.MIMEHeader{"Content-Disposition":[]string{"form-data; name=\"file1\"; filename=\"hello.txt\""}, "Content-Type":[]string{"application/octet-stream"}}]
file hello.txt uploaded ok
```


我们看到hello.txt这个文本文件被成功上传！

### 4. 自定义file分段中的header

从上面file_server1的输出来看，client1这个客户端上传文件时在file分段(part)中设置的Content-Type为默认的**application/octet-stream**。有时候，服务端可能会需要根据这个Content-Type做分类处理，需要客户端给出准确的值。上面的client1实现中，我们使用了multipart.Writer.CreateFormFile这个方法来创建file part：

```
// file part1
_, fileName := filepath.Split(filePath)
fw1, _ := bw.CreateFormFile("file1", fileName)
io.Copy(fw1, f)
```


下面是标准库中CreateFormFile方法的实现代码：

```
// $GOROOT/mime/multipart/writer.go
func (w *Writer) CreateFormFile(fieldname, filename string) (io.Writer, error) {
h := make(textproto.MIMEHeader)
h.Set("Content-Disposition",
fmt.Sprintf(`form-data; name="%s"; filename="%s"`,
escapeQuotes(fieldname), escapeQuotes(filename)))
h.Set("Content-Type", "application/octet-stream")
return w.CreatePart(h)
}
```


我们看到无论待上传的文件是什么类型，CreateFormFile均将Content-Type置为application/octet-stream这一默认值。如果我们要自定义file part中Header字段Content-Type的值，我们就不能直接使用CreateFormFile，不过我们可以参考其实现：

```
// github.com/bigwhite/experiments/multipart-formdata/client/client2.go
var quoteEscaper = strings.NewReplacer("\\", "\\\\", `"`, "\\\"")
func escapeQuotes(s string) string {
return quoteEscaper.Replace(s)
}
func createReqBody(filePath string) (string, io.Reader, error) {
var err error
buf := new(bytes.Buffer)
bw := multipart.NewWriter(buf) // body writer
f, err := os.Open(filePath)
if err != nil {
return "", nil, err
}
defer f.Close()
// text part1
p1w, _ := bw.CreateFormField("name")
p1w.Write([]byte("Tony Bai"))
// text part2
p2w, _ := bw.CreateFormField("age")
p2w.Write([]byte("15"))
// file part1
_, fileName := filepath.Split(filePath)
h := make(textproto.MIMEHeader)
h.Set("Content-Disposition",
fmt.Sprintf(`form-data; name="%s"; filename="%s"`,
escapeQuotes("file1"), escapeQuotes(fileName)))
h.Set("Content-Type", "text/plain")
fw1, _ := bw.CreatePart(h)
io.Copy(fw1, f)
bw.Close() //write the tail boundry
return bw.FormDataContentType(), buf, nil
}
```


我们通过textproto.MIMEHeader实例来自定义file part的header部分，然后基于该实例调用CreatePart创建file part，之后将hello.txt的文件内容写到该part的header后面。

我们运行client2来上传hello.txt文件，在file_server侧，我们就能看到如下日志：

```
the uploaded file: name[hello.txt], size[15], header[textproto.MIMEHeader{"Content-Disposition":[]string{"form-data; name=\"file1\"; filename=\"hello.txt\""}, "Content-Type":[]string{"text/plain"}}]
file hello.txt uploaded ok
```


我们看到file part的Content-Type的值已经变为我们设定的**text/plain**了。

### 5. 解决上传大文件的问题

在上面的客户端中存在一个问题，那就是我们在构建http body的时候，使用了一个bytes.Buffer加载了待上传文件的所有内容，这样一来，如果待上传的文件很大的话，内存空间消耗势必过大。那么如何将每次上传内存文件时对内存的使用限制在一个适当的范围，或者说上传文件所消耗的内存空间不因待传文件的变大而变大呢？我们来看下面的这个解决方案：

```
// github.com/bigwhite/experiments/multipart-formdata/client/client3.go
... ...
func createReqBody(filePath string) (string, io.Reader, error) {
var err error
pr, pw := io.Pipe()
bw := multipart.NewWriter(pw) // body writer
f, err := os.Open(filePath)
if err != nil {
return "", nil, err
}
go func() {
defer f.Close()
// text part1
p1w, _ := bw.CreateFormField("name")
p1w.Write([]byte("Tony Bai"))
// text part2
p2w, _ := bw.CreateFormField("age")
p2w.Write([]byte("15"))
// file part1
_, fileName := filepath.Split(filePath)
h := make(textproto.MIMEHeader)
h.Set("Content-Disposition",
fmt.Sprintf(`form-data; name="%s"; filename="%s"`,
escapeQuotes("file1"), escapeQuotes(fileName)))
h.Set("Content-Type", "application/pdf")
fw1, _ := bw.CreatePart(h)
cnt, _ := io.Copy(fw1, f)
log.Printf("copy %d bytes from file %s in total\n", cnt, fileName)
bw.Close() //write the tail boundry
pw.Close()
}()
return bw.FormDataContentType(), pr, nil
}
func doUpload(addr, filePath string) error {
// create body
contType, reader, err := createReqBody(filePath)
if err != nil {
return err
}
log.Printf("createReqBody ok\n")
url := fmt.Sprintf("http://%s/upload", addr)
req, err := http.NewRequest("POST", url, reader)
//add headers
req.Header.Add("Content-Type", contType)
client := &http.Client{}
log.Printf("upload %s...\n", filePath)
resp, err := client.Do(req)
if err != nil {
fmt.Println("request send error:", err)
return err
}
resp.Body.Close()
log.Printf("upload %s ok\n", filePath)
return nil
}
```


在这个方案中，我们通过io.Pipe函数创建了一个读写管道，其写端作为io.Writer实例传给multipart.NewWriter，读端返回给调用者，用于构建http request时使用。io.Pipe基于channel实现，其内部不维护任何内存缓存：

```
// $GOROOT/src/io/pipe.go
func Pipe() (*PipeReader, *PipeWriter) {
p := &pipe{
wrCh: make(chan []byte),
rdCh: make(chan int),
done: make(chan struct{}),
}
return &PipeReader{p}, &PipeWriter{p}
}
```


通过Pipe返回的读端读取管道中数据时，如果尚未有数据写入管道，那么读端会像读取channel那样阻塞在那里。由于http request在被发送时(client.Do(req))才会真正基于构建req时传入的reader对Body数据进行读取，因此client会阻塞在对管道的read上。显然我们不能将读写两端的操作放在一个goroutine中，那样会因所有goroutine都挂起而导致panic。在上面的client3.go代码中，函数createReqBody内部创建了一个新goroutine，将真正构建multipart/form-data body的工作放在了新goroutine中。新goroutine最终会将待上传文件的数据通过管道写端写入管道：

```
cnt, _ := io.Copy(fw1, f)
```


而这些数据也会被client读取并通过网络连接传输出去。io.Copy的实现如下：

```
// $GOROOT/src/io/io.go
func Copy(dst Writer, src Reader) (written int64, err error) {
return copyBuffer(dst, src, nil)
}
```


io.copyBuffer内部维护了一个默认32k的小buffer，它每次从src尝试最大读取32k的数据，并写入到dst中，直到读完为止。这样无论待上传的文件有多大，我们实际上每次上传所分配的内存仅有32k。

下面就是我们用client3.go上传一个大小为252M的文件的日志：

```
$go run client3.go -file /Users/tonybai/Downloads/ICME-2019-Tutorial-final.pdf
2021/01/10 12:56:45 createReqBody ok
2021/01/10 12:56:45 upload /Users/tonybai/Downloads/ICME-2019-Tutorial-final.pdf...
2021/01/10 12:56:46 copy 264517032 bytes from file ICME-2019-Tutorial-final.pdf in total
2021/01/10 12:56:46 upload /Users/tonybai/Downloads/ICME-2019-Tutorial-final.pdf ok
upload file [/Users/tonybai/Downloads/ICME-2019-Tutorial-final.pdf] ok
$go run file_server1.go
http request: http.Request{Method:"POST", URL:(*url.URL)(0xc000078200), Proto:"HTTP/1.1", ProtoMajor:1, ProtoMinor:1, Header:http.Header{"Accept-Encoding":[]string{"gzip"}, "Content-Type":[]string{"multipart/form-data; boundary=4470ba3867218f1130878713da88b5bd79f33dfbed65566e4fd76a1ae58d"}, "User-Agent":[]string{"Go-http-client/1.1"}}, Body:(*http.body)(0xc000026240), GetBody:(func() (io.ReadCloser, error))(nil), ContentLength:-1, TransferEncoding:[]string{"chunked"}, Close:false, Host:"localhost:8080", Form:url.Values{"age":[]string{"15"}, "name":[]string{"Tony Bai"}}, PostForm:url.Values{"age":[]string{"15"}, "name":[]string{"Tony Bai"}}, MultipartForm:(*multipart.Form)(0xc0000122a0), Trailer:http.Header(nil), RemoteAddr:"[::1]:54899", RequestURI:"/upload", TLS:(*tls.ConnectionState)(nil), Cancel:(<-chan struct {})(nil), Response:(*http.Response)(nil), ctx:(*context.cancelCtx)(0xc000026280)}
the uploaded file: name[ICME-2019-Tutorial-final.pdf], size[264517032], header[textproto.MIMEHeader{"Content-Disposition":[]string{"form-data; name=\"file1\"; filename=\"ICME-2019-Tutorial-final.pdf\""}, "Content-Type":[]string{"application/pdf"}}]
file ICME-2019-Tutorial-final.pdf uploaded ok
$ls -l upload
-rw-r--r-- 1 tonybai staff 264517032 1 14 12:56 ICME-2019-Tutorial-final.pdf
```


如果你觉得32k仍然很大，每次上传要使用更小的buffer，你可以用io.CopyBuffer替代io.Copy：

```
// github.com/bigwhite/experiments/multipart-formdata/client/client4.go
func createReqBody(filePath string) (string, io.Reader, error) {
var err error
pr, pw := io.Pipe()
bw := multipart.NewWriter(pw) // body writer
f, err := os.Open(filePath)
if err != nil {
return "", nil, err
}
go func() {
defer f.Close()
// text part1
p1w, _ := bw.CreateFormField("name")
p1w.Write([]byte("Tony Bai"))
// text part2
p2w, _ := bw.CreateFormField("age")
p2w.Write([]byte("15"))
// file part1
_, fileName := filepath.Split(filePath)
h := make(textproto.MIMEHeader)
h.Set("Content-Disposition",
fmt.Sprintf(`form-data; name="%s"; filename="%s"`,
escapeQuotes("file1"), escapeQuotes(fileName)))
h.Set("Content-Type", "application/pdf")
fw1, _ := bw.CreatePart(h)
var buf = make([]byte, 1024)
cnt, _ := io.CopyBuffer(fw1, f, buf)
log.Printf("copy %d bytes from file %s in total\n", cnt, fileName)
bw.Close() //write the tail boundry
pw.Close()
}()
return bw.FormDataContentType(), pr, nil
}
```


运行这个client4：

```
$go run client4.go -file /Users/tonybai/Downloads/ICME-2019-Tutorial-final.pdf
2021/01/10 13:39:06 createReqBody ok
2021/01/10 13:39:06 upload /Users/tonybai/Downloads/ICME-2019-Tutorial-final.pdf...
2021/01/10 13:39:09 copy 264517032 bytes from file ICME-2019-Tutorial-final.pdf in total
2021/01/10 13:39:09 upload /Users/tonybai/Downloads/ICME-2019-Tutorial-final.pdf ok
upload file [/Users/tonybai/Downloads/ICME-2019-Tutorial-final.pdf] ok
```


你会看到虽然上传成功了，但由于每次read仅能读1k数据，对于大文件来说，其上传的时间消耗增加了不少。

### 6. 下载文件

客户端基于multipart/form-data下载文件的过程的原理与上面的file_server1接收客户端上传文件的原理是一样的，这里就将这个功能的Go实现作为“作业”留给各位读者了:)。

### 7. 参考资料

[Form-based File Upload in HTML](https://www.ietf.org/rfc/rfc1867.txt)[Returning Values from Forms: multipart/form-data](https://www.ietf.org/rfc/rfc2388.txt)[《Go Web Programming》](https://book.douban.com/subject/27204133/)[Hypertext Transfer Protocol (HTTP/1.1): Range Requests](https://www.ietf.org/rfc/rfc7233.txt)

本文中涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/multipart-formdata)(https://github.com/bigwhite/experiments/tree/master/multipart-formdata)下载。

“Gopher部落”知识星球开球了！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订阅！

![](../../assets/d8e58987c0d3be58.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

文章中的代码

r.ParseMultipartForm(100)

mForm := r.MultipartForm

for k, _ := range mForm.File {

// k is the key of file part

file, fileHeader, err := r.FormFile(k)

遇到傻鸟前端给出下面这样的多个同名字段

就只能接收到其中一个文件。

现在go标准库的ParseMultipartForm依赖这个key，如果填成一样，或不填，都会导致问题。