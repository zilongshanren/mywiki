---
tags: [source, 数据格式, parquet, csv, json, 工程实践]
date: 2026-04-14
sources: 1
---

# Data formats: Why CSV and JSON aren't the best（Anteru / anteru.net）

[[matthaeus-chajdas]]（Anteru）发表于 2024 年 12 月的一篇工程反思博客，主题是：为什么 CSV 和 JSON 都不是存储表格型测量数据的好选择，以及 [[parquet-vs-csv-json|Parquet]] 为什么是更合理的默认。作者在文中承认自己早年也曾在 MongoDB 里以 JSON 形式存实验结果，这篇博客是他对那一段历史的公开更正。

## 摘要

作者从三项需求出发讨论表格数据的存储格式：**结构化**、**可版本化**、**易查看**。他认为"易查看"在实践中的权重往往高于性能与体积。在三个常见方案里，电子表格类型脆弱且批处理笨重但至少能被人直接打开；CSV 没有字符串转义与类型标准、无法原生存版本，在归档场景下几乎不可信；JSON 受限于 double 精度，无法可靠地表达 64 位整数或日期，且"每行一个对象重复列名"的写法会造成 10–100 倍膨胀。Protocol Buffers 偏向 RPC、HDF5 过于灵活而小众，都不合适。作者的结论是 Apache Parquet——列式、强类型、支持 Zstd 压缩、能承载版本元数据、有 Pandas / DuckDB / Iceberg 等整条生态，并且可以廉价地派生出 CSV 或电子表格来安抚便利派。

## 关键要点

- **需求优先级**：易查看 > 版本化 > 性能 / 体积。版本号必须**内嵌在数据里**，光靠时间戳或文件名无法保证多年后可追溯。
- **CSV 的核心问题不在"简单"，在"方言"**：作者声称自己为 CSV 的各种变体写过十多个不同的 parser。没有转义标准、没有类型标准、没法存版本，归档 CSV 基本属于"薛定谔的数据"。
- **JSON 的核心缺陷是类型系统**：数字全是 double，53 位以上整数失真；没有标准日期格式；行对象里重复列名带来 10–100× 膨胀，压缩虽能缓解磁盘占用，却救不了解析开销。
- **二进制 JSON 家族（BSON / CBOR / UBJSON / MessagePack）没有事实标准**，跨语言/跨库支持割裂，不解决问题只转移问题。
- **Parquet 的优势是"嵌在正确的生态位"**：1:1 替代 CSV/电子表格，列式 + 强类型 + Zstd 压缩 + 元数据，Pandas 原生读写，VS Code Data Wrangler 等开源 viewer，DuckDB / Iceberg 作为查询与表格层。
- **推荐的工程模式**：把 Parquet 作为**主存储**（primary storage），CSV / xlsx 作为按需派生的**衍生格式**（derivative），这样既尊重便利性，也不让便利性侵蚀数据完整性。
- **归档视角**：Parquet 文档完整、生态开源，即使若干年后需要迁移，也能轻易转出；而 CSV / JSON 的"易迁移"只是错觉——类型和版本信息早就丢失了。

## 链接到的概念

- [[parquet-vs-csv-json]]
- [[matthaeus-chajdas]]
- [[gpgpu-json-parsing]]

## 原文

- 链接：https://anteru.net/blog/2024/data-formats-why-csv-and-json-aren-t-the-best
- 本地：`raw/articles/anteru.net/2024-12-29_data-formats-why-csv-and-json-aren-t-the-best.md`
