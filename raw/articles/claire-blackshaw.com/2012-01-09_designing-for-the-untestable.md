---
title: Designing for the Untestable
url: https://claire-blackshaw.com/blog/2012/01/792/
author: Claire Blackshaw
published: '2012-01-09'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Designing for the Untestable](../../assets/4e402aebc4c1a4e8.png)

Sometimes you’re asked to design for the untestable scenario. For instance, design a system for 10,000 players to asynchrously interact in a persistent competitive world with progression mechanics that plays out over 3 months.

**Disclaimer**: The entire time you are reading this remember one basic truth or else everything else contained herein is useless.

Focus on second-to-second play first. Nail it. Move on to minute-to-minute, then session-to-session, then day-to-day, then month-to-month (and so on). If your second-to-second play doesn’t work, nothing else matters. Along these lines, if your day-to-day fails, no one will care about month-to-month, either. - Brenda Brathwaite

force map (mission impossible?)" by Yish![](/images/Blog/impossibledesign-227x300.jpg)


### 1st Rule: Be as Flexible as possible

Your toolchain and setup should allow for the quickest possible editing as possible as well as bulk editing. I highly recommend integrating a Python or Lua console which allows live editing of data and constants. If you can get sliders for editing or fast visualisation HUDS then all the better.Ensure that everything possible is loaded from data, the simple stuff like magic numbers to basic behaviours and conditions.

Everything should be in data explicitly. For instance if your original design states that the Weapon Strength is proportional to the phase of the moon and character level which can be expressed in a mathematical equation then DO NOT put the equation in code. Instead your data should contain the equation. There are several reasons for this the most common is when you discover a level is off balance. Then you can adjust level 22 without altering a complex equation which was used as the base-line.

Ensure that your data is robust enough to migrate between versions and survive minor alterations to the structure of the data. Sometimes you may need to throw away some data because it can’t be migrated but this should always be a last resort.

### 2nd Rule: Model It

Okay I lied, everything is testable but you need to be clever about it.Mathematical modelling is a process by which we take massively complex systems like population growth or oxygenation in the human blood stream. By monitoring the inputs, outputs and some control variables we can build an understanding of a system.

I know this all sounds like really heady stuff and it is a complex field but even a limited understanding can reap massive rewards. For example take a weapon in an action MMO. Given a weapon that has 100 different stats we can express a rating out of 10 in two areas, Speed and Damage, and our measurement is Kill / Death ratio. We could start by building regression fit by some data we have gathered, thank you [WolframAlpha](http://www.wolframalpha.com/input/?i=fit+20.9%2C23.2%2C26.2%2C26.4%2C16.3%2C-12.2%2C-60.6%2C-128.9). Though with a bit more effort we could model a 2D plane with K/D as the height which provides even more information. The richer the model the more you can learn.

Always remember the Lab is NOT the real world however.

I cannot strongly enough express the power of models in large scale designs for the broad strokes. Even better if you have a complex model you can create a simple representation of it using Python or similar to create a model which you can adjust in realtime. With simple visuals you can quickly see the potency of an action, such as rewarding a sum of gold in an early quest, can inject into the system.

I highly recommend all designers pick up a book on the subject and if lost ask your programming or financial department. I know that sounds strange but there are likely a few people there with the background to help you build a few basic models.

### 3rd Rule: Measure Everything

Of course all the above is useless without measurement. Everything is a datapoint. You must have the analytical muscle to get detailed data out of the system fast or else everything will always work from theory and feeling. Poor data will lead to instant failure.Which leads to a sub-rule which is never trust your intuition when dealing with large scale systems. Your common sense is built on very primitive immediate feedback. It’s great for telling you if a tiger is about to eat you or a date is going well but when it comes to massive mathematical systems more often than not it will lead you down dead ends and false leads.

Even if you’re certain about something, measure it and confirm it. That way you know with confidence that the simple stuff is true. Then when a complex system throws a wobbly you won’t waste countless hours because a basic assumption was false.

### 4th Rule: Speed and Automata

The ability to time-jump or accelerate the game-time can be immensely useful in complex systems.Ensure you can decouple rendering or else this is impossible. This is a basic, “Are your shoelaces tied?” question but it bears repeating.

Try making your time jump or acceleration as low level as possible. It should be as stupid and unaware of the game systems of possible.

Consider a delta of a month. I know it sounds crazy but try it. If your floating point math breaks, a number overflows, something clamps, or some code clamps or assumes a delta then that’s bad. Sometimes it can be helped, but then algorithmically (if possible) calculate the maximum time step and ensure you can’t overstep it. It’s also a good idea to pad this estimate to be safe.

Talk to your AI programmer; get an estimate for coding up in order: a random bot, a non-suicidal bot, a stupid bot, a reasonable bot, a perfect solution bot. The last one may not be possible but it usually is. Often a thousand random bots, while computationally expensive, are the best place to start. They will quickly identify edge cases or dead end scenarios. Bearing in mind that the smarter bots will be more prone to breaking when the game changes.

As the game becomes more stable it becomes more and more useful to have these bots around, even post launch. They will quickly let you thrash at a release candidate before letting it out in case you introduced an unstable equilibrium or exploding problem, bad designer no cookie!

### 5th Rule: Accept your Failure

After all this work you must accept you’re guaranteed to fail. What’s important is the size of the failure and how quickly and confidently you can adjust your system once it’s gone live.First step is build a bunch of predicated milestones and thresholds for your game. Setup alerts so the moment the live game is drifting outside those thresholds warning bells go off. The sooner you can address them the less likely the model is to explode.

**NEVER EVER ADJUST A VALUE WITHOUT UNDERSTANDING IT!!!**

This is fine in the lab or experimentation phrase but once things are live and you’re working on a live game you need to understand every nuance of that value. Your models will help here along with clear documentation. It’s helpful to have a rough graph or visual for how the value will propagate out into the system.

Without this knowledge you could just be making things worse. Honestly this is where the true value of your understanding of the systems and numbers behind your impossible system come into play.