---
title: A* Algorithm Node Sort – Node 排序實作
url: https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-node-sort/
author: Ted Sie
published: '2016-07-08'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

新增 C# 腳本命名為 NodeSort.cs

用來處理 Node 排序的相關動作

using System.Collections; public class NodeSort { private ArrayList nodes = new ArrayList(); public int Length { get { return this.nodes.Count; } } public bool Contains(object node) { for( int cnt = 0; cnt < nodes.Count; cnt++ ) { if( ( (Node)node ).position == ( (Node)nodes[cnt] ).position ) return true; } return false; } public Node First() { if (this.nodes.Count > 0) { return (Node)this.nodes[0]; } return null; } public void Push(Node node) { this.nodes.Add(node); this.nodes.Sort(); } public void Remove(Node node) { this.nodes.Remove(node); this.nodes.Sort(); } }

這個腳本中主要包含了以下功能

1. 取得 ArrayList 的長度

2. 判斷 Node 是否在 ArrayList 裡

3. 取得 ArrayList 中第一個 node

4. 在 ArrayList 中新增 Node

5. 在 ArrayList 中移除 Node

其中可以看到有一個 this.nodes.Sort() 方法

這是這個腳本最重要的地方

也是之前提到的對Node做排序的實作

因為利用了 ArrayList 以及前一篇中的 Node class

實現排序動作

PS：這個排序方法並不是效率最好的

想知道排序更深入的內容

可以上網搜尋 Bubble Sort 以及 Heap Sort

Bubble Sort 適合初學者一開始使用的排序方法

因為內容簡單，但實際上運作效率過低，所以通常不使用

Heap Sort 則是較為進階的排序方法

利用二元樹的概念快速的進行排序

## 3 thoughts on “A* Algorithm Node Sort – Node 排序實作”