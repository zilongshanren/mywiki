---
title: Firefox 74，為安全賦予更多價值 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/03/security-firefox-74/
author: Chris Mills
published: '2020-03-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

目前Firefox 74已經發布了。這次我們提供最重要的新功能是安全性的提升：特徵策略（Feature Policy），`Cross-Origin-Resource-Policy`

標頭和移除TLS 1.0 / 1.1支援。我們還新增一些新的CSS文本屬性功能，JS鏈接運算符還有其他2D canvas文本度量標準功能，以及大量DevTools增強功能和錯誤修復功能。

本文同樣包含一些重點，你也可以在以下文章中閱讀新增功能的完整列表：

## 提升安全性

讓我們看看74版本中安全性的改良。

### 特徵策略（Feature Policy）

我們終於在默認模式中啟用[Feature Policy](https://developer.mozilla.org/docs/Web/HTTP/Feature_Policy/Using_Feature_Policy)。你現在可以使用`<iframe>`

`allow`

屬性還有[ Feature-Policy](https://developer.mozilla.org/docs/Web/HTTP/Headers/Feature-Policy) HTTP標頭設定頂級文檔和iframe功能權限。語法範例如下：

`<iframe src="https://example.com" allow="fullscreen"></iframe>`


`Feature-Policy: microphone 'none'; geolocation 'none'`


### CORP

我們也啟用支援[ Cross-Origin-Resource-Policy (CORP)](https://developer.mozilla.org/docs/Web/HTTP/Cross-Origin_Resource_Policy_(CORP))標頭，允許網站和應用程序因安全考量選擇拒絕針對某些跨域請求。例如：

`<script>`

和`<img>`

元素。這也可以幫助減少潛在的旁路攻擊（例如Spectre和Meltdown）以及跨網站指令碼包含攻擊。可用的屬性有`same-origin`

和`same-site`

。`same-origin`

僅允許擁有相同scheme，host和port的請求讀取相關資源。這和網絡的默認同源協定相比，提供更高級的保護。`same-site`

僅允許共享同一網站的請求。

可以將標頭依照以下範例運用CORP，例如：

`Cross-Origin-Resource-Policy: same-site`


### 移除TLS 1.0 / 1.1

最後，Firefox 74為了提升整體Web平台的安全性，取消支援TLS 1.0 / 1.1。這對於推動TLS生態系統的發展很重要，同時也可以消除TLS 1.0 / 1.1導致的許多漏洞。這項功能沒有像我們希望的那麼有效，它們需要退場了。

2018年10月在Mozilla，Google，Microsoft和Apple的共同倡議下，首次宣布這項變更。2020年3月，我們現在都兌現了我們的諾言（蘋果公司除外，蘋果公司稍後將進行變更）。

結論是你要確保你的Web服務器支持TLS 1.2或1.3。請閱讀[移除TLS 1.0 and 1.1更新](https://hacks.mozilla.org/2019/05/tls-1-0-and-1-1-removal-update/)了解如何測試和更新TLS / SSL配置。現在開始，Firefox將回傳[安全連線失敗（Secure Connection Failed）](https://support.mozilla.org/kb/secure-connection-failed-firefox-did-not-connect)錯誤訊息，你的服務器為較舊的TLS版本。如果你還沒升級的話，請點選**立即升級**！

![安全連線失敗錯誤訊息，您使用的服務器為TLS 1.0或1.1版本。（secure connection failed error message, due to connected server using TLS 1.0 or 1.1）](../../assets/b02e36f205b1a345.png)


**注意**：在未來幾個更新週期中（Firefox ESR跟新週期較長）， *安全連線失敗（Secure Connection Failed）*錯誤頁面將具有一個覆蓋按鈕，允許你在尚未升級服務器時，啟用TLS 1.0和1.1。但是你沒辦法一直用這個方法。

欲了解移除TLS 1.0 / 1.1與其背景的更多訊息，請閱讀

[以上是TLS 1.0和TLS 1.1的啟動程序。](https://hacks.mozilla.org/2020/02/its-the-boot-for-tls-1-0-and-tls-1-1/)

## 其他網路平台功能

在74版本中，我們提供了更多其他功能。

### CSS文字新功能

首先，默認模式中會啟用[ text-underline-position](https://developer.mozilla.org/docs/Web/CSS/text-underline-position)屬性。這項功能在一些情況下很方便，可以在文本中設定底線以達到特定的印刷效果。

舉例來說，如果你的[文字模式（writing-mode）](https://developer.mozilla.org/docs/Learn/CSS/Building_blocks/Handling_different_text_directions)是水平的，你可以利用`text-underline-position: under;`

在下標劃底線，這項功能經常運用於科學和數學公式的下標。

```
.horizontal {
text-underline-position: under;
}
```


如果[ writing-mode](https://developer.mozilla.org/docs/Web/CSS/writing-mode)是垂直的，則可以利用

`left`

或`right`

根據需求讓底線出現在文字的右方或左方。```
.vertical {
writing-mode: vertical-rl;
text-underline-position: left;
}
```


此外，[ text-underline-offset](https://developer.mozilla.org/docs/Web/CSS/text-underline-offset)還有

[的屬性現在也可以應用於百分比，例如：](https://developer.mozilla.org/docs/Web/CSS/text-decoration-thickness)

`text-decoration-thickness`

`text-decoration-thickness: 10%;`


以這些屬性來說，這是目前字體大小`1em`

的百分比。

### JavaScript中的可選鍵

現在JavaScript中有[可選鍵操作符](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Optional_chaining)(`?.`

)。當你試著取得鍵中下層的一個物件時，這項特性可以對鏈中較上層的物件的進行測試，除了可以避開錯誤，也不需要編寫測試代碼。

`let nestedProp = obj.first?.second;`


### 新的2D Text Metrics

[ TextMetrics](https://developer.mozilla.org/docs/Web/API/TextMetrics)介面（使用

[方法）已擴展為包含四個測量實際邊界框的更多屬性——](https://developer.mozilla.org/docs/Web/API/CanvasRenderingContext2D/measureText)

`CanvasRenderingContext2D.measureText()`

[,](https://developer.mozilla.org/docs/Web/API/TextMetrics/actualBoundingBoxLeft)

`actualBoundingBoxLeft`

[,](https://developer.mozilla.org/docs/Web/API/TextMetrics/actualBoundingBoxRight)

`actualBoundingBoxRight`

[, and](https://developer.mozilla.org/docs/Web/API/TextMetrics/actualBoundingBoxAscent)

`actualBoundingBoxAscent`

[。](https://developer.mozilla.org/docs/Web/API/TextMetrics/actualBoundingBoxDescent)

`actualBoundingBoxDescent`

例如：

```
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
const text = ctx.measureText('Hello world');
text.width; // 56.08333206176758
text.actualBoundingBoxAscent; // 8
text.actualBoundingBoxDescent; // 0
text.actualBoundingBoxLeft; // 0
text.actualBoundingBoxRight; // 55.733333333333334
```


## DevTools其他功能

接下來介紹DevTools的其他功能。

### 響應式設計模式（Responsive Design Mode）中類似設備的渲染

[Android版Firefox](https://blog.mozilla.org/futurereleases/2020/01/17/a-brand-new-browsing-experience-arrives-in-firefox-for-android-nightly/)搭載[GeckoView](https://mozilla.github.io/geckoview/)[變得更快，隱私方面也有所提升，](https://blog.mozilla.org/firefox/firefox-android-new-features/)而DevTools也需要與時俱進。在移動裝置上測試應該要盡可能提供順暢的體驗，在桌上型電腦使用 [響應式設計模式（Responsive Design Mode）](https://developer.mozilla.org/docs/Tools/Responsive_Design_Mode)，或在個人裝置上使用 [遠端偵錯（Remote Debugging）](https://developer.mozilla.org/docs/Tools/about:debugging)亦同。

正確性對於響應式設計模式很重要，即使開發人員手邊沒有設備對於輸出也可以很有信心。在先前發行的版本中，我們推出了重大改進，並確保正確地將[meta viewport](https://developer.mozilla.org/docs/Mozilla/Mobile/Viewport_meta_tag)應用於*觸碰模擬（Touch Simulation）*。這關係改良後移動裝置的預設模式，移動裝置會自動啟用觸碰模擬（Touch Simulation）。

![GIF動畫顯示響應式設計模式如何更優秀地顯示view meta設置。](../../assets/00f1ddda7748920e.gif)


有趣的事實：我們的團隊模擬因為太過精確，現在已經幫助偵測並修復Android版Firefox的渲染錯誤。

**DevTools建議：**若不使用DevTools開啟響應式設計模式，可利用Windows的工具選單或Ctrl + Shift + M或macOS上的Ctrl + Opt + M。

我們期待聽到你們在網頁中使用RDM或是在Android手機使用[Firefox Nightly for Developers](https://play.google.com/store/apps/details?id=org.mozilla.fennec_aurora)的反饋。

### 你也可以上手的CSS工具

[Page Inspector](https://developer.mozilla.org/docs/Tools/Page_Inspector)針對無效CSS規則新的上下文警告已經得到很多正面的反饋。除了幫助你解決粗糙的CSS問題之外，也同時教你CSS規則的複雜相互依存關係。

自發布以來，我們經常根據用戶反饋持續調整並增加規則。 74的亮點之一就是新的檢測設定。當屬性取決於定位的元素時，該警告設定會提醒您，例如：[ z-index](https://developer.mozilla.org/docs/Web/CSS/z-index),

[,](https://developer.mozilla.org/docs/Web/CSS/top)

`top`

[,](https://developer.mozilla.org/docs/Web/CSS/left)

`left`

[, and](https://developer.mozilla.org/docs/Web/CSS/bottom)

`bottom`

[.](https://developer.mozilla.org/docs/Web/CSS/right)

`right`

![Firefox Page Inspector現在顯示無效的位置屬性，例如：z-index， top](../../assets/5744426e48f2a528.png)


你的反饋將幫助我們完善規則和進行擴展。你可以在[DevTools chat](https://chat.mozilla.org/#/room/#devtools:mozilla.org) on [或是 Mozilla’s Matrix instance](https://wiki.mozilla.org/Matrix) 和我們的團隊打聲招呼。你也可以在[@FirefoxDevTools](https://twitter.com/FirefoxDevTools)了解我們的近況。

### Nested Workers偵錯工具

Firefox的[JavaScript Debugger](https://developer.mozilla.org/docs/Tools/Debugger) 除錯團隊在過去的幾個版本中一直致力於改善[Web Workers](https://developer.mozilla.org/docs/Web/API/Web_Workers_API/Using_web_workers)，降低偵測與排除錯誤的難易度。使用workers完成主要執行緒的開發人員和框架越多，瀏覽器就越有可能根據用戶的操作優先執行特定運行代碼。

Nested web workers允許工作程序產生並控制自己的工作程序。除錯工具中顯示如下：

![Firefox JavaScript除錯工具與nested workers範例](../../assets/3b6dccb9bd207706.png)


### 提升React DevTools的整合

[React Developer Tool附加工具](https://addons.mozilla.org/firefox/addon/react-devtools/)是其中一個和Firefox DevTools合作密切的[開發人員附加工具](https://addons.mozilla.org/firefox/collections/4757633/webdeveloper/) that integrate tightly with Firefox DevTools. 利用[瀏覽器擴充功能](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions)，開發人員可以為同一個代碼庫的瀏覽器自行創造並發行附加工具。

透過和React附加工具維護人員的[合作](https://github.com/facebook/react/issues/17681)， 我們協力重新啟用並優化附加工具的選單，例如：*Go to definition*。這個動作可以讓開發人員從React Components直接跳轉到除錯工具的原始檔案。Inspector中也有同樣的功能，可以直接跳轉到指定元素。我們希望藉由這個功能，讓[框架](https://addons.mozilla.org/firefox/collections/4757633/webdeveloper/)和其他工具的運作更為流暢。

### 搶先體驗開發者版本DevTools功能

Firefox透過[開發者版本](https://www.mozilla.org/firefox/developer/)開放搶先體驗平台的一些特色。默認設定中也提供開發人員使用更多功能。我們希望盡快在開發者版本中加入新功能，並匯集您的反饋。以下為幾項重點：

#### 即時測試Console表達式

利用即時測試的功能，探索JavaScript的事件、函式和DOM感覺猶如魔法般神奇。在[Web Console](https://developer.mozilla.org/docs/Tools/Web_Console)輸入表達式不會產生副作用，你可以在輸入的同時預覽結果，讓你可以比先前更快地發現並修正錯誤。

#### 應用非同步堆疊追蹤於除錯工具和Console

現在的JavaScript大量依賴[ async/await](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/async_function)其他的


[非同步作業](https://developer.mozilla.org/docs/Learn/JavaScript/Asynchronous)，例如

[event](https://developer.mozilla.org/docs/Learn/JavaScript/Building_blocks/Events),

[promise](https://developer.mozilla.org/docs/Learn/JavaScript/Asynchronous/Promises), 還有

[timeout](https://developer.mozilla.org/docs/Learn/JavaScript/Asynchronous/Timeouts_and_intervals). 因為JavaScript引擎有效的整合，非同步執行現在也提供了更全面的功能。

除錯工具的非同步呼叫堆疊可以讓你了解event、timeout還有promise等呼叫功能執行的狀況在Console中，非同步堆疊也可以讓你更容易找到錯誤的根本原因。

#### 一窺Service Worker除錯功能

這個功能已經出現在Nightly版本有一段時間了，我們很興奮你們也將能夠受惠。請期待四周後即將發行的Firefox 76的[開發者版本](https://www.mozilla.org/firefox/developer/)。

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.