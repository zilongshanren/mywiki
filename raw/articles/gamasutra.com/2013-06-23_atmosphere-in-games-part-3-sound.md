---
title: Atmosphere in Games - Part 3 - Sound
url: https://www.gamedeveloper.com/audio/atmosphere-in-games---part-3---sound
author: Matthew Bentley
published: '2013-06-23'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![Loudness Wars Loudness Wars](https://www.prosoundweb.com/images/uploads/BobbyOHypercompressionGraphic.jpg?width=229&auto=webp&quality=80&disable=upscale)


Overcompression

(Courtesy of Bobby Owsinsky and the Mastering Engineer's Handbook)

There is a tendency for sound to pour from every orifice of a game, particularly in the AAA field now. You don't just have background music and sfx - you have constant exposure. Often with indie games, but also occasionally with popular titles, the sound is so poorly configured that you get high-level clipping with almost every sound effect when it combines with the music. In addition, the dynamic range is compressed out of both samples and music and as a result there's no hidden element or depth to the audio. You hear every detail but feel nothing (the same factor is present in most 'remastered' albums, but thats' another topic).

When a game gets it right, both music and sound effects are not significantly compressed (please note we are not talking audio codec compression here (ogg, .mp3 etc) but dynamic range compression - compression is an effect which almost always makes sounds feel unreal, unless the intention is to decrease the psychoacoustic distance between the viewer and the sound-eminating object. The most atmospheric sound effects will match the worldview and feel real, not 'hyped'. Hyped sound effects are appropriate for unrealistic sequences or for meta-world events (signaling end-of-level or powerup progression for example).


The bottom line is that a lot of games seem to make you /not/ listen to them by screaming at you constantly. A good sound/music scheme will invite you in, make you part of the team, not just show off. Obviously dialogue and SFX need to be both separated from and above the level of music, but there are multiple ways to do this (basic volume disparity, eq, stereo spread and stereo location) that don't involve 'cornholing' the audio. Further, individual repeated sound effects will feel far less grating and more natural when kept to reasonable levels of compression.

Asides from these largely technical notes, the creative process in creating sounds for games is simple: inject life into the game, ground it, and make something that fits the theme and style of the game. It's relatively difficult to get it wrong - though some people do.

A final point on sfx and music, and this one is solely for audio engineers: if you want to preserve that 'real world' feel, retain your 16khz-20khz frequencies rather than lo-passing them out - and make sure your audio codec preserves them too - most mp3 encoders for example lo-pass out these frequencies by default, however there is usually an option for leaving them in. The reason is, a lot of what makes the brain identify these sounds as 'real' is the somewhat less audible upper frequency information. Sure, some speakers won't reproduce them, but then, that's always a challenge we face.

Games which do this well:

Starcraft (AAA, payware): Although the SFX were somewhat compressed volume-wise, they didn't acieve maddening levels, always staying just high enough to be audible above the music. The fact that the music itself wasn't heavily 'mastered' probably helped, and to be honest for the most part the 'on-click' noises of the troops and buildings got a little irritating after two games, but they could be turned off. More to the point the SFX were clean, delivered stylistic and character 'feeling' information and got away with being a little humourous by poking some postmodern fun at the game itself.

Borderlands (AAA, payware): There was plenty of ambient space in the soundfx, the background music was good, the compression appropriate to both the weapons and their distancing and the overall style of the game was preserved throughout the aural piece.

Games which do this poorly:

Supercratebox (indie, freeware): Fitting with the retro theme, the sfx were fairly basic, and that's all well and good. However the loudness and distortion of the SFX were offputting in the extreme, and after a while, irritating.

NaaC (indie, freeware): The volume of the sound and music came together and clipped and distorted, and though it was possible to turn both down, the individual effects were also over-the-top clipped, unpleasant to listen to and unrealistic.