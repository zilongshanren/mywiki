---
title: Being a Test-Driven Developer is a choice
url: http://www.learn-cocos2d.com/2013/10/testdriven-development-choice/
author: Lawrence says
published: '2013-10-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

This is my coming out: I’m not a test-driven developer. I have stopped trying to force it onto myself.

Yet I do test.

TDD never seemed to work very well for me personally. As a consequence the process never took hold in my habits of writing code, it did not prove itself as the uber-strategy to advancing to the next engineering level.

It took me a while to free myself of thinking that by not following TDD, that I am somehow an undergraduate software engineer. Or worse. As is sometimes implied by more religiously test-driven developers.

Eventually I realized that test-driven development is a thing that you’re born to love, or you aren’t. A process that works better or worse depending on personal habits, circumstances and environment - in that sense I now regard test-driven development along other relatively subjective and debated processes, like pair programming (XP).

Moreover, like pair programming, the minimum requirement is two programmers. If there are only two programmers in your team, it’s a freakin’ waste of time to do pair-programming round the clock. In the same light my experience with TDD is specifically in environments where I was/am the sole programmer, perhaps only occasionally sharing code development with one or two other developers at most.

This is where TDD’s proposed benefits lose a lot of their weight, while its drawbacks are more pronounced, and a more “agile” process works just as well for sole developers and tiny teams.

### TDD is a personal preference

