---
title: 'Postmortem : Breach (Prometheus Game Jam 2017)'
url: https://halisavakis.com/postmortem-breach-prometheus-game-jam-2017/
published: '2017-07-12'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

On July 7th-9th, the Prometheus Game Jam was organized in the town of Lavrio. This jam was also a competition, with prizes for the 3 best games, as well as commendations for 4 or 5 categories. I’ll get this out of the way quickly: we didn’t win anything. The reasons (that I believe were responsible) for that are discussed in the “what went wrong” section.

The theme was “Prometheus” (shockingly), and me and my team (see below) wanted to make something different, and not settle on something in the theme of ancient Greece. We decided to use the message of the Prometheus myth, which was to stand against authority in order to do the right thing and help the greater good. Therefore, in the 48 hours of the jam, we created “Breach”!

Here are some screenshots:

The game can be found here: [https://haliss.itch.io/breach](https://haliss.itch.io/breach)


The team:

- Harry Alisavakis – Programming, art
- Theologos G. Linakis O’Neill – Music, SFX
- Theodoros Ratzos – Programming
- Myrto Houliara – Art


# Gameplay

The game is fairly complex (especially for a game jam entry). It’s a fast-paced FPS roguelite with some platforming, mostly in the form of bunny hopping. The goal was to progress through the 4 levels of the game to get an artifact that would save humanity from a cyber-galactic tyranny.

Features:

- Fast-paced action
- Randomly generated levels
- 4 types of enemies and 2 bosses
- Mobility features, like dash, double jump and teleportation grenades
- Ranged and melee attacks
- Laser traps and pickups dropped by enemies

Enemies:

- Defaulter: A simple sphere-shaped enemy that will follow and shoot at the player
- Kamikaze: Another sphere-shaped enemy that will get close to the player and then explode, damaging them (a lot) and any enemies near it
- Turrets: Immobile enemies that will rotate until they find you and shoot at the player
- Shockers: Annoying little floating enemies that will throw a laser beam at the player dealing continuous damage

Bosses:

- Gatekeeper: Mini boss that needs to be defeated in levels 2 and 3 in order to move to the next level (seen in the first screenshot)
- Zeus: The final boss found in level 4. He’s guarding the artifact that the player needs to get. He has 3 attack phases: bullet storm, summoning shockers and guarding, where he replenishes health.

Pickups:

- Health
- Ammo
- Energy


# What went right

## Huge game for 48 hours

When we thought about what the game would be, we seriously didn’t think we could pull this off in 48 hours. The scope was huge for such a short amount of time, and we’re all really proud that we got as far as we did.

## It was fun

The mobility features worked pretty well alongside the custom first-person controller and the game turned out pretty fun! We did fall a lot from the platforms but we enjoyed the traversal through the levels! Once I got the hang of it, I felt like speedrunning! And I thing this is the first time I had fun with a controller I made, so this is always good news!

## The levels

While the levels where procedurally generated, each individual room was pre-designed, which gave an interesting feel to each level. Plus, the level generation system was pretty flexible, which allowed for easy integration of new rooms in the form of prefabs. That was really important in a game jam. Also, it was pretty convenient because when the other programmer didn’t have something to work on, he made more levels, providing even more content.

## Art style

We didn’t want to have a complex art style, mostly because we wouldn’t be able to afford losing time achieving it! So, we went with something minimalistic that would look cool in an abstract sci-fi environment: low poly + reflection + emission + huge amount of bloom. And, personally, I think it worked. We also added some fog on the levels so that it gives an interesting atmosphere and has the player wondering what’s on the other side. We also had Myrto who was a dedicated artist, and she really helped with some of the models. Her help was very precious, as for the first 12 hours, the game was still in prototype mode, full of white blocks and default particles. Sure, we were working on the mechanics at the time, but seeing that the game was like that for so many hours really made me nervous.

## Details and polish

If you know me, you know that I always try to polish a game as much as I can, especially in a game jam. This time was no exception. I added particles, flashes, effects and as much feedback as I could for when you get or deal damage. And I’m pretty happy that I didn’t have to compromise the quality of polishness, especially given the scope of the game. There were also some really cool details, like the minimap which I really loved (Theodoros made that one). It was really cool and it helped gameplay-wise, as it allowed the player to be able to find his way somewhat easily.

## Music and SFX

This time we had a dedicated sound guy (Theologos), and boy was I glad! In older game jams I was also responsible for this kind of stuff, and not having to think about this field gave me a lot more time to focus on the actual game. And Theologos did a great job as well! The music and sound effects were really fitting with the atmosphere of the game, and some of the story (that Theologos also wrote) was conveyed through the audio design, which I though was genius.

## The collaboration

I’m not just talking about the team, but mostly the practical aspect of the collaboration. We started from the first game jam where we were sharing the project in USB flash drives, and in this jam we used the “Collab” function in Unity, which is truly amazing. No GitHub, no Dropbox, no flash drives, just 2 clicks. Doesn’t sound like much, but not having to worry about importing stuff, downloading assets and possible merging problems was a huge advantage.

# What went wrong

## Connection with the theme

While we knew that the game was about, and Theologos wrote a story that made sense for both the game and the jam theme, inside the game the connection was not really obvious. When there were games that had used the Prometheus myth in the most literal way possible, ours looked like it was very loosely connected to the theme, and I get it. It would probably help if we could somehow fit the story in there and make it a bit more obvious. But in the end, this game just looked like a sci-fi shooter game in a jam about a titan in the Greek mythology. Which did not help our case.

## AI and different bugs

There were bugs. I mean, sure, it’s understandable for a game jam entry, but this bothered me, as it always does. You could say that it……..bugged me. Most of the problems concerned the AI, as the enemies just wouldn’t move in a straight line to go to the player. I know it’s a really simple and stupid problem, but the lack of sleep along with working on all the other aspects of the game just wouldn’t let me focus on it. There were also a bunch of bugs that I discovered 1 day after the jam had ended (of course).

## UI

I have to be honest, I don’t like the UI. I can’t think of any way to make it better, and I certainly couldn’t think of anything there. We tried some different iterations but it just wouldn’t click, and for me it never did. I don’t have anything more to add on this subject.

## Level difficulty

The levels were hard. Mostly because the player would fall to their death all the time. This also didn’t help with the contest. The members of the team (me included) are mostly hardcore gamers; we play lots of games of every difficulty. So yeah, we also died a lot, but we knew that the game could be beaten, as long as we could “git gud”. However, we didn’t think something really critical: the judges are not necessarily as skilled as we are. They came from different backgrounds, and they were either developers or researchers, but we couldn’t just assume that they would be as “skilled” to manage to enjoy the game and not rage quit after the first 5 deaths. However, I’m sure that some of them could actually “git gud” and enjoy the game. But the thing is that they had less that 5 minutes to check every game in the contest, and I truly doubt that they could get enough practice in such little time. This is also part of my next point.

## Marketing and presentation

Something that I forget in almost every game jam, is how important it is to do successful marketing for the game. And this jam was no exception. I also always forget that marketing is a part of the development, and I should consider it even before creating the game. Due to the nature of the jam and the contest, “Breach” was a **really bad** game to market. And that’s because there’s no 5 minute playthrough or 3 minute video that can successfully convey what this game was about. I think of “Breach” as a game that you really have to try to get into it, that you have to first give it a chance. I knew that some of the other games I saw would get prizes, mostly because if you sat there for 30″ and watched the game you could **immediately **figure out what the game was about. What was done right and what was done wrong. How it’s played, what its purpose is and what the developer wanted to achieve and what they eventually achieved. That was probably the most important thing to consider, and “Breach” couldn’t be further away from that. The presentation also didn’t help with our case. We didn’t have the time or the means to make a good video, so Theodoros had to record his playthroughs until he got a good one to show. Which was not easy, since, as mentioned, the game was hard. When we run out of time, we just got the best run and showed it. And there were 2 main problems with that video: The sound was only at 30%, therefore the amazing music and SFX that Theologos made, were almost inaudible. Also, the playthrough didn’t make it to the last level. Hence, the boss, Zeus, that I spent the 3 last hours making, was never seen by anyone, especially the judges. Which was really bad, because I was pretty proud of that boss, as I never made a boss before. But it was especially bad because the whole work of Theologos also went unnoticed! This video along with the awkward speech of mine that I made up as I was talking really made a bad impression, or at least I think it did.

# Conclusion

I personally don’t care that we didn’t get a good place in the contest. It would be nice, of course, to get some recognition for the huge amount of work that was done in 48 hours, but I don’t care because we know what we made and what the game was. And we’re goddamn proud of that game, how it turned out, and the fact that we made something like that in such a short time. Sure there were problems, but there were mainly about the contest and the judging. As a game, it was pretty well made for my standards and I learned a lot, both about the development of such a game as well as what it means to market your product in contest like that. I don’t know if my speculations are correct about why we didn’t get any prizes or commendations, but this is my best assumption that I believe makes sense. Either way, I had fun, the jam was very well organized, and I am looking forward for the next game jam like that!

Until then, see you in the next one!