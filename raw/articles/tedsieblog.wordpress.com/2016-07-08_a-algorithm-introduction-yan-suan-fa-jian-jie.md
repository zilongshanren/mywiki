---
title: A* Algorithm Introduction – 演算法簡介
url: https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-introduction/
author: Ted Sie
published: '2016-07-08'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

A*(A-Star) 是一種知名的演算法，在遊戲中通常被應用在尋找最短路徑。

在介紹 A* 演算法之前，必須先稍微提一下另一個知名的演算法，Dijkstra 演算法。

Dijkstra 演算法可以保證找到最短路徑，但在演算效能上卻沒有 A* 來的快速，A* 也就是因為考慮到 Dijkstra 的演算速度而進行改良的一種演算法。

接下來先來看一下 Dijkstra 演算法與 A* 演算法兩者的差異：

先不考慮兩者的演算方式，讀者們看到比較圖後會發現Dijkstra演算法的演算深度(有顏色的方格數)與A*演算法的演算深度兩者的差別，雖然A*的演算深度不如Dijkstra演算法，但其結果與效能是令人滿意的。

A*演算法能達到這樣令人滿意的結果，是因為它採用了一套特殊評價公式（Heuristic Estimate），這個公式避免了一些不必要的路徑排除，所以能用較高的演算效率計算出一條最佳結果。

Heuristic Estimate的公式如下：

F(n) = G(n) + H(n)

n：目前節點

G(n)：從起始點到目前節點實際移動的距離

H(n)：目前節點到終點的估算值

F(n)：目前節點的評價分數總和

A*演算法的虛擬程式碼如下：

AddStartNodetoOpenListwhileOpenListis not empty get the first node n form theOpenListremove node n from theOpenListadd node toCloseListif n isEndNodereturn the path get neighbors of node n and count cost if neighbors is not inOpenListadd it toOpenListelse if the cost of G is smaller than old one update the cost value of G end while


**A* 演算法系列文章連結**

[A* Algorithm Node Definition – 定義 Node](https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-node-definition/)

[A* Algorithm Node Sort – Node 排序實作](https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-node-sort/)

[A* Algorithm Node Generate – 生成 Node、Node 可視化](https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-node-generate/)

[A* Algorithm Implement – 虛擬程式碼實例化](https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-implement/)

[A* Algorithm Achievement – 演算法實作成果](https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-achievement/)

[A* Algorithm Obstacle Detection – 障礙物判定](https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-obstacle-detection/)

[A* Algorithm Eight Ways – 斜向方向優化](https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-eight-ways/)

[A* Algorithm Line of Sight – 可視點優化](https://tedsieblog.wordpress.com/2016/07/10/a-start-algorithm-line-of-sight/)

## 4 thoughts on “A* Algorithm Introduction – 演算法簡介”