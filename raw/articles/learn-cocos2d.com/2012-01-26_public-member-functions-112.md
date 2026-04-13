---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_call_func/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCActionInstant.h>`


| id |
|

Calls a 'callback'

| id CCCallFunc::actionWithTarget:selector: | ( | id | t, |
| [selector] SEL | s |
||
| ) | ` [static, virtual]` |

creates the action with the callback

| void CCCallFunc::execute | ( | ) | ` [virtual]` |

exeuctes the callback

| id CCCallFunc::initWithTarget:selector: | ( | id | t, |
| [selector] SEL | s |
||
| ) | ` [virtual]` |

initializes the action with the callback

id CCCallFunc::targetCallback` [read, write, retain]` |

Target that will be called