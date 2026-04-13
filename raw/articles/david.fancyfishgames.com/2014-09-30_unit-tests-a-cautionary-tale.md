---
title: Unit Tests - A Cautionary Tale
url: http://david.fancyfishgames.com/2014/09/unit-tests-cautionary-tale.html
author: Legend
published: '2014-09-30'
source_blog: The Legend of GameDev
source_site: http://david.fancyfishgames.com/
category: graphics
fetched: '2026-04-13'
---

*are*useful and can save a lot of time, headache and debugging. So even if you're like me, you should still consider when it might be a good idea to add unit tests.

First off, what are unit tests? Unit tests are where you literally write code to test a section or function of your code. As a quick example, the following function:

`function square(x){return x*x;}`


Might have the following unit tests:```
assert square(5) == 25; //Normal case, 5 squared should be 25.
assert square(-4) == 16; //Negatives, -4 squared should be 16.
assert square(0) == 0; //Edge case, 0 squared should be 0.
```


This tests the function with a few inputs to ensure it has the right output. If all of the unit tests are successful, than you can assume the function is more or less correct. Later on in development, you can run the tests again to make sure that it is still correct (and that nobody messed up that bit of code).Now you might see why I hate unit tests. They can be very tedious, and typically only work for small, deterministic functions where it's pretty obvious that it works anyways. However, the idea of using a bit of code to test a much larger and more complex section of code is pretty appealing. Instead of having to test and debug output by hand countless times to make sure it's not broken or to track down a bug, you can simply run the test and hopefully find bugs before you even release the game to testers.

Of course, as I hate unit tests, I didn't originally write any for my current game, I Can't Escape: Darkness. However, a month or so ago I made a small change to the procedural generation code of the game to add a new feature. The change was small and I didn't think it would affect any of the other code. Checking the procedurally generated layout by hand many times, everything seemed to be in working order. But that's one of the downsides of procedural generation - since it is random, there can be bugs that don't appear in the majority of generations. This is exactly what that small change did - it broke an assumption from an earlier bit of the generation code that, in a very rare case, would allow a section of the map that should've been reachable to be attached to an unreachable section (instead of attaching it to a reachable section so that the player could actually get there). A month later, a team member was playing the game, and noticed that he couldn't find an essential button he needed to progress in the game. He was stuck, and looking at the generated layout, it turned out that the button could not be pressed as it was spawned down an unreachable corridor. Oops!

I'm sure you've all encountered problems and bugs like this, and some of them can be very game-breaking like this one was. Worried that other game-breaking bugs might exist and tired of manually checking generated layouts by hand, I finally decided to add a unit test. However, I didn't add small unit tests checking each function to make sure that all the parts of the whole work. What I did was one large unit test that checked the integrity of the procedural generation as a whole (and the procedural generation section in I Can't Escape: Darkness is big - about 40 classes and 200 functions). That is the kind of unit test I view as beneficial in game development - one that checks a large section that IS changed a lot, and takes less time to code than to manually check.

The unit test I have now does higher level checks like this:

```
assert canEnter("vwm", "lr3"); //You should be able to enter vwm from lr3.
assert canEnter ("cr3", "vwm"); //You should be able to enter cr3 from vwm.
assert !canEnter ("cr3", "lr3"); //You should NOT be able to enter cr3 from lr3 without first going through vwm.
```


Where cr3, lr3 and vwm are codenames for rooms, events and areas that are generated (which I will not explain so as not to spoil what you can find in I Can't Escape: Darkness).These checks use basic pathfinding, and there are a lot of them that do the same kinds of checks I would do by eye. It ensures that all of the buttons, events and rooms are reachable, and that there are no holes in the maze that let you reach sections that you shouldn't be able to reach (without first hitting a button to open a door or exiting an event). Yes, this took some time to write and is more complex than "normal" unit tests, but it is infinitely more useful. Now, I can run this test 1,000 times or 10,000 times, and even though some bugs may be rare with procedural generation, this test has a much higher chance to catch bugs than I do by hand. This does what unit tests were really meant to - ensure that everything is working properly and saving time.

As a quick caution, I'll mention that you should be careful your unit testing code is simple to limit the chance that it itself has bugs. There's nothing more useless than a buggy unit test that misses errors, and nothing sillier than having to write unit tests for your unit tests! The test I wrote uses hand-written checks that only relies on a pathfinder that I've used many times before and am very confident that it works without bugs. Don't write a unit test that is so complex it breaks more often than it correctly checks your code.

To conclude, I think that you should start considering where in your code a unit test would be beneficial, preferably before someone else finds a game breaking bug. You'll still need to do plenty of testing and debugging by hand, but a good unit test can save you (and others) a lot of time and headache. Whenever you find yourself having to check something often (like the generated map layouts in I Can't Escape: Darkness), ask yourself whether you could automate the process with a unit test. If you can automate it, it's not too complex and it will save you time, then it might be a good idea to write a unit test. Unit tests

*can*be useful - just don't waste your time writing unit tests for functions like square!

## No comments:

## Post a Comment