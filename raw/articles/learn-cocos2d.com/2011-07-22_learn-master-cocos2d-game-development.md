---
title: Learn & Master Cocos2D Game Development
url: http://www.learn-cocos2d.com/2010/05/cocos2d-faq-addition-sprite-bounding-rectangle/
published: '2011-07-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I’ve added two short lessons to the cocos2d for iPhone FAQ about [getting a sprite’s bounding box (with code)](http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/14813-how-to-get-a-sprites-bounding-box-bounding-rectangle-with-code/) and [testing rotated rectangles for intersection](http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/14814-how-to-test-intersection-of-rotated-rectangles/) (collision).

cocos2d doesn’t have [a method to get the bounding box](http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/14813-how-to-get-a-sprites-bounding-box-bounding-rectangle-with-code/), and using the [sprite contentSize] to create a rectangle is flawed because it will stop working as soon as the sprite is either scaled or its anchorPoint is not at the center (0.5f, 0.5f). It’s easy to fix that and it’s even easier to write an Objective-C category so that you can call [sprite getBoundingRect] as if it were a regular CCSprite method provided by cocos2d. Of course i know that as soon as cocos2d developers read this the question about [testing for rotated rectangle intersection](http://www.learn-cocos2d.com/knowledge-base/cocos2d-iphone-faq/learn-cocos2d-public-content/manual/cocos2d-general/14814-how-to-test-intersection-of-rotated-rectangles/) will come up. I linked to the “proper” solution but honestly, i believe the more pragmatic approaches that i’ve added will actually work better in most cases.