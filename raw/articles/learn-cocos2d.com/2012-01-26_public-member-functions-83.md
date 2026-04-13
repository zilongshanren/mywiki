---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_suspend_handler/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Provides two controls (interrupted and manuallySuspended) for suspending a slave object, and also propagates such control messages to interested listeners.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_suspend_handler/#details)

`#include <OALSuspendHandler.h>`


| id |
|

Provides two controls (interrupted and manuallySuspended) for suspending a slave object, and also propagates such control messages to interested listeners.

"interrupted" is meant to be set by the system when an interrupt occurs.


"manuallySuspended" is a user-settable control for suspending an object.

"manuallySuspended" also has an extra step in its processing: When set, the handler makes a note of what its listeners' "manuallySuspended" values are. When cleared, it will only clear a listener's "manuallySuspended" value if it was not set at suspend time. This allows for ad-hoc setting/clearing of "manuallySuspended" in the middle of a handler/listener graph rather than only from the top level.


When either control is set, the slave object will be suspended. When both are cleared, the slave object will be unsuspended.


Add a listener that will receive manual suspend and interrupt events.

| listener | The listener to register with this handler. |

|

` [static, virtual]`

Create a new handler with the specified slave target and selector.

The selector provided must take a single boolean value like so:


| target | The slave object that will receive suspend/unsuspend events. |
| selector | The selector for a "set suspended" method, taking a single boolean parameter. |

| id OALSuspendHandler::initWithTarget:selector: | ( | id | target, |
| [selector] SEL | selector |
||
| ) | ` [virtual]` |

Initialize a handler with the specified slave target and selector.

The selector provided must take a single boolean value like so:


| target | The slave object that will receive suspend/unsuspend events. |
| selector | The selector for a "set suspended" method, taking a single boolean parameter. |

Remove a registered listener.

| listener | The listener to unregister from this handler. |

Listeners that will receive manualSuspend and interrupt events.

Holder for the state of manualSuspend in listeners when this object is manually suspended.

Selector to be invoked on suspend or unsuspend.

Takes the signature: setSelected:(bool) value

Slave object that is notified when this object suspends or unsuspends.

bool OALSuspendHandler::interrupted` [read, write, assign]` |

If YES, the interrupt control is set.

bool OALSuspendHandler::manuallySuspended` [read, write, assign]` |

If YES, the manual suspend control is set.

bool OALSuspendHandler::suspended` [read, assign]` |

If YES, the slave object is suspended.