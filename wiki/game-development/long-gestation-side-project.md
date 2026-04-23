---
tags: [indie, side-project, career, codebase-reuse, proun]
date: 2026-04-19
sources: 1
---

# 六年业余项目 Proun —— 独立游戏的长孕期与复用链

[[joost-van-dongen]] 把 Proun 从 2005 年「CableRacer」原型一直磨到 2011 年 6 月正式发行，前后六年。他在回顾里把这段时间拆成两个事实：**(1) 全程业余时间；(2) 中间有大段时间完全没碰**。这种「长孕期副项目」是独立开发里常见却很少被细写的模式。

## 时间线结构

- **2004** HKU 第二学年，大班两组做赛车项目全部搞砸；Joost 的同学 Huub 曾提过「绕电缆躲障碍」的极简点子被组内否决。
- **2005 春-夏** Joost 捡起这个点子，取名 CableRacer，学着用 Ogre 引擎搭起原型；自写 3ds Max 插件做 mesh/bezier 导出；几周内可玩。
- **2005 夏 - 2006 春** 停工一年：去德国 Collision Studios 做 Red Ocean 的 3D normal-mapped 美术实习。
- **2006** 回 HKU 做 **De Blob**：直接剥 CableRacer 代码改成 3D 物理 gameplay，几天就跑起来；De Blob 完工后再把积累反哺回 CableRacer。
- **2006 夏** 画面方向尝试 Mondriaan 失败（直线与 Proun 的曲线不兼容），转向 Kandinsky 后期几何抽象期作品，确立最终美学。
- **2006-2009** 三年停工：[[ronimo-games|Ronimo]] 成立、做 Guerrilla 的 Killzone 衍生练习项目（又是从 CableRacer 代码库改出）、**Snowball Earth**（融资失败被砍，也是 CableRacer 衍生）、**Swords & Soldiers**；同时攻读 Utrecht 大学 Game & Media Technology 硕士，周末全用在论文上。
- **2009 夏** 硕士完成，玩三周游戏玩腻了，做了个巴洛克教堂穹顶 3D 模型（卡住），顺手回到 Proun。一个几个月后的新 trailer 复活项目。
- **2009 末** Van Abbe 博物馆看到 El Lissitzky 的「Proun」系列抽象构成作品——这个 Lissitzky 虚构的词正好契合游戏气质，游戏改名为 Proun。
- **2010-2011** 音乐与音效由 Arno Landsbergen 接手；继续做赛道、打磨；最终 2011-06-24 以 *Pay What You Want* 模式发行 PC 版。

## 代码复用链

六年里 CableRacer/Proun 的代码库衍生出至少四个项目：**De Blob**（HKU 学校项目）→ **Killzone 人群控制练习**（Guerrilla assignment）→ **Snowball Earth**（Ronimo 首款被砍游戏）→ 最终的 **Proun** 正式版。这是一条很能说明问题的链条：副项目的核心 codebase 同时是商业项目的起跑架，商业项目完成后又反哺回副项目。

## 模式要点

- **业余时间 + 断续推进**并不等于失败，反而让作者跨越式成长——从不会写 shader 到能处理 Kandinsky 风格烘焙。
- **副项目代码反复被抽出来做正式项目的地基**，双向受益。
- **美术方向需要真正喜欢的艺术家参考**（Joost 说 Kandinsky 是他最爱的画家）；方向错了（Mondriaan）就换。
- **命名可以等到项目接近完成**：Lissitzky 那个词是 2009 年才冒出来的礼物。

## Sources

- [[sources/joostdevblog-proun-history]]
