---
title: Building Cogmind's Ambient Soundscape
url: https://www.gamedeveloper.com/audio/building-cogmind-s-ambient-soundscape
author: Josh Ge
published: '2020-09-08'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Building Cogmind's Ambient Soundscape

Describing the methodology behind bringing Cogmind's maps, machines and other sources of atmospheric audio to life.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

I first introduced Cogmind's ambient sound system [back in 2014](https://www.gridsagegames.com/blog/2014/01/ambient-sound/) during the pre-alpha days, as it was initially developed for Cogmind's predecessor ([X@COM](https://xcomrl.blogspot.com/)) in the years before that, and sound would continue to play an important role going forward. It wasn't an especially long post like the ones I tend to write these days, but it did touch on the basics of propagation, sound dampening, and falloff models.

Since then I've also written a number of articles about [sound effects and audio in general](https://www.gridsagegames.com/blog/category/dev-series-sound-effects/), but now it's finally time to address the relative lack of ambient audio in Cogmind! I'd been putting this feature off for a long while and it sat at the end of the pre-1.0 roadmap for years, at first because it made more sense to work on all that content after everything else was complete, but then later due to my concussion leading to hearing issues, which only after a couple years finally reached a point where they wouldn't be a significant roadblock.

Here we go!

# Technical Overview

For relevant background to help better understand this article, here's a quick review of the ambient audio system's features...

![](https://media.indiedb.com/images/articles/1/284/283085/auto/cogmind_sound_effect.png?width=1280&auto=webp&quality=80&disable=upscale)


There's a whole lot of sound-related values defined in Cogmind's data files. Above is an excerpt combining various sections, both ambient and non-ambient from a range of categories, to give a sampling of the variety (the full file contains 1122 entries :P).


Each sound is defined along with a "minimum" radius representing the distance before its "falloff" begins (i.e. the volume begins decreasing due to distance), and a maximum radius indicating the furthest distance out to which the sound travels as it's fading. A given sound can use one of four different falloff models depending on its needs, either linear, logarithmic, reverse logarithmic, or inverse.

![](../../assets/417f8545c1fad2c1.png)


Demonstrating the relative volume of audio emitted from a given source (the machine at the center) using different falloff models, alongside rough approximations of the graph representing each.


The above examples all have a minimum radius of 2 (and max of 15), so the different results come purely from changes to the falloff, but by adjusting the other values a huge range of options become possible. For comparison, here's a logarithmic falloff with a longer plateau (radius 8~15):

![](../../assets/2ebfe5f6122458b5.png)


This falloff sample has a longer plateau than I generally use, but it can come in handy for some purposes.


On every player move, or with any action that might have affected the amount of sound reaching the player's location (terrain destruction, machine toggling, etc), the audio sources potentially within earshot of the player pathfind to the player to determine how far away they are for volume determination purposes. The final new sound profile for the player's current location is compared to the any sounds that were playing from the previous state, and the old state fades into the new state, which might involve simply slowly adjusting the volume of the same set of sounds, adding new sounds, or gradually removing those that are no longer in range.

![](../../assets/7685015984cbf3a7.gif)


Visualizing the sound paths from each nearby audible machine, paths which are used

to determine the final volume at the player's location.


Using a system like this is both quick and makes it pretty easy to account for dampening effects of the path successfully passing through materials, like the doors in Cogmind which block 50% of the volume. You can see the effect of doors in the falloff samples from earlier (it's most noticeable in the reverse log demo), but here's another still shot using the sound path visualizer in which you can see the volume dropping quickly when passing through doors.

![](../../assets/69a21ee4ae79117c.png)


Doors to two rooms lowering the volume of the machines heard within.


So that's the underlying architecture we're working with here, let's move on to where the soundscape actually takes shape.

# Audio Style

Naturally a lot of games tend to use music to fill the role of "continuous audio," which when done well is instrumental in conveying the desired mood, and possibly atmosphere as well.

It can also be great to just enjoy out of game. I personally love VGM, having listened to it for the past 30 years (I guess since before listening to VGM was a thing many people really did :P), and in the early years recorded the music from console games on my TV to create OSTs and mix tapes. Later on importing OST and arrangement CDs from Japan became a thing, so I did a lot of that, too, and still listen to the original rips I made to this day...

So yeah getting a Cogmind OST by a proper composer would be pretty damn awesome, but at the same time developers need to choose for their game the type of audio that will best achieve the vision for its world.

The audio style discussion has played in some form or another, in some place or another, pretty much every year of Cogmind development so far as different players ask about it, or I bring it up myself when planning for the future. It was once even the topic of a post [here on the blog](https://www.gridsagegames.com/blog/2017/04/music-for-cogmind/), back in 2017. Over the years I've certainly been collecting a list of interested composers, or others that I've become interested in, and analyzing whether or not I think they'd be appropriate for this particular job if it came to that. Many have also approached me asking about Cogmind, including a number of players.

For now though, music is probably not right for Cogmind. With an emphasis on immersive atmosphere, and a semi-realistic dark sci-fi one at that, I think environment-driven ambient audio would better fit the role. Even if it doesn't work out the way I envision it (spoiler: it does), considering that the architecture for an environment-based ambient audio system already exists and the only further need is to add the content, and doing so involves fewer challenges and commitments than working with a third party composer, it makes sense to start with this approach and experience the results to hear for ourselves. Let the machines and other objects of the world dynamically create the soundscape, and if that works then we're all set.

Then there's the additional benefit of this approach: it's heavily focused on sound effects and loops, which I'm familiar with after working with them for many years, and is also something I can manage on my own, which in my book is always a plus over bringing in outside help. It means that iterating is faster, and I have more direct control over making sure each step along the way is successfully integrating with my vision. Also of course when I inevitably need more content I'm always available to add it :P

That's what the rest of this article is about--the process behind pulling that soundscape together.

# Machine Loops

The main focus of the ambient audio is Cogmind's machines, of which there are over a hundred.

Technically before reaching this part of the development process, in previous years I'd already added loops for 17 special machines and other various sources especially meaningful to the plot or mechanics. At the time I didn't want to wait on those since in some cases they're quite important, so it made sense to emphasize their impact with audio as soon as possible. "Fluff" machines could wait, but not things like machines capable of significantly changing the entire run :P

## Categorization

With such a large number of machines, providing sound for all of them is a rather daunting task, so we do what we do with all daunting tasks: break it down! I first roughly identified the different categories of machines in Cogmind from an audio perspective. (Technically Cogmind machines were already divided into themes for map placement purposes, but those categories do not always align perfectly with what kinds of audio you might get from them, hence the need for alternative audio-specific categories.)

Here's the breakdown as reflected in the ambient loop directory structure, including the number of loops in each as of this writing (there will no doubt be a few more added in the near term, but most everything has audio at this point):

![](../../assets/c5103802017136e7.png)


The current tally of Cogmind's ambient loop files. Ambient audio is sourced from "props," which are anything in the environment that is not a cell, item, or entity (robot)--generally machines for the most part.


"Interactive" refers essentially to terminal types, all of which were originally using the same placeholder loop, but now every faction has one or more unique sounds for their terminals. They look and operate differently, so it only makes sense to differentiate their sounds, too :D

"Prefab" includes machines I draw directly into hardcoded map sections via [REXPaint](https://www.gridsagegames.com/rexpaint/), those with a unique name and possibly function as well. (Read more about prefab development [here](https://www.gridsagegames.com/blog/2017/01/map-prefabs-in-depth/).)

The "Theme" directory contains all the machines that are [procedurally inserted](https://www.gridsagegames.com/blog/2014/07/furnishing-athe-dungeon/) into maps. A majority of these are fluff, though in particular the "Special" subcategory includes all the explosive machines and a few with unique functions. Among the Theme machines I did that group first to ensure they got first pick from the audio resources I was working with, since they're more important.

## Creation

In terms of actually creating the sounds, I've already covered that before in the [sound design how-to article](https://www.gridsagegames.com/blog/2014/05/sound-design-cogmind/) I wrote in the early years of the project. Reminder: I don't do this from scratch, instead using existing samples and editing them as necessary.

I spent a couple weeks going through lots of samples looking for what sounded like my vision for each machine in question. Obviously since it's sci-fi there's often a lot of leeway for interpretation, but still important to be consistent. Working with a single category/subcategory at once, I'd use [Audacity](https://www.audacityteam.org/) for looping all the tracks, adjusting or mixing some of them for better effect.

![](../../assets/13bfcb2f8b71ba59.png)


Editing Cogmind's machine loops in Audacity.


As each category's loops were completed, I'd fire up Cogmind's sandbox mode to hear them in game and adjust sound propagation values as appropriate. The sandbox contains one of every themed machine, making it more convenient to do this than actually finding them in game.

![](../../assets/0b5a795e4bbd794b.png)


Cogmind's development sandbox, which has grown incredibly messy over the years since it has continued automatically expanding itself based on game content, but I don't really use it much anymore--it was instrumental in early development but barely gets loaded up these days.


However, the machines in the sandbox are also quite close together, which would interfere with the task of making machine-specific adjustments (although the proximity does come in handy when testing out overlapping audio from different machines!). So right away I needed some new debug features to make this job easier.

Enter audio toggling. It was suddenly important and very useful to be able to toggle all ambient sources across an entire map, as well as toggle them individually by source. This functionality would also be of help once we get to the stage of testing ambient audio in regular map environments.

![](../../assets/cc493f28182371ff.gif)


Toggling ambient audio sources in the sandbox.


Now I could more easily hear any given machine in isolation, and test how its audio propagation settings worked for its particular sound. I started everything with reasonable default propagation values, and adjusted from there. These values are set in the external data file shown earlier, a file which requires a game restart in order to load any changes. So while at first I was determining final values by listening to each machine and making educated guesses about what it should be changed to before restarting, this approach is slow and incompatible with the sheer amount of content being worked with here.

Time for another new debugging feature!

Rapid iteration is important, so I added a way to dynamically adjust a given audio source's min/max radius and falloff using the debugging console, making it possible to immediately experience the results of any change and easily experiment with different possibilities.

![](../../assets/66ac9a14dfc6d1bd.gif)


Adjusting machine audio propagation settings dynamically.


This continued for more than 100 machines until everything seemed to have suitable values...

## Polishing

Of course with all this audio content going into the game at once, it's about more than just editing loops for individual sources--we'd also need to take a look at the atmosphere as a whole and ensure it's properly balanced, and I'd need new tools to facilitate that process as well.

First of all, as I walked around real maps it became apparent that the default linear falloff model I'd been using for most machines didn't actually work that well when applied to all machines across the floor. I'd started with that type because it happens to be what was used all these years for the special prefab machines added before this new undertaking, and it works there because those tend to have longer audio ranges and I wanted them to be pretty clearly identifiable shortly after they come into earshot. Not so with all the generic machines scattered about. (When applied to them, a linear falloff makes the ambiance feel more confusing with a greater number and variety of sounds quickly fading in and out as you move around.)

To experiment with a new default falloff model, I added a console command to simultaneously switch all machines to a different model, eventually settling on logarithmic as the default:

![](../../assets/2b3664cf89fe961f.gif)


Testing a couple of different falloff models under the ambient audio visualizer.


Another factor to explore was the extent of silent gaps between areas of machinery on various maps. Technically we could fill an entire map with machine audio if the ranges are long enough, although this would also mean more overlapping and general cacophony. Still, to test the size of gaps and see how changing average audio ranges might affect the experience, I also added the ability to simultaneously adjust the range of all sources:

![](../../assets/d5964985f3f375e4.gif)


Adjusting machine ambient ranges across an entire map at once.


When the majority of machines had ambient audio, I did a dev stream to demo the intermediate results while talking about the process and exploring what maps sounded like at that stage. Still very WIP at that point, but it was exciting to finally hear the soundscape taking shape!

One thing clear from walking around was the lack of normalization--some machines are clearly too loud relative to others (some also seemed too quiet, but we'll get to that later in the section on mapwide ambience). So the next thing I worked on after the stream was addressing that issue, starting with yet another console-based convenience feature: the ability to reduce the base volume of individual machines on the fly, in game. Commence rapid iteration!

(Normally I'd show you a gif of realtime volume adjustment here, but the ambient visualization system only reflects relative volume numbers rather than absolute volume, so it wouldn't be much use since nothing appears to change when this setting is modified :P)

After confirming this would give satisfactory results, I made it a part of the architecture, i.e. machine audio samples could have their base volume reduced via settings in the game data. This means it would be possible to avoid resampling all the associated audio tracks, which would be pretty time-consuming by comparison. In all, I lowered about half of the machines' volume by 50~75% through this method in the week after that stream.

# Mapwide Ambience

A soundscape composed primarily of the humming, whirring, buzzing and clanking of machines is great, though there are always going to be some gaps, places where machine audio doesn't reach. The idea is to fill those with a general ambient track, preferably a different one for each unique map type.

To demonstrate the gaps relative to the areas from which machines are heard, in these images I've used a separate color (blue) to highlight gaps, or any location reached by absolutely no sourced ambient audio:

![](../../assets/23c8b436163ffd76.png)


Audio gaps (blue) compared to sounds emitted by machines (orange), in part of a Factory map.


![](../../assets/4d29096b0049b537.png)


Audio gaps vs. machine audio in a sample Garrison map.


![](../../assets/7d9d33db6e90b979.png)


Audio gaps vs. machine audio in a sample small Materials map.


Although sometimes silence is a good thing (and put to use for that reason), it's not great in areas that are otherwise brimming with machine activity, since repeatedly passing between louder and completely silent areas can be unnecessarily jarring and weird.

So we've gotta fill those gaps with something. Enter mapwide ambience.

We've actually had a couple of mapwide ambient tracks in the game for years now, originally labeled placeholders and essentially added to test out the system and also let players know this is a likely feature to be expanded upon. The one with which players will be most familiar is in the cave areas, a spooky organic drone that many commented on as being quite fitting for the area, and still others said they'd never even noticed xD (because technically I set the sample to quite a low base volume, and whether or not certain players could hear it might depend on their audio setup).

To fill gaps on other maps I wanted to expand on this idea, for the most part just using very low-key synth drones to act as a bridge between areas with sourced audio and set the overall tone with your average sci-fi background fare. Overall the tracks I'm using are relatively dark and mysterious, fitting with Cogmind's general atmosphere.

Now instead of 2 mapwide tracks we have 26 :)

I might go on to add additional random faint sound effects as necessary to serve as "accents" for the generic loops to liven the audio up just a bit, although I haven't done that at this phase yet, and even if it were to happen it probably wouldn't be until after Beta 10 releases with all the new audio, in order to leave time for broader feedback.

One issue that popped up with the mapwide tracks is that their desired volume level in otherwise silent areas could easily drown out some fainter or deeper machine sound effects when applied at the same level across the entire map. The answer seemed pretty obvious: Just lower the mapwide ambient volume when around other machines. Cogmind dynamically reduces the ambient volume by 50% of the loudest foreground loop's volume. For example if the player is passing near a machine they're hearing at 80% of its max volume, then the mapwide ambient audio is set to 60% volume (100-(80/2)). This seems to work quite well!

![](../../assets/e964a14b26631f61.png)


Visualizing only the volume level of the mapwide ambient track as it varies across a section of Factory map (as usual darker represents quieter).


# Results

As of this writing and the latest prerelease build I released for patrons, Cogmind gained an additional 117 sourced ambient sounds over the previous release and the soundscape is really coming together. It adds to the atmosphere without generally being too overwhelming despite the number of possible sources. There's usually no more than 2-3 different types within earshot of each other anyway, if that.

![](../../assets/8d58b2e1167431f5.png)


Visualizing the variety of machine audio across a Factory floor,

where each unique sound is associated with a random color.


These plus the 24 new mapwide tracks did, of course, expand Cogmind's disk size--a clean install now weighs in at 43.5 MB, a 45% increase over Beta 9.6. The audio samples went from comprising 46% of install size to 63%. Overall still pretty lightweight considering the massive number of samples included (by indie game standards), but Cogmind is certainly getting a bit hefty since its 3 MB 7DRL days :P

To see the latest WIP version of Cogmind's soundscape in action, check out my first Beta 10 prerelease stream where we'll explore the audio while fooling around and kicking butt:

In the next article we're going to take this whole thing to the next level by adding a closed caption-like feature in the form of an audio log, so you can get the full tactical advantages of this audio system even with the sound off! (Actually you can already see it in action in the stream recording above, but I'm going to go into detail about its design and the challenges I encountered in building it.)

(This article was originally published [here](https://www.gridsagegames.com/blog/2020/06/building-cogminds-ambient-soundscape/), on the Grid Sage Games dev blog.)