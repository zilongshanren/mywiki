---
title: Kobold2D Preview 4 now available!
url: http://www.learn-cocos2d.com/2011/09/kobold2d-preview-4/
author: Learn Cocos; Release Date; Learn; Master Cocos
published: '2011-09-28'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Without further ado:

**Enjoy it!**

The Most Important Changes & Additions:


#### Better & Easier User Input with KKInput

**KKInput** ([Class Reference](http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_input/)) enables you to [poll Mac keyboard & mouse states](http://www.learn-cocos2d.com/2011/09/kobold2d-polling-user-input-kkinput/) (Mac) as well as accelerometer, gyroscope and device motion data (iOS).

KKInput comes with a **User Input template project** and a CCNode extension method **containsPoint** which allows you to test if the given point is within the node’s contentSize and works correctly even if the node is rotated and/or scaled - a commonly asked question if you [google it](https://www.google.com/search?rls=en&q=cocos2d+sprite+touch+rotated&ie=UTF-8&oe=UTF-8):

[cc lang=”cpp”]

KKInput* input = [KKInput sharedInput];

CCSprite* sprite = (CCSprite*)[self getChildByTag:99];

if ([sprite containsPoint:input.mouseLocation])

{

touchSprite.color = ccGREEN;

}

else

{

touchSprite.color = ccWHITE;

}

[/cc]

Accelerometer filtering ([Class reference](http://www.learn-cocos2d.com/)) is built into KKInput! You only need to access one of the “filtered” accelerometer properties (smoothed or instantaneous) and specify the filtering factor (defaults to 0.1f). The filtering algorithm is only performed once per frame, and only if you read from the smoothed or instantaneous properties - in all other cases filtering is not applied to conserve those precious CPU cycles.

Gyroscope ([Class reference](http://www.learn-cocos2d.com/)) and Device Motion ([Class reference](http://www.learn-cocos2d.com/)) is also available on devices that support it: iPhone 4, iPod touch 4, iPad 2 and newer, running iOS 4.0 or newer. Check out this code to see how easy it is now to animate a game object based on accelerometer (acceleration: raw, smoothed and instantaneous), gyroscope (rotation) or deviceMotion (attitude: pitch, roll, yaw) values with KKInput:

[cc lang=”cpp”]

-(void) moveShipWithMotionSensors

{

const float kShipSpeed = 25.0f;

KKInput* input = [KKInput sharedInput];

CGPoint shipPosition = ship.position;

switch (inputType)

{

case kAccelerometerValuesRaw:

shipPosition.x += input.acceleration.rawX * kShipSpeed;

shipPosition.y += input.acceleration.rawY * kShipSpeed;

break;

case kAccelerometerValuesSmoothed:

shipPosition.x += input.acceleration.smoothedX * kShipSpeed;

shipPosition.y += input.acceleration.smoothedY * kShipSpeed;

break;

case kAccelerometerValuesInstantaneous:

shipPosition.x += input.acceleration.instantaneousX * kShipSpeed;

shipPosition.y += input.acceleration.instantaneousY * kShipSpeed;

break;

case kGyroscopeRotationRate:

shipPosition.x += input.rotationRate.x * kShipSpeed;

shipPosition.y += input.rotationRate.y * kShipSpeed;

break;

case kDeviceMotion:

shipPosition.x += input.deviceMotion.pitch * kShipSpeed;

shipPosition.y += input.deviceMotion.roll * kShipSpeed;

break;

default:

break;

}

ship.position = shipPosition;

}

[/cc]

The touches and gesture recognizer functionality will be added to KKInput in the next version. Except it to be just as easy-peasy, yet powerful - the trademark-sign of the Kobold2D API.

#### LOG_EXPR: Logging in Perfection

You may find the macro **LOG_EXPR(variable)** to be very useful - I surely do! I use it all the time because its so much easier and less error prone than using CCLOG or NSLog. LOG_EXPR simply prints out the contents of the variable in a readable format - including the code within the brackets - without having to specify a format string:

[cc lang=”cpp”]

// old-school, tiresome way of logging stuff

CCLOG(@”ship.position = %f, %f”, ship.position.x, ship.position.y);

CCLOG(@”ship boundingBox = %f, %f, %f, %,”,

[ship boundingBox].origin.x, [ship boundingBox].origin.y

[ship boundingBox].size.width, [ship boundingBox].size.height);

CCLOG(@”ship.texture = %@”, ship.texture);

// logging the exact same variables with LOG_EXPR

LOG_EXPR(ship.position);

LOG_EXPR([ship boundingBox]);

LOG_EXPR(ship.texture);

// LOG_EXPR output is automatically & neatly formatted.

// Notice how [ship boundingBox] is exactly what was passed to LOG_EXPR:

ship.position = {240, 160}

[ship boundingBox] = {{176, 128}, {128, 64}}

ship.texture =

[/cc]

LOG_EXPR was created by Dave Dribin and improved by [Vincent Gable](http://vgable.com/blog/tag/log_expr/), then adapted to Kobold2D and ported to Mac.

#### Improved Mac Support

The Mac templates now use the entire window (the gray bar at the bottom is gone) and the Mac window size now correctly takes the window’s title bar into account. Previously the window height was about 24 pixels less tall than it should have been.

The Mac projects now have the KKApplicationMac class set as their principal application class, to allow Kobold2D to provide default functionality. The KKApplicationMac class overrides sendEvent to ensure that the Mac window receives “key up” events while the Command key is held down. This is a [workaround for what seems to be an AppKit bug](http://www.cocoadev.com/index.pl?GameKeyboardHandlingAlmost).

Btw, autoscaling for Mac windows is now disabled by default because it causes various “freak” errors like artifacts and incorrectly scaled content every now and then.

#### Misc Bits

Next to various fixes related to project settings, the biggest changes are the included iSimulate 1.5 Lite ([adds Video-Streaming support](http://www.vimov.com/isimulate/update/)) and preliminary compatibility with Xcode 4.2 and iOS 5 beta. With “preliminary” I mean that Kobold2D projects compile with Xcode 4.2 / iOS 5 beta and run, but they haven’t been thoroughly tested and remain unsupported until iOS 5 is officially available.

The project templates have also been overhauled to correctly precompile the Box2D headers (if you need them).

There are also several internal changes which I hope alleviate the “ld: file not found … libkobold2d-ios.a” linker error some users are getting. The Strict Selector Matching warning has been turned off by default since it’s causing too many false alarms.

For the complete list of changes please refer to the [Kobold2D Preview 4 release notes](http://www.kobold2d.com/x/3wYO).

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] Kobold2D Preview 4 now available! […]