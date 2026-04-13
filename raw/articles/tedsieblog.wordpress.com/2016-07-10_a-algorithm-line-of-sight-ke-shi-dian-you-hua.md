---
title: A* Algorithm Line of Sight – 可視點優化
url: https://tedsieblog.wordpress.com/2016/07/10/a-start-algorithm-line-of-sight/
author: Ted Sie
published: '2016-07-10'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

偶然和同好聊到 A* 時

得知了一種優化方法

可以得到更高效能的運算結果


先來看一張沒有用這種方法優化所算出來的路徑



可以看出雖然原來的方法所算出來的路徑的確正確

但卻又不能算是最佳路徑

原因在於一定要經過我們所定義出可行走的點

但如果將算出來的路徑再重製一次後會不會得到更好的結果呢?


可視點優化(Line of sight)：

原理相當簡單，我們人在行走時如果遇到上面這種狀況

一定會以我們 “看” 到的最佳點前進

以上圖為例

我們在左下角的起點要向右上角的終點移動時

一定會直接以紅框為下一個目標點

因為我們可以 “看” 見紅框點


找到專案中的 AStar.cs

並新增 Function 如下

private static ArrayList LineOfSight( ArrayList path ) { ArrayList list = new ArrayList(); list.Add( (Node)path[0] ); Node startNode = (Node)path[0]; Node nextNode; int checkIndex = 1; while( checkIndex < path.Count ) { nextNode = ( (Node)path[checkIndex] ); if( !Physics.Linecast( startNode.position, nextNode.position ) ) { checkIndex++; } else { if( checkIndex == path.Count - 1 ) { list.Add( (Node)path[checkIndex - 1] ); list.Add( (Node)path[checkIndex] ); } else { list.Add( (Node)path[checkIndex - 1] ); startNode = (Node)path[checkIndex - 1]; nextNode = (Node)path[checkIndex]; } checkIndex++; } } return list; }


接著找到原來的 CalculatePath 方法

並修改成

private static ArrayList CalculatePath(Node node) { ArrayList list = new ArrayList(); while (node != null) { list.Add( node ); node = node.parent; } list.Reverse(); return LineOfSight( list ); }


這樣一來就可算出 Line of sight 優化過後的路徑



和沒有優化的路徑相比

是不是又更簡單明瞭

附上一張多障礙物模擬


大大您好 我用完之後 scene上就顯示不出來路徑了 請問可能是甚麼原因

LikeLike

已解決 原來是我點位置放錯 感謝大大的分享

LikeLike