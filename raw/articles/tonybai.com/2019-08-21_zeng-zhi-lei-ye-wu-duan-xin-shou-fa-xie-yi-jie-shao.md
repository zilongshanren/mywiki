---
title: 增值类业务短信收发协议介绍
url: https://tonybai.com/2019/08/21/introduction-on-tech-protocol-of-transfering-value-added-sms/
published: '2019-08-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 增值类业务短信收发协议介绍

在上一篇[《增值类短信业务图文简介》](https://tonybai.com/2019/08/20/introduction-to-value-added-sms-in-graphic-form/)中，我们介绍了什么是增值类短信业务以及增值类短信的收发流程。在这篇中我们将进一步深入介绍增值类短信收发协议的相关内容，不过重点放在短信内容编码对短信呈现的影响。

从近两年大火的5G我们可以看到，在移动通信领域**规范和标准先行**。虽然第一条短信在1992年在实验室就被发了出来，但是这离真正的短信商用还有很长一段距离。之后作为GSM(Global System for Mobile Communications，全球移动通信系统)技术的一个组成部分，[GSM规范](https://www.ietf.org/rfc/rfc5724.txt)中对短信内容编码格式作了进一步说明：

-
SMS消息内容的最大长度为160个字符（GSM字符集中的7比特字符）或140个八位字节，也可以支持其他

[字符集](https://tonybai.com/2007/11/03/also-talk-about-char-encoding/)，例如UCS-2的16位编码的字符，最多支持70个UCS-2字符长度的消息。处理SMS消息的应用程序必须确保争取的[字符集映射](https://tonybai.com/2007/11/03/also-talk-about-char-encoding/)。 -
SMS消息的接收者不必是移动电话。它可以是一个可以通过网关来处理SMS消息的服务器。 SMS消息可用于传输几乎任何类型的数据（虽然有一个非常严格的大小限制），唯一标准化的是其

**基于字符的数据格式**，字符按照一定的字符集格式进行编码。SMS消息的最大长度为160个字符 （当使用7位字符编码时）或140 字节。但是，SMS消息可以连接起来以形成更长的消息。但如何连接在此GSM规范中并未规范化的明确描述。

上面GSM规范中关于短信的约束和限制，显然是考虑了短信收发硬件设备、网络带宽等综合因素，**但这一约束一直延续至今**。当然在短信后续的发展中，通过对短信内容编码格式的扩展，丰富了短信的内容的展现形式，使短信尽可能的满足各种场景的需要。

## 一. 按短信内容呈现形式分类

短信内容的呈现形式是通过设置短信协议控制字段、短信内容编码和短信内容共同实现的。我们日常常见的三种短信内容形式如下：

- 普通短信

![img{512x368}](../../assets/1bd5ebc0dd0b7d9b.png)


普通短信是指短信内容在70个中文字符以内（含70个字符，采用UCS-2编码或GB2312编码）或160个英文字符以内（含160个字符，采用7比特字符编码）的短信。由于国内工信部要求发送给手机用户的增值类短信必须有“签名”（比如上面截图中的短信开始处的【美团点评】），因此短信实际承载内容要少于70个中文字符或160个英文字符（7bit编码字符）。因此，一旦SP要发送超过如此规定长度的短信，那么普通短信将无法满足,这就有了下面级联短信的需求。

- 级联短信（俗称长短信）

![img{512x368}](../../assets/d6ea95670ce56b6d.png)


对于普通手机用户来说，你可能不会注意到级联短信和普通短信的差别，因为到达手机后，这两种短信都以一条短信的形式呈现，只是级联短信内容较长罢了。我们看到手机上呈现的级联短信虽然是一条，但是其长度已经远超出上述GSM对短信内容长度的规定，这样的短信其实是在手机侧合成的。当某个SP要给某手机用户发送长度超出单条普通短信内容承载长度的短息时，会将超长内容拆分为多条有一定关联性的短信下发。这批短信被手机用户的终端接收后，终端会根据其关联关系将这批短信合并为一条短信显示出来。具体的细节在下面介绍短信协议内容时会详细说明。

- WAPPUSH短信

![img{512x368}](../../assets/28969e3552c8a812.png)


注意这是一条垃圾短信。现在通过wappush短信发送垃圾信息也是一种趋势，运营商正在这方面加强防范和堵漏。

WAPPUSH短信是一类特殊格式的短信，它诞生于2.5G时代，那个时候通过手机浏览互联网尚不十分方便，流量贵，带宽还窄。一些服务为了方便手机用户能快速定位到自己的页面，便将携带服务url的内容通过短信下发给手机用户。手机用户点击链接即可打开服务页面。这类短信还可以在用户阅读WAPPUSH短信时自动加载服务页面，而无需用户手动点击内容中的链接。

彩信通知也是通过这种方式下发到手机用户的。这样手机用户既可以在查看短信时自动在手机上下载并查看彩信，也可以手动点击彩信通知短信中的链接，打开存储彩信内容的服务页面查看彩信内容。

上面是目前可以见到的最常见的三类短信形式，当然还有类似**闪信**等不太常见的短信呈现形式，这里就不重点描述了。

## 二. 短信相关规范

在[上一篇文章](https://tonybai.com/2019/08/20/introduction-to-value-added-sms-in-graphic-form/)中，我们说过SP是通过各大运营商的专用协议连接到运营商的短信网关进行增值类短信下发的，这里就以中国移动的[CMPP协议(China Mobile Peer to Peer)](https://tonybai.com/wp-content/uploads/sms/CMPP3.0.pdf)为例（版本3.0)进行举例说明。

CMPP是在TCP之上的**基于请求-响应的应用层通信协议**，从内容上看，它改编自SMPP规范，但对暴露给SP的字段做了进一步约束；增加了运营商对短信计费相关字段。我们要关注的是CMPP协议的submit包。submit包是SP向短信网关发送的承载短信的协议包，一个submit包可以理解为最终到达手机用户的一条短信（当然submit包也支持群发）。

### 1. tp_udhi（用户数据头指示器）

这里我们重点关注的是协议字段对短信内容呈现的影响。**在CMPP submit包中，字段tp_udhi（用户数据头指示器）、msg_fmt（内容编码格式）、msg_length（内容长度）和msg_content（短信内容）**对网关解析短信、手机解析并呈现短信起到了至关重要的作用，因为这几个字段将被后续处理短信的各个网元“透传”直至手机上，并影响着手机对所接受到的短信的解析和呈现。

CMPP规范描述tp_udhi字段时提到了参考** GSM03.40 中的 9.2.3.23**。在

[《图解3GPP规范文档组织结构与编号规则》](https://tonybai.com/2019/07/25/illustrate-3gpp-spec-docs-structure-and-numbering)一文中，我们提到过03.40中的03系列文档仅适用于早期GSM系统，如今已经进化到4G、5G时代，我们可以直接参考对应该规范的新版规范

[23.040](https://www.3gpp.org/DynaReport/23040.htm)，你也可以看到23.040和03.40的

**Title是一致的**，都是”Technical realization of the Short Message Service (SMS)”。

我们直接打开23.040（这里使用的版本是v12.2.0)文档，定位到9.2.3.23小节，我们看到的就是对tp_udhi字段的说明。在3GPP规范中，tp_udhi只是短信协议数据单元（PDU）第一个字节中的一个bit位，它只有两个值：0和1。当我们将cmpp submit包中的tp_udhi设置为1时，3GPP中短信PDU中的tp_udhi bit位将被置为1，也就是表明在短信内容中携带有**短信头结构**。如果为0，则内容里不包含短信头结构：

```
判断逻辑：
tp_udhi bit位是否置为 1?
no -> 普通短信；
yes -> 内容带有短信头结构的短信（可能是级联短信、可能是wappush短信）
```


对于普通短信，短信接收侧仅需要根据msg_fmt、msg_length对短信内容进行解析呈现即可。但对于带有短信头结构的短信（tp_udhi bit位置1），还需要进一步分析。

### 2. 短信内容中的用户短信头结构

用户短信头结构是一组类TLV格式的数据段。注意这里明确是一组，也就是说短信内容头中支持放置多个数据段（如下图中的part1~partN)。

![img{512x368}](../../assets/2d5f0a0a9b08526c.png)


如图所示，cmpp submit的msg_length标识了整个短信内容的长度。如果tp_udhi被置为1，即短信内容中包含短信头结构，那么短信内容的第一个字节是UDHL，即后面短信头的长度。短信头可由多个part组成，每个part都是一个类TLV格式的连续数据：IEI、IEIDL、IED。IEI：信息元素标识符，大小为一个字节，相当于TLV中的T(Type)；IEIDL(信息元素数据长度)指示本part中IED的长度，相当于TLV中的L；IED（信息元素数据）是本part中承载的有价值数据，相当于TLV中的V。

3GPP 23.040定义了一组已知的IEI标准值(9.2.3.24)，我们从中取出几个我们关心的：

-
0×00 – Concatenated short messages, 8-bit reference number

-
0×04 – Application port addressing scheme, 8 bit address

-
0×05 – Application port addressing scheme, 16 bit address

-
0×08 – Concatenated short message, 16-bit reference number


其中0×00和0×08对应的是级联短信；0×04、0×05对应的是WAPPUSH消息，下面我们来逐一详细说明。

### 3. 级联短信

前面对级联短信做了简单的诠释：SP将超出普通短信长度的短信拆分为多条短信（每条短信称为该批次级联短信的一个segment），这些短信之间存在关联，当手机用户收到这些短信后，手机上的短信接收程序会将它们重新组装为一条长长的短信并呈现给用户。这里提到的“短信间的关联”就是通过附着在短信内容中的短信头结构实现的。

3GPP规范定义了将短信连接在一起形成更长短信的标准方式（参考23.040 9.2.3.24.1和9.2.3.24.8）。根23.040规范中的描述，IEI = 0×00和0×08的part是为级联短信服务的。但二者只能选择一种，不能共存。我们分别来说说：

#### 1) IEI = 0×00即reference number为一个字节的级联短信

![img{512x368}](../../assets/81091f9100e4b1a2.png)


上图是一个IEI=0×00的级联短信的例子。当短信为IEI=0×00级联短信的一个segment时，短信内容头部的IEIDL为0×03，IED由三部分组成，每个部分一个字节。它们依次是：

-
reference number – 该批次级联短信的唯一标识（0~255），手机端重组短信时，就是使用该字段将一批segment重组在一起的；

-
max number – 该批次级联短信共多少条（0~255）

-
sequence number – 当前短信segment是该批次级联短信的第几条（从1开始）,该字段用于在重组短信时为短信segment排序。（0~255）


#### 2) IEI = 0×08即reference number为两个字节的级联短信

![img{512x368}](../../assets/6220f677a2eaaaa6.png)


为了减少两条不同的级联短信因reference number的值空间过小导致ref number一致而冲突的情况，3GPP还增加了一个IEI=0×80的增强级联长短信类别。与8bit的ref number相比，仅仅是ref number的长度变长了,由一个字节变为两个字节（值空间由256个变为65536个）。而其他字段的位置和含义完全不变。这里就不赘述了。不过要注意的是打包或解析ref number时要注意[字节序](https://tonybai.com/2005/09/28/also-talk-about-byte-order/)转换。

### 4. 端口应用类短信

很多朋友会提出：上面图中每条消息的内容组成和网络协议栈怎么很相像呢？都是header + payload！没错！基于短信头结构，我们还可以通过在头结构中放置应用端口号，手机收到短信后，会根据目的应用端口将消息发送给对应的应用或启动对应的应用来处理这条短信，**而短信的内容(payload)则是应用所需的数据**，这类短信我称之为**端口应用类短信**。在3GPP 23.040的标准IEI定义表中，IEI=0×04和IEI=0×05就是用于在短信头中携带应用端口信息的，两者不同的是端口号所占字节不同，IEI=0×04对应的port占用1个字节（端口号表示的值空间较小，最大255），而IEI=0×05对应的port占用2个字节（扩展了端口号表示的值空间，最大65535）。我们用一幅图来诠释一下IEI=0×04和IEI=0×05时，短信头结构的样式：

![img{512x368}](../../assets/0eabfa8943e2c9d1.png)


由于IEI=0×04对应的port值空间有限，因此在实际使用中并不广泛。更多的采用短信协议承载应用数据的使用的是IEI=0×05，即应用端口采用16bit表示。

WAPPush短信是端口应用类短信的一种，它属于基于短信递送网络(Bearer Network)实现的WAP协议族中的push类应用。所谓Push类应用是用于向驻留在WAP设备（比如手机）上的应用程序传输数据的。这和我们在上面的理解一致，通过短信向手机上的某些应用传递数据，短信内容（去头后）就是应用所需的数据。IANA list一些标准的服务名和端口，可以在[这里](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.txt)查询。

下面我们就以WAPPush类短信为例，看看要传输的应用数据是如何打包在一条短信的内容中的。

#### 1) WAP协议栈与短信的映射

我们即将从[3GPP规范](https://tonybai.com/2019/07/25/illustrate-3gpp-spec-docs-structure-and-numbering/)转换到[WAP相关规范](http://www.openmobilealliance.org/wp/Affiliates/WAP.html)。WAP（Wireless Application Protocol）是一套基于无线协议的应用协议栈。在2G或2.5G时代以及3G初期，它是无线网络应用的主流。下面是WAP的完整协议栈示意图(来自网络)，也可参考规范[《Wireless Application Protocol Architecture Specification》:wap-210-waparch-20010712-a.pdf](http://www.openmobilealliance.org/tech/affiliates/wap/wap-210-waparch-20010712-a.pdf)中的协议栈全图Figure-7（不过不是很清晰）：

![img{512x368}](../../assets/5b981b90f565f678.jpg)


接下来我们要明确WAP协议栈在wappush短信应用时是如何与短信进行映射的：

![img{512x368}](../../assets/4f207a851407dcaa.png)


在图中我们看到了WAP Push应用与短信的映射关系：

-
底层递送网络使用SMS；

-
Transport Layer即WDP对应到短信内容头部的一个IE part，在这部分数据中，我们能找到源port和目的port，这与IP网络协议栈中UDP十分类似（参考：

[《Wireless Datagram Protocol Specification](http://www.openmobilealliance.org/tech/affiliates/wap/wap-259-wdp-20010614-a.pdf)》WAP-259-WDP-20010614-a.pdf 6.3.1和6.3.2）。 -
安全层和Transaction layer被省略了，暂无对应。

-
WSP(Session layer)对应到短信内容头之后的第一段自定义数据段。这段数据的形式由Type字段确定。以Push类(type=0×06)为例，这段数据包含：tid, type,headerslen,contenttype,headers和data。而data就是真正应用层的数据。（参考：

[《Wireless Session Protocol Specification》](http://www.openmobilealliance.org/tech/affiliates/wap/wap-230-wsp-20010705-a.pdf)WAP-230-WSP-20010705-a.pdf 8.1.2、8.2.1、8.2.4.1、8.4.1) -
WAE（application layer)对应的就是wsp承载的data字段，以push为例，这里存放的是应用所需的数据。这里的数据究竟是什么，要根据wsp层的ContentType确定。如果是 “application/vnd.wap.mms-message”，那么data中存放的就是mms notification(彩信通知短信）。


#### 2) WSP PDU介绍

这里把WSP PDU单独介绍一下，该PDU的字段涉及的内容还是略微复杂的。下面是一个push类的WSP PDU的构成字段示意图：

![img{512x368}](../../assets/57d53aee22623f35.png)


-
TID – Transaction ID uint8类型，标识该PDU所属transaction；

-
Type – 标识PDU的类型，uint8类型。该字段直接决定了该PDU后面的数据组成格式。WAP规范定义了标准的Type值列表，可参考：

[《Wireless Session Protocol Specification》](http://www.openmobilealliance.org/tech/affiliates/wap/wap-230-wsp-20010705-a.pdf)附录A 表34 PDU Type Assignments；这里我们用push类型举例，因此该字段为0×06。

接下来的数据字段是Push类型wsp pdu特有的，其他type pdu会有不同，但构成类似。熟悉了push类型的pdu字段的解析方式后，其他type的pdu也不是问题了。

-
HeadersLen 这个字段指示了push类pdu的header的长度：包括后面的ContentType和Headers的长度之和。值得注意的是该字段是uintvar类型，这是一种带有continue bit的7 bit编码的类型，其解析算法参见

[《Wireless Session Protocol Specification》](http://www.openmobilealliance.org/tech/affiliates/wap/wap-230-wsp-20010705-a.pdf)WAP-230-WSP-20010705-a.pdf 8.1.2。uintvar类型在WSP规范中大量出现，可以实现一个独立的函数来读取一个uintvar或写入一个uintvar，便于重用； -
ContentType 指示后面Data中的内容类型。ContentType是一个多字节的数据。它也是WSP PDU头部解析的一个难点。WSP要求客户机和服务器之间交换的信息都采用紧缩的编码格式，很多常见字段的name使用了well-known value作替代了，这样可以压缩存储空间，提高传输效率。ContentType字段本身就支持多种值格式，包括well-known value，变长字节数据(以uintvar开头的)或纯文本字符串形式。在WAP-230-WSP-20010705-a.pdf的 8.4.2.24小节有关于ContentType字段值格式的定义。在8.4.1.2中有关于header中field value第一个octet的值以及对应的含义，以帮助你解析Header field value，ContentType也是一个Header field value。这里摘录如下：


```
the first octet in all the field values can be interpreted as follows:
Value Interpretation of First Octet
0 - 30 This octet is followed by the indicated number (0 ¨C30) of data octets
31 This octet is followed by a uintvar, which indicates the number of data octets after it
32 - 127 The value is a text string, terminated by a zero octet (NUL character)
128 - 255 It is an encoded 7-bit value; this header has no more data.
```


因此，解析ContentType我们要区分多种情况。

#### 3) ContentType解析举例

我们以两种情况为例，一种是Well-known value形式; 另外一种形式是text string形式。

先来看Well-known value形式。如果我们解析到ContentType时遇到一组字节：03AE81EA。

-
0×03在[0,30]范围内，按照WSP规范，这个0×03是一个是一个length，表明后面的三个octets都是ContentType的值。我们看到03后面的三个字节分别为0xAE、0×81和0xEA；

-
按照WSP规范8.2.4.1关于 Short-integer的定义：


```
Short-integer = OCTET
; Integers in range 0-127 shall be encoded as a one octet value with the most significant bit set ; to one (1xxx xxxx) and with the value in the remaining least significant bits.
```


位于[0,127]区间的数字，在编码这些数字的时候，需要将字节最高bit置1。因此，我们需要将0xAE、0×81和0xEA还原为原先的值，通过 n & 0x7F计算 还原为0x2E、0×01和0x6A。这三个值都是well-known value，我们需要查表找到其对应的含义。根据[content type assignment(WSP 附录Table 40)](http://www.wapforum.org/wina/wsp-content-type.htm)、parameter(WSP规范 附录Table 38)以及该parameter对应的assignment(WSP规范附录 Table 42)的顺序，我们分别在表中确定三个字节对应的text：

```
0x2E - "application/vnd.wap.sic"
0x01 - "Charset"
0x6A - "utf-8"
```


因此该ContentType的值的文本形式是：”application/vnd.wap.sic; charset=utf-8″。

我们再来看看ContentType直接采用文本形式值的情况，这种情况较为简单：

```
0x61, 0x70, 0x70, 0x6c, 0x69, 0x63, 0x61 , 0x74 , 0x69, 0x6f, 0x6e, 0x2f, 0x76, 0x6e, 0x64,
0x2e, 0x77, 0x61, 0x70, 0x2e, 0x6d, 0x6d, 0x73 , 0x2d , 0x6d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65, 0x00
```


该段数据的第一个字节为0×61，其值在[32, 127]区间内，表明这是一个以零值结尾的字符串。我们将其以字符形式输出，得到的是：”application/vnd.wap.mms-message”。

得到ContentType数据后，我们再结合HeaderLen字段的值，可以计算出后面的Headers的长度。Headers中可能有多个字段，其构成格式与解析方式与ContentType的类似，这里不赘述了。

#### 3) 应用数据举例：彩信通知消息介绍

在WSP头解析后，我们剩下的就是Data这个字段了。这个字段承载的是应用真正需要的数据。我们以ContentType=”application/vnd.wap.mms-message”为例，即彩信通知短信。来看看wappush承载的彩信通知短信的解析。

在[《Multimedia Messaging Service Encapsulation Specification》](http://www.openmobilealliance.org/tech/affiliates/wap/wap-209-mmsencapsulation-20020105-a.pdf) wap-209-mmsencapsulation-20020105-a.pdf 7.1 中有关于彩信通知短信字段编码的规则，彩信通知仅仅是包含彩信的Headers字段。因此，我们仅适用mms header的编码规则解析即可，这里摘录如下：

```
MMS-header = MMS-field-name MMS-value
MMS-field-name = Short-integer
MMS-value =
Bcc-value |
Cc-value | Content-location-value |... ...
```


彩信通知的字段列表在[《Multimedia Messaging Service Encapsulation Specification》](http://www.openmobilealliance.org/tech/affiliates/wap/wap-209-mmsencapsulation-20020105-a.pdf)规范的6.2小节。

有了之前ContentType的解析经验后，解析这些字段便轻车熟路了。要注意几点：

-
header field name的well-known value在

[《Multimedia Messaging Service Encapsulation Specification》](http://www.openmobilealliance.org/tech/affiliates/wap/wap-209-mmsencapsulation-20020105-a.pdf)规范的7.3小节表中 -
header field name都是short integer，因此要注意与上0x7F的转换，转换后的值与7.3小节表中的值进行比对。

-
某个具体header field的值的形式，是零值结尾字符串、uintvar还是特定值，查看对应header field的具体说明即可。


## 三. 小结

到这里我们了解了短信协议对短信内容在手机端呈现形式的影响，我们知道了级联短信让我们可以接收到超过70个汉字字符的超长短信，我们知道了通过短信承载wap push协议，我们可以让手机上的应用接收到服务数据（比如一个服务的url或是一条彩信的访问地址）甚至可以在打开短信的时候自动加载彩信，并在手机端呈现彩信内容。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论