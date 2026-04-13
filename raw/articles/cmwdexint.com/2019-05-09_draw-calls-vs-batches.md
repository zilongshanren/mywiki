---
title: Draw calls VS batches
url: https://cmwdexint.com/2019/05/09/draw-calls-batches/
author: Ming Wai Chan
published: '2019-05-09'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

For example** static batching**:

groups objects to **1 big batch** -> this 1 big batch contains **many fast and cheap draw calls**

expensive draw calls = many changes between draw calls

Unity profiler shows no. of batches

Render doc shows no. of draw calls