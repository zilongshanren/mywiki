---
title: 'RPG Playground 0.13: Conversations'
url: https://dewitters.com/rpg-playground-0-13-conversations/
published: '2015-01-15'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

Finally, the new version of RPG Playground is available at [http://rpgplayground.com](http://rpgplayground.com)! First of all, this release took waaaay too long. The previous version was released 1 year back, which is definitely a very long time ago. I don’t want any of my next releases to take this long ever again. The plan is to make a new release every few months, or even faster.

A lot of you were asking, poking and bugging me when this release will be out, and what features it will contain. So thanks for your patience! I hope you will stick around while I keep adding new features.

So, why did it take so long? Well, a lot of work was done both on visible features and framework improvements. I will explain everything in this post (so yeah, this is going to take a while). I will handle the most important features first, so feel free to quit reading and [start designing your game](http://rpgplayground.com).


## Conversations with Screenplays

So a new concept was introduced called *screenplays*. This allows you to make scripted sequences such as conversations and cutscenes. For now, I kept it simple and only 1 kind of action can be specified: *character says “text”*. For an example, take a look here:

hero says "Hi mom!" mom says "Hello sweetheart. Are you going into the forest?" hero says "Yes" mom says "Be careful, alright?" dad says "And be home before supper!"

You can name each character, and then use that name in the screenplay. In the future lots of other action will be added such as giving the player a choice, moving characters, showing info text, … . But I first want to see if everyone finds it easy to get started with a simplified version. For more details, you can take a look at the [screenplay section](http://rpg-playground-manual.readthedocs.org/en/latest/screenplay.html#screenplays) in the user manual.

## GUI Improvements

All editor functionality moved inside the project pane on the left. This means that when you close the project pane, the only thing left of the editor is the edit button on the top left. All other things are part of your actual game. This allows me (and you) to add other buttons to your game such as an ingame menu. Take a look below to see where all the menu items went:

![New menu New menu](../../assets/3166a194efd7395d.png)


## New tutorial video

Since the GUI has changed, and screenplays need some extra explanation, I had to create a new tutorial video.

## User Manual

Screenplays are not that straight forward, and therefore I also created a small [RPG Playground user manual](http://rpg-playground-manual.readthedocs.org/en/latest/index.html), which contains more detailed documentation of screenplays. But next to screenplays, other functionality and background information is also included in that first draft of the user manual.

## Automated Testing

Right before doing a new release, I have to test everything to see if nothing is broken. As RPG Playground gets bigger, more things need to be tested. Since I want to do small and fast releases in the future, this can take up quite some time. Therefore I now have a lot of tests which automatically test the most important features. When something breaks, I know it immediately.

This one is crucial for small and fast releases.

## Data driven GUI

The games you create with RPG Playground are stored in data files. It contains the tilemap, where characters are, what they say, etc. For my editor GUI on the other hand, all was hardcoded inside my ActionScript source code. But now my editor also moved to data files, which are actually the same data files as the ones from the game. This allows me to quickly add and adapt the editor GUI. And for the far future, it might even allow me to create RPG Playground inside RPG Playground. This last part might sound weird, but my architecture will allow a lot of stuff to be created inside RPG Playground, such as graphical user interfaces. Can’t wait to get to this point :).

## What will the future bring?

Well, that’s it for this release. Before I extend the screenplays with other actions, I first want to see what you girls and guys are doing with it. In the mean time, I’m going to add an extra indoor tileset. This last part is preparation to support multiple levels (walk inside buildings etc.). So to summarize what you can expect for the next releases:

- Extra indoor tileset
- Extra actions for screenplays
- Multiple levels, which allows you walking into buildings.

If you have any questions, remarks, requests or any other feedback, let me know!!! You can do this by leaving a comment below, message me on [Twitter](http://twitter.com/koonsolo), [Facebook](http://www.facebook.com/pages/Koonsolo/131223576036) or [Google+](https://plus.google.com/102606831916030049663), or email me at koen@koonsolo.com.

## 0 Comments