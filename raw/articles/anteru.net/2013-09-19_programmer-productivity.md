---
title: Programmer productivity
url: https://anteru.net/blog/2013/programmer-productivity
published: '2013-09-19'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I’m a graphics researcher, but I’m also a programmer, and as such, I’m programming most of my day. The question is, how productive I am, and what factors influence this? With productivity, I mean the number of completed tasks per day and the time working on completing tasks compared to “unproductive” time like answering e-mails, reading a web page or talking with an office colleague.

As a programmer, measuring is of course the right approach. What makes this slightly difficult is that there is no simple measurement for productivity; if I take code commits or number of lines written. Instead, I logged for the last 6 months what I did every day. Every morning, I open up a new text file, and write how I spent my time this day. If I end up talking with a colleague for half an hour, this gets noted. If I write three e-mails, it gets noted. If I improve the performance of my raytracer by 3x, well, you know the drill.

Over the time, I found that there are lots of different reasons why a day turns out to be unproductive, but there are two patterns which indicate a productive day.

## Finishing lots of small stuff

The one category of productive days is when I finish lots and lots of small tasks. For instance, I manage to reply to the five e-mails waiting in my inbox, get that three small bugs fixed, and finish my bill of expenses for the last trip, all before lunch break. These tasks have a few things in common:

- They are not really urgent. Sure, if you are the one waiting for an e-mail reply from me, you might think otherwise, but heck, if you wait a day longer the world isn’t going to end.
- They require usually little intellectual effort: That is, you have high skill in that particular area and the task provides little to no challenge, making these tasks boring. Or the task is mostly time-consuming, like installing some SDK and setting up the debugging environment.
- If they need intellectual effort, then the tasks have some frustrating component to them: Bugs which require elaborate setup before you can actually debug them; code refactoring which will need touching lots of files, etc.

So even though the tasks are really stupid or frustrating, why do I end up having productive days solving lots of them? Each of them requires a context switch and usually a bit of preparation time.

It turns out that on the days where I wind up solving a lot of them, I usually have a list of the tasks to do. That is, all the stupid/frustrating bugs are tracked, so I can see my progress, the e-mails are all lined up in my inbox and most importantly, the tasks are actually finished when I finish them. That is, there won’t be an immediate follow-up task. And finally, the scope of these tasks is really clear. If these circumstances come together, I can crunch through them really fast and be productive even if I get interrupted.

## Flow

The other productive days can be simply described as being in the “flow”, or working on very few tasks for longer times. Optimizing your BVH traversal kernel is just needs a few hours of work. In order to be productive, I need long uninterrupted chunks of time; ideally, I’ll start with anything urgent in the morning so I have nothing else to do. It’s interesting to see that I typically tend to delay anything coming up during such days until either shortly before I leave work or the next morning.

I’m also much more likely to continue working on such days from home, either to really finish the task or do solve related problems. For instance, if I hit a non-critical issue, I just delay it, and in the evening, I sit down to solve it so on the next day, I can focus solely on the core problem again.

On such days, you might also see me having a hard time killing “dead” time. Chances are high that I’ll finish some large task at 11.45, and I’ll have no clue what to do until 12.00 (lunch break), as 15 minutes is too short to start working on the next task. I haven’t found a satisfactory solution to this yet. Most often, I spend reading some paper or blog online, so it’s not completely wasted.

## Bad days

All other days are bad days. The number one problem is of course interruptions; the worst ones are those that need follow-up action. For example, I send back some required paper work, and once I get the reply, I will have to quickly do some other paper work/call someone, etc. This blocks me from starting work on larger tasks, as I need uninterrupted time for them. You might think that this is one of the days for the small tasks, but it turns out that I might not have enough small tasks piled up to fill it up effectively. Or, worse, several of the small tasks have dependencies, so I can’t schedule them the way I want.

There are also external reasons why a day might suck, as traffic jams, getting too late to bed, eating the wrong stuff, etc. Two are in particular detrimental to productivity:

- Lack of sleep: Your day is going to suck, get over it. Go home earlier, go for a walk, and get some sleep!
- Headache: You overdid it the last day or you slept badly. Try to focus on easy tasks, take more breaks, go for a walk.

Otherwise, there’s only one good solution: Focus on getting things done instead of “working”. As long as there are not too many interruptions, this usually works. What I have learned though is not to worry too much about bad days. If you have them logged, you can check how many and take corrective means. For instance, you’ll just delay that e-mail until tomorrow with three other small tasks that you wanted to do to get a longer chunk today. Just make sure to note these things down so you are productive the next day (because you can see progress) and today (so they don’t bother you all the time.) Or, go home, do something else, and sit down in the evening to churn through the most boring stuff and go to bed afterwards.

## Programming task observations

I have also done a few observations over the last few months:

- Simple tasks take either less than 5 minutes or between 30-60 minutes. If the task is really simple (fix a typo), it can be done nearly immediately, but if the task is only simple (fix the integer ceil-division routine to work with negative numbers), you will spend half an hour to make sure that the documentation is updated, that you have written the right unit tests, and that you have updated all the right places in the code.
- Complex tasks require wasted work: Adding rendering tests is a complex task, but putting them into a single test library which turns out to be a dead-end due to excessive compile times is an additional time sink you have to accept. Why it takes some experience to see dead-ends right away, often you have to do some extra work to make sure that you solved the complex task correctly.
- Putting in the hours: Programming takes time. There’s no kidding yourself that you can skip work by doing something really fast. Writing all these functions, documentation and unit tests requires you to spend hours. While there are days where you only have one commit with just a few lines of code changed, you should typically commit lots lines of new or improved code every day. Each new feature means more code, tests and documentation. Even most refactorings which results in a net reduction usually require some new code and then changes in lots of places. All of this takes a lot of time.
- Seemingly stupid tasks like building your code base from scratch on another machine have a high risk of taking longer than expected, due to obscure problems. These tasks either take exactly as long as you have planned for, or much longer, but they are never faster. I found it best to do those things on Friday.

So much for today! I’m curious to hear how you track your productivity, and if you have spotted similar patterns to me.