---
title: Supercharge your workflow with Template Assets! | PlayCanvas Blog
url: https://blog.playcanvas.com/supercharge-your-workflow-with-template-assets
author: Steven Yau
published: '2020-09-22'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

![](../../assets/7cea2caf40a6c1ed.jpg)


It’s finally here! The PlayCanvas team is very excited to announce the public release of our new Templates feature! 🎉

Templates allow you to create preconfigured entities with all the values and child hierarchy as an asset reference.

This is a huge workflow boost as managing and changing objects in a scene is now easier and faster to do. New instances of the Template can be placed in the scene with the Editor. These instances have a link to the Template asset, so any changes to the asset will change the instances in the scene too.

Now we are able to change and update many scene entities via a **single** asset which is a welcome change from the tedious manual updating of multiple entities across multiple scenes.

![](../../assets/78ca3484200447fd.gif)


Other features of the Template system also include:

- Adding instances in the Scene editor (including drag and drop support of template assets to the Hierarchy panel)
- Overriding properties on a per instance basis
- Nested Templates which allows referencing a Template in another Template
- Creating a new instances via code from an asset reference

In terms of how they can be used, we have been beta-testing the feature since early 2020 (big thanks to all those that have given us feedback and bug reports 🙏) and some of the use cases we've seen so far include:

- Designing and creating sections of an infinite runner game
- Managing UI screens and instantiating them at runtime
- Different enemy types that a script can reference to randomly generate a level

As you can see, Templates give you a wide range of flexibility of workflow options to manage and modify content in your projects.

Find out more about [Templates in the User Manual](https://developer.playcanvas.com/user-manual/templates/) and give them a try yourself!