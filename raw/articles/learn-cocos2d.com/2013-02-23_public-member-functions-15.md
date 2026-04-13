---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_send_messages/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone-extensions
0.2
Cocos2D Extensions API Reference (iOS version) for www.kobold2d.com developers
|

| (id) | -
|

sends messsages to a target when it is run.

It is different than the CCCallFunc classes in that any message can be sent to a target regardless of the number/type of arguments.

NOTE: Any selector in the NSObject class and any selector in the NSObject and NSCopying protocals cannot be added via -addMessage. If you need to call one of those selectors, create an NSInvocation and add it via -addInvocation:.

Usage: Create a [CCSendMessages](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_send_messages/) instance with a target using -initWithTarget: or +actionWithTarget:

Add message call(s) to it: (assuming sendMessages is your [CCSendMessages](http://www.learn-cocos2d.com/api-ref/2.1/cocos2d-iphone-extensions/html/interface_c_c_send_messages/) object) [[sendMessages addMessage] setOpacity:0.5]; [[sendMessages addMessage] long:0.5 selector:obj example:ccp(3,3)];

Run it on a CCNode with -runAction:, or add it to a CCSequence to run it later on!

Also, arguments don't have to be Objective-C objects.

Sends all captured messages to a target.

You don't need to use this method directly - use CCNode::runAction: instead.