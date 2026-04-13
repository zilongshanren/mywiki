---
title: Light and Collision Component API | PlayCanvas Blog
url: https://blog.playcanvas.com/light-and-collision-component-api
author: Dave Evans
published: '2013-10-31'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

Light and Collision components have been consolidated from 7 components to 2!

Today we deployed the second of two changes to our Component System designed to make dealing with Collision and Lighting much simpler. We've combined the 4 collision Components (*collisionbox*, *collisionsphere*, *collisioncapsule*, and *collisionmesh*) into a single *collision* Component. And we've combined 3 light Components (*directionlight*, *pointlight*, *spotlight*) into a single *light* Component. Both Components now have a *type* attribute which you can use to switch between the different behaviors.

Why make this breaking change, I hear you ask? These changes drastically simplify the API when you are coding. So now code like this:

`this.entity.light.enable = false;`

this.entity.collision.on("collisionstart", this.onCollision);



It will work with every type of light or collision shape you are using.

We've automatically migrated all Packs in your Projects to the new Components, so in most cases you won't even notice the difference.

However, for some people - if you are using the old Components in scripts - this will break your existing projects. We don't do this lightly, even though we are pre-1.0. However, fixing your projects should be straightforward. In most cases just changing the old Component to the new one in your code will fix it. You might also need to add the *type* property to set which Component type you want.