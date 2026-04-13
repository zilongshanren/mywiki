---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_action/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCAction.h>`


| id |
|

| id CCAction::action | ( | ) | ` [static, virtual]` |

Allocates and initializes the action

| id CCAction::init | ( | ) | ` [virtual]` |

Initializes the action

| BOOL CCAction::isDone | ( | ) | ` [virtual]` |

| void CCAction::startWithTarget: | ( | id | target | ) | ` [virtual]` |

called before the action start. It will also set the target.

called every frame with it's delta time. DON'T override unless you know what you are doing.

| void CCAction::stop | ( | ) | ` [virtual]` |

called after the action has finished. It will set the 'target' to nil. IMPORTANT: You should never call "[action stop]" manually. Instead, use: "[target stopAction:action];"

called once per frame. time a value between 0 and 1 For example: 0 means that the action just started 0.5 means that the action is in the middle 1 means that the action is over

id CCAction::originalTarget` [read, assign]` |

The original target, since target can be nil. Is the target that were used to run the action. Unless you are doing something complex, like [CCActionManager](http://www.learn-cocos2d.com/), you should NOT call this method.

NSInteger CCAction::tag` [read, write, assign]` |

The action tag. An identifier of the action

id CCAction::target` [read, assign]` |

The "target". The action will modify the target properties. The target will be set with the 'startWithTarget' method. When the 'stop' method is called, target will be set to nil. The target is 'assigned', it is not 'retained'.