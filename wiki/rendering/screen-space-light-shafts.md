---
tags: [light-shafts, god-rays, screen-space, post-process, volumetric]
date: 2026-04-19
sources: 1
---

# 屏幕空间 light shafts / god rays

体积光（volume light / god rays / Jacob's ladder）的物理正解要求沿视线 ray-march 空气中大量采样点，每点查询密度、散射、以及**该点是否被阴影遮挡**——相当于在空气里额外跑一套 shadow 查询。2010 年的硬件完全承受不起。

游戏里普遍用的替身是一个和真实体积光**几乎零物理关系**的屏幕空间 trick：**从当前像素向屏幕里太阳投影的那个点走一条 2D 直线，沿途采样已经渲染好的图像亮度并按距离衰减累加**。雾密度、阴影、立体散射全部被忽略，但最终出图极其接近真实体积光（Far Cry 2、Crysis 都是这个做法）。[[joost-van-dongen]] 在 *Proun* 第三条赛道上接入了同款效果，原始出处是 GPU Gems 3 第 13 章。

**核心限制**：**太阳必须在屏幕内**——如果手电筒背对相机、或阳光从屏外射来，采样路径就没有亮源可走，效果退化为零。这个限制使它无法胜任一般的体积光（例如室内聚光灯），只适合「光源本身可见」的外景场景。

整条技术是 van Dongen 自己反复提到的他最喜欢的例子——shader 作为一门「**物理扔掉、感觉保留**」的创意手艺：不写 ray-march、不查密度场、不做 shadow volume，只是把图像当成光强图在 2D 平面上向一个点扫一遍，就能骗出让人信服的大气散射。

## 相关

- [[volumetric-raymarching-intro]] —— 物理正解一端的对照
- [[volumetric-fog-raymarch-shadows]]
- [[joost-van-dongen]]

## Sources

- [[sources/joostdevblog-sun-rays]]
