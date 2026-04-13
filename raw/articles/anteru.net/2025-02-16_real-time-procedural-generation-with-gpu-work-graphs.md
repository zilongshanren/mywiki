---
title: Real-Time Procedural Generation with GPU Work Graphs
url: https://anteru.net/research/real-time-procedural-generation-with-gpu-work-graphs
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

We present a system for real-time procedural generation that makes use of the novel GPU programming model,
work graphs. The nodes of a work graph are shaders, which dynamically generate new workloads for connected
nodes. This greatly simplifies the implementation of recursive procedural algorithms on GPU s. Combined with
GPU ray tracing and procedural mesh shaders, our system makes use of this graph structure to tackle various
common problems of procedural generation. Our system is very easy to implement, requiring no additional
data structures from what would already be available in a modern rendering engine. We demonstrate the
real-time editing capabilities on representative examples. We augment the scene in the teaser image with
79,710 instances in 3.74 ms on an AMD Radeon RX 7900 XTX.