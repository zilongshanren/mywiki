---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_scheduler/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCScheduler.h>`


| void |
|

Scheduler is responsible of triggering the scheduled callbacks. You should not use NSTimer. Instead use this class.

There are 2 different types of callbacks (selectors):

The 'custom selectors' should be avoided when possible. It is faster, and consumes less memory to use the 'update selector'.

| BOOL CCScheduler::isTargetPaused: | ( | id | target | ) | ` [virtual]` |

Returns whether or not the target is paused

| void CCScheduler::pauseTarget: | ( | id | target | ) | ` [virtual]` |

Pauses the target. All scheduled selectors/update for a given target won't be 'ticked' until the target is resumed. If the target is not present, nothing happens.

| void CCScheduler::purgeSharedScheduler | ( | ) | ` [static, virtual]` |

purges the shared scheduler. It releases the retained instance.

| void CCScheduler::resumeTarget: | ( | id | target | ) | ` [virtual]` |

Resumes the target. The 'target' will be unpaused, so all schedule selectors/update will be 'ticked' again. If the target is not present, nothing happens.

| void CCScheduler::scheduleSelector:forTarget:interval:paused: | ( | SEL | selector, |
| [forTarget] id | target, |
||
| [interval]
|

` [virtual]`

The scheduled method will be called every 'interval' seconds. If paused is YES, then it won't be called until it is resumed. If 'interval' is 0, it will be called every frame, but if so, it recommened to use 'scheduleUpdateForTarget:' instead. If the selector is already scheduled, then only the interval parameter will be updated without re-scheduling it again.

| void CCScheduler::scheduleUpdateForTarget:priority:paused: | ( | id | target, |
| [priority] NSInteger | priority, |
||
| [paused] BOOL | paused |
||
| ) | ` [virtual]` |

Schedules the 'update' selector for a given target with a given priority. The 'update' selector will be called every frame. The lower the priority, the earlier it is called.

returns a shared instance of the Scheduler

'tick' the scheduler. You should NEVER call this method, unless you know what you are doing.

| void CCScheduler::unscheduleAllSelectors | ( | ) | ` [virtual]` |

Unschedules all selectors from all targets. You should NEVER call this method, unless you know what you are doing.

| void CCScheduler::unscheduleAllSelectorsForTarget: | ( | id | target | ) | ` [virtual]` |

Unschedules all selectors for a given target. This also includes the "update" selector.

| void CCScheduler::unscheduleSelector:forTarget: | ( | SEL | selector, |
| [forTarget] id | target |
||
| ) | ` [virtual]` |

Unshedules a selector for a given target. If you want to unschedule the "update", use unscheudleUpdateForTarget.

| void CCScheduler::unscheduleUpdateForTarget: | ( | id | target | ) | ` [virtual]` |

Unschedules the update selector for a given target

Modifies the time of all scheduled callbacks. You can use this property to create a 'slow motion' or 'fast fordward' effect. Default is 1.0. To create a 'slow motion' effect, use values below 1.0. To create a 'fast fordward' effect, use values higher than 1.0.