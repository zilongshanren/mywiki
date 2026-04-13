---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/interface_c_c_scheduler/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.0
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

| (void) | -
|

Pause all selectors from all targets. You should NEVER call this method, unless you know what you are doing.

Pause all selectors from all targets with a minimum priority. You should only call this with kCCPriorityNonSystemMin or higher.

Pauses the target. All scheduled selectors/update for a given target won't be 'ticked' until the target is resumed. If the target is not present, nothing happens.

Resumes the target. The 'target' will be unpaused, so all schedule selectors/update will be 'ticked' again. If the target is not present, nothing happens.

Resume selectors on a set of targets. This can be useful for undoing a call to pauseAllSelectors.

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

The scheduled method will be called every 'interval' seconds. If paused is YES, then it won't be called until it is resumed. If 'interval' is 0, it will be called every frame, but if so, it recommened to use 'scheduleUpdateForTarget:' instead. If the selector is already scheduled, then only the interval parameter will be updated without re-scheduling it again. repeat let the action be repeated repeat + 1 times, use kCCRepeatForever to let the action run continiously delay is the amount of time the action will wait before it'll start

| - (void) scheduleUpdateForTarget: | (id) | target |
|
| priority: | (NSInteger) | priority |
|
| paused: | (BOOL) | paused |
|

Schedules the 'update' selector for a given target with a given priority. The 'update' selector will be called every frame. The lower the priority, the earlier it is called.

Unschedules all selectors from all targets. You should NEVER call this method, unless you know what you are doing.

Unschedules all selectors for a given target. This also includes the "update" selector.

Unschedules all selectors from all targets with a minimum priority. You should only call this with kCCPriorityNonSystemMin or higher.

| - (void) unscheduleSelector: | (SEL) | selector |
|
| forTarget: | (id) | target |
|

Unshedules a selector for a given target. If you want to unschedule the "update", use unscheudleUpdateForTarget.

Unschedules the update selector for a given target

'update' the scheduler. You should NEVER call this method, unless you know what you are doing.

Modifies the time of all scheduled callbacks. You can use this property to create a 'slow motion' or 'fast fordward' effect. Default is 1.0. To create a 'slow motion' effect, use values below 1.0. To create a 'fast fordward' effect, use values higher than 1.0.