---
title: Building a gameplay driven soundtrack
url: https://www.gamedeveloper.com/audio/building-a-gameplay-driven-soundtrack
author: Julien Ribassin
published: '2016-05-31'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Building a gameplay driven soundtrack

In illumine, the audio is not only setting the mood, it is also telling you what awaits in the dark. In this first blog post, I detail how gameplay elements can dynamically generate a soundtrack.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![](../../assets/889ff4eaa0a6ac59.png)


For the last few months I have been working on a game for Windows, Mac and Linux called [illumine](https://illuminegame.com/). It is a roguelike in real-time in which I tried to explore a different approach to procedural generation. The game's world is not a static level generated before dropping the player in the game. In [illumine](https://illuminegame.com/) the player is dynamically creating his own path. When designing the game, it appeared from the get-go that the audio would have to be very flexible because of the ever-changing nature of the environment. It was clear that I would have to create some kind of adaptive soundtrack.

Adaptive soundtracks have now become a pretty common feature in modern video games. Having a soundtrack that matches the actions of the player is a very effective way to reinforce immersion. Early examples can be found in the nineties in Lucas Arts games. In Monkey Island 2: LeChuck's Revenge, their in house iMuse engine allowed soundtracks to transition smoothly from one scene to another. The game felt like a big adventure and not like a succession of levels.

Another great use of adaptive soundtracks is for gameplay purposes. Elements of the soundtrack can be used as cues to inform the player about his surroundings. In The Legend of Zelda: Ocarina of Time, the soundtrack dynamically changes as the player approaches an enemy. The volume of an additional audio track rises as the distance to the closest enemy decreases. The obvious effect is that the tension is rising. However the most important effect is linked to spatial awareness. When the Zelda games moved from 2D to 3D, the player lost the ability to see behind Link. The developers thus needed a way to tell the player if there was an enemy behind him, otherwise the player might feel like the game was cheating if he got hit from behind out of nowhere. That's the real purpose of this additional audio track. If an enemy is creeping behind Link, audio kicks in, the tension rises, pushing the player to turn around or run away.

The game I am working on, [illumine](https://illuminegame.com/), is a roguelike without any combat. However, aggressive NPCs kill the player with a single hit. The player thus has no choice but to outsmart the AI. From a design point of view one of the biggest challenges is to make sure the player has at any given time all the strategic information he needs to make the right decisions quickly. Ideally, before exploring a new area, the player should have an idea of the positions and types of NPCs that await him in the dark.

[illumine](https://illuminegame.com/) features dynamic shadows whose light source is the player. It basically means that if the player can't see any NPCs, they can't see him either. To convey information to the player about those NPCs hidden in the dark, audio was the obvious choice. However, audio tracks fading in and out for each type of NPC would have resulted in a huge mess. Instead I decided to assign to each type of NPC a short (< 400ms) and distinctive sound. I then gave to every one of them a musical score at 90 bpm that varied depending on the NPC's state (idle, angry, scared...). Without entering a room, the player can now tell what types of AI he will have to face. The next step is to figure out how to convey the positions of the NPCs.

[illumine](https://illuminegame.com/) is a 2D game with a top-down perspective. Stereo can't help us and positional audio is thus extremely difficult. The only audio tool at our disposal is the sound volume of each individual NPC. Raising the volume as the player gets closer is the obvious application. To give the player an idea of the NPC's location I decided to add a visual representation of the propagation of the sound waves. Choosing different shapes also helped distinguish different types of AI when a lot of them are in the same area.The way the player interacts with the environment is by breaking down walls with a single press of a button. After a few tests, a problem appeared. All elements of the game were in rhythm, except the player. To fix this I implemented a small variable lag (at most 150ms) to make sure the player would break walls in rhythm. Incidentally this small noticeable lag also reinforced the sense of feedback.

As a result, we obtain a soundtrack dynamically created by the gameplay, with smooth transitions between the successive situations as the different parts of the soundtrack naturally fade in and out with the player's movements. Although very useful from a gameplay perspective, the soundtrack is so far pretty bland. It mostly consists of a drum kit and a few bass lines. To spice things up a bit, the idea was to add melodic adaptive tracks. To make sure that all those tracks would transition nicely to one another, they were all built in the same key and at 90 bpm. All those tracks also feature random variations that are triggered by the situation in order to raise the tension when a lot of NPCs are on screen for example.

In retrospect, this approach of audio design turned out to be much more difficult to implement than I had initially expected. For the last tracks there were so many constraints that composing the music had become a challenge in itself. The simplicity of the resulting music is a direct consequence of all those constraints. Amongst all the tracks that were created I always kept the simplest ones in order to avoid confusing the player. He or she should be able to decipher the soundtrack at all times. Despite this apparent simplicity, I am rather satisfied with the result. The soundtrack manages to not feel repetitive thanks to its procedural nature. However, I feel like I barely touched the surface. For example it would be very interesting to try to procedurally generate melodies in a game that would be appropriate.

A very positive effect that the soundtrack had on the game as a whole was that it convinced me to completely revamp the structure of the game. Halfway through development I realized that it was possible to transition smoothly from one track to another and I decided to ditch a classic structure with successive levels to adopt a more organic progression. And this is basically how the game became a roguelike. I'll write more about this dramatic change in a future post.


illumine is now on [Steam Greenlight](http://steamcommunity.com/sharedfiles/filedetails/?id=678729256) and is available on [itch.io](https://dejima.itch.io/illumine).