---
title: Thea Render jumps on the GPU bandwagon
url: http://raytracey.blogspot.com/2010/05/thea-render-jumps-on-gpu-bandwagon.html
author: Sam Lapere
published: '2010-05-01'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://www.thearender.com/downloads/TheaRenderRoadmap.pdf](http://www.thearender.com/downloads/TheaRenderRoadmap.pdf).

A list of released and announced GPU renderers:

1. V-Ray GPU (Chaos Group)

2. iray (mental images)

3. SmallLuxGPU (LuxRender)

4. Octane Render (Refractive Software)

5. Arion Render (Random Control/FryRender)

6. Thea Render

7. SHOT using iray (Bunkspeed)

8. RTT Powerhouse and RTT DeltaGen using iray (Realtime Technology)

UPDATE:

9. Indigo Render also announced plans for GPU acceleration

UPDATE 2 (Sep 29):

10. finalRender (cebas Visual Technology)

[http://www.cebas.com/?pid=hot_news&nid=378](http://www.cebas.com/?pid=hot_news&nid=378)

11. Artisan using OptiX (LightWorks)

[http://architosh.com/2010/07/sig-lightworks-unveils-power-of-optix/](http://architosh.com/2010/07/sig-lightworks-unveils-power-of-optix/)

12. Zeany using OptiX (Works Zebra)

I bet Maxwell and Modo will quickly follow.

## 6 comments:

another one VRED by PI-VR

I just checked their page, it's realtime but it's not a GPU renderer or accelerated by GPU. The direct nurbs raytracing sounds interesting though.

running on the GPU does not automagically make a fantastic tool ... there are more than enough scenarios where memory on gfx cards are very limiting factors ... if your scene exceeds gfx memory most of the mentioned renderers simply do nothing :)

Yes, memory is a limitation, but if you check Octane render gallery, there is a lot you can do with the current GPU memory.

Thanks for adding Indigo Renderer to your list :)



We use a hybrid approach that does not require as much memory as pure GPU renderers, we only store what's needed for the GPU-accelerated portion of the workload. Furthermore, through the use of instancing you can make a little GPU memory go a long way!

A GeForce GTX 400 series card makes a powerful ally for an i7, often doubling and sometimes even tripling rendering speed, while still supporting Indigo's full feature set (including SSS, complex materials, full motion blur etc.)

@lycium, no problem!

Post a Comment