---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_contact_filter/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2WorldCallbacks.h>`


| virtual bool |
|

Implement this class to provide collision filtering. In other words, you can implement this class if you want finer control over contact creation.

| virtual bool b2ContactFilter::ShouldCollide | ( |
|

` [virtual]`

Return true if contact calculations should be performed between these two shapes.