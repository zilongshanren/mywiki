---
title: 'HTML5 games: 3D collision detection – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/10/html-5-games-3d-collision-detection/
author: Belén Albeza
published: '2015-10-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last week we took a look at [Tilemaps](https://hacks.mozilla.org/2015/10/html-5-games-tilemaps/), and I shared some new articles that I’d written on MDN. This week I’m back to introduce **3D collision detection**, an essential technique for almost any kind of 3D game. I’ll also point you to some more new articles about [game development](https://developer.mozilla.org/en/docs/Games) on MDN! Hope they inspire you to stretch your skills.

In 3D game development, **bounding volumes** provide one of the most widely used techniques for determining whether two virtual objects will collide (i.e., intersect with each other) during game play. The technique of bounding volumes consists of wrapping game objects with some virtual volumes, and applying intersection algorithms to describe the movement and interaction of these volumes. You can think of this approach as a shortcut: it is easier and faster than detecting intersections between arbitrary, complex shapes.

In terms of bounding volumes, the use of **axis-aligned bounding boxes** (AABB) is a popular option. Depending on the game, sometimes spheres are used as well. Here’s an image of some 3D objects wrapped with AABB:

![Screen Shot 2015-10-16 at 15.11.21](../../assets/34fa6bea9a1e2072.png)


The new MDN article on [3D collision detection](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_collision_detection) describes how to use generic algorithms to perform 3D collision detection with AABB and spheres. This article should be useful regardless of the game engine or programming language you are using to develop your game.

We also published an article about doing [collision detection with bounding volumes using three.js](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_collision_detection/Bounding_volume_collision_detection_with_THREE.js), a popular 3D library for JavaScript. (Learn more about [three.js](http://threejs.org/).)

Check out the [live demos](http://mozdevs.github.io/gamedev-js-3d-aabb/) and peek at [their source code](https://github.com/mozdevs/gamedev-js-3d-aabb). One of the demos uses a [physics engine](https://en.wikipedia.org/wiki/Physics_engine) (in this case, [Cannon.js](http://www.cannonjs.org/)) to perform collision detection. Embedded below you can find another demo that shows how to use Three.js to detect collisions:

Hope you enjoy the demos and find them useful. If there’s a particular topic in HTML5 game development you’d like to learn more about, please drop a comment here and let us know! We’ll try to get it covered for you.

## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.

## 2 comments

JesseOctober 30th, 2015 at 11:15svfx animation stuidoOctober 31st, 2015 at 11:15