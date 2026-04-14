---
tags: [source, 颜色, 显示, EDID, Windows]
date: 2026-04-14
sources: 1
---

# Extracting your display Colorspace（Robin Green / Bases and Frames）

[[robin-green]] 2017 年的一篇短文，介绍如何用 Windows PowerShell + WMI 把每台机器接的显示器的 RGB 三原色色度和白点从 EDID 记录里拉出来——作为[[display-edid-colorspace|低成本筛查 wide-gamut 显示器]]的手段。

## 摘要

EDID（Extended Display Identification Data）起源于 VGA 时代的一条数字串行侧信道：把显示器插上电脑时，一组 SPI 两线协议允许显示器把自己的能力表（支持的刷新率等）告诉显卡，以免电脑输出一个会把 CRT 打坏的信号。标准的 EDID block 还包含显示面板 **R/G/B 三原色的 CIE xy 色度和默认白点**——也就是这块显示屏的原生 gamut 顶点。

文章提供了一段 PowerShell 脚本：查询 `root\wmi` 命名空间下的 `WmiMonitorColorCharacteristics` 类，把 `$_.Red.X / 1024.0` 这类整数归一化成浮点 xy 坐标，组织成一个包含 `Monitor / Red / Green / Blue / White` 字段的对象。有 admin 权限的话可以把这段代码推到整个 domain 的所有机器上，得到整栋楼每台机器显示屏的 primaries 表格——非常适合前期筛查有没有值得进一步测试的 wide-gamut / HDR 屏。

需要注意：EDID 里报告的色度**不完全可信**——有的面板厂会填入 sRGB 样板值而不是真实面板能力，所以这只是一阶筛查，不能替代实测。

## 关键要点

- EDID 记录里已经嵌入了显示器自报的 primaries + 白点——一次 WMI 查询就能拿到。
- Windows 下不需要装额外工具：PowerShell + `Get-WmiObject -Namespace root\wmi -Class WmiMonitorColorCharacteristics` 即可。
- 色度整数字段需要除以 1024 得到标准 xy 坐标（这是 EDID block 的固定缩放）。
- 可以扩展成跨 domain 的批量扫描脚本，得到整个组织的显示器 gamut 调查。
- **数据可信度有限**：厂商可能填 sRGB 样板值而不是真实面板能力，只能作为一阶筛查。
- 这个套路是把显示-侧的 [[color-space|色彩空间]]主动化：传统上应用假定 sRGB，EDID 让你知道实际面板能做到什么。

## 链接到的概念

- [[display-edid-colorspace]]
- [[color-space]]
- [[robin-green]]

## 原文

- 链接：https://basesandframes.wordpress.com/2017/05/12/extracting-your-display-colorspace/
- 本地：`raw/articles/basesandframes.wordpress.com/2017-05-12_extracting-your-display-colorspace.md`
