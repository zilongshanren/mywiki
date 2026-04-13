---
title: 'Firefox 76: Audio worklets 以及其他更新 – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2020/05/firefox-76-audio-worklets/
author: Chris Mills
published: '2020-05-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

大家好，希望你們一切順心，身體健康。

你們總是期盼最愛的瀏覽器再度發行新版本，現在我們正式推出Firefox 76！在這個新版本中，我們新增了一些很棒的功能支援Web平台，例如在JavaScript的[Audio Worklets](https://developer.mozilla.org/docs/Web/API/AudioWorklet)和[ Intl優化](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl)。此外，我們也在Firefox DevTools中添加許多新工具，使開發的過程更加輕鬆且便利。

與往常一樣，請往點擊下方閱讀亮重點，或在下列文章中，瀏覽所有新增功能的完整列表：

## 新增開發人員工具

在此發行版本中的每個領域都有有趣的DevTools更新。在[ Firefox 開發者版本](https://www.mozilla.org/firefox/developer/)中可以預覽未來即將推出的新功能。

### 提升JavaScript生產力的技巧

Firefox JavaScript除錯的功能又更進一步了。

#### 忽略除錯工具中的特定檔案

通常除錯的作業只集中在可能包含錯誤根源的特定檔案上。透過使用「Blackbox」的功能，你可以告訴[除錯工具](https://developer.mozilla.org/docs/Tools/Debugger)忽略不需要除錯的檔案。

現在多虧[Stepan Stava](https://bugzilla.mozilla.org/user_profile?user_id=652974)設計的除錯工具列表，針對特定檔案進行除錯的動作也變得更簡單了。你可以忽略所選資料夾中或資料夾以外的檔案。只要搭配「設定directory root」就可以獲得絕佳的除錯體驗。

#### 匯出時收疊控制台中大型代碼

[控制台](https://developer.mozilla.org/docs/Tools/Web_Console)的[多行編輯模式](https://developer.mozilla.org/docs/Tools/Web_Console/The_command_line_interpreter#Multi-line_mode)非常適合較長的代碼。早期的反饋顯示用戶不希望在控制台匯出時出現重複的代碼，以免過於混亂。感謝[thelehhman](https://github.com/thelehhman)，現在多行代碼可以被巧妙地收疊，並依照需求展開。

#### 在呼叫堆疊複製完整URL

在除錯工具中可以複製棧，並在運行過程中共享截圖。這不僅有助於偵錯，也有助於交接給同事。為了向協作者提供錯誤的完整信息，現在[呼叫堆疊窗格](https://developer.mozilla.org/docs/Tools/Debugger/UI_Tour#Call_stack)功能選單中的「複製堆疊追蹤」可以複製完整的URL，而不僅僅是檔案名稱。

#### 在Firefox的JSON預覽中永遠提供「全部展開」的功能

JSON檔案的內見預覽功能使搜尋響應和瀏覽API端點變得更為容易。這也適用於大型文件，在大型文件中可以根據需要展開數據。感謝[zacnomore](https://github.com/zacnomore)的貢獻，現在都可以看到「全部展開」的功能。

### 更多網路檢查技巧

Firefox 76利用[網路監視器](https://developer.mozilla.org/docs/Tools/Network_Monitor)使取得網路訊息更為方便。

#### 在WebSocket檢查中新增Action Cable支援

WebSocket庫中使用多種格式來針對訊息進行編碼。為了能夠讀取它們，我們要確保它們負載的解析和格式化皆正確。在過去的發行版中，我們針對Socket.IO、SignalR和WAMP 新增[WebSocket訊息檢查](https://developer.mozilla.org/docs/Tools/Network_Monitor/Inspecting_web_sockets)的支援。多虧了[Uday Mewada](https://bugzilla.mozilla.org/show_bug.cgi?id=1590046)的貢獻，現在Action Cable訊息的格式化也已經完善。

#### 隱藏WebSocket控制框架

服務器和瀏覽器利用WebSocket控制框架來管理實時連接，但其中不包含任何數據。貢獻者[kishlaya.j](https://bugzilla.mozilla.org/show_bug.cgi?id=1566780)在默認情況下隱藏控制框架，讓除錯的過程更加通順。如果你需要查看它們，可以在已發送／已接收下拉列表中啟用。

#### 根據內容調整網路表格的大小

從掃描實時更新轉向關注特定數據點時，網絡請求和響應數據可能會不堪重負。透過自定義可見的網絡面板選單，可以在輸出時解決當前的問題。過去，這必須要一直拖移並調整大小。感謝[Farooq AR](https://twitter.com/Farooq_AR)，如同現代數據表格一樣，現在你只要雙擊表格的調整大小把柄，就可以調整表格的寬度以因應其內容。

#### 提升網路響應細節和複製功能

我們曾收到反饋，表示複製部分網絡數據用以分析的過程應該更加簡便。

除了加快渲染速度，並提升可靠性，現在網路細節的「響應」方面已經更為現代化，使檢查和複製的過程更加輕鬆。我們將在不久的將來使網絡分析在使用上更為容易。[謝謝你們的反饋！ ](https://twitter.com/FirefoxDevTools/status/1255209764541263872)

### 社群貢獻

[Laurențiu Nicola](https://bugzilla.mozilla.org/show_bug.cgi?id=1549773)透過將`--globoff`

添加至生成的命令中，使網絡請求選單更加可靠。`Copy as cURL`

[Patricia Lee](https://bugzilla.mozilla.org/show_bug.cgi?id=1612276)在控制台中添加「在檢查器中顯示」上下文選單選項，提供從記錄DOM元素跳轉到在DOM樹中位置的另一種方法。[sankalp.sans](https://bugzilla.mozilla.org/show_bug.cgi?id=1424863)改善[檢查器「變更」面板](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#Track_changes)中的複製格式。現在只要在規則之間插入空行就可以「複製CSS規則」，使得在編輯器中重複使用時更加輕鬆。[Basavaraj](https://bugzilla.mozilla.org/show_bug.cgi?id=1574456)修復了造成無法顯示包含「 +」的[網絡查詢參數](https://developer.mozilla.org/docs/Tools/Network_Monitor/request_details#Params)的問題。[Aarushivij](https://bugzilla.mozilla.org/show_bug.cgi?id=1339558)改善了[Network性能分析](https://developer.mozilla.org/docs/Tools/Network_Monitor/Performance_Analysis)的呈現方式，提升對小尺寸的感應靈敏度。

### 開發者版本新功能：CSS相容性面板

[開發者版本](https://www.mozilla.org/firefox/developer/)是Firefox的預發布渠道，可以提早體驗編程和平台功能。瀏覽器在默認模式中提供開發人員更多功能。我們希望在開發者版本中盡快添增新功能，並收集不同的反饋。重點如下：

最重要的是在開發者版本77中，我們正積極創造新的兼容性面板。除了通知你所有其他瀏覽器可能不支援的CSS屬性之外，你也可以透過檢測器進行瀏覽。

歡迎在體驗之後利用內建的「反饋」連結來回饋它運作的效果並提供我們進一步可以改進的地方。

## 網路平台更新

讓我們一起看看Firefox 77在Web平台方面的更新。

### Audio worklet

Audio worklet提供一套處理自定義JavaScript音頻代碼的有效方法。Audio worklet與其前身— [ ScriptProcessorNode](https://developer.mozilla.org/docs/Web/API/ScriptProcessorNode)之間的區別在於worklet的運作方式與Web worker相似，除了執行主執行序，也解決了先前性能的問題。

基礎的概念大致上如下：你先自訂[ AudioWorkletProcessor](https://developer.mozilla.org/docs/Web/API/AudioWorkletProcessor)處理進程，接著進行註冊。

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


在主腳本中加載處理器，並創建[ AudioWorkletNode](https://developer.mozilla.org/docs/Web/API/AudioWorkletNode)實例，然後傳遞處理器名稱。最後，將節點連接至音頻圖。

```
async function createAudioProcessor() {
const audioContext = new AudioContext()
await audioContext.audioWorklet.addModule('white-noise-processor.js')
const whiteNoiseNode = new AudioWorkletNode(audioContext, 'white-noise-processor')
whiteNoiseNode.connect(audioContext.destination)
}
```


閱讀[背景音頻處理指南—利用 AudioWorklet](https://developer.mozilla.org/docs/Web/API/Web_Audio_API/Using_AudioWorklet)以獲得更多訊息。

### 其他更新

除了worklet之外，我們也針對網路平台新增了一些其它的功能。

#### HTML `<input>`


對於值為周期性的控件類型，當`min`

的值比`max`

還大時，HTML [ <input>](https://developer.mozilla.org/docs/Web/HTML/Element/input)元素中的

[和](https://developer.mozilla.org/docs/Web/HTML/Element/input#attr-min)

`min`

[可以正常運作。（週期性的值以固定的時間間隔重複，從結尾又再度重複開始。）以輸入](https://developer.mozilla.org/docs/Web/HTML/Element/input#attr-max)

`max`

`date`

和`time`

為例，你可以指定時間範圍為下午11點至早上2點，因此這項功能非常方便。#### 優化`Intl`


[ Intl.NumberFormat](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat)、

[和](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat)

`Intl.DateTimeFormat`

[建構器選項中的](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat)

`Intl.RelativeTimeFormat`

`numberingSystem`

和`calendar`

現在在默認模式中皆為啟用狀態。試試看下方的範例：

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


#### Intersection observer

[ IntersectionObserver()](https://developer.mozilla.org/docs/Web/API/IntersectionObserver/IntersectionObserver) 構造器現在接受

[和](https://developer.mozilla.org/docs/Web/API/Document)

`Document`

[對象為root。在這個情況中，root這個區域的邊界盒則是基於以觀察為目的視區。](https://developer.mozilla.org/docs/Web/API/Element)

`Element`

## 瀏覽器附加工具

[Firefox Profiler](https://profiler.firefox.com/)這個工具可以協這分析和改善Firefox中站點的性能。當網路請求因附加工具的[blocking webRequest處理程序](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/webRequest/BlockingResponse)而被暫停時，它將會顯示標記。這對於開發阻擋內容的附加工具的開發人員特別有用，他們將能夠確保Firefox保持最高速度。

下方為Firefox profiler實際運作時的截圖：

![Firefox profiler extension UI](../../assets/9d5e920fb9762921.png)


## 結論

以上就是最新版的Firefox，希望你們喜歡這些新功能！與往常一樣，歡迎隨時提供反饋並在評論區中提出問題。

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.