---
title: Scheduling multiple update selectors
url: http://www.learn-cocos2d.com/2011/03/scheduling-multiple-update-selectors/
author: The Ultimate Cocos; Learn; Master Cocos
published: '2011-03-02'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I have a seemingly simple requirement for my project: each node should have preUpdate and postUpdate methods in addition to the regular update method. Preprocessing and postprocessing before and after all entities have run their “update” logic is a common requirement in game development. Sometimes called the setup stage before processing all entities in the world, and the finalize stage to complete the current game step and possibly resolve collisions or check any win, lose or achievements conditions.

Of course there are alternative and some may argue “better” implementations, after all an experienced game dev might argue that using pre and post update methods are merely signs of a badly designed game update loop (the jury is out on that one). However beginning game developers definitely understand this concept much better and every game-making tool I know implements pre and post updates, so it has its validity. Plus I find it more convenient than “outsourcing” some logic to a central game loop.

On the other hand it’s also bad practice to rely on one node’s update method to be called before or after all others. Especially once you get to prioritizing update method calls among various groups of nodes it’s just going to get you into trouble. If you set the priority wrong just once you can introduce very subtle issues that’ll be hard to track down. Think of some objects not colliding with the player, or some monsters crashing when you shoot at them with a specific weapon. Scheduled methods should **never** rely on the order they are called for various entities.

#### Not so easy …

It turns out the system in Cocos2D only allows one update method per node. That means for each node you can only have one update selector, and via the priority parameter you can only control when its update method is called relative to all other nodes’ update method. In that way you can at least ensure that the player’s update method is always called first, or last, depending on your requirements. But it’s bad programming practice to do so.

I thought, why not just schedule a “regular” selector with CCScheduler? Well, they don’t have a priority, and they are always called after any update method, so you could never schedule a “before update” method this way. And those scheduled selectors aren’t meant to be used for selectors that are called every frame due to the additional processing overhead (eg allocating, updating and releasing the CCTimer object, and comparing & updating time elapsed every frame).

So I had to write a class called ScheduleMultiUpdate which creates proxy instances, registers them with CCScheduler to receive an update message of their own, and then they forward that message to the actual node implementing the special update selector. By using the priority you can define if the selector is called before or after the regular update by using a negative (before) respectively a positive priority (after, must be 1 or greater).

#### Example Code

Here’s an example usage scheduling the beforeUpdate and afterUpdate selectors to be called before and after the regular update method.

[cc lang=”ObjC” height=”550″]

// in interface (.h)

KKScheduleMultiUpdate* multiUpdate;

// in implementation (.m)

-(void) scheduleUpdateMethods

{

multiUpdate = [[KKScheduleMultiUpdate alloc] initWithNode:self];

[multiUpdate scheduleUpdateSelector:@selector(beforeUpdate:) priority:-1];

[self scheduleUpdateWithPriority:priority];

[multiUpdate scheduleUpdateSelector:@selector(afterUpdate:) priority:1];

}

// this has to be cleanup because CCScheduler retains scheduled targets

// we have to give KKScheduleMultiUpdate a chance to unschedule its selectors or it won’t be deallocated

-(void) cleanup

{

[multiUpdate release];

multiUpdate = nil;

[super cleanup];

}

-(void) beforeUpdate:(ccTime)delta

{

}

-(void) update:(ccTime)delta

{

}

-(void) afterUpdate:(ccTime)delta

{

}

[/cc]

Here’s the actual implementation of KKScheduleMultiUpdate and its proxy class. Notice how the KKScheduleMultiUpdate simply retains a list of proxies and creates new ones, while the proxy class registers itself with CCScheduler to schedule its own update method based on the given priority, and then forwards the message to the baseNode. There’s currently no way to unschedule an update selector, but it should be fairly easy to add if you ever need to unschedule an update method while the game is running (I’d rather just use a bool and skip update).

##### @interface

[cc lang=”ObjC” height=”500″]

#import “cocos2d.h”

/** Allows you to schedule multiple update methods per node. */

@interface KKScheduleMultiUpdate : NSObject

{

CCNode* baseNode;

CCArray* updateProxies;

}

-(id) initWithNode:(CCNode*)node;

-(void) scheduleUpdateSelector:(SEL)selector priority:(int)priority;

@end

/** Since there can be only one update selector scheduled per instance, this proxy will implement

that update method and forward the message to the desired selector. */

@interface KKScheduleMultiUpdateProxy : NSObject

{

id target;

SEL selector;

TICK_IMP impMethod;

}

