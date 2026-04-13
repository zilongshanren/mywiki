---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_action/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Represents an action that can be performed on an object.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_o_a_l_action/#details)

`#include <OALAction.h>`


| id |
|

Represents an action that can be performed on an object.

| id OALAction::initWithDuration: | ( | float | duration | ) | ` [virtual]` |

Initialize an action.

| duration | The duration of this action in seconds. |

| void OALAction::prepareWithTarget: | ( | id | target | ) | ` [virtual]` |

Called by runWithTraget to do any final preparations before running.

Subclasses must ensure that duration is valid when this method returns.

| target | The target to run the action on. |

| void OALAction::runWithTarget: | ( | id | target | ) | ` [virtual]` |

Run this action on a target.

| target | The target to run the action on. |

| void OALAction::startAction | ( | ) | ` [virtual]` |

Called by runWithTarget to start the action running.

| void OALAction::stopAction | ( | ) | ` [virtual]` |

Stop this action.

| void OALAction::updateCompletion: | ( | float | proportionComplete | ) | ` [virtual]` |

float OALAction::duration` [read, assign]` |

The duration of the action, in seconds.

float OALAction::elapsed` [read, write, assign]` |

The amount of time that has elapsed for this action, in seconds.

bool OALAction::running` [read, assign]` |

If true, the action is currently running.

id OALAction::target` [read, assign]` |

The target to perform the action on.

WEAK REFERENCE.