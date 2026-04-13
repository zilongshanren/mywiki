---
title: Understand How Garbage Collection Works in Unity – 淺談 Unity Garbage Collection
  機制
url: https://tedsieblog.wordpress.com/2018/12/13/understand-how-garbage-collection-works-in-unity/
author: Ted Sie
published: '2018-12-13'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

Garbage Collection 是讓記憶體回收再利用的過程，當記憶體區塊不在需要時，該區塊即可被釋放並回收，以便在下一筆資料進來時能夠重複利用。

在一些程式語言中，開發者需要透過適當的函數來分配和釋放這些堆內存區塊。

而 Garbage Collection 機制會自動幫開發者管理內存，減少顯示分配和釋放堆內存區塊的編碼工作量，也大大降低內存洩漏的可能性。

但若 Garbage Collection 發生的次數過於頻繁則會導致遊戲表現不佳，這也是常見的性能問題。


#### Value Type & Reference Type

Value Type 儲存的值是「實值」，如 int、float、bool、Unity’s struct type（Color、Vector3）

Reference Type 儲存的值是「參考」，也就是記憶體的位址，使用指標紀錄儲存內容記憶體區塊的開始位置，如 object, string, array

#### Stack & Heap

Stack：用於小區塊資料的短期存儲

Heap：用於大區塊資料的長期存儲

Allocated Memory：變數生成時，會在 Stack 或 Heap 上分配記憶體區塊，只要變數還在變數可視範圍（Scope）內，該記憶體區塊就會保持使用狀態。

Deallocated Memory：當變數離開變數可視範圍，該記憶體區塊不再使用。

#### Stack Allocation & Deallocation

因為 Stack 專門用於小區塊資料的短期存儲，所以 Stack Allocation 和 Deallocation 是一個簡單又快速的過程，發生的順序及資料大小都是可預料的。

#### Heap Allocation & Deallocation

Heap Allocation 比起 Stack Allocation 要複雜許多，因為 Heap 可同時用於短期與長期數據，以及各種類型的資料，而不同類型的資料所要求的記憶體區塊大小也不一樣，導致 Heap Allocation 和 Deallocation 的順序無法預料。

**Heap Allocation 執行步驟**

- 確認目前 Heap 記憶體的可分配記憶體是否足夠，若記憶體足夠，則分配記憶體（Allocated Memory）。
- 若可分配記憶體不足，觸發 Garbage Collection 嘗試釋放未使用的記憶體（此操作性能花費大），若釋放記憶體後可分配記憶體足夠，則分配記憶體（Allocated Memory）。
- 若在釋放記憶體後仍然沒有足夠的可分配記憶體，會將 Heap 記憶體進行擴充（此操作性能花費大），最後分配記憶體。

#### Garbage Collection 過程中發生了些什麼？

當變數離開變數可視範圍，該記憶體區塊並不會立刻回收，只有在 Garbage Collection 執行時才會將未使用的記憶體區塊進行釋放。

**Garbage Collection 執行步驟**

- 遍歷所有在 Heap 記憶體中的物件
- 檢查該物件是否在變數可視範圍內
- 若該物件不再變數可視範圍內則在該物件加上 Deletion 標籤
- 將擁有 Deletion 標籤的物件刪除並釋放其記憶體

#### Garbage Collection 什麼時候會執行？

- 宣告變數時 Heap 記憶體不足
- 定期執行（依平台不同）
- 手動執行

#### Heap 破碎化

由於資料型態的不同，分配記憶體時會要求不同大小的記憶體區塊，造成記憶體破碎化（Fragmentation）。當 Heap Allocation 發生時，雖然可分配記憶體總量足夠，但由於破碎化，導致無法取得合適的區塊，迫使 Garbage Collection 執行。

#### 三種降低 Garbage Collection 影響的方法

- 減少單次 Garbage Collection 執行時間
- 減少 Garbage Collection 執行頻率
- 在非關鍵時期執行 Garbage Collection

對應的三種策略

