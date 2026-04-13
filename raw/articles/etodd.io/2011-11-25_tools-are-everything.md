---
title: Tools are everything
url: https://etodd.io/2011/11/25/tools-are-everything/
published: '2011-11-25'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Tools are everything

You've probably heard the whole "don't make engines, make games" shtick. As I progress I am learning another important lesson: tools are the most important aspect of any project, game *or* engine. Whether you're rolling a custom engine or shopping around for middleware, tools should be absolutely top priority. Seriously.

The question should not be "how many shiny graphics techniques can I incorporate?". It should be "how easy is it to create content for this game?". Content is the center of every game, whether that content is an AI algorithm, a map layout, or an art asset. If the content pipeline is even a little inefficient, it will prevent you from making the game you want to, whether you realize it or not. If you have to jump through hoops to create a new level or script a story sequence, you're going to put it off and focus instead on adding another feature that provides tangible results, like a new lighting technique. Problem is, those features don't make the game. Content does.

Even if your content pipeline is efficient, you'd be amazed what better tools can do for you. I recently learned this when I started using the audio authoring tool [XACT](http://msdn.microsoft.com/en-us/library/ee415964). Before the switch, adding sounds to my project was pretty streamlined. Create the wave file, add it to the Visual Studio project, done. In code I could loop the sounds and control their pitch and volume and who knows what else. But I didn't really take advantage of these features, because it was a pain. I got away with the bare minimum.

Started using XACT, and suddenly I'm adding new sounds, playing with the settings, and actually enjoying it. What changed? I didn't "unlock" any new features in the audio system. My code didn't change either. Yet the sound is much better now. The tool made the difference. It made it easy for me to go in and control sounds without writing code and recompiling. Now there will be a lot more variation in the sound, because it's so easy to do.

Another example. I recently added a button to switch between my editor and the actual game instantly, without exiting and booting the game. Now my level design still sucks, but it's much better than it was because I can instantly see the results of my work, and it actually makes it enjoyable.

I'm now wondering what other parts of my game are suffering from a lack of tools. Obviously the level editor is something I'm pouring a lot of work into, but what other tools could improve the process? Automated testing? A statistics collection tool for alpha releases? A better asset system?

I think this idea extends to code as well. When I started work on my iPhone game this summer, there were none of the nifty little transition animations that make mobile apps feel more responsive. I certainly had the ability to implement them; most of them just consist of "increase this number a little every frame until you reach the end". But it was a pain. Then I discovered an animation system built into the library I was using that reduced most animations to a single line of code. Suddenly I'm putting in animations all over the place.

So, moral of the story, tools are everything. If you're using Unity or UDK you're probably set to go, but just keep this in mind. Making your life (or your co-workers' lives) easier will result in a better game down the line.

**Project update**
With that out of the way, here's the latest progress on Project Lemma! Yes, now that the game is taking a different direction, I'm not sure what it's going to be called anymore. So I'm reverting to the internal codename I've been using.

**New features**

- First-person immersion: the player has arms, legs, and a shadow, and the camera can be animated along with the rest of the player's body. Speaking of animations, they now blend smoothly from one to the next instead of instantly switching.
- More realistic destruction: if you break a block in half, it will actually split into two physics entities, instead of having the two halves magically remain attached to each other.
- AI enemies: there's a turret and a ball thing that rolls toward you for a melee attack. The best part: I can make these enemies in any shape and size I want, and they're fully destructible, just like the environment.
- More player moves: the player can now double jump (the second jump is a flip) and do a bicycle kick to smash through walls. The double jump can also be targeted so the player lands on an exact location.

Enough talk, here's the video!