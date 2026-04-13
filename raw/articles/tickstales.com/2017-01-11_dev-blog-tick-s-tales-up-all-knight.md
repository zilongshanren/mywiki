---
title: 'Dev Blog — Tick''s Tales: Up All Knight'
url: http://www.tickstales.com/dev-blog
published: '2017-01-11'
source_blog: 'Home - Tick''s Tales: Up All Knight'
source_site: http://www.tickstales.com/home/
category: game programming
fetched: '2026-04-13'
---

It's now been six months since I've released my first [adventure game](http://store.steampowered.com/app/411610/). Now that the development effort is over, I've spent some time considering, "What next?", and, even more importantly, "What would make it better?". Ron Gilbert, creator of Monkey Island, famously wrote the article, "[Why Adventure Games Suck.](http://grumpygamer.com/why_adventure_games_suck)" It's an excellent read. Believe it or not, this article heavily affected the design of Tick's Tales, and I'm happy for it. However, I spent so much time emphasizing what not to do -- dead ends, death, mind-bending logic. I wish I spent as much time thinking about what to do. And that is the subject of this research.

So I'm writing a series called Why Adventure Games Rock to catalog my research. Unlike Ron Gilbert, I don't have a suite of my own games to reflect upon. Instead, I'll reflect on other developer's games. I'll try to look at 1-2 each week. My goal is to examine adventure games with a critical eye, both classic and modern, and figure out why they work. Adventure games' flaws are now well known. But I'd like to look at what makes a player feel great accomplishment, feel invested in the characters, and a narrative style that complements the adventure genre.

## King's Quest V

The year is 1991. A six-year-old me is watching my grandfather play the desert sequence in King's Quest V, pad of paper in hand. This particular desert is made up of screen after screen of monotonous desert, speckled here and there with oasises. Upon reaching one, Graham and the player alike are relieved as the narrator says, "Ahh, life giving water, nectar of the gods. Graham can now feel strength and renewal flowing through him." I was quite enchanted by this artful, albeit deeply flawed, adventure game. Let's see what design elements really worked in this game. We're going to set aside the plethora of problems this game has, especially the infuriating dead ends.

### Exploration is the means of progress and the reward for progress

King's Quest V tailors the "explorable area" very well. When the player makes progress in this game, they know it. They're taken to a new land. Progress is made by exploring and solving puzzles, which, in turn, opens new areas to explore.

Most adventure games follow a similar pattern. However, King's Quest V mostly closes off areas as the player advances. This might seem cheap at first, but King's Quest V uses it to its advantage.

First, it creates a clear chapter boundary, giving the player a definitive sense of accomplishment. The linear flow makes progress undeniable, and it feels measurable. Other adventure games will open new areas in different parts of the game, resulting in an ever-expanding explorable world. In those games, it's hard to gauge "how far have I come?"

Perhaps even more importantly, closing off areas after a opening new ones gives a sense of relief, because the player knows they won't have to backtrack. Think if you had to walk all the way back to Crispin's house after arriving on Mordack's island. Not fun.

And finally, closing off old sections gives the designer the ability to control pacing. King's Quest V doesn't take as much advantage of it as, say, Kyrandia 2: Hand of Fate, in which each area has just the right amount of puzzles to make the world feel populated. The player doesn't wander through a world that is 95% done. We want a graph that looks like right side:

The ever-expanding world

Closing old areas when new ones are opening

It's worth noting that this design feature is not unique to adventure games. For example, in the Diablo series, progress is also marked by a change in scenery. But it's especially rewarding when each backdrop is a piece of art, as is the case in King's Quest V.

### Player's knowledge > Character's knowledge

This is an area in which I've come to disagree with Ron Gilbert. He argues that you shouldn't have to have the player die in order to get information necessary to win. In one sense, I totally get it. If the player has to watch Graham die 20 times in a desert in order to locate an oasis for the 21st Graham, then it's a really unrealistic puzzle that breaks immersion. However, I'm becoming convinced that [this is an unhelpful term, and, in fact, a goal not worth pursuing](https://www.youtube.com/watch?v=Xncs1mrMV6o).

This issue has everything to do with the user experience, and nothing to do with breaking immersion. Here's my rationale:

- In nearly every other game genre, death is a thing. Strategy, RPG, platformers, heck, even card games! We don't consider it bad design there.
- Death in early adventure games resulted in costly consequences, and burdensome preparations. Hopefully you saved recentely. And hopefully you saved before it was too late. It's best to create a unique save file every 10 seconds, just in case. Not to mention it'll take several button presses [boring] to restore.
- Having consequences to making the wrong decision results in a sense of tension.
- It's just as easy to break immersion by removing death altogether. Imagine if Mordack just stood there waiting for the player to try inventory item after inventory item to defeat him. That would take them out of the game pretty quick.

Take your time. No rush.

In total, player knowledge and character knowledge are not equal. Heavily relying on a player to die or gain information that the character couldn't know may be a sign of bad design, but it isn't always. In fact, sometimes it's used to very good effect. For example:

- The desert puzzle is rewarding. Yes, the player has to make map or memorize oasis locations -- many people may not consider this fun. But the relief of seeing an oasis is a product of the consequence of the many attempts without finding one.
- Many scenes have compelling tension: sneaking past the sleeping bandit, choosing which treasure to take from the treasure room, the blue creature, and the wizard showdown with Mordack.
- The genie bottle. Now, admittedly, this puzzle sucks, but not because of the death. The player gets a genie's bottle that, when opened, traps Graham in the bottle and then, game over. If the player gives it to the wicked witch (no rationale), she'll open it, and herself becomes trapped. By no means am I defending this puzzle's logic, however, the player learns of its effect by first dying. When the player gives the bottle to the witch, they know what would befall her, but, presumably, Graham doesn't. And that's great. It gives the player the feeling of outsmarting the witch. To be sure, this same effect could be accomplished without the prerequisite death. However, if dying allows an opportunity to give the player a moment of triumph, I'm all for it.

In the end, death requires tact, and if a scenario can be better written without death, perhaps that's the way to go. Of critical importance: if a game has death, the save/restore UX needs to be seamless. No hunting for save files, no requisite saves every 5 seconds. Player died? Get a funny message and they're back at it 3 seconds later.

### Music / SFX

The early 90's was still the wild west in game design. They didn't have rules and guidelines to the extent we do now. I've noticed that modern AAA games have mastered the art of background music. The themes may be memorable, but their goal is to subtly complement the experience the player is having.

Not so with Sierra, and King's Quest in particular. I would describe the music as "melody-forward". The tunes are memorable. They grab the player's attention. They can hardly be called background music. This is a very good thing for a more lighthearted adventure. Since the adventure game experience is so much simpler than, say, strategy games, there's room for more forward music.

Additionally, the timed/orchestrated cutscenes makes for a rewarding experience. The music plays part of the storytelling, emphasizing certain points, even using music for sound effects, much like old cartoons would use the orchestra for their sound effects. This, stylistically, works well for the high spirited adventure. Would it work as well for sci-fi? Probably not.

## King's Quest VI

King's Quest VI is rather different from King's Quest V. The pacing is different and the puzzle styles are completely different. Let's focus on some of those differences.

### The contraption is a plan, not a contraption.

So adventure games are notorious for requiring the player to build contraptions. There's the infamous make-a-disguise puzzle in Gabriel Knight 3. In King's Quest VII, the player sends the moon back up using a rubber chicken. They're obscure, and often mind-bending. How is King's Quest VI different?

Puzzles are combined to create a master plan.

Think about it. Early in the game, the player; meets Jollo. He's the royal clown, and Alexander befriend him. Later, the player concocts a plan with him -- to swap lamps with the evil, genie-possessing royal vizier, and to convince said genie that Alex is dead. That's not a slingshot, it's not a trap, it's a clever plan. It requires the player to solve puzzles in the same way that you might for a contraption, but it feels more grand. Additionally, it makes Alexander only part of the puzzle. It requires the help of at least 7 people to defeat Alhazred (Alexander, Jollo, Cassima, Saladin, Shamir, and Cassima's parents). That feels rather grand.



### Few "fetch" quests

King's Quest VI has very few fetch/trade puzzles. Compare it to King's Quest V. The player essentially have a series of unrelated trades. For example, you need a hammer that you get from a cobbler by giving him a pair of shoes that you get in exchange from some emeralds that you could only acquire using an amulet that you got from a gypsy in exchange for a gold coin that you got with a staff that you steal.

The interactions are the same -- e.g., use ring on guard, give lamp to Jollo -- but the effect in the game is very different.

Let's take a look at an example.

Each gnome has a single sense

- These five gnomes are the guardians of the Isle of Wonder. They act as a sort of locked door to this island. The player must first satisfy them in order to pass. How do you satisfy them? Each gnome has a single sense, and the player must use inventory items to convince them that Alexander is not a human, one at a time. This could've easily been written as a 5 item fetch quest, each gnome wanting a single item to appease them. But that would be
*boring*. Notice that this puzzle isn't immersive. It doesn't try to be realistic. It's a quirky puzzle applied to quirky, fictional, unrealistic characters, and it works.

The scenarios like this go on and on. Very few puzzles are explicitly spelled out as a fetch quest. E.g.,

- Send a message to princess Cassima through a nightengale
- Gather incriminating evidence
- Save yourself from burning to death
- Make the lord of the dead shed a tear.

The more outlandish the idea, the more compelling the storytelling.

### Tell the player the answer as part of the puzzle

In Tick's Tales, I made it a point to always tell the player the solution before the player solves it. The player only has to pay attention, and figure out how. King's Quest VI doesn't do this always, but it has a couple of subtle tricks to accomplish the same effect.

Old lamps for new...

- Musical themes are reprised in related situations, giving the player a clue to the solution. For example, Beauty's theme is almost the same as Beast's theme. By the time the player meets Beast, they've probably heard Beauty's theme several times. Also, the dangling participle has a similar melody to the bookworm. These are signposts to the solution, and, ideally, the player doesn't even notice.
- Sometimes it's said outright. Jollo says, "Maybe you could convince him (the genie) that you died!"
[Checkhov's gun principle](https://en.wikipedia.org/wiki/Chekhov%27s_gun)says: "Remove everything that has no relevance to the story. If you say in the first chapter that there is a rifle hanging on the wall, in the second or third chapter it absolutely must go off. If it's not going to be fired, it shouldn't be hanging there." A similar rule applies to adventure games, and King's Quest VI directly manipulates the order the player is exposed to certain characters, so that they definitely know a solution before they see it. For example, the first time the player makes their way into town, they see a peddler selling new lamps in exchange for old lamps. Later, when they acquire an old lamp, they think, "Oh, I can exchange it for a new lamp!" but the peddler has since left. This makes them ponder what the purpose of the peddler is. Later on, it "clicks" when they learn they need a replica of the genie's lamp.

## In summary

Not all of these principles applies to every single game. But these principles do work for King's Quest genre, and I think they're worth considering. [Tick's Tales](http://store.steampowered.com/app/411610/) follows some of the principles, and others it doesn't. For future games, I'll think about crafting the narrative and puzzles considering these principles.

If there are specific games you'd like me to study in this fashion, please write a comment! Stay tuned for more.