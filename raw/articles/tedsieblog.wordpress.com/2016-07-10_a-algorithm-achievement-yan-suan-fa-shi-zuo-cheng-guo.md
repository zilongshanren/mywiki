---
title: A* Algorithm Achievement – 演算法實作成果
url: https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-achievement/
author: Ted Sie
published: '2016-07-10'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

終於到了最後一步

可以看到辛苦理解後的實現成果了


新增一個 C# 腳本命名為 TestAStar.cs

using UnityEngine; using System.Collections; public class TestAStar : MonoBehaviour { //The start and end gameobject public GameObject startCube, endCube; private Transform startTransform, endTransform; private Node startNode; private Node endNode; public ArrayList pathArray; private float elapsedTime = 0.0f; //Interval time between pathfinding public float intervalTime = 1.0f; void Start () { startTransform = startCube.transform; endTransform = endCube.transform; pathArray = new ArrayList(); FindPath(); } void Update () { elapsedTime += Time.deltaTime; if (elapsedTime >= intervalTime) { elapsedTime = 0.0f; FindPath(); } } void FindPath() { //Get start node with position startNode = new Node( NodeManager.instance.GetNodeCenter( startTransform.position ) ); //Get end node with position endNode = new Node( NodeManager.instance.GetNodeCenter( endTransform.position ) ); pathArray = AStar.FindPath(startNode, endNode); } //Display the a-star path finding line void OnDrawGizmos() { if (pathArray == null) return; if (pathArray.Count > 0) { for( int cnt = 0; cnt < pathArray.Count; cnt++ ) { if( cnt <= pathArray.Count - 2 ) Debug.DrawLine( ( (Node)pathArray[cnt] ).position, ( (Node)pathArray[cnt + 1] ).position, Color.green); } } } }


這個腳本主要是用來呼叫前面幾篇寫好的方法

直接來看怎麼使用 TestAStar.cs


在場景中新增一空物件取名為 AStar

並新增兩個 Cube 分別取名為 Start 以及 End 當作起始點與終點

並將兩個 Cube 分別拉近 AStar 欄位中

執行開始則會看到實作結果



到此 A* 演算法實作已經完成了

不好意思 我是還在學習的新手

因為想做戰棋遊戲所以來參考你的A*文章

理解演算法也花了很久的時間

在這篇實作結果

Unity執行開始後

卻出現InvalidOperationException: No IComparable or IComparable interface found.

錯誤

想請問這是甚麼原因應該如何解決

LikeLike

IComparable 在這篇中有提到 https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-node-definition/

它是一個 C# 介面

詳細資料可以直接從 MSDN 中查看 https://msdn.microsoft.com/zh-tw/library/system.icomparable(v=vs.110).aspx

LikeLike

太神了

LikeLike