---
title: GNU Make, Parallel Processing
url: https://www.4rknova.com/blog/2012/11/28/make
author: Nikolaos Papadopoulos
published: '2012-11-28'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

GNU make provides the ‘-j’ switch, which enables parallel processing. To automatically use this feature without having to type it each time you compile your programs you could add the following entry in your ~/.bashrc script.

```
alias make="make -j $(cat /proc/cpuinfo | grep processor | wc -l)"
```