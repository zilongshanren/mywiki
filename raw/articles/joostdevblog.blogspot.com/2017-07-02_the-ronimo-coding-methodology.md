---
title: The Ronimo coding methodology
url: http://joostdevblog.blogspot.com/2017/07/the-ronimo-coding-methodology.html
author: Joost van Dongen
published: '2017-07-02'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Ronimo](http://www.ronimo-games.com), which every programmer and intern gets to read on their first day. Our

*Methodology*document explains the workflow while the

*Style Guide*explains the layout of our code. Today I'd like to show our Methodology and describe the reasoning behind the rules in this document.

![](../../assets/4fc7c4ace5fe6df3.jpg)

Note that the contents of this document aren't very original: most if it is a combination of common agile practices that I like.

Let's start by having a look at the actual methodology document:

## The Ronimo coding methodology## General method of implementing a new feature:
## Implementing a |

Most of these are quite clear, but it's interesting to discuss some of the reasons behind these rules. Often enough I've seen coding interns have loose ends everywhere in their code because they were working on five things at the same time and forgot to test, clean up and finish some of them. That's why our coding methodology requires that you finish what you were doing before you get to the next thing. This is also why I require that big tasks are split into smaller ones: a person can only remember so much and the more things you're working on simultaneously, the bigger the chance that you'll overlook something important.

At the same time I prefer the agile way: only make what you actually need and expand the codebase as you go. During early development you don't know all the features you'll need, nor do you know for all problems how you'll solve them. However, adding things one at a time will often make code bloated and without focus, and will muddy class responsibilities. That's why code needs to be refactored often. Refactoring requires discipline. Often you can hack in a new feature in just a few hours, or first spend half a day refactoring to make room for that feature in a good way. It's easy to skip or postpone refactoring, but doing so often produces unworkable code in the long run. That's why refactoring is an explicit step in our methodology.

Focusing only on one small new thing at a time shouldn't be taken too literally though. While I think it's important to not work on other things until what you're doing is finished and clean, that doesn't mean you shouldn't look ahead. When building something complex it's important to think about how you're going to make the whole system work. I once had an intern who had to rebuild a large part of a tool because he had taken our coding methodology too literally and hadn't thought ahead at all. The most complex features of the tool were not possible at all with what he had build. The key here is to find the right balance between thinking ahead and focusing on one thing at a time.

![](../../assets/5b9ae29e32632d64.gif)

Another staple of mine is that programmers need to communicate directly with designers and artists. We believe extensive design documents are rarely a good idea, so the only way to know what's needed exactly is to talk to the designer or artist who needs a new feature. Often that person hasn't defined the exact details of the feature, so the coder needs to discuss it with them and think about the caveats, also from a design and art perspective. To smoothen this communication it helps a lot if the programmer has a little bit of experience in design and art, but even if that's not the case I think it's the programmer's job to talk the language of the designer or artist, not the other way around. It's really difficult for a designer to speak code, but a programmer should be able to talk about his work in comprehensible English (or Dutch in our case).

One thing that's surprisingly missing in our Coding Methodology is unit testing. We have a strong focus on testing our own code extensively, but the document doesn't say you need to write unit tests. This is because I think gameplay is often too chaotic and unpredictable to test well with unit tests. Certain things are testable with unit tests, but the bugs we encounter are often not things where I can imagine how a unit test would have found them. Often it's things that function fine but result in undesired gameplay.

I do realise that not making units tests makes us more vulnerable to bugs than a team that always writes unit tests, so we emphasise that if a crash or major bug is found, it needs to be fixed right away. We might have more bugs than software developers who write extensive unit tests, but at least we fix them quickly. I do think we ought to use unit tests more for things like server architecture. Unit testing isn't in our blood at all and it probably should be at least a little bit. I'm curious though: do you use unit tests for your gameplay or engine code?

Regardless of whether you agree with the particular rules in our methodology document, I think it's important that all programmers think about their workflow. Just doing whatever you feel like doing isn't good enough. Discipline and structure are important for anyone who works on larger, more complex systems. What's you're coding methodology like? If you happen to work at a company, is there an official document like the one I've shown today?

So that's it, the Ronimo Coding Methodology! Next week I'll show our Coding Style Guide, which is quite a bit more strict than most coders are used to.

cool

ReplyDeleteHey Joost,




ReplyDeleteThanks for sharing these insights, it's very interesting to see how other companies are doing things. At Sticky Studios we have a very similar methodology. Adhering to Scrum and using Jira helps us break work down into smaller tasks in a similar way. Testing everything on device is a requirement for completing a task and we're using a "review" step for any task for which a review is required by either a designer or another programmer, which is decided when estimating the task.

Unit tests are tough subject; we have also rarely used them in the past for the reasons you state, as well as others. In the end all principles and methodologies come down to the same thing at the very end; saving time.

In my own experience writing unit tests or even applying full-blown test driven development, where you write your tests before your implementation, roughly doubles the initial time taken to build something. This is then supposed to pay off by costing less time to debug and becoming much easier to maintain afterwards. The issue with gameplay related features is that they change the second you finish them; test it with a designer and they'll have a list of modifications or even draw the conclusion "well, it was a nice idea but it just doesn't work in practice". At that point you don't get the benefits of writing your tests but you did take much longer.

I have found great value in test driven development and unit tests when writing well-defined systems. When you know what you're building and also how you want to build it then you can apply test driven development to great effect. But most gameplay is simply to prone to change to fall in that category.

We have very few unit tests, just a handful in the engine. We probably ought to have more ^^


ReplyDeleteHowever we do a lot of peer reviews (through pull requests on github). Almost nothing goes into the master branch without a review. That was a HUGE improvement when we started doing it. Ensures simpler/cleaner code + regularly catches a few bugs.

This comment has been removed by the author.

DeleteAnd thanks for this article, it's really interesting to learn how the others do!

ReplyDelete"We might have more bugs than software developers who write extensive unit tests, but at least we fix them quickly"


ReplyDeleteHad to reread that ;D As you state you have 0 software developers who write extensive unit tests, it is only logical that you would have more critical bugs than that...