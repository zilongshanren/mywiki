---
title: runevision blog
url: https://blog.runevision.com/2025/01/
published: '2025-01-10'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

For my game [The Big Forest](https://runevision.com/multimedia/thebigforest/) I want to have creatures that are both procedurally generated and animated, which, as expected, is quite a research challenge.

As mentioned in my [2024 retrospective](https://blog.runevision.com/2025/01/2024-retrospective.html), I spent the last six months of 2024 working on this – three months on procedural model generation and three months on procedural animation. My work on the creatures actually started earlier though. According to my commit history, I started in 2021 after shipping [Eye of the Temple](https://runevision.com/multimedia/eyeofthetemple/) for PCVR, though my work on it prior to 2024 was sporadic.

Though the creatures are still very far from where they need to be, I'll write a bit here about my progress so far.

### The goal

I need lots of forest creatures for the gameplay of *The Big Forest*, some of which will revolve around identifying specific creatures to use for various unique purposes. I [prototyped the gameplay](https://blog.runevision.com/2024/10/procedural-game-progression-dependency.html) using simple sprites for creatures, but the final game requires creatures that are fully 3D and fit well within the game's [forest terrain](https://www.youtube.com/watch?v=VxMwggFQRQM).

![creatures from prototype → replace with 3D procedural creatures → put into procedural terrain](../../assets/59e611f419db45ec.jpg)


![creatures from prototype → replace with 3D procedural creatures → put into procedural terrain](../../assets/59e611f419db45ec.jpg)


Another year went by as an indie game developer and what do I have to show for it?

In [last year's retrospective](https://blog.runevision.com/2024/01/2023-retrospective-and-goals-for-new.html) I wrote that apart from working on my game The Big Forest in general, I had four concrete goals for 2024:

- Present my Fractal Dithering technique
- Release my Layer-Based ProcGen for Infinite Worlds framework as open source
- Wrap up and release The Cluster as a free experimental game
- Make better use of my YouTube channel

I ended up doing only two of those, but it was the two most important ones to me, so I'm feeling all right with that.

### Release of LayerProcGen as open source

I released my [LayerProcGen framework](https://runevision.com/tech/layerprocgen/) as open source in May 2024. LayerProcGen is a framework that can be used to implement layer-based procedural generation that's infinite, deterministic and contextual.

![](../../assets/b482d4f21927bfab.jpg)

I wrote [extensive documentation](https://runevision.github.io/LayerProcGen/) describing not only the specifics of how to use it, but also the overarching ideas and principles it's based on. I also did [a talk at Everything Procedural Conference](https://www.youtube.com/watch?v=4oJGkx0K8UQ) about it, which was well received.