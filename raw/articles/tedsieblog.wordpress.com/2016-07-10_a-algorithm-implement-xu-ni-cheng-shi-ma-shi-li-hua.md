---
title: A* Algorithm Implement – 虛擬程式碼實例化
url: https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-implement/
author: Ted Sie
published: '2016-07-10'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

**A* 虛擬程式碼實例化**

看到這步的人可能還是會覺得一頭霧水

怎麼前面已經三篇了可是都還沒有看到 A* 的實作成果

但這篇看完後會突然發現概念都連接起來了 ( 應該吧…..

首先希望各位回想一下最一開始的 A* 演算法虛擬碼

這篇將會以那個虛擬碼來處理 A* 演算法運算

[A* Algorithm Introduction – 演算法簡介](https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-introduction/)

新增一個C#腳本命名為AStar.cs

using UnityEngine; using System.Collections; public class AStar { public static NodeSort closedList, openList; private static float HeuristicEstimateCost(Node curNode, Node goalNode) { Vector3 vectorCost = goalNode.position - curNode.position; return vectorCost.magnitude; } public static ArrayList FindPath( Node start, Node goal ) { openList = new NodeSort(); openList.Push(start); start.G_Cost = 0.0f; start.H_Cost = HeuristicEstimateCost(start, goal); closedList = new NodeSort(); Node node = null; while (openList.Length != 0) { node = openList.First(); //Push the current node to the closed list closedList.Push(node); //and remove it from openList openList.Remove(node); //Check if the current node is the goal node if ( node.position == goal.position ) { return CalculatePath(node); } //Create an ArrayList to store the neighboring nodes ArrayList neighbours = new ArrayList(); NodeManager.instance.GetNeighbours(node, neighbours); Node neighbourNode; for ( int i = 0; i < neighbours.Count; i++ ) { neighbourNode = (Node)neighbours[i]; if ( !closedList.Contains( neighbourNode ) ) { float cost; float totalCost; float neighbourNodeEstCost; if ( !openList.Contains( neighbourNode ) ) { //G cost = HeuristicEstimateCost( node, neighbourNode ); totalCost = node.G_Cost + cost; //H neighbourNodeEstCost = HeuristicEstimateCost( neighbourNode, goal ); neighbourNode.G_Cost = totalCost; neighbourNode.parent = node; neighbourNode.H_Cost = neighbourNodeEstCost; openList.Push(neighbourNode); } else { cost = HeuristicEstimateCost( node, neighbourNode ); totalCost = node.G_Cost + cost; if( neighbourNode.G_Cost > totalCost ) { neighbourNode.G_Cost = totalCost; neighbourNode.parent = node; } } } } } if ( node.position != goal.position ) { Debug.LogError("Goal Not Found"); return null; } return CalculatePath(node); } private static ArrayList CalculatePath(Node node) { ArrayList list = new ArrayList(); while (node != null) { list.Add( node ); node = node.parent; } list.Reverse(); return list; } }

**6**

一開始先分別定義 openList 以及 closeList

**8~13 HeuristicEstimateCost**

用來計算兩個節點間的移動距離

**15~96 FindPath**

這段是 A* 演算法實作中最複雜的一部分

可以將虛擬碼與實作互相對照

在演算初期先將 openList 及 closeList 初始化

並將 StartNode 的 G_Cost 及 H_Cost 也初始化

( 小提醒：G_Cost為實際移動距離、H_Cost為到終點的預估距離 )

接著將 StartNode 加入 openList 裡面

開始進行 A* 演算法中的核心計算

接下來都是將虛擬碼轉換為實際code的結果

需要注意的是取得 neighbors 用到了上一篇中的 GetNeighbours 方法

下一步則是判斷 neighbors 是否在 openList 裡

如果沒有再 openList 裡代表該節點沒有被運算過

所以需要將其 cost 算出來後加入 openList 裡

如果 neighbors 已經在 openList 裡

代表該節點已經運算過

但若這次運算的 cost 小於之前計算過的結果

則將它更新

如此一來，當程式運行到找到終點時

則會呼叫 CalculatePath 方法

**98~110 CalculatePath**

獲得終點 Node 後

即可逐一的從終點 Node 回推回起點 Node

最後將該陣列反轉後

就可以取得 A* 移動路徑

程式碼似乎只有到76行而已

LikeLike

也許是排版問題造成行數出錯

感謝指正

已修改

LikeLiked by 1 person

Line 49, it keeps saying “error CS0165: Use of unassigned local variable `totalCost'”, is there any problem? As i tried to disable that line but then the code does not work. It is not able to find the goal.

LikeLike

The script is messy at line 46, I will fix it.

For now, if you scroll the script at line 46 you can find the code.

LikeLike

I have modified the script, you should get the correct result for now.

Thanks for the message.

LikeLike