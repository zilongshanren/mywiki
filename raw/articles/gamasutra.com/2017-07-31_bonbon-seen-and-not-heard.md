---
title: 'Bonbon: Seen and not heard'
url: https://www.gamedeveloper.com/audio/bonbon-seen-and-not-heard
author: Nick Bell
published: '2017-07-31'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Bonbon: Seen and not heard

Bonbon is a work-in-progress short-form narrative horror game. This is the story of how a badly planned feature became a serendipitous mechanical metaphor at the eleventh hour.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

[Bonbon](https://aethericgames.itch.io/bonbon) is a work-in-progress short-form narrative horror game, by Aetheric Games. I've been keeping a devlog on the itch.io page, here are some links.

[Toys and Textures: a few production notes](https://aethericgames.itch.io/bonbon/devlog/2339/toys-and-textures-a-few-production-notes)[Animism and Procgen](https://aethericgames.itch.io/bonbon/devlog/2972/animism-and-procgen)[Preschool Reticule](https://aethericgames.itch.io/bonbon/devlog/4453/preschool-reticule)[Trailer... Release date... Cost..?](https://aethericgames.itch.io/bonbon/devlog/5446/trailer-release-date-cost)


The post below is the final devlog before Bonbon is released for Windows on 4th August.

This is the story of how a badly planned feature became a serendipitous mechanical metaphor at the eleventh hour of the development of Bonbon.

For once, I gave myself enough time for beta testing. As a single developer with no budget, that means a very select few people trying the game out on the two machines available. I hope that turns out to be less risky than it sounds: Bonbon is a short narrative game that has virtually no mechanics, uses a 3rd party engine, is launching initially on Windows only, and what systems it does have were tested and locked down weeks ago. This past week and the upcoming one are for repeated proof reading and looking for low-cost opportunities for extra polish. Aetheric Games is having a comfortably small-fry beta.

[Edit: It turned out in the end there was a little further play-testing by Joel Goodwin, and his feedback was very useful in making an important last-minute update. Kudos to Joel.]

It nearly didn't happen like that. Just a few days ago a long-planned central feature was almost cut and then reinstated. This post is about how things nearly got very messy.

The final stages of the dev plan were to go over the writing and record dialogue. Placeholder dialogue was already in the game, so that just needed a polish. Recording the dialogue was relatively painless. It's kind of a thing that when Aetheric Games needs to record vocals, my wife and I do the voice acting. It's not that we're amazing voice actors or anything, but I think we're decent enough. It started when I made a mod for Amnesia: The Dark Descent called The Trapdoor. I recorded a lot of dialogue in a particular affected Victorian chap voice that I'm surprisingly well practised in, and my wife delivered some excellent lines too and it all came off rather well, so it stuck. But anyway, the main thing is that, as I mentioned, there's no budget for actors for Bonbon.

There are three characters in the game with recorded VO (well technically there's four if you count Bonbon himself, but those sounds were already in the bag) - there's Mummy, Daddy and the player character, a three year old child (whose gender is not specified). As you may know from previous posts, the child protagonist personifies the toys. And even though you don't talk to adults, you can talk to the toys in single lines, e.g. "Hello Bouncy Hopper!" You can also talk to Bonbon with similar single lines. This feature was planned very early on. As well as voices, MrsBehemoth also contributes to the design process because I bounce ideas off her and she gives super useful feedback and her own contributions. Being able to say a well timed "No, Bonbon!" or "Go away, Bonbon!" came up in the very first discussion.

And was then promptly forgotten about. I would sort that out when it came to recording. We knew I would voice Daddy, my other half would voice Mummy, and one of us would do a kiddie voice. Easy. We're both good at voices. Nope.

We recorded several takes of all the adults' dialogue, and it was fine. My dear lady wife recorded some of the lines for the kid. We listened back. We tried some filters. Raised it a tone and a half. Hmmm. Not sure about this. I tried a few lines. Hmmmmmm. Tried some filters. Oh dear. It wasn't great, at all. Not wanting to come away without any material for the kid, I persevered. I affected the best voice I could. I rammed words out of my mouth in that way that toddlers do when they are tripping over their tongues with frank and unrestrained patterns of stress and pitch. It was exhausting.

I spent another 6 hours trying different combinations of filters and editing to get it sounding as good as I thought I possibly could, then the next day got it all imported, scripted and set up for the system of the game that mixes it with a distorted version at certain moments. This system is the system that I am specifically not calling a "sanity meter", because it doesn't exactly symbolise a lack of "sanity" but rather a traumatic lack of comprehension and agency that comes with being a small child in an adult world, but it's virtually the same idea. At times when the kid protagonist's comprehension and agency are most threatened, the speech comes out garbled, as well as some visual effects. With the player vocals in place, I started up the game and tried talking to some toys.

I hated it. The garble/distortion was fine when it was in effect, but the acting was not. An adult voicing a child character convincingly is no mean feat. No matter how hard I had tried, no matter how "good" I am at "doing voices", no matter how carefully I'd tweaked the filters and editing, I'm not a trained actor. But with no budget and time ticking away, it was all that could be done. The only other option was, gulp, cut the feature all together.

The next morning I had decided that there was in fact only one option. That feature, the one where the kid talks to things, the one that had been planned right from the start, it would have to go. But would it? Yes. But no! It felt too brutal to make such a heavy handed cut. I didn't make any changes for another day and a half, because I didn't really want to lose the feature but felt that it ought to go.

I put some mental effort into trying to diegetically justify the cut, for my own sanity. It did make sense for the protagonist to be silent. After all, what voices do children have, in the socio-linguistic sense. The child in Bonbon is very much "seen and not heard", whereas the adults are "heard and not seen". The kid's lack of a voice would symbolise his lack of comprehension and agency... And then the solution presented itself, very neatly. It was a very small change to make it so that whenever the protagonist tried to speak out, the "not-a-sanity-meter" effect kicks in, and the speech, whatever the situation, comes out garbled. Which is an even better solution.

And most importantly, instead of sounding like a garbled 35 year old man, it sounds like it might just in fact be a garbled 3 year old kid.

There are two lessons I am taking away from this. The first is that I am not an actor, and the next game that I make, if I don't suddenly have the oodles of cash to hire professional actors, and I'm almost certain that I won't, then I'll make it text-based. Games with lots of text-only dialogue are still doing fine.

The other lesson is that received wisdom is usually, but not always, right. Such as the idea that if something doesn't work then you just cowboy-up and put it out of its misery, well, it might recover and go out to pasture, or some other, more appropriate, extended metaphor. If you're not confident that a change is right for your game, then sit on it, sleep on it, take it into the shower. Try it on with different shoes. Find ways of justifying the changes within your vision of what your game is going to be. If I had done what I felt I was supposed to do, and cut the feature right away, then a central pillar would be missing and I was scared that the game would suffer. But, since I sat with that fear for a while, serendipity presented what I hope is a better idea.