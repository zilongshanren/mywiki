---
title: Adaptive Audio for Mobile
url: https://www.gamedeveloper.com/audio/adaptive-audio-for-mobile
author: Game Developer
published: '2015-03-11'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Adaptive Audio for Mobile

An look at some of the adaptive, mix specific features we've developed for our new mobile game at CWF. I'll detail some of the unique challenges we faced in making a game aimed at children playing in a classroom environment... with headphones.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)


![Zorbit's Math Adventure K1 Zorbit's Math Adventure K1](https://dl.dropboxusercontent.com/u/2185137/article_images/K1Images/logo.jpeg?width=1280&auto=webp&quality=80&disable=upscale)


This is a kind of sequel to a previous article I put out [earlier this year](http://gamasutra.com/blogs/RobBridgett/20140405/208210/ReImagining_the_Sound_of_PreSchool_Games.php) on Zorbit’s Math Adventure. This time around, I’ll be taking a closer look at some of the thinking behind a few specific new audio features and approaches to listening in our new game series, Zorbit for Kindergarten.

First, a little background...

Clockwork Fox Studios is a small independent developer based on St John’s, Newfoundland, Canada. For the past couple of years we’ve been developing kids math games, with a focus on fun for the player combined with useful data tracking for teachers. With our small team’s background in film, TV animation and console game development we have always put quality and player experience first in our development approach. Though, for this series of games, aimed specifically at Kindergarten children in a classroom setting, we’ve dug a lot deeper in extending that experience to include teachers.

Developing an Adaptive Product

Many games aimed at younger children offer little more than distraction, a way for parents to keep the kids busy and engaged for perhaps a few minutes, or even an hour or two. Some titles also offer a tantalizing prospect of educational content - whether or not they deliver on this is sometimes difficult to qualify.

Some developers do offer data tracking features for parents that display certain kinds of progress and milestone achievement data. We beleive strength in both of these areas, entertainment and meaningful data, is the future path of children's interactive entertainment, but that this too is only the first step.

Our new game series is focussed on Kindergarten Math, and we realized that the thing we were developing, ‘the game’, was only really part of the wider solution, and that If we were going to solve anything at a classroom level with teachers involved, we had to take a look at the entire experience of teachers and children and position the game as a performance data collector at the heart of that experience.

The solution we came up with was to create a game that not only tracked performance data on the child’s progress in the specific actions and areas of the game (broken down into different areas of the math curriculum), but that also employed adaptive difficulty algorithms to ensure that the difficulty curve at which each child was playing, and content the child is seeing, was always suited to their skills. Alongside this, we developed the game to be the engine behind a robust and connected live overview web portal for teachers, in which they can track progress of individuals or the entire classroom, looking at the specific flags for either individual children struggling or excelling with particular areas of the game (and even suggesting specifically tailored worksheets and activities for them to help with those specific problems) or overall classroom trends of progress through various topics areas.

Mapping Adaptive Ideas to Audio

So, we have a lot of things going on in our games and services under the surface, and a key product pillar of a "fun experience that supports and adapts to a child's needs". There were a great many additional technical challenges that needed to be considered to provide a seamless exprience tailored for each different player in each unique environment.

The underlying principle behind our audio direction for every product at the studio, is to provide the absolute best listening experience for the user, and nowhere else could the case for an exceptional listening experience be made more explicit than with very young, sensetive ears.

Many of the elements of the soundtrack needed to function to not only engage and entertain the children playing, but also to provide a clear and coherent experience focusing around instructional and feedback dialogue where needed and supporting a fun context for exploring and solving math problems. At its very core though, the experience needed to be clear, intelligible and appropriately balanced for the audience's young ears. The main challenge was that this game is developed as a mobile experience and could theoretically be used in (and need to be perfectly audible in) a huge variety of scenarios from classroom to home or travel situations.

There are two main areas/features that I can focus on to best illustrate where we took the throughline and notion of an ‘adaptive’ experience and applied it to the soundtrack.

I'll get into a little of our overall 'adaptive' approach to areas like music state switching centred around the player's activity, and then dig into detail on two complimentary systems, that of an adaptive loudness model based on device output and an adaptive output compression model driven by the loudness of the user's environment.

Adaptive vs Interactive

A good thing to probably do up front is distinguish what I mean by ‘adaptive’ rather than ‘interactive’. By adaptive, I’m describing a system that is aware of the activity of the user through collection of data, which then makes changes of certain factors to either fit that behavior, or to adjust certain parameters and responses to best cater for that behavior. It is a system that doesn’t ask for a user-input, but makes changes on their behalf based on data collected. By interactive, I simply mean that a user has access to, and control over, certain elements of the experience.

We had plenty of interactive systems in place, our in-game ambience model is a good example of an interactive system that was developed as a toy-like free play environment which can be changed by the player at will. Dialogue branches too could be considered interactive, being based on set responses to correct or incorrect actions and conveying specific feedback to the player.

Yet, inside the activities themselves we made use of a simple adaptive music engine based on player activity.

We developed a very simple, user-focused, adaptive method of switching the music based on when the player was interacting with the game or not. Having this as the overriding reason for playing musical accompaniament in the first place was, for us, a more interesting proposition than us using music to ‘tell the player what they should be feeling or doing’ via music. This way, if a child had to stop playing to take a break, or to listen to a teacher’s comments for a while, the music doesn’t become an annoying factor in the experience where they need to reach for the pause, mute or volume. Music will also come to a natural end if no interaction is detected for ~15 seconds. The two zones, active & calm, also allow us to force transitions to 'less busy' music scoring in order to hear important dialogue etc, which is useful in helping the mix elements be less competitive.

![Adaptive Music Adaptive Music](https://dl.dropboxusercontent.com/u/2185137/article_images/K1Images/adaptivemusic.jpeg?width=1280&auto=webp&quality=80&disable=upscale)


(Adaptive music switching based on player input)

Adaptive Loudness

Mobile gaming can only really said to have reached a mass market in the last 5 or 6 years, and with this has come a unique set of challenges for audio content creators in terms of tailoring their audio to sound its best over a small device’s speaker. Sounds pretty simple, design and eq all the sounds for the speaker, make sure everything is sounding great coming out of that speaker and you’re done. The issue is complicated once you consider that the user may be wearing headphones, and not even listening on the speaker at all. This usually leads to the following audio connundrum... Do you try to gather data to support the use of one method of listening over another, in order to make a best guess to support one output mix over another? Or do you consider that both may be equally valid and must both sound their absolute best? Straddling over this divide to find a feasible range with a single mix approach is, at best, a compromise, at worst an poor experience delivered to the most non-supported output. How does this approach stand up when we add a third potential output scenario, that of mirroring the game to an apple TV via AirPlay? What happens when you consider that one of the most important factors here isn’t just the EQ or audibility of the assets, but overall loudness or loudness range?

In console games, the approach of providing several different mixes for the various outputs has long been established (Battlefield, Uncharted, Prototype 2 et al). Mixes tailored for stereo, 7.1 and 5.1 are fairly common now. The main difference being that these settings are often left open for the player to figure out and have control over inside an options menu. This assumes a fair degree of comprehension of things like dynamic range and compression on the part of the player, and to remedy this we’ve seen these modes renamed as more consumer friendly terms like ‘war tapes’ etc.

So, here's how we approached this on mobile. For our games, which are aimed at 5 year old children, even exposing the most simple user-option is a difficult proposition (we have a music on/off toggle button, and that is the full extent of all our user-options) In the case of our game, and by extension in the case of nearly any kind of game designed for a mobile device, a differentiation of the mix could be applied adaptively to suit the output method that is currently being used by the player. In our previous title, Zorbit's Math Adventure, we hard-coded a similar system for detecting headphones and reducing output level to protect children's ears, but we wanted to push further for our Kindergarten games and for more nuanced adaptive control this time around by using Audiokinetic's Wwise as our middleware.

Another of the reasons that we've found adaptive predictive systems work better in the mobile environment is that an adaptive system knows that you are using headphones (or speaker, or AirPlay), without you needing to go into the options and manually set what you think is the appropriate mix. One of the main reasons for this is that the OS and the device are distinctly architected as one and are aware of the states of many of these hardware inputs and outputs. It is a design approach that I’m confident we'll see more of in the future, perhaps even in console and PC architecture.

In terms of implementing these changes to the loudness of the game. We identified three main paths; headphones, airplay and device speaker that were likely routes for people playing our game.

Getting notified of these conditions was fairly straightforward from the programming side (via a unity plug-in skillyfully written by our audio programmer Matt Dominey), as was the loudness adjustment side of things inside Wwise via the creation of three mix simple states…

![Output States Output States](https://dl.dropboxusercontent.com/u/2185137/article_images/K1Images/OutputStates.png?width=1280&auto=webp&quality=80&disable=upscale)


Output States in Wwise

These mix states could then be used to alter the levels for individual buses, such as particular character dialogue buses, overall dialogue levels, or overall music and fx levels. The default levels, with no attenuation, were used for the speaker loudness, and downward attenuation was expressed inside the mixer states by moving the volumes of various busses down with the state changes...

![headphone attenuation headphone attenuation](https://dl.dropboxusercontent.com/u/2185137/article_images/K1Images/state_attenuation_headphones.png?width=1280&auto=webp&quality=80&disable=upscale)


(Above) Headphone Attenuation in the mixer

![AirPlay attenuation AirPlay attenuation](https://dl.dropboxusercontent.com/u/2185137/article_images/K1Images/state_attenuation_airplay.png?width=1280&auto=webp&quality=80&disable=upscale)


(Above) AirPlay Attenuation in the mixer

Focusing on the classroom setting, as well as supporting the home environment gave us more confidence to fully recommend and support headphone-use for this game (wheras with our pre-kindergarten game aimed at prantes/home it was most likely in a travel scenario), while also remaining aware that the use-cases for classrooms are anything but predictable.

Now we know that our device can provide us with where the audio path is being routed, it is a "simple" matter of coming up with loudness specifications that will suit each of those output destinations. Here is what we came up with...

Speaker -18LUFS (-16 is often recommended here, yet I found this to be too loud for the device speaker on iOS when considering small children as the audience, who often get closer to the speaker than an adult would)

AirPlay -23LUFS (This makes sure that any content played on a home TV or home entertainment system will match that of the content created for that zone via ITU BS .1770-3 broadcast standards and thus be in line with kid's TV shows and movies)

Headphones -28LUFS (We could have gone quieter here to be honest, the variety of headphones available with differing ohmage means that there is still a wide spectrum of loudness that can’t be controlled in the way it can for the device speaker. I went with what felt comfortable over the most over-ear headphone types I could find and test at full device volume)

![Headphone Mode Flow Headphone Mode Flow](https://dl.dropboxusercontent.com/u/2185137/article_images/K1Images/headphone_mode_flow.jpeg?width=1280&auto=webp&quality=80&disable=upscale)


The original overview and model of headphone modes


![Adaptive Loudness in Action Adaptive Loudness in Action](https://dl.dropboxusercontent.com/u/2185137/article_images/K1Images/AdaptiveLoudnessMix.jpg?width=1280&auto=webp&quality=80&disable=upscale)


The same gameplay in our three different output loudness models (headphones/airplay/speaker - captured in Nuendo 6)

Mixing was thankfully a reasonably trivial matter thanks to Wwise’s mixer state system, loudness profiling and a live connection to the iPad, the output of which was calibrated via -20dB sine wave (played from dropbox) and recorded into Nuendo 6 with loudness lanes to measure overall LU values of each state. Wwise also has some incredibly useful loudness miniitoring built into the profiler view itself, which meant that it was easy to compare what was being measured from 'inside' the system with what was being recorded 'outside' the system via Nuendo.

![Wwise Loudness Monitoring Wwise Loudness Monitoring](https://dl.dropboxusercontent.com/u/2185137/article_images/K1Images/LoudnessWwise.png?width=1280&auto=webp&quality=80&disable=upscale)


(Above) Live Loudness Monitoring in Wwise using the Profiler

![Mixing and Monitoring Mixing and Monitoring](https://dl.dropboxusercontent.com/u/2185137/article_images/K1Images/mix_mon.jpg?width=1280&auto=webp&quality=80&disable=upscale)


(Above) Live tuning in Wwise (Top) + recording & monitoring in Nuendo using the loudness lane (Bottom)

With Nuendo monitoring what was coming 'out of the box', and Wwise metering what was happening 'inside' the software, this helped with easy debugging of the signal chain and a metering sanity check. (Nuendo recording and monitoring also helped by allowing us to compare other game's loudness side-by-side with our own, which can be very useful)

Once we’d come up with these loudness targets and implemented them, it became very clear how inadequate a static mixing model that doesn’t take this into account really is. For example, the difference between our chosen headphone and our device speaker output is a whopping 10dB. If we'd only mixed your game for headphones at a comfortable level, it would be 10dB too quiet for the speaker, which even in a slightly noisy environment means that much of the experience will be lost. If we'd mixed the game at -18 for the speaker, (or even -16.2 as I’ve seen some mobile games mixed at) then what the user is going to experience on headphones is shockingly loud, particularly when you consider it would be a child hearing this.

These three listening experiences and environments are so different that having loudness adapt between headphones and speaker, at a minimum, seems like an essential approach for mobile.

Knowing that our game was focused on younger children made it much easier for us to choose these loudness levels. An adult could theoretically be expected to simply turn something down if it is too loud, but you can’t make that assumption with children and have to start from the position of idealized and comfortable listening levels on each device output. With AirPlay it was also made easier because with most other content that goes through the home entertainment signal path, we can assume it is at an average loudness of -23 and firmly in the same domain as console games, movies and broadcast tv shows.

Taking it further.

A few ideas to consider for the future of adaptive mixes is to extend functionality to include all the possible output routes and ensure that they are covered under one of the above mix states. A full list for iOS audio ports and how to access them can be found [here](https://developer.apple.com/Library/ios/documentation/AVFoundation/Reference/AVAudioSessionPortDescription_class/Reference/Reference.html). There are a few equivalents for Android too, though for now, headphones and speaker are all we switch between for these devices.

Adaptive Compression.

This all works great for overall loudness, but what about compression of the loudness range (LRA)? For our K1 game initial release we had a compressor set up on the master bus to only kick in and control the sound during some of the louder output settings (via the speaker). This felt like a fairly unsatisfactorily static solution, albeit one that we could ship with.

But, rather than simply implement fixed compressor settings for each sound output mode, it felt like the problem that compressors are trying to solve was a slightly different one, and one that could be solved, again, with an adaptive approach.

Whenever using a compressor on the master bus I found I was always trying to answer a question that had multiple possible answers “What situation will our audience be listening in? A quiet classroom? A noisy classroom? What if there are only two children in the class? What if there are 25? What if the classroom itself has a noisy background of AC? Should I simply research the most common scenario for kids playing games? It seemed I couldn’t answer the question that would help me set my compressor because there was an infinite range of answers.

Quietly mixed content with a large dynamic range may work fine for a very quiet environment, but what happens when the user is playing the game in their nice quiet environment when it suddenly changes into a noisy environment via the introduction of background AC, conversational noise, or they wissh to continue their game in the back of the car on teh way home?

A great analogy to use here is the screen auto-dimming and brightening functionality based on the amount of light available in the room; Macbooks and iOS devices do this by default - it is built into the OS and it is rarely perceived, or overriden, by the user. The proposed methodology here for msater compression is to port this approach to the sound output.

![Adaptive Compression Model Adaptive Compression Model](https://dl.dropboxusercontent.com/u/2185137/article_images/K1Images/AdaptiveCompressionModel.jpeg?width=1280&auto=webp&quality=80&disable=upscale)


Adaptive Compression using user’s mic to measure SPL to control amount of master bus compression applied. (Initial Idea sketch)

Using the microphone to determine an average background sound level in SPL and to adjust the level of the output in real-time is the area to investigate here and one which we are currently investoigating in our next games in the series. By mapping input sound level of the microphone to two or three distinct (and subtle) compressor setting zones - one could quite simply have the LRA and gain makeup adjust to accommodate the dynamic loudness of the listening environment. So in a quiet setting, there would be a higher dynamic range and a generally quieter sound output (our idealized loudness ranges specified earlier), yet in situations with noisier backgrounds, a more compressed output at a slightly elevanted output level (by ~5dB) can be instigated. Gentle transitions over several seconds (done through slew rate of parameters) ease any awkwardness and jumpyness of such transitions for the user. Having the compressor adjust on-the-fly while wearing headphones is the nicer option here, as with most cheap over-ear headphones, they isolate very little noise from the surrounding environment. Theoretically then, even though a user would still have full control of the overall volume at any time, the dynamic range would be altered for them in such as way to provide the optimal LRA at all times.

In reality, through tests, something obvious occurred in that the speaker sound output of the game itself would force the compressor on, so our proposed solution could only work cleanly when the output is routed to headphones leaving the device mic free to listen solely to the environment. This makes sense assuming that 99.9% of our users (kids) won't be listening on fancy noise isolating headphones, but on cheaper over-ear sets.

Mapping the three proposed zones in my ambitious sketch, it turns out, was fairly simple by directly parametizing a compressor on the master bus in Wwise… in fact it allows a much more incremental and gentle approach via the custom envelope curves between SPL and no 'switching' between modes - it also allows us to accomodate an entire spectrum of loudness situations, such as really loud environments like plane travel.


Video: Wwise: Mic Input on Left Meter: Parametized LRA compressor setting shown in middle. Loudness Metering on Right

Summary

All these ideas are aimed at providing the optimal user-listening experience across dynamic and fast changing user-environments. At its heart is a desire to ensure that the child playing the game doesn’t miss any crucial information because of the noisiness of their background environment, or at least stands the best chance of hearing and understanding everything happening in the game.

Having these two complimentary systems of an adaptive compressor working with an adaptive loudness output that maps seamlessly across all the available output zones on the device, we can now better guarantee an optimal user listening experience in a fast changing ‘mobile’ realm.

Given the dynamic elements present in most home environments too, this approach could easily be taken and applied to console games with microphones built in or any other system with the ability to take SPL readings via a microphone to modify output. This is a fairly simple approach that can lessen the dizzying amounts of awkwardly named options present in many options menus today and providing a player with an optimal sound experience tailored to a changing listening environment without the player needing to worry or even think about the sound settings.


Updated: At my recent GDC talk on this subject: I mentioned a few caveats and gotchas with this system... Here are a few...

Headphone volume varies considerably based on ohmage / impedance. The cheaper in-ear sets tend to have much lower impedance and are much louder, whereas mid range "DJ" headphones (around 80ohms) tend to be quieter. Some kids headphones already have loudness limiting circuitry built into them, which end up making our game pretty quiet. High-end audiophile headphones can often be too quiet for mobile use at all. This makes the case for standardized headphone loudness a tricky one.

At the time of writing, Wwise doesn't yet support easy access to the device microphone via Unity out of the box. In order to get the mic input working, you'd have to write your own code to turn the mic input into a data stream (numbers), convert those numbers to a useable scale (e.g. -96 to 0) and from there optimize in order to not flood an RTPC with values / affect game performance.

Using the device mic requires that you notify the user "This App wants to use your Microphone, allow? Y/N" at startup. This can be a big 'uh oh' for anyone at all security conscious etc. As long as you are able to explain what the mic is doing (gathering numbers) and not 'listening/recording to what you are doing' you should be able to get around this - but it requires some groundwork.

On that previous point, this whole adaptive dyanmic LRA compression thing via the mic, would ideally be taken care of by the OS itself. An option in the device settings to use dynamic loudness, and to more accurately gather loudness data in the same way that the screen brightness gathers light data via a specific sensor, would be an ideal solution. This would also mean that all apps would have the same attenuation applied to them. Take note Apple!!!

EQ on the mic input, to roll off low end caused by wind or hands and fingers brushing past the mic is something to consider to more accurately gather info about the loudness of the environment and get around unwanted attenuation caused by 'other' factors.