---
title: Adaptive music in competitive games
url: https://www.gamedeveloper.com/audio/adaptive-music-in-competitive-games
author: Denis Zlobin
published: '2016-11-29'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Adaptive music in competitive games

An article describing a way of using vertical re-orchestration to create highly dynamic music for all kinds of games where 2 or more side compete to each other.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Vertical re-orchestration or layering is one of the most commonly used techniques for creating adaptive music in videogames. It is generally based on adding or removing different layers to the score depending on the game state. Usually this technique is utilized to make music sound more intense in certain moments and situations. I want to push this concept a bit further and describe how we can use vertical re-orchestration to seemlessly shift between different compositions through some transitional layers. As an example I will use our little game from Global Game Jam 2016, called 7 Layers of Summoning. The game was developed in less than 48 hours by the team of four people in Espoo, Finland.

The idea behind this approach is to let the music adapt to balance of power in the game while it shifts from one side to another. It can be also treated as a positive feedback loop (check [this](https://learn.canvas.net/courses/3/pages/level-4-dot-4-feedback-loops) article if you don't know what it is) to reward the player who is about to win. In simple words, I wanted music to adopt some themes, motives and moods of the character controlled by the winning player.

7 Layers of Summoning is a simple 2d game about a duel between Finnish shaman and a demon. Players can freely move horizontally and attack each other by dialing a certain combination of buttons on a PS4 controller. Background music serves as a game state indicator, showing which side is winning and how close it is to an actual victory. Here are the full versions of music themes for each of the characters:

In the beginning of the round we hear "zero layer" - a neutral composition made from different elements of both themes. When one of the players lands a successful attack, zero layer crossfades into the first layer of his character's theme. Next succesfull attack will make his theme sound more intense by adiing one more layer to it. Opponent's attacks will remove additional layers until the music crossfades back into the neutral state. Take a look on this gameplay video to hear how it works.

The system is designed in a way that neither zero layer nor any character theme layers can be played together with the theme of opposing character. Graphic representation of the system will look like this:

![](https://i.imgsafe.org/c88cd0de65.png?width=560&auto=webp&quality=80&disable=upscale)


Vertical re-orchestration is all about constraints: this technique usually requires all assets to be done in the same tempo, time signature and harmony. Some of these constraints might be hacked under certain circumstances, and I'll give you a couple examples in the end of this post. However, 7 Layers of Summoning was developed on a game jam under serious time pressure, so I didn't have much time for experiments. Instead I decided to follow a simple set of rules:

Themes should have fixed duration of ~30 seconds. Longer pieces wouldn't make much sense: music changes quite often, so it is unlikely that players will be able to notice the repetitions.

Themes should be composed in the same key, harmony and tempo (in this case - f-minor, i-VII-i-iv, 130 bpm).

Themes should have different rhythmic structures and should be composed with different instruments to somehow compensate same tempo and harmony.

Each new layer should bring a very noticeable element to the music to indicate that the game state has changed.

All work should be done in the same project within the DAW. Folder tracks and buses help to organize the project, so it is easy to adjust different layers to each other, as well as to move instruments between the layers.


Here you can listen full Demon-to-Shaman theme transition where each possible state of backgorund music is played for a full cycle.

I must admit that I made one serious mistake. I started working with characters' themes first and left zero layer for the end of production. Because of that zero layer turned out to sound boring and featureless, and I couldn't do much about it without revisiting my previous work. One reason for this decision was to play safe. I wasn't sure that I'll be able to make everything I had planned in such a limited timeframe, so if I failed, Shaman's theme would become a static background music theme for entire game. In any other circumstances it makes sense to start composing with a zero layer, trying to naturally develop other themes out of it.

That's it for 7 Layers of Summoning. Now let's think how can we push this method even further.

In fact, we don't have to utilize same harmony, instead we can think about harmonic framework. Starting point of a theme doesn't really matter since we are dealing with loops. For example, we can have theme X in minor with chord progression i-VII-III-VI (i.e. Cm-Bb-Eb-Ab). Then we can have theme Y in parallel major I-IV-vi-V (Eb-Ab-Cm-Bb), and it's starting point will be in the middle of theme A.

Harmonic framework might be broken if we use quantization and set up a system in a way that transition happens on the next bar (or another suitable measure). It makes the system more flexible, but reduces its responsivness which is the main advantage of vertical re-orchestration.

If you really need to write the themes in different tempo and/or time signatures, you can still utilize this method if you make the zero layer very ambient and abstract. In that case you can add or remove rhythmic layer at the very moment the game state has changed without any loss of consistency.

Replacing the layers might be as important as adding them. For example, you can change the harmony while melody stays the same, and then shift towards the new melody and so on. This approach lets you create interesting evolving nonlienar scores without too much effort on the production site.


7 Layers of Summoning was developed in January 2016 by Lassi Vapaakallio, Laura Laakso, Ondrej "Omar" Martinek and Denis Zlobin.