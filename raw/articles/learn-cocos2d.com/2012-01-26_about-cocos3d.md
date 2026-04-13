---
title: About cocos3d
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/index/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Cocos3d extends cocos2d to add support for full 3D rendering, in combination with normal cocos2d 2D rendering.

Rendering of 3D objects is performed within a [CC3Layer](http://www.learn-cocos2d.com/), which is a specialized cocos2d layer. In your application, you will usually create a customized subclass of [CC3Layer](http://www.learn-cocos2d.com/), which you add to a CCScene, or other CCLayer, to act as a bridge between the 2D and 3D rendering.

The [CC3Layer](http://www.learn-cocos2d.com/) instance holds a reference to an instance of [CC3World](http://www.learn-cocos2d.com/), which manages the 3D model objects, including loading from 3D model files, such as PowerVR POD files. You will usually create a customized subclass of [CC3World](http://www.learn-cocos2d.com/) to create and manage the objects and dynamics of your 3D world.