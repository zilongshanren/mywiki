---
title: Firefox 77新功能：開發者工具改良與Web平台更新 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/06/firefox-77/
author: Florian Scholz
published: '2020-06-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

全新 Firefox 穩定版正式推出！第 77 版為開發者提供了更多新功能。

這篇文章包含新版本中的精彩亮點，想了解完整資訊，請瀏覽以下網頁：

## 開發者工具改善

讓我們先來看看第 77 版開發者工具中最有趣的優化與創新。如果你想使用更多開發中的新功能，並提供建議，請安裝 [Firefox 開發者版本](https://www.mozilla.org/firefox/developer/)即可搶先體驗。

### 更快、更有效的 JavaScript 除錯

大型 Web 應用程式對開發者工具來說無疑是一項艱難的挑戰，因為需要快速而正確地處理捆綁（bundling）、實時重載（live reload）和相依性。 Firefox 77 的 Debugger 學了一些新技巧，讓你可以因此更加專注於除錯。

在先前的許多版本中，我們持續致力於提升除錯性能，也幾乎除光了影響層面最嚴重、可處理的問題。為了找出剩餘的瓶頸，我們一直積極地和社群保持聯繫。得益於我們收到的許多詳細回報，我們終於能夠改善除錯的效率，不僅提升暫停和步進速度，也減少記憶體長期用量。

#### 就是會動的 JavaScript 和 CSS Source Map

Source Map 也包含在此次社群訪查中，在新版本速度表現也有所提升。些行內的 Source Map 載入的時間加快了 10 倍。更重要的是，我們改善了不同 Source Map 設定的可靠性。感謝大家回報各種含輕微錯誤的 Source Map 案例，我們因此得以調整了解析和映射的 fallback 機制。整體而言，先前有些無法載入的 CSS 和 JavaScript / TypeScript 等原始碼，現在應該就是會動了。

### 在 JavaScript 選定堆疊範圍中逐步除錯

步進是除錯時很關鍵，但卻又不直觀的環節。在步進和步出函數，或是在函式庫和自己的代碼之間轉移時，往往很容易迷失方向或跳過頭。

現在，除錯器會在步進時，遵循當前選擇的堆疊。這個功能在進入函數呼叫、或在堆疊中更下方的函式庫中暫停時特別實用。只需在「呼叫堆疊」（Call Stack）中選擇正確的函式，就可以跳至其當前暫停的行數，然後從那裡繼續逐步除錯。

我們希望這可以使步進除錯的過程更加直觀，讓你更不會錯過重要的那一行程式。

### 網路和除錯器滿出來的功能

為了使工具列欄更加簡潔，網路和除錯器遵循主控制台的模方式，將結合部分現有的選取功能選項框格和新的功能選取框格，並合併到新的設置選單菜單中。這使得如「關閉Disable JavaScript」等的強大功能觸手可及，並為往後更強大的功能預留了更多空間。

### 在腳本讀取屬性或寫入屬性時暫停執行

了解狀態的改變是常透過主控制台來記錄或除錯時經常檢查的問題。Firefox 72 中推出的[監看檢查點（Watchpoints）](https://wiki.developer.mozilla.org/en-US/docs/Tools/Debugger/How_to/Use_watchpoints)可以在程式腳本讀取屬性或寫入屬性時暫停執行。暫行執行時，你可以在 Scopes 窗格中的屬性上單擊右鍵，以新增監看檢查點。

貢獻者 [Janelle deMent](https://bugzilla.mozilla.org/user_profile?user_id=637866)結合了 get / set ，讓監看檢查點在使用上更為方便。在新增這個選項之後，使任何程式參考script reference 都能將觸發暫停程序。

### 改善網路資料數據優化預覽

在先前的每個發行版本中，我們都針對網路絡的詳細訊息（Network details）面板窗格都有逐步進行了調整。因為舊的界面在具有事件處理有點的錯誤，在選擇和複製文字文本時很不穩定。此外，我們也提升了大量資料項型數據條目的性能。

這是大幅清理網路（Network）窗格的其中一步中較大幅的調整，而我們也不斷透過 [@FirefoxDevTools Twitter](https://twitter.com/FirefoxDevTools) 和 [Mozilla’s Matrix community](https://chat.mozilla.org/#/room/#devtools:mozilla.org) 針對社群用戶進行調查。歡迎加入我們，讓我們了解你們的想法。 只要取得 [Firefox 開發者版本](https://www.mozilla.org/firefox/developer/)，就可以搶先體驗更多網路面板窗格側欄的新設計。

## Web 網頁平台更新

Firefox 77 開始支援一些 Web 網頁平台的新功能。

`String#replaceAll`


Firefox 67 引入了[ String#matchAll](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/matchAll)，這是用來迭代字串中所有取代

[正規表達式](https://en.wikipedia.org/wiki/Regular_expression)匹配結果匹配更為的便捷的方法。在 Firefox 77 中，我們讓他更加方便是提升了整體的使用體驗：

[可以用來替換所有相符出現的字串字符串──這個功能你之前可能曾經搜尋過千百次了。（特別感謝超有幫助的 StackOverflow 的大力幫忙！）](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/replaceAll)

`String#replaceAll`

以前，如果想要用「dog」替換所有的「cat」時，必須使用全局正規則表達式

`.replace(/cats/g, 'dogs');`


`.split('cats').join('dogs');`


現在，利用 [String#replaceAll](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String/replaceAll) 可以大幅提升語法的可讀性：

`.replaceAll('cats', 'dogs');`


### IndexedDB 游標請求

Firefox 77 將公開源自[IDBCursor](https://developer.mozilla.org/docs/Web/API/IDBCursor)的起源（originated from），公開成請求為 [該游標的屬性](https://developer.mozilla.org/docs/Web/API/IDBCursor/request)。這是一個很好的改進良，往後在編寫包裝如「升級」資料數據庫功能的包裝函式等等的內容將變得更加容易。以前要在游標位置上進行升級時，必須傳遞游標物件對象（cursor object）及其起源的請求物件對象（request object），因為前者仰賴於後者。但是在此一改變新版本優化之後，因為請求物件對象已可透過在游標取得上，所以現在只需要傳遞游標物件對象。

## Firefox 77 擴充套件功能：減少授權及等其他功能

自 Firefox 57 版本發行以來，用戶會在附加元件的安裝與更新過程中或是在更新過程中，當有請求新權限請求時，用戶會看到附加元件擴充功能要使用訪問的權限。這些提示的頻率有時常多到令人感到不知所措，而且如果未能在附加元件擴充功能更新時，如果未能接受新的權限請求，這可能會使用戶陷入卡在只能使用舊版本的困境擾。現在擴充功能開發人員可以將某一些權限設置為[選用自訂權限](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/optional_permissions)，如此一來就可以輕鬆地避免觸發過多的提示。選用自訂權限不會在安裝時，或在添加到擴充功能更新版本時觸發權限請求。另外，選用自訂權限也可以[在執行時即時進行請求設置](https://extensionworkshop.com/documentation/develop/request-the-right-permissions/?utm_source=blog.mozilla.org&utm_medium=blog&utm_campaign=hacks-fx-77#request-permissions-at-runtime)，因此以便用戶可以更加了解查看目前正在進行請求的權限的實際用途。

拜訪問[附加元件部落格擴充功能專區](https://blog.mozilla.org/addons/)了解 Firefox 77 更多附加元件的相關更新其他的擴充功能！

## 總結

以上就是這次 Firefox 77 的精采亮點！了解新功能並之後，記得動手親自體驗看看！與往常一樣，歡迎隨時留言反應反饋，或在評論區中提問。

## About
[
Florian Scholz ](https://developer.mozilla.org)

Florian is the Content Lead for MDN Web Docs, writes about Web platform technologies and researches browser compatibility data. He lives in Bremen, Germany.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.