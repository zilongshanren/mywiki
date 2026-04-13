---
title: 'Download the first AnKi demo: Hundreds of lights'
url: https://anki3d.org/download-the-first-anki-demo-hundreds-of-lights/
author: Panagiotis Christopoulos Charitos
published: '2013-05-12'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

After some years of development I am happy to present the **first AnKi 3D engine demo**. The demo is in **alpha** state and it’s very rough around the edges so please bare with me and report any problems found [in the project’s google code page](http://code.google.com/p/anki-3d-engine/issues) or use the emails in the contact page. Also note that at the moment it only runs and compiles in Linux.

**And here is download link:** [https://anki-3d-engine.googlecode.com/files/anki_hundreds_lights_demo.tar.gz](https://anki-3d-engine.googlecode.com/files/anki_hundreds_lights_demo.tar.gz)

To run the demo navigate to the directory that contains the **demo64** binary and run that binary. The source is also included in case you want to build everything yourselves. Read the txt files in the directory for more info.

Some points on the tech behind the demo:

- Its been using using the new tile based deferred renderer.
- You can visualize more than 100 lights at the same time.
- You can see al the the shadows of the spot lights.
- It features post processing effects like HDR, SSAO, color correction, sharpen filter and other.
- Taking advantage of multi-core CPUs.

What you will need to run the demo:

- A Linux powered box. Ubuntu 12.04 and beyond it’s supposed to work.
- The Linux box should be 64bit.
- A modern GPU and driver that supports OpenGL 3.3 core profile. nVidia with proprietary drivers is supposed to work.

Controls:

*ESC*will quit the demo.*wasd*moves the camera forward/back and left/right.*z*moves the camera up.*space*moves it down.*q*and*e*roll the camera.*F1*will show the debug meshes.

Credits:

- The building is “sponza” by Crytek.
- The horse model is from Endre Barath (http://etyekfilm.hu).

Any feedback is appreciated. Enjoy!