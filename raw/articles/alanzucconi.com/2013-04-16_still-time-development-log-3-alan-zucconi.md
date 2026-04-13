---
title: '“Still time” – Development log #3 - Alan Zucconi'
url: https://www.alanzucconi.com/2013/04/16/still-time-development-log-3/
author: Alan Zucconi
published: '2013-04-16'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Despite the fact that the style of “Still Time” is absolutely minimalistic, a huge effort has been put into its visual effects. In this post I will show how some frames are post-processed.

**[Step 1: dark overlay]**A dark mask is superimposed to the original image. To speed up the process, there are four separate images for each edge (top, bottom, left, right). The central part of the frame is multiplied with a grey Perlin noise mask. This will result in a nice vintage effect.**[Step 2: screen curvature]**To better simulate the style of an old CRT monitor, the frame is curved. This effect is achieved with a displacement mask that is generated directly in the game. This allows a more fine control over the amount of curvature and enables smooth animations and transitions.**[Step 3: RGB lines]**Monitors use a grid of red, green and blue lights to produce an image. In some cheap CRT models, this grid can be perceived looking closely to the image. To simulate this effect, thick RGB lines are drawn on top of the image.

|
|
|
|
|
|

In the next development blog about “Still Time” I will show how in-game frames are actually processed.

## Leave a Reply Cancel reply