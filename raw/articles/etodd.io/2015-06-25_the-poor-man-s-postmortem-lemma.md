---
title: The Poor Man's Postmortem - Lemma
url: https://etodd.io/2015/06/25/poor-mans-postmortem-lemma/
published: '2015-06-25'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# The Poor Man's Postmortem - Lemma

The big secret of our industry is, we don't actually enjoy making games. We slave away in obscurity for years in anticipation of one glorious day.

Not release day, no. The day we can finally write a postmortem full of pretentious anecdotes, bad jokes, and unsolicited advice.

Well I just finished a game, and doggone it, I am going to exercise my inalienable rights as a developer.## Things to do when making a game

Ancient gamedev postmortem traditions mandate that this section be titled "what went right". Unfortunately, the game was so shockingly good and so many things went right that a full overview would stretch on endlessly.

Instead you'll have to settle for this. These are some things I did that I recommend you do as well.

### Come up with a good concept

I didn't do this one, actually. The original concept was a
cartoony third-person game called [Parkour Ninja](https://etodd.io/assets/3qqRJqk.jpg).
It changed every other week or so for the remainder of development. For a
while the player had a pistol:

![](../../assets/bae8955aef55beb9.jpg)


![](../../assets/bae8955aef55beb9.jpg)

And for a while, you could rip voxels apart and re-attach them:

![](../../assets/1e83d14e59577f7b.jpg)


![](../../assets/1e83d14e59577f7b.jpg)

![](../../assets/c5b9eebdd8533ef8.jpg)


![](../../assets/c5b9eebdd8533ef8.jpg)

Almost everything got cut.

The final concept is not particularly unique. First-person parkour with a
female protagonist has definitely [been done before](http://www.mirrorsedge.com/),
and every third game on Steam uses voxels.

It worked in the end though, by combining familiar elements in a unique way, and by throwing in a weird, trippy, puzzle-y aesthetic. Every new idea steals from existing ideas.

![](../../assets/9c9db5168eda5691.jpg)


![](../../assets/9c9db5168eda5691.jpg)

In 2012 I released a short, strange, ugly, buggy alpha demo which
nevertheless communicated the core ideas of parkour and mysterious voxels.
Incredibly, Rock Paper Shotgun [covered it](http://www.rockpapershotgun.com/2012/02/28/island-hopping-lemma/).
I doubt I would have stuck with the project without that affirmation.

### Make it through Greenlight

I honestly have no idea how to replicate this feat. I don't know how it happened. Fortunately, Greenlight is much less daunting today than it was in April 2014.

I did almost nothing to promote the Greenlight page. I ran the campaign in tandem with a Kickstarter (more on that later), but almost all traffic came from Steam itself. Here's the embarassing trailer I used for both Greenlight and Kickstarter:

The game was greenlit in 16 days as part of a bundle of 75 other games, even though it hadn't reached the top 100 yet.

![](../../assets/84bfb24a0c9ec31a.jpg)


![](../../assets/84bfb24a0c9ec31a.jpg)

As you'll see later, if you want to make a living developing PC games, you have to get through Greenlight.

### Iterate the controls

My [character controller](https://etodd.io/2015/04/03/poor-mans-character-controller/)
article goes into much more detail on this, but basically, take however
much time you plan to spend on the controls, and then double it.

Use MIDI knobs to control game variables. [Explore the game space](http://game.engineering.nyu.edu/projects/exploring-game-space/).
Use offline processing to [bullet-proof your character controller](http://mollyrocket.com/casey/stream_0006.html).

This point applies to all games, even those that don't have a character. The player's action and the game's reaction are arguably the most important aspects of a game, because they are unique to the medium.

### Design your graphics carefully

Lemma has been pretty ugly for most of its life. I got lucky with a few textures in the 2012 alpha, particularly the stone texture which features heavily in the final game. But mostly I just slapped textures on haphazardly. Here are some perfectly good textures applied in the worst possible way:

![](../../assets/25f994f20e089b32.jpg)


![](../../assets/25f994f20e089b32.jpg)

At the time, I knew something was wrong with this scene, but I couldn't put my finger on it. Allow me now, with the benefit of hindsight, to put my finger all over it.

- Nowhere to climb. This is a claustrophobic indoor scene set inside some sort of derelict vessel. It belongs in Bioshock, not a parkour game.
- Too busy. The textures are incredibly loud and detailed while the voxels are huge, flat, and boring.
- No composition. Nothing draws my attention or invites me to explore. The shapes are all uninspired boxes.
- Abysmal lighting and colors. If I recall correctly, I randomly placed the red point light on the left on a whim.

Compare to this shot from the final game:

![](../../assets/b3b79d5ff37b0d54.jpg)


![](../../assets/b3b79d5ff37b0d54.jpg)

Still some rough edges, but not overly painful.

Here's what I learned to get from point A to point B:

- If you're like me, make up for your lacking art skills with code. God rays, SSAO, and particle effects worked wonders for me. And turn on mip-mapping for gosh sake.
- Form and composition are more important than detailed textures. You can make a beautiful scene with just a few carefully placed shapes.
- If you're trying to convey a massive sense of scale, your forms should have interesting features at every scale. A single, giant, featureless cube won't inspire awe. Neither will a giant cube with a detail pattern.
- Colors and lighting make or break scenes. I probably spent as much time picking (and re-picking) colors as I did building voxels.

### Support all the things

At the very least, add proper gamepad support. For me, Oculus Rift support was a huge selling point and a ton of fun for YouTubers.

Things like sparse options menus, missing gamepad support, and shoddy VR implementations enrage gamers, especially PC gamers. There's a reason TotalBiscuit starts every video with a look at the options menu.

I threw in every option I could think of, and almost every option requested by players. Y axis inversion, gamma, FOV, gamepad bindings, a framerate limiter, you name it.

### Get involved with the community

I almost lost it In January 2014. Shut in my apartment for days on end, stuck in a difficult rut in production, I was going insane.

Thankfully, Columbus has a budding game development scene. I rented a desk from a local gaming incubator. The mere act of driving to work and existing around other humans got me through the winter. As an added bonus, I gained a ton of playtesters!

![](../../assets/fd186749711de742.jpg)


![](../../assets/fd186749711de742.jpg)

Every month I attend a local game development meetup. As a solo developer, it's the only time I get to talk openly about the topic that consumes 90% of my life. Seeing the same people every month and catching up on their progress is incredibly rewarding.

For the rest of the month, there's Twitter!

### Do your own marketing

If you're like me, your marketing budget is $0.

On launch day, I spammed announcements to all of Lemma's accumulated fan base via Twitter, Facebook, IndieDB, GameJolt, Kickstarter, Steam Greenlight, YouTube, and an email list.

I spent several days collecting contact info by hand for various press and YouTubers. Whenever possible, I automated the process with Python and Javascript. Some resources I used:

[Video Game Caster](http://videogamecaster.com/)[Video Game Journaliser](http://videogamejournaliser.com/)[Top 100 YouTubers](http://vidstatsx.com/youtube-top-100-most-subscribed-games-gaming-channels)[Bolo](http://bolohq.com)- useful for digging up journalist email addresses

I pulled everything into a Google Docs spreadsheet and ran a
[mail merge](http://www.gamedev.net/blog/832/entry-2261072-pr-o-matic/)
on it two weeks before the launch. Somewhere around 400 Steam keys ended up
being activated.

YouTube ended up bringing the most traffic. Over [400 videos](https://www.youtube.com/playlist?list=PL-gEd0fjxH3W83gH2RJytYfh4JFRLZ5kU)
have been uploaded to date, totalling over 5 million views, mostly thanks
to three huge videos posted by jacksepticeye.

### Ship your localization strings in plain text

Lemma uses Excel files for localization. I use a [third-party library](https://github.com/ExcelDataReader/ExcelDataReader)
to read them, which makes the code [pretty simple](https://github.com/et1337/Lemma/blob/6ad035a3e2db3a91463a3b8c3859006ccbe0446a/Lemma/Strings.cs).

This ended up being a great decision, because foreign players step up with their own volunteer translations. They can edit the Excel files in place and see the results immediately in-game.

## Things to never do, ever

### Run a Kickstarter

As Greenlight becomes easier to conquer, Kickstarter becomes exponentially more difficult. Backers have been burned too many times by now, and everyone sets their goals much lower than the amount they need to deliver on their promises.

I ran [a failed Kickstarter for Lemma](https://www.kickstarter.com/projects/et1337/lemma-first-person-parkour)
in March 2014. Originally, I planned to abandon the game if the Kickstarter
failed. Then the Greenlight went through and I decided to cut back the
budget, take some contract work, and do some budgeted art items (namely the
character model) myself.

Running a Kickstarter takes too much time away from development. My advice is to find another way to fund your game if at all possible.

### Write a pretentious story

If you're making Deus Ex, feel free to go wild with gritty lore and philosophical questions about trans-humanism. But if you're making Flappy Bird, you can get away with maybe a 10 second cut scene, tops. Know how much story your game can "afford".

The story of Lemma features quantum mechanics, the [Philadelphia Experiment](https://en.wikipedia.org/wiki/Philadelphia_Experiment),
life and death choices, infidelity, betrayal, and jealousy. All this
crammed into 50 optionally collectible notes in a game about parkour.

The story tries to do too much. When all these conflicting ideas combine, they blur together into a jumbled mess that neutralizes the impact of each individual idea.

When it comes to story, do one thing, and do it well.

### Suddenly switch from linear to non-linear design half-way through

I planned this from the beginning, actually. The first half of the game is linear so I can introduce mechanics one at a time. The player knows everything by the second half, so the game opens up into a non-linear cornucopia of levels that review the things you've learned so far.

This is a pretty good pattern as far as pacing, but the linear to non-linear transition confuses players. The whole first half teaches you that there's one way to "win", then suddenly, you're dropped out in the cold and left to your own devices with a completely incomprehensible world map.

![](../../assets/ccadefb3fe2a1a46.jpg)


![](../../assets/ccadefb3fe2a1a46.jpg)

I did this because I thought, "this game is about exploration, it needs to be more non-linear". But all of the alpha releases were completely linear and not a single player complained about it. In fact, many of them commented that they enjoyed how each individual level could be cleared in many different ways.

The takeaway is, there are tons of ways to make your game feel more non-linear than it is, without building a confusing tangle of interconnected levels.

### Design bad puzzles

My worst puzzles break the game rules. If you have to write a custom script that manually pokes the game state when the player solves the puzzle, stop and re-think your life decisions.

I'm always worried that my puzzles are too easy and that players will breeze through them too quickly, but in reality it doesn't take much to slow players down.

Often, the simple act of exploring a 3D space is enough of a puzzle. Games like this are a continuous conversation between level designer and player. It's enough of a challenge for the player to parse what the level designer is saying.

### Throw in unnecessary enemies

Enemies have been a part of Lemma since day one. I love watching players encounter them for the first time, because they're truly terrifying. That small taste of horror shakes things up and fits perfectly into the pacing.

But after the novelty wears off, enemies become annoying and redundant. There's no combat; your interaction with them is always the same: run away.

My goal was always to integrate enemies seamlessly with the environment. In parkour, the environment is already your biggest enemy and your most powerful tool, so it makes sense. Unfortunately, I only came up with one enemy that came anywhere close to achieving this goal: a sort of tower that detaches from the environment and falls on you.

In hindsight, I should have been more confident in the core gameplay and remove the enemies to focus on better level design.

### Spend time on an unnecessary level editor

Some games benefit hugely from a level editor. Heck, Garry's Mod
*is* a level editor. If you're making that type of game, more power
to you.

If you're making a mostly linear, story-driven singleplayer game, a level editor doesn't make much sense. Everyone says "oh cool, there's a level editor", creates a few cubes, and then completely forgets about it.

Again: do one thing, and do it well.

### Start a hobby project and transition it to professional

Hobby game development is like building a tower of bricks. You don't know how tall it's going to be, you just keep stacking bricks. Each brick represents something that happens to interest you at the time. Branching dialogue? Sure, stack it on there. A pistol? Why not. Pretentious story? Check-a-mundo.

Professional game development is like sculpting. You start with a certain amount of raw materials: time, money, motivation, player attention, etc. You plan out a rough idea of your sculpture, then you start chiselling. The size of the sculpture is irrelevant if you put your chisel in exactly the right spot.

The two paradigms are incompatible. If you're a hobbyist looking to make the switch, consider starting fresh with a new project.

## Results

### Steam

The second spike in these graphs is mostly due to jacksepticeye's Let's Play videos.

### itch.io

![]() |

### Humble widget (direct website sales)

![]() |

![](../../assets/25707b0354c02a9b.png)

![](../../assets/25707b0354c02a9b.png)

### IndieGameStand

| Sales: | 4 |
| Gross revenue before 30% cut: | $57 |

### IndieDB

| Demo downloads: | 1,388 |

### Piracy

Lemma offers the option to [anonymously upload analytics](https://etodd.io/2014/02/19/the-poor-mans-gameplay-analytics/).
5,732 out of 13,410 demo downloaders (43%) actually opened the game and
opted in to the analytics program.

A total of 7,310 pirated copies of the game have submitted analytics data to my server. Assuming 43% of pirates opt in to the analytics, I estimate about 17,000 people have pirated the game, for a piracy rate of 82%.

The worst part about piracy is that torrents cannot be updated, which means YouTube is full of footage of old, outdated builds.

## Conclusion

![](../../assets/8af27595d7954422.jpg)


![](../../assets/8af27595d7954422.jpg)

- Schedule: 3 years part-time, 1.5 years full-time
- Core team members: 1
- Contractors: 6
- Budget: $30,000
- Sunk opportunity cost: $80,000
- Lines of code: 55,000
- Audio assets: 200
- Git revisions: 1,200

[Lemma](http://lemmagame.com) released May 12. The entire
game engine is [on GitHub](https://github.com/et1337/Lemma). If you
enjoyed this article, try these:

[The Poor Man's Character Controller](https://etodd.io/2015/04/03/poor-mans-character-controller/)[The Poor Man's Voxel Engine](https://etodd.io/2015/02/18/the-poor-mans-voxel-engine/)[The Poor Man's Dialogue Tree](https://etodd.io/2014/05/16/the-poor-mans-dialogue-tree/)[The Poor Man's Gameplay Analytics](https://etodd.io/2014/02/19/the-poor-mans-gameplay-analytics/)

Thanks for reading!