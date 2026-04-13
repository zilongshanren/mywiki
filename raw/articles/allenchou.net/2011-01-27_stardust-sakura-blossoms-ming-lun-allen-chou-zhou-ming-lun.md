---
title: Stardust Sakura Blossoms | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/01/stardust-sakura-blossoms/
author: Allen Chou
published: '2011-01-27'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

I’ve just created another sakura particle effect demo with [Stardust](https://allenchou.net/code.google.com/p/stardust-particle-engine/).

(Here’s the original official Stardust example: [Sakura](http://stardust-particle-engine.googlecode.com/svn/trunk/examples/3D/Stardust%203D/Sakura/Sakura.html))

Check out the source code on [WonderFL](http://wonderfl.net/c/ePOA)!

Click on the stage to create a base, and click the base again to plant a sakura tree.

Hi check the I’ve been working on, it uses away3DLite since I’ve been getting issues with away3D : http://bdesignet.com/projects/as3/magicEffect3D/index.htm Let me knwo what u think. Regards.

Nice one! The particle effect is pretty smooth 🙂

Thank you. to get it, I needed to use away3Dlite and reduce the number of particles, alto take care of the number of objects created. So far I see your animation so much better.

Hi, I’ve been testing your stardust tool, so far an awesome tool, now I wanted to test the 3d features after trying many APIs I’ve came into away3d and I found one problem, using this : tarInitializer1.addInitializer(new Away3DObject3DClass(Plane,[{material:new BitmapMaterial(item1), width:10, height:10}]));

The planes are created but the properties are not passed to the away3d API, the code works well on away3dlite so the problem looks to be the way stardust is passing teh parameters to away3D, any clue about how to fix this problem.

Thanks

Thanks for pointing out the issue. I’ll contact Paq about it. He’s the one in charge of the Away3D extension.

Cool thanks, the away3dlite works great so fast and the speed is really good.