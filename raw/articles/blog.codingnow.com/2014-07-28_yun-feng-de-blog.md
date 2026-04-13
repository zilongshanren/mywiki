---
title: 云风的 BLOG
url: https://blog.codingnow.com/2014/07/sproto.html
published: '2014-07-28'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### sproto 的实现与评测

这个周末，我实现了[上周设计的简化版 protocol buffers 协议](http://blog.codingnow.com/2014/07/ejoyproto.html) ，并重新命名为 [sproto](https://github.com/cloudwu/sproto) 。

在实现过程中，发现了许多编码格式上可以优化的地方，所以一边实现一边做调整，使结构更适合编码和解码，并且更紧凑。

做了如下改动：

由于这个东西主要 binding 到 lua 这样的动态语言中使用，所以我不需要按 Cap'n Proto 那样，直接访问编码后的数据结构（直接把数据结构映射为 C/C++ 对象），所以数据对齐是不必要的。

编码时的 tag 如果要求严格升序也可以更快的处理数据，减少实现的复杂度。数据段也要求按持续排列，且不准复用。这样可以让数据中有更多的 0 方便压缩。

把 boolean 数组按位打包的意义也不太大（会增加实现的复杂度）。

暂时先不实现 64bit id 的类型。（以后再加）

最终的 Wire Protocol 是这样的：

所有的数字编码都是以小端方式(little-endian) 编码。

打包的单位是一个结构体（用户定义的类型） 每个包分两个部分：1. 字段 2. 数据块

首先是一个 word n，描述字段的个数，接下来有 n 个 word 描述字段的内容。这个结构体的前半部分的长度就是 (n+1) * 2 字节。

字段的 tag 从 0 开始累加，每处理一个字段，将 tag 加一。

如果一个字段 v 为奇数，则把当前 tag 加上 (v-1)/2 + 1 ，并继续处理下一个字段值。 如果一个字段为 0 ，表示这个字段引用后面的一个数据块。 如果一个字段不为 0(且为偶数），这个字段的值为 v/2 - 1。（可以表示 [0, 32767] 的值）

接下来是被上面字段引用的数据块。

数据块用于描述字段中的大数据。它是由一个 dword 长度 + 字节串构成。通常用来表示数组或结构。大于 32767 的整数和负整数用 4 字节或 8 字节长的数据块表示(取决于需要和实现)。

数组的编码就是把同一类型的数据依次打包成数据块。如果是布尔数组，按 1 字节一个编码。如果是整数数组，它比较特殊，会根据需要打包成 4 字节或 8 字节一个数字；第一字节是 4 或 8 ，指明后面的整数宽度。

最后，数据中的 0 将被压缩的。压缩算法见[上一篇 blog](http://blog.codingnow.com/2014/07/ejoyproto.html) 。

我的实现分两部分：C 库，和 Lua 绑定。

C 库最主要的用途是用于其它语言的绑定，所以并没有提供类似 [pbc](https://github.com/cloudwu/pbc) 那样丰富的 api 。而仅仅提供了回调模式的 encode 和 decode 。

#define SPROTO_TINTEGER 0 #define SPROTO_TBOOLEAN 1 #define SPROTO_TSTRING 2 #define SPROTO_TSTRUCT 3 typedef int (*sproto_callback)(void *ud, const char *tagname, int type, int index, struct sproto_type *, void *value, int length); int sproto_decode(struct sproto_type *, const void * data, int size, sproto_callback cb, void *ud); int sproto_encode(struct sproto_type *, void * buffer, int size, sproto_callback cb, void *ud);

encode 的时候，将回调用户传入的 callback 函数，通知现在要打包哪个字段（tagname），以及数据的类型。如果数据类型为 `SPROTO_TSTRUCT`

，表示这是一个结构，这个时候有另一个参数 `sproto_type`

指明结构类型。用户可以递归调用 encode 编码。

callback 函数给出了 buffer 地址和长度，如果 buffer 长度不够，应该返回 -1 ；如果正确的打包，返回使用掉的 buffer 的长度。

如果需要打包的是一个数组，index 大于 0 ，表示要把数据打包到 tagname 指向的数组的 index 索引处（base 1）；对于非数组的数据，index 等于 0。

encode 函数本身不会分配任何内容，当你的 buffer 给的不够大时，请适当加大，再调用一次。

decode 的过程和 encode 类似，只不过这个时候，buffer 指针指向的是解码器解开的数据。callback 函数只需要把数据复制到 tagname 指明的位置即可。

这个库尚未全部完工，但基本功能都已经全了。我把 sproto 和我自己实现的 pbc 的 lua binding 做了一个简单的性能测试：

首先我定义了这个一组协议。

.Person { name 0 : string id 1 : integer email 2 : string .PhoneNumber { number 0 : string type 1 : integer } phone 3 : *PhoneNumber } .AddressBook { person 0 : *Person }

如果用 google protocol buffers 描述，大概长得是这样的：

message Person { required string name = 1; required int32 id = 2; // Unique ID number for this person. optional string email = 3; message PhoneNumber { required string number = 1; optional int32 type = 2 ; } repeated PhoneNumber phone = 4; } message AddressBook { repeated Person person = 1; }

完全一致，只是语法上略有区别而已。

我编写两段 [lua 代码](https://github.com/cloudwu/sproto/blob/master/test.lua)测试。处理以下数据：

local ab = { person = { { name = "Alice", id = 10000, phone = { { number = "123456789" , type = 1 }, { number = "87654321" , type = 2 }, } }, { name = "Bob", id = 20000, phone = { { number = "01234567890" , type = 3 }, } } } }

编码很简单，对于解码，另外还加上了遍历所有的字段，这是因为 pbc 库对于二级以上的结构是惰性展开的（不访问就不解码），而 sproto 则是全部展开。

| 编码 1M 次 | 解码 1M 次 | 体积 | |
| sproto | 3.18s | 14.30s | 83 bytes |
| sproto (nopack) | 2.45s | 13.20s | 130 bytes |
| pbc-lua | 11.71s | 30.60s | 69 bytes |
| lua-cjson | 19.46s | 15.17s | 183 bytes |

注1：解码比较慢，主要在于 lua 表结构的创建。另外遍历 lua 表的开销为 3.6s ，这块时间和解码无关。

注2：pbc-lua 解码比较慢，还在于它需要为每张表生成 metatable 以支持 default 值。

注3： protobuffer 的数据本身不带长度信息，实际使用时，必须再加上长度信息才可以正确解码。

另外，json 是 Schemaless 的，这种结构处理起来一定会快的多（处理 schema 需要额外的时间），所以放在一起比较是不公平的。同样 schmaless 的结构还有 bson msgpack 等等。

7 月 29 日补:

前面的测试在 mingw32 上完成 (CPU i5-2500 @3.3GHz) ，而操作系统是 Windows 7 (64 位) ，在 64 位系统下跑 32 位程序对测试结果有很大干扰。

今天重新在 Linux 3.8.0 64 位 上重新测试 (CPU E5-2407 0 @ 2.20GHz)

| 编码 1M 次 | 解码 1M 次 | 体积 | |
| sproto | 2.47s | 9.52s | 83 bytes |
| sproto (nopack) | 2.45s | 8.60s | 130 bytes |
| pbc-lua | 9.54s | 23.0s | 69 bytes |
| lua-cjson | 5.32s | 9.72s | 183 bytes |

7 月 30 日 补:

前面 mingw32 生成的代码在我的系统上有很大的性能问题，所以我用 mingw64 重新编译测试了一次：

| 编码 1M 次 | 解码 1M 次 | 体积 | |
| sproto | 2.15s | 7.84s | 83 bytes |
| sproto (nopack) | 1.58s | 6.93s | 130 bytes |
| pbc-lua | 6.94s | 16.9s | 69 bytes |
| lua-cjson | 4.92s | 8.30s | 183 bytes |

## Comments

Posted by: JackLeeDev | (22) March 28, 2026 04:19 PM

Posted by: 悲喜混合物 | (21) August 9, 2017 07:45 PM

Posted by: 王光汉 | (20) July 22, 2017 02:41 AM

Posted by: 在线一对一 | (19) April 28, 2016 06:04 PM

Posted by: 北京代孕 | (18) March 14, 2016 03:33 PM

Posted by: 中央财经大学在职研究生 | (17) September 9, 2015 10:29 AM

Posted by: serl | (16) September 3, 2015 06:14 PM

Posted by: 在线教育 | (15) June 23, 2015 02:29 PM

Posted by: 在线教育 | (14) June 23, 2015 02:29 PM

Posted by: 秋木耳 | (13) June 13, 2015 06:06 PM

Posted by: seo | (12) June 8, 2015 05:55 AM

Posted by: seo培训 | (11) April 6, 2015 04:15 PM

Posted by: xavierxia | (10) January 5, 2015 11:48 PM

Posted by: lili | (9) November 3, 2014 11:34 AM

Posted by: 文字控吧 | (8) August 25, 2014 09:52 PM

Posted by: 小米 proto | (7) August 21, 2014 09:28 PM

Posted by: Celebi | (6) August 21, 2014 02:26 PM

Posted by: Anonymous | (5) July 30, 2014 09:33 PM

Posted by: Cloud | (4) July 30, 2014 04:06 PM

Posted by: dwing | (3) July 29, 2014 11:17 AM

Posted by: Cloud | (2) July 28, 2014 08:16 PM

Posted by: Anonymous | (1) July 28, 2014 07:32 PM