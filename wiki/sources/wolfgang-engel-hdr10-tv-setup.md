---
tags: [source, graphics, hdr, 色彩管理, 显示器]
date: 2026-04-19
sources: 1
---

# HDR10 - TV setup（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel|Wolfgang Engel]] 2017 年 4 月发表在 *Diary of a Graphics Programmer* 的一篇短笔记——记录**把一款 LDR demo 搬到 HDR10 电视上意外翻车**后的反思。

## 摘要

Confetti 办公室有不少 HDR 电视（因为做 HDR 标准相关工作），平时跑 HDR 内容都没问题。但在一次会议上，Engel 把一个**没有做任何 HDR 处理**的 LDR demo（没有 tone mapper、art asset 都是 LDR）接到会场提供的 HDR10 电视上，发现画面「丑到震惊」。这让他意识到**LDR 并不是 HDR 的一个「直接可显示的子集」**。HDR10 电视菜单有几十个滑杆分散在多个子菜单里——普通用户根本没法调到一个合理状态。Engel 由此提出几个悬而未决的问题：游戏要不要随附各品牌电视的推荐设置？要不要像 PC 显卡那样推荐显示器？能不能像过去的 gamma 校准屏那样给 HDR 也设计一套标准校准步骤？

评论区一位读者补上了技术解释：过去 20 年 SDR 生态建立在 Rec.709 之上，显示器默认 Rec.709 + BT.1886 gamma；但今天的面板实际把 `(1,1,1)` 映射到 ~300 nits（而非标准的 100 nits），并且加了"vividness"让颜色转出 Rec.709 色域。Rec.2100 标准设计时本来就假定 SDR 信号要**按 100 nits scale 到 300 nits + Rec.709 → Rec.2100 色域旋转 + PQ 编码**才能还原出观众习惯的效果。这套变换是从 SDR 过渡到 HDR10 的"最低限度"做法。

## 关键要点

- LDR → HDR 并非「直接兼容」——默认显示到 HDR10 面板上是「又暗又失色」，必须主动把内容 scale 到 ~300 nits 参考白
- 没有 tone mapper 的 LDR demo **几乎注定**在 HDR10 电视上翻车
- HDR10 电视菜单的复杂度已经超出普通用户——对 ship 一款 HDR 游戏的开发者来说这是真实的发行风险
- Rec.2100 规定了 SDR → HDR10 的转换公约：scale 到 300 nits + Rec.709 → Rec.2020 色域旋转 + PQ 编码
- Engel 提出一个开放问题：HDR 能否像 gamma 校准图那样做一套标准化的**色彩 / 亮度校准屏**？（到 2026 仍无普遍共识）

## 链接到的概念

- [[color-space]] —— Rec.709 vs Rec.2020 / BT.1886 vs PQ
- [[hdr-video-edr-metal]] —— Apple 平台的 EDR 自适应 tonemap
- [[local-tonemapping]] —— 从 HDR → 显示域的艺术选择
- [[display-edid-colorspace]] —— 从 EDID 读出显示器实际 gamut
- [[people/wolfgang-engel]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2017/04/hdr10-tv-setup.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2017-04-07_hdr10-tv-setup.md`
