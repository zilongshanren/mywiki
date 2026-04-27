---
tags: [source, llm, 程序化生成, 游戏ai, constrained-generation]
date: 2026-04-27
sources: 1
---

# Constrained Text Generation with AI（Boris The Brave）

[[boris-the-brave]] 发表于 2023 年 2 月的文章，探讨如何用受约束的束搜索（constrained beam search）让大语言模型只从预先审核过的句子集合中选择输出，从而在游戏场景中安全使用 LLM 生成对话。

## 摘要

文章从一个游戏设计痛点出发：LLM 在运行时生成文本的最大障碍是无法充分控制输出——模型可能脱离角色、输出有害内容。Boris 提出的方案受 Gene Wolfe 小说中「Ascian 语言」的启发：限制模型只能从一组预先批准的短语中选择，但仍然利用模型的语言理解能力来决定**选哪一句**最合适。

技术上，这是「引导文本生成（guided text generation）」的简化版，借助 HuggingFace Transformers 的 `prefix_allowed_tokens_fn` 在 token 树探索过程中动态过滤候选 token，使生成路径只经过预批准句子的前缀。实验以 GPT-2 为模型：不受约束时几乎无法回答问题；加入固定短语集合后，模型能按语义选出最合理的回答（如「How many quarts in a gallon?」会优先选到 `13`）。

文章进一步讨论扩展方向：可将固定句子集替换为任意树过滤器（如 Tracery 语法），也可约束输出符合固定 JSON schema，防止 LLM 在结构化输出任务中偏离格式。作者坦承该技术适用范围有限，但认为在对话机器人、游戏 NPC 对话等场景有实用价值。

## 关键要点

- LLM 文本生成本质是对 token 树的搜索；约束生成就是在搜索过程中裁剪不合法的分支。
- `prefix_allowed_tokens_fn`（HuggingFace）允许在每步生成时动态屏蔽 token，从而将输出锁定在预批准短语集合内。
- 固定短语集可替换为任意语法（如 Tracery），使 LLM 充当语法扩展的「智能选择器」而非开放生成器。
- 强制 JSON schema 输出是同一思路的实用变体，解决 LLM 结构化输出不稳定的问题。
- 该技术不能提升事实准确性，只能限制输出形式。

## 链接到的概念

- [[game-development/constrained-beam-search-llm]]

## 原文

- 链接：https://www.boristhebrave.com/2023/02/11/constrained-text-generation-with-ai/
- 本地：`raw/articles/boristhebrave.com/2023-02-11_constrained-text-generation-with-ai.md`
