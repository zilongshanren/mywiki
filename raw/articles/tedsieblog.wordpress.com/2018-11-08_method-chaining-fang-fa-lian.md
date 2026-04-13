---
title: Method Chaining – 方法鏈
url: https://tedsieblog.wordpress.com/2018/11/08/method-chaining/
author: Ted Sie
published: '2018-11-08'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

方法鏈（鏈式編程、鏈接編程），第一次看到這個名詞可能會認為這是一種困難的設計技巧，但就如同設計模式一般，這種技巧已時常運用至軟體開發中，但開發者渾然不知。

關鍵字快搜：Method chaining、Fluent interface


#### 基礎概念

方法鏈是物件導向程式設計中調用多個方法的常用語法。

每個方法都會回傳物件本身，允許在單個語句中將方法鏈接在一起，而不需要參數來儲存過渡結果。

在每個過渡階段中，鏈接編程消除了額外的參數，降低開發者在命名參數及記住參數時的認知負擔。

#### 第三方套件範例

在 Unity 中已有許多第三方套件運用了方法鏈的概念，如 DoTween、UniRX。

using UnityEngine; using DG.Tweening; public class NewBehaviourScript : MonoBehaviour { private void Awake() { transform .DOMoveX(1.0f, 1.0f) .SetEase(Ease.Linear) .OnComplete(() => Debug.Log("Complete")); } }

using UniRx; using UniRx.Triggers; public class DangerousDragAndDrop : MonoBehaviour { void Start() { this.gameObject.OnMouseDownAsObservable() .SelectMany(_ => this.gameObject.UpdateAsObservable()) .TakeUntil(this.gameObject.OnMouseUpAsObservable()) .Select(_ => Input.mousePosition) .Repeat() // dangerous!!! Repeat cause infinite repeat subscribe at GameObject was destroyed.(If in UnityEditor, Editor is freezed) .Subscribe(x => Debug.Log(x)); } }

#### 範例實作 – 已計算機為例

Calculator.cs

using UnityEngine; public class Calculator { private float m_value; public Calculator() { m_value = 0; } public Calculator Add(float value) { m_value += value; return this; } public Calculator Subtract(float value) { m_value -= value; return this; } public Calculator Multiply(float value) { m_value *= value; return this; } public Calculator Divide(float value) { m_value /= value; return this; } public Calculator Print() { Debug.LogFormat("Result = {0}", m_value); return this; } }

ExampleClass.cs

using UnityEngine; public class ExampleClass : MonoBehaviour { private void Awake() { new Calculator() .Add(1.5f) .Multiply(10f) .Subtract(5.0f) .Divide(2.0f) .Print(); } }

#### 實作範例 – 以計時器為例

Timer.cs

using System; public class Timer { public bool IsDone; private float m_duration; private Action<float> m_onUpdate; private Action m_onComplete; public void Update(float deltaTime) { m_duration -= deltaTime; if (m_duration <= 0 && !IsDone) { IsDone = true; if(m_onComplete != null) { m_onComplete(); } } else { if (m_onUpdate != null) { m_onUpdate(m_duration); } } } public Timer SetDuration(float duration) { m_duration = duration; return this; } public Timer OnUpdate(Action<float> onUpdate) { m_onUpdate = onUpdate; return this; } public Timer OnComplete(Action onComplete) { m_onComplete = onComplete; return this; } }

TimerManager.cs

using System.Collections.Generic; public class TimerManager { private List<Timer> m_timers; private Queue<Timer> m_removeTimers; private Timer m_cacheTimer; public TimerManager() { m_timers = new List<Timer>(); m_removeTimers = new Queue<Timer>(); } public void Update(float deltaTime) { if (null == m_timers) { return; } if (m_timers.Count == 0) { return; } for (int i = 0; i < m_timers.Count; i++) { m_cacheTimer = m_timers[i]; m_cacheTimer.Update(deltaTime); if (m_cacheTimer.IsDone) { m_removeTimers.Enqueue(m_cacheTimer); } } while (m_removeTimers.Count > 0) { m_timers.Remove(m_removeTimers.Dequeue()); } } public Timer Create() { Timer newTimer = new Timer(); m_timers.Add(newTimer); return newTimer; } }

ExampleClass.cs

using UnityEngine; public class ExampleClass : MonoBehaviour { private TimerManager m_timerManager; private void Awake() { m_timerManager = new TimerManager(); m_timerManager.Create() .SetDuration(0.1f) .OnUpdate((float obj) => Debug.Log("OnUpdate = " + obj.ToString())) .OnComplete(() => Debug.Log("OnComplete")); } private void Update() { m_timerManager.Update(Time.deltaTime); } }

感謝分享，在搜尋DOTween時，無意間找到這篇。我也嘗試把我的計時器小工具改用這樣的寫法，非常不錯。

LikeLike

計時器真的滿適合用這種方法的

寫起來直觀許多

LikeLike