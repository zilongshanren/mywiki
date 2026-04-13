---
title: A Virtual Frame Buffer Abstraction for Parallel Rendering of Large Tiled Display
  Walls
url: https://www.willusher.io/publications/ospdisplaywall/
published: '2020-01-01'
source_blog: Will Usher's Blog
source_site: https://www.willusher.io/
category: game programming
fetched: '2026-04-13'
---

# A Virtual Frame Buffer Abstraction for Parallel Rendering of Large Tiled Display Walls

#### Mengjiao Han, Ingo Wald, Will Usher, Nate Morrical, Aaron Knoll, Valerio Pascucci and Chris R. Johnson

In *IEEE VIS Short Papers*, 2020.

![](https://cdn.willusher.io/img/e4HJywq.webp)

**Fig. 1:**

*Left: The Disney Moana Island rendered remotely with OSPRay’s path tracer at full detail using 128 Skylake Xeon (SKX) nodes on Stampede2 and streamed to the 132Mpixel POWERwall display wall, averages 0.2-1.2 FPS. Right: The Boeing 777 model, consisting of 349M triangles, rendered remotely with OSPRay’s scivis renderer using 64 Intel Xeon Phi Knight’s Landing nodes on Stampede2 and streamed to the POWERwall, averages 6-7 FPS.*

## Abstract

We present dw2, a flexible and easy-to-use software infrastructure for interactive rendering of large tiled display walls. Our library represents the tiled display wall as a single virtual screen through a display ‘service’, which renderers connect to and send image tiles to be displayed, either from an on-site or remote cluster. The display service can be easily configured to support a range of typical network and display hardware configurations; the client library provides a straightforward interface for easy integration into existing renderers. We evaluate the performance of our display wall service in different configurations using a CPU and GPU ray tracer, in both on-site and remote rendering scenarios using multiple display walls.

`@inproceedings{han_displaywall_2020, author={Han, Mengjiao and Wald, Ingo and Usher, Will and Morrical, Nate and Knoll, Aaron and Pascucci, Valerio and Johnson, Chris R.}, booktitle={IEEE VIS 2020 - Short Papers}, title={A {Virtual} {Frame} {Buffer} {Abstraction} for {Parallel} {Rendering} of {Large} {Tiled} {Display} {Walls}}, doi={10.1109/VIS47514.2020.00009}, year={2020} }`