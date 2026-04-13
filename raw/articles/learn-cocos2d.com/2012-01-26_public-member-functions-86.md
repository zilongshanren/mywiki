---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/protocol_o_a_l_suspend_manager-p/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A suspend manager is a listener that also allows other objects to subscribe to receive events as the manager receives them.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/protocol_o_a_l_suspend_manager-p/#details)

`#include <OALSuspendHandler.h>`


| void |
|

A suspend manager is a listener that also allows other objects to subscribe to receive events as the manager receives them.

Add a listener that will receive manual suspend and interrupt events.

| listener | The listener to register with this handler. |

Remove a registered listener.

| listener | The listener to unregister from this handler. |