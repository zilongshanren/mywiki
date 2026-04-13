---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_destruction_listener/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2WorldCallbacks.h>`


| virtual void |
|

Joints and fixtures are destroyed when their associated body is destroyed. Implement this listener so that you may nullify references to these joints and shapes.

Called when any joint is about to be destroyed due to the destruction of one of its attached bodies.

Called when any fixture is about to be destroyed due to the destruction of its parent body.