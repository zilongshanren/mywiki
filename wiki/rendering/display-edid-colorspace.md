---
tags: [颜色, 色彩空间, 显示, EDID, 操作系统]
date: 2026-04-14
sources: 1
---

# 从 EDID 提取显示器色彩空间（Display EDID Colorspace）

每台接到电脑上的显示器都会通过 **EDID（Extended Display Identification Data）** 自报一份「身份卡」——包含分辨率、刷新率、厂商、面板能力，以及**面板原生的 R/G/B 三原色色度和默认白点**。这些色度坐标加上白点就定义了一个该显示器理论上的 **native gamut**，可以和 sRGB / DCI-P3 / Rec.2020 等标准色域直接做三角形包含检查——这是应用层做「当前屏是不是 wide-gamut」判断的最低成本途径。

## EDID 是什么

EDID 起源于 VGA 时代的一条数字串行侧信道：VGA 线里预留了两根额外的针脚走 SPI/I²C 协议，显示器通电后通过它把 128 字节（后续扩展到 256/512 字节）的 EDID block 告诉显卡，防止显卡输出一个会把 CRT 打坏的信号（例如超出行频范围）。随着 DVI/HDMI/DisplayPort 的发展，EDID 被继承下来并扩展了 **CEA** 和 **DisplayID** 等附加块。EDID 标准块里固定有一段 **chromaticity bytes**，编码了 R/G/B/White 四点的 CIE xy 坐标——每个分量用 10 bit 精度存储。

## 在 Windows 上抽出来

Windows 的 WMI（Windows Management Instrumentation）提供 `root\wmi\WmiMonitorColorCharacteristics` 类，直接把 EDID 的色度字段暴露为对象属性。用 PowerShell 查询即可：

```powershell
Get-WmiObject -Namespace root\wmi -Class WmiMonitorColorCharacteristics
```

返回对象里的 `Red.X`, `Red.Y`, `Green.X`, `Green.Y`, `Blue.X`, `Blue.Y`, `DefaultWhite.X`, `DefaultWhite.Y` 都是 10-bit 整数，**除以 1024.0** 得到标准 CIE xy 坐标。Robin Green 提供了一段包装脚本把这些字段组织成 PSObject 返回。

有 admin 权限的话，可以把脚本推到整个 Windows domain 的所有机器上做批量扫描，得到一张「整栋楼每个显示器的色度」电子表格——**前期筛查 wide-gamut 显示器的零成本方案**。

## 可信度警告

EDID 里的色度**并不完全可信**：

- 一些面板厂为了简化，填入 sRGB 的样板值（比如所有 IPS 面板都写 Rec.709 原色），而不是真正的面板原生 gamut。
- 一些 OEM 显示器的 EDID 是「通用模板」，没做 per-panel 校准。
- 有时厂商会故意写「更窄」的 gamut，因为有些驱动的色彩管理在宽 gamut 下处理得差。

因此 EDID 只应作为**一阶筛查**——得出候选之后用专门的分光光度计（比如 X-Rite i1）实测才算。

## 为什么有用

游戏和图形应用传统上假设「显示器是 sRGB」，但：

- 现代 4K / OLED 面板很多是 DCI-P3，色域比 sRGB 大约大 25%；
- Rec.2020 目标在 HDR10/Dolby Vision 内容流行后越来越常见；
- 同一张 [[color-space|线性 RGB 图]]在 sRGB 监视器和 P3 监视器上会明显不同。

应用层主动读取 EDID 可以做到「开机就知道屏能做什么」——而不是盲目假设 sRGB 再让用户吐槽色彩偏差。

## 相关

- [[color-space]] — RGB 值必须配色彩空间才有意义
- [[oklab-color-space]]
- [[robin-green]]

## Sources

- [[sources/green-display-edid-colorspace]]
