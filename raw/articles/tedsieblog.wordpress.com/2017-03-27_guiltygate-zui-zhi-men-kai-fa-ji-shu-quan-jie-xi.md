---
title: GuiltyGate 罪之門 – 開發技術全解析
url: https://tedsieblog.wordpress.com/2017/03/27/guiltygate-technique-review/
author: Ted Sie
published: '2017-03-27'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

[GuiltyGate 罪之門](https://play.google.com/store/apps/details?id=com.hipartystudio.guiltygate)，是一款在 Android 平台上所推出近未來風格推理解謎遊戲，結合密室逃脫的概念讓玩家可以透過關卡中的線索，慢慢的解開深藏在關卡中的謎題。


![](../../assets/a15625b00acc106c.jpg)


![](../../assets/852ac60815104196.jpg)


GuiltyGate 罪之門（以下簡稱 GG）由 HiParty Studio 所開發，團隊成員只有兩位，負責**美術**、**企劃**的[日式蝦球吃到飽](https://www.facebook.com/%E6%97%A5%E5%BC%8F%E8%9D%A6%E7%90%83%E5%90%83%E5%88%B0%E9%A3%BD-1416561795309638/)以及負責**程式**、**專案規劃**的[阿祥的開發日常](https://www.facebook.com/tedsieblog/)。而這次則要以程式負責人的身份來分享開發 GG 的過程中所用到的各種技術以及遇到的問題，以下就針對**核心機制**、**輔助工具**和**細節優化**三大部分來做分享。


#### 核心機制

**程式架構**

相信有很多人都清楚 Unity 是一款組件式遊戲引擎（Component-Based Engine）或稱為實體組件系統（Entity-Component System），透過 [AddComponent](https://docs.unity3d.com/ScriptReference/GameObject.AddComponent.html) 可以很輕易地將組件化腳本附加於遊戲物體（GameObject）。但這種便利的優點同時也帶來了相對應的缺點，使得開發者無法輕易的掌握各腳本之間的生命週期（[Script Lifecycle](https://docs.unity3d.com/Manual/ExecutionOrder.html)），雖然這部分可以透過 [Script Execution Order](https://docs.unity3d.com/Manual/class-ScriptExecution.html) 來強制修改腳本的執行順序，但使用上卻十分不方便。

![](../../assets/4aac4b856951fee4.png)


所以這次在設計核心機制時，嘗試規劃了一套獨立運作的程式架構，一方面降低對 Unity 引擎的依賴性，另一方面提升腳本的可控性，透過腳本 Engine.cs 作為唯一與 Unity 引擎溝通的接口來驅動其餘系統。

![](../../assets/6edeab67284be541.png)


而為了讓各系統之間的溝通能夠更加順暢，規劃了一套程式架構來作為遊戲的骨架，透過這一套架構達到：避免各系統之間的依賴性、保留資料互通的便利性以及遊戲邏輯的獨立性。

![](../../assets/83f6c541f1355a4d.png)



**狀態管理器（State Manager）**

在完成了許多專案後，漸漸察覺到可以將遊戲的運作流程視為一個巨大的狀態機，透過狀態機來切換不同遊戲畫面、運作邏輯甚至遊戲場景。所以在 GG 專案中遵循了狀態模式（[State Pattern](https://en.wikipedia.org/wiki/State_pattern)）來實作出狀態管理器，使場景的轉換透過狀態管理器來驅動，增加場景轉換時開發者對場景資源的可控性，這邊可以試著將狀態管理器理解成一個自定義的場景切換器。

![](../../assets/220b3c8d0186d557.png)



**任務管理器（Task Manager）**

在不同的狀態中，常常需要處理許多運作方式完全不同的子任務，像是互動介面、觸發道具、劇情播放、解謎步驟…等都是獨立的遊戲邏輯，而任務管理器的首要任務就是管理、切換在狀態中所包含的子任務。

![](../../assets/a5863d6686979cd8.png)



**遊戲系統管理器（Game System Manager）**

獨例模式（[Singleton Pattern](https://en.wikipedia.org/wiki/Singleton_pattern)）是最常見的設計模式之一，透過獨例模式可以相當輕易的讓開發者能夠取得唯一的實體物件，但在這方便且容易使用的特性背後，也往往造成開發者濫用獨例模式，使獨例模式的擴充出現問題。所以在 GG 專案中則透過唯一實作獨例模式的遊戲系統管理器，來註冊並管理各系統類別。

using System; using System.Collections.Generic; using TEDCore.Utils; using UnityEngine; namespace TEDCore { public class GameSystemManager { private static GameSystemManager _instance = null; public static GameSystemManager Instance { get { if(_instance == null) { _instance = new GameSystemManager(); } return _instance; } } private GameObject _root; private Dictionary<Type, MonoBehaviour> _monoBehaviours; private Dictionary<Type, System.Object> _objects; public GameSystemManager() { _root = new GameObject ("[GameSystemManager]"); _root.hideFlags = HideFlags.HideInHierarchy; GameObject.DontDestroyOnLoad (_root); _monoBehaviours = new Dictionary<Type, MonoBehaviour>(); _objects = new Dictionary<Type, System.Object>(); } public static void Set<T>(System.Object entity) where T : class { if (Has<T> ()) { Debug.LogException (new Exception (string.Format ("[GameSystemManager] - GameSystem \"{0}\" has already existed!", typeof(T).Name))); } else { Debug.LogFormat (string.Format ("[GameSystemManager] - GameSystem \"{0}\" has set up.", typeof(T).Name)); Instance._objects.Add(typeof(T), entity); } } public static void Set<T>() where T : MonoBehaviour { if (Has<T>()) { Debug.LogException (new Exception (string.Format ("[GameSystemManager] - GameSystem \"{0}\" has already existed!", typeof(T).Name))); } else { Debug.LogFormat (string.Format ("[GameSystemManager] - GameSystem \"{0}\" has set up.", typeof(T).Name)); Instance._monoBehaviours.Add(typeof(T), Instance._root.AddComponent<T> ()); } } public static T Get<T>() where T : class { if(Has<T>()) { if (IsInheritMonoBehaviour<T> ()) { return Instance._root.GetComponent<T> (); } else { return Instance._objects[typeof(T)] as T; } } Debug.LogException(new Exception(string.Format("[GameSystemManager] - GameSystemManager of {0} doesn't exist!", typeof(T).Name))); return null; } public static bool Has<T>() where T : class { if (IsInheritMonoBehaviour<T> ()) { return Instance._monoBehaviours.ContainsKey (typeof(T)); } else { return Instance._objects.ContainsKey(typeof(T)); } } private static bool IsInheritMonoBehaviour<T>() where T : class { return typeof(T).IsSubclassOf(typeof(MonoBehaviour)); } } }

但由於 Unity 的 MonoBehaviour 特性，導致必須針對繼承與無繼承 MonoBehaviour 的兩種情況做相對應的處理，所以在進行類別註冊時會產生相對應的兩種寫法。

//註冊繼承 MonoBehaviour 類別 GameSystemManager.Set<ResourceManager>(); //註冊無繼承 MonoBehaviour 類別 GameSystemManager.Set<EventManager>(new EventManager()); //使用類別 GameSystemManager.Get<ResourceManager>(); GameSystemManager.Get<EventManager>();


**資源管理器（Resource Manager）**

資源管理器是為了將所有資源操作功能進行整合，包含 Resources 目錄以及 AssetBundle 的載入、讀取、生成…等。當開發者對資源進行任何操作時，只需要針對需求而使用相對應的方法即可。


**事件管理器（Event Manager）**

事件管理器的實現是透過觀察者模式（[Observe Pattern](https://zh.wikipedia.org/wiki/%E8%A7%82%E5%AF%9F%E8%80%85%E6%A8%A1%E5%BC%8F)），目的是為了在沒有互相關聯情況下的腳本中傳送訊息，透過這種方式可以很輕易地降低類別或腳本之間的依賴性。其中管理器主要包含三個公開方法，分別是註冊事件、註銷事件與傳送事件。

GameSystemManager.Get<EventManager>().RegisterListener(eventName, IEventListener, priority); GameSystemManager.Get<EventManager>().UnregisterListener(eventName, IEventListener); GameSystemManager.Get<EventManager>().SendEvent(eventName, eventData);


**聲音管理器（Audio Manager）**

與資源管理器的作用相當，集中處理有關聲音的所有功能，包含播放一次性音效、播放背景音樂…等。


**計時管理器（Timer Manager）**

一般在處理計時功能時，都會單獨處理該類別中的計時邏輯，像是時間倒數、動畫間隔、特效延遲…等。雖然各個效果的運作流程有些許差異，但在計時器運作方面卻完全相同，所以為了集中管理計時器的運作而完成這個子系統。

**Timer.cs**

using System; namespace TEDCore.Timer { public class Timer { public float Duration { get { return _duration; } } public object Data { get { return _data; } } public bool HaveFinished { get { return _haveFinished; } } private float _duration; private Action<object> _onTimerFinished; private object _data; private bool _haveFinished = false; public Timer(float duration, Action<object> onTimerFinished = null, object data = null) { _duration = duration; _onTimerFinished = onTimerFinished; _data = data; } public void Update(float deltaTime) { _duration -= deltaTime; if (_duration <= 0 && !_haveFinished) { _haveFinished = true; if (null != _onTimerFinished) { _onTimerFinished (_data); } } } } }

**TimerManager.cs**

using System; using System.Collections.Generic; using UnityEngine; namespace TEDCore.Timer { public class TimerManager { private List<Timer> _timers; private bool _pause = false; private Timer _timerCache; private float _lastRealTime = 0; public TimerManager() { _timers = new List<Timer> (); } public void Add(Timer timer) { _timers.Add (timer); } public void Remove(Timer timer) { _timers.Remove (timer); } public void Update() { _lastRealTime = Time.realtimeSinceStartup - _lastRealTime; if (_timers.Count != 0 && !_pause) { for (int cnt = 0; cnt < _timers.Count; cnt++) { _timerCache = _timers [cnt]; _timerCache.Update (_lastRealTime); if(_timerCache.HaveFinished) { Remove (_timerCache); } } } _lastRealTime = Time.realtimeSinceStartup; } public void Pause() { _pause = true; } public void Resume() { _pause = false; } } }

**TimerExample.cs**

using UnityEngine; using TEDCore; using TEDCore.Timer; public class TimerExample : MonoBehaviour { private void Awake() { //Callback OnTimerFinished after 0.1s Timer timer1 = new Timer (0.1f, OnTimerFinished); GameSystemManager.Get<TimerManager> ().Add (timer1); //Callback OnTimerFinishedWithFloat with 1.0f after 0.2s Timer timer2 = new Timer (0.2f, OnTimerFinishedWithFloat, 1.0f); GameSystemManager.Get<TimerManager> ().Add (timer2); //Callback OnTimerFinishedWithBool with false after 0.3s Timer timer3 = new Timer (0.3f, OnTimerFinishedWithBool, false); GameSystemManager.Get<TimerManager> ().Add (timer3); } private void OnTimerFinished(object data) { Debug.Log ("OnTimerFinished"); } private void OnTimerFinishedWithFloat(object data) { float timerData = (float)data; Debug.Log ("OnTimerFinishedWithFloat = " + timerData); } private void OnTimerFinishedWithBool(object data) { bool timerData = (bool)data; Debug.Log ("OnTimerFinishedWithBool = " + timerData); } }


**輸入管理器（Input Manager）**

在 GG 專案中由於有手勢判斷的需求，切換房間、切換道具、點擊畫面…等，在觸發手勢、點擊時利用事件管理器來發送訊息，來輕易的判斷玩家操作。


#### 輔助工具

由於這個專案在引擎製作端是單獨開發，所以為了盡量減少重複性的工作流程開發出了一些傾向自動化概念的輔助工具，以優化開發時程。分別設計了以下工具：**企劃編輯工具**、**自動化腳本生成工具**、**自動化 AssetBundle 建置**、**自動化版本建置**。

**企劃編輯工具**

因為 GG 本身是一款解謎遊戲，所以在遊戲中有許多的解謎道具、劇情對話、對話選單、密碼鎖答案…等遊戲資料，在遊戲資料量相當龐大且必須時常更新的前提下，為了讓企劃編輯與程式實作能夠同步作業，所以透過 Google Spreadsheets 設計出了一個資料編輯頁面。透過這個頁面，企劃可以很方便地進行資料新增以及資料更新。

像是地圖資料、道具資料、主角 OS 資料或對話資料…等。

![](../../assets/aba6c881b64eb3c2.png)


![](../../assets/5a1276398cbfca7e.png)


![](../../assets/9eb1a3a265f65d3a.png)


![](../../assets/539cc106f7f92d6e.png)



**自動化腳本生成工具**

在最初的版本中，將企劃資料匯入專案後必須針對資料變動或新增的部分來做相對應的程式腳本更新，運作一段時間後發現，一旦企劃的欄位需求改變，程式部分也需要付出相對應的時間來進行重複的製作流程。為了減少這個流程所耗費的時間，著手開發了自動化腳本生成工具，透過直接讀取企劃資料的欄位以及資料，自動化的將相對應的腳本生成，以節省開發成本及時間。而這一套自動化腳本生成工具，也已經發佈在 Github 中，有興趣的讀者們可以自行觀看。[本地端資料庫工具 Github 連結](https://github.com/ted10401/DataManager/tree/master/zh-tw)。

以上面的資料為例，會自動生成出下列類別，而開發者就只需要專注在邏輯新增、修改的部分。

public class MapData { public string Key; public string Room; public float InitialAngle; public string InitialDirection; } public class OSData { public string Key; public string Description; } public class ItemData { public string Key; public string TriggerDialog; public string TriggerItem; public string Resource; public string KeyItem; public string StartAnimation; public string EndAnimation; } public class DialogData { public string Key; public string SaveAfterDialog; public string TriggerAfterMap; public string TriggerBeforeMap; public string NextDialog; public bool TriggerOnce; public string Title; public string CharacterImage; public string BackgroundImage; public List<string> ImageAnimation; public string Description; public string TriggerItem; public List<string> TriggerOption; public string TriggerFlash; public string OptionImage; public string SetChapter; }


**自動化 AssetBundle 建置**

進入遊戲製作後期時，開始規劃導入 Unity AssetBundle 機制以增加資源下載的擴充性。在這個工具中利用了**自定義規範**，將所有儲存在 AssetBundleResources 資料夾下的資料都視為 AssetBundle。

![](../../assets/9b20c34122ea5494.png)


在藉由 [AssetImporter.assetBundleName](https://docs.unity3d.com/ScriptReference/AssetImporter-assetBundleName.html) 來將資料夾內的資源做 AssetBundle Name 的設置。

最後選擇需要產出的 AssetBundle 對應平台進行自動化建置。

![](../../assets/3b70dc73c9d44673.png)



**自動化版本建置**

由於建置版本的過程是一個固定流程，所以可以透過規劃自動化建置步驟，來確保每次生成的安裝包都能夠有相同的設定。其中，在這個專案中的自動化建置流程為：取得遊戲發佈場景 > 更新版本輸出位置 > 設定 Android Keystore > AssetBundle 建置 > Define Symbol 設定 > 版本建立。

![](../../assets/085f322c053828bf.png)



#### 細節優化

在開發 GG 的過程中，並沒有遇到太多的效能議題，但是在處理檔案大小以及遊戲順暢性時，做了幾項特別的處理，**檔案包優化**、**Sprite Packer**、**預載管理器**以及**預載優化**。

**檔案包優化**

如同每個專案的開發進度一樣，GG 在開發的初期與開發後期，檔案包的大小有很明顯的提升，由初期的 26 MB 一路上升到 76 MB，造成檔案包變化這麼巨大的其中一個最明顯的原因就是貼圖的數量以及品質的設定。所以為了有效降低檔案包的大小，很簡單的做了切換貼圖格式的小工具，來進行有效率的貼圖格式切換動作。

![](../../assets/08a29e9cbdeb41ed.png)


![](../../assets/8dbdd79d00897974.png)


![](../../assets/f10c79fcb3472fd1.png)


![](../../assets/ffef9593542a038a.png)


**Sprite Packer**

[Sprite Packer](https://docs.unity3d.com/Manual/SpritePacker.html) 是 Unity 所提供的圖集工具，由於 GG 是一款純 2D 結構的遊戲，所以在開發過程中只使用了 uGUI 來作為介面操作。雖然在開發過程中遊戲的 Draw Call、CPU Usage、Memory…等都沒有遇到太大問題，但是在遊戲上架前夕，還是一口氣的將圖片資源做了分類處理，使專案的 Draw Call 能夠維持最小值。

**預載管理器（Preload Manager）**

在遊戲開發初期中，資源都是在使用時才進行載入的動作，導致遊玩時的順暢度降低，為了改善這個問題將資源做了預載處理，配合前面所提到的資源管理器，透過關卡之間的讀取畫面來進行該關卡中的所有資源預載。

在專案中，預載流程分別為：讀取新關卡資源 > 比對並釋放舊關卡的無用資源 > 進行資源載入。

**預載優化**

在預載的過程中，一開始是直接使用異步讀取機制，但是這個做法導致讀取畫面的流暢性降到最低，為了改善這個環節，使讀取畫面帶給玩家較為順暢的體驗，所以在異步讀取機制的基礎上新增了排程規劃，透過排程規劃將資源分批讀取，以達到順暢讀取畫面的需求。

private void Preloading() { _loadingTimer = Time.realtimeSinceStartup; Debug.LogFormat("Start loading object {0}", m_loadingObjects[0]); Engine.Instance.StartCoroutine(m_resourceManager.LoadResourceAsync(m_loadingObjects[0], AsyncCallback)); } private void AsyncCallback(string name) { m_loadingObjects.Remove (name); Debug.LogFormat("Finish loading object {0} in {1} seconds. Remaining object count = {2}", name, Time.realtimeSinceStartup - _loadingTimer, m_loadingObjects.Count); if (m_loadingObjects.Count == 0) { isReady = true; if (null != _onPreloadFinished) { _onPreloadFinished (); } } else { Preloading (); } }


#### 開發回顧

2015 年 06 月 09 日，在某個奇妙的因緣際會之中認識了蝦球，經過簡單的認識後就很正常的開始聊起遊戲開發的故事，也因為這樣得知了 GuiltyGate 罪之門這款遊戲風格強烈的作品。一拍即合的聊天過程中，得知遊戲製作遇到了意想不到的阻礙，當時並沒有過多的想法，單純的認為這款遊戲相當特別，如果就這樣看它消失在茫茫的遊戲大海中實在是很可惜的一件事，於是就毛遂自薦的提議「要不我們就一起合作吧！」，也是因為這樣才有這個機會讓玩家們可以玩到現在的這個版本。

在開發初期時，進度的控制都相當順利，幾乎沒有太多的溝通、討論或是意見不合的情況，就這樣一路順利的開發到了 2015 年底，但事情往往沒有這麼順遂。就在這時開始發生了製作問題，由於時間配合與工作的種種因素導致製作從 2015 年底停擺到 2017 年初將近一年之久，這其中只包含了少數的技術實驗與優化更新，但在故事內容、美術素材與關卡設計就沒這麼順利了。

![](../../assets/eedcaf6b82cbc5e3.png)


在 2017 年初時，我們決定終止 GuiltyGate 罪之門的開發，並且打算就這樣讓玩家漸漸的淡忘它，不過在經過簡單的溝通後，覺得不管遊戲完成與否，還是希望這段時間中彼此的努力能夠有個結局，所以「就讓它推出吧！」，而遊戲也在 2017 年 01 月 23 日上架 GooglePlay，曾經悄悄的進入熱門免費排行榜前二十名，截至目前為止也獲得超出團隊成員預期的收穫。

![](../../assets/bf8274d2a322b234.png)


![](../../assets/f9485c4c748dd949.png)


整體來說，參與 GuiltyGate 罪之門開發的這段時間真的是相當的充實，雖然最後沒辦法帶給玩家們最完善的遊戲內容與體驗，但若是能夠回到過去再選擇一次，我還是會立刻參與專案開發。獨立開發的過程雖然辛苦，但從中獲得的經驗是相當珍貴的，正在為獨立開發而苦惱的開發者們，相信自己吧！

至於 GuiltyGate 罪之門真的就這樣結束了嗎？各位玩家們，就拭目以待吧！

終於一窺 TEDCore 的真面目，各種值得取經的內容

LikeLike

還有很多細節沒有公開，有機會在完整的介紹這套開發架構

LikeLiked by 1 person

可以哦 期待。

LikeLike

很棒和實用的經驗分享，神文已跪

LikeLike

多分享多交流，開發風氣才會越來越好！

LikeLike

很棒的经验分享，我把它转载到了GAD平台上哈

http://gad.qq.com/article/detail/7194296

LikeLike

謝謝分享，希望這些經驗能讓大家從中獲得些什麼

LikeLike

不错，麻雀虽小五脏俱全。

LikeLike

刚过了一遍，不少地方有不少性能问题，比如参数用object导致的装箱拆箱。不妨考虑用泛型代替之。

LikeLike

是的事件系統在 Boxing Unboxing 部分的確是一個要解決的問題，用泛型的方式也有考慮過，但會降低一些事件系統的便利性，所以就沒在這次的專案中做這個改動。

LikeLike