---
title: Not Ninjas, Just Programmers
url: https://tsherif.wordpress.com/2015/10/19/not-ninjas-just-programmers/
author: Tarek Sherif
published: '2015-10-19'
source_blog: Tarek Sherif
source_site: https://tsherif.wordpress.com
category: game programming
fetched: '2026-04-13'
---

var ninja = { sneakAround: function() {...}, strikeFromShadows: function() {...}, writeStableWebApp: function() {...} };

Terms like JavaScript ninja or JavaScript wizard tend to make me uneasy. They suggest a set of priorities in programming that I would argue are counterproductive. To begin discussing why, let’s refer to some definitions:

-
[ninja](http://dictionary.reference.com/browse/ninja)[nin-juh], noun: a member of a feudal Japanese society of mercenary agents, highly trained in martial arts and stealth (ninjutsu) who were hired for covert purposes ranging from espionage to sabotage and assassination. -
[wizard](http://dictionary.reference.com/browse/wizard)[wiz-erd], noun: a person who practices magic; magician or sorcerer.

I wouldn’t consider any of the qualities implied here as important, or even attractive, in software development. Why would anyone want code to be stealthy? Or covert? Or magic? Glorifying these qualities betrays an attitude that shifts focus away from the software we build to the cleverness of the code that’s used to build it. Exploiting syntactic idiosyncrasies in novel ways or displaying one’s knowledge of the esoteric details of a language takes priority over creating robust, maintainable applications. It’s programming as performance, rather than programming as craft.


## The Code is Not the Thing

To build robust software and have it remain viable in the long term, the priority must always be the application. That the code do what it does in a way that might impress fellow developers should simply not be of interest in any serious software development. The qualities we strive for in our code should be those that allow us to build software that does what it’s supposed to and does it well. In my own practice, those qualities would be the following, ordered by priority:

- Correctness
- Clarity
- Performance

While pursuing these qualities will involve all parts of the development workflow (design, automated testing, QA, deployment), I will focus here on the actual writing of code. The discussion will include a few examples of my own coding and workflow conventions that I believe help me build better software, along with the reasoning behind them. I want to make clear from the outset that I don’t believe these conventions are necessarily for everyone. They’re simply some that I’ve developed over the course of my career because they fit my programming sensibilities. My argument is certainly not that everyone should have the same conventions, but rather that everyone should have *some* conventions and that the primary consideration for choosing those conventions should be the quality of the software they help one create.

## Correctness

ninja.stumble = function() { this.beSneaky(); setTimeout(function() { this.writeStableWebApp(); }, 2000); };

Aside from the design of algorithms we use, correctness of code depends on avoiding errors in implementation. Bugs will always creep into software, it can’t be avoided, but the risk can be mitigated by choosing coding conventions that make it harder to introduce bugs and make it easier to track them down when they occur. Whether or not we agree with [Douglas Crockford](http://shop.oreilly.com/product/9780596517748.do) about what the “good parts” of JavaScript are, the principle of using the “good parts” of a language and avoiding the “bad parts” should be a part of everyone’s software development practice. For my own practice, this involves considerations like the following:

**Always**Mainly for the guarantee that it will prevent me from accidentally introducing global variables due to missing`"use strict"`

:`var`

s or binding of`this`

to the global context**Avoid**I hate having to remember to assign`this`

:`this`

to a variable when the function scope changes, so I tend to avoid it entirely if possible**Strict equality:**I don’t want my software to depend on my (or my team’s) recollection of JavaScript’s[coercion rules](http://webreflection.blogspot.com/2010/10/javascript-coercion-demystified.html). So for me, it’s strict equality everywhere.

## Clarity

Array.prototype.ninja = function() { return -Math.max.apply( Math, this.map(function(n) { return -n; }) ); };

Next to performing correctly, the most important role of our code is to communicate its purpose, both to ourselves and to others who might work on it. Code should be readable. This is useful in the initial writing of code in that it can help keep thoughts organized while working towards a solution. It’s *critical* for the long-term viability of software, particularly when it is developed by a team. The more difficult it is for a team to understand each other’s code, or for one to understand one’s own, the more likely it is that that understanding will be flawed and errors will be introduced.

Maintaining clarity, as with maintaining correctness, is about conventions. When working alone, one’s own criteria for clarity can be determined and conventions can be chosen accordingly. Developing conventions for a team is more complex in that it depends on formulating a mutually understood definition of clarity. In a team environment, my approach tends to be the following:

**Don’t be fancy:**This principle clashes most directly with the ninja/wizard coding ethos. If there’s a straightforward way to do something, just do it that way. Name everything descriptively. Be concise without being cryptic.**Define the team’s coding conventions:**Understanding one another’s code becomes much easier if there is consensus on which language patterns are being used and which are being explicitly avoided.**Accept your team’s coding conventions (even if they’re ill-defined):**Having one’s own coding style is important, but team projects are not about one’s style. Working on a team is about achieving the group’s maximum*collective*potential. This potential is almost always significantly greater than the potential of any individual member, so I’d argue the friction involved in changing one’s habits is worth it.

## Performance

ninja.transformGeometry = function(geometry) { var newGeometry = new Float32Array(geometry.length); for (var i = 0; i < geometry.length; i += 3) { var vertex = transormVertex({ x: geometry[i], y: geometry[i+1], z: geometry[i+2] }); newGeometry.set([vertex.x, vertex.y, vertex.z], i); } return newGeometry; };

The value of performance shouldn’t need argument, but I want to say a few words about how I feel performance should be assessed. Saving a few nanoseconds by using one kind of object property access over another in a code path that runs once over the course of an application’s lifetime is not optimization. It’s important to know where code is spending its time and focus attention there. This will generally be specific to the type of application being built. In [my own work](https://www.biodigital.com/), which primarily involves WebGL, my focus is almost always on the render loop (especially loops within that loop!) and code that has to deal with geometry (i.e. large binary arrays). I’ll mention a few optimization habits I’ve developed that might be of use to others.

**Know the cost of built-in operations:**This basically means knowing the JavaScript runtime environment as well as you can. DOM operations are often a killer. Property lookups as simple as`element.clientWidth`

can trigger[layout recalculations](http://wilsonpage.co.uk/preventing-layout-thrashing/)behind the scenes. WebGL API calls are[expensive](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices). Passing large data to a Web Worker will require an expensive[structured clone](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm)(unless you can use[transferable objects](https://developer.mozilla.org/en-US/docs/Web/API/Transferable)). Knowing these details is invaluable when it comes time to look for performance bottlenecks.-
**Be aware of how your application is using memory:**This can be tricky for web developers since garbage collection usually hides memory details from us. In compute or memory intensive applications, however, awareness of memory usage is critical to avoiding garbage collection penalties and maintaining stability on low-memory platforms. Key things to be wary of are:**Allocations in tight loops:**Be especially careful about common JavaScript patterns that might not immediately look like allocations, e.g. passing parameter object literals to functions, inline callback functions, returning object or array literals from functions.**Copying large objects:**In my own work, this involves being careful with how geometry arrays are handled. This[update to SceneJS](https://github.com/xeolabs/scenejs/commit/4c4a7cf1e32a445153815cbbe650837b6f2f276b), for example, prevents copies of geometry arrays from being made if the arrays are already in the correct format. This[update to BrainBrowser](https://github.com/aces/brainbrowser/commit/a0d65c81fd390e38951b6ace3a7f8623a7e622ae)uses transferable objects to avoid the cost of copying geometry data into Web Workers.


## The Application is the Thing

Coding is fun. And I’ll admit that figuring out fancy tricks in a flexible language like JavaScript can be a lot of fun. But serious software development isn’t about tricks. It’s about seeing the quality of the application one is building as the one and only real priority. Nothing is more fun than seeing people using software you’ve built, seeing it make their lives easier, seeing it make them happy. I’ve presented a few examples of my own conventions here that I believe help me build better software, but I’m certainly not suggesting that those conventions are for everyone. What I do hope we can agree on is that everything we do as developers should be at the service of creating software that works, that works well, and that continues work long into the future.