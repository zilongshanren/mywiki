---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/interface_c_c_event_dispatcher/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCEventDispatcher.h>`


| void |
|

This is object is responsible for dispatching the events:

Only available on Mac

| void CCEventDispatcher::addKeyboardDelegate:priority: | ( | id<
|

` [virtual]`

Adds a Keyboard delegate to the dispatcher's list. Delegates with a lower priority value will be called before higher priority values. All the events will be propgated to all the delegates, unless the one delegate returns YES.

IMPORTANT: The delegate will be retained.

| void CCEventDispatcher::addMouseDelegate:priority: | ( | id<
|

` [virtual]`

Adds a mouse delegate to the dispatcher's list. Delegates with a lower priority value will be called before higher priority values. All the events will be propgated to all the delegates, unless the one delegate returns YES.

IMPORTANT: The delegate will be retained.

| void CCEventDispatcher::addTouchDelegate:priority: | ( | id<
|

` [virtual]`

Adds a Touch delegate to the dispatcher's list. Delegates with a lower priority value will be called before higher priority values. All the events will be propgated to all the delegates, unless the one delegate returns YES.

IMPORTANT: The delegate will be retained.

| void CCEventDispatcher::removeAllKeyboardDelegates | ( | ) | ` [virtual]` |

Removes all mouse delegates, releasing all the delegates

| void CCEventDispatcher::removeAllMouseDelegates | ( | ) | ` [virtual]` |

Removes all mouse delegates, releasing all the delegates

| void CCEventDispatcher::removeAllTouchDelegates | ( | ) | ` [virtual]` |

Removes all touch delegates, releasing all the delegates

| void CCEventDispatcher::removeKeyboardDelegate: | ( | id | delegate | ) | ` [virtual]` |

removes a mouse delegate

| void CCEventDispatcher::removeMouseDelegate: | ( | id | delegate | ) | ` [virtual]` |

removes a mouse delegate

| void CCEventDispatcher::removeTouchDelegate: | ( | id | delegate | ) | ` [virtual]` |

Removes a touch delegate