---
title: 'Armello: The tools, tips and tricks that allow us to perform our magic'
url: https://www.gamedeveloper.com/audio/armello-the-tools-tips-and-tricks-that-allow-us-to-perform-our-magic
author: Stephan Schutze
published: '2015-09-16'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Armello: The tools, tips and tricks that allow us to perform our magic

Creating and implementing all the sounds for a project in less than a month would always be a challenge. When the game is as unique and beautiful as Armello, with a stunning musical score already in place, the expectations increase dramatically.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Never underestimate the value experience has in the games industry. Those of us privileged enough to have been working on games for many years can draw on our knowledge and understanding of the different processes available to help us get our work done. But it is the tools, resources and established workflows that often really help us perform the impossible; create the magic and breathe the life into our projects.

The Clans of the Kingdom sense a darkness is growing

[Armello](http://armello.com/) has been a passion project for the [League of Geeks](http://leagueofgeeks.com/) team since its inception nearly four years ago. Like many game projects, it started as a simple idea and grew in scope and design over time. Fortunately, unlike many projects, Armello did not fall victim to the many (sometimes fatal) issues that can crop up during the development process. Armello has become a true success story for the passion of its Indy developers.

[Defiant Development’s](http://defiantdev.com/) founder Morgan Jaffit [recently suggested](https://medium.com/@morganjaffit/indipocalypse-or-the-birth-of-triple-i-eba64292cd7a) that high-calibre, independently developed games need their own descriptive label, as AAA is problematic when compared to the products of multi-million dollar studio budgets. He suggested the term Triple I (III), which I think is a perfect description for the accomplishments of Independent developers. Armello is a true III game in every sense of the word.

To say I was brought on late in the schedule is accurate, bordering on understatement. When I came on board, Armello already had an incredibly strong design, a gorgeous visual aesthetic, and most of its music had been produced and implemented. [Michael Allen](http://michaelallen.com.au/about.html) had written a stunning and evocative musical score that included vocal parts performed by [Lisa Gerrard](http://www.lisagerrard.com/). Everything about Armello had been produced to the highest standard. Now it needed SFX to complete the world, but time was very short.


What Went Wrong?

Game development is difficult, game development is very difficult. Anyone that has ever completed a game project will freely admit that often it can be a bit of a miracle that a game ever sees the light of day. So while Armello was driven by passion, it was no less vulnerable to the very real issues that can plague development.

By necessity, any game in development for more than three years will need to evolve its design, update its processes and toolset. Armello was no different. The release of [Unity 5](https://unity3d.com/) provided an excellent opportunity for the League of Geeks team to update their animation workflow and create a better game. Combined with a new agreement with Sony to release Armello on PS4, the development bar was continually being raised.

Unity 5 provided a significant update to the game-engine toolset and allowed Armello to continue to develop at the highest possible levels for PS4. Unfortunately, the Unity 5 audio feature set was brand new and as such posed a high risk so late in development. While the Unity 5 audio solutions may have ultimately provided everything that Armello required there was a risk/reward call to make. A solution was needed that would future-proof the Armello project through release, updates and possible DLC as well as multiple cross-platform deployment. This meant time needed to be spent at a very late stage of development to refactor the audio and redesign how it all worked. Essentially, Armello’s entire SFX suite needed to be rebuilt within only a few weeks. Regardless of the exciting new features Unity 5 Audio might have offered, the timeframe required a known toolset to create and implement Armello’s audio.

Tools of the Trade

Just prior to me being brought on, the team had made a decision to work with the FMOD Studio middleware solution. The FMOD team was literally just down the road from the LoG studio, further mitigating the risk if problems should arise. The basic functionality had already been implemented by the code team and the music had started to be worked into the game world.

I was brought on board with less than a month to design, create, implement and balance the vast majority of the non-music audio assets.

My experience with FMOD Studio was more than just a benefit in this situation, if it had been any other tool, it probably would have been an impossible task for me. This brings me to one of the principle points of this article. There are a number of quality middleware solutions for audio production in games. The argument of which tool is best is not at issue here, rather, my point is that every sound designer for games should make sure that they are proficient to a very high level with at least one of the audio middleware packages. For situations like this where you need to achieve seemingly impossible outcomes, a thorough working knowledge and understanding of a toolset is the only way to master the situation.

The second key point of this article was something of a revelation to me, that I only discovered because of the demanding circumstances I encountered working on Armello’s audio. SFX libraries are not only powerful as a resource but can quite literally make the difference between success and failure!

I want to pause for a second on this point and put this statement into context. For over 16 years, I have created and implemented assets for game audio, but within that time I have almost never used SFX libraries, in fact I have usually created them. I have always had a policy of going out and recording all my own raw material, designing and building my own sounds, and using those in game. It was this very process that began [Sound Librarian](http://www.soundlibrarian.com/) as a company. So while I was happy to record and create libraries for others to use, I was actually a terrible advocate for my own product. Having gone through the recent, high-pressure development process with Armello, I have now seen that this was a poor decision. Looking back at my previous attitude, I detect a regrettable omission; I believed that any sound I would ever need, I could record myself. My assumption that recording my own sounds was all I would ever need completely overlooked the outstanding work produced by other SFX library producers.

For a project like Armello, there was no way I could ever recording all the raw material I needed in the time available, so I turned to the libraries I had available. Specifically, beyond my own Sound Librarian collection, I had access to the [Pro Sound Effects Master Library](http://shop.prosoundeffects.com/products/pro-sound-effects-master-library).*

While having access to hundreds of thousands of sounds was a boon, it still came down to the “how and why” of every decision for the audio. I needed to work out the best approach to create a large number of sound assets in a short period of time, and importantly I needed to include the optimisation process into the design process, which is not how I usually work. My usual process is to cram in all the sounds I want to use and then, at a later date, optimize to make it all work once it is sounding good. Fortunately for me, recent conversations with experienced audio people about the use of sweeteners in sound design helped me realize this could be the perfect way to achieve the results I needed in the time allowed.


Armello's stunning visual style is a tribute to its creators.

Sweetening the Deal

Audio sweeteners have long been used in film and television production. Sweeps, drones, pulses and impacts can significantly enhance a visual experience. A subtle whoosh sound accompanying a camera movement is actually a very common thing in media. Most people are not even aware they are hearing it as it exists less as a distinct sound effect and more as an element of the visuals. Low frequency sounds similarly work to enhance other sound effects for the sub-woofer channel. For Armello, I used sweeteners as a bonding agent across the entire audio design to help tie the audio environment together and add a cinematic quality to the SFX.

So instead of my usual process of bundling everything together and sorting it out once it sounded right, I started as I would often start when writing music, by auditioning my instruments and building up a palette of “colors.” I searched my sound libraries for every sweep, whoosh, drone, pulse and impact I could find. I auditioned every single one (and there were thousands) and copied the ones I liked into a separate folder. This was my ammunition box, or jar of screws from which I would be drawing regularly.

How it all Worked

Combining the functionality of FMOD Studio with my “jar of screws” not only sped up the asset creation process, but it let me develop a specific, and efficient, workflow. By selecting a range of sweeps and other sweeteners I was able to define a series of core sound textures that would function as layers across many of the required sound events. I named my sweeteners appropriately to help me with rapid prototyping and development. So I was working with things like:

Dark_Surge

Magic_Sweep

Attack_Layer

Corrupted_Drone

Each of these would have multiple examples to draw from. The advantage of doing this in FMOD was that once those sound files were added to the Audio Bin they became part of the project and would remain in memory. This meant there was no limit on their use. So the process of adding consistent sound layers across the project was also incredibly resource efficient.

For example, Dark_Surge may work as the perfect accompaniment for the spawning of a Bane. The ominous low frequency content adds good weight to the creation of an evil creature. However the spawn sound for the Bane consists of multiple layers all triggered in real-time as the creature appears. This means that Dark_Surge is blended as part of that sound event. The exact same sound file can then be used again, blended with different sounds to create an ambience for dungeon exploration, pitched up and used as a layer for the death of a King’s Guard, or pitched down still elsewhere to become an ambient drone. In this example, Dark_Surge is an indicator of a bad occurrence. The player will subconsciously start associate that sound layer with bad situations. This significantly strengthens the communication between the game and the player.

A Bane spawns from a dark portal at night

This is more than just resource efficiency. The reuse of a series of SFX for various audio events creates a strong binding consistency across the overall game. If I use a specific sound as a layer within multiple sound events it ties those events together. If that layer exists within the sound events for the following game events it strengthens their bond:

Healing Spell

The healing effect of a Stone Circle terrain tile

A Temporary HP buff from a character event

An equipable item that protects the user

All of these events are related to character health, so sharing a sound element strengthens this relationship. In many cases the connection is subtle, as the sweetening layer may be one of multiple audio tracks and may even be blended very low in the mix, but this can still enhance the relationship. Do not underestimate the sophistication of human hearing. We may not consciously be aware that a common layer exists across several sounds, but we will subconsciously link those sounds as we feel the familiarity of the frequency content.

The final benefit for this method is that it is fast. Once I have established the layer I want for a specific event type I can instantly establish templates for this event types. I know my core sound textures for all my elemental magic; I have a binding theme for all my character clan sounds. The inspiration for each type of sound was already there, and once I had the core sweeteners defined, my sound design happened much faster than I imagined.

I am not advocating the use of raw sound library materials as your final solution; you still need to “own” the sounds you create and make them yours. The identity of your game can ride on the effectiveness and originality of your sound design. Simply dropping in a sound from a library will always seem lazy to me. Sound libraries are your ingredients and it is only when you combine them carefully that you achieve the best results.

Using What You Know

Another trick I made use of was one of the techniques I had developed working on [Defect: Spaceship Destruction Kit](http://sdkgame.com/). For Defect, I have been using reference events commonly across the music system. For Armello, these became a valuable part of the workflow for SFX creation.

In FMOD Studio you can drag an existing Event into another Event and it will be triggered just like any other sound object. This creates a Reference Event. The power of this functionality is that you can later make edits and changes to the original referenced Event and these will instantly update across all uses of that Event within the project.

In Armello I used this technique for all the combat elements. I created a series of sounds, sword clashes, armour impacts, swipes, metallic “shling” sounds and allocated these all to a separate folder. I would then draw from this folder any time I needed to create a sound for a combat action.

Important Tip: A Reference Event acts like a basic sound file within its parent event AND it adopts the characteristics OF its parent event. This meant that I could create the combat elements as 2D Events within FMOD. I could then deploy them within other 2D Sound Events to be used in Armello’s 2D dice combat screen and the sounds including the reference events would trigger correctly as 2D sounds. Equally I could add them the reference sounds to 3D Sound Events and sync them up to the animations of the 3D characters in the map screen and they would function correctly spatialized within the 3D game world. So the reference events became the core of all combat events both 2D and 3D across the entire game. This method is efficient on resources and a huge time saver.



2D Combat resolution screen

The other advantage of Reference Events was the universal updating. As progress was made on the audio, feedback came through from the designers, “The Shield Block sound needs less metal elements in it as it is being confused with the sword hit sounds.” Making a change to the core Shield Block sound meant every instance of that sound instantly updated. This saved hours of reworking and tuning the audio. It meant that I could respond to requests for edits and tweaks quickly without having a major impact on the short timeframe I had to work with.


Be Nice to Your Coders

I generally apply the above statement all the time, but more than anything the late stage of development of Armello meant there simply was no time for the programmers to give me even if I had wanted it. Data-driven audio is exactly how you deal with this situation. By making use of Parameters within the project, I was able to gain significant control over various aspects of the audio playback without requiring significant systems to be coded up by the programmers.

I redesigned the entire environmental system to work from a couple of parameters. Day/Night and Summer/Winter provided a significant level of control over what the player would hear. To be exact, there was a Night Parameter that functioned from zero to one, either it was night time or it wasn’t. The Winter Parameter worked in the same manner.

With these two pieces of information, I created a single Sound Event. Within that Event, I could define if the players would hear bird ambiences during the day on the summer map, or insects and frogs during the night. Night time would include sounds of owls and wolves. If it was winter the birds would be replaced with a chilling wind sound and the occasional fall of snow from the leaves. All of these elements were generative in nature, so they were efficient on resources, removed repetition entirely and created a more realistic dynamic environment. 90% of Armello players will never notice or be aware of any of this, but hopefully they will feel like they are experiencing an engaging and realistic world environment.

Importantly, these Parameters provide data to the audio system that you can use for whatever you need. So the day/night data can now drive the appropriate musical cues, the summer/winter data defines if the character footsteps are the soft impact of grass or the crunch of snow. The brief period of time that was required of a programmer to link up this data, which the game was already tracking, was well worth the effort. In future content such as updates and DLC, this facilitates the rapid deployment of dynamic audio elements.

Day & Night, Summer & Winter, Armello is always beautiful

Mixing and Debugging

Beyond the three weeks I had to create and implement content, I had a few sporadic days with which to debug and mix the project ready for launch on PS4. Bugs were fairly rare; I will put that down to a combination of good planning (16 years’ experience should account for something) and good luck. Integrating FMOD Studio into Unity 5 is straightforward, and that is a tribute to both development teams.

Being able to Live Link the FMOD project to Armello as it was running in Unity to mix the audio, look for issues and make changes, is another thing that contributed to this tight schedule being achievable. I created a series of Snapshots of the audio to lower or “duck” the volume at certain times during gameplay. So when a quest is started, all the other audio would lower to get out of the way, making the quest-specific ambience and UI sounds clearly audible. A second Snapshot lowered all the volume levels within the winter environment and completely removed any reverb from the mix to provide a still, dampened audio world.

Both of these mix steps were created and balanced in real time while playing the game. This is the only way to mix any game with 3D elements as position plays a part in defining output levels. The occasional use of the Profiler allowed to me to find out if I had done something wrong, or if there was a greater issue at play.

In Conclusion

I would certainly not say that being required to produce and implement the audio for a game the size of Armello in about a month is my preferred way of operating; however as a general rule many of us do perform better under pressure. When I started in the games industry many years ago the tools to make something like this even possible simply did not exist. So while knowledge and experience does account for a lot, and I personally love learning new aspects of my craft, I am extremely happy that we now have powerful game audio engines, and integrated middleware solutions (even if they do all crash occasionally). These can be combined with a growing wealth of sound assets in SFX libraries produced by passionate recordists that can inspire us as they enable us.

I learnt some really valuable things in the short time I worked on Armello and this is another reason why I love this industry so much. What could have been seen as a high pressure, panic situation with a short schedule, revealed itself as an opportunity to learn something new. I think creative people are at their best when they are constantly learning, it is how we evolve our skills. I am already turning my new love of SFX collections to other projects as I realize not only do I not have to do all the work, I will get a better result if I take advantage of all of the audio resources available to me. I am looking forward to continuing to support Armello and contribute to its magical realm.

* Sound Librarian material is included within the Pro Sound Effects Master Collection, that is why I had access to this library.

Stephan Schütze is the Co-Founder and Director of [http://www.soundlibrarian.com ](http://www.soundlibrarian.com );