---
title: Tencent's genAI animation tools don't seem to make games more fun
url: https://www.gamedeveloper.com/art/tencent-s-genai-animation-tools-don-t-seem-to-make-games-more-fun
author: Bryant Francis
published: '2026-03-24'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/e427d8b5c9f968cf.png)


![](../../assets/e427d8b5c9f968cf.png)

**GDC Festival of Gaming (March 9-13, 2026) **

Keep up with the latest news, interviews, talk coverage, and other game dev insights from GDC 2026 right here on Game Developer. __Read More__

# Tencent's genAI animation tools don't seem to make games more fun

Tencent's generative AI tools shown off at GDC are technically impressive, but do they offer anything for developers?

![A character from The Hidden Ones looks at the camera, their hand raised. A character from The Hidden Ones looks at the camera, their hand raised.](../../assets/f722fd8c192f5658.jpg)

## At a Glance

- Tencent showed off a number of generative AI tools at GDC, including one for improving dynamic in-game animation.
- The technology was visually impressive—but the company's presentation raised questions about its effectiveness.

Taken in a vacuum, the demonstration for Tencent's generative AI animation tool is really cool.

Let's cast aside [developers' doubts](https://www.gamedeveloper.com/business/devs-are-more-worried-than-ever-that-generative-ai-will-lower-the-quality-of-games) about genAI for just a moment (of which there are many) and examine what this tool promises to do. At the 2026 GDC Festival of Gaming, Tencent was on hand to tout a number of its AI tools, including tools for AI-generated voices and genAI-powered NPCs. Elvis Liu, head of AI at Tencent subsidiary MoreFun, sat with down with Game Developer to show us his studio's tooling (which he'd presented earlier in [a sponsored GDC session](https://schedule.gdconf.com/session/the-hidden-ones-real-time-ai-generation-of-kung-fu-motions-presented-by-tencent-games/917893)).

It was the kind of "before-and-after" comparison that you visit GDC to see. The tool in question isn't used to create whole animations, but to dynamically create in-between frames for animations in a way that theoretically allows for more "realistic" movement with less clipping, sliding, or other animation imperfections players have grown used to due to the limits of game animation.

In one clip from the 3D action fighting game [The Hidden Ones](https://playthehiddenones.com/), Liu showed how the team first used "math-based" procedural frame generation. In it, a swordfighter took a hit from their opponent, and their sword clipped through their straw hat. In a second clip using the AI animation tech that showed the same strike, the swordfighter's blade swung around the hat. Liu said that after the game's open beta, players responded positively to a survey, broadly saying that The Hidden Ones' animation was "quite good."

I didn't doubt the veracity of that feedback. But as Liu described how the process worked—the low-budget motion capture tools, the kung fu artists hired to generate training data, the "lots of PhDs" plowing away on making this tech—I found myself unconvinced this technology would open new doors in game development.

Truthfully—for all the impressive under-the-hood work—it seemed designed to polish up elements most players don't notice in order to boost Tencent's prospects for investors viewing it as an AI-first company.

## How do Tencent's genAI animation tools help game developers?

Liu's pitch about these generative AI tools was not, thankfully, not entirely about productivity. What he hoped for was that tools like this could help game developers present more authentic animation, so in-outfit clipping and "slide" animations—where a character performs an animation as though they were standing while sliding across the environment—wouldn't occur.

A fighting game seemed like a strange title to showcase this technology with. Fighting games do have very precise animation but top-tier players inherently know they're playing a game intensely focused on frames and hitboxes. Your standard fighting game isn't made any better by tweaking the animations, there are core design principles that already promote visual clarity. Any jank from optional outfits isn't necessarily something that ruins the player experience.

But I'll meet Liu halfway. We do have games where the exquisitely precise position of a weapon does matter. Watch any clip of FromSoftware's [Elden Ring](https://www.bandainamcoent.com/games/elden-ring) and you'll see how enemy weapons are essentially always "on" when it comes to collision, so a stray swipe can send players flying even if it's not part of a major attack.

We also have games like WarpFrog's [Blade and Sorcery](https://store.steampowered.com/app/629730/Blade_and_Sorcery/), which boast "fine hitboxes" that again factor into the core gameplay. So we do know games tracking the precise position of weapons and limbs are fun...we just already have the tools to make them.

The pitch about preventing "sliding" animations proved even more confusing. To be fair, there are instances in games where characters perform standing animations while moving that look downright unsettling. Everyone from players to developers understands those are out-and-out bugs.

But sliding is also sometimes a desired visual effect. Games inspired by anime are already aping an "unrealistic" art style, and there is the classic visual trope of a character blocking a hit and being sent sliding on the ground. That's a stylistic choice (one born of how animators must carefully manage how many keyframes they make to stay in budget).

Once again, this seems to be a case of a tool papering over an uncommon problem in game development rather than creating fundamentals for fun. Players may appreciate these visual quality-of-life improvements—but would they do so if they felt the cost of implementing them?

## What are the downsides of Tencent's genAI tools?

There are few questions I try to have game developers answer when examining their generative AI tools. These questions reflect the documented harm generative AI has done in the years since Midjourney and ChatGPT opened the floodgates to widespread genAI adoption.

What data was the genAI tool trained on, and who held its original copyright?

Is your tool intended to replace workers (even if it can't hit the quality bar of a trained game developer?)


Liu seemed to anticipate my questions, explaining that the AI processing happens on the player's device (and was trained on local devices, not in data centers), that Tencent owns all the training data, and that this tool can accomplish what a team of animators could not.

Fair enough. Except—let's go back to the training data for a moment.

Tencent's genAI animation tool uses motion capture data provided by real kung fu practitioners. The data was captured using AI-based motion tracking technology that could organically capture a performer's movements on a far smaller stage than what's used in big-budget capturing facilities.

(Someone here might point out that eliminating the need for capture facilities could kill development jobs. But low-budget motion capture [has been possible for many years](https://youtu.be/QIOQNs-QCVg)...without using AI tech. I'd just point out that different games need different sorts of motion capture data and leave it at that).

After we spoke, I recalled a 2018 interview with [martial arts movie star Jet Li](https://www.avclub.com/jet-li-turned-down-the-matrix-sequels-because-he-didnt-1829855867) where he explained why he turned down a role in the Wachowski's sequels to The Matrix. He explained that Warner Bros. wanted to contract him for nine months. He'd spend three months on set with the cast, then six months with a motion capture crew gathering video footage of his moves so they could be used in CGI setpieces.

"For six months, they wanted to record and copy all my moves into a digital library," he said at the time. "By the end of the recording, the right to these moves would go to them."

"I was thinking: I’ve been training my entire life. And we martial artists could only grow older. Yet they could own [my moves] as an intellectual property forever. So I said I couldn’t do that."

Eight years later, here was a Tencent engineer telling me how the company was doing the same thing in a faster timeframe. He declined to comment when I sent follow-up questions over via a PR representative.

Now we can split some hairs. Jet Li is a camera-ready martial arts master whose signature moves literally sell movies. Are generic kung fu moves performed by everyday martial artists worth anywhere near the same value?

On a film screen, probably not. But in the world of generative AI, Tencent likely hopes that these bargain-value performances can bring in millions of dollars by wowing players with realistic animation. If martial artists were aware about the game's expected ROI, surely they'd have reason to pause, just as Li did, and think about whether they're being fairly compensated for their work.

This dynamic is not just a challenge in the world of generative AI. Performers of all types have fought hard to keep their craft from being erased by generative AI, and more niche artists like "[face models](https://www.gamedeveloper.com/art/how-should-face-models-be-compensated-in-video-games-)" have pressed the topic of fair pay. If your face—or martial arts skillset—becomes a key part of a billion dollar franchise, isn't it worth more than a slightly-above-average day rate?

## Technology should drive gameplay, not use games to justify its existence

My conversation with Liu took place on the same day I visited Nintendo's talk on the destructible voxel-based environments of Donkey Kong Bananza and [spoke with](https://www.gamedeveloper.com/design/how-voxels-enabled-a-juicy-gameplay-loop-in-donkey-kong-bananza) producer Kenta Motokura and programmer Tatsuya Kurihara about the link between game technology and gameplay. I left that conversation with a clear perspective on how experimenting with voxel-based environments shaped the level design, combat, and other interactive elements of Donkey Kong's newest romp.

By contrast, Tencent's generative AI tool left me feeling rather hollow.

We're in the age of [friendslop](https://www.gamedeveloper.com/business/peak-co-developer-aggro-crab-shares-lessons-in-friendslop) and [jank](https://www.jank.cool/what-is-your-fondest-memory-of-jank-14-game-devs-tell-us/), where games with low-fidelity graphics are just as appealing as slick, big-budget titles. When one of the most popular games in the world is Roblox, there's plenty of indication that you don't need to race for realism if you can execute on strong gameplay fundamentals and a strong artistic vision.

That doesn't mean we need to disregard games with strikingly realistic animation, but we do need to scrutinize what is gained by using genAI tools to produce it.

Liu and his colleagues have produced a fascinating bit of software that could make some kinds of animation newly feasible. But with no clear vision about how it makes games fun—and no answers about how the martial arts performers were compensated—those efforts feel frankly misplaced.

Game Developer and GDC Festival of Gaming are sibling organizations under Informa Festivals.

Read more about:

[GDC Festival of Gaming](https://www.gamedeveloper.com/keyword/gdc-festival-of-gaming)

[Generative AI, Machine Learning, & LLMs](https://www.gamedeveloper.com/keyword/generative-ai)

[Tencent](https://www.gamedeveloper.com/keyword/tencent)

[Top Stories](https://www.gamedeveloper.com/keyword/top-stories)

[Interviews](https://www.gamedeveloper.com/keyword/interviews)

[Features](https://www.gamedeveloper.com/keyword/features)