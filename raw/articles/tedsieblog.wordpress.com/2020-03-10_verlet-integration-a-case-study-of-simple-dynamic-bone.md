---
title: Verlet Integration – A Case Study of Simple Dynamic Bone
url: https://tedsieblog.wordpress.com/2020/03/10/verlet-integration-a-case-study-of-simple-dynamic-bone/
author: Ted Sie
published: '2020-03-10'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

[Dynamic Bone](https://assetstore.unity.com/packages/tools/animation/dynamic-bone-16743) 是 [Unity Asset Store](https://assetstore.unity.com/) 中的一套動態骨骼系統，開發者不需要任何的程式基礎也能夠快速上手並使用動態骨骼功能，透過簡易的設定就能夠快速的進行物理模擬，讓腳色的頭髮、衣服、胸部…等物體進行更加真實的物理移動。

在先前的文章 [Verlet Integration 韋爾萊積分法 – 以邊緣檢測與繩索模擬為例](https://tedsieblog.wordpress.com/2020/03/04/verlet-integration-a-case-study-of-boundary-and-rope-simulator/) 中，在韋爾萊積分法的基礎上實作了邊緣檢測，並加入長度約束藉此模擬繩索擺動。

Dynamic Bone 則是在韋爾萊積分法的基礎上額外加入了**重力**、**外力**、**慣性**、**阻力**、**彈性**、**剛性**、**碰撞**、**長度約束**等因素，模擬出更真實的物理移動。

此篇文章將重點放在如何在韋爾萊積分法的基礎上加入**慣性**、**阻力**、**彈性**、**剛性**、**長度約束**，藉此變化出簡化版的動態骨骼，不但有效的優化了原版動態骨骼的效能，還會解釋動態骨骼中的韋爾萊積分法及每個步驟的物理模擬是如何計算的。


##### 使用參數說明

**慣性**: 物體具有保持原來運動狀態的性質。

**阻力**: 系統的振盪多快可以衰減。

**彈性**: 物體發生變形，讓物體恢復原本形狀的性質。

**剛性**: 施力與變形量的比值。

##### 簡易 Dynamic Bone 說明

**1. 計算物體慣性**

物體上一幀位置


物體當前位置



**2. 慣性模擬**

節點上一幀位置


節點當前位置



**3. Verlet Integration 數學式**


**4. 阻力模擬**


**5. 彈性模擬**

節點目標位置


節點目標位置與當前位置差



**6. 剛性模擬**

節點目標位置與當前位置長度


父節點實際位置


節點實際位置


父節點實際位置與節點實際位置長度



**7. 長度約束**

父節點實際位置與當前位置差



##### 簡易 Dynamic Bone 實作

**1. 計算物體慣性**

m_objectInertia = transform.position - m_objectPrevPosition; m_objectPrevPosition = transform.position;

**2. 慣性模擬**

//Inertia Vector3 particleInertia = m_objectInertia * inertia; particle.prevPosition += particleInertia; particle.position += particleInertia;

**3. 阻力模擬**

//Damping Vector3 velocity = particle.position - particle.prevPosition; particle.prevPosition = particle.position; particle.position += velocity * (1 - damping);

**4. 彈性模擬**

//Elasticity Matrix4x4 m0 = parentParticleTrans.localToWorldMatrix; m0.SetColumn(3, parentParticle.position); Vector3 targetPosition = m0.MultiplyPoint3x4(particleTrans.localPosition); Vector3 delta = targetPosition - particle.position; particle.position += delta * elasticity;

**5. 剛性模擬**

//Stiffness float deltaLength = delta.magnitude; float length = (parentParticleTrans.position - particleTrans.position).magnitude; float lengthMax = length * 2 * (1 - stiffness); if (deltaLength > lengthMax) { particle.position += delta * (deltaLength - lengthMax) / deltaLength; }

**6. 長度約束**

//Length Constraint delta = parentParticle.position - particle.position; deltaLength = delta.magnitude; particle.position += delta * (deltaLength - length) / deltaLength;

**7. 更新旋轉及位置**

Vector3 v = particleTrans.localPosition; Quaternion rot = Quaternion.FromToRotation(parentParticleTrans.TransformDirection(v), particle.position - parentParticle.position); parentParticleTrans.rotation = rot * parentParticleTrans.rotation; particleTrans.position = particle.position;

##### 成果展示

![](../../assets/45c3af1d88efa3f2.gif)


![](../../assets/18cb80a10bb7f1fc.gif)


##### Patreon 連結

##### 完整原始碼

##### 參考資料

[Inertia – Wikipedia](https://en.wikipedia.org/wiki/Inertia)

[Damping ratio – Wikipedia](https://en.wikipedia.org/wiki/Damping_ratio)

[Elasticity (physics) – Wikipedia](https://en.wikipedia.org/wiki/Elasticity_(physics))

[Stiffness – Wikipedia](https://en.wikipedia.org/wiki/Stiffness)

[动态骨骼Dynamic Bone算法详解](https://zhuanlan.zhihu.com/p/49188230)