---
title: 'Degine: 60FPS on $99 Kindle Fire'
url: https://cybereality.com/degine-60fps-on-99-kindle-fire/
author: Cybereality
published: '2023-07-01'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

I spent the last two days adding GPU compressed texture support to Degine, my custom OpenGL / WebGL 3D engine. I tried a few formats, but ended up going with ASTC, since it was the only one that appears to be supported on both desktop and web. While it’s not a massive difference, it was enough to get the Amazon Kindle Fire HD 8 running smooth at 60FPS (it was borderline previously). This means I can now run the FSR render scale at 70% (rather than 50%) and still have FXAA anti-aliasing and shadows enabled. Using ASTC compression slightly increases the file size, and does have a small loss in quality, but honestly it would be hard to tell the difference. The video above shows my benchmark scene, with 200K polygons and about 30 draw calls. Realistically, a game would likely need at least 100 – 200 draw calls with batching, but I need to create some of my own mobile-optimized assets, as 200K polys seems to be pushing it. And this is the absolute minimum target, a $99 tablet. For example, on the higher-end Samsung Tab S8+ I can run at native resolution (above 1440P) at 120FPS.

That said, there is still a lot left on the renderer. Currently I am only lighting with a single directional light and shadow. Since this is targeting mobile, I’m going to stick with only one real-time shadow. But I do need to figure out how I’m going to handle multiple lights. Did some research today on deferred rendering, which looks promising, but the increased bandwidth may cripple cheap tablets. So probably tomorrow I will look for a simple solution, for example supporting a fixed number of lights per mesh (e.g. 8). For export, everything is going to be baked anyway, but you need to be able to preview the lighting in the editor while creating the scene. I think this will be a good thing to test next. After that I will start creating the editor UI and develop a level file format, as right now it’s all hard-coded in C++. But progress is happening fast.