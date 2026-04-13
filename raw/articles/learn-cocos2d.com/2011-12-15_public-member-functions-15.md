---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone-mac/html/protocol_c_c_mouse_event_delegate-p/
published: '2011-12-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCEventDispatcher.h>`


| BOOL |
|

called when the "mouseDown" event is received. Return YES to avoid propagating the event to other delegates.

called when the "mouseDragged" event is received. Return YES to avoid propagating the event to other delegates.

called when the "mouseEntered" event is received. Return YES to avoid propagating the event to other delegates.

called when the "mouseExited" event is received. Return YES to avoid propagating the event to other delegates.

called when the "mouseMoved" event is received. Return YES to avoid propagating the event to other delegates. By default, "mouseMoved" is disabled. To enable it, send the "setAcceptsMouseMovedEvents:YES" message to the main window.

called when the "mouseUp" event is received. Return YES to avoid propagating the event to other delegates.

called when the "otherMouseDown" event is received. Return YES to avoid propagating the event to other delegates.

called when the "otherMouseDragged" event is received. Return YES to avoid propagating the event to other delegates.

called when the "otherMouseUp" event is received. Return YES to avoid propagating the event to other delegates.

called when the "rightMouseDown" event is received. Return YES to avoid propagating the event to other delegates.

called when the "rightMouseDragged" event is received. Return YES to avoid propagating the event to other delegates.

called when the "rightMouseUp" event is received. Return YES to avoid propagating the event to other delegates.

called when the "scrollWheel" event is received. Return YES to avoid propagating the event to other delegates.