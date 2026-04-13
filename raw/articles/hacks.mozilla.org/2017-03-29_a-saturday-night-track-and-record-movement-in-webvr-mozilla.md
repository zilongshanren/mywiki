---
title: 'A Saturday Night: Track and record movement in WebVR – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2017/03/a-saturday-night-track-and-record-movement-in-webvr/
author: Belén Albeza
published: '2017-03-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Mozilla’s [WebVR team](https://mozvr.com/) has released a fun new **virtual reality demo** called [ A Saturday Night](https://aframe.io/a-saturday-night). Put your VR headset on, perform a dance, and share it with the world!

*
A Saturday Night* has been developed with

[A-Frame](https://aframe.io/), an open source JavaScript framework created at Mozilla that makes building VR experiences much more accessible. If you have some knowledge of HTML you can create basic scenes with animations, and the A-Frame API allows you to use JavaScript to provide richer interactive experiences. There is also a

[registry of components](https://aframe.io/aframe-registry/), so you can easily include community-contributed code in your own projects.

Not only you can dance along with the demo, we also encourage you to peek at [ A Saturday Night source code](https://github.com/aframevr/a-saturday-night) on Github. The most interesting part is that it shows how to track the user’s movement and position (both headset and controllers). And, you can easily reuse that code in your own A-Frame projects too!

The tracking code has been released as a **standalone A-Frame component**, which you can grab [from this Github repository](https://github.com/dmarcos/aframe-motion-capture) or via NPM:

```
npm install aframe-motion-capture
```


There are a few controllers in that repository. The highest-level controllers, `avatar-recorder`

and `avatar-replayer`

, allow you to record and replay the avatar’s movement (head and hands). This is very useful for QA or automated tests –where recording and replaying what a user has done has tremendous value. There’s also the possibility of exploring new use cases: game mechanics or other types of interactive activity that could benefit such as controlling character movement, casting spells by gesturing with your hands, etc.

If you want to learn more about *A Saturday Night*, or the reusable tracking components, [take a look at the A-Frame blog post](https://blog.mozvr.com/p/a37c7bb7-f03e-4a9b-90cc-3eaf2e05f61a/), where [Diego Marcos](https://twitter.com/dmarcos) from Mozilla’s WebVR team shares more technical detail.

## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.