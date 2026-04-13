---
title: Enumerations
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.0/Kobold2D/html/_k_k_input_enums_8h/
published: '2013-01-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
Kobold2D
2.0
Kobold2D API Reference (iOS version) for www.kobold2d.com developers
|

| enum |
|

The modifier flags (bits) for special keyboard keys, like Shift, Control, Option, Command, Function, Help, etc.

The "virtual keyCodes" for mouse buttons. These are left, right and other. The "other" buttons may include multiple keys which, if supported by the hardware and driver, you can identify with kKKMouseButtonOther and an optional offset, eg "kKKMouseButtonOther + 2" for a fifth mouse button. Note that any of the "other" mouse buttons are non-standard and typically require non-Apple mice to work. You can not rely on any of the "other" buttons being available at all.

Mouse double-clicks are an offset (kKKMouseButtonDoubleClickOffset) to the button codes. Double-clicks are treated as separate buttons by [KKInput](http://www.learn-cocos2d.com/) for your convenience, ie you don't have to test for two consecutive mouse button presses.

Direction bits for the swipe gesture relative are relative to the current device orientation.

A touch can have just began, it can be moving, or it can be ended this frame. The kKKTouchPhaseAny can be used if want to include all three phases in a touch test. The KKTouchPhase enum values are equal to those in the UITouchPhase enum (except for any and lifted), that means they can be used interchangeably.