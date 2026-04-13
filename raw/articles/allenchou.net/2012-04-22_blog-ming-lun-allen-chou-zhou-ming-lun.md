---
title: Blog | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/blog/
author: Allen Chou
published: '2012-04-22'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

Source files and future updates are available on [Patreon](https://www.patreon.com/TheAllenChou).

You can follow me on [Twitter](https://twitter.com/TheAllenChou).

This post is part of my [Game Programming Series](http://allenchou.net/game-programming-series/).

## Prerequisite

## Introduction

In the previous tutorial, I used exposure avoidance as an example to demonstrate how to optimize computation with delayed result gathering. The basic idea is: kick jobs to run on worker threads and gather the results later. This prevents the main thread from being stalled.

If the game can afford one-frame latency, then we can kick the job in one frame and gather the results in the next frame. If the game cannot afford such latency, it’s still worth trying kicking the job early and gather the results later in the same frame.

What if the job takes too long to fit in a single frame? Or what if the job is just taking longer than we’d like? Then we can split the work across multiple frames. This is the core idea of time slicing, another optimization technique I picked up at work and one of my longtime favorites.

If you think about it, time slicing is everywhere. Texture streaming, seamless loading, etc., work that happens “in the background” without tanking a game’s frame rate. Can’t do it all in one frame? Then do it across multiple! It’s a simple but very effective idea.

[Continue reading](https://allenchou.net/2021/05/time-slicing/#more-6821)