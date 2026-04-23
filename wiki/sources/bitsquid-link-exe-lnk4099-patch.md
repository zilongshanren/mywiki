---
tags: [source, bitsquid, 工具链, msvc, 构建系统]
date: 2026-04-19
sources: 1
---

# Code Share: Patch link.exe to Ignore LNK4099（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 12 月的工具帖：MSVC 的 `link.exe` 把 LNK4099（"找不到第三方库的 PDB"）钉在一份"不可 ignore 的 warning 列表"里，引入的第三方静态库只要不带 PDB 就会产生成百上千条这种链接警告。Frykholm 直接给出解法——二进制 patch `link.exe` 把 4099 从那份列表里换掉。

## 摘要

问题本质是 MSVC 有一份硬编码的 warning 白名单不允许用户 `/ignore`，LNK4099 恰好在里面。作者参考 bottledlight.com 的一份 reverse engineering 笔记，写了一段 Ruby 脚本自动化整个流程：扫 `VS90COMNTOOLS` / `VS100COMNTOOLS` / `XEDK`（Xbox 360 SDK）环境变量找到所有 link.exe，在二进制里搜字节序列 `[4088, 4099, 4105].pack("III")`，替换成 `[4088, 65535, 4105].pack("III")`（65535 是空 warning 号的哨兵），先备份再写回。作者强调"重复三次以上的事就写脚本"这条哲学——附链接到他在 altdevblogaday 上的 *write-a-script-for-it*。脚本还处理了已 patch 过的情况、多个命中位置的异常、找不到位置的异常。

## 关键要点

- **MSVC 硬编码白名单**：LNK4099 不能用 `/ignore:4099` 绕掉，必须改二进制；
- **patch 模式**：搜连续三个 warning 号 `(4088, 4099, 4105)`，把中间一个换成哨兵 65535；
- **覆盖 VS2008/VS2010/Xbox 360 SDK** 三个 link.exe 位置；
- **幂等性**：先检测"已 patch"签名避免重复执行；
- **安全性**：patch 前按时间戳备份 `link.exe-YYMMDD-HHMMSS.bak`；
- **write-a-script-for-it** 是工程生活哲学——把一次性 hack 升格成可复用工具。

## 链接到的概念

- [[link-exe-lnk4099-patch]]
- [[tools-first-iteration-loop]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/12/code-share-patch-linkexe-to-ignore.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-12-28_code-share-patch-link-exe-to-ignore-lnk4099.md`
