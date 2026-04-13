---
title: Making tooltips appear in the echo area
url: https://www.masteringemacs.org/article/making-tooltips-appear-in-echo-area
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

By default Emacs will display its tooltips in a separate frame. If you want to force Emacs to use the echo area exclusively, you can do that with this handy code snippet:

```
(tooltip-mode -1)
(setq tooltip-use-echo-area t)
```


By default Emacs will display its tooltips in a separate frame. If you want to force Emacs to use the echo area exclusively, you can do that with this handy code snippet:

```
(tooltip-mode -1)
(setq tooltip-use-echo-area t)
```


Are you struggling with the
basics? Have you mastered movement and editing yet? When you
have read *Mastering Emacs* you will understand
Emacs.

Have you read my
[Reading Guide](https://www.masteringemacs.org/reading-guide)
yet? It's a curated guide to most of my articles, and I
guarantee you'll learn something whether you're a beginner
or an expert.
[And why not check out my book? ](https://www.masteringemacs.org/book)

I write infrequently, so go on — sign up and receive an e-mail when I write new articles