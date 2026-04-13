---
title: 'LearnCocosTV 5: Pretty State Machine'
url: http://www.learn-cocos2d.com/2012/02/4630/
author: Chad says
published: '2012-02-13'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

**KoboldScript** is coming! KoboldScript brings Lua scripting to Cocos2D and Kobold2D, with Objective-C performance for the [StateMachine](https://en.wikipedia.org/wiki/Finite-state_machine) part and faster-than-Wax performance for the runtime Lua functions.

More details and first looks at some early development scripts in this LearnCocosTV episode. I’ll have something more visual to show in 2-4 weeks.

##### Episode #5 - Pretty State Machine

• KoboldScript: Lua Scripting for Cocos2D & Kobold2D

o Poll: Which scripting language for Cocos2D?

o iDevBlogADay: Text Editors for Lua

• KoboldScript combines:

o Lua StateMachine generator (full ObjC performance)

o Runtime Lua functions (faster than Wax)


#### Very early KoboldScript sample script

```
testLuaFunctionParams = {
[1] = "one",
one = 1,
ones = 111,
wahr = true,
falsch = false,
counter = 0,
}
function conditionTestFunction(params)
params.counter = params.counter + 1
if (params.counter >= 166) then
params.counter = 0
return true
end
return false
end
function actionTestFunction(params)
print("AAAAACTION!!!!!!!!!!!!!!!!!!!!")
end
StateMachine
{
Name = "my Machine",
State
{
Name = "first State",
OneTimeEvent
{
Conditions
{
};
Actions
{
-- Objective-C style with named parameters ...
VariableAssign{Name = "my good var", Value = -123},
-- ... and shorter C-style can be used interchangeably!
VariableAssign("my evil var", 678),
TimerStart("ding-dong"),
DebugLogMessage("VERY FIRST STEP"),
StateMachineSetActiveState{Name = "2nd state"},
};
};
NonStopEvent
{
Conditions
{
LuaFunctionReturnsTrue{Function = "conditionTestFunction",
Table = "testLuaFunctionParams"},
};
Actions
{
DebugLogMessage{Message = "testLuaFunction SUCCESS"},
LuaFunctionExecute{Function = "actionTestFunction",
Table = "testLuaFunctionParams"},
};
};
NonStopEvent
{
Conditions
{
TimerIsElapsed{Name = "ding-dong",
Steps = secondsToSteps(10)},
};
Actions
{
DebugLogMessage{Message = "DING DONG DING DONG DING DONG"},
TimerStart("ding-dong"),
};
};
PeriodicEvent
{
IntervalSteps = secondsToSteps(0.5), -- check twice per second
Conditions
{
OR
{
TimerIsElapsed{Name = "ding-dong",
Steps = secondsToSteps(2)},
TimerIsElapsed{Name = "ding-dong",
Steps = secondsToSteps(5)},
};
};
Actions
{
DebugLogMessage("time passed ..."),
};
};
};
-- alternative style (if you prefer K&R style ... me? <shudders>)
State {
Name = "2nd state",
NonStopEvent {
Conditions {
TimerIsElapsed{Name = "ding-dong",
Steps = secondsToSteps(3)},
};
Actions {
StateMachineSetActiveState{Name = "first State"},
DebugLogMessage{Message = "... and back!"},
};
};
};
};
```


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I am really looking forward to KoboldScript. What a great feature!

Hey thanks for the video, gave me a ton of ideas and hints (especially the SWIG part) for my integration of lua into my app(s). If you combine this with the one of your earlier videos, (loading resources form server) it would mean no more compiling, well almost

I have done my own implementation to learn, otherwise I would definitely use your product.

KoboldScript will be awesome. 😀