---
title: 'Stop being the Useless Designer: Programming'
url: https://claire-blackshaw.com/blog/2011/08/stop-being-the-useless-designer-programming/
author: Claire Blackshaw
published: '2011-08-25'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Stop being the Useless Designer: Programming](../../assets/4e402aebc4c1a4e8.png)

Let’s face it, there is nothing more annoying than being bossed about by someone who is useless.

![](/images/Blog/lazydesign-300x300.png)

Let’s face it, there is nothing more annoying than being bossed about by someone who is useless.[?](https://claire-blackshaw.com#foot1)

So here are three simple rules.

- Work with them in the trenches.
- Everyone in the trenches has to be useful.
- Supplement don’t Replace
[?](https://claire-blackshaw.com#foot2)

[?](https://claire-blackshaw.com#foot3)

### Part 2: Programming Skills

A designer does not need to be a programmer but understanding programming is key.

One of the most valuable but more expensive skills for a designer to acquire is programming. Brenda Brathwaite succinctly makes the point in her post, ["Built on a Foundation of Code – Game Edu Rant"](http://bbrathwaite.wordpress.com/2011/03/01/built-on-a-foundation-of-code-game-edu-rant/).

Where to start? While I would suggest [Codecademy](http://www.codecademy.com/) or [GameMaker](http://www.yoyogames.com/gamemaker/), because if, as a designer, you can get to the point of making digital games solo, it will exponentially increase the potential of your learning curve.

While researching this post I discovered [Codecademy](http://www.codecademy.com/), a brilliant introduction to programming with interactive. My tweet of my discovery (this was prior to it’s press coverage) spread like wildfire, I can easily say it was my most popular tweet out of the 3000+. This supports my belief that programming is fast becoming a life skill and I expect the basics should be included in schools in the near future. So I shall move past this point to less well covered ground.

Designers should be interested in Logic & Behaviours, not Code

At the end of the day the reason you need to understand code is because it’s the brick and mortar your game is built with. Though you want to continue to interact with it at the Logic and Behaviour level, you’re interested in how your game functions. Don’t get lost in performance or implementation, that is the job of the programmers and you should work with them to achieve the desired effect but not attempt to do their job.

Negotiate Policy with Programmers

Just as Designers don’t want unqualified doodles on their design specs, programmers don’t want the mad ramblings of a half trained programmer clogging up their code-base. You should work with your programmers and find a safe, efficient way of exposing as much game behaviour to the design team as possible in a safe manner which won’t damage the code productivity or quality.

You are part of the team, not an End-User

These solutions don’t need to be over-engineered, sometimes simple policy helps. For example, one of the easiest lo-tech ways to expose a bunch of balance numbers to designers is to have a game_numbers.h. This contains all the game constants in native code which the designer can edit, without fear of damaging everything or polluting the code base.

A similar approach can be taken with game logic. Exposing a function list to designers, and having all the game behaviours in a single code file, means that with a fairly basic programming knowledge the designers can craft complex behaviour systems or logical systems without the need for code support or complex tools.

The important thing is that it is an agreement, a policy and common sense which control these. As a member of the team you are trusted. Yes, under this system a designer could go into the code base and turn it all to goo but they won’t. You are not an end-user, you can be restricted by soft systems (policy).

Programmers like to Provide Solutions

Try to make it easy for your programmers. It’s easier for them to knock-up a basic text interface than a full contextual GUI. That being said good tools are the key and so often quoted in post-mortem. If you ever find yourself doing a repetitive design task, are frustrated with a process or are unable to “get at” the parts of the game you want then talk to your team.

Programmers like to solve problems and provide software solutions. If they have time and can see a way they will provide you with a solution.

Learn the Tools

If your studio has a scripting language, or a toolset which is used in developing content, learn it! It is your job to understand and learn that tool from start to finish. Find the manuals, if they are out of date, you should have them updated, if they don’t exist, get them written. If they have bugs, faults, or areas which need improvement, report them.

Someone has made the effort to build that tool, if you do not learn it and use it then you are wasting their time.

Get your hands dirty and own the tools. If your lucky enough to have sufficient programming skills you might even do a little minor tool maintenance, but ask permission first. The muddier and dirtier you get in the trenches, the more hands on your are with your systems the better you will understand them.

So here is to getting your hands dirty, your systems tuned and your game built.

[Post Series for #AltDevBlogADay](http://altdevblogaday.com/2011/08/25/stop-being-the-useless-designer-programming/)

## Footnotes

[#Please note: I’m not dismissing high-level design or the need to get an overview on the project but too often useless people use these as shields to hide incompetence.]

[#You have a team of specialists who will always have more time and expertise than you in many things. Look to understand their work, support them, and refine the design with your increased knowledge but never try do their job.]

[#Hard in terms of based on solid fact, brick and mortar stuff, as opposed to soft skills like communication and developing a feel for a product which can often be more difficult to master.]