---
title: A* Algorithm Eight Ways – 斜向方向優化
url: https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-eight-ways/
author: Ted Sie
published: '2016-07-10'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

到目前為止

A* 的基本實作都已經結束了

但我們可以做一些簡單的優化來提高 A* 的運算結果


在上一篇中可以發現

雖然計算出來的路徑的確是最短路徑

但在移動方向上卻只限制於上下左右四個方向


考慮到優化演算的結果

我們在這邊加入斜向方向判定


首先一樣找到 NodeManager.cs 腳本

找到 GetNeighbours 方法

//Get the current node's neighbors public void GetNeighbours( Node node, ArrayList neighbors ) { Vector3 neighborPos = node.position; int row = GetNodeRow( neighborPos ); int column = GetNodeColumn( neighborPos ); //Bottom int leftNodeRow = row - 1; int leftNodeColumn = column; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); //Top leftNodeRow = row + 1; leftNodeColumn = column; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); //Right leftNodeRow = row; leftNodeColumn = column + 1; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); //Left leftNodeRow = row; leftNodeColumn = column - 1; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); }

在原本的方法中

我們只有上下左右四個方向

所以在這邊將斜向方向也一併加入運算

//Get the current node's neighbors public void GetNeighbours( Node node, ArrayList neighbors ) { Vector3 neighborPos = node.position; int row = GetNodeRow( neighborPos ); int column = GetNodeColumn( neighborPos ); //Bottom int leftNodeRow = row - 1; int leftNodeColumn = column; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); //Top leftNodeRow = row + 1; leftNodeColumn = column; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); //Right leftNodeRow = row; leftNodeColumn = column + 1; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); //Left leftNodeRow = row; leftNodeColumn = column - 1; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); //Bottom Right leftNodeRow = row - 1; leftNodeColumn = column + 1; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); //Bottom Left leftNodeRow = row - 1; leftNodeColumn = column - 1; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); //Top Right leftNodeRow = row + 1; leftNodeColumn = column + 1; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); //Top Left leftNodeRow = row + 1; leftNodeColumn = column - 1; AssignNeighbour(leftNodeRow, leftNodeColumn, neighbors); }


再次執行 Unity

結果如下



加入斜向移動後果然移動距離又更短了

最後附上多個障礙物的模擬


## 3 thoughts on “A* Algorithm Eight Ways – 斜向方向優化”