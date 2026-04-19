---
tags: [source, unity, urp, 编辑器]
date: 2026-04-19
sources: 1
---

# Where to find URP Settings（cmwdexint）

[[ming-wai-chan]] 发表于 2021 年 12 月的一页短速查，回答"URP 相关设置都藏在 Unity 编辑器的哪里"。

## 摘要

URP 的配置被 Unity 分散到四个互相依赖的入口：Preferences（控制高级属性是否可见的个人偏好）、Project Settings → Quality（每个 Quality Level 绑定的 Render Pipeline Asset）、Project Settings → Graphics → URP Global Settings（全局 shader stripping 等）、以及 Project 视图里选中 Render Pipeline Asset 自己的 Inspector（三点菜单里的 *Show Additional Properties*）。这些设置互相依赖：想看高级属性需要先在 Preferences 里允许可见、Pipeline Asset 生效必须被 Quality Level 选上。是 URP 常见的**配置发现问题**之一——设置不是不存在，只是入口散。

## 关键要点

- 偏好：Preferences → Core Render Pipeline → Additional Properties → Visibility。
- 项目级：Project Settings → Quality 绑定 Pipeline Asset；Project Settings → Graphics → URP Global Settings 管全局。
- Pipeline Asset 的高级属性：Inspector 右上角三点 → Show Additional Properties，并受 Preferences 里 Visibility 开关控制。

## 链接到的概念

- [[urp-settings-locations]]

## 原文

- 链接：https://cmwdexint.com/2021/12/02/where-to-find-urp-settings/
- 本地：`raw/articles/cmwdexint.com/2021-12-02_where-to-find-urp-settings.md`
