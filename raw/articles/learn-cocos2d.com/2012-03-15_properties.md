---
title: Properties
url: http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_touch/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <KKTouch.h>`


| NSUInteger |
|

The Kobold2D equivalent of the UITouch class contains the same information as a UITouch. The locations are already converted to the Cocos2D view coordinate space, you should *not* call convertToGL on the [KKTouch](http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_touch/) locations. Touches are pooled to avoid frequent alloc/dealloc cycles as fingers touch the screen and are lifted back up again.

The touchID property is a unique identifier for a particular finger that touches the screen. The touchID is simply the UITouch* pointer cast to NSUInteger, so you can get to the UITouch* if needed by casting touchID to UITouch*: UITouch* uiTouch = (UITouch*)(kkTouch.touchID);

CGPoint KKTouch::location` [read, assign]` |

The current location of the touch, already converted to Cocos2D view coordinates and device orientation.

CGPoint KKTouch::previousLocation` [read, assign]` |

The previous (frame's) location of the touch, already converted to Cocos2D view coordinates and device orientation.

NSUInteger KKTouch::tapCount` [read, assign]` |

How often the finger was tapped for this touch.

NSTimeInterval KKTouch::timestamp` [read, assign]` |

The timestamp when the UITouch was last updated.

NSUInteger KKTouch::touchID` [read, assign]` |

An identifier that uniquely identifies one particular finger while it is touching. Used to track fingers over several frames.