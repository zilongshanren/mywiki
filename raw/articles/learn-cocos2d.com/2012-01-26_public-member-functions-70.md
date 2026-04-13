---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Kobold2D/html/interface_k_k_input/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <KKInput.h>`


Kobold2D User Input handler that gives you both a polling API (eg isKeyDown) and an event-driven API configurable via config.lua. [KKInput](http://www.learn-cocos2d.com/api-ref/1.0/Kobold2D/html/interface_k_k_input/) supports all input methods: keyboard, mouse, touch, motion (accelerometer and gyroscope) and gestures.

The design of the [KKInput](http://www.learn-cocos2d.com/api-ref/1.0/Kobold2D/html/interface_k_k_input/) API is meant to be as simple as possible, giving you many convenience functions. For example, mouse button double-clicks are treated as if they were separate buttons so you don't have to write your own code to test for double-clicks. You can also easily test mouse button states in combination with keyboard modifierFlags to detect Control-Clicks and the like.

It is legal (no compile error) to call keyboard & mouse methods on iOS, as is calling touch, motion and gesture methods on Mac OS. Of course you won't get meaningful results/values, the real benefit is that you can write #ifdef-less code.

Note: all "ThisFrame" methods are only useful if you poll the state every frame (eg scheduled update method without an interval), otherwise you might "miss" the event because the state will only remain true for one frame.

| BOOL KKInput::isAnyTouchOnNode:touchPhase: | ( | CCNode * | node, |
| [touchPhase]
|

` [virtual]`

Tests if a touch in the given touchPhase was on a node. The test is correct even if the node was rotated and/or scaled.

returns true if the key with the given virtual keyCode is down

| BOOL KKInput::isKeyDown:modifierFlags: | ( |
|

` [virtual]`

returns true if the key with the given virtual keyCode and the given modifierFlags are down

returns true if the key with the given virtual keyCode just changed from keyUp to keyDown state in the current frame

| BOOL KKInput::isKeyDownThisFrame:modifierFlags: | ( |
|

` [virtual]`

returns true if the key with the given virtual keyCode just changed from keyUp to keyDown state in the current frame, with modifiers. The modifiers must already be down, eg pressing modifier(s) followed by key will return true but pressing key first and modifier(s) second won't.

returns true if the key with the given virtual keyCode is up

| BOOL KKInput::isKeyUp:modifierFlags: | ( |
|

` [virtual]`

returns true if the key with the given virtual keyCode and the given modifierFlags are up

returns true if the key with the given virtual keyCode just changed from keyDown to keyUp state in the current frame

| BOOL KKInput::isKeyUpThisFrame:modifierFlags: | ( |
|

` [virtual]`

returns true if the key with the given virtual keyCode just changed from keyDown to keyUp state in the current frame, with modifiers. The modifiers must already be down when the key is released.

returns true if the mouse button with the given button code is down

| BOOL KKInput::isMouseButtonDown:modifierFlags: | ( |
|

` [virtual]`

returns true if the mouse button with the given button code and the given modifierFlags are down

returns true if the mouse button with the given button code just changed from up to down state in the current frame

| BOOL KKInput::isMouseButtonDownThisFrame:modifierFlags: | ( |
|

` [virtual]`

returns true if the mouse button with the given button code just changed from up to down state in the current frame, with modifiers. The modifiers must already be down, eg pressing modifier(s) followed by mouse button will return true but pressing mouse button first and modifier(s) second won't.

returns true if the mouse button with the given button code is up

returns true if the mouse button with the given button code just changed from down to up state in the current frame

Returns the location (in cocos2d coordinates) of any touch in the given phase. If there is no finger touching the screen, CGPointZero is returned.

The given touch will be invalidated, its touch phase is set to KKTouchPhaseLifted and all information in the [KKTouch](http://www.learn-cocos2d.com/) class is reset. However the [KKTouch](http://www.learn-cocos2d.com/) remains in the CCArray* touches list for the remainder of the frame, it is removed after the current frame ends. This allows calling the removeTouch method while iterating over the touches array.

| void KKInput::resetInputStates | ( | ) | ` [virtual]` |

Resets the entire [KKInput](http://www.learn-cocos2d.com/api-ref/1.0/Kobold2D/html/interface_k_k_input/) system, meaning all current touches, keypresses, etc. will be removed and state variables are reset. However gesture recognizers will remain enabled and so are other "enabled" states. Note: This method is called automatically when changing scenes (replaceScene, pushScene, popScene).

| UISwipeGestureRecognizer* KKInput::swipeGestureRecognizerForDirection: | ( |
|

` [virtual]`

Returns the UISwipeGestureRecognizer for the given direction if enabled, otherwise returns nil.

Returns the [KKAcceleration](http://www.learn-cocos2d.com/) object used by [KKInput](http://www.learn-cocos2d.com/api-ref/1.0/Kobold2D/html/interface_k_k_input/) internally. The acceleration object is valid during the entire lifetime of your application and its acceleration values will continue to be updated (depending on the accelerometerActive property).

BOOL KKInput::accelerometerActive` [read, write, assign]` |

Set to YES to enable accelerometer input. When enabled, the acceleration values are updated every frame. On devices that support it (running iOS 4.0) the CMMotionManager is used to obtain acceleration data, otherwise UIAcceleration is used. If deviceMotion is set to YES, acceleration will be taken from userAcceleration property of the [CMDeviceMotion](http://developer.apple.com/library/ios/#documentation/CoreMotion/Reference/CMDeviceMotion_Class/Reference/Reference.html#//apple_ref/doc/c_ref/CMDeviceMotion) class.

BOOL KKInput::accelerometerAvailable` [read, assign]` |

Is YES if the current device has an accelerometer, and accelerometer input can be activated and used.

BOOL KKInput::acceptsMouseMovedEvents` [read, write, assign]` |

Determines if mouse moved events are accepted or not. Unless you need to track all mouse movements it is recommended to set this to NO. This is the same setting as: AcceptsMouseMovedEvents in config.lua.

BOOL KKInput::anyTouchBeganThisFrame` [read, assign]` |

Returns YES if any touch began this frame.

BOOL KKInput::anyTouchEndedThisFrame` [read, assign]` |

Returns YES if any touch ended this frame.

CGPoint KKInput::anyTouchLocation` [read, assign]` |

Returns the location of any touch, or CGPointZero if there's no touch. Useful mostly when not using multi touch and you just want to get the touch location easily.

Returns the [KKDeviceMotion](http://www.learn-cocos2d.com/) object used by [KKInput](http://www.learn-cocos2d.com/api-ref/1.0/Kobold2D/html/interface_k_k_input/) internally. The deviceMotion object is valid during the entire lifetime of your application and its properties will continue to be updated (depending on the deviceMotionActive property). Gives you access to acceleration, rotationRate, gravity and attitude as [CMDeviceMotion](http://developer.apple.com/library/ios/#documentation/CoreMotion/Reference/CMDeviceMotion_Class/Reference/Reference.html#//apple_ref/doc/c_ref/CMDeviceMotion) object.

BOOL KKInput::deviceMotionActive` [read, write, assign]` |

Set to YES to enable device motion input (combined accelerometer & gyroscope -> attitude). DeviceMotion relies on the CoreMotion.framework which is only available on devices running iOS 4.0 and later, and only available on devices that have both accelerometer and gyroscope (4th generation devices and iPad 2). Use deviceMotionAvailable property to check for availability on the current device. You can get acceleration, rotation plus attitude and gravity via the deviceMotion property ([KKDeviceMotion](http://www.learn-cocos2d.com/)). The rotationRate and acceleration can also be obtained via the regular rotationRate and acceleration properties.

BOOL KKInput::deviceMotionAvailable` [read, assign]` |

Is YES if the current device has both a gyroscope and accelerometer, and device motion (sensor fusion) input can be activated and used.

UITapGestureRecognizer* KKInput::doubleTapGestureRecognizer` [read, assign]` |

Returns the UITapGestureRecognizer for double-taps if enabled, otherwise returns nil.

BOOL KKInput::gestureDoubleTapEnabled` [read, write, assign]` |

Enables the (one finger) double tap gesture recognizer. Note that single tap gesture will be delayed if it is active. This is because the single tap gesture recognizer has to wait for the double-tap recognizer to fail before it is being recognized. See this question for a more detailed explanation: [http://stackoverflow.com/questions/3081215/ipad-gesture-recognizer-delayed-response](http://stackoverflow.com/questions/3081215/ipad-gesture-recognizer-delayed-response)

CGPoint KKInput::gestureDoubleTapLocation` [read, assign]` |

The location of the last double-tap. Is updated every time a double-tap gesture is recognized.

BOOL KKInput::gestureDoubleTapRecognizedThisFrame` [read, assign]` |

Is YES if a double-tap gesture was recognized in this frame.

BOOL KKInput::gestureLongPressBegan` [read, assign]` |

Is YES when the long-press gesture has began and stays true until the finger moves too far or is lifted.

BOOL KKInput::gestureLongPressEnabled` [read, write, assign]` |

Enables the (one finger) long-press gesture recognizer. A long-press occurs when the finger stays almost stationary (default: 10 pixels) on the screen for a minimum time period (0.5 seconds). If these conditions are true, the long-press gesture remains active until the finger is lifted. That means you have to long-press an object, and when the long-press gesture is recognized the user can move the finger freely. This makes long-press gestures ideal for initiating a drag & drop operation.

CGPoint KKInput::gestureLongPressLocation` [read, assign]` |

Returns the location of the long-press gesture.

BOOL KKInput::gesturePanBegan` [read, assign]` |

Is YES when the pan gesture has began and stays true until the finger is lifted.

BOOL KKInput::gesturePanEnabled` [read, write, assign]` |

Enables the (one finger) pan gesture recognizer. A pan occurs when the finger touches the screen and starts moving within a short amount of time (otherwise it may be recognized as a long press gesture instead). Since the pan gesture is similar to the swipe gesture, the swipe and pan gestures will be recognized simultaneously if both are enabled at the same time.

CGPoint KKInput::gesturePanLocation` [read, assign]` |

Returns the location of the pan gesture.

CGPoint KKInput::gesturePanTranslation` [read, write, assign]` |

Returns the translation of the pan gesture, ie how far (in points) the finger has moved from the point where the pan gesture began. For example, if translation is -50, 20 then the finger has moved 50 points to the left and 20 points upwards from its initial position. You can set the translation at any time, for example to reset it to (0,0). Note that setting the translation resets the gesturePanVelocity.

CGPoint KKInput::gesturePanVelocity` [read, assign]` |

Returns the velocity of the pan gesture in points per frame. If you need points per second (like UIPanGestureRecognizer returns), simply multiply the x and y coordinates with the MaxFrameRate setting (ie 60).

BOOL KKInput::gesturePinchBegan` [read, assign]` |

Is YES when the pinch gesture has began and stays true until both fingers are lifted.

BOOL KKInput::gesturePinchEnabled` [read, write, assign]` |

Enables the (two finger) pinch gesture recognizer. A pinch occurs when two fingers touch the screen and move either towards or away from each other. The rotation gesture ends when both fingers are lifted. Can be used simultaneously with the rotation gesture recognizer for a rotate & scale action.

It is recommended to not enable the pan or long press gestures simultaneously with the pinch gesture, since the pan and long press gestures will make it difficult for the user to correctly initiate the pinch gesture. If the pan gesture is enabled, the user must place both fingers on the screen before moving either one more than 10 pixels. This is tricky to achieve. If the long press gesture is enabled, the user must place both fingers on the screen within the time it takes to initiate a long press (0.5 seconds). This is feasible but can still be confusing.

CGPoint KKInput::gesturePinchLocation` [read, assign]` |

Returns the location of the pinch gesture, which is the middle point between the two fingers.

float KKInput::gesturePinchScale` [read, write, assign]` |

Returns the scale factor relative to the two fingers. If you change the scale factor the pinch velocity will be reset.

float KKInput::gesturePinchVelocity` [read, assign]` |

Returns the velocity of the pinch gesture in scale factor per frame.

float KKInput::gestureRotationAngle` [read, write, assign]` |

Returns the rotation angle in Cocos2D direction values (an angle in the range 0 to 360 degrees). If you change the rotation angle the rotation velocity will be reset.

BOOL KKInput::gestureRotationBegan` [read, assign]` |

Is YES when the rotation gesture has began and stays true until both fingers are lifted.

BOOL KKInput::gestureRotationEnabled` [read, write, assign]` |

Enables the (two finger) rotation gesture recognizer. A rotation occurs when two fingers touch the screen and the fingers move in opposing directions in a circular motion. The rotation gesture ends when both fingers are lifted. Can be used simultaneously with the pinch gesture recognizer for a rotate & scale action.

It is recommended to not enable the pan or long press gestures simultaneously with the rotation gesture, since the pan and long press gestures will make it difficult for the user to correctly initiate the rotation gesture. If the pan gesture is enabled with rotation, the user must place both fingers on the screen before moving either one more than 10 pixels. This is tricky to achieve. If the long press gesture is enabled, the user must place both fingers on the screen within the time it takes to initiate a long press (0.5 seconds). This is feasible but can still be confusing.

CGPoint KKInput::gestureRotationLocation` [read, assign]` |

Returns the location of the rotation gesture, which is the middle point between the two fingers.

float KKInput::gestureRotationVelocity` [read, assign]` |

Returns the velocity of the rotation gesture in degrees per frame.

BOOL KKInput::gesturesAvailable` [read, assign]` |

Returns YES if gesture recognizers are available. Gesture Recognizers are available on devices running iOS 3.2 or newer.

The direction of the swipe. The direction is already converted to the current device orientation, so that left/right/up/down are relative to how the user is holding the device and up is always up, left is always to the left, and so on.

BOOL KKInput::gestureSwipeEnabled` [read, write, assign]` |

Enables the (one finger) swipe gesture recognizer. A swipe occurs when moving the finger mostly in one direction. The swipe can be slow over a short distance or fast over a long distance. Since the pan gesture is similar to the swipe gesture, both will be recognized simulataneously if swipe and pan gestures are enabled at the same time.

CGPoint KKInput::gestureSwipeLocation` [read, assign]` |

The start location of the swipe. Use locationOfAnyTouchInPhase method with phase of KKTouchPhaseCancelled to get the end location of the swipe.

BOOL KKInput::gestureSwipeRecognizedThisFrame` [read, assign]` |

Is YES if a swipe gesture was recognized in this frame.

BOOL KKInput::gestureTapEnabled` [read, write, assign]` |

Enables the (one finger) tap gesture recognizer. Note that the tap recognition may be delayed if double-tap is also active. See the explanation in gestureDoubleTapEnabled.

CGPoint KKInput::gestureTapLocation` [read, assign]` |

The location of the last tap. Is updated every time a tap gesture is recognized.

BOOL KKInput::gestureTapRecognizedThisFrame` [read, assign]` |

Is YES if a tap gesture was recognized in this frame.

BOOL KKInput::gyroActive` [read, write, assign]` |

Set to YES to enable gyroscope input. When enabled, the gyro values are updated every frame. Only available on devices that have a gyroscope (4th generation, iPad 2, and newer). Use gyroAvailable property to check for gyroscope availability on the current device. If deviceMotion is set to YES, rotationRate will be taken from rotationRate property of the [CMDeviceMotion](http://developer.apple.com/library/ios/#documentation/CoreMotion/Reference/CMDeviceMotion_Class/Reference/Reference.html#//apple_ref/doc/c_ref/CMDeviceMotion) class.

BOOL KKInput::gyroAvailable` [read, assign]` |

Is YES if the current device has a gyroscope, and gyroscope input can be activated and used.

BOOL KKInput::isAnyKeyDown` [read, assign]` |

returns true if any keyboard key is down

BOOL KKInput::isAnyKeyDownThisFrame` [read, assign]` |

returns true if any keyboard key changed from keyUp to keyDown state in the current frame

BOOL KKInput::isAnyKeyUpThisFrame` [read, assign]` |

returns true if any keyboard key changed from keyDown to keyUp state in the current frame

BOOL KKInput::isAnyMouseButtonDown` [read, assign]` |

returns true if any mouse button is down

BOOL KKInput::isAnyMouseButtonDownThisFrame` [read, assign]` |

returns true if any mouse button changed from up to down state in the current frame

BOOL KKInput::isAnyMouseButtonUpThisFrame` [read, assign]` |

returns true if any mouse button changed from down to up state in the current frame

UILongPressGestureRecognizer* KKInput::longPressGestureRecognizer` [read, assign]` |

Returns the UILongPressGestureRecognizer if enabled, otherwise returns nil.

CGPoint KKInput::mouseLocation` [read, assign]` |

returns the mouse cursor location in window coordinates. If you want to track ALL mouse movements you'll have to turn on trackMouseMovedEvents (AcceptsMouseMovedEvents in config.lua).

CGPoint KKInput::mouseLocationDelta` [read, assign]` |

returns the delta of the current and previous mouse cursor location in window coordinates. With trackMouseMovedEvents (AcceptsMouseMovedEvents in config.lua) turned OFF (NO) the delta location will be the location of the previous mouse down, mouse up, or mouse dragged event and could be quite far away from the current mouseLocation. If you need to track delta locations accurately you need to turn on trackMouseMovedEvents.

BOOL KKInput::multipleTouchEnabled` [read, write, assign]` |

Set to YES to allow multi touch events. If NO, only the first touch will be tracked. Same as config.lua setting EnableMultiTouch.

UIPanGestureRecognizer* KKInput::panGestureRecognizer` [read, assign]` |

Returns the UIPanGestureRecognizer if enabled, otherwise returns nil.

UIPinchGestureRecognizer* KKInput::pinchGestureRecognizer` [read, assign]` |

Returns the UIPinchGestureRecognizer if enabled, otherwise returns nil.

CGPoint KKInput::previousMouseLocation` [read, assign]` |

returns the previous mouse cursor location in window coordinates. With trackMouseMovedEvents (AcceptsMouseMovedEvents in config.lua) turned OFF (NO) the previous location will be the location of the previous mouse down, mouse up, or mouse dragged event and could be quite far away from the current mouseLocation. If you need to track previous locations accurately you need to turn on trackMouseMovedEvents.

UIRotationGestureRecognizer* KKInput::rotationGestureRecognizer` [read, assign]` |

Returns the UIRotationGestureRecognizer if enabled, otherwise returns nil.

Returns the [KKRotationRate](http://www.learn-cocos2d.com/) object used by [KKInput](http://www.learn-cocos2d.com/api-ref/1.0/Kobold2D/html/interface_k_k_input/) internally. The rotationRate object is valid during the entire lifetime of your application and its rotation values will continue to be updated (depending on the gyroActive property).

CGPoint KKInput::scrollWheelDelta` [read, assign]` |

returns the current scroll wheel delta position. Will be (0,0) if the user hasn't scrolled the wheel in the current frame.

UITapGestureRecognizer* KKInput::tapGestureRecognizer` [read, assign]` |

Returns the UITapGestureRecognizer if enabled, otherwise returns nil.

CCArray* KKInput::touches` [read, assign]` |

BOOL KKInput::touchesAvailable` [read, assign]` |

Returns YES if there are touches available this frame, ie if the uiTouches array contains UITouch objects. NO if uiTouches is currently empty.

BOOL KKInput::userInteractionEnabled` [read, write, assign]` |

Enable or disable user interaction events for the Cocos2D glView entirely.