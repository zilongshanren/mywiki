---
title: Mac and Linux Support
url: https://etodd.io/2012/11/19/mac-and-linux-support/
published: '2012-11-19'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Mac and Linux Support

How's everyone doing? I'm doing okay. [It's a Monday.](http://www.youtube.com/watch?v=cZO9tMetxno) Hope you're doing okay too. Surviving Sandy aftermath, school, work, and whatever other forms of oppression you may be under.

I don't have anything pretty to show for the past... wow, it's been three weeks. I've been working on a very lofty addition to Lemma's feature bullet list. And that is **Mac and Linux support**, via the awesome [MonoGame](http://monogame.codeplex.com/) project.

Don't get too excited. There is a ton of work left to do before this becomes a reality. But after a few weeks' work, I do know a few things:

- It's possible. There's a lot missing, but all the code compiles against MonoGame, and a subset runs correctly.
- I'll have to implement a lot of necessary features on my own. I'll be pushing (or attempting to push) these features back upstream in to the MonoGame project for everyone else to enjoy. It's not as bad as I thought, though. I already completed one big feature (sampler and render states parsed out of .fx files) and am waiting to merge it.
- In the meantime, I have a build set up where I can quickly switch back and forth between XNA and MonoGame. I can continue developing game features under XNA while patching MonoGame on the side.

My plan is to focus primarily on the game code, and whenever the creative juices run dry, I can switch gears and knock out a couple MonoGame features.

It's pretty exciting contributing to MonoGame, as it's a very active project. I'm still new to the whole GitHub workflow, and it seems a bit wonky, but it's leaps and bounds better than anything else out there. Especially because *everything is on GitHub*. It's like Facebook. It isn't even that great, but the killer feature is that everyone uses it.

Anyway, this week I'll be getting back to game features. Expect pretty screenshots soon.

In other news, I'm roughly one month away from graduating, moving into my first apartment, and starting a real job. I'm worried that coding all day at work will slow progress on Lemma, so I'm trying to get as much work done as possible before then. Hopefully once I start work I can find a schedule that keeps me from burning out on Lemma, because I've come way too far to quit.