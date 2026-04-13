---
title: A* Algorithm Node Definition – 定義 Node
url: https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-node-definition/
author: Ted Sie
published: '2016-07-08'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

首先開一個新的 Unity 專案

新增一個 C# 腳本命名為 Node.cs

Node.cs 是用來定義 Node 的相關資訊

using UnityEngine; using System.Collections; using System; public class Node : IComparable { //G cost is current cost public float G_Cost; //H cost is estimate cost public float H_Cost; //Desicion the node can move or not public bool isObstacle; //Record the node's parent public Node parent; //the position of the node public Vector3 position; //Initial the node public Node() { this.G_Cost = 0.0f; this.H_Cost = 0.0f; this.isObstacle = false; this.parent = null; } //Initial the node with position public Node(Vector3 pos) { this.G_Cost = 0.0f; this.H_Cost = 0.0f; this.isObstacle = false; this.parent = null; this.position = pos; } //Set the node to be an obstacle public void MarkAsObstacle() { this.isObstacle = true; } //Because our Node class inherits from IComparable, we need to override this CompareTo method. //We need to sort our list of node arrays based on the total cost of G and H. //The ArrayList type has a method called Sort. //Sort basically looks for this CompareTo method, implemented inside the object ( in this case our Node objects ) from the list. //The IComparable.CompareTo method can be found at http://msdn.microsoft.com/en-us/library/system.icomparable.compareto.aspx. public int CompareTo( object obj ) { Node node = (Node)obj; //If new node's total cost is bigger than old node, don't change if ( this.G_Cost + this.H_Cost < node.G_Cost + this.H_Cost ) return -1; //If new node's total cost is smaller than old node, change if ( this.G_Cost + this.H_Cost > node.G_Cost + this.H_Cost ) return 1; return -1; } }

G_Cost：用來記錄該 Node 的已知移動距離

H_Cost：計算該 Node 到終點的估算距離

isObstacle：判斷該 Node 是否為障礙物

parent：記錄移動到此 Node 的上一個 Node

position：記錄該 Node 的位置資訊

這段程式碼裡最重要的片段為 CompareTo()

因為 Node clas s繼承了 IComparable interface

所以必須複寫 CompareTo，否則會導致編譯錯誤

CompareTo 的作用是用來排序

在前一篇中有提到 Heuristic Estimate 公式，

其目的就是再判斷下一個 Node，

而判斷下一個 Node 的方法就是計算它的 G + H 值，

該值越小則優先計算

各位也可以先試著想想看

目前已經定義出 Node 結構

下一步就是要建立一個資料結構用來處理 Node 的相關排序

例如：新增Node、移除Node、排序Node

大大您好 請問compareto這邊是不是多註解調Change後面的if判斷

LikeLike