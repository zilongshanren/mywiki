---
title: Singleton Pattern – 獨體模式、單例模式
url: https://tedsieblog.wordpress.com/2016/07/10/design-pattern-singleton/
author: Ted Sie
published: '2016-07-10'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

前一陣子看了一本設計模式的書

學到了一些專有名詞

這裡先來介紹一下

很簡單但卻很實用的獨體模式


首先，什麼是獨體模式呢? 獨體模式又要用在什麼地方呢?


獨體模式是一種常用的設計模式

在使用這個模式時，可以確保生成對象只有一個實例存在


而獨體模式可以應用的範圍非常廣泛

簡而言之的話

只要在開發遊戲時希望某個類別只會有一個實例化物件

就可以使用到獨體模式

例如：伺服器溝通系統、遊戲主管理類等等


獨體模式的初始化有很多種作法

靜態初始化、靜態延遲初始化等等

個人比較喜歡延遲初始化

延遲初始化是在需要時才進行初始化

而靜態初始化就是在遊戲一進行就進行初始化


第一種：

最簡易版本，有線程問題

using UnityEngine; using System.Collections; public class Singleton : MonoBehaviour { private static Singleton _instance; public static Singleton Instance { get { if( _instance == null ) { if( _instance == null ) { GameObject singleton = new GameObject(); _instance = singleton.AddComponent<Singleton>(); singleton.name = "[Singleton] " + typeof(Singleton).ToString(); DontDestroyOnLoad( singleton ); Debug.Log( "[Singleton] An instance of " + typeof(Singleton) + " is needed in the scene, so '" + singleton + "' was created with DontDestroyOnLoad."); } else { Debug.Log( "[Singleton] Using instance already created: " + _instance.gameObject.name ); } } return _instance; } } }


第二種：

針對線程問題修改，使用 lock

using UnityEngine; using System.Collections; public class Singleton : MonoBehaviour { private static Singleton _instance; private static object _lock = new object(); public static Singleton Instance { get { lock( _lock ) { if( _instance == null ) { if( _instance == null ) { GameObject singleton = new GameObject(); _instance = singleton.AddComponent<Singleton>(); singleton.name = "[Singleton] " + typeof(Singleton).ToString(); DontDestroyOnLoad( singleton ); Debug.Log( "[Singleton] An instance of " + typeof(Singleton) + " is needed in the scene, so '" + singleton + "' was created with DontDestroyOnLoad."); } else { Debug.Log( "[Singleton] Using instance already created: " + _instance.gameObject.name ); } } } return _instance; } } }


第三種：

看到網路上的高手的寫法拿來自己用

使用泛型、使用 Double-Checked Locking

using UnityEngine; using System.Collections; public class Singleton<T> : MonoBehaviour where T : MonoBehaviour { private static T _instance; private static object _lock = new object(); public static T Instance { get { if( applicationIsQuitting ) { Debug.LogWarning( "[Singleton] Instance '" + typeof(T) + "' already destroyed on application quit." + " Won't create again - returning null." ); return null; } lock( _lock ) { if( _instance == null ) { _instance = (T) FindObjectOfType( typeof(T) ); if( FindObjectsOfType( typeof(T) ).Length > 1 ) { Debug.LogError( "[Singleton] Something went really wrong " + " - there should never be more than 1 singleton!" + " Reopenning the scene might fix it."); return _instance; } if( _instance == null ) { GameObject singleton = new GameObject(); _instance = singleton.AddComponent<T>(); singleton.name = "[Singleton] " + typeof(T).ToString(); DontDestroyOnLoad( singleton ); Debug.Log( "[Singleton] An instance of " + typeof(T) + " is needed in the scene, so '" + singleton + "' was created with DontDestroyOnLoad."); } else { Debug.Log( "[Singleton] Using instance already created: " + _instance.gameObject.name ); } } } return _instance; } } private static bool applicationIsQuitting = false; void OnDestroy() { applicationIsQuitting = true; } }

想像一下 test case :每scene有相同的script loader,負責載入缺失的manager class,(重點:動態載入singleton類物件)

多重load scene 是用async load

因為awake 有先後+同時, 被查詢時FindObject會機率失效 e.g. construct但未awake

然後就出現雙包問題, 簡單說面臨的問題是如何處理多於一個的singleton

而在這環境下在unity3d

使用 applicationIsQuitting 會有機會被自己lock得死死的處理要小心.

LikeLike

其實這個情況，建議是不要使用多個 Scene，也更不要在每個 Scene 都檢查缺失的 Manager，照理說，Singleton 並不需要去檢查，而是使用時才做動態生成就好

LikeLike

Ted 大你好!

想請教第 3 個方法有用到 Double-checked locking 嗎?

根據 Wiki: https://goo.gl/F32ckW

Double-checked locking 似乎是為了節省 lock 開銷

但第 3 種直接就 lock 住了沒有省到啊 XD

LikeLike

若是根據這篇的說明的話

我在這邊所實現的方法並不是 Double-checked locking

而是 Single-checked locking 而已

LikeLike