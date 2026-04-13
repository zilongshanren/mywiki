---
title: Strategies for Accessing Other Cocos2D Nodes In The Scene Hierarchy
url: http://www.learn-cocos2d.com/2012/09/strategies-accessing-cocos2d-nodes-scene-hierarchy/
author: Grillaface says
published: '2012-09-20'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A question I see frequently asked by Cocos2D developers, in simplified form:

`"I have this node A, how can I access this other node B?"`


Whether it’s executing a message or getting the node itself as a reference, developers have a problem accessing nodes in other parts of the scene. Or the scene itself.

The most obvious is also a potentially dangerous solution: initialize the node with the references to the other nodes it needs. The danger lies in [retain cycles](http://www.mikeash.com/pyblog/friday-qa-2010-04-30-dealing-with-retain-cycles.html), when node A has a retaining reference to node B and vice versa - then neither of them will let go, memory is leaked, strange bugs appear.

From the [Cocos2D questions on stackoverflow.com](http://stackoverflow.com/questions/tagged/cocos2d+or+cocos2d-iphone+or+cocos2d-android+or+cocos2d-x+or+cocos2d-x-for-xna+or+cocos2d-python+or+cocos2d-javascript+or+cocos3d+or+kobold2d+or+koboldscript+or+packagemaker?sort=newest&pagesize=50) it’s obvious how prevalent retain cycles issues are among Cocos2D developers. Therefore this article with strategies for accessing other nodes in various situations with their benefits and drawbacks.

And an explanation why *self.parent.parent.parent…* is really terrible practice.

![paperbackstack_medium](../../../wordpress/wp-content/uploads/paperbackstack_medium.png)


#### Essential Cocos2D: Free Sample

Today’s [iDevBlogADay](http://idevblogaday.com/) article is a sample article from the upcoming **Essential Cocos2D** online documentation. That’s why it’s on a separate page.

More about **Essential Cocos2D** soon. It’s growing fast. And not to forget: **Learn cocos2d 2** is now available!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Great article Steffen. Question though - like you mentioned, the first thing that comes to mind is passing a reference to the node in init. Assuming the node to be referenced is always stored in a weak property, is there ever any risk of a retain cycle?

No. But in ARC it should be a zeroing weak reference. Otherwise, and under MRC, you run the risk of a crash. It’s fine though if the referenced node is a parent or grandparent because the lifetime of the node will end before that of the parent. But if the node is a sibling (parallel) node or from a different branch of the node hierarchy, you can’t really be 100% sure about the referenced node’s lifetime.