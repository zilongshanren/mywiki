---
title: 'KoboldTouch: MVC Wrapper For Cocos2D'
url: http://www.learn-cocos2d.com/2012/10/koboldtouch-mvc-wrapper-cocos2d/
author: Toni Sala says
published: '2012-10-04'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Here’s what I’m working on. Hopefully this answers the questions I’ve been getting, in particular those about KoboldScript. And what’s happening with it, when is it coming, when can we stop using Corona SDK, etc.

Well then, let’s start with …

### KoboldTouch

*Huh, what?*

Well, the short answer is: KoboldTouch is an [MVC](https://en.wikipedia.org/wiki/Model–view–controller) wrapper around Cocos2D.

The long answer … let me start by saying that Cocos2D is *suboptimal*. From a code architecture point of view. Cocos2D has no concept of structure besides views (nodes), and doesn’t encourage structure in your own code. It happily lets users subclass views in order to add data and game logic.

I can’t stop but feel helpless to see beginners learning the things we’ve abandoned 20 years ago as bad practice. Yet Cocos2D code is written by subclassing views as if it were the most natural thing to do. It’s also the very thing Apple tells you **not** to do.

The result are projects lacking in what is called [separation of concerns](http://www.aurelienribon.com/blog/2011/04/logic-vs-render-separation-of-concerns/). It’s not just about experience. Without a clear architectural model frequently reminding you to consider separation of concerns, anyone is more likely to end up creating a blend of design patterns at best, [or worse:](http://joostdevblog.blogspot.de/2012/05/programming-with-pasta.html)


Even with good intentions at the beginning my own projects often devolved over time to a greater degree than I would have liked or imagined. Unfortunately KoboldScript is one of the victims.

I created it as an extension of Cocos2D by subclassing CCScene and CCNode. I didn’t like it, yet it seemed the only possible way at the time. But it created a huge problem: a user can easily, and simply by habit, bypass the KoboldScript extensions and run methods on the super classes.

*Terrible things happening. Trains crashing. Cute kittens dying in vain. Mothers-In-Law visiting.*

I could have enforced policy - which would have meant unlearning how Cocos2D works. I don’t want to force developers to re-learn Cocos2D. I also wanted to encourage Cocos2D developers to [stop needlessly subclassing view nodes for game code](http://stackoverflow.com/a/12643938/201863).

**But how?**

Unhappy with that situation, even though KoboldScript in itself is fairly complete, made me put it away and think about fixing this fundamental issue. It took me a while to realize the solution is already out there.

#### Why isn’t MVC employed more in game engines?

[This very question](http://gamedev.stackexchange.com/questions/3426/why-are-mvc-tdd-not-employed-more-in-game-architecture) kickstarted a thought process.

I’ve heard users ask about Cocos2D + MVC before and rather frequently too. I’ve read the few tutorials that exist but none convinced me, they seemed “tacked on”. MVC is certainly something developers are interested in learning or using, specifically if you have a background in Cocoa. But MVC didn’t seem to apply to Cocos2D, or does it?

The breakthrough revelation was to think of Cocos2D as the view and nothing else. Yes, Cocos2D brings along baggage like caching, input, actions, scheduling and so on, but put that away and it’s a 2D hierarchical rendering engine with animation support. Not unlike UIKit.

So I began evaluating how exactly MVC could be applied to Cocos2D. From that thought process the mindmap to the right came to be. It’s already been superseded by the actual implementation.

Right now, I’d say most of you are writing the game code inside subclassed node objects. That’s the Cocoa Touch equivalent of *subclassing a UIButton in order to directly update the text that’s in your subclassed UITextField object*.

**It really sounds scary if you think about it that way!**

Let’s put an end to that! One of the goals of KoboldTouch is to make changing these old habits a natural, easy, straightforward, wishing you’d have had always done it like this and wondering how it ever worked before kind of process. But still using Cocos2D as you know it, as the views inside a larger MVC framework.

*(cue epic music)*

#### KoboldTouch Architecture

My attempt at adding the missing Model-Controller link to the Cocos2D views is KoboldTouch. It’s a hierarchy of controllers plus an optional model for each controller, where the Cocos2D views (nodes) are encapsulated and managed by view controllers.

Among other things this solves the issue of [accessing other nodes in the hierarchy](http://www.learn-cocos2d.com/2012/09/strategies-accessing-cocos2d-nodes-scene-hierarchy/), avoiding (or at least detecting) retain cycles, and having a global game and multiple scene controllers to access global functionality and global data without having to stuff these things into numerous Singleton objects.

The architecture is very modular and plugin-capable. If you need Game Center, you add the GameCenterController. If you need sprite batching, you add your SpriteViewControllers to a SpriteBatchViewController. If you need physics, you add the PhysicsController and specify the physics engine. I already have a simple wrapper for Box2D going, which is pure Objective-C and has a few tricks, like allowing you to add/destroy bodies during the contact callback method!

This works so well, I’m still amazed. Everything just seems to be falling into place naturally. I really felt stupid not having thought about it that way before. It also made me wonder why hasn’t anyone else?

KoboldTouch has the following benefits:

- Whenever possible, follows UIKit naming conventions. For example,
*viewDidLoad*instead of*onEnter*(huh?) or*viewWillDisappear*instead of*onExitTransitionDidStart*(huh?). - Every controller has a quick access to its parent, the scene and the game controller. Accessing a global controller is always within reach:
*self.gameController.audioController*or*self.sceneViewController.physicsController*. - View controllers can register themselves by name on the scene controller. Other controllers can then request a registered controller by name or class. Controllers can easily establish one-to-one relationships. Your boss’s minion controllers need a reference to the boss controller? No problem!
- Since retain cycles are a very real threat in any hierachical code architecture, the game controller verifies that the most recently replaced scene controller did actually deallocate. If not, it shoves it right in your face. The sooner you know it, the easier it’ll be to fix.
- Each controller can have an optional model object, using them comes naturally. But you can also write all the code in the controller. Such a “ModelController” is a viable alternative for simple things, small apps, prototypes and the occasional lazy bean approach. 😉
- View controllers receive the
*viewWillLoad*,*viewDidLoad*,*viewWillDisappear*and*viewDidDisappear*messages to run setup and cleanup code. Models also receive load and unload methods. You almost never have to write any code in the init method. It’s all geared towards lazy initialization. - Xcode Class Templates for KoboldTouch will allow you to quickly create the Controller and Model source files, one or both.
- Controllers and models automatically run beforeStep, step and afterStep methods when implemented. No (un)scheduling required. To create an interval, simply set the
*nextStep*property to the step number the step methods should run the next time. - Both controllers and models can be paused, also pausing the step methods of sub controllers. You can pause/resume individual layers, and pausing the scene controller also pauses cocos2d (director pause), whereas pausing the game controller will stop cocos2d altogether (director stopAnimation).
- You do not necessarily have to subclass view controllers. You can use a standard view controller, and pass in a LoadViewBlock to create the nodes for the view when it loads, and assign a model object for the views’ logic and data.
- Because of the standardized controller hierarchy, sharing controller classes is straightforward. Just add the code, create the controller object and start using it! I’m going to rewrite my GameKitHelper singleton as the GameCenterController.
- Models support NSCoding. You can save your models, then when presenting the scene load the saved model data back in. When carefully designed, there’s no need to archive either controllers or views (cocos2d nodes).

On the right you can see an actual KoboldTouch example with a scene containing a menu and sprite-batched physics-animated sprites, initialized with blocks. ![Screen Shot 2012-09-30 at 12.04.51](../../../wordpress/wp-content/uploads/Screen-Shot-2012-09-30-at-12.04.51-286x300.png)


One thing of note is that you write the view setup code **before** presenting the scene.

KoboldTouch is built with ARC, minimum targets are iOS 5.0 and Mac OS X 10.7. This enables the use of zeroing weak references, which make a couple things easier and some possible in the first place. Weak references are a small feature yet extremely helpful in designing a framework like KoboldTouch.

Here’s the preliminary, [work-in-progress API reference for KoboldTouch](http://www.learn-cocos2d.com/api-ref/KoboldTouch/html/index/).

#### Where does KoboldScript fit in?

Coming full circle, KoboldTouch reinvigorates KoboldScript development, with some alterations. KoboldScript has two goals: making it easier to design the node hierarchy (human readable and tool-friendly file format) and scripting game logic.

![Kobold Touch MVC Architecture](../../../wordpress/wp-content/uploads/Kobold-Touch-MVC-Architecture.png)


The view part would be similar to the LoadViewBlock, allowing you to define a branch of the node hierarchy in Lua, then feeding this as input to a ScriptViewController. Minus the part where it runs any logic. It’s primarily settings for the view: which type of view node, where, which image, what color, what text, which view controller class, which script to run, and so forth. Init parameters and properties are direct translations of the Cocos2D class interfaces, thanks to a parser and code generator tool I’ve already written.

Said ScriptViewController would also have a ScriptModel, which would then forward the step, setup and cleanup methods to regular Lua functions residing in a specific Lua script, exposing the model’s interface to Lua. Lua can set and get variables in the model, using KVC for custom variables and direct access for already existing properties.

Scripts only interact with the model, they do not directly interact with the view. If, for example, you need the player sprite to change color after eating a mushroom, you’d have to program that part in the ScriptViewController. This is still beneficial since the bulk of game code is game logic, not view logic. And that glue code requires little effort, and can often even be generalized.

#### How does KoboldScript compare to … ?

KoboldScript will [differ from other Lua game engines](http://www.learn-cocos2d.com/2011/08/comparison-lua-scripting-corona-sdk-wax-kobold2d/) like Corona, and Cocos2D’s approach at developing a unified Javascript API. KoboldScript will help setup the view and will help implement game logic. To avoid misunderstandings:

*KoboldScript will not enable you to write a game entirely in Lua. It will not attempt to expose the entire Cocos2D API. It can not be any more cross-platform than Cocos2D already is (iOS + Mac).*

It will be easy to work with and extend - that’s priority #1!

### All Rolled Into Essential Cocos2D

![paperbackstack_small](../../../wordpress/wp-content/uploads/paperbackstack_small.png)


Sometime in the **second half of October** I will launch [ Essential Cocos2D](http://www.learn-cocos2d.com/2012/09/coming-learn-cocos2d-2-essential-cocos2d/), the Cocos2D reference documentation project.

I’ll be writing one or more reference articles every week, based on your suggestions and votes. And I’ll answer your Cocos2D related questions, just [like I do on stackoverflow.com](http://stackoverflow.com/users/201863/learncocos2d?tab=answers&sort=votes) but more often and more thorough.

To sweeten the deal I will also give you access to the **KoboldTouch** project, so you can give it a spin and help guide its development in the right direction. I find it important to see how you’re actually going to use it, to learn what I can improve and what needs fixing.

Once KoboldTouch has matured somewhat I’ll add **KoboldScript** to the mix!

**Essential Cocos2D** is not just Cocos2D reference documentation anymore. It will also include a new Cocos2D development paradigm and the support to help you get started running. You can be part of it from the beginning, help me accomplish these goals and at the same time become a better developer and learn best practices.

Stay tuned! Watch this blog for updates and [follow me on Twitter](https://twitter.com/intent/follow?original_referer=http%3A%2F%2Fwww.learn-cocos2d.com%2F2012%2F10%2Fkoboldtouch-mvc-wrapper-cocos2d%2F%3Fpreview%3Dtrue%26preview_id%3D5758%26preview_nonce%3Dba620bbc56®ion=follow_link&screen_name=gaminghorror&source=followbutton&variant=2.0).

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I’ve been playing around with MVC and cocos2d during the last year. And I also reached the conclusion that you should see cocos2d as only being the View part of the MVC. This is the key aspect.

However, my solution is not so sophisticated as yours :p I have stated some “rules” and “constrains” when working with cocos2d, trying to use the “render” functionality of cocos only on view classes and the logic functionality on model and controller classes. So, for instance:

- “CCSprite can only be used on view classes”

- “the ccp() macro and its variations can be used everywhere”

- “Model classes can be subclasses of CCNode to be able to use cocos2d logic functionality but the previous rules and constrains must be taken into account”

- etc.

I even wrote a document with this kind of rules :p Obviously, this “solution” is only useful for me and the people I work with. It is very difficult to keep attached to all the rules and every now and then you make some little exceptions :p

On the other hand, during the last 2 or 3 months I have been using Kobold2d for my next iOS game (Muster my Monsters http://indiedevstories.com/games/muster-my-monsters/) and I must admit that it’s really amazing. Good job!

So you know, I can’t wait for KoboldTouch to be released 😉

Thanks for your hard work!!

I worked with the “CCNode subclass as controller/model” approach for the past two years. It was always a crutch solution because you somehow had to add some kind of node to the scene in order to run scheduled updates and so on. But as you said, the problems come with those “exceptions”, quick hacks, lazy code, or just not thinking about it. Then things start falling apart, slowly but surely.

Quite interesting reading, man. Although your Xcode color scheme burns my eyes. 😀

I think I will try Kobold2D in future projects.

I’m a hippie coder. I like my code colorful.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I will be more than happy to move my project to KoboldTouch but… why the target is 5.0?! There is no way to bring it down a little, let’s say to a 4.0/4.3 at least? There are dozens of people that don’t give a crap about updating their devices but they are still huge target audience.

Dozens of people against millions? I think that case is self-evident.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


The news I read tell a clear picture that iOS 4 is hardly relevant today. The argument for supporting older iOS versions is not really sound either, just because there’s potentially more devices doesn’t mean you’re actually increasing your potential market. And to test iOS 4 support you have to have a device still running iOS 4.x since the iOS 4.x Simulator is no longer available.

Here’s a few good reads on the subject:

March 2012: 80% iOS 5 adoption rate with iOS 6 adoption rate

Oct 2012: 60% iOS 6 adoption rate (iPad has less, but that’s because of iPad 1)

Stackoverflow: Should I support < iOS 5? (some of Apple’s own apps require iOS 5)

Matt Gemmell: Great Argument for Supporting Only the Latest Version

Please also consider that KoboldTouch is just starting, this year it’s mainly for bleeding edge developers and those who “support the cause”. I don’t expect a notable number of games made with KT to be released before Q2 2013. And typically the users who don’t upgrade don’t buy new apps anyway. Matt Gemmell makes a good argument there.

Why I chose iOS 5? The reason is mainly weak references. It’s amazing how this little feature helps with framework development. Without it, I would have run much more frequently into retain cycles and leaking memory (from my experience building a similar system). The lesser reason is that you (and I) have to worry no more about an OS version that’s almost extinct (minus the devices that can’t upgrade to iOS 5 - but those aren’t supported by cocos2d 2.0 anyway) and can take iOS 5 features for granted.

Going forward I think it’ll make sense to upgrade the minimum target with every iOS release, so that generally only the dominant two OS versions are being supported. Imagine if iOS 7 were released today I would probably release a new version within 3-6 months using new iOS 7 features (but still supporting iOS 6) and number it KoboldTouch 7.0. Users who are on KT 5.x or 6.x will still get important updates and compatibility fixes and can decide for themselves if they want to upgrade now or complete their project on KT 5 before starting the next with KT 7.

I generally like the idea of numbering releasing to match the current iOS version.

[…] KoboldTouch: MVC Wrapper For Cocos2D The Development Plan for KoboldTouch […]