-(id) initWithTarget:(id)target selector:(SEL)selector priority:(int)priority;

@end

[/cc]

##### @implementation

[cc lang=”ObjC” height=”500″]

#import “KKScheduleMultiUpdate.h”

@implementation KKScheduleMultiUpdate

-(id) initWithNode:(CCNode*)node

{

if ((self = [super init]))

{

NSAssert(node != nil, @”%@ %@ - node is nil!”, NSStringFromClass([self class]), NSStringFromSelector(_cmd));

baseNode = [node retain];

updateProxies = [[CCArray alloc] initWithCapacity:1];

}

return self;

}

-(void) dealloc

{

CCLOG(@”%@ %@”, NSStringFromSelector(_cmd), self);

[baseNode release];

baseNode = nil;

// must do a cleanup to unschedule CCSelector, this is because CCScheduler retains scheduled targets

[updateProxies makeObjectsPerformSelector:@selector(cleanup)];

[updateProxies release];

updateProxies = nil;

NSAssert([self retainCount] == 1, @”%@ %@ - retainCount on cleanup should be 1 but is %i”, NSStringFromClass([self class]), NSStringFromSelector(_cmd), [self retainCount]);

[super dealloc];

}

-(void) scheduleUpdateSelector:(SEL)selector priority:(int)priority

{

NSAssert([baseNode respondsToSelector:selector], @”%@ %@ - node %@ does not respond to selector”, NSStringFromClass([self class]), NSStringFromSelector(_cmd), baseNode);

// TODO: might want to check here if the selector happens to be already scheduled

KKScheduleMultiUpdateProxy* proxy = [[KKScheduleMultiUpdateProxy alloc] initWithTarget:baseNode selector:selector priority:priority];

[updateProxies addObject:proxy];

[proxy release];

}

@end

@implementation KKScheduleMultiUpdateProxy

-(id) initWithTarget:(id)target_ selector:(SEL)selector_ priority:(int)priority

{

if ((self = [super init]))

{

NSAssert(target_ != nil, @”target is nil”);

NSAssert(selector_ != nil, @”selector is nil”);

target = target_; // weak ref

selector = selector_; // weak ref

impMethod = (TICK_IMP)[target methodForSelector:selector];

NSAssert(impMethod != nil, @”selector is not an instance method of target %@”, target);

[[CCScheduler sharedScheduler] scheduleUpdateForTarget:self priority:priority paused:NO];

}

return self;

}

-(void) cleanup

{

CCLOG(@”%@ %@”, NSStringFromSelector(_cmd), self);

[[CCScheduler sharedScheduler] unscheduleUpdateForTarget:self];

impMethod = nil;

NSAssert([self retainCount] == 1, @”%@ %@ - retainCount after cleanup should be 1 but is %i”, NSStringFromClass([self class]), NSStringFromSelector(_cmd), [self retainCount]);

}

-(void) dealloc

{

CCLOG(@”%@ %@”, NSStringFromSelector(_cmd), self);

[super dealloc];

}

-(void) update:(ccTime)delta

{

impMethod(target, selector, delta);

}

@end

[/cc]

As always, you’re free to use this code. I release it under the [MIT License](http://creativecommons.org/licenses/MIT/). You do not need to include a copyright notice, but I’d appreciate any mention or backlink to this website.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] Scheduling multiple update selectors […]

Steffen - Could you possible shed some light on a CCScheduler issue?

When scheduling methods it seems as though the method gets called about a hundredth of a second after I would have expected it each time. This doesn’t become a noticeable problem until it repeats for some time, but the hundredths of a second add up quickly. An example of this would be if you were to schedule a method to be called in 7 seconds using

[self schedule:@selector(someMethod) interval:7]

…The first time it gets called may be 7.04 seconds in, but the second time would get called at 14.05 seconds in and then at 21.06 seconds in. As I said it’s not a problem until it runs about 45 times, and the difference in time varies.

Have you experienced this, or know of a fix, or is it simply just inherent in using the scheduler? Thanks!

I don’t know about the CCScheduler accuracy but it’s commonplace to see slight variations with timers in general. It depends on the resolution of the implementation and of course the framerate. If your game renders 30 fps the granularity of the scheduler should be 0.03 seconds. If you have noticable hiccups in framerate (eg some frames take a significant time to render, for example 0.2 seconds) the inaccuracy will be even higher.

Each time a scheduled method is called, the time is reset. So if you see it take 7.04 seconds on the first call, and 14.05 in the second it means the second time it was actually more precise (14.05 - 7.04 = 7.01).