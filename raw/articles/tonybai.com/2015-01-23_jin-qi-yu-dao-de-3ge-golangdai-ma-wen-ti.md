---
title: 近期遇到的3个Golang代码问题
url: https://tonybai.com/2015/01/23/three-issues-about-go-code/
published: '2015-01-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 近期遇到的3个Golang代码问题

这两周来业余时间都在用[Golang](http://tonybai.com/tag/golang)写代码，现在处于这样一个状态：除了脚本，就是Golang了。反正能用golang实现的，都用golang写。

Golang语言相对成熟了，但真正写起来，还是要注意[一些“坑”](http://tonybai.com/2015/01/13/a-hole-about-variable-scope-in-golang/)的，下面是这周遇到的三个问题，这里分享出来，希望能对遇到同样问题的童鞋有所帮助。

**一、误用定时器，狂占CPU**

golang中有一个通过[channel](http://tonybai.com/2014/09/29/a-channel-compendium-for-golang/)实现timeout或tick timer的非常idiomatic的方法，代码如下：

func worker(start chan bool) {

for {

**timeout := time.After(30 * time.Second)**

select {

// … do some stuff

case <- timeout:

return

}

}

}

func worker(start chan bool) {

for {

**heartb****eat**** := time.Tick(30 * time.Second)**

select {

// … do some stuff

case <- heartbeat:

return

}

}

}

没错，就像上面这两个例子，如果你单独执行它们，你不会发现任何问题，但是当你将这样的代码放到一个7 * 24小时的Service中，并且timeout间隔或heartbeat间隔为更短时间，比如1s时，问题就出现了。

我的程序最初就是用上面的代码实现了一个timewheel，通过放置在一个单独goroutine中的定时器检测timewheel是否有到期的 timer。程序跑在后台运行的很好，直到有一天晚上我无意中执行了一下top，我发现这个service居然站用了40%多的CPU负荷。最初我怀疑是 不是代码中有死循环，但仔细巡查一遍代码后，没有发现死循环的痕迹，算法逻辑也没问题。

于是重启了一下这个service，发现cpu占用降了下来。出去去了趟卫生间，回来继续用top观察，不好，这个service占用了1%的CPU，再 过一会升到2%，观察一段时间后，发现这个service对cpu的占用率随着时间的推移而增加。gdb attach了相应的进程号，stack多是go runtime的调度。

再次回到代码，发现可能存在问题的只有这里的tick。我的tick间隔是1s。这样每1s都会创建一个runtime timer，而通过runtime的源码来看，这些timer都扔给了runtime调度(一个heap)。时间长了，就会有超多的timer需要 runtime调度，不耗CPU才怪。

于是做了如下修改：

func worker(start chan bool) {

**heartbeat := time.Tick(****1**** * time.Second)**

for {


select {

// … do some stuff

case <- heartbeat:

return

}

}

}

重新编译执行service，观察了一天，cpu再也没有升高过。

**二、小心list.List的Dele****te逻辑**

其实这是一个在哪种语言中都会遇到的初级问题，这里只是给大家提个醒罢了。不多说了，上代码：

从一个list.List中删除一个element，一般逻辑是：

l := list.New()

… …

for e := l.Front(); e != nil; e = e.Next() {

if e.Value.(int) == someValue {

l.Remove(e)

return or break

}

}

但是如果list里有重复元素，且代码要遍历整个list删除某个值为somevalue的元素呢？上面的一般方法是由逻辑缺陷的，例子：

func foo(i int) {

l := list.New()

for i := 0; i < 9; i++ {

l.PushBack(i)

}

**l.PushBack(6)**

for e := l.Front(); e != nil; e = e.Next() {

fmt.Print(e.Value.(int))

}

for e := l.Front(); e != nil; e = e.Next() {

if e.Value.(int) == i {

l.Remove(e)

}

}

fmt.Printf("\n")

for e := l.Front(); e != nil; e = e.Next() {

fmt.Print(e.Value.(int))

}

fmt.Printf("\n")

}

func main() {

foo(6)

}

该程序试图删除list中的所有值为6的element，但执行结果却是：

go run testlist.go

0123456786

012345786

list中尾部的那个6没有被删除，程序似乎在删除完第一个6之后就不再继续循环了。事实也是这样：

当l.Remove(e)执行后，e.Next()被置为了nil，这样循环条件不再满足，循环终止。

为此，对于这样的程序，下面的方法才是正确的：

func main() {

bar(6)

}

func bar(i int) {

l := list.New()

for i := 0; i < 9; i++ {

l.PushBack(i)

}

l.PushBack(6)

for e := l.Front(); e != nil; e = e.Next() {

fmt.Print(e.Value.(int))

}

var next *list.Element

for e := l.Front(); e != nil; {

if e.Value.(int) == i {

next = e.Next()

l.Remove(e)

e = next

} else {

e = e.Next()

}

}

fmt.Printf("\n")

for e := l.Front(); e != nil; e = e.Next() {

fmt.Print(e.Value.(int))

}

fmt.Printf("\n")

}

执行结果：

$ go run testlist.go

0123456786

01234578

**三、要给template起个正确的名字**

编写一个Web程序，需要用到html/template。

… …

t := template.New("My Reporter")

t, err = t.ParseFiles("views/report.html")

if err != nil {

w.WriteHeader(http.StatusInternalServerError)

return

}

t.Execute(w, UserInfo{xx: XX})

结果一执行却crash了：

[martini] PANIC: runtime error: invalid memory address or nil pointer dereference

/usr/local/go/src/runtime/panic.go:387 (0×16418)

/usr/local/go/src/runtime/panic.go:42 (0x1573e)

/usr/local/go/src/runtime/sigpanic_unix.go:26 (0x1bb50)

/usr/local/go/src/html/template/template.go:59 (0x7ed64)

/usr/local/go/src/html/template/template.go:75 (0x7ef0d)

/Users/tony/Test/GoToolsProjects/src/git.oschina.net/bigwhite/web/app.go:104 (0x2db0)

reportHandler: t.Execute(w, UserInfo{xx: XXX})

问题在t.Execute这行，单独把template代码摘出来放在一个测试代码中:

//testtmpl.go

type UserInfo struct {

Name string

}

func main() {

t := template.New("My Reporter")

t, err := t.ParseFiles("views/report.html")

if err != nil {

fmt.Println("parse error")

return

}

err = t.Execute(os.Stdout, UserInfo{Name: "tonybai"})

if err != nil {

fmt.Println("exec error", err)

}

return

}

执行结果：

go run testtmpl.go

exec error template: My Reporter: "My Reporter" is an incomplete or empty template; defined templates are: "report.html"

看起来似乎template对象与模板名字对不上导致的错误啊。修改一下：

t := template.New("report.html")

执行结果：

<html>

<head>

</head>

<body>

Hello, tonybai

</body>

</html>

这回对了，看来template的名字在与ParseFiles一起使用时不是随意取的，务必要与模板文件名字相同。

ParseFiles支持解析多个文件，如果是传入多个文件该咋办？godoc说了，template名字与第一个文件名相同即可。

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

mark 一下 http://tonybai.com/2015/01/23/three-issues-about-go-code/

关于第1个问题，这应该是很明显可以看出来的吧？Tick的含义是定时触发，只需要一个就行了。如果放在循环内，必然是每次循环就创建一个Timer。这后果是可想而知的。

ssss

请问下第一个问题在1.8还会出现吗？

下面这种写法有问题吗？

for _ = range time.Tick(time.Second)

仍然会啊。这个是用法问题，创建了太多的ticker没有释放。你这种用法应该没有什么问题，只是创建了一个ticker而已。

第一个问题建议在用 time.NewTicker 创建 Ticker，然后加一个 defer 来 Close，如果直接用 time.Tick 的话在 consumer goroutine 退出的时候 Ticker 不会被 GC，可能造成泄露。可以用 pprof 观察，会发现如果不 Close， goroutine 退出后依然存在 time.sendTime / runtime.epollwait。