---
title: 'Classic Postmortem: People Can Fly''s Bulletstorm'
url: https://www.gamedeveloper.com/audio/classic-postmortem-people-can-fly-s-i-bulletstorm-i-
author: Adrian Chmielarz
published: '2016-02-22'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

On the fifth anniversary of the release of this unique and underappreciated shooter, Here's an in-depth postmortem that first ran in Game Developer magazine in 2011. It was written by Adrian Chmielarz, who was creative director of People Can Fly.

What could go wrong if your first project is an unassuming old-school PC shooter, and your second project is a big, multiplatform AAA title? Why would things be different if you grew from 15 to 70 employees in a couple of years? How does it feel to go from e-mail interviews to standing in front of the entire world as it watches your live E3 presentation?

Yeah, this could be a book.

Ten thousand things went right and ten thousand things went wrong during the production of Bulletstorm. Obviously there's not enough space to talk about them all, so this article is a very subjective selection, mostly filtered through the design side. It took three and a half years to make Bulletstorm. We've learned, we've grown, and we hope you'll find something for yourself in this story as well.

BULLETSTORM

PUBLISHER: Electronic Arts

DEVELOPER: People Can Fly/Epic Games

NUMBER OF DEVELOPERS: Around 80 at PCF

LENGTH OF DEVELOPMENT: 3.5 years

RELEASE DATE: February 22, 2011

SOFTWARE: Unreal Engine 3, 3ds Max, Maya, Photoshop, Modo, ZBrush, Motion Builder, MS Office

PLATFORM: Xbox 360, PlayStation 3, PC

# WHAT WENT RIGHT

## 1) Focus on core combat loop

///Our philosophy is that it’s better to have a great game that’s just about spitting than a mediocre game about spitting, screaming, and playing the banjo.

If you have ever sighed at a game’s attempt to offer variety (e.g., not every game needs a driving section), you already know what I mean.

Also, stop thinking about that banjo game. It’s not going to happen.

We spent months polishing our core combat loop: shooting, kicking, sliding, leashing. A millisecond here, a 1% more transparent particle there. Improve, playtest to death, rinse, repeat. We knew it all worked together well when we started missing elements of our CCL while playing other games. I cannot count the amount of times I wanted to kick or slide into an enemy when enjoying a competitor's FPS.

Of course, modern games cannot rely on the CCL alone, but we also don't think that having myriad core features is the right solution. You will never have the time to polish them all properly.

We decided to focus only on the crucial ingredients, get them to 100%, and have the gameplay variety come from a wide palette of contexts to the CCL. For example, the kick is always the same thing—the same animation, the same sound, the same button—but its purpose can change depending on what the player needs to do. Kick to push an enemy away. Kick to destroy an enemy's armor. Kick to open a door.


2) Pacing and balancing pass

/// As with most games, Bulletstorm was built by multiple level designers, each working on their own fragment of the game. At a certain point we felt that every level had really great pacing: a good warm-up, varied encounters, and an interesting cliffhanger.

Most of the levels were done with “big picture” pacing in mind. For example, the Cave level started slow, because the ending of the preceding level was a six-minute boss fight, and we wanted to let players relax a little.

But as all game designers know, theory is one thing, and the actual implementation is another. When we put the game together, some pacing problems immediately crawled out of the woodwork. The Cave's relaxed opening was a good idea, but lasted far too long. The Underground and Ulysses sections were great on their own, but both exclusively featured one type of enemy (Burnouts), and that was tiring in the long run. The Dam level felt too long, even though in isolation it was one of the best levels in the game.

We made pacing and balancing our priority. We removed and added battles. We shortened cinematics. We fine-tuned all the values for ...everything.

In the end, we got a really well-paced game. Unfortunately, it was a little too well-paced for its own good. Wait, what?!

Imagine a shooter or a horror game that takes eight hours to finish, but where the experience is so intense that you only play one to three hours daily. It means it will take you three to five days to finish the game, which is how we imagined our game would be.

However, with Bulletstorm, we have seen time and time again that people got so engaged in the experience that they finished the game in one day. It was still eight hours, but played in only one or two sessions. That allows us to enjoy the fact that over 50% of players finished Bulletstorm, which is higher than the industry's standard (this is easily trackable by checking “Finished the game” achievements in services like Raptr—see References for more). But at the same time, opinions started floating around that the game was short.