Unit testing is a tool used in [test-driven development](https://en.wikipedia.org/wiki/Test-driven_development). If you don’t “test first” and then write the class’ code and then refactor, you aren’t doing test-driven development, you are testing. On the other hand, you can do just that without following the formal TDD process.

In test-driven development, the tests are written first. They are made to fail because the class they test hasn’t been written yet, it’s only a stub. Therefore all tests initially fail. Then you write code. Then you test and verify. Then you refactor. Then you test and verify again.

TDD is a fairly rigorous, rinse and repeat kind of process. It formalizes the process of writing code. It sometimes feels great, other times it feels terribly constrictive. Unfortunately TDD is not someting that you can do on and off, and still expect it to be very effective. Which means you have to be a rigorously test-driven developer. That might also explain why some developers are quite religious about TDD.

I wager that TDD is significantly harder to subscribe to for certain developer archetypes than others. It makes little sense to force it on developers. A lot of the process has to do with personal preference and a certain enlightened feeling that comes when applying and succeeding with it. Likewise, others may still be in shock after weeks and may forever struggle to adapt.

What is often forgotten when adapting TDD is to actually measure key metrics for the team and individual programmer, both before and after - for some teams/individuals the benefits may be tremendous, for others it may reveal fewer defects but also slower development. Then what remains is a tradeoff: do you prefer fewer defects or faster development? This is a valid question in any product development.

It should also be considered that it takes significantly greater effort for an experienced software engineer to change his or her personal process of developing code than it is for a student. Talk about teaching old dogs new tricks. The students are also more likely to find great rewards in test-driven development as TDD encourages them to learn and experience many software engineering principles.

Undeniably, test-driven development has benefits even for experienced developers. But since I’m talking about TDD specifically for sole developers and fairly small projects, then TDD is simply much less effective in my experience. A more informal process works just as well.

### TDD benefits are generally overrated

There are benefits and drawbacks to TDD. Most remain inconclusive and subjective, only few have been measured in some very narrow-focused case studies ([here](http://www.learn-cocos2d.com/laurie/Papers/TDDpaperv8.pdf) and [here](http://research.microsoft.com/en-us/groups/ese/nagappan_tdd.pdf)).


The aspect of improving courage or confidence in one’s code is a personal thing, and its effect diminishes with greater domain expertise. It can also lead to over-confidence, putting too much trust in test cases when the tests themselves may be wrong.

Unit tests are not a replacement for (reference) documentation and do not provide code examples in context of real application usage. Learning from test code is only marginally better than no documentation. Most test code is so trivial there’s nothing to learn from at all.

The improved quality aspect is debatable and has a lot to do with experience and domain expertise. And of course the team, the environment/culture, the client, and how bleeding-edge the product is.

The quality aspect has been studied with development teams sized 5 or more - but never with individuals or 2-3 developer teams. The results of studies were not overwhelmingly in favor of TDD even in those environments. And with any software development, quality vs time is a trade-off - as much as developers hate to admit that, sometimes less quality with a few more bugs is quite acceptable.

TDD in the small falls in the same category as, say, pair programming. It’s a way of doing things, it helps some but not others, it has benefits that are more important to and more likely to succeed with some developers/teams than others. Unlike pair programming however, you can’t really do it on and off as needed.

But the most important factor remains each developer’s experience and domain expertise. In terms of what you can get out of applying TDD and how you can achieve many of TDD’s benefits without subscribing to the TDD process.

### Testing vs asserting

After repeatedly failing to see TDD through from start to finish of any project, I realized I do just fine without it.

One of my problems with TDD is that the majority of classes are trivial. Trivial to test, too. I don’t gain much from testing those classes. I find assertions a tool much better suited to the job. Yes, assertions only trigger at runtime and only if the code does get called. But what point is there in testing code that isn’t being run anyway?

The better solution is of course to only write the code that you need (or at least test) right now. For an app where you use most of your code most of the time, this works just as well. And you can use the same process: create the stub structure first, test the output in your app, then write the code.

I would go as far as to claim that writing good assertions is just as effective and certainly faster than writing unit tests when it comes to catching issues early. They also have the added benefit that other developers and end users gets a (hopefully) understandable error message, possibly allowing the user to locate and fix an issue due to incorrect usage without having to file a bug report.

Not the same tool, but if you’re not writing tests you better be using assertions! Which goes the same if you do unit tests. Assertions are essential either way.

### Throw-away tests

Trivial test cases also means they’re trivially easy to put anywhere in your code to test that one thing and see whether it fails or not. Then throwing it away again. This is less costly because unit tests are intended to be maintained. But it’s this maintenance that make unit tests time consuming.

Keeping unit tests up to date is a chore. So much so that I’m confident the costs of keeping the tests running is higher than re-writing targeted tests from time to time. I refactor the frameworks I write a lot over time. And quite significantly, which means changing the interfaces and layout - not just renaming things. Having to update unit tests along with the frameworks code greatly increases the time to perform the refactoring, and I noticed this built-in friction actually made me refactor less diligently.

Plus many times when refactoring, the tests need to be rewritten and adapted to the new way things work. Hence there’s no confidence gained from existing tests when the interface changes.

Moreover, I noticed when refactoring interactions and layout of a framework, the unit test code often finds issues only because they either haven’t been correctly refactored or contain new bugs. False positives are extremely annoying. At this point it feels like I’m maintaining a separate project just for the sake of adhering to a certain process. And there are always the nasty issues newly introduced by the refactoring that are caught only by live-testing the app, never by the (already refactored) unit tests.

One then goes on to keep a test specifically for that nastiness. Unfortunately that never crops up again, or if it does, you quickly recognize the pattern if you’re one-on-one with the code. And if you use assertions to ensure that no such bug goes undetected twice you absolutely don’t need extra tests for those nasty issues.

### Complex tests

Then there are complex test cases. I don’t even bother automating them. Yet this is where I’d need automated unit tests most - but the time it takes to set up these intricate test cases with bogus data, let alone maintaining them over time, is just too prohibitive.

Plus bogus data lends itself a lot to [coder’s bias](https://en.wikipedia.org/wiki/Experimenter's_bias).

I find it easier and just as effective to build test scenarios using real data, using the actual app to verify new code works the way it should. And then keep these test scenarios around and maintained as long as possible. But never be afraid to throw them away.

### Designing better APIs

One thing often argued in favor of TDD is that the test-first approach helps to improve the resulting class’ API, its user interface so to speak. I disagree, so long as the developer has a good understanding of API design in the first place. Otherwise it might help.

What really helps to write a better API is to design it before you write code. Spell it out. Test-first isn’t going to magically create a better API without upfront class and interaction design, without requirement specifications, without anticipating future uses and changes.

What unit tests can do is to help verify the overall design and flow of a more complex layout of classes interacting with one another. This is essentially a form of writing UML, but in code. But again, if this is code you’re going to use as you write it, you don’t need unit tests.

I much rather design “on paper” first and then test the actual app with its logic and user interface, with some built-in tests in the code paths that verify the current state of progress and output what’s happening to the screen or log - test code that gets thrown away when no longer needed because past the initial test it’s all downhill from there - in terms of maintenance cost.

Once you have learned the code smells that make an API cumbersome and less flexible to use, you avoid them naturally, classes become simpler, interfaces slicker, code more readable and to the point. This is a matter of experience, where TDD helps the less experienced by forcing them to write testable interfaces which in turn and generally result in better APIs - and for some it forces them to think about code architecture in the first place.

But there’s a point of diminishing return here as one gains more interface design experience. Eventually you no longer need to test-first to think about how to make a class or method (more) testable. In my experience test-first is instructive in teaching good API design, but once you’ve taken it to heart you don’t need to test-first anymore to make your interfaces in any way better.

### Code correctness

Finally, how can I be sure that my code is working correctly?

The simple answer: I don’t, and neither do TDD developers. But like them I can still increase my chances through testing. Just not necessarily unit testing.

For example I locate and fix most of my code bugs by using the code and specifically testing it in an on-the-fly test which is essentially a unit test with a relatively short half-life and written in the context of the application. When I’m done, I move on.

I quickly throw away these tests because my experience told me that maintaining those little buggers is going to add up over time. It’s code baggage that I don’t want to have to maintain. And then when I do need another test, I write another discardable test.

After all, and this is what unit testing proponents always stress: the best tests are simple and to the point. So I’ll just rewrite tests when I need them again, because they’re short and rewritten quickly to the exact thing I need to test at that point in time.

Often overlooked is the issue that unit tests can give a false sense of correctness. A variation of [“works on my machine”](http://www.codinghorror.com/blog/2007/03/the-works-on-my-machine-certification-program.html). Together with false positives and not catching issues you’d think unit tests should have caught make the tests themselves not all too helpful in confirming code correctness. And definitely not interaction correctness, unless you build those complex test cases - with the potential to fall victim to coder’s bias.

In my experience, trying to confirm code correctness by writing lots more unit tests to verify every conceivable input and output is the most time-consuming and wasteful aspect of writing unit tests. It is TDD misunderstood. It’s writing unit tests for the sake of writing more unit tests - unless your code is possibly life threatening, this is in vain.

### Testing informally

I did notice that I do a lot of unit testing and refactoring informally, so I’m often not that far from the overall TDD process. Perhaps I’m mostly opposed to the rigor and required discipline of the TDD approach - writing the tests first, maintaining the unit tests, and doing so for every code you write.

Overall to me TDD kind of feels like switching from right-hand mouse to left-hand mouse - so the question always painfully lingered in the back of my head: why? And what do I get in return? Is it really worth doing all things considered?

I could never get rid of that lingering, nagging feeling. I work well the way I work, doing tests on the fly and building elaborate test scenarios that I can run through manually or semi-automated. I never felt like TDD enhanced my development workflow, or that it improved my confidence and the quality of my work.

### Test opportunistically

With all that said, my final advice to those struggling to adapt TDD or peer-pressured into it is simple:

Write unit tests where you find they help you. Don’t feel compelled to have to do test-driven development just because a vocal group of developers swear by it. TDD isn’t for everyone, and it isn’t for every situation, and unit tests by themselves can still be helpful even if they cover only 5% of your entire code base.

But don’t forget the other tools: assertions, scenario (live) testing and quick, throw-away inline code tests. Never be afraid to throw away tests!

If your unit tests are ludicrously simple, it’s hard to reassure oneself that they ought to be written **and** maintained. If unit tests cost a lot of time refactoring and maintaining them, they themselves become a second project that needs to be tended to with questionable benefits for individual developers and tiny teams.

But if you feel TDD is still beneficial to you personally that’s okay, too. It doesn’t necessarily apply to everyone though, so please, stop nagging us that we’re not developing software “the one true way”.

I personally could never shake the feeling that TDD is just as much opposed to agile development as it is part of it. The much needed discipline in writing, testing, refactoring and maintaining unit tests, and some TDD supporter’s non-compromising attitudes, feel a lot more waterfall than agile to me. More so if you consider that unit tests can add noticable friction to refactoring code and design changes in the first place, one of the hallmarks of agile development.

Let’s not miss the point though: (unit) testing is a tool that can be used as you see fit, on and off, and can and should be thrown away if the cost of maintaining them grows too large. Writing unit tests must not be misunderstood as “doing TDD” however. TDD is a formal software development process, which no one should be forced to do if they don’t want it. For one, if you force it, it’s not going to stick nor will it be very effective.

Whether you as a sole developer find pleasure in writing code in the test-driven development methodology (and doing so rigorously), or just “normally” with or without adding some (unit/temporary) tests, largely remains a personal preference. I’m convinced that TDD is not nearly as beneficial (if not detrimental) for an experienced tiny team of software engineers than it is for a team comprised of several developers with mixed experience levels, overlapping and changing responsibilities and a typically much larger code base.

But, by all means, do test. Test early, test often, test in any way you can. And make assertions, not assumptions.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Very nicely written. Great points made! Makes me feel a lot better because I was thinking some of the same things.