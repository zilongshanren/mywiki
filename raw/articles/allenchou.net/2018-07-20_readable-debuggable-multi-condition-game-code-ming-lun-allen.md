---
title: Readable & Debuggable Multi-Condition Game Code | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2018/07/readable-debuggable-multi-condition-game-code/
author: Allen Chou
published: '2018-07-20'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Programming Series](http://allenchou.net/game-programming-series/).

Over time, I have adopted several coding patterns for writing readable and debuggable multi-condition game code, which I systematically follow.

By multi-condition code, I’m talking about code where certain final logic is executed, after multiple condition tests have successfully passed; also, if a test fails, further tests will be skipped for efficiency, effectively achieving [short-circuit evaluation](https://en.wikipedia.org/wiki/Short-circuit_evaluation).

**NOTE:** I only mean to use this post to share some coding patterns I find useful, and I do NOT intend to suggest nor claim that they are “the only correct ways” to write code. Also, please note that it’s not all black and white. I don’t advocate unconditionally adhering to these patterns; I sometimes mix them with opposite patterns if it makes more sense and makes code more readable.

**Shortcuts:**

[Early Outs](https://allenchou.net#early-outs)

[Debuggable Conditions](https://allenchou.net#debuggable-conditions)

[Debug Draw Locality](https://allenchou.net#debug-draw-locality)

[Forcing All Debug Draws](https://allenchou.net#forcing-all-debug-draws)


### Early Outs

There are two ends of spectrum regarding this subject, **early outs** versus **single point of return**. Both camps have pretty valid arguments, but I lean more towards the early-out camp. The early-out style is the foundation of all the patterns presented in this post.

As an example, consider the scenario where we need to test if a character is facing the right direction, if the weapon is ready, and if the path is clear, before finally executing an attack.

This is one way to write it:

FacingData facingData = PrepareFacingData(); if (TestFacing(facingData)) { WeaponData weaponData = PrepareWeaponData(); if (TestWeaponReady(weaponData)) { PathData pathData = PareparePathData(); if (TestPathClear(pathData)) { Attack(); } } }

The code block above is written in the so-called **single-point-of-return** style. The logic flow is straightforward and always ends at the bottom of the code block. If the code block is wrapped inside a function, the function will have one single point of return, i.e. at the bottom of the function:

void TryAttack() { FacingData facingData = PrepareFacingData(); if (TestFacing(facingData)) { WeaponData weaponData = PrepareWeaponData(); if (TestWeaponReady(weaponData)) { PathData pathData = PareparePathData(); if (TestPathClear(pathData)) { Attack(); } } } // return here }

The same logic in **early-out** style would look something like this, returning right where the first test fails:

void TryAttack() { FacingData facingData = PrepareFacingData(); if (!TestFacing(facingData)) return; WeaponData weaponData = PrepareWeaponData(); if (!TestWeaponReady(weaponData)) return; PathData pathData = PareparePathData(); if (!TestPathClear(pathData)) return; Attack(); }

I like this style better, because the intent to get out of the function right after the first failing test is very clear. Also, as the number of tests get large, it avoids excessive indentation, which many jokingly call “indent hadouken.”

PHP Streetfighter 🙂

[#php][pic.twitter.com/5dQ5H1UrB2]Paul Dragoonis (@dr4goonis)

[June 11, 2014]

Early outs don’t just apply to functions. They apply to loops as well. For example, this is how I would iterate through characters and collect those who can attack:

for (Characer &c : characters) { FacingData facingData = ParepareFacingData(c); if (!TestFacing(facingData)) continue; WeaponData weaponData = PrepareWeaponData(c); if (!TestWeaponReady(weaponData)) continue; PathData pathData = PareparePathData(c); if (!TestPathClear(pathData)) continue; charactersWhoCanAttack.Add(c); }

One special case where early out is not quite possible without refactoring, is that if there’s more code that must always be executed after the condition tests.

In the single-point-of-return style, it may look like this:

void TryAttack() { FacingData facingData = PrepareFacingData(); if (TestFacing(facingData)) { WeaponData weaponData = PrepareWeaponData(); if (TestWeaponReady(weaponData)) { PathData pathData = PareparePathData(); if (TestPathClear(pathData)) { Attack(); } } } // always execute PostAttackTry(); }

But using the early-out style, we’d have a problem:

void TryAttack() { FacingData facingData = PrepareFacingData(); if (!TestFacing(facingData)) return; WeaponData weaponData = PrepareWeaponData(); if (!TestWeaponReady(weaponData)) return; PathData pathData = PareparePathData(); if (!TestPathClear(pathData)) return; Attack(); // Uh, oh. Not always executed! PostAttackTry(); }

If you’re comfortable with using forward-only `goto`

s to jump to the `PostAttackTry`

call and your team’s coding standards allow it, then you’re set. Otherwise, we need to keep looking for solutions.

What about calling `PostAttackTry`

wherever the function returns?

void TryAttack() { FacingData facingData = PrepareFacingData(); if (!TestFacing(facingData)) { PostAttackTry(); return; } WeaponData weaponData = PrepareWeaponData(); if (!TestWeaponReady(weaponData)) { PostAttackTry(); return; } PathData pathData = PareparePathData(); if (!TestPathClear(pathData)) { PostAttackTry(); return; } Attack(); PostAttackTry(); }

This is also not good. The moment someone adds a new return while forgetting to also add a call to `PostAttackTry`

, the logic breaks.

In this case, if the logic is trivial, I’d be okay with just using the single-point-of-return style. Otherwise, I would refactor the tests into a separate function, while maintaining the early-out style:

bool CanAttack() { FacingData facingData = PrepareFacingData(); if (!TestFacing(facingData)) return false; WeaponData weaponData = PrepareWeaponData(); if (!TestWeaponReady(weaponData)) return false; PathData pathData = PareparePathData(); if (!TestPathClear(pathData)) return false; return true; } void TryAttack() { if (CanAttack()) Attack(); PostAttackTry(); }

[EDIT]

I’ve received feedback proposing the use of destructors of some helper class to invoke the final logic, a la [scope-based resource management (RAII)](http://allenchou.net/2014/10/scope-based-resource-management-raii/).

For me, the acceptable instances that rely on destructors like this are scoped-based resource management, [profiler instrumentation](http://allenchou.net/2014/10/safe-scope-based-instrumented-profiler/), and whatever logic that comes in the form of a tightly coupled “entry” and “exit” logic pairs, but not this.

In my acceptable cases, an exit logic is ensured to always accompany its corresponding entry logic, taking burden off programmers by preventing them from accidentally exiting a scope without executing the exit logic.

I think relying on destructors to execute arbitrary logic upon scope exit that is not coupled with an entry logic induces unnecessary complexity and risk of omittance. When reading the code, instead of making a mental note of “something is executed here, and the accompanying exiting logic will be executed upon scope exit”, the readers now have to remember that “nothing is done yet, and only when the scope is exited will something happen.” To me, the latter is a mental burden that is more likely to be omitted, because it’s not tied to any concrete logic execution right at the code location where the helper struct is constructed.

[/EDIT]

### Debuggable Conditions

Continuing using the character attack example from above, let’s consider the scenario where each test function now returns a results struct that contains a success flag indicating whether the test has passed, as well as extra info gathered from the test that is useful for debugging purposes.

This is what the code might look like:

void TryAttack() { FacingData facingData = PrepareFacingData(); if (!TestFacing(facingData).IsFacingValid()) return; WeaponData weaponData = PrepareWeaponData(); if (!TestWeaponReady(weaponData).IsWeaponReady()) return; PathData pathData = PareparePathData(); if (!TestPathClear(pathData).IsPathClear()) return; Attack(); }

It looks good and all, but there’s one specific issue that technically doesn’t lie in the code itself, but it affects the programmer’s experience when debugging this piece of code.

Embedding the test function’s return value within `if`

conditions like this, means that if we want to set a break point and peek inside the extra info in the results structs, we’d have to step into the individual tests, step out of the tests, and then look at the returned value.

[Visual Studio](https://visualstudio.microsoft.com/) supports this feature inside the [autos window](https://docs.microsoft.com/en-us/visualstudio/debugger/autos-and-locals-windows):

![](../../assets/26392154790a44fa.png)


I find it slightly annoying to have to step in and then step out of test functions, just to inspect their results results structs. So, I normally assign the return values to local variables, and then perform `if`

checks on those variables instead.

This way, I can just step over the test function calls and inspect the results structs, without having to step in and out of the test functions:

void TryAttack() { FacingData facingData = PrepareFacingData(); FacingResults facingResults = TestFacing(facingData); if (!facingResults.IsFacingValid()) return; WeaponData weaponData = PrepareWeaponData(); WeaponResults weaponResults = TestWeaponReady(weaponData); if (!weaponResults.IsWeaponReady()) return; PathData pathData = PareparePathData(); PathResults pathResults = TestPathClear(pathData); if (!pathResults.IsPathClear()) return; Attack(); }

Even if we’ve stepped past some tests, extra info regarding the tests is still available in the [locals window](https://docs.microsoft.com/en-us/visualstudio/debugger/autos-and-locals-windows), which is a convenience I now cannot live without:

![](../../assets/7773adbeaa2352f4.png)


As a side note, if the test is just a trivial expression, I think embedding it in the `if`

condition is totally fine, and it can actually make the code cleaner.

### Debug Draw Locality

**NOTE:** For simplicity’s sake, code mechanisms to effectively strip debug draws in release build is omitted in this post (e.g. `#ifdef`

s, macros, flags, etc.).

Sometimes we need to debug draw based on test results, to show why a test succeeded or failed. That’s what the results structs returned from test functions are for.

I like to keep debug draw code close to the related condition tests, if not inside the test function themselves. In my opinion, this makes the code cleaner and easier to read in independent chunks.

It’s perfectly fine if leaving certain debug draw logic inside the test functions themselves makes more sense. However, there are cases where drastically different debug draws are desired at different call sites of the test functions.

My experience tells me that it’s not possible to anticipate how others will use test results for their own debug draws, so I usually put trivial or common debug draw logic inside the test functions, and leave use-case specific debug draw logic to the client code calling the test functions. In the attack example, the `TryAttack`

function body is considered client code that uses the test functions.

I generally follow this pattern:

void TryAttack() { // facing FacingData facingData = PrepareFacingData(); FacingResults facingResults = TestFacing(facingData); if (facingResults.IsFacingValid()) { DebugDrawFacingSuccess(facingResults.GetSuccessInfo()); } else { DebugDrawFacingFailure(facingResults.GetFailureInfo()); return; } // weapon WeaponData weaponData = PrepareWeaponData(); WeaponResults weaponResults = TestWeaponReady(weaponData); if (weaponResults.IsWeaponReady()) { DebugDrawWeaponSuccess(weaponResults.GetSuccessInfo()); } else { DebugDrawWeaponFailure(weaponResults.GetFailureInfo()); return; } // path PathData pathData = PareparePathData(); PathResults pathResults = TestPathClear(pathData); if (pathResults.IsPathClear()) { DebugDrawPathSuccess(pathResults.GetSuccessInfo()); } else { DebugDrawPathFailure(pathResults.GetFailureInfo()); return; } // final logic Attack(); }

This pattern is, again, in the early-out style.

If we use the single-point-of-return style, the code above can turn into this:

void TryAttack() { FacingData facingData = PrepareFacingData(); FacingResults facingResults = TestFacing(facingData); if (facingResults.IsFacingValid()) { DebugDrawFacingSuccess(facingResults.GetSuccessInfo()); WeaponData weaponData = PrepareWeaponData(); WeaponResults weaponResults = TestWeaponReady(weaponData); if (weaponResults.IsWeaponReady()) { DebugDrawWeaponSuccess(weaponResults.GetSuccessInfo()); PathData pathData = PareparePathData(); PathResults pathResults = TestPathClear(pathData); if (pathResults.IsPathClear()) { DebugDrawPathSuccess(pathResults.GetSuccessInfo()); } else { DebugDrawPathFailure(pathResults.GetFailureInfo()); } } else { DebugDrawWeaponFailure(weaponResults.GetFailureInfo()); } } else { DebugDrawFacingFailure(facingResults.GetFailureInfo()); } Attack(); }

The call to `DebugDrawFacingFailure`

is all the way down inside the bottom `else`

block. This is bad in terms of code locality. When I see the call to `DebugDrawFacingFailure`

at the end, I’d have to trace all the way up to find its corresponding condition test.

There are single-point-of-return alternatives that can improve debug draw locality, but it’s still always going to be a challenge to make clean cuts to separate code into chunks that fully contain reference to individual tests. Later test chunks will always need to reference earlier test results.

### Forcing All Debug Draws

Sometimes it’s preferable to force debug draws for all test results, even when early tests fail. In this case, we don’t care about the effect of short-circuit evaluation any more.

This is the pattern I follow that adds a flag to force all debug draws, which in turn could be toggled by a debug option:

void TryAttack(bool forceAllDebugDraws) { bool anyTestFailed = false; // facing const FacingResults facingResults = TestFacing(); if (facingResults.IsFacingValid()) { DebugDrawFacingSuccess(facingResults.GetSuccessInfo()); } else { DebugDrawFacingFailure(facingResults.GetFailureInfo()); anyTestFailed = true; if (!forceAllDebugDraws) return; } // weapon const WeaponResults weaponResults = TestWeaponReady(); if (weaponResults.IsWeaponReady()) { DebugDrawWeaponSuccess(weaponResults.GetSuccessInfo()); } else { DebugDrawWeaponFailure(weaponResults.GetFailureInfo()); anyTestFailed = true; if (!forceAllDebugDraws) return; } // path const PathResults pathResults = TestPathClear(); if (pathResults.IsPathClear()) { DebugDrawPathSuccess(pathResults.GetSuccessInfo()); } else { DebugDrawPathFailure(pathResults.GetFailureInfo()); anyTestFailed = true; if (!forceAllDebugDraws) return; } // we'd only get here if total debug draw is forced // don't perform attack if any test has failed if (anyTestFailed) return; // final logic Attack(); }

If the flag to force all debug draws is set to true, all condition tests as well as debug draws will be executed. But the final `Attack`

function call still wouldn’t be reached, because it’s guarded by a flag keeping track of whether any test has failed.

You might have already foreseen that if the number of tests grow large, we can end up having a lot of duplicate code and logic structure, respectively the use of `anyTestFailed`

& `forceAllDebugDraws`

inside the `else`

blocks, and `if`

statements branching into calling success & failure debug draws.

If you’re willing to make a sacrifice to prepare a single master data struct at the start, which is to be passed into all test functions declared with the same signature, plus a master results struct that holds all test info for debug draws, here’s one alternative pattern for your consideration:

// these are C++ function pointers // if you're using C#, think of them as delegates bool (* TestFunc) (const Data &data, Results &results); bool (* DebugDrawFunc) (const Results &results); struct TestSpec { TestFunc m_func; DebugDrawFunc m_debugDrawSuccess; DebugDrawFunc m_debugDrawFailure; }; void TryAttack(bool forceAllDebugDraws) { bool anyTestFailed = false; // define sets of test function and debug draw functions TestFuncSpec testFuncs[] = { { // facing TestFacing, DebugDrawFacingSuccess, DebugDrawFacingFailure }, { // weapon TestWeaponReady, DebugDrawWeaponSuccess, DebugDrawWeaponFailure }, { // path TestPathClear, DebugDrawPathSuccess, DebugDrawPathFailure } } // iterate through each test Data masterData = PrepareMasterData(); Results masterResults; bool anyTestFailed = false; for (TestFuncSpec &spec : testFuncs) { bool success = spec.m_func(masterData, masterResults); if (success) { spec.m_debugDrawSuccess(masterResults); } else { spec.m_debugrRawFailure(masterResults); anyTestFailed = true; if (!forceAllDebugDraws) return; } } if (anyTestFailed) return; Attack(); }

When a new test function and its success & failure debug draw functions are defined, simply add the function set to the `testFuncs`

array. There is only one shared code structure (the range-based `for`

loop) that runs the tests, selects the success or failure debug draw functions to call, and optionally performs early outs.

Finally, if the length of the `TryAttack`

function grows to a point where the purpose of the function is not trivially clear any more. Recall a refactored variation above where all the condition tests are extracted into a separate `CanAttack`

function:

void TryAttack() { if (CanAttack()) Attack(); PostAttackTry(); }

This seems like a good change no matter how the conditional tests are done, as it makes the intention of `TryAttack`

crystal clear to the reader. I’d do this if readability is compromised due to function length.

### Summary

That’s it! I’ve shared the coding patterns I think help make code readable and debuggable.

Using the early-out style as foundation, I’ve shown how to write debuggable conditions, achieve debug draw locality, and optionally force all debug draws.

I don’t consider these patterns exciting nor groundbreaking, but I find them very useful, and I hope you do, too.

I’ve hit this situation before and the early out issue is that cleanup code can change and replicating it is problematic. I found using a do{…}while(0) loop cleans this up nicely.

I use this extensively and once you get used to the non-looping do while, it seems to keep the right balance between readability and code complexity/replication

Ah, yes. I heard from a friend that they’ve used this pattern extensively in their code base. I use it in my personal projects sometimes, but at work it’s against our coding standard as they consider it a thinly-veiled go-to equivalent. I think using go-to’s to get out and to the end of a scope is fine, but I also get that sometimes people think it’s better to be safe than sorry by banning the use of it in a code base maintained by a huge number of people.

For PostAttackTry(), C++ has a trick called “scope guard” which can run specific tasks when leaving a scope. I’m not sure whether there is anything similarly in C#.

I was considering including that pattern in the post, but decided not to. My reason is that no matter where you put it inside the scope, it wouldn’t be as readable as scope-based resource management, even though they utilize destructors in the same way.

If it’s put at the beginning of the scope, the backward instruction jump is not immediately obvious to readers who are not used to this pattern (even if they are familiar with scope-based resource management). If it’s put at the end of the scope, the readers would not become aware of the extra function call unless they read the whole block.

I would recommend against using this pattern for the readers’ sake.

Fair enough. In my team, I always encourage my colleagues to use this pattern as it can help avoid early return mistakes of resource management.

FILE* f = fopen();

ON_SCOPE_EXIT(fclose(f));

And once I get used to the pattern, I get when resources are released immediately because it is just next to the statement of allocation. But in this case, it could be a different story.

Right. In your example, it’s about resource management (files, locks, etc.), so that’s actually preferable. My peers and I do that as well.

I was talking more about non-resource management cases, where the program hinges on arbitrary logic being executed when a scope is exited. My concern is that this is not a common practice and most users are not used to it and thus would not take notice of it.

好棒的技巧！學習了！