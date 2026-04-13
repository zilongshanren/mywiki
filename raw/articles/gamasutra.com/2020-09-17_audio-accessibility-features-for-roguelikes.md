---
title: Audio Accessibility Features for Roguelikes
url: https://www.gamedeveloper.com/audio/audio-accessibility-features-for-roguelikes
author: Josh Ge
published: '2020-09-17'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Audio Accessibility Features for Roguelikes

Explaining Cogmind's closed caption-like audio log, visible SFX, and other audio options, as well as discussing some parts of the implementation process.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Anyone who's followed my development work over the years will know that I'm big on providing all sorts of quality of life features, optional functionality, configurable settings, and so on. This is also why even from the earliest stages (pre-7DRL!), and ever since, I've given the utmost priority to Cogmind's interface.

How players interact with a game, both in terms of input and feedback, is vital to the experience, so even the greatest mechanics and content can be held back by insufficient attention to UX. Although it's a lot of work to always be putting the interface first (while still trying to maintain progress and design within the necessary constraints), and I sometimes have to pick and choose what I can implement as a result, I think it's been worth it in the long term. Not everything I'd like to do is really possible, but I try my best.

Having recently covered the new [ambient audio system](https://www.gamasutra.com/blogs/JoshGe/20200908/369616/Building_Cogminds_Ambient_Soundscape.php), today I'll be introducing Cogmind's audio-related accessibility features, features that other roguelike developers could potentially learn from and apply to help their players as well.

In particular I'll be talking about Cogmind's "visible SFX" system, allowing you to see the sources of sound effects, and the audio log for listing in text form both ambient and non-ambient sounds currently heard from Cogmind's position. As we'll see, the cool thing about both of these features is that they're not just for people who must have them by necessity for accessibility reasons, but can also help other players in certain situations! Like anyone playing with the volume low, or even muted, or in an otherwise loud environment--everyone can benefit :D

# Visible SFX

Originally a "what if" kinda feature that was mostly intended as a fun experiment, I immediately started liking the implications of being able to see the origin of sound effects outside your field of vision. This means being more aware of battles happening nearby, pinpointing enemies attacking from outside your visual range, locating undiscovered doors currently in use, knowing exactly where nearby garrison reinforcements are coming from... all kinds of useful applications. It's essentially a free type of sensor, but one that only works when the surroundings are changing and therefore often lends itself more to reactive than proactive tactics.

![](../../assets/895f74852541a4be.gif)


Visible SFX demo, "seeing" a battle playing out around the corner.


![](../../assets/7d3e3e97b580c797.gif)


More or less the same situation as above, but playing out on a black background so it's a bit clearer.


The animation is generally just a single flashed dot at the origin and a quickly fading box around it, although for sounds with especially longer ranges (usually explosions) and therefore presumably louder, the animation is both brighter and has a larger fade radius.

Visible SFX animations are also color-coded by sound type to make the indicators more useful, even more so when lots of things are happening at once:

Red: Combat-related

Orange: Door open/close

Yellow: Trap trigger, carrier deployment, or garrison dispatch

Blue: Emergency door open/close or phase wall destroyed

Green: Machine destroyed

Brown: Walls destroyed or cave-in


Successive red flashes mean there's fighting going on, naturally one of the more common situations, and if you didn't instigate it, then depending on your build and condition it might be wise to either avoid the area or hurry over to lend your firepower to whichever side is on good terms with you (hopefully one of them is? :P). Either way, the system offers more options for informed decision-making rather than flying blind.

Together with the extra positional information you otherwise wouldn't have simply by listening to the sounds, this feature also has the added advantage of better accessibility for hearing-impaired players, or anyone else playing without sound.

Although visible SFX are active by default, it's possible to turn off in the advanced configuration file in case the extra visual flair bothers someone.

(Visible SFX were added to Cogmind three years ago back in [Beta 1](https://www.gridsagegames.com/forums/index.php?topic=787), though I haven't mentioned them on the blog before.)

# Audio Log

Something I was excited to finally add to Cogmind, since I've wanted to do it for a very long time now, is the audio log. The audio log is meant primarily as an accessibility feature akin to closed captions, allowing anyone who keeps their volume low or muted to be able to retain access to important audio knowledge (alongside the visual SFX feature, although that one is much more of a perk for everyone). This optional feature is disabled by default, but after testing it out I think this'll be a pretty popular one even among those who don't require it.

## Features

Now, I say "closed captions," but it's definitely not a list of "pew-pew" and "kaboom" or anything like that, instead listing the name of the effect's source in a small window embedded in the top-right corner of the map view. Ambient sounds are listed first, followed by a separator, then any non-ambient sound effects (the latter category referring to one-time sounds like gunfire and explosions).

![](../../assets/6dfccc88c3727dac.gif)


Walking around a Materials map as the audio log updates to reflect machines that are being heard from each point.


The number to the left of each sound type indicates its current volume, which players can use as a proxy for distance.

Like visible SFX, the audio log also color-codes its contents to provide extra info where applicable:

Gray: Fluff machines, those serving to reflect the theme of the area and be destructible obstacles rather than serving an otherwise significant mechanical function.

Orange: Explosive machines. Beware.

Blue: Special-purpose machines with a unique function. Destroying these always has some effect.


![](../../assets/505773c4a47e4539.gif)


Watching the audio log while passing turns and occasionally moving around as a war is playing out nearby. This demo also makes it clearer that sounds are ordered by near-to-far rather than the order in which they were heard.


Non-ambient sounds are color-coded by category as well:

Yellow: Attacks and gunfire.

Orange: Explosions.

Red: Robot destruction. Very specific compared to other categories, but also very important so it gets its own color.

Green: A wide variety of events including traps, drones, turrets, scans, phase doors, door hacking--basically everything that doesn't fit in any of the other three categories.


When combined with the visible SFX system the non-ambient data is even more powerful: "see" this great fight heard outside the room as it's described by the audio log and blips on the map:

![](../../assets/428cdd5d1afc4ad2.gif)


Funny how it ends ;)


Not quite every sound appears in the log. In choosing what sounds to report in the audio log, in most cases it was geared towards information that is strategically helpful to know when out of view, rather than providing an exhaustive list. Limiting it to what really matters helps keep the log cleaner.

Although door interaction is fairly important, it is not reflected in the audio log since even if out of view they are clearly displayed via the visible SFX system, and their frequency is often rather high so it might threaten to drown out more meaningful sounds. An exception was made for phase wall interactions, since those are strategically important but do not reveal their precise location as a visible SFX source.

Other sounds that have clear visual alternatives are also generally excluded to avoid padding the audio log with unnecessary "noise." Examples include dispatch alerts, and the EMP charging and discharging in Waste (which come with their own graphics and messages).

So while the audio log technically doesn't paint a 100% complete picture of Cogmind's soundscape, it provides one aimed at an optimized play experience, not unlike the optimizations found in many other parts of the interface.

## Challenges

It was a surprising amount of work to finish the audio log, taking an entire week to complete as I discovered quite a few roadblocks along the way. Definitely worth it and I'm glad it's now implemented, but I expected it to take just a day or two xD

There were lots of questions to answer about this feature...

Right from the initial mockup stage we of course needed to know what kind of information would be conveyed. At first I was thinking distance alongside the name of the sound's origin (e.g. the machine--at this point I was only thinking about ambient loops), but then realized that precise distance is conveying more specific information than you get by simply hearing a machine. Overall I wanted to try to avoid making the audio log seem like a necessary feature for everyone to have active at all times, meaning the info provided should to be comparable to hearing a sound. So of course it should report the volume as a number (percentage), duh.

![](../../assets/f54cc0c06d66c27f.png)


Excerpt from my original audio log mockups. You can see there were yet more changes made after these ideas.


Then I was considering how an ambient sound list would treat multiple sources of the same type, like a group of Nuclear Reactors. The answer is to just do like the actual ambient audio system and only list the type once at its loudest current volume, again maintaining parity between the audio log and what is heard, but I clearly kept getting sidetracked thinking about all the new info made possible by this new format! The point is that throughout the process one of the roadblocks was myself--I repeatedly had to reign in these wild design thoughts :P

Naming the ambient sounds for the audio log wasn't hard since I already had a list of the sources and their respective names, and none of them are reused across different sources. Non-ambient sounds, however, were much more problematic since there was no precedent for this in the architecture (which of course hadn't taken it into account from the start), but including them is quite important for accessibility. After all, once you're familiar with the sounds certain weapons make, for example, the fact that you can hear them around the corner technically lets you guess what types of enemies (or allies) are fighting nearby, even without sensor data. This same information needs to be reflected in the audio log.

I experimented with a number of different approaches for the names of one-time sound effects, but after a complete survey of the parts involved (in particular weapons) determined that it made the most sense to use a single name associated with the audio sample and add no further differentiation. This means that weapon sounds do not necessarily list the specific weapon name, but instead the base name for the sound. For example there are a number of railgun variants that use the same sound, and the audio log will not differentiate between them, simply listing each as a "Railgun." Any weapons with unique sounds are indicated by their specific name where applicable, though. This, too, seems obvious in hindsight, again maintaining parity with what is heard, but it wasn't clear to me at first...

Other naming issues or ideas considered along the way:

I originally thought the audio log would have to take into account player knowledge, i.e. unknown parts or unidentified prototypes, but in the end it doesn't really make sense to obscure that information since players who generally play with the sound on learn to quickly recognize different SFX and retain that metaknowledge regardless of what the game would list in the log anyway. So we can ignore this limitation (which would otherwise be a hugely complex possibility to account for). Bullet dodged.

At one point I also thought about using descriptive names that didn't exactly match weapon names, e.g. "Weak Laser" for Small Lasers or Backup Lasers, since both use same sound effect, but this approach doesn't scale well at all and would just end up being unnecessarily confusing, forcing players to learn a whole new set of words just for this feature.

Then I also thought about using a special type of marker, prefixing the sound name with a tilde (~) in certain cases to represent that the sound belongs to a category of multiple variants and it could be any of them, but that seemed like unnecessary extra info so I simply removed all of those from the data.


Under the final naming system explosion sounds were an issue since many of the same samples are shared across different types of sources such as launchers, machines, and traps, so for those I opted to go with a more generic "Explosion (XX)", where the XX refers to the common abbreviation for the relevant damage type.

Multiprojectile weapons presented one of the biggest problems, one for which I sadly only found a partial solution. Each projectile actually plays its own sound because of how the projectile mechanics are tied to the particle system, and because the audio log is directly tied into the sound system, which doesn't know about game mechanics or what's really happening, thus a single weapon can cause more than one (or even numerous!) entries to appear at once.

The best solution I could come up with for limiting the extra entries involved adding a variable set manually for each sound effect that essentially blocks a predetermined number of subsequent matching audio log messages after the first. Hacky, yes, but it mostly works...

For example an EM Shotgun fires two projectiles, each playing the same sound*, but because the sound effect has a '1' assigned to that variable, on playing the sound the first time the audio system records that it should simply block the next attempt from being logged. (*Note that even though it's the same sound, weapons tend to randomly modify their pitch for each firing/projectile, and multiprojectile weapons in particular may also add a random but slight amount of staggering to their projectile firing times.)

Unfortunately it's not a perfect solution because the value must be set at the SFX level, but in rare cases some weapons use the same sound effect but each fire a different number of projectiles, so there are a small handful weapons for which the log might desync on certain turns, though in most cases these are not weapons enemies use anyway (only Cogmind does), so it should rarely if ever come into play.

Technically I suppose we could just always report every single projectile as a separate audio entry, but for some weapons that could get excessive, and it also just makes the log harder to read by polluting it with extra lines, so maybe I could change it later, but for now we'll stick with this method.

Aside: I did actually test the per-projectile approach, using the standard roguelike message log behavior for duplicate entries, but that didn't pan out. The idea was to merge duplicate entries with a multiplier, like "50 / Flak Gun (x6)" and so on, simply allowing multiple projectiles to stack when they are of the same type and volume. One problem here is that weapon sound effects are often heard at maximum volume across a decent range, leading to lots of overlap in the log and making it difficult to discern just how many different weapons are being heard (or at least require the player to do some math when there are lots of things happening at once). The potential gains here (being precise and consistent in every case) didn't outweigh the costs (confusing!), and considering how rare it is for enemies to have a weapon that might cause temporary audio log desyncing, I prefer that the log show weapons on a per-weapon basis rather than per-projectile. Obviously most games don't have to worry about this kind of thing at all--it's kind of a weird situation likely unique to the way Cogmind's projectile, logic, and audio systems interact :P

Altogether it was a lot of work to go back through every sound and projectile, cross-referencing all their uses in order to assign names and other values for audio log purposes, but eventually that was done and... oh wait, there was still more to do xD

Aside from the content, the new audio log's existence itself caused some issues. For one its design places it against the right edge of the map, which would obscure any intel markers appearing along that edge segment.

To resolve that I spent a while updating the intel marker placement system to get them to avoid the window itself:

![](../../assets/894e175ab8e0bb16.gif)


The audio log displacing various intel markers that would appear along the right edge.


Labels for offscreen exits needed a similar treatment, although there are always far fewer of those, so I opted to instead just shift them downward rather than pushing them to the left of the audio log window:

![](../../assets/a072f4da41442335.gif)


The audio log displacing various offscreen exit labels by pushing them downward if they would otherwise appear behind the window.


In hindsight maybe it'd be better to just treat the audio log like most other on-map windows that can appear and displace it from every edge by 1 column/row, although I felt like the right side should be snug against the edge since this particular window doesn't have its own border. So maybe it needs its own border??? As a result of writing this article to here I had to mock it up :P

![](../../assets/241e121e0b7242a0.png)


Mockup for an alternative audio log concept, with a border and increased padding.


This option occupies more space (and has to leave even more space for markers), but I guess the consistency could be worth it? It also serves to better separate the log from the map behind it so that it's more clearly it's own thing, which is kinda nice. Cogmind's special mode UI windows that appear at the bottom-left of the map already do this, as do the achievement icons that appear in the bottom right when those are earned...

That said, I saw the audio log as more of a right-adjusted counterpart to the full combat log appearing at the top-left of the map, also without any border. Designwise that one is slightly different, however, because as left-adjusted lines (and potentially long ones at that) it felt fine to have them cover only as much of the map as they needed to on a per-line basis, whereas the audio log on the right works better when the width of the area covered is uniform.

Anyway, I'll have to think about that one. (Edit: On discussing this with patrons, one good point brought up by Tone is that an explicitly bordered window that frequently changes its height could end up being more distracting, which makes a lot of sense and is good reason to leave it as is, without the border, like its similarly "shapeshifting" borderless counterpart, the full combat log.)

There you have it, just a sampling of the problems encountered in building the audio log--there were lots of other little ones, mostly specific to how Cogmind's architecture works, its limitations, or trying to get information from one place to another, and, again, overall it took a full week to finish this "little" feature for which a lot of the foundation had already been established!

## Options

The audio log itself is optional, off by default but accessible from the options menu. As usual, I've also made some of its behaviors tweakable where that may be desirable:

Normally ambient sounds are always listed, while non-ambient sounds are only shown when the origin is outside Cogmind's FOV. Although this goes against the idea of a truly complete "closed captioning" system, this is actually a more reasonable approach to default to since you can clearly see visible attacks and other sources of audio anyway, and this behavior also keeps the audio log focused on sources currently out of view without letting it become too cluttered with duplicate information. But of course the option is always there to include every sound effect if someone wants/needs to expand the rules. Regardless of this setting, non-ambient sounds originating from Cogmind's own position (mainly attacks) aren't reported to the audio log, since those should be obvious and would just clog up the log with too much info.

Ambient sources ended up being listed regardless of whether they're in view because even though it might've similarly made sense to only list those that are outside FOV, it turns out this was completely impossible without rewriting much of the ambient audio system xD. No matter, it's fun (and sometimes convenient) to see those listed, anyway, and they're definitely not excessive like non-ambient sounds can be!

Fluff machines (reminder: those that do not explode and have no special mechanical purpose) are normally included in the audio log, but there is also a setting to exclude them to avoid the extra noise. I imagine most players would want to leave them on for a number of reasons, though preferences could depend on what other settings are being used.

The maximum length of the log is adjustable, too (down to the bottom of the map view, which is actually the default), as is the length of time for which non-ambient sound effects remain visible before disappearing from the log.

# General Audio Settings

As a majoraccessibility feature the audio log toggle has been given a place in the Audio section of Cogmind's primary options menu, alongside several other options some might find useful.

![](../../assets/f43772163de19f82.png)


Cogmind's latest options menu layout and contents.


Of course there's a master volume control, but as part of that each of four separate channel categories can also be adjusted individually to change their relative volume. "Interface" includes all the UI feedback, the beeps and clicks and alerts, etc.; "Game"covers mechanics, combat, and other events; "Props" are all the environment objects like machines (basically any ambient loops that aren't the mapwide audio); and "Locale" refers to the mapwide ambient audio track for the current map.

Over the years I've also added a couple other special audio options by request, though these only appear in the advanced configuration file:

muteTextSfx: Some players are sensitive to the text typing sound, which is pretty ubiquitous in Cogmind because there's text being printed to the log all the time as things are happening, but it usually isn't a vital part of the interface feedback, so I added a way to disable that particular effect.

muteGlobalAlertSfx: At least one player didn't like hearing global alerts, generally referring to enemy squad dispatches as a result of your presence or actions, or otherwise potential danger coming your way, so I added a separate way to disable those. Alert situations are also accompanied by a more specific white log message and an additional flashing message at the top of the map view, anyway, so it's usually not too hard to miss. Personally I tended to miss anything except an alarm playing, but the idea of options is that not everyone has the same observational habits or abilities so making things customizable is usually advantageous where possible.


As with many of Cogmind's huge range of quality of life features, it took a while to reach the current state--naturally not every issue will be foreseen and implemented right away, and it can take years to properly add all this stuff to a game (especially as a solo dev), but in the long run listening to feedback from players and doing what I can to offer improvements to the experience has been an important part of the process.

# SFX, Stereo, Action!

You can see both the visible SFX and audio log in action in my first Beta 10 prerelease stream in which I introduced the log alongside the new soundscape: