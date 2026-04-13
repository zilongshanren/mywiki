---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_scheduler/
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

| (void) | -
|

|

|

|

| - (BOOL) isTargetPaused: | (id) | target |

Returns whether or not the target is paused

| - (NSSet*) pauseAllTargets |

Pause all selectors and blocks from all targets. You should NEVER call this method, unless you know what you are doing.

| - (NSSet*) pauseAllTargetsWithMinPriority: | (NSInteger) | minPriority |

Pause all selectors and blocks from all targets with a minimum priority. You should only call this with kCCPriorityNonSystemMin or higher.

| - (void) pauseTarget: | (id) | target |

Pauses the target. All scheduled selectors/update for a given target won't be 'ticked' until the target is resumed. If the target is not present, nothing happens.

| - (void) resumeTarget: | (id) | target |

Resumes the target. The 'target' will be unpaused, so all schedule selectors/update will be 'ticked' again. If the target is not present, nothing happens.

| - (void) resumeTargets: | (NSSet *) | targetsToResume |

Resume selectors on a set of targets. This can be useful for undoing a call to pauseAllSelectors.

| - (void) scheduleBlockForKey: | (NSString *) | key |
|
| target: | (id) | target |
|
| interval: | (
|

The scheduled block will be called every 'interval' seconds. 'key' is a unique identifier of the block. Needed to unschedule the block or update its interval. 'target' is needed for all the method related to "target" like "pause" and "unschedule" If 'interval' is 0, it will be called every frame, but if so, it recommended to use 'scheduleUpdateForTarget:' instead. 'repeat' lets the action be repeated repeat + 1 times, use kCCRepeatForever to let the action run continuously. 'delay' is the amount of time the action will wait before it'll start. If paused is YES, then it won't be called until it is resumed. If the block is already scheduled, then only the interval parameter will be updated without re-scheduling it again.

| - (void) scheduleSelector: | (SEL) | selector |
|
| forTarget: | (id) | target |
|
| interval: | (
|

calls scheduleSelector with kCCRepeatForever and a 0 delay

| - (void) scheduleSelector: | (SEL) | selector |
|
| forTarget: | (id) | target |
|
| interval: | (
|

The scheduled method will be called every 'interval' seconds. If paused is YES, then it won't be called until it is resumed. If 'interval' is 0, it will be called every frame, but if so, it recommended to use 'scheduleUpdateForTarget:' instead. If the selector is already scheduled, then only the interval parameter will be updated without re-scheduling it again. repeat lets the action be repeated repeat + 1 times, use kCCRepeatForever to let the action run continuously delay is the amount of time the action will wait before it'll start

| - (void) scheduleUpdateForTarget: | (id) | target |
|
| priority: | (NSInteger) | priority |
|
| paused: | (BOOL) | paused |
|

Schedules the 'update' selector for a given target with a given priority. The 'update' selector will be called every frame. The lower the priority, the earlier it is called.

| - (void) unscheduleAll |

Unschedules all selectors and blocks from all targets. You should NEVER call this method, unless you know what you are doing.

| - (void) unscheduleAllForTarget: | (id) | target |

Unschedules all selectors and blocks for a given target. This also includes the "update" selector.

| - (void) unscheduleAllWithMinPriority: | (NSInteger) | minPriority |

Unschedules all selectors and blocks from all targets with a minimum priority. You should only call this with kCCPriorityNonSystemMin or higher.

| - (void) unscheduleBlockForKey: | (NSString *) | key |
|
| target: | (id) | target |
|

Unshedules a block for a given key / target pair. If you want to unschedule the "update", use unscheudleUpdateForTarget.

| - (void) unscheduleSelector: | (SEL) | selector |
|
| forTarget: | (id) | target |
|

Unshedules a selector for a given target. If you want to unschedule the "update", use unscheudleUpdateForTarget.

| - (void) unscheduleUpdateForTarget: | (id) | target |

Unschedules the update selector for a given target

'update' the scheduler. You should NEVER call this method, unless you know what you are doing.

|
readnonatomicassign |

Will pause / resume the [CCScheduler](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_scheduler/). It won't dispatch any message to any target/selector, block if it is paused.

The difference between `pauseAllTargets`

and `pause, is that`

setPaused`will pause the `

pauseAllTargets[CCScheduler](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_scheduler/), while`will pause all the targets, one by one. `

setPaused`will pause the whole Scheduler, meaning that calls to`

resumeTargets:`,`

resumeTarget:` won't affect it.

Modifies the time of all scheduled callbacks. You can use this property to create a 'slow motion' or 'fast forward' effect. Default is 1.0. To create a 'slow motion' effect, use values below 1.0. To create a 'fast forward' effect, use values higher than 1.0.