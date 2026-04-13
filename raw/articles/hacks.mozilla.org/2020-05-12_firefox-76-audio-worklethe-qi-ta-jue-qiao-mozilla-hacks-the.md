---
title: Firefox 76：Audio Worklet和其他诀窍 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/05/firefox-76-audio-worklet/
author: Chris Mills
published: '2020-05-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

大家好，希望各位都平安顺遂。

对于深受用户喜爱的浏览器来说，新版本必定值得期待我们的Firefox 76终于面世了！Web平台支持在此版本中新增了许多精彩功能，例如[AudioWorklet](https://developer.mozilla.org/docs/Web/API/AudioWorklet)和JavaScript的[ Intl改进](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl)。另外，Firefox DevTools中也添加了诸多改进，让开发变得更加轻松快捷。

与往常一样，请继续阅读来了解重点内容，或从以下文章中查找所有新增功能的完整列表：

## 开发人员工具补充

在这个发行版本中，DevTools的每个面板都有值得关注的更新。另外，也可通过[Firefox Dev Edition](https://www.mozilla.org/firefox/developer/)预览即将推出的功能。

### 更多JavaScript效率诀窍

Firefox JavaScript调试又上一个新台阶。

#### 在Debugger中忽略整个文件夹

许多时候，调试的重点仅放在那些存在纰漏的文件上。通过“放进黑箱”，您可以告诉[Debugger](https://developer.mozilla.org/docs/Tools/Debugger)忽略不需要调试的文件。

现在对于文件夹也能轻松办到，而这要归功于[Stepan Stava](https://bugzilla.mozilla.org/user_profile?user_id=652974)在Debugger的“Sources”面板中加入的上下文菜单。“忽略”的对象可被限制为选定文件夹里面或外面的文件。结合使用“Set directory root”，就能实现精准调试体验。

#### 折叠较长的Console代码片段输出

[Console](https://developer.mozilla.org/docs/Tools/Web_Console)的[多行编辑器模式](https://developer.mozilla.org/docs/Tools/Web_Console/The_command_line_interpreter#Multi-line_mode)完美适合迭代较长的代码片段。根据我们之前收到的反馈，用户不希望Console输出中看到重复的代码，以便能避免凌乱不堪。感谢[thelehhman](https://github.com/thelehhman)的贡献，现在能轻松折叠含有多行代码的代码片段，并可在需要时展开。

#### 复制调用堆栈中的完整URL

在Debugger中复制堆栈，轻松共享分步执行的快照。如此一来，提交Bug错误更加便捷，移交给同事也很方便。为了让合作者们获得Bug错误的完整上下文信息，[调用堆栈面板](https://developer.mozilla.org/docs/Tools/Debugger/UI_Tour#Call_stack)的“Copy stack trace”菜单现在可以复制完整的URL，而不仅仅是文件名。

#### Firefox的JSON预览中始终提供“Expand All”选项

通过内置的JSON文件预览功能，轻松搜索响应和探索API端点。这也适用于大文件，随时根据需要展开其中的数据。感谢[zacnomore](https://github.com/zacnomore)的贡献，“Expand All”选项现在始终可见。

### 更多网络检查诀窍

Firefox 76中的[Network Monitor](https://developer.mozilla.org/docs/Tools/Network_Monitor)让用户能够更加轻松地访问网络信息。

#### WebSocket检查中支持Action Cable

WebSocket库使用许多不同的格式来编码其消息。我们希望正确解析和格式化它们的有效负载，从而方便您阅读。在以前的发行版中，我们添加了对Socket.IO、SignalR和WAMP [WebSocket消息检查](https://developer.mozilla.org/docs/Tools/Network_Monitor/Inspecting_web_sockets)的支持。感谢[Uday Mewada](https://bugzilla.mozilla.org/show_bug.cgi?id=1590046)的贡献，Action Cable消息现在也能妥当地格式化。

#### 隐藏WebSocket控制帧

WebSocket控制帧供服务器和浏览器用于管理实时连接，但它们不含任何数据。[kishlaya.j](https://bugzilla.mozilla.org/show_bug.cgi?id=1566780)贡献了一个新思路，通过默认隐藏控制帧来为您的调试再减少一些干扰。当您需要查看时，也可在已发送/已接收下拉菜单中启用。

#### 调整Network表格列宽度来适配内容

在从浏览实时更新转向关注特定数据点时，网络请求与响应数据可能会令您烦恼不已。通过自定可见的Network面板列，您可以根据手边的问题来调整输出。这在过去需要许多拖放与大小调整操作才能实现。感谢[Farooq AR](https://twitter.com/Farooq_AR)的贡献，现在可以通过双击表格的大小调整手柄，像现代数据表中一样将列宽度调整为与内容匹配。

#### 更好的Network响应细节和复制

我们收到了反馈，用户希望能更加轻松地复制网络数据部分作进一步分析。

现在，Network详细信息中的“Response”部分得到了现代化，通过加快渲染速度并提高可靠性，使检查和复制变得更加轻松。因为有[大家的贡献](https://twitter.com/FirefoxDevTools/status/1255209764541263872)，我们很快会给Network分析添加更多易用性改进。

### 社区贡献

[Laurențiu Nicola](https://bugzilla.mozilla.org/show_bug.cgi?id=1549773)在生成的命令中添加了`--globoff`

选项，增强了网络请求[“Copy as cURL”](https://developer.mozilla.org/docs/Tools/Network_Monitor/request_list#Copy_as_cURL)菜单的可靠性。[Patricia Lee](https://bugzilla.mozilla.org/show_bug.cgi?id=1612276)在Console中添加了“Reveal in Inspector”上下文菜单选项，作为从记录的DOM元素跳转到DOM树中对应位置的另一途径。[sankalp.sans](https://bugzilla.mozilla.org/show_bug.cgi?id=1424863)改进了[Inspector的“Changes”面板](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#Track_changes)中复制文本的格式。“Copying CSS Rules”现在会在规则之间插入空行，使它们能够在编辑器中更加方便地重新利用。[Basavaraj](https://bugzilla.mozilla.org/show_bug.cgi?id=1574456)解决了造成[Network查询参数](https://developer.mozilla.org/docs/Tools/Network_Monitor/request_details#Params)含有“+”时无法显示的问题[Aarushivij](https://bugzilla.mozilla.org/show_bug.cgi?id=1339558)攻克了[Network性能分析](https://developer.mozilla.org/docs/Tools/Network_Monitor/Performance_Analysis)，使其能够更加灵敏地响应较小的规模

### Dev Edition新增功能：CSS兼容性面板

[Developer Edition](https://www.mozilla.org/firefox/developer/)是Firefox的预发布渠道，可以抢先体验各种工具和平台功能。该版本的默认设置中为开发人员开启了更多功能。我们乐于将新功能快速引入Developer Edition，以便收集反馈信息，重点包括以下内容。

首先，我们期盼大家对Dev Edition 77中新兼容性面板谏言纳策。此面板会告知可能在其他浏览器中不受支持的CSS属性，可以通过Inspector来访问。

您不妨试验一下，并使用“Feedback”链接分享它给您的体验，告诉我们如何能进一步改进。

## Web平台更新

我们来看看Firefox 77在网络平台更新方面带来了什么。

### Audio Worklet

Audio Worklet提供了一种运行JavaScript音频处理代码的实用方法。Audio Worklet与其前代[ ScriptProcessorNode](https://developer.mozilla.org/docs/Web/API/ScriptProcessorNode)的区别在于，Worklet通过与Web工作进程相似的方式从主线程中运行，解决了过去遇到的性能问题。

基本思路是：定义一个用于负责音频处理的[ AudioWorkletProcessor](https://developer.mozilla.org/docs/Web/API/AudioWorkletProcessor)，再将它注册。

```
// white-noise-processor.js
class WhiteNoiseProcessor extends AudioWorkletProcessor {
process (inputs, outputs, parameters) {
const output = outputs[0]
output.forEach(channel => {
for (let i = 0; i < channel.length; i++) {
channel[i] = Math.random() * 2 - 1
}
})
return true
}
}
registerProcessor('white-noise-processor', WhiteNoiseProcessor)
```


接着在您的主脚本中，加载此处理器，创建一个[ AudioWorkletNode](https://developer.mozilla.org/docs/Web/API/AudioWorkletNode)实例，并将处理器名称传递给这个实例。最后，将节点与音频图表连接。

```
async function createAudioProcessor() {
const audioContext = new AudioContext()
await audioContext.audioWorklet.addModule('white-noise-processor.js')
const whiteNoiseNode = new AudioWorkletNode(audioContext, 'white-noise-processor')
whiteNoiseNode.connect(audioContext.destination)
}
```


如需更多信息，请阅读我们有关[使用 AudioWorklet进行后台音频处理](https://developer.mozilla.org/docs/Web/API/Web_Audio_API/Using_AudioWorklet)的指南。

### 其他更新

除了Worklet外，我们还添加了一些Web平台功能。

#### HTML `<input>`


对于值为期间的控制类型，HTML [ <input>](https://developer.mozilla.org/docs/Web/HTML/Element/input)元素的

[和](https://developer.mozilla.org/docs/Web/HTML/Element/input#attr-min)

`min`

[属性在](https://developer.mozilla.org/docs/Web/HTML/Element/input#attr-max)

`max`

`min`

值大于`max`

值时现在也能正常运作。（期间值以固定间隔重复，达到终点时轮回到起点。）这对于`date`

和`time`

输入特别有用；例如，指定一个从11 PM到2 AM的时间范围。`Intl`

改进

[ Intl.NumberFormat](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat)、

[和](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat)

`Intl.DateTimeFormat`

[构造函数的](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat)

`Intl.RelativeTimeFormat`

`numberingSystem`

和`calendar`

选项现已默认启用。不妨试试下面的示例：

```
const number = 123456.789;
console.log(new Intl.NumberFormat('en-US', { numberingSystem: 'latn' }).format(number));
console.log(new Intl.NumberFormat('en-US', { numberingSystem: 'arab' }).format(number));
console.log(new Intl.NumberFormat('en-US', { numberingSystem: 'thai' }).format(number));
var date = Date.now();
console.log(new Intl.DateTimeFormat('th', { calendar: 'buddhist' }).format(date));
console.log(new Intl.DateTimeFormat('th', { calendar: 'gregory' }).format(date));
console.log(new Intl.DateTimeFormat('th', { calendar: 'chinese' }).format(date));
```


#### IntersectionObserver函数

[ IntersectionObserver()](https://developer.mozilla.org/docs/Web/API/IntersectionObserver/IntersectionObserver)构造函数现在接受

[和](https://developer.mozilla.org/docs/Web/API/Document)

`Document`

[对象作为其根。在这个语境中，根是指边界框被视为观察视口的区域。](https://developer.mozilla.org/docs/Web/API/Element)

`Element`

## 浏览器扩展

[Firefox Profiler](https://profiler.firefox.com/)是一款可用于分析和改进网站在Firefox中性能的工具。现在，它可以在网络请求被[ webRequest拦截处理程序](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/webRequest/BlockingResponse)暂挂时显示标记。这对于内容拦截扩展开发人员而言特别有用，方便他们确保Firefox保持快速运行。

下图是Firefox Profiler实际运行的一个截图：

![Firefox Profiler扩展UI](../../assets/9d5e920fb9762921.png)


## 总结

以上就是Firefox的最新版本，希望您能喜欢这些新功能！与过去一样，欢迎您随时留言反馈并提出疑问。

结束。

摘录：

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.