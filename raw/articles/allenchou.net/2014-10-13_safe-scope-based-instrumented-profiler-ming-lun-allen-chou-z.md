---
title: Safe Scope-Based Instrumented Profiler | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2014/10/safe-scope-based-instrumented-profiler/
author: Allen Chou
published: '2014-10-13'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Programming Series](http://allenchou.net/game-programming-series/).

Let’s say we have an interface for an instrumented profiling library that looks like this:

namespace Profiler { void BeginBlock(const char *name); void EndBlock(void); };

The argument you pass to `BeginBlock`

is a custom block name for you to identify the block in the profiler output.

You call `BeginBlock`

at the beginning of a block of code and call `EndBlock`

when the program exits the block.

void GameLoop(void) { Profile::BeginBlock("GameLoop"); UpdateInput(); UpdatePhysics(); UpdateLogic(); Render(); Profile::EndBlock(); }

Let’s say you also inserted the proper calls to the profiling functions inside the functions you wish to profile, then the profiler might give you an output like this:

GameLoop - 16.0ms // 60fps, woo~ |--UpdateInput - 1.0ms |--UpdatePhysics - 10.0ms | |--InitRigidBodies - 0.1ms | |--SolveConstraints - 0.6ms | |--IntegrateRigidBodies - 0.3ms |--UpdateLogic - 5.0ms

This all depends on the fact that you properly call the `EndBlock`

function before the program exits a block of code. What if, say, someone decides to throw in an early-out inside one of your functions and forgets to call `EndBlock`

?


void MyFunction(void) { Profile::BeginBlock("MyFunction"); // 1000 lines of code if (someCondition) { // whoops return; } // 1000 lines of code Profile::EndBlock(); }

If you’ve read my previous post about [scope-based resource management](http://allenchou.net/2014/10/scope-based-resource-management-raii/), then you can probably already tell what I’m leading up to. We can let the compiler insert proper code that calls `EndBlock`

for us at the exit points of a block of code, making use of the constructor and destructor of a helper object on the stack.

Here’s our helper class:

class ProfilerBlock { public: ProfilerBlock(const char *name) { Profiler::PushBlock(file); } ~ProfilerBlock(void) { Profiler::EndBlock(); } }; // helper macro that generates an object name #define PROFILER_BLOCK(name) \ ProfilerBlock profiler_##name##(name)

Our function now becomes:

void MyFunction(void) { PROFILE_BLOCK("MyFunction"); // 1000 lines of code if (someCondition) { // PopBlock automatically called here return; } // 1000 lines of code // PopBlock automatically called here }

Now we have a safe scope-based instrumented profiler!

You know you can use a __func__ identifier to get the function name in C++11 right?

Yes, I do. However, the approach shown here allows you to specify custom name for a profiler block that is not necessarily the same as the function name. So you can have nested profiler blocks within a single function with descriptive names.