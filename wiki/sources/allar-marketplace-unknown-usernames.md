---
tags: [source, unreal-engine, marketplace, web-debugging]
date: 2026-04-19
sources: 1
---

# Fixing UE4 Marketplace Comment Usernames Being Unknown（Michael Allar）

[[michael-allar]] 2018 年 4 月的小文，记录用 Fiddler 拦截改写 Epic UE4 Marketplace 前端 JS 的一次调试过程。一句话总结：**Epic 处理"已删除用户评论"的分支错写到了普通用户身上，把所有评论用户名覆盖成 "Unknown"**。

## 摘要

Allar 打开 UE4 Marketplace 发现自己资产页的评论用户全部显示 "Unknown"。他没有后端源码，就用 Fiddler 抓 `store.epic-store-frontend.js`（webpack + 压缩），搜字符串 `messages.com.epicgames.plugin.commentrating.comments.deleted_user` 定位到处理"已删除账号"的两段代码。Epic 新加"显示账号已删除"时把状态分支写反：正常账号的 `e.accountDisplayName` 也被赋成 "Unknown"。把这一行 `e.accountDisplayName = "Unknown"` 删掉、让 Fiddler 把本地改过的 JS 作为 auto-response 回给浏览器，用户名就恢复了。整个过程从定位到修复大约 2-3 分钟。

## 关键要点

- Fiddler 的 auto-response 是调试第三方前端（包括 Epic Launcher）时的利器：能把线上的压缩脚本换成本地改过的版本而不碰服务端。
- "处理异常分支"的补丁经常把正常路径也一起污染，是非常典型的 regression 模式。
- 这种 hack 只在本机生效，不修到 Epic 服务器上——Allar 把它当作"我有多少控制权"的思维练习。

## 链接到的概念

- [[michael-allar]]

## 原文

- 链接：https://allarsblog.com/2018/04/14/fixing-ue4-marketplace-comment-usernames-being-unknown/
- 本地：`raw/articles/allarsblog.com/2018-04-14_fixing-ue4-marketplace-comment-usernames-being-unknown.md`
