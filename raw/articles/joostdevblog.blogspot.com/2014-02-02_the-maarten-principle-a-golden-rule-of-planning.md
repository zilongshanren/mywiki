---
title: 'The Maarten Principle: a golden rule of planning'
url: http://joostdevblog.blogspot.com/2014/02/the-maarten-principle-golden-rule-of.html
author: Joost van Dongen
published: '2014-02-02'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Ronimo](http://www.ronimo-games.com)for years now and although I won't claim that they are always correct, I have definitely learned a lot so far. One of the most important things I learned is what I like to refer to as

*The Maarten Principle*, which I would like to discuss today. The Maarten Principle is named after Ronimo programmer Maarten who first coined this concept.

An important part of planning is trying to figure out how long it is going to take to build something. Scrum extremists might have you believe that you don't need to do this since your game is always finished and just getting better over time, but in practice there are a lot of things that you just

*have*to do to make the game releasable. Implementing console certification requirements is a good example of a task that cannot be skipped, but usually there is also a vision for the game that just requires a certain amount of features and assets to make it a good game.

To have any idea how much work is left to finish the game, we need some kind of schedule. At Ronimo the core of the schedule is basically just a long list of everything that still needs to be done. We might change this schedule at any time, but we try to always keep it up to date with our current plans for the game.

To use this list to estimate how much work is left, each task needs an estimate of how long it is going to take to complete. Coming up with good estimates is the most difficult part of making a schedule, and we have gathered a bunch of tricks and guidelines through the years to help us make decent assessments. Unfortunately our estimates are still often not correct, but at least they are a lot better than they would be without these guidelines.

The most important of these guidelines is The Maarten Principe, the topic of today's blogpost. Its basic formulation is sarcastic:

![Anything can be finished in two weeks](../../assets/6bd49d3d4243760a.gif)

The more elaborate way of saying the same thing is this:

![No matter how big a task, it always feels like it can be completed in two weeks](../../assets/e9f7ddce7602564b.gif)

The point of this rule is that when estimating a complex task that takes a lot of work (like for example implementing matchmaking in an online multiplayer game), it is impossible to make a decent estimate for the task as a whole. Two weeks feels like a long period in which you can do a lot of work, so for many big tasks it feels like it can be completed within two weeks, even if the feature in practice turn out to take much longer to implement. Distinguishing between tasks that take two weeks, three weeks or one month is incredibly difficult.

We learned this lesson the hard way. Halfway development of

[Awesomenauts](http://www.awesomenauts.com)we made a task overview with all the coding work we had left. This schedule contained a lot of large tasks (PS3 matchmaking, 360 matchmaking, bandwidth optimisation, performance improvements, menus, etc.) and in the end every single one of them turned out to take way longer than we had estimated in that overview. Development of Awesomenauts turned out to take three full years while we had planned this to be much less, so this was a huge mistake that back then caused our studio a lot of problems.

The problem with this schedule became very clear whenever we arrived at an actual task. Say for example we had estimated that implementing menus took 10 days of work (I don't know the exact estimate we had at the time, this is just an example). As soon as someone was to actually work on this task, we split it up into all the screens the menu needed and all the general systems we needed to make menu screens. We then estimated how much time each of these smaller tasks would take. It turned out that they added up to much more than the original estimation for the job as a whole!

This is a pattern that we have seen time and again: whenever a big task is split into smaller tasks, it turns out to take much more time than expected, often twice as much or even more. If we split up the task into smaller subtasks much earlier, we get a way better estimate of how long it will really take to implement. In our experience the problem is not so much that the task is too far away to give a good estimate, but more that the task is too big to grasp its complexity well enough to give an estimate.

![Whenever a big task is split into smaller tasks, its estimated size grows a lot](../../assets/8244561ff590408f.gif)

Since I have so far mostly been responsible for the coding schedules at Ronimo, one might assume that this is just a problem with programmers (or maybe even just a problem with programmers

*at Ronimo*). However, I recently helped our lead artist Gijs to make the art planning and I saw the exact same thing happening. We wanted to split several big tasks of dozens of days each into smaller tasks, and adding those all up immediately grew the total estimated time a lot. Just as it does with the coding estimates, splitting a big task into smaller subtasks immediately grew the expected time to finish it.

I still cannot claim that The Maarten Principle goes for any game studio, but I can definitely say that it does not apply only to programmers.

Based on The Maarten Principle we always try to split bigger tasks into ones that take at most 3 days to complete. At a maximum of three days per task it is still very doable to imagine all the things that need to be done to complete that task, and thus to make a decent estimate of how long it takes to complete. For tasks bigger than that, we try to split them into smaller tasks until each is at most 3 days. Of course this is sometimes impossible to do, as more information might be needed to have any idea how to split a big task. But in practice, most tasks can be split into smaller tasks quite easily.

![3 days is the maximum size of a task that can be reasonably estimated](../../assets/5914e1b262ece849.gif)

Following The Maarten Principle does not grand one the power to make perfect schedules, but this rule does help us a lot in making better estimates!

Very recognisable problem, and interesting solution. So far I've countered it by spreading... maybe entropy is a decent word for it. My global estimate of all of the work is usually far more accurate than the estimate of larger tasks put together, perhaps due to previous experience with projects of similar scope. Of course this only works if the features don't expand during development, which they always do, which is another interesting tidbit I encountered: the longer you drag out development, the more features will expand.



ReplyDeleteThis was especially noticeable when we had a tech problem that took a long time to fix (so no features were being updated at all in the current build), at which point the design of the game had pretty much completely changed.

The biggest problem I've encountered with estimates is when you have to do something you've never done before. The second biggest problem is that we tend to do this all of the time.

The last paragraph makes for a great quote! :)


DeleteJudging a project by its complete scope is an interesting approach, but I guess we will have to do many more projects to make that work. We only finish one game every few years, so gathering projects to compare to goes very slowly that way... This will work better for teams that finish at least several games per year, I expect.

Planning is a world of pain. I think the whole thing is kind of futile, even with the best planning technique it is hard to get it right within 20% (assuming that is your contingency). At the same time it is essential, you must go through the process to keep your development realistic, as long as you keep in mind that your plan isn't always correct.



ReplyDeleteI prefer a hybrid format, somewhere between scrum and waterfall, where you separate the core features from extension goals, and remain fairly agile.

At the end of the day, everyone always knows what their budget is, this is usually fairly fixed so the point of planning is to make sure what you are working towards isn't entirely unrealistic.

great article by the way :-)

DeleteAfter years of planning, I have concluded the same thing: a planning is never perfect. We now consider it a living breathing thing that is constantly updated with whatever new information we get. So it might not be perfect, but at least it is always as informative as it can be and helps us make decisions. In other words: it helps us cancel features in time... ;)

DeleteGood article - it reminds me of Joel Spolsky's Evidence Based Scheduling article (http://www.joelonsoftware.com/items/2007/10/26.html) where the cut off is 16 hours!

ReplyDeletei just love devs blogs...thanks!

ReplyDelete