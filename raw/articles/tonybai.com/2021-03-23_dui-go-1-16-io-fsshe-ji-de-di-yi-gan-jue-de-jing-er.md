---
title: 对Go 1.16 io/fs设计的第一感觉：得劲儿！
url: https://tonybai.com/2021/03/23/io-fs-interface-is-an-excellent-design/
published: '2021-03-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 对Go 1.16 io/fs设计的第一感觉：得劲儿！

![](../../assets/6012259ca13d41cf.png)


### 1. 设计io/fs的背景

Go语言的接口是Gopher最喜欢的语法元素之一，其隐式的契约满足和“当前唯一可用的泛型机制”的特质让其成为面向组合编程的强大武器，其存在为Go建立事物抽象奠定了基础，同时也是建立抽象的主要手段。

Go语言从诞生至今，最成功的接口定义之一就是io.Writer和io.Reader接口：

```
type Writer interface {
Write(p []byte) (n int, err error)
}
type Reader interface {
Read(p []byte) (n int, err error)
}
```


这两个接口建立了**对数据源中的数据操作的良好的抽象**，通过该抽象我们可以读或写满足这两个接口的任意数据源：

- 字符串

```
r := strings.NewReader("hello, go")
r.Read(...)
```


- 字节序列

```
r := bytes.NewReader([]byte("hello, go"))
r.Read(...)
```


- 文件内数据

```
f := os.Open("foo.txt") // f 满足io.Reader
f.Read(...)
```


- 网络socket

```
r, err := net.DialTCP("192.168.0.10", nil, raddr *TCPAddr) (*TCPConn, error)
r.Read(...)
```


- 构造HTTP请求

```
req, err := http.NewRequestWithContext(ctx, "POST", url, bytes.NewReader([]byte("hello, go"))
```


- 读取压缩文件内容

```
func main() {
f, err := os.Open("hello.txt.gz")
if err != nil {
log.Fatal(err)
}
zr, err := gzip.NewReader(f)
if err != nil {
log.Fatal(err)
}
if _, err := io.Copy(os.Stdout, zr); err != nil {
log.Fatal(err)
}
if err := zr.Close(); err != nil {
log.Fatal(err)
}
}
```


… …

能构架出io.Reader和Writer这样的抽象，与Go最初核心团队的深厚的Unix背景是密不可分的，这一抽象可能深受“在UNIX中，一切都是字节流”这一设计哲学的影响。

Unix还有一个设计哲学：**一切都是文件**，即在Unix中，任何有I/O的设备，无论是文件、socket、驱动等，在打开设备之后都有一个对应的文件描述符，Unix将对这些设备的操作简化在**抽象的文件**中了。用户只需要打开文件，将得到的文件描述符传给相应的操作函数，操作系统内核就知道如何根据这个文件描述符得到具体设备信息，内部隐藏了对各种设备进行读写的细节。

并且Unix还使用树型的结构将各种抽象的文件(数据文件、socket、磁盘驱动器、外接设备等)组织起来，通过文件路径对其进行访问，这样的一个树型结构构成了文件系统。

不过由于历史不知名的某个原因，Go语言并没有在标准库中内置对文件以及文件系统的抽象！我们知道如今的**os.File**是一个具体的结构体类型，而不是抽象类型：

```
// $GOROOT/src/os/types.go
// File represents an open file descriptor.
type File struct {
*file // os specific
}
```


结构体os.File中唯一的字段file指针还是一个操作系统相关的类型，我们以os/file_unix.go为例，在unix中，file的定义如下：

```
// file is the real representation of *File.
// The extra level of indirection ensures that no clients of os
// can overwrite this data, which could cause the finalizer
// to close the wrong file descriptor.
type file struct {
pfd poll.FD
name string
dirinfo *dirInfo // nil unless directory being read
nonblock bool // whether we set nonblocking mode
stdoutOrErr bool // whether this is stdout or stderr
appendMode bool // whether file is opened for appending
}
```


![](../../assets/cace468ec8fcfcce.png)


不过就像Russ Cox在上述issue中的comment那样：“我想我会认为io.File应该是接口，但现在这一切都没有意义了”：

![](../../assets/cde67215ef911c64.png)


