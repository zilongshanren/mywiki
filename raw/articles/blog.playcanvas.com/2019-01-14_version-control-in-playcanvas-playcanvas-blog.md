---
title: Version Control in PlayCanvas | PlayCanvas Blog
url: https://blog.playcanvas.com/version-control-in-playcanvas
author: Dave Evans
published: '2019-01-14'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

One of our most requested features has always been for more advanced version control features. We're very pleased to announce that from today we now have built in version control throughout the PlayCanvas Editor. Integrated support for branches, merging and checkpoints brings a host of new workflow options for your team and we're confident that it's going to be a huge productivity multiplier for your HTML5 games and 3D applications.

## How does it work?[](https://blog.playcanvas.com#how-does-it-work)

### Checkpoints[](https://blog.playcanvas.com#checkpoints)

Checkpoints take a snapshot of your project at a moment in time. This lets you restore previous versions or just see a timeline of what changes are being made by each member of your team.

![Version Control Panel](../../assets/2dc2f470883b3baf.jpg)


### Branches[](https://blog.playcanvas.com#branches)

Like other version control systems with PlayCanvas you can create independent lines of development by creating branches. Branches let you or your team work on changes and features that don't affect your main product development.

![Branch and Merge](../../assets/d66fb539bc2d581e.png)


### Merging[](https://blog.playcanvas.com#merging)

Once you've finished work in your branch, you'll want to merge you branch back into your production development. We've got a sophisticated merging interface that let's you merge your code, scenes and assets and resolve any conflicting changes in your scenes and code.

![Conflict Manager](../../assets/a059f195b1ef0d64.jpg)


We've been testing the version control features over the last few months and we know you're going to love them. Read more about how you can use branches in your project in our [developer docs](https://developer.playcanvas.com/user-manual/version-control/).

## What's next?[](https://blog.playcanvas.com#whats-next)

We know that our users have specific needs and want to customize their workflows. With branches now available to isolate development, we've unlocked a host of new opportunities that you can try via our API. For starters it's now possible to synchronize your script assets from your PlayCanvas branch into an external source control system like GitHub. Try this yourself via our [Asset REST API](https://developer.playcanvas.com/user-manual/api/asset-file/), but we'll be building on these features in the future.