It was not short by current standards. But to gamers, two four-hour sessions are not the same as five hour-and-a-half sessions.

We are still proud of the pacing and balancing work, but intensity versus time is something we’ll have to think about in future projects.

## 3) Finding the fun through early focus tests

/// We never planned to offer a unique gameplay hook. We just wanted to evolve the genre a tiny bit. Maybe we’d do it by unmuting the main hero, even though it’s a first-person game. Maybe we’d differentiate by making sure that the sidekicks are not automatons spewing context-sensitive comments, but actual people we can have strong feelings about. Our intentions were nothing more than that. We just wanted to offer a fun high adventure—that's it.

However, the aforementioned focus on the core combat loop, constant iterations, and—most of all—internal focus tests led to the invention of Skillshots.

I am a big fan of games that offer multiple pseudo-independent systems. That is the core of any emergent gameplay. Bulletstorm has a few systems like that: multifunctional weapons (e.g., the flail chain can wrap around enemies or objects), an interactive environment (e.g., the explosive trash cans of the future can be moved around) and the tools of war (kicking, sliding, leashing).

Players can manipulate and use these systems any way they want. That leads to a lot of emergent gameplay moments. You can kick an enemy into a trash can, which then explodes, which causes another enemy to go airborne and get pierced by a rocket fired by another enemy positioned on the rooftop.

But I would never have thought of naming these crazy actions—and indeed, I would never have thought of Skillshots at all—if not for internal focus tests.

To some developers, the focus test sounds like something to dread. They think: “There’s a reason why I’m the creator, and they’re the consumers.” That’s fair enough, and there is some truth to it; but on the other hand, there’s also a reason why Blizzard wins so big after spending insane amounts of time playtesting and fine-tuning.

Our early focus tests were nothing official. We were just watching each other play. In casual conversations we debated what was fun and what sucked.

But it was during these monitored play sessions that I noticed people were using Bulletstorm's emergent combat not to be efficient, but to have fun. A headshot is a much faster kill than leashing an enemy toward you, then kicking him into a cactus. And yet still people kept on doing that, and even much more elaborate things. They were experimenting. Testing theories. Having fun.

“Hey, why don't we actually reward people for being creative?” I thought. “How about we call it a Skillshot system?” And one of our core selling points was born.

## 4) Many companies, one game

/// You can imagine the fragmentation challenges we faced with PeopleCanFly as the main developer and creative owner, Epic as co-developer and quality enforcer, and EA as the publisher. And there were a number of additional companies from all around the world helping us as well (in Germany, USA, China, Sweden, and Poland).

This stuff is not for the faint of heart.

Oddly enough, coordinating the outsourcing was not the hardest part. With good, dedicated producers in place, it’s actually something I am sure to repeat in the future.

It was the PCF/Epic/EA cooperation that caused the most problems. Everybody was equally important, and everybody could influence any part of the development process: design, production, and so forth. For example, both EA and Epic were giving us independent feedback on the milestones and playable builds. It was a mess.

Fortunately, we all noticed that very quickly. We understood that the key to fluid cooperation is a proper distribution of roles and responsibilities. In other words, sometimes you have to let go.

We immediately streamlined all these processes. Using the feedback example, EA was no longer sending feedback to PCF but to Epic. Epic then merged EA's feedback with its own, empowered to remove whatever they disagreed with, and then sent one unified chunk of feedback to PCF. This way we only had to deal with one source of feedback, were no longer prey to multiple masters, and stopped worrying about the priorities of the feedback items.

If you are working with several partners, letting go is the key. One of you knows more about the marketing than the other, another is a better judge of quality. Clearly define who is responsible for what, and make life easier for everyone.

## 5) Unreal Engine 3

/// Ha! What a surprise: a guy from a company owned by Epic, creator of Unreal Engine, praising the Unreal Engine. Good one!

In 2004, we released Painkiller. The game took two years to make, with a 15-person team (on the average). We had a long single-player campaign, and a fun multiplayer mode that was a CPL (Cyberathlete Professional League) game of the year. And we did all that using our own engine, which we created from scratch.

Painkiller was really an extremely simple game at its core, though, and yet still we struggled. We had to outsource cinematics in order to finish the game on time, for example. If it had been any more complicated—and I am not talking about big stuff like going multiplatform, I merely mean things like featuring a sidekick—the game would never have happened.

