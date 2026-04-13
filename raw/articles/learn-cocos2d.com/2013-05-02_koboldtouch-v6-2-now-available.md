---
title: KoboldTouch v6.2 now available!
url: http://www.learn-cocos2d.com/2013/05/6679/
author: Kurt says
published: '2013-05-02'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[KoboldTouch](http://www.koboldtouch.com/) v6.2 marks the third major milestone for KoboldTouch. It also marks the longest development cycle between two updates: exactly 30 days.

That’s 30 days packed with new features, improvements and bugfixes, there’s a [new development blog](http://www.koboldtouch.com/x/YwCC) for the work-in-progress “Angry Trains” starterkit and slowly but surely the [documentation is coming together](http://www.koboldtouch.com/x/MgCC).

So let’s check out the **exciting new features in KoboldTouch v6.2**:

### Objective-C Box2D Physics wrapper

The Objective-C wrapper for Box2D (aka “Boxjective2D”) is now in a state that I feel very comfortable with. And proud. It’s the only Box2D Objective-C wrapper that’s both fairly complete **and** supported **and** will be continuously improved. It’s also stable, super-slick and easy to use, highly efficient without compromising integrity (ie no @private vars) and you can always access the underlying Box2D objects.

The **following Box2D components are wrapped in Objective-C classes**, which is about 80% of the public API of Box2D (and I won’t stop there):


- b2World -> KTPhysicsController
- b2Body & b2BodyDef -> KTPhysicsBody
- b2Fixture & b2FixtureDef -> KTPhysicsFixture
- b2Shape & b2ShapeDef -> KTPhysicsShape
- b2Joint & b2JointDef -> KTPhysicsJoint (implemented: friction, distance, revolute, mouse - rest are coming soon, they’re easy to add)
- b2ContactListener -> KTPhysicsBodyContactDelegate protocol
- b2Contact -> KTPhysicsContact
- GLESDebugDraw -> KTPhysicsDebugViewController

I mainly need to add the remaining joint types, and I’ll add the manifold and contact impulse or any other classes when requested or when needed for the train game. Most of the classes and methods are fairly straightforward to wrap now that the Objective-C physics framework is in place, so please do make requests if something’s amiss.

Also, it’s worth mentioning **there are a couple extra goodies in “Boxjective2D”** that you don’t get out of the box(2d):

- Can destroy bodies during contact callbacks. Yup, you read that right!
- All coordinates are in points! Pixels-To-Meter conversions happen entirely behind the scenes!
- Work with contact categories & groups by name.
[Bitwise operations](http://stackoverflow.com/questions/47981/how-do-you-set-clear-and-toggle-a-single-bit-in-c)are entirely optional! - Built-in support for PhysicsEditor shapes & fixtures (GB2ShapeCache also wrapped).
- Slow-motion effect by changing the physics world’s time scale.
- Create the “world bounding box” with a single line of code.
- No “def” classes. The same physics class’ properties are used both pre-init and post-init.
- Your physics code will be in .m files, since it’s Objective-C!

You can see what it’s like to work with “Boxjective2D” in this coding demo:

### Skeletal Animations with Spine

With KTSpineViewController you can conveniently use the [Kickstarter-backed skeletal animation tool Spine](http://esotericsoftware.com/) in your projects, or rather its export files.

I incorporated the **brand new, much improved Spine runtime** that’s ARC compatible and “more like Objective-C”. Yes, there was a shitstorm. I hope they don’t get this %§#$! for each of their 13 spine-runtime variants (Corona, libgdx, Löve, …). Though of course I’m all in favor for more and better Objective-C code whenever possible.

So should there still be something about the Spine runtime not to your liking, you can now subclass the KTSpineViewController and easily make your own front-end to the Spine runtime without needing to rewrite everything from scratch.

A video says more about Spine than a thousand pictures (actually a thousand pictures is about a 33 second video at 30 fps, so… this one doesn’t quite cut it):

### Train Game Starterkit & Development Blog

Many of the features, various improvements and bugfixes included in v6.2 came from actually using KoboldTouch to make a **game and starter kit** - a feature the KoboldTouch users voted for.

One of the things I might not have done otherwise (so soon) is to change the way KoboldTouch initializes objects. Initially I wanted to incorporate lazy initialization, but alas that was difficult to achieve and it proved counter-intuitive. This became very obvious after writing some actual game code. **You just can’t beat dogfood!**

Since the game at this stage is mainly a prototype and far from an actual starterkit, I decided to make up for it by [frequently posting to the Angry Trains development diary](http://www.koboldtouch.com/x/YwCC) and showcasing progress with screenshots and videos. Here’s the latest development video, with cargo on the cars and a slow-motion effect:

### Removing the Crust

You know what makes programmers intuitively feel that a piece of code is crap?

**Inconsistencies!**

Code that *may only look like* it wasn’t crafted with care. Reading such code feels like reading a book that suddenly changes font style mid-sentence for now apparent reason. Yuk!

Since KoboldTouch uses several 3rd party libraries I wanted to combat this effect (and for my own sake of course). Thus all the source code in KoboldTouch is now f**requently beautified** with

[uncrustify](http://uncrustify.sourceforge.net/). Now it’s as if all of the code in KoboldTouch had been crafted by a single, excruciatingly disciplined individual. That’s what makes automated code formatting so sweet.

And before you ask: no, your own code isn’t going to be touched. Unless that’s something you’d like…? Let me know, post a comment.

### Cocoa View Controller

The KTCocoaViewController is **similar to CCUIViewWrapper**, but does its job more efficiently and it also works on Mac OS X with NSView objects.

Again another series of pictures drives the issue home, and it shows the benefits of separating views from models and controllers. **Any view can be animated by physics, including UIViews!**

### Any Model, Any View, Anything for You!

Speaking of which: You can now use the base class KTViewController and combine it with any node and any model object. This means you can now use any custom node class without having to write a custom KTViewController subclass.

I also made the create/load blocks optional that used to be required to init/setup models and cocos2d nodes (views). In the near future I intend to phase out the create/load blocks entirely. You can now do just what you would expect: assign a model to the model property, assign a cocos2d node to the rootNode property of a KTViewController.

And KT customers will also enjoy the various reported bugs I fixed and improvements I made from your suggestions. [You’ll find them in the change log](https://www.learn-cocos2d.com/api-ref/CHANGELOG-KoboldTouch.txt).

### Check out KoboldTouch

If you found something in this post you liked about KoboldTouch, then [go check it out](http://www.koboldtouch.com/)!

Or [go straight to the store](http://www.koboldtouch.com/) to see what it costs to code with the pros. (Hint: really not that much!)

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hey Steffen,

A couple questions if you wouldnt mind answering them for me.

1) What is the difference between Kobold Touch and Kobold2D?

2) With the objective - c, box2d wrapper, does that come with Kobold Touch? Or can i purchase it all alone?

Thanks a bunch!

Kurt

More details here: http://www.koboldtouch.com/x/64Bq

The Objective-C Box2D physics engine wrapper is not available separately.