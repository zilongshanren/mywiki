---
title: 'Making a tale tick: The making of Tick''s Tales - Part 1 — Tick''s Tales:
  Up All Knight'
url: http://www.tickstales.com/dev-blog/2015/11/16/making-a-tale-tick-the-making-of-ticks-tales-part-1
author: Bryce Covert
published: '2015-11-16'
source_blog: 'Home - Tick''s Tales: Up All Knight'
source_site: http://www.tickstales.com/home/
category: game programming
fetched: '2026-04-13'
---

# What makes a tale tick?

This is the first in a series of blog posts describing the programming, art, story, and music direction behind Tick's Tales: Up All Knight. My goal is to show some of the methodology behind the game, both for those interested in making adventure games of their own, and for those who are just curious about Tick's Tales. If there's something you're interested in hearing about, please make sure to post a comment, and I'll share what I can! If you're interested in the game, please do follow [@tickstales](http://www.twitter.com/tickstales) on twitter!

I'm going to start by sharing some details about Tick's Tales' backend, as it's probably the most unique aspect amongst other adventure games.

## This story has Clojure

Tick's tales is built in Clojure. It's a very atypical programming language choice for a game. As far as I know, there haven't been any sizeable games built in Clojure. So why choose it?

- The
[REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop)(Read Evaluate Print Loop) is very powerful, and allows me to rapidly change the game while it's running. - Using
[play-clj](https://github.com/oakes/play-clj)and[libgdx](http://www.badlogicgames.com/wordpress/)means that I can target Windows, OS X, Linux, Android, and iOS easily. - A lot of new creative opportunities open up if I create my own engine (vs.
[visionaire](http://www.visionaire-studio.net/cms/licenses-visionaire-studio-4.html),[ags](http://www.adventuregamestudio.co.uk/)) - Clojure's
[persistent data structures](https://en.wikipedia.org/wiki/Persistent_data_structure)could prove incredibly flexible for building out entities in a stateless way - I could leverage
[core.async](https://github.com/clojure/core.async)to easily build a scripting language/api. (covered in a future article)

### The REPL

When I started, I underestimated just how much the REPL sped development up. This dramatic speed-up came in two forms. The first is that I could make changes to the game while it's running. And secondly, I didn't have to create any editors or tool.

### A quick feedback loop

Using the REPL, I can change the game while it's running. When Tick's Tales starts up in development mode, I can change any file, and see its changes immediately. A typical example might be tweaking a script. Perhaps I'm trying to fine-tune the timing in the dialogue. I can make the code changes, Cmd+Tab over to the game, and see it while it's running. If I'm not happy, I can just rinse and repeat. A picture's worth 1000 words, so watch this example of changing a font color on the fly.


It also means that I have access to game state while it's running. I can inspect any entity as the game is running, and even change it, without making any code changes.


### Editor-less

Many adventure game engines will include an editor that lets you define animations, walkable areas, write scripts, place objects and characters, etc. To be sure, these are very helpful tools, and make it easy to quickly put the game together. But they also take a lot of development effort to maintain, and most of the time, probably more than the game engine itself. With the quick feedback loop that I had above, I never found the need to do this. It was a simple enough task to tweak the game as it was running.

There was another added benefit to this. When you use an editor, essentially the game is serialized to some data format. It essentially draws the boundaries of what your game can do. Without one, it made it much more rapid to try out new ideas.

For example, there's a water fountain in the game. Originally, when you walked into that scene, the water fountain would play at a constant volume. Based on a recommendation from a friend, it would be better to have the fountain's volume be based on Tick's proximity to it. This was trivial to try, and it ended up making it into the game. This was so easy, in part, because I didn't have an editor. Instead of having to define a way to describe this behavior with data, I was able to replace a constant (the volume of the sound) with a function that returns the volume of the sound.

### Creative power

By rolling my own engine, I tried some things that are atypical to the adventure genre. The best example is probably the camera. Most of the time, adventure games either have a fixed background, or a panning background with some parallax. I tried something different with Tick's Tales. I wanted to make it feel like there was someone behind the camera. I wanted to have a little camera shake and zooming.


This was relatively easy to do (thanks libgdx!), and I think it does make the game feel more alive, even though it is low-res.

### Persistent data structures

Most games these days either use Object-oriented programming or an Entity-component system for modeling the world. While you can do either in Clojure, I wanted to stick to simple data structures for modeling most things. Most everything you see in Tick's tales are simple maps, vectors, and sets. If you're familiar with json, this will look vaguely familiar.

; the clouds on the title screen { :texture (get-texture "title/clouds.png" ) :x 0 :y 0 :scale-x 4 :scale-y 4 :origin-x 0 :origin-y 0 :z 2 :arbitrary-data [1 2 3]}

This might seem relatively simplistic, but what it meant is that I could add behavior and data to objects very easily. There's an Alan Perlis adage that goes, "It is better to have 100 functions operate on one data structure than 10 functions on 10 data structures." I believe this to be true. For Tick's Tales it means that there is a consistent and predictable way to change all of the objects in the game. Clojure's library provides a huge tool set for manipulating data structures, and those can be used for literally everything in the game:

; change some state about an entity (assoc-in entities [:room :entities :damsel :saved?] true) ; shift player over 20 pixels (update-in entities [:room :entities :ego :x] + 20) ; or, shift any entity to any position (update-in entities [:room :entities target] assoc :x 100 :y 50) ; calculate the total distance of a walk path (reduce + 0 (map :distance (:path ego)))

I can't overstate how much boilerplate code I didn't have to write because I was able to use persistent data structures, and the many, consistent, operations to manipulate them.

Persistent data structures do have disadvantages, though. For one, because they are immutable, each change does require some memory allocation. In a game the size of Tick's Tales, it's pretty much negligible on the desktop. However, on mobile, garbage collection is notably slower and causes noticeable jitter and FPS, and I'm going to have to find optimization opportunities before it's ready for those platforms.

Additionally, I spent quite some time optimizing pathfinding, as Clojure's persistent data structures and arithmetic were too slow by default.

### In conclusion

I'm really happy I wrote Tick's Tales in Clojure. I'd do it again in a heartbeat. Feel free to post any questions, and I'll try to answer them in the next post.

Until next time,

Bryce