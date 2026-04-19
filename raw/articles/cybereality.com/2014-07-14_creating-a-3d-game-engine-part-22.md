---
title: Creating a 3D Game Engine (Part 22)
url: https://cybereality.com/creating-a-3d-game-engine-part-22/
author: Cybereality
published: '2014-07-14'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

After struggling for a bit with the shadow mapping implementation, I finally have something presentable. I followed [a tutorial from Microsoft](http://msdn.microsoft.com/en-us/library/windows/apps/dn263152.aspx) and thought I understood what was happening. However, it required a lot of changes in the rendering code and it took a little while to get things working. Even once it was somewhat functional, I still had some issues with what they call shadow acne. It seemed really bad on the self-shadowing side of objects. I tried tweaking all the values I could (i.e. the bias in the shader), but I was not able to get it to look right. Finally I just set it so that there wouldn’t be self-shadowing of a single polygon. This happens to look fine, since the lighting equations make the polygon shaded anyhow. I’m not sure if this will work for every single instance, but with the simple models I’m testing with it’s fine.

I’m at the point where I really want to get the physics engine up and running. Still have some more research to do, so I bet it will take some time before I have something more to show. But it’s coming along.