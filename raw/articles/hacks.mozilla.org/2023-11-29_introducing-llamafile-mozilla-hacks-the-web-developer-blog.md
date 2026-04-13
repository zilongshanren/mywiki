---
title: Introducing llamafile – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2023/11/introducing-llamafile/
author: Stephen Hood
published: '2023-11-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*A special thanks to Justine Tunney of the Mozilla Internet Ecosystem (MIECO), who co-authored this blog post.*

Today we’re announcing the first release of [llamafile](https://github.com/Mozilla-Ocho/llamafile) and inviting the open source community to participate in this new project.

llamafile lets you turn large language model (LLM) weights into executables.

Say you have a set of LLM weights in the form of a 4GB file (in the commonly-used GGUF format). With llamafile you can transform that 4GB file into a binary that runs on six OSes without needing to be installed.

This makes it dramatically easier to distribute and run LLMs. It also means that as models and their weights formats continue to evolve over time, llamafile gives you a way to ensure that a given set of weights will remain usable and perform consistently and reproducibly, forever.

We achieved all this by combining two projects that we love:[ llama.cpp](https://github.com/ggerganov/llama.cpp) (a leading open source LLM chatbot framework) with[ Cosmopolitan Libc](https://github.com/jart/cosmopolitan) (an open source project that enables C programs to be compiled and run on a large number of platforms and architectures). It also required solving several interesting and juicy problems along the way, such as adding GPU and dlopen() support to Cosmopolitan; you can read more about it in [the project’s README](https://github.com/Mozilla-Ocho/llamafile#readme).

This first release of llamafile is a product of Mozilla’s innovation group and developed by [Justine Tunney](https://justine.lol), the creator of Cosmopolitan. Justine has recently been collaborating with Mozilla via [MIECO](https://future.mozilla.org/mieco/), and through that program Mozilla funded her work on the [3.0 release](https://justine.lol/cosmo3/) ([Hacker News discussion](https://news.ycombinator.com/item?id=38101613)) of Cosmopolitan. With llamafile, Justine is excited to be contributing more directly to Mozilla projects, and we’re happy to have her involved.

llamafile is licensed Apache 2.0, and we encourage contributions. Our changes to llama.cpp itself are licensed MIT (the same license used by llama.cpp itself) so as to facilitate any potential future upstreaming. We’re all big fans of llama.cpp around here; llamafile wouldn’t have been possible without it and Cosmopolitan.

We hope llamafile is useful to you and look [forward to your feedback](https://github.com/Mozilla-Ocho/llamafile).



## About
[
Stephen Hood ](https://stephenhood.com)

Stephen leads open source AI projects (including llamafile) in Mozilla Builders. He previously managed social bookmarking pioneer del.icio.us; co-founded Storium, Blockboard, and FairSpin; and worked on Yahoo Search and BEA WebLogic.