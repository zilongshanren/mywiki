---
tags: [source, rendering, pc-porting, drivers, qa, compatibility]
date: 2026-04-19
sources: 1
---

# The horror that is PC development（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen]] 2010 年 12 月发表的文章，借 *Swords & Soldiers* 上 Steam 的血泪经验主张：**PC 发行比主机发行难**。

## 摘要

主机认证（PS3 / Wii / 360）虽有几百条 TRC/TCR 要求，但内容合理、目标硬件 uniform——测一台 PS3 等于测所有 PS3。PC 在「硬件 × 驱动 × Windows × 用户设置」的笛卡尔积里挨坑。文章列举 *Swords & Soldiers* / *De Blob* / *Proun* 四个真坑：(1) **NPOT 检测**——查 GL 扩展不靠谱，van Dongen 放弃自动识别、让用户坏了再切 SD；(2) **max vertex index**——某些老 Intel 板载上限 65534 顶点，Proun 作为 hobby 不拆 mesh；(3) **shader 能力说谎**——*De Blob* 遇到显卡声称支持 shader 2.0、实际拒载；(4) **`glTexSubImage2D` 玄学**——*Swords & Soldiers* 动态字形 QA 后加入未复测，\~1% 用户完全看不到字，Day-1 补丁绕开该函数，根因没查清。评论补充：双显示器不同刷新率卡全屏 DX、DirectX SDK 的 *CardCaps.xls* 列出了最低 MaxVertexIndex 值可查。后续 Q&A 里他给出 *Awesomenauts* 工作室的 QA 流程：**用最烂老 GPU 当毒药测试机**、发前 Steam beta、发后靠当日热补丁、给报 bug 的用户寄带日志的定制 build 协作排查。

## 关键要点

- 论点：PC 发行 > 主机发行（难度上）。主机硬件 uniform、合理；PC 是硬件笛卡尔积
- 坑 1：NPOT 扩展查询不可靠 → 放弃自动 detect，改用户选
- 坑 2：老 Intel max vertex index = 65534（*CardCaps.xls* 可查）
- 坑 3：shader 2.0 能力查询说谎
- 坑 4：`glTexSubImage2D` 在部分卡上炸字体；疑似和 IA8 / RGBA 纹理格式相关
- QA 流程：老 GPU netbook、Steam beta、Day-1 patch、玩家协作 custom build
- 可迁移结论：2025 年硬件分布更散（Proton / 集显 / 多厂），原则只会更强

## 链接到的概念

- [[pc-gpu-driver-compat-qa]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/12/horror-that-is-pc-development.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-12-04_the-horror-that-is-pc-development.md`
