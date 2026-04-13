---
title: 'Smart Scan: Jump between symbols in a buffer'
url: https://www.masteringemacs.org/article/smart-scan-jump-symbols-buffer
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

A few years ago I wrote Effective Editing I: Movement and in that article I included a bunch of code for a feature I called “Smart Scan.” Back then I didn’t bother putting it on Github so I just left it as source code embedded in the article. I’ve now realized that hundreds have stuck it in their .emacs file but without the benefit of any potential updates, and with no way to actually contribute to the package.

Basically, Smart Scan let’s you jump between symbols in your current buffer that matches the one point is on. It does it unintrusively and without any prompts or other fancy UI gimmicks. Simply put your point on a symbol you want to search for in your buffer and type either `M-n`

or `M-p`

to move forward or backward respectively. Give it a shot. I have [moved it Github here](https://github.com/mickeynp/smart-scan). Patches welcome :) Enjoy!