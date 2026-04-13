---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_listener/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

The listener represents the user who is listening to sounds in 3D space.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_listener/#details)

`#include <ALListener.h>`


| id |
|

The listener represents the user who is listening to sounds in 3D space.

This object controls his position, orientation, and velocity, as well as providing a master gain.

A context contains one and only one listener.

(INTERNAL USE) Initialize a listener for the specified context.

| context | the context to create this listener on. |

(INTERNAL USE) Create a listener for the specified context.

| context | the context to create this listener on. |

Handles suspending and interrupting for this object.

float ALListener::gain` [read, write, assign]` |

Gain (volume), affecting every sound this listener hears (0.0 = no sound, 1.0 = max volume).

Only valid if this listener's context is the current context.

bool ALListener::muted` [read, write, assign]` |

Causes this listener to stop hearing sound.

It's called "muted" rather than "deaf" to give a consistent name with other mute functions.

Orientation (up: x, y, z, at: x, y, z).

Only valid if this listener's context is the current context.

Position (x, y, z).

Only valid if this listener's context is the current context.

Velocity (x, y, z).

Only valid if this listener's context is the current context.