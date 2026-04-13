---
title: When To Rewrite
url: http://hacksoflife.blogspot.com/2010/01/when-to-rewrite.html
author: Benjamin Supnik
published: '2010-01-02'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Joel's treatment](http://www.joelonsoftware.com/articles/fog0000000069.html)on the subject is thorough and clear. I would only add that beyond the intensely poor return on investment of a total rewrite (e.g. spending developer time to replace field tested, proven code that users like with a track record for making money with new untested code that may be buggy without adding new features), the actual dynamics of a rewrite are even worse in practice. This is how I would describe the prototypical rewrite:

Software product X is first developed by a small team of grade A programmers - programmers who understand what they are doing completely, can ship product, fully chase down bugs, and understand the trade-offs of architecture vs. ship date. These programmers maybe don't always write the cleanest code, but when they write something dirty, they know why it's dirty, what they will do about it, and at what point it will make sense from a business standpoint to fix it. (And the fact that the "dirty" code shipped means: that time to fix the problem hasn't come yet.)

Once the product starts making money, the team grows, and the product goes into a feature mode - new versions get new features added into the code. The business model is to sell upgrades by putting features into the code on a timely basis. This is where things start to get tricky:

- The business model rewards shipping new features. Thus the metric that the company should be looking at is "efficiency", e.g. how many man-months to get a feature valued at some number of dollars?
- There is an opportunity cost to not shipping features, thus the team has been increased in size with "grade B" developers.
- Now management has a serious problem: if the efficiency of the team is declining, is it because the grade B developers aren't as efficient (a known and acceptable risk) or because the code is becoming harder to work with?

*what the code says*) they are not going to have any tools to recognize the problem. Combine that with the fact that every developer says every piece of code not written by himself/herself within the last 3 days is fugly, and management just doesn't know the extent of the problem.

Is the code base getting worse at this point? Almost certainly yes!

- If the original design was business-optimal, it did not contain a bunch of code to make future expansion easy. (Side note: this is the right decision and this problem of architectural drift should
*not*be solved by making the "grand design" in version 1. No one knows what features will actually be useful in version 2, so a "grand designed" version 1 is going to have a ton of crap that will never get productized and just take longer to ship in the first place.) - If the business model can't track efficiency and code quality, then the A team (the only ones capable of rearchitecting the design) are under strong pressure not to do so. In fact, they're getting the hardest problems and are probably critical path in every release; asking them to rearchitect to will seem like an impossibility.
- The B team doesn't understand the design, and thus every feature they're putting in is probably screwing up the program a little bit more.

Management is eventually convinced that this is a good idea, but can't accept the idea of not having revenue. So the team is split in half:

- Half the team does maintenance updates on the existing code, to ship the next version, with new features, business as usual. This team will probably be in a bad mood, as they have to work in a pit of slime.
- The other half of the team is split off to build the next-generation system, to ship one release after this one, on all new code.

- The next-generation approach will start with an architecture that is too grand for its own good. Without the pressure to ship a 1.0 product, with the mandate not to ship product but to "clean the system up", and after years of dealing with crappy code, the next-gen design will be brilliant, but severely over-architected from the start. To expect the engineers in this situation to really be good about minimalism in architecture is to expect monkeys to fly. (If there are any technological fads going around, expect the new design to pick them up like a fleece attracts dog fur.)
- When the marketing team realizes there is a "next generation" scheme, they will promptly hang every ridiculous feature they have ever thought of on the scheme. As long as you're rewriting the architecture, why don't you make it so that the entire system can be remotely accessed from your car radio? Can we make the user interface fully customizable so it can be skinned in baby blue or pink? We would like it to use this series of TLAs that Microsoft thinks are clever right now.
- What won't go into the initial design is all of the small features (and bugs/design flaws that users think are features) that make the existing product a hit. So while we already have a hugely over-scoped product, it's going to pick up another set of features, the ones that really make money, late in the design. Of course, it was never architected for those features (hell, the designers probably thought the old code was "dirty"
*because*of those features) and thus if this product ever ships, the code will be considered fugly as soon as it is finished.

I'm not entirely sure what the practical solution to this is. Since I now work at a company with only two full time developers (myself included) we have the advantage of there simply not being a B team to hose our design. It makes me wonder what management should have done? Possibilities include:

- Hire only "A team" programmers and accept that the lost short-term revenue and higher cost of hiring only really top-notch employees is offset by the long term ROI of code that can efficiently generate features over a longer span. (It may be that this isn't a win, and that the above parable, while depressing, is the best ROI...products don't make money for ever, and the financially lucrative thing to do might be to ship 1.0, add features until it's dead, then kill it.)
- Accept the cost of refactoring during work. This requires a really special type of programmer - you need someone who fully understands the architecture and the business model and can balance the two. This business model implies that the team trusts the absolute judgment of the very small (maybe only one) group of individuals who see both sides.
- Keep the B team on a really, really, really short leash. This probably reduces their efficiency even more (to the point where they may not be useful ROI-wise) and probably drives those deveopers crazy.

**So When Do You Rewrite**

Implicit in all of this is a very basic idea: if the software is

*incrementally*rearchitected during development, the long term return on investment is going to be a lot better. You're going to make more money (in the long term) because:

- You're rearchitecting lots of smaller, easier to fix problems instead of the mother of all train-wrecks. The cost of working on code is non-linear and a function of interdependency, so it's almost always going to be a huge win to nip a problem in the bud.
- The cost of adding features will stay low, which means the cost of your team isn't going to go up relative to output over time.

So when is the right time to do this rearchitecting? At this point in my programmer career, my answer is:

Right before you would lose any productivity by not rearchitecting.(Note that this is after "right after you are completely sure that you will need to rearchitect.")

Basically you never want to rearchitect until you are 100% sure that it is necessary. Rearchitecting early risks wasted work. (I would say the cost is worse - you pay for the complexity of your software continuously so any unused abstractions are hurting your business.) Once you know that the feature you are doing is being made difficult by an existing inadequate architecture, you have 100% certainty.

Since the long term costs of rearchitecting are going to be less if you do it earlier, refactor as soon as it's holding you back. Start every feature with a behavior-neutral rewrite of the underlying code to be exactly how it needs to be - the actual feature work will be so much more efficient, and the resulting code will look like you could keep working on it without sticking needles in your eyes.

(But: don't start reachitecting on a module that is going to remain unmodified. You'll have to retest the module even though you didn't gain revenue. If you rearchitect now for the feature you will code in six months, you increase the amount of testing the release now is going to have. So make a note "this code will need work", and in six months, that's when you dig in.)

The point "If you have management by metrics (e.g. a management team that uses proxy metrics like bug count, KLOC and other such things but doesn't actually look at what the code says) they are not going to have any tools to recognize the problem" is a good one. Without ways or measuring (and agreeing upon) what is pretty and what is ugly, we can make no progress.

ReplyDeleteThere are other ways to handle the complete rewrite problem. One method is figure out what the motivating feature is behind the rewrite, and write the new version exclusively for those people who need that feature, cutting out all other features. Ship that, then expand the rewrite's scope out to the original product.


ReplyDeleteBut yeah, you're still going to be reusing at least some code. Tossing all of your code and literally doing a complete rewrite is just silly.