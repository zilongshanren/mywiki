---
title: Verlet Integration – A Case Study of Boundary and Rope Simulator
url: https://tedsieblog.wordpress.com/2020/03/04/verlet-integration-a-case-study-of-boundary-and-rope-simulator/
author: Ted Sie
published: '2020-03-04'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

一般而言在實作物體移動時會使用**Kinematic Equation 運動方程式**

由於運動方程式需要速度

加速度等資訊才能夠有效運算

**Verlet Integration 韋爾萊積分法**則是另一種運動方程式的解決方案

能夠在不需要速度的前提下

只依靠物體的當前位置、前一幀位置就模擬出結果


##### Kinematic Equation 運動方程式

在離地五公尺的地方放開一顆球

想要知道這顆球的位置與時間的關係

從高中物理等加速度運動公式可以得知

##### Verlet Integration 韋爾萊積分法

本質上是運動方程式的一種解決方案

將時間變化量帶入運動方程式

調整為


由此可知

只要知道當前位置 、前一位置

、加速度

、時間變化量


在不需要物體速度的前提下

即可求得物體的下一位置


##### 實作範例 – 邊界限制

**1. 定義移動點**

public struct Dot { public Vector3 position; public Vector3 prevPosition; public Dot(Vector3 position, float defaultVelocity) { this.position = position; prevPosition = position - Quaternion.Euler(0, 0, Random.Range(0f, 360f)) * Vector3.up * defaultVelocity; } }

**2. 計算 Verlet Integration**

//定義加速度為 0 Vector3 newPosition = 2 * position - prevPosition;

**3. 邊界條件判斷**

![](../../assets/8ccb3f4802bdf68e.jpg)


![](../../assets/296b3d1c3cb6bc1f.jpg)


![](../../assets/71ebda5c8120861a.jpg)


![](../../assets/962434843ec24939.jpg)


**4. 完成**

![](../../assets/c426bfb130eed7c9.gif)


![](../../assets/44e1666c3d6d2f2c.gif)


##### 實作範例 – 繩索模擬

**1. 定義繩索節點**

public struct Node { public Vector3 position; public Vector3 prevPosition; public bool pinned; public Node(Vector3 position) { this.position = position; prevPosition = position; pinned = false; } }

**2. 生成繩索節點**

**3. 計算 Verlet Integration**

for(int i = 0; i < m_lastNodeCount; i++) { Node node = m_nodes[i]; Vector3 position = node.position; Vector3 prevPosition = node.prevPosition; Vector3 newPosition = 2 * position - prevPosition + m_finalGravity; node.position = newPosition; node.prevPosition = position; m_nodes[i] = node; }

**4. 繩索位置約束**

當繩索兩端為固定點時，用於約束繩索兩端

private void ApplyPinned(TargetData targetData) { int index = targetData.index; Node node = m_nodes[index]; node.pinned = targetData.IsPinned(); if(node.pinned) { node.position = targetData.GetPosition(); m_nodePositions[index] = node.position; } m_nodes[index] = node; }

**5. 繩索長度約束**

![](../../assets/fcb6d0b6d4d415b3.jpg)


![](../../assets/d27b35cec97f50eb.jpg)


**6. 更新節點位置**

**7. 完成**

![](../../assets/9a839a80ee12f039.gif)


![](../../assets/759bae5101e7738e.gif)


![](../../assets/d6f264cc0811e3f4.gif)


##### Patreon 連結

##### 範例原始碼

##### 參考資料

[Math for Game Developers – Verlet Integration](https://www.youtube.com/watch?v=AZ8IGOHsjBk)

[2D Rope Tutorial – Make Swinging Rope in Unity (Verlet Integration)](https://www.youtube.com/watch?v=FcnvwtyxLds)

[Create Rope Bridge, String in Unity – Verlet Integration Part 2](https://www.youtube.com/watch?v=k32g4ujzxP0)

[Verlet Integration · GitBook](https://www.algorithm-archive.org/contents/verlet_integration/verlet_integration.html)

[Coding Math: Episode 37 – Verlet Integration Part I](https://www.youtube.com/watch?v=3HjO_RGIjCU)

[Coding Math: Episode 36 – Verlet Integration Part II](https://www.youtube.com/watch?v=pBMivz4rIJY)

[Coding Math: Episode 38 – Verlet Integration Part III](https://www.youtube.com/watch?v=tAd7ttKbugA)

[Coding Math: Episode 39 – Verlet Integration Part IV](https://www.youtube.com/watch?v=YgRZDCBLDfs)

## One thought on “Verlet Integration – A Case Study of Boundary and Rope Simulator”