Instead of merely listing the benefits of Unreal Engine—something you either already know or can easily google—let me just tell you three facts from PCF's past.

First, we decided to switch from our own engine to Unreal well before we had any idea that one day we might be a part of Epic. It was worth it to hear Mark Rein scream, “Finally!” into the phone. Second, from the moment we got the engine, it took us only a month to prepare a demo for publishers—a demo that Epic saw and said “Hold on for a second there, let’s talk.” Third, it took us two months to make two levels of Bulletstorm for a pitch demo that we showed in Leipzig to various publishers, and which got us a deal with EA. I have absolutely no idea how we could have achieved that without UE3.

# WHAT WENT WRONG

## 1) Creative f-bombs

/// Bulletstorm was often critiqued for its seemingly endless stream of four letter words.

Do you know any swear word in a foreign language? German, French, Polish? When you say it out loud, no biggie, right? Not a problem to use it during a family dinner, I assume?

That is how all the f-bombs sounded to us. Being Polish, all the strong language in Bulletstorm was just exotic and fun to us. We did not feel its power. In other words, Epic thought this is what we wanted and respected our creative vision, while we had no idea this vision was a bit more than we really wanted.

It was only at the end of the development, when I read the Polish translation of the game, that I realized how dirty we were. I swear a lot. A LOT. Yet still I ... kind of blushed.

But, to be honest, the language would not have been a problem if not for its creative usage. There are games that use way more f-bombs than Bulletstorm, and yet somehow it's less of a problem for them. Why?

That’s because most of the time the language is forgettable. If you hear a character say “You f***** scared me, you a******!” you forget about it two seconds later. Although, if he says “You scared the d*** off me!" it stays with you for a little bit longer, which creates the impression that the game is much fouler than it really is.

We tried to solve that by adding the language filter. Originally we forced the players to make a choice before they even got to the main menu. With best intentions to make the experience more fluid we moved the option to one of the submenus.

Big mistake. No one noticed it existed. It cost us a few prestigious reviews and a sea of tweets from angry gamers.

Next time, do it like Brutal Legend: a forced choice, during the game, right before the first f-bomb. Personally, just in case, the game should ask the players once more some time later.

## 2) Slow beginning, debatable ending

/// I am not a fan of action-packed openings to video games. You do get players’ attention, even if the attempt reeks of desperation, but the inevitable lull after the intro is over is a pacing killer. I think the only time I have seen a hi–octane opening work well was God of War, but that's just because Kratos doesn't take a break, and the opening is actually the entire game.

But, by Crom, that does not mean your game can take 45 minutes before you get to the core gameplay! Which is exactly what Bulletstorm did.

Endings are even more important. That 2–5% of the game can increase the review score if it's awesome, and kill the other 95–98% if it sucks. A bad ending is like finishing a delicious dinner only to learn there were worms in it.

Our ending is decent, but we were just trying to be too clever. We wanted the players make a certain mental choice. Bad things start happening in main character Grayson Hunt’s life when revenge becomes the only thing he cares about. At the end of the game, he can choose to continue walking down that path, or let go. What would YOU do? Do you think Grayson has learned anything?

But that was a bit fuzzy, and many people treated the lack of a clear resolution and closure—even though we destroyed an entire planet—as a blatant attempt to trick them into buying the sequel.

Guess what? Throughout the entire development time we were perfectly aware how crucial the beginning and ending of a game were, and still we got both of them wrong.

Be triple careful and assign an overkill amount of time and resources to making sure that the first and last page of your book are perfect.

## 3) Wrong choice for the online mode

/// I’m going to tell you a secret. We had a working, playable player-versusplayer mode in Bulletstorm. It was only a basic deathmatch, and it was a mere prototype, but it was playable—and it was tons of fun.

But we felt that the PvP space was too crowded. Ignoring the fact that our PvP was unlike anything else out there (thanks to the Skillshot system you could win with fewer kills than the opposite team), we felt we needed something different. That’s how the Anarchy co-op mode was born.

That, in itself, was not a bad choice. The problem was that we decided on Anarchy too late in the development process. We managed to make the mode really fun for the hardcore, advanced Bulletstorm players, but everyone else struggled. Anarchy requires tight cooperation, and is not bulletproof. If you don't work together, the mode is just not fun. That’s quite unlike PvP, where most of the time both teams and individuals can enjoy the carnage.

You only have one chance to make the first impression. It's better to release a fun and polished bare minimum effort than an unfinished experiment, no matter how unique.

## 4) Lack of context in the demo

/// In the game industry we often debate whether releasing a demo makes sense. It’s a controversial topic. But you know what's not controversial? Bad demos.

I wouldn't say our demo was textbook “bad,” but it just wasn't the right demo. Demos should be about emotions, about the atmosphere, about the vibe of the game. Remember the Batman: Arkham Asylum demo? Perfection.

With the Bulletstorm demo, we wanted to show people how fun the Skillshot system was. We wanted the players to fight for the best score, and thus replay the demo over and over again. So we took a very short, storyless fragment of one of the levels, stripped it of any story-related dialogue, and focused the gameplay flow on core mechanics. Also, because our mechanics were new in the FPS world, we added a tutorial movie.

EEEEK. Wrong.

In the full game, we take it slowly. We still have elements of the tutorial two hours into the adventure. Why did we expect that people would learn all that from a three-minute movie? Why did we expect people to watch these movies anyway?

Gamers were confused. So is this a time-attack, arcade-style kind of game? There’s no story, right? How can such a shamelessly short demo be so boring? All I had to do to finish it was kick, kick, kick!

We should have chosen the opposite: a story-driven “blockbuster” fragment of the game, focused on mystery and visual appeal. The Bulletstorm demo did get two million downloads across Xbox 360 and PS3 in two weeks’ time, which is a good success metric, but we needed to make sure that the demo really communicated what we wanted it to.

## 5) Echo mode: too little, too late

/// At PCF, we keep saying that Echo mode—a sort of trials and challenges spin on the Skillshot system that ranks players based on creativity and clearing stages—was created by gamers and journalists.

Our E3 demo was focused on the gameplay and core mechanics: we knew there was no way anyone would be able to appreciate the story with a thousand other games around fighting for attention with speakers larger than a fridge.

The one silly thing we did in the E3 demo—displaying the amount of earned skill points—turned out to be a big deal. People stayed in the demo room longer just to see how others performed. They were taking photos of their score. Even the crew held an internal competition between waves of visitors. Then, when we introduced Echoes via the demo, it spawned thousands of homemade YouTube videos.

We had never planned on making an arcade experience for Bulletstorm, but what happened at E3 could not be ignored. We decided to embrace the score hunt and added a special gameplay mode with unlocks, stars, and leaderboards—the whole shebang.

It was very risky, adding a new, big gameplay mode six months before going gold. But we did it. We didn’t get it quite right, however. There were too many Echoes (maps) to make competition meaningful, and those maps didn’t offer new content because they were simply locations from the campaign.

Players could win vanity items in Echo mode, but not tangible gameplay rewards, so the persistence layer was lacking. We also didn’t have time to implement leaderboards such as Best of the Week or Best in the Area. The list goes on.

Statistics on how many people finish games: [[http://edition.cnn.com/2011/TECH/gaming.gadgets/08/17/finishing.videogames.snow/index.html?hpt=te_t1](http://edition.cnn.com/2011/TECH/gaming.gadgets/08/17/finishing.videogames.snow/index.html?hpt=te_t1)]

The lesson here is that the time needed to put a feature into the game does not equal the time of implementation. It’s possible to strike gold and have your first iteration be the last, but most of the time that's not the case.

We addressed Echoes-related issues in the DLC packs by adding completely new maps made from scratch, but it was too little, too late. We’re grateful that the mode took off in popularity so quickly, and the fact that it helped round out Bulletstorm’s gameplay, but we were unable to invest enough time to flesh it out.

# I B E L I E V E !

/// Bulletstorm is bittersweet for us. As a new IP, it sold well over a million units, which is amazing when you consider the craziness of 2011, but disappointing if you remember that everyone expected more. It suffers from a catch-22: it would have been very profitable if it had taken less than three and a half years to create, but it would not have been the same game if we did not use all that time to make it shine.

But, as Mike Capps, the boss of Epic, said, "It was worth it." Through hard work and passion we have become a ninja team ready for any zombie apocalypse. We helped improve the Unreal Engine, adding features and improving its multiplatform support. We made a game that got praise from the most prestigious, toughest magazines in the world, and that has become a lasting memory for many gamers.

Thank you, EA, and thank you, Epic. You kick ass, PCF. We're ready for the next round.