---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_action/
published: '2013-06-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.koboldtouch.com developers
|

`#import <CCAction.h>`


| (id) | -
|

| (id) | +
|

|

| id |
|

| + (id) action |

Allocates and initializes the action

| - (void) startWithTarget: | (id) | target |

called every frame with its delta time. DON'T override unless you know what you are doing.

| - (void) stop |

called after the action has finished. It will set the 'target' to nil. IMPORTANT: You should never call "[action stop]" manually. Instead, use: "[target stopAction:action];"

called once per frame. time a value between 0 and 1 For example:

Implemented in [CCDelayTime](http://www.learn-cocos2d.com/#aaa5640c9e87dcb73cf94dca6fe104d04), [CCFadeIn](http://www.learn-cocos2d.com/#a0804c9113f29c407ea182b58a477653e), [CCFadeOut](http://www.learn-cocos2d.com/#a6440214d38d77a79a971db6eb0760162), [CCEaseElasticIn](http://www.learn-cocos2d.com/#abea6af2a0240a45f15a81a09b9e454c1), [CCEaseElasticOut](http://www.learn-cocos2d.com/#a069b3fce533cd8ef4cfd5e7be3e805cb), [CCEaseElasticInOut](http://www.learn-cocos2d.com/#abb2ba1b2ee7d9691b7211d494a9b98fd), [CCEaseBounceIn](http://www.learn-cocos2d.com/#a8cebc9959536ec089b95d67577c7f85a), [CCEaseBounceOut](http://www.learn-cocos2d.com/#abdf721ee69ca6fe70171005d911ea0bb), [CCEaseBounceInOut](http://www.learn-cocos2d.com/#a06f5153e2ebb51fdd619670fa6b9a8e7), [CCEaseBackIn](http://www.learn-cocos2d.com/#a53b77d4e1c03578cdfc3245ebb1bbee1), [CCEaseBackOut](http://www.learn-cocos2d.com/#a16251a93e5e880967a9d684de561775d), [CCEaseBackInOut](http://www.learn-cocos2d.com/#ab51c7ffcd14a89520fbef572796930dd), [CCShow](http://www.learn-cocos2d.com/#ac717d18ab28fc7a473b1e0bf4b1f5b32), [CCHide](http://www.learn-cocos2d.com/#a8725141a1e3bee9dceb2d66fe7ef23a9), [CCToggleVisibility](http://www.learn-cocos2d.com/#ab70b05c8c66c0393919395aeb8e1a157), [CCPageTurn3D](http://www.learn-cocos2d.com/#ae1e2f4edae32203dd5776b2948b85ba2), [CCEaseIn](http://www.learn-cocos2d.com/#aff18692a06ac70b5a5f5ec5fb272bf2c), [CCEaseOut](http://www.learn-cocos2d.com/#a93043577059639678d3dcfee09736c37), [CCEaseInOut](http://www.learn-cocos2d.com/#ac514b0cef1f54314940bc00ae2a254a2), [CCEaseExponentialIn](http://www.learn-cocos2d.com/#af3bc4d09bcd537868b53a33ee1bfc342), [CCEaseExponentialOut](http://www.learn-cocos2d.com/#a47842dd3cbfdb4360b8597517f1131b8), [CCEaseExponentialInOut](http://www.learn-cocos2d.com/#a8342f02e1d0678b0f4c8377a5b2de1be), [CCEaseSineIn](http://www.learn-cocos2d.com/#a786c99d69bd0b1de52ef1bcc6a44109d), [CCEaseSineOut](http://www.learn-cocos2d.com/#a5ceb9465c34739755403ed5457887df5), [CCEaseSineInOut](http://www.learn-cocos2d.com/#a14d22c8e48c0fbc167ce1d9927dfefd4), and [CCFlipY3D](http://www.learn-cocos2d.com/#a66602435f5d1a7372eab7ee69b9849cb).

|
readnonatomicassign |

The original target, since target can be nil. Is the target that were used to run the action. Unless you are doing something complex, like [CCActionManager](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_action_manager/), you should NOT call this method.

|
readwritenonatomicassign |

The action tag. An identifier of the action

|
readnonatomicassign |

The "target". The action will modify the target properties. The target will be set with the 'startWithTarget' method. When the 'stop' method is called, target will be set to nil. The target is 'assigned', it is not 'retained'.