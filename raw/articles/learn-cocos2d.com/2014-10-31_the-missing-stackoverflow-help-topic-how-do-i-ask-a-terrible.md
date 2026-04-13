---
title: 'The Missing StackOverflow Help Topic: How do I ask a terrible question?'
url: http://www.learn-cocos2d.com/2014/10/missing-stackoverflow-topic-terrible-question/
published: '2014-10-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

This guide goes through the telltale signs of terrible questions asked on stackoverflow. You’ll learn **how not to ask questions**.

If instead you like to learn [how to ask good questions](http://stackoverflow.com/help/how-to-ask) you came to the wrong guide. You may also want to learn to tell people [what the Matt you’ve tried](http://mattgemmell.com/what-have-you-tried/) so far. Jon Skeet has an

[excellent checklist for the perfect question](http://codeblog.jonskeet.uk/2012/11/24/stack-overflow-question-checklist/)that you should go through before submitting your question.

Okay, admittedly I make some poignant observations and suggestions that can be seen as helpful.

If you have been given this link as a response to your question on stackoverflow.com, please don’t take the following personally. I do not intend to offend or insult you, it’s just that I’ve become a little too annoyed to not point out the flaws directly and admittedly without sugarcoating them. Nevertheless there’s good advice in here and I’m sure you’ll know how to apply that to your question and you will get (better) answers because of it. I’m just trying to ~~vent~~ .. help. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


### Any Ideas? Suggestions?

So tell me, what you you **really** want to know?

You can’t expect stackoverflow users to give random suggestions and guidance. This is [not what stackoverflow is about](http://stackoverflow.com/help/on-topic). It is about concrete problems that are likely to have a specific answer (or two).

If you don’t know what specific question you should ask then it’s the same as not asking anything at all. It tells everyone you did not understand your problem well enough to ask a specific question about the problem. Which means any suggestions are very unlikely to point out the flaw in your thinking, or even nudge you in the right direction.

Worse, in some cases it’s obviously just poor laziness. You don’t even want to invest time in properly asking a question? Fine, but please don’t do that on stackoverflow.

### … is not working (properly).

“Not working” is not a problem description. You can say “my car is not working” if you need an excuse for your boss why you’ll be late to work. But even a mechanic won’t be able to diagnose your car’s problem if you can’t describe what you were doing and what the car did.


Did you turn the key? Yes. Did the car make a noise? Yes. What noise? Uh, the not starting noise. Do you have enough gas? I think so. Are the dashboard lights flickering? They barely come alive. Okay sounds like you have a dead battery, I’ll send someone over with a starter cable.

This is a troubleshooting example. Questions and answers back and forth. Except that you have to ask yourself those questions **while** writing your question because all of this **will** be necessary to help pinpoint the source of the problem.

“Not working” can mean many things. Did the object fail to create? Did it crash? Did it simply not show up on screen? Did it rotate the other way? Did it not collide with other objects? Did it not, as you expected, step into a time machine, activate it, warp back in time, kill its parents, only to fade out of existence?

The most annoying thing on stackoverflow is having to ask more questions that shouldn’t be necessary if the question had been asked properly. Most SO users don’t bother doing that, so if your question receives no response at all, not even close votes, then your problem description (or lack thereof) may be the culprit.

You want an answer, so put some effort into writing the question with as much detail as possible but without posting entire classes or your entire project.

If you can not (or are too lazy to) describe your problem in detail you will not get an answer, so writing the question in the first place is a waste of everyone’s time. Instead, explain the steps you took, what you observe and what you expected to happen instead.

### My project is on github/dropbox

No. No no no.

No one will download, run and debug your project. Forget it.

If you can not condense the problem so that you have a few dozen lines of code that you can post right into the question, you haven’t taken enough care to narrow down your issue. And then by the nature of it you will not be able to ask a good question or receive good answers.

Also, it would really help if you got the most basic debugging steps done. Here’s a few things you should look up that you need to be able to do in your development environment even if you’re the most n00bish beginning programmer that ever existed:

- Logging

- Setting breakpoints

- Stepping through/over code

- Viewing variables

Really, that’s all. And it’s really simple to do in almost every IDE in almost every language! Even where there’s only logging you can get to know a lot about your code’s runtime behavior by logging.

If everyone would know how to do these simple debugging tasks we could easily cut down the number of questions on stackoverflow by half.

### My program crashes …

So, what’s the crash message? Anything in the log? What is the call stack? What line does it crash? Which function/class is it in? Is it reproducable? What are the steps to reproduce it?

If you can’t answer those questions it’s pretty pointless to ask how to fix the crash because it could literally be almost anything.

Also please don’t post screenshots of your IDE with the error. Screenshots are resized and text within it becomes hard if not impossible to read. Almost every IDE allows you to select things and copy & paste most items as plain text. Certainly that’s the case with build and runtime logs, call stacks and error/warning messages.

### What is the best .. ?

The hallmark question of an indecisive or simply clueless programmer. There’s always many ways to do one thing, and they are often subjective or depend heavily on requirements, personal experience/preference and what not.

Try for a moment to define what “best” means. How else could you write “What is the best xxx”? I’ll give you a second.

…

Here, I’ll show you what “best” without context *could* mean:

- the fastest ..

- the most memory efficient ..

- the smallest executable generating ..

- the fastest compiling ..

- the least amount of bandwidth consuming ..

- the most readable ..

- the most maintainable ..

- the quickest ..

- the cheapest ..

- the most popular ..

- the one with the most tutorial videos ..

- the one that’s been used the most by professionals ..

- the most legally sound ..

.. solution. I certainly forget a couple more “bestest” variants here. But I think you get the point.

There is no “best” because “best” with no or only little context *doesn’t mean anything*. But even where the meaning is clear from the given context, “best” is often subjective and stackoverflow has strict rules discouraging questions that provoke opinion-based answers.

Lastly, who are we to say what is “best” for you and your actual problem? Often times we aren’t even told about the situation, so any answer would amount to making wild guesses. Consider that my “best” will often not be your “best” for your given situation and development requirements.

Questions like “Which game engine is better, A or B?” have no definite answer.

Let’s be honest: [you just want someone to tell you what to use or do](https://en.wikipedia.org/wiki/Analysis_paralysis). So if anything you could just randomly pick one of your choices and see if this applies well to your situation and your level of experience. I bet with you, the actual choice doesn’t nearly matter as much as you think it does.

Also, if you can’t decide that for yourself based upon the requirements you have for your app, you’re not doing your job as a programmer. If you have to choose between several technologies, analyse your requirements and then test each technology with your requirements and see which one seems to work best. This doesn’t take long, and it will be *very* instructive.

So, pleaaaaase stop using the word “best” in stackoverflow questions, it’s appalling! Thank you!

### Please help, it’s urgent!!!11

“Anyone here? I still need help with this!!1”

This is the kind of question I expect to be duplicated within an hour or two in order to bump it.

Sorry, if you can’t wait until someone answers, don’t ask. Especially if you can’t even take the time to properly ask a question.

If it’s that urgent, fix it yourself. If you can’t fix it yourself, you chew off more than you can swallow. Accept that. I don’t care whether a client is breathing down your neck to fix a last-minute approval rejection issue or whatever it may be.

It’s your problem, so please, if you want help with it, don’t put the pressure on us. Find a solution by yourself or ask nicely and be patient.

### Is this possible?

Well, maybe. Maybe yes, maybe no. Do you really want a “Yes” or “No” as an answer? I don’t think so.

Avoid asking “yes” / “no” questions. No one will answer them because Stackoverflow doesn’t allow a simple Yes or No as an answer (or even just as a comment) - it’s not enough text.

You can encourage a more specific answer simply by avoiding your question to be answerable with a simple “yes” or “no”. If you can’t ask a more specific question and really want to get a “yes” or “no” as an answer, know that you **will** have follow-up questions. So take that thought one step ahead and think about what your questions would be if the answer were “yes” or “no”.

### I’m not telling you why I’m doing this

A number of questions revolve around a coding problem that raises eyebrows. Why are you even trying to do this?

More often than not, those are [XY problems](http://meta.stackexchange.com/a/66378). In short, you are asking about your attempted solution without saying what it is that you really want to accomplish. Instead, inquire about possible other ways to achieve your goal. Which means you have to state your goal in the first place.

Fact: If you state your intended goal, you will get far better answers. A lot of the experts will give you true and tested solutions to common problems if only you state your goal. If you don’t state your goal, you won’t get that expert advice. Or just raised eyebrows inquiring about why you’re doing this in that very odd way.

### My windows is closing

Not using the proper term: for instance if you say “window” every time you mean “view”, or “map” instead of “two-dimensional array”, or “conflagutalate” when you really mean “compile”.

This is just purely annoying because it is often very misleading if you don’t use the commonly accepted terms for given items. Some of them can be *very* different things!

You have certainly read tutorials or documentation of some kind using the proper terms so if you can at all then please try to figure out what everyone is calling X and henceforth use X whenever you talk about X.

If you are unsure, paraphrase. Or take it to google to find the correct term. Or post an image.

### Don’t read the tag descriptions!

So you are done writing your question but it won’t let you submit it because you didn’t add tags. Darn, quickly add some and be done with it!

So you add whatever comes to your mind without reading the tag descriptions. You missed all the finer points like “DO NOT USE THIS TAG” or that “spawn” doesn’t refer to spawning enemies, it’s about spawning processes. The “load” tag isn’t about loading resources, it’s about CPU “load”.

Consider that cocos2d-iphone is very different from cocos2d-x and that there’s a [Unity](http://msdn.microsoft.com/en-us/library/ff649614.aspx) that’s not the [Unity](http://unity3d.com/) you think it is. Or you could just add both, one of them will be the correct one, right?

Please, read the tag description for every tag you add and consider whether this particular tag adds valuable context to the question or not. If the tag has no description and very, very few questions tagged with that tag, it’s better to use a different tag. Dead or dormant tags add no value to the question.

Also consider what tags are really applicable in the first place. If you make an iOS app and you have an Objective-C or Cocoa programming problem, like a certain method doesn’t run, then don’t add the Xcode tag just because you’re building your app within Xcode. For one it’s self-understood that you are using Xcode, and of course your problem really isn’t with Xcode itself, is it?

Tags are important to get the question in front of the proper audience. If you use the wrong tags, you can easily limit your audience or miss the right audience entirely.

### (gibberish)

Okay. Have you read your question out loud? Does it make any sense? No?

Then write it again in proper english!

I understand that not everyone’s mother tongue is english. In that case you can still enhance your question with code and images, and fragments from publicly available documentation. Don’t hide the gist of your question behind “sorry my bad write english can”.

However there are english folk who just can’t seem to write coherent sentences. It really, really makes me wonder how you are capable of writing code that compiles in the first place? It really comes off as simply being lazy and careless, which is in fact another form of being rude.

### don’t format your question/code

Who needs tabs, paragraphs, hell - even punctuation, right?

Why would anyone write code where the indentation increased within each bracket?

Why shouldn’t you put an entire paragraph or the entire question in bold letters?

Perhaps some coders ought to be put through the task of writing a complex Python program just to understand the need for properly formatting code.

Also don’t post screenshots of your code. Code is text, you can paste text right into your question. Then select the code, and hit the curly braces icon. That formats the selected block of text as code. If the code comes out terribly garbled, check your IDE. There’s often an auto-format option that let’s you straighten out your code, replacing tabs with spaces or vice versa. Then copy & paste the corrected code.

Posting readable and properly formatted code is very important if you are looking for an answer to a coding problem.

### Conclusion

Sometimes, when reading questions on StackOverflow, I’m like this guy (except for the turtle, I don’t have a turtle):

Really, it isn’t that hard to write good questions. Or at least acceptable ones. It is well worth your time (and ours) if you went through, read and understood the [“how to ask” section on stackoverflow’s Help Center](http://stackoverflow.com/help/asking).

The thing is: **you** want an answer. So you need to do whatever it takes to make us **want** to give you an answer! Or at least try to make it as easy for us as is possible for you.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |