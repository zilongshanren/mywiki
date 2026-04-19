---
tags: [source, mysql, 字符编码, 数据迁移, 运维]
date: 2026-04-19
sources: 1
---

# 有惊无险的一次网站系统升级（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2025 年 9 月的一篇运维复盘，讲他把运行了十多年的博客服务器做操作系统升级时，踩到的 MySQL 4 → MySQL 8 跨越式升级导致的 GBK → UTF-8 迁移问题。

## 摘要

事情起于一次"脑抽"的系统升级，一升就捅了整条老栈：PHP 从 5 强升到 7，作者 2004 年写的留言板程序垮掉，Apache 配置语法变了，但最棘手的是 MySQL 从 4 一路升到 8——老库里以 GBK 存的字节被统一标成了 latin1，读出来全是乱码。官方给出的"先转 binary 列再转目标字符集"方案对有索引的字段不工作，作者于是把数据库 dump 下来做本地迁移。关键步骤：**`mysqldump` 必须加 `--default-character-set=binary`**，不然出口就把字节按 latin1 错转一次；原以为 `iconv` 一把梭就完事，结果发现 dump 里既有 GBK 又有 UTF-8（约 680 条，推测是当年试过一次改编码的残留），`iconv` 对这种混杂编码束手无策；而且 MySQL 的引号转义一旦被编码转换吃掉字节就会破坏 SQL 合法性。最后作者写了个 Lua 小程序对 dump 做最低限度的词法解析，只挑 binary 字符串字面量，用启发式判断 GBK/UTF-8 分流处理，再重新转义。最终把 latin1 声明 `sed` 替换为 utf8mb4 即可导回。

## 关键要点

- 老 MySQL 不存储字段字符集，升级后默认被当 latin1
- 跨编码迁移第一步：`mysqldump --default-character-set=binary` 保原字节
- 官方"binary 列 → 目标列"方案对有索引字段不工作，要先 drop 索引
- `iconv` 无法处理混杂编码的 dump，必须分桶判断后再局部转码
- SQL 转义需要最低限度的词法解析，不能纯文本替换
- 经验：老数据里藏着早已忘掉的编码残渣，事先不要假设数据一致性

## 链接到的概念

- [[mysql-charset-migration]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2025/09/
- 本地：`raw/articles/blog.codingnow.com/2025-09-16_yun-feng-de-blog.md`