- 減少 Heap Allocation 產生
- 減少 Heap Allocation 和 Deallocation 頻率
- 針對 Garbage Collection 和 Heap 擴充進行計時，使它們在可預料的狀況下發生

#### 幾種減少垃圾產生的方法

**緩存 Caching**

頻繁地調用函數並丟棄 Reference Type，會產生不必要的 Heap Allocation。

改善方法：儲存這些 Reference Type 並重複利用他們。

改善前

private void OnTriggerEnter(Collider other) { GameObject[] gameObjects = FindObjectsOfType<GameObject>(); DoSomething(gameObjects); }

改善後

private GameObject[] m_gameObjects; private void OnTriggerEnter(Collider other) { m_gameObjects = FindObjectsOfType<GameObject>(); DoSomething(m_gameObjects); }


**不要在調用次數頻繁的函數中分派記憶體**

在 Unity 的 MonoBehaviour 中，調用頻率最高的莫過於 Update 及 LateUpdate，若在這些函數中分派過多記憶體則會產生大量 Garbage。

改善方法：減少這些函數的調用次數，可使用計時器控制更新頻率，或是加入判斷式控制更新時間點。


**集合清空**

使用生成新集合的方式會產生不必要的記憶體分配。

改善方法：將集合緩存起來，當需要重複利用集合時，清空代替生成。

改善前

private void Update() { List<int> list = new List<int>(); DoSomething(list); }

改善後

private List<int> m_list = new List<int>(); private void Update() { m_list.Clear(); DoSomething(m_list); }


**物件池 Object Pooling**

物件池是一種回收機制，將物件進行回收避免重複性的生成及銷毀，減少記憶體分配及釋放。


**Strings**

在 C# 中 String 是 Reference Type 而不是 Value Type，所以生成、捨棄 strings 會產生 garbage，若在程式碼中大量使用 Strings 會使垃圾大量堆積。

此外，C# 中的 String 是不可變的，意即首次創建後無法修改它的值，在連接 String 時，會創建一個帶有新值的 String 並拋棄舊 String，大量對 String 進行操作，也會產生過多垃圾。


**Unity 函數**

當開發者使用不是自行開發的函數時，也需要多加注意，在調用ㄧ部分 Unity 函數時會產生 Heap Allocation，在使用上時需要謹慎使用。

但目前並沒有相關文件說明這些差異，只能在開發時勁量使用 Profiler 來進行判斷，針對當前使用狀況找出最適合的作法。

改善前

GameObject.tag == targetTag

改善後

GameObject.CompareTag(targetTag)


**Coroutines**

調用 StartCoroutine() 時 Unity 會創建管理 Coroutines 的實例，導致些許垃圾的產生。

考慮到這一點，當對效能有疑慮時，必須盡量避免大量調用 StartCoroutine()。

在 Coroutine 中使用的 yield statement 本身並不會產生任何 Heap Allocation，但我們所使用的數值卻會產生不必要的 Heap Allocation。

改善前

yield return 0;

改善後

yield return null;

另一個常見的錯誤是在數值相同的情況下創建重複的 YieldInstruction。

改善前

while (!isComplete) { yield return new WaitForSeconds(1f); }

改善後

WaitForSeconds delay = new WaitForSeconds(1f); while (!isComplete) { yield return delay; }

#### Feature Preview: Incremental Garbage Collection

若 Garbage Collection 和 Heap 擴充同時發生，會導致單幀內操作性能花費明顯上升，造成卡頓的情況。

而 Incremental Garbage Collection 是尚在實驗中的機制，將操作性能花費從單幀分散到數幀中，減少 FPS 浮動過大的情形。

#### 參考資料

[Optimizing garbage collection in Unity games](https://unity3d.com/learn/tutorials/topics/performance-optimization/optimizing-garbage-collection-unity-games)

[Unity – Manual: Understanding Automatic Memory Management](https://docs.unity3d.com/Manual/UnderstandingAutomaticMemoryManagement.html)

[Feature Preview: Incremental Garbage Collection](https://blogs.unity3d.com/2018/11/26/feature-preview-incremental-garbage-collection/)