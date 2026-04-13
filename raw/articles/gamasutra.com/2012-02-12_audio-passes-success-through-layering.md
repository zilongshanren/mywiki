---
title: 'Audio Passes: Success Through Layering'
url: https://www.gamedeveloper.com/audio/audio-passes-success-through-layering
author: ALEXANDER BRANDON
published: '2012-02-12'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Audio Passes: Success Through Layering

Audio requires numerous iterations, both with technology and the creative process. Learn about these layers and how they can help your audio be more effective and integrated with the rest of the game.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

No, I’m not talking about free trips to GDC for audio folks. You’ll have to buy your pass like everyone else. And they’re well worth it. I’d like to discuss a concept that applies to both the creative process and technology when it comes to game sound.

In graphics technology and films, the concept of a pass or a layer is a single image combined (or composited) with other images to form a single frame. This might consist of a flat shaded cube, texture and / or material, a lighting pass, bump map, normal map, and so forth, combined to make an impressive looking realistic cube (or rock, or fuzzy dice). In the same way, audio has its own set of passes:

Raw sound, recorded or procedurally generated dry

Rendered in space (reverb, delay)

Dynamically mixed (mixing behavior relative to other sounds)

Sweetener (acoustic or synthetic frequencies added for the proper effect based on the context)


Keep your eye on the sound design section of the [Funky Rustic site](http://www.funkyrustic.net) for example mp3s of this.

As a concept this is easy enough to understand, however in addition to the passes listed above, creatively it’s rare that a single pass in the game space yields the perfect piece of music, sound or voice over. Let’s go through each set for some specifics. And I name these what I name them, you can call them whatever you want.

Music Passes

Concept: Before a lick of score goes in, take some concept art and generate concept music. The two of them living happily together along with design’s knowledge of the pacing of the game will work wonders down the road. And it keeps someone on the team from attempting to throw in some ludicrous genre because everyone will sign off on the concept music and have that in their heads as what works.

Mute: Yes, once the game begins development it is typically best to place your key sounds first, unless the game is a music game and the sfx are really musical bits. The key sounds will establish the important and high priority sonic elements that serve as your foundation for what the player’s ear will need to listen for.

Working: The working pass or layer is the concept of being able to have music connectivity to your game outside of any work done by the rest of the team. In UDK this is known as a sublevel in Kismet. In Unity it can exist as an instance of a prefab or a custom music manager script. The goal is to enable work to continue in parallel, not wait for a compiled build or someone else to give up a particular level before you can start working on implementing music.

Incidental: Taking a cue from your music appreciation class, this music is specific to the game. It does not set a mood, it does not establish a motif or a theme. It supports and enhances player activity and game reactivity. Easy examples are the 4th interval sound when Mario grabs a coin or the action of music playing backwards in “Braid”. One is a sound itself; the other is a sound behavior, more thoroughly implemented in the behavior pass.

Absolute: This can be any number of things, from a sweeping orchestral score (not many games do this, do they…) to something licensed off the radio to, well, anything. It can exist as loops or short segments, it can be a MIDI file, a MOD file, a WAV or MP3, OGG, you name it. The great part about this pass is that it will be mostly defined in your concept pass.

Behavior: Sure you can place your music, but you can also spend a long time tweaking just how it behaves both in the mix of the game once all sounds are placed as well as how it behaves. A stinger can be rewritten 10 times before it has just the right effect to provide a transition or serve as an appropriate intro to a loop. Wwise and FMOD both give you tools to integrate interactive music but it’s a fine art to really get it sounding seamless, and your composer and / or music supervisor should be prepared for several behavior passes in a title that has a lot of things going on that require unique music behavior. You may wish to consider this a polish pass and this pass may need to be repeated.

Sound Design Passes

Concept: Just as important as music, your sound design can be super realistic or 8 bit or filtered, or generative in some way. This is the perfect time to play with your style and see how it fits with the visuals. How much or how little ambience do you want? Set up an ideal mix and go from there with how it is to be implemented. Much better to compromise down the road than be overwhelmed with uncertainty when production really ramps up.

Placement: These will be temp assets, a first pass. A means to at least see how many sounds need to trigger and how to prioritize your channels and overall mix. Ensure your zones are set up and play with effects and effects chains (in Wwise there’s quite a difference between the convolution reverb and the standard ‘verb… but do you have the horsepower in your engine to pull it off?) and make sure you have a good solid template of limitations from channels to memory / streaming restrictions. You can also figure out how to assign mix groups should you be using them in a text file or setting them up in Wwise / FMOD. Last but not least during the placement pass is figuring out what triggers sound in a component fashion or what is baked into a single file and played back with a cinematic sequence. Or both.

Polish 1: This establishes at least that the effects are doing what they’re supposed to be doing. All your settings are fairly well set from mix levels to hookups.

Polish 2: This is more design and creative than anything else. You should be tweaking the effectiveness of your raw sounds and polishing them with whatever settings you can adjust in your engine. But it usually takes at least two polish passes before the sounds really shine properly as a group.

Voice Over Passes

While this might seem like it might be the easiest set, brace yourself folks. It ain’t. Voice over is by far and away the most removed discipline in all of game audio from that little important thing I like to call the game itself. With a sound designer you’re only a minute or so at most from your sound design and playing what you design in context. Voice actors typically don’t see squat. Think of Avatar and how Cameron broke new ground by placing the actors in the 3d landscape and simultaneously capturing their facial / mouth movements as well as their body movements. Games need this, and in fact games like Drake’s Fortune have already started down this path.

Script: It all starts with the script, and the script can knock out a lot of problems, but the script itself has sub passes.

Design: This is where you align properly with game events, and it gets refined throughout the cycle. The main rule of thumb is to not blatantly add words where none are necessary just because you’ve signed with the latest Hollywood star.

Table reads: Make sure your writing isn’t hokey. Read it out loud before you go anywhere near a studio and refine from there. The best way to do this is with a director who has experience in dialogue, or a dialogue coach.

Temp: Timing sometimes is needed before recording of final VO can take place. It could be that this is needed for blocking out scenes or for determining how much motion capture will be needed for a scene. This is a mistake but sometimes for whatever reason it needs to happen. If this is the case, auto generation of lines will not give you the proper timing. Have folks in house or better yet actors you have actually cast read these lines at home and put them in.

Simulcap: A few folks are able to provide actors with a scene to view or ADR, and even play a little before they act it out with both motion capture and voice over. If you’re lucky enough to have the technology to accomplish this, it eliminates a lot of back end work for timing and cohesion with the lines, and it is that step closer to the game that so many actors (and creative directors) deserve.

Recording: Standard recording is the way most of us go, and it’s oh so sad. But not to worry, if you record a number of takes and keep them all you can still manage to get a decent amount of vocal dimension and effectiveness in your game with a good director that can deliver the proper context. In addition you can benefit depending on the situation with ensemble recording with multiple actors in one room. Takes a bit more coordination but it has a great benefit in that the actors play off of preceding lines rather than having to imagine them being spoken, or read by the voice director.

Take these passes into account, producers and creative leads. Just as much in the way of polish is required on audio as it is with other disciplines, most particularly once the other disciplines have been signed off. A couple of weeks while programmers bugfix and optimize (TRC / submission as well) will do wonders for your audio if you build it into your schedule.