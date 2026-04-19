---
tags: [unity, urp, 编辑器, 配置]
date: 2026-04-19
sources: 1
---

# URP 设置面板的散落地图

URP 相关的配置**不在一个地方**，Unity 把它们分散到偏好、项目设置、Asset 检视器等四处。Ming Wai Chan 列了一张入口速查，省得每次找半天。

- **Preferences → Core Render Pipeline → Additional Properties → Visibility**：控制检视器里 *Additional Properties*（高级属性）是否可见。这是一个**编辑器本地偏好**，不会进版本库。
- **Project Settings → Quality**：每个 Quality Level 绑定一个 *Render Pipeline Asset*。切 Quality 等于切一整套 URP 设置。
- **Project Settings → Graphics → URP Global Settings**：URP 全局设置（如 shader stripping、lighting layer 的可用性），与具体 pipeline asset 无关。
- **Project 视图 → 选中 Render Pipeline Asset → Inspector 右上角三点 → "Show Additional Properties"**：打开该 asset 的 *高级属性*（和 Preferences 那个 Visibility 开关配合才会显示）。

这些入口彼此互相依赖：例如想看 pipeline asset 上的"高级属性"，得先在 Preferences 里把 Visibility 打开；想让 pipeline asset 生效，又要通过 Project Settings → Quality 绑定。对刚上手 URP 的人是一个常见的**配置发现问题**——不是设置不存在，是藏得深。

## Sources

- [[sources/cmwdexint-urp-settings-locations]]