但在[Go 1.16](https://mp.weixin.qq.com/s/UPNn4G_m0zfvJgWxEVl_Tw)的embed文件功能设计过程中，Go核心团队以及参与讨论的Gopher们认为引入一个对File System和File的抽象，将会像上面的io.Reader和io.Writer那样对Go代码产生很大益处，同时也会给embed功能的实现带去便利！于是Rob Pike和Russ Cox亲自上阵完成了[io/fs的设计](https://github.com/golang/proposal/blob/master/design/draft-iofs.md)。

### 2. 探索io/fs包

io/fs的加入也不是“临时起意”，早在很多年前的godoc实现时，对一个抽象的文件系统接口的需求就已经被提了出来并给出了实现：

![](../../assets/29564c4e0009bcbc.png)


最终这份实现以godoc工具的[vfs包](https://github.com/golang/tools/tree/master/godoc/vfs)的形式一直长期存在着。虽然它的实现有些复杂，抽象程度不够，但却对[io/fs包的设计](https://github.com/golang/proposal/blob/master/design/draft-iofs.md)有着重要的参考价值。

Go语言对文件系统与文件的抽象以io/fs中的FS接口类型和File类型落地，这两个接口的设计遵循了Go语言一贯秉持的[“小接口原则”](https://www.imooc.com/read/87/article/2425)，并符合开闭设计原则(对扩展开放,对修改关闭)。

```
// $GOROOT/src/io/fs/fs.go
type FS interface {
// Open opens the named file.
//
// When Open returns an error, it should be of type *PathError
// with the Op field set to "open", the Path field set to name,
// and the Err field describing the problem.
//
// Open should reject attempts to open names that do not satisfy
// ValidPath(name), returning a *PathError with Err set to
// ErrInvalid or ErrNotExist.
Open(name string) (File, error)
}
// A File provides access to a single file.
// The File interface is the minimum implementation required of the file.
// A file may implement additional interfaces, such as
// ReadDirFile, ReaderAt, or Seeker, to provide additional or optimized functionality.
type File interface {
Stat() (FileInfo, error)
Read([]byte) (int, error)
Close() error
}
```


FS接口代表虚拟文件系统的最小抽象，它仅包含一个Open方法；File接口则是虚拟文件的最小抽象，仅包含抽象文件所需的三个共同方法(不能再少了)。我们可以基于这两个接口通过[Go常见的嵌入接口类型的方式](https://www.imooc.com/read/87/article/2423)进行扩展，就像io.ReadWriter是基于io.Reader的扩展那样。在这份设计提案中，作者还将这种方式命名为*extension interface*，即在一个基本接口类型的基础上，新增一到多个新方法以形成一个新接口。比如下面的基于FS接口的extension interface类型StatFS：

```
// A StatFS is a file system with a Stat method.
type StatFS interface {
FS
// Stat returns a FileInfo describing the file.
// If there is an error, it should be of type *PathError.
Stat(name string) (FileInfo, error)
}
```


对于File这个基本接口类型，fs包仅给出一个extension interface：ReadDirFile，即在File接口的基础上增加了一个ReadDir方法形成的，这种用扩展方法名+基础接口名来命名一个新接口类型的方式也是Go的惯用法。

对于FS接口，fs包给出了一些扩展FS的常见“新扩展接口”的样例：

![](../../assets/b8198b8ae9f3aa9d.png)


以fs包的ReadDirFS接口为例：

```
// $GOROOT/src/io/fs/readdir.go
type ReadDirFS interface {
FS
// ReadDir reads the named directory
// and returns a list of directory entries sorted by filename.
ReadDir(name string) ([]DirEntry, error)
}
// ReadDir reads the named directory
// and returns a list of directory entries sorted by filename.
//
// If fs implements ReadDirFS, ReadDir calls fs.ReadDir.
// Otherwise ReadDir calls fs.Open and uses ReadDir and Close
// on the returned file.
func ReadDir(fsys FS, name string) ([]DirEntry, error) {
if fsys, ok := fsys.(ReadDirFS); ok {
return fsys.ReadDir(name)
}
file, err := fsys.Open(name)
if err != nil {
return nil, err
}
defer file.Close()
dir, ok := file.(ReadDirFile)
if !ok {
return nil, &PathError{Op: "readdir", Path: name, Err: errors.New("not implemented")}
}
list, err := dir.ReadDir(-1)
sort.Slice(list, func(i, j int) bool { return list[i].Name() < list[j].Name() })
return list, err
}
```


我们看到伴随着ReadDirFS，标准库还提供了一个helper函数：**ReadDir**。该函数的第一个参数为FS接口类型的变量，在其内部实现中，ReadDir先通过类型断言判断传入的fsys是否实现了ReadDirFS，如果实现了，就直接调用其ReadDir方法；如果没有实现则给出了常规实现。其他几个FS的extension interface也都有自己的helper function，这也算是Go的一个惯例。如果你要实现你自己的FS的扩展，不要忘了这个惯例：**给出伴随你的扩展接口的helper function**。

标准库中一些涉及虚拟文件系统的包在Go 1.16版本中做了对io/fs的适配，比如：os、net/http、html/template、text/template、archive/zip等。

以http.FileServer为例，Go 1.16版本之前建立一个静态文件Server一般这么来写：

```
// github.com/bigwhite/experiments/blob/master/iofs/fileserver_classic.go
package main
import "net/http"
func main() {
http.ListenAndServe(":8080", http.FileServer(http.Dir(".")))
}
```


Go 1.16 http包对fs的FS和File接口做了适配后，我们可以这样写：

```
// github.com/bigwhite/experiments/blob/master/iofs/fileserver_iofs.go
package main
import (
"net/http"
"os"
)
func main() {
http.ListenAndServe(":8080", http.FileServer(http.FS(os.DirFS("./"))))
}
```


os包新增的DirFS函数返回一个fs.FS的实现：一个以传入dir为根的文件树构成的File System。

我们可以参考DirFS实现一个goFilesFS，该FS的实现仅返回以.go为后缀的文件：

```
// github.com/bigwhite/experiments/blob/master/iofs/gofilefs/gofilefs.go
package gfs
import (
"io/fs"
"os"
"strings"
)
func GoFilesFS(dir string) fs.FS {
return goFilesFS(dir)
}
type goFile struct {
*os.File
}
func Open(name string) (*goFile, error) {
f, err := os.Open(name)
if err != nil {
return nil, err
}
return &goFile{f}, nil
}
func (f goFile) ReadDir(count int) ([]fs.DirEntry, error) {
entries, err := f.File.ReadDir(count)
if err != nil {
return nil, err
}
var newEntries []fs.DirEntry
for _, entry := range entries {
if !entry.IsDir() {
ss := strings.Split(entry.Name(), ".")
if ss[len(ss)-1] != "go" {
continue
}
}
newEntries = append(newEntries, entry)
}
return newEntries, nil
}
type goFilesFS string
func (dir goFilesFS) Open(name string) (fs.File, error) {
f, err := Open(string(dir) + "/" + name)
if err != nil {
return nil, err // nil fs.File
}
return f, nil
}
```


上述GoFilesFS的实现中：

- goFilesFS实现了io/fs的FS接口，而其Open方法返回的fs.File实例为我自定义的goFile结构；
- goFile结构通过嵌入*os.File满足了io/fs的File接口；
- 我们重写goFile的ReadDir方法(覆盖os.File的同名方法)，在这个方法中我们过滤掉非.go后缀的文件。

有了GoFilesFS的实现后，我们就可以将其传给http.FileServer了：

```
// github.com/bigwhite/experiments/blob/master/iofs/fileserver_gofilefs.go
package main
import (
"net/http"
gfs "github.com/bigwhite/testiofs/gofilefs"
)
func main() {
http.ListenAndServe(":8080", http.FileServer(http.FS(gfs.GoFilesFS("./"))))
}
```


通过浏览器打开localhost:8080页面，我们就能看到仅由go源文件组成的文件树！

### 3. 使用io/fs提高代码可测性

抽象的接口意味着降低耦合，意味着[代码可测试性的提升](https://www.imooc.com/read/87/article/2427)。Go 1.16增加了对文件系统和文件的抽象之后，我们以后再面对文件相关代码时，我们便可以利用io/fs提高这类代码的可测试性。

我们有这样的一个函数：

```
func FindGoFiles(dir string) ([]string, error)
```


该函数查找出dir下所有go源文件的路径并放在一个[]string中返回。我们可以很轻松的给出下面的第一版实现：

```
// github.com/bigwhite/experiments/blob/master/iofs/gowalk/demo1/gowalk.go
package demo
import (
"os"
"path/filepath"
"strings"
)
func FindGoFiles(dir string) ([]string, error) {
var goFiles []string
err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
if info.IsDir() {
return nil
}
ss := strings.Split(path, ".")
if ss[len(ss)-1] != "go" {
return nil
}
goFiles = append(goFiles, path)
return nil
})
if err != nil {
return nil, err
}
return goFiles, nil
}
```


这一版的实现直接使用了filepath的Walk函数，它与os包是紧绑定的，即要想测试这个函数，我们需要在磁盘上真实的构造出一个文件树，就像下面这样：

```
$tree testdata
testdata
└── foo
├── 1
│ └── 1.txt
├── 1.go
├── 2
│ ├── 2.go
│ └── 2.txt
└── bar
├── 3
│ └── 3.go
└── 4.go
```


按照go惯例，我们[将测试依赖的外部数据文件放在testdata下面](https://www.imooc.com/read/87/article/2438)。下面是针对上面函数的测试文件：

```
// github.com/bigwhite/experiments/blob/master/iofs/gowalk/demo1/gowalk_test.go
package demo
import (
"testing"
)
func TestFindGoFiles(t *testing.T) {
m := map[string]bool{
"testdata/foo/1.go": true,
"testdata/foo/2/2.go": true,
"testdata/foo/bar/3/3.go": true,
"testdata/foo/bar/4.go": true,
}
files, err := FindGoFiles("testdata/foo")
if err != nil {
t.Errorf("want nil, actual %s", err)
}
if len(files) != 4 {
t.Errorf("want 4, actual %d", len(files))
}
for _, f := range files {
_, ok := m[f]
if !ok {
t.Errorf("want [%s], actual not found", f)
}
}
}
```


FindGoFiles函数的第一版设计显然可测性较差，需要对依赖特定布局的磁盘上的文件，虽然testdata也是作为源码提交到代码仓库中的。

有了io/fs包后，我们用FS接口来提升一下FindGoFiles函数的可测性，我们重新设计一下该函数：

```
// github.com/bigwhite/experiments/blob/master/iofs/gowalk/demo2/gowalk.go
package demo
import (
"io/fs"
"strings"
)
func FindGoFiles(dir string, fsys fs.FS) ([]string, error) {
var newEntries []string
err := fs.WalkDir(fsys, dir, func(path string, entry fs.DirEntry, err error) error {
if entry == nil {
return nil
}
if !entry.IsDir() {
ss := strings.Split(entry.Name(), ".")
if ss[len(ss)-1] != "go" {
return nil
}
newEntries = append(newEntries, path)
}
return nil
})
if err != nil {
return nil, err
}
return newEntries, nil
}
```


这次我们给FindGoFiles增加了一个fs.FS类型的参数fsys，这是解除掉该函数与具体FS实现的关键。当然demo1的测试方法同样适用于该版FindGoFiles函数：

```
// github.com/bigwhite/experiments/blob/master/iofs/gowalk/demo2/gowalk_test.go
package demo
import (
"os"
"testing"
)
func TestFindGoFiles(t *testing.T) {
m := map[string]bool{
"testdata/foo/1.go": true,
"testdata/foo/2/2.go": true,
"testdata/foo/bar/3/3.go": true,
"testdata/foo/bar/4.go": true,
}
files, err := FindGoFiles("testdata/foo", os.DirFS("."))
if err != nil {
t.Errorf("want nil, actual %s", err)
}
if len(files) != 4 {
t.Errorf("want 4, actual %d", len(files))
}
for _, f := range files {
_, ok := m[f]
if !ok {
t.Errorf("want [%s], actual not found", f)
}
}
}
```


但这不是我们想要的，既然我们使用了io/fs.FS接口，那么一切实现了fs.FS接口的实体均可被用来构造针对FindGoFiles的测试。但自己写一个实现了fs.FS接口以及fs.File相关接口还是比较麻烦的，Go标准库已经想到了这点，为我们提供了testing/fstest包，我们可以直接利用fstest包中实现的基于memory的FS来对FindGoFiles进行测试：

```
// github.com/bigwhite/experiments/blob/master/iofs/gowalk/demo3/gowalk_test.go
package demo
import (
"testing"
"testing/fstest"
)
/*
$tree testdata
testdata
└── foo
├── 1
│ └── 1.txt
├── 1.go
├── 2
│ ├── 2.go
│ └── 2.txt
└── bar
├── 3
│ └── 3.go
└── 4.go
5 directories, 6 files
*/
func TestFindGoFiles(t *testing.T) {
m := map[string]bool{
"testdata/foo/1.go": true,
"testdata/foo/2/2.go": true,
"testdata/foo/bar/3/3.go": true,
"testdata/foo/bar/4.go": true,
}
mfs := fstest.MapFS{
"testdata/foo/1.go": {Data: []byte("package foo\n")},
"testdata/foo/1/1.txt": {Data: []byte("1111\n")},
"testdata/foo/2/2.txt": {Data: []byte("2222\n")},
"testdata/foo/2/2.go": {Data: []byte("package bar\n")},
"testdata/foo/bar/3/3.go": {Data: []byte("package zoo\n")},
"testdata/foo/bar/4.go": {Data: []byte("package zoo1\n")},
}
files, err := FindGoFiles("testdata/foo", mfs)
if err != nil {
t.Errorf("want nil, actual %s", err)
}
if len(files) != 4 {
t.Errorf("want 4, actual %d", len(files))
}
for _, f := range files {
_, ok := m[f]
if !ok {
t.Errorf("want [%s], actual not found", f)
}
}
}
```


由于FindGoFiles接受了fs.FS类型变量作为参数，使其可测性显著提高，我们可以通过代码来构造测试场景，而无需在真实物理磁盘上构造复杂多变的测试场景。

### 4. 小结

io/fs的加入让我们易于面向接口编程，而不是面向os.File这个具体实现。**io/fs的加入丝毫没有违和感，就好像这个包以及其中的抽象在Go 1.0版本发布时就存在的一样**。这也是Go interface隐式依赖的特质带来的好处，让人感觉十分得劲儿！

本文中涉及的代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/iofs)下载。https://github.com/bigwhite/experiments/tree/master/iofs

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

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

## 评论