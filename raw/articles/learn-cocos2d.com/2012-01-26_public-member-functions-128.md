---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_parallax_node/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCParallaxNode.h>`


| void |
|

[CCParallaxNode](http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_parallax_node/): A node that simulates a parallax scroller

The children will be moved faster / slower than the parent according the the parallax ratio.

| void CCParallaxNode::addChild:z:parallaxRatio:positionOffset: | ( |
|

` [virtual]`

Adds a child to the container with a z-order, a parallax ratio and a position offset It returns self, so you can chain several addChilds.

array that holds the offset / ratio of the children