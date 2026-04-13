---
title: “Multiple” particle textures with 1 draw call
url: https://cmwdexint.com/2015/02/01/multiple-particle-textures-with-1-draw-call/
author: Ming Wai Chan
published: '2015-02-01'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

The idea came from [https://www.youtube.com/watch?v=vuLf6yE406c](https://www.youtube.com/watch?v=vuLf6yE406c) which was sent from my colleague that using the “texture sheet animation” can let unity particle system uses an atlas as texture. That means a particle system with different “textures” can use 1 material thus 1 draw call.


In my case, I want to increase the variety of the falling leaves. My texture atlas is like following and I defined the grid like this:


To let the emitter randomize which “leaf” to emit, I input the id range to “Texture Sheet Animation”:

The emitter now emits “different textures”! Now I don’t have to duplicate emitters to create the variety.



thats helpful

LikeLike

very helpful thanks !!

LikeLike