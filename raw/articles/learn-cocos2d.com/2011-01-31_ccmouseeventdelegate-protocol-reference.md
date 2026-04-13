---
title: <CCMouseEventDelegate> Protocol Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_mouse_event_delegate-p/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCEventDispatcher.h](http://www.learn-cocos2d.com/)"

| (BOOL) | -
|

[CCMouseEventDelegate](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/protocol_c_c_mouse_event_delegate-p/) protocol. Implement it in your node to receive any of mouse events

| - (BOOL) ccMouseDown: | (NSEvent *) | event |
` [optional]` |

called when the "mouseDown" event is received. Return YES to avoid propagating the event to other delegates.

| - (BOOL) ccMouseDragged: | (NSEvent *) | event |
` [optional]` |

called when the "mouseDragged" event is received. Return YES to avoid propagating the event to other delegates.

| - (void) ccMouseEntered: | (NSEvent *) | theEvent |
` [optional]` |

called when the "mouseEntered" event is received. Return YES to avoid propagating the event to other delegates.

| - (void) ccMouseExited: | (NSEvent *) | theEvent |
` [optional]` |

called when the "mouseExited" event is received. Return YES to avoid propagating the event to other delegates.

| - (BOOL) ccMouseMoved: | (NSEvent *) | event |
` [optional]` |

called when the "mouseMoved" event is received. Return YES to avoid propagating the event to other delegates. By default, "mouseMoved" is disabled. To enable it, send the "setAcceptsMouseMovedEvents:YES" message to the main window.

| - (BOOL) ccMouseUp: | (NSEvent *) | event |
` [optional]` |

called when the "mouseUp" event is received. Return YES to avoid propagating the event to other delegates.

| - (BOOL) ccOtherMouseDown: | (NSEvent *) | event |
` [optional]` |

called when the "otherMouseDown" event is received. Return YES to avoid propagating the event to other delegates.

| - (BOOL) ccOtherMouseDragged: | (NSEvent *) | event |
` [optional]` |

called when the "otherMouseDragged" event is received. Return YES to avoid propagating the event to other delegates.

| - (BOOL) ccOtherMouseUp: | (NSEvent *) | event |
` [optional]` |

called when the "otherMouseUp" event is received. Return YES to avoid propagating the event to other delegates.

| - (BOOL) ccRightMouseDown: | (NSEvent *) | event |
` [optional]` |

called when the "rightMouseDown" event is received. Return YES to avoid propagating the event to other delegates.

| - (BOOL) ccRightMouseDragged: | (NSEvent *) | event |
` [optional]` |

called when the "rightMouseDragged" event is received. Return YES to avoid propagating the event to other delegates.

| - (BOOL) ccRightMouseUp: | (NSEvent *) | event |
` [optional]` |

called when the "rightMouseUp" event is received. Return YES to avoid propagating the event to other delegates.

| - (BOOL) ccScrollWheel: | (NSEvent *) | theEvent |
` [optional]` |

called when the "scrollWheel" event is received. Return YES to avoid propagating the event to other delegates.