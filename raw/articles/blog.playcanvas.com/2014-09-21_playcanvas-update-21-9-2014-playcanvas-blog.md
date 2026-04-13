---
title: PlayCanvas Update 21/9/2014 | PlayCanvas Blog
url: https://blog.playcanvas.com/playcanvas-update-2192014
author: Dave Evans
published: '2014-09-21'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

**New news and old news: plans, iOS support, etc.**

After a short summer hiatus, we're back with regular PlayCanvas feature updates.

### iOS Support[](https://blog.playcanvas.com#ios-support)

In light of the launch of iOS 8 and the new iPhones. We've launched a great new feature which lets you get your PlayCanvas game straight on the App Store. For Pro account holders we now let you download a XCode project which builds quickly and painlessly into a iOS 8 program ready to run natively on your iPhone or iPad.

Take a look at how easy this is in the video we published this month.

### Pricing plans[](https://blog.playcanvas.com#pricing-plans)

We're adding additional plans to our pricing structure to better accommodate bigger users of PlayCanvas. Take a look at our [announcement post](https://blog.playcanvas.com/new-plans/).

### Improvements[](https://blog.playcanvas.com#improvements)

#### Synchronous Components and Cloning[](https://blog.playcanvas.com#synchronous-components-and-cloning)

This has been on the horizon a little while. With this new update to the engine, adding components to an entity and cloning it into new entity are now synchronous. Making your code much simpler:

` var e = this.entity.clone();`

// e is ready to use



Previously in this code, the clone method took at least one frame to execute. This is a big improvement when you are creating Entities on the fly.

#### Publish over existing applications[](https://blog.playcanvas.com#publish-over-existing-applications)

Another little improvement that'll save you time. If you publish an application with the same name as an existing application you'll be prompted to overwrite the older app.

### Application view counts[](https://blog.playcanvas.com#application-view-counts)

This is just the start of something big, but we now display how many people have viewed your published game on the application page. Just take a look at [Doom 3 Gangnam Style](https://playcanv.as/p/iCL6sxgF/)!

### Stay In The Loop[](https://blog.playcanvas.com#stay-in-the-loop)

- Follow us on Twitter,
[@playcanvas](https://twitter.com/playcanvas), for updates on PlayCanvas. - Like the
[PlayCanvas Facebook](https://facebook.com/playcanvas)page for our whimsical views on the game dev scene. - Join and start discussions on the
[PlayCanvas Forum](https://forum.playcanvas.com/).