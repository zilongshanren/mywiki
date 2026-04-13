---
title: Simple 2D soft bodies in Box2D
url: https://gamedevcoder.wordpress.com/2011/05/25/simple-2d-soft-bodies-with-box2d/
published: '2011-05-25'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

[Box2D](http://www.box2d.org/) is an excellent, widely used and completely free 2D physics engine. It has support for variety of 2D shapes and joints but there’s no out of the box support for soft bodies and so if you want one you have to do it yourself.

I’ve made an experiment and implemented simple round soft bodies using a couple of circles linked using distance joints, then thought why not to share it. Here’s how you use the code:


b2ExSoftCircleBodyDef def;

def.numParts = 10; // Number of linked internal circles

def.radius = 10.0f;

def.center = b2Vec2(0.0f, 15.0f);

def.softness = 0.5f; // Softness within 0..1 range

b2ExSoftCircleBody* body = b2ExSoftCircleBody_Create(world, &def);


And this is the result:


Get the demo and source code from [GitHub](https://github.com/macieks/soft_circle_body_box2d) and use it freely 🙂