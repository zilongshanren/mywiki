---
title: Creating a 3D Game Engine (Part 9)
url: https://cybereality.com/creating-a-3d-game-engine-part-9/
author: Cybereality
published: '2014-04-28'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

Today I have finally gotten a simple sort of animation working. It looks easy, but I made my life a lot harder by implementing by own math library. So far I have a Vector3D and a Matrix4x4 class almost finished. Well the Vector class is pretty much done. The Matrix class still needs some fleshing out, but I got it working well enough to spin a triangle. I realize I could have used the D3DX library (which is deprecated), or XNAMath (also deprecated), or DirectXMath (safe for now), but I thought making my own math functions would be a good learning experience. I did also have to reimplement D3DXMatrixLookAtLH and D3DXMatrixPerspectiveFovLH, but Microsoft is nice enough to list the equations in their documentation (thanks!).

In addition, I got a lot of help from this book, [3D Math Primer for Graphics and Game Development](https://www.amazon.com/Math-Primer-Graphics-Game-Development-ebook/dp/B008KZU548), which may be one of the best I’ve seen for 3D math. While there are other books, this text has very clear explanations, equations, and actual C++ implementations. I did try my best not to “cheat” and just copy the code, and instead based it on the equations listed. Unfortunately, I got cocky and wrote the length function without checking the reference, and left out the square root function call by accident (resulting in about a hour of debugging). Eventually I figured it out, but not after checking pretty much everything else with a fine-toothed comb. No worries, it’s working now.

Feels nice to see some movement on the screen. For this week I’d like to get a textured cube spinning. Also, I realized that DirectX 11 doesn’t come with a way to import models out-of-box. So pretty soon I will probably have to write a model importer (I’m looking at COLLADA now). Sometimes I wonder if all this work is really worth it, especially with Unreal Engine 4 at $19/month at the moment. I guess I do realize I can likely never hope to compete with the big commercial engines, but I still think this is a great exercise of the mind. We’ll see how long I can keep my faith.