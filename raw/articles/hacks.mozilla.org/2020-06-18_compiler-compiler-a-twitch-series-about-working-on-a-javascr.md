---
title: 'Compiler Compiler: A Twitch series about working on a JavaScript engine –
  Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2020/06/compiler-compiler-working-on-a-javascript-engine/
author: Yulia Startsev
published: '2020-06-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last week, I finished a three-part pilot for a new [twitch stream](https://www.twitch.tv/codehag) called *Compiler Compiler*, which looks at how the JavaScript Specification, [ECMA-262](https://tc39.es/ecma262/), is implemented in [SpiderMonkey](https://firefox-source-docs.mozilla.org/js/index.html).

JavaScript …is a programming language. Some people love it, others don’t. JavaScript might be a bit messy, but it’s easy to get started with. It’s the programming language that taught me how to program and introduced me to the wider world of programming languages. So, it has a special place in my heart. As I taught myself, I realized that other people were probably facing a lot of the same struggles as I was. And really that is what Compiler Compiler is about.

The first bug of the stream was a test failure around increment/decrement. If you want to catch up on the series so far, the pilot episodes have been posted and you can watch those in the [playlist](https://www.youtube.com/playlist?list=PLo3w8EB99pqJVPhmYbYdInBvAGarDavh-) here:

Future episodes will be [scheduled here](https://developer.mozilla.com/events/compiler-compiler-yulia-startsev/) with descriptions, in case there is a specific topic you are interested in. Look for blog posts here to wrap up each bug as we go.

## What is SpiderMonkey?

[SpiderMonkey](https://firefox-source-docs.mozilla.org/js/index.html) is the JavaScript engine for Firefox. Along with [V8](https://v8.dev/), [JSC](https://webkit.org/blog/7536/jsc-loves-es6/), and other implementations, it is what makes JavaScript run. Contributing to an engine might be daunting due to the sheer amount of underlying knowledge associated with it.

- Compilers are well studied, but the materials available to learn about them (such as
[the Dragon book](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools), and other texts on compilers) are usually oriented to university-setting study — with large dedicated periods of time to understanding and practicing. This dedicated time isn’t available for everyone. - SpiderMonkey is written in C++. If you come from an interpreted language, there are a number of tools to learn in order to really get comfortable with it.
- It is an implementation of the
[ECMA-262 standard](https://tc39.es/ecma262/), the standard that defines JavaScript. If you have never read programming language grammars or a standard text, this can be difficult to read.

The Compiler Compiler stream is about making contributing easier. If you are not sure how to get started, this is for you!

## The Goals and the Structure

I have two goals for this series. The first, and more important one, is to introduce people to the world of language specification and implementation through SpiderMonkey. The second is to make SpiderMonkey as conformant to the ECMA-262 specification as possible, which luckily is a great framing device for the first goal.

I have organized the stream as a series of segments with repeating elements, every segment consisting of about 5 episodes. A segment will start from the ECMA-262 conformance test suite ([Test262](https://test262.report/)) with a test that is failing on SpiderMonkey. We will take some time to understand what the failing test is telling us about the language and the SpiderMonkey implementation. From there we will read and understand the behavior specified in the ECMA-262 text. We will implement the fix, step by step, in the engine, and explore any other issues that arise.

Each episode in a segment will be 1 hour long, followed by free chat for 30 minutes afterwards. If you have questions, feel free to ask them at any time. I will try to post materials ahead of time for you to read about before the stream.

If you missed part of the series, you can join at the beginning of any segment. If you have watched previous segments, then new segments will uncover new parts of the specification for you, and the repetition will make it easier to learn. A blog post summarizing the information in the stream will follow each completed segment.


### Last but not least, a few thank yous


I have been fortunate enough to have my colleagues from the SpiderMonkey team and TC39 join the chat. Thank you to [Iain Ireland](https://hacks.mozilla.org/author/iirelandmozilla-com/), [Jason Orendorff](https://hacks.mozilla.org/author/jorendorffmozillacom/) and [Gus Caplan](https://twitter.com/devsnek) for joining the streams and answering questions for people. Thank you to [Jan de Mooij](https://hacks.mozilla.org/author/jdemooijmozilla-com/) and André Bargull for reviews and comments. Also a huge thank you to [Sandra Persing](https://hacks.mozilla.org/author/spersingmozilla-com/), Rainer Cvillink, [Val Grimm](https://hacks.mozilla.org/author/vgrimmmozilla-com/) and [Melissa Thermidor](https://twitter.com/melissatherms) for the support in production and in getting the stream going, and to [Mike Conley](https://github.com/mikeconley) for the streaming tips.

## 13 comments

AnandJune 25th, 2020 at 10:59Triandi SihombingJune 25th, 2020 at 20:21Aaron WrightJune 26th, 2020 at 18:32pauloJune 27th, 2020 at 07:15Yulia StartsevJune 29th, 2020 at 02:42SamuelJune 27th, 2020 at 10:54MarkJune 29th, 2020 at 02:20Yulia StartsevJune 29th, 2020 at 02:45MarkJune 29th, 2020 at 06:51Yulia StartsevJune 29th, 2020 at 07:01BhaveshJune 30th, 2020 at 10:08ruthJuly 17th, 2020 at 05:16Yulia StartsevJuly 17th, 2020 at 05:22