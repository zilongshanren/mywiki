---
title: Kobold2D v1.0 Preview 5 released!
url: http://www.learn-cocos2d.com/2011/10/kobold2d-v10-preview-5-released/
author: Jandujar Says
published: '2011-10-12'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

To put it in Apple’s words: [“Taking Cocos2D to a whole new level.”](http://www.apple.com/ios/) I can’t brag with 200+ new features though I have a few in store that should make a big bang for no bucks! 😀

So, here speaketh the market crier for [Kobold2D](http://www.kobold2d.com/). What’s new and noteworthy about this version of Kobold2D, you ask?

#### Built-In Gesture Recognition

Recognizing gestures has never been this easy. No (speak: **zero**) iOS SDK knowledge required! All gesture recognizers provided by the iOS SDK are implemented:

**Tap, Double-Tap, Long-Press, Swipe, Pan, Rotation and Pinch.**


Here’s how you would enable both rotate and pinch gestures simultaneously to provide a rotate & zoom action on a sprite:

[cc lang=”cpp”]

// enable recognizers once, ie in init method

KKInput* input = [KKInput sharedInput];

input.gestureRotationEnabled = YES;

input.gesturePinchEnabled = YES;

// update sprite direction & scale continuously, ie in update: method

KKInput* input = [KKInput sharedInput];

if (input.gestureRotationBegan)

{

aSprite.direction = input.gestureRotationAngle;

}

if (input.gesturePinchBegan)

{

aSprite.scale = input.gesturePinchScale;

}

[/cc]

Radians, degrees? Who gives a f#§$ if the angle is already in the format Cocos2D expects it to be, right? It doesn’t get any simpler and easier than this! Unless you live in a Star Trek world (hey, invite me in!).

Check out the [KKInput Gestures documentation](http://www.kobold2d.com/x/0wgO) for more details.

#### Also: “Did you just touch my Node???”

Touch and multi-touch input processing is now insanely simple:

[cc lang=”cpp”]

KKTouch* touch;

CCARRAY_FOREACH([KKInput sharedInput].touches, touch)

{

// do something with each touch here

aSprite.position = touch.location;

}

[/cc]

Notice how you don’t need to f#$§ing know how, when, or where to convert the touch locations. Touch locations are already converted to Cocos2D’s OpenGL view coordinates. Let alone the fact that you can work with touches anywhere, in any class and method. What you see here is a game engine doing what it is supposed to be doing: taking care of the things you shouldn’t need to concern yourself with.

**Speaking of which: **

What do you do if you want to know if a [touch was on a sprite](http://www.cocos2d-iphone.org/forum/topic/7303#post-43968)? Make it complicated, let’s assume the sprite is scaled and rotated. Hmmm … well, Kobold2D makes that mindlessly simple too:

[cc lang=”cpp”]

aSprite.scale = 1.23f;

aSprite.direction = 321;

KKTouch* touch;

CCARRAY_FOREACH([KKInput sharedInput].touches, touch)

{

if ([aSprite containsPoint:touch.location])

{

// it’s sooooo touching!

}

}

[/cc]

Read up on the more touchy-feely stuff in the [KKInput Touches documentation](http://www.kobold2d.com/x/tAgO).

#### Support for Core Motion and Gyroscope

KKInput gives you access to [DeviceMotion](http://www.kobold2d.com/x/_AgO) data in a similarly simple fashion. Device Motion is combined accelerometer and gyroscope input which, through [sensor fusion](https://en.wikipedia.org/wiki/Sensor_fusion), provides much better controls on devices that support it (4th generation, iPad 2). Again, no knowledge of the iOS Core Motion framework required. None at all.

Device Motion acceleration is already filtered into two components: user acceleration and gravity acceleration. You also get access to Euler angles (roll, pitch, yaw) to learn about the device’s orientation (attitude). And of course the gyroscope’s rotation rate.

[cc lang=”cpp”]

// turn on device motion input if available (ie in init method)

KKInput* input = [KKInput sharedInput];

input.deviceMotionActive = input.deviceMotionAvailable;

// get the sensor-fused acceleration values (ie in update: method)

float userAccelerationX = motion.acceleration.rawX;

float rotationRateY = motion.rotationRate.y;

CGPoint attitude = CGPointMake(motion.pitch, motion.roll);

[/cc]

Refer to the [KKInput Device Motion documentation](http://www.kobold2d.com/x/_AgO) for more details. Also have a look at the documentations for [KKInput Gyroscope](http://www.kobold2d.com/x/7AgO) and [KKInput Accelerometer](http://www.kobold2d.com/x/5AgO).

#### Google AdMob Banner Integration

Thanks to [Simon Jewell](http://blog.sygem.com/) who provided me with the initial [Google AdMob](http://www.admob.com/) implementation for Kobold2D, the Ad banner support got an overhaul.

You can now choose between iAd and AdMob as ad providers, and use AdMob as a fallback option on devices where iAd isn’t available. The entire configuration of ad banners is done in the config.lua file, no programming required!

[cc lang=”lua”]

EnableAdBanner = NO,

PlaceBannerOnBottom = YES,

LoadOnlyPortraitBanners = NO,

LoadOnlyLandscapeBanners = NO,

AdProviders = “iAd, AdMob”,

AdMobRefreshRate = 15,

AdMobPublisherID = “YOUR_ADMOB_PUBLISHER_ID”,

AdMobTestMode = YES,

[/cc]

Just get your app setup for iAd in iTunes Connect respectively obtain your AdMob publisher ID, and you’re ready to make some money from free apps! Since AdMob works on all devices, pays via PayPal, and doesn’t require the lengthy contract, tax and bank account setup that Apple does, it perfect for anyone who wants to see results (ie money) quick and easy. See the instructions in the [Ad Banner documentation](http://www.kobold2d.com/x/jQgO) for guidance on how to become an affiliate in the iAd and AdMob systems.

#### UIKit View Integration, with Hit Testing!

The second edition of my [Learn Cocos2D book](http://www.learn-cocos2d.com/store/book-learn-cocos2d/) has an entire Chapter dedicated to integrating UIKit views with Cocos2D (and also integrating Cocos2D to an existing UIKit app). One of the UIKit integration example projects from the book is now included in Kobold2D.

There’s a gem in that project: the UIKit views are both in front of and behind the Cocos2D OpenGL view. And if that weren’t enough, I’ve added a hit testing flag to config.lua and the Cocos2D OpenGL view so that touches are properly recognized by UIKit views and Cocos2D nodes, whether they’re in the foreground or in the background, whether they’re rotated or scaled.

#### Box2D v2.2.1 with updated Template Projects

Box2D has a new version that Kobold2D now uses. The [Box2D API](http://www.learn-cocos2d.com/api-ref/latest/Box2D/html/annotated/) changed a bit, but you can look up the necessary changes to world initialization, the GLESDebugDraw class, setting the screen bounding body, and other things in the Box2D and Pinball game template projects.

#### The No-Brainer: iOS 5 & Xcode 4.2 Compatibility

Kobold2D is now extensively tested with both Xcode 4.2 / iOS 5 and Xcode 4.1 / iOS 4.3. If you’re using Xcode 4.2 / iOS 5 you’ll automatically get the benefit of the new Apple LLVM 3.0 compiler. Note that LLVM 3.0 has an increased nagging level, and will issue compiler warnings and errors where there were none before. This is normal, and not Kobold2D’s fault.

#### FAQ: Common Issues, Simple Explanations

I realized that a nagging, inexplicable issue turned out to be nothing than an [old, die-hard habit](http://www.kobold2d.com/x/IQkO) of opening .xcodeproj files instead of .xcodeworkspace. Another common issue is [not changing the default scheme](http://www.kobold2d.com/x/SgYO) from “box2d-ios” to the actual project scheme. It’ll build but of course one can’t “run” the Box2D library by itself.

Kobold2D projects - as much as it pains me to say it as proponent of [warning-free code](http://www.artima.com/cppsource/codestandards.html) - now build successfully even if there are warnings in your projects. You complained, I caved i … err, I listened! 😀

#### What are you waiting for?

Head on over and download the latest (and last) [Kobold2D Preview 5](http://www.kobold2d.com/display/KKSITE/Kobold2D+Download). By “last” I mean that in about two weeks, when the second edition of Learn Cocos2D hopefully hits the streets, I will release the “official”, non-preview version 1.0 of Kobold2D.

If you run into any issues, need help or just want to talk about Kobold2D, please don’t hesitate to use the [Kobold2D forum](http://cocos2d-central.com/forum/50-kobold2d-for-ios-mac-os-x/). Likewise, if there’s something you’d love to see in Kobold2D, suggest it and/or vote on existing suggestions in the [Kobold2D Feedback area](http://www.kobold2d.com/display/KKSITE/Kobold2D+Feedback). Thank you for your time!

Of course I would highly appreciate it if you could help spread the word and click on those tweet, like and plus-one buttons. Here and in particular on the [Kobold2D website](http://www.kobold2d.com/). Thanks again!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

What an incredible upgrade!!!

I can’t wait to download preview 5 release and use this incredible features.

But I have a question, the project upgrader is compatible with snow leopard? or as the preview 4, needs a Lion installation to upgrade the projects. I don’t have lion installed yet.

It’s one of the things I fixed, so yes: the Upgrader tool is now working under Snow Leopard. I simply forgot to set the deployment target of the project to 10.6, there’s nothing Lion-specific in the tool.