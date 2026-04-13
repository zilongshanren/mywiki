---
title: Audio Challenges in a "Gamer's Game for Facebook"
url: https://www.gamedeveloper.com/audio/audio-challenges-in-a-quot-gamer-s-game-for-facebook-quot-
author: Dren McDonald
published: '2013-01-14'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Audio Challenges in a "Gamer's Game for Facebook"

A reflection on the audio development on Ghost Recon Commander; reconciling a 'core game' audio experience for the Facebook game platform.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

In the last week I did some archive video capture for [Ghost Recon Commander](http://www.facebook.com/ghostreconcommander) before it was taken offline by Ubisoft. In doing so I was reminded of some of the audio questions and answers I came up with during development of the game. I found it oddly meaningful that the day that Ghost Recon Commander was taken offline was almost exactly one year ago, to the day, that I began as Audio Director at Loot Drop. I'm taking that as a sign to reflect on the Ghost Recon Commander experience here.

A GAMER'S GAME FOR FACEBOOK

This was the marketing tagline that was given to GRC when it was announced, and for better or worse, it sums up the first audio conundrum I faced on the project. But first, a little background..

Loot Drop was started by John Romero, Brenda Romero and Tom Hall, and I had previously worked with John and Brenda on Ravenwood Fair at Lolapps. Ravenwood Fair was a fairly typical Facebook game for it's era (2010) and was designed to be enjoyed by a wide swath of the population (not unlike Frontierville, or Farmville at the time). I continued working on Ravenwood Fair after John and Brenda left to begin Loot Drop, and I worked on Facebook titles such as Idle Worship, Ravenskye City, Zoo World 2, Ravenshire Castle, and a few others. Needless to say, I was pretty familiar with the Facebook game audience (if you can use a blanket term like that.)

Rule # 1 of the Facebook game audience was "don't do anything to discourage the player from playing the game!" For the audio side that meant that the sounds should be fairly tame (not aggressive), not realistic (usually), and not grating (I avoided recurring sounds in the 1.5k-3k area). Musically, for these types of games, you want to create a safe and happy place. "DON'T DISCOURAGE THE PLAYER FROM PLAYING THE GAME!" I actually saw footage of paid playtesters that revealed players booting up a Facebook game, hearing ONE annoying sound and proceeding to leave the game! There were also more reasonable play testers who would only turn off the audio when they heard something annoying. BUT STILL!

Taking that experience with me, I was asked to join Loot Drop and start in on Ghost Recon Commander (in addition to Pettington Park...I'll have to do a story on that one too). In Ghost Recon Commander the player is always in danger, the sounds are realistic, aggressive, repetitive and grating (guns, explosions, loot pickups etc). These aren't the Facebook audio principles I've been holding, gripping, and bending to for the last few years...a reconciling was in order!

THE BIG AUDIO PICTURE

So we were making a game with guns and explosions. Not cute forest animals with big heads. If guns and explosions were an accepted part of the soundscape (and wouldn't drive the player away) then I had a sonic freedom in a Facebook game that I hadn't previously enjoyed. But it was still a Facebook game. I couldn't just go Dead Space on this title and freak out the player with audio. I was still assuming that at least some of those non-gamer types might check out this game and I didn't want them to run screaming. Knowing that John and Brenda were stoked about making this game because of the love they had for the original Ghost Recon game (circa 2001) I went back to check that one out to get some insight into how that title worked with the audio.

If you've played that title, you'll know what a scary, isolating experience it can be. Audio plays a HUGE part in the game, as there is no gameplay music, just ambience. You can also hear, in 3D space, where your enemies are, and if they are coming for you. Creepy. However, GRC was not in a 1st person, 3D space. It's an isometric game, looking down on the players, similar to an RTS. The 1st person audio approach wouldn't work with that view and wouldn't be possible in Flash (not to mention that we had to keep the footprint of this game pretty small).

One thing I did take from the audio experience in the 2001 Ghost Recon was the use of ambience and the psychological impact of the space between sounds. When you are deep in a mission in the 2001 GR, and you hear nothing, (especially right after shooting towards someone), you start to quickly wonder if you've made a terrible mistake. Quite often you can't see where the shots are coming from, which also adds to this paranoia. This subtle approach seemed to be a nice way to merge the worlds of Facebook game audio expectations and a core gaming experience.

THE BRENDA FILTER

We knew that GRC would be released at the same time as Ghost Recon: Future Soldier (the console version). So we had some GR:FS weapon sound assets provided by Ubisoft, but almost no music. I think there was one short loop that was temporarily inserted into the pre-alpha build of the game. This gave me a little direction, but having some familiarity with the IP I felt comfortable in finding a musical direction for the game.

At the time of pre-Alpha, we were spending a lot of time running around in the game's base camp, so I started with writing that music. Brenda was the designer on the game, and I would get notes on the music that she liked a few parts of the piece, but also found specific elements in the music to bother her. After some IM's and emails it seemed easier to simply listen to the piece together so she could specifically point to parts of the music that she didn't like. It turned out that this was incredibly helpful for conceiving the rest of the game's music as I gained insight into what the game designer did and didn't want in the game music and applied what I learned in that short listening experience to the rest of the game's music. I've [posted a little sample here of the music ](https://vimeo.com/57106946)before learning the "Brenda filter", and after.

Generally, it seemed that providing a simple musical atmosphere, leaving a good amount of space was always better than filling it with cool or eerie sounds. A point that reinforced my initial takeaway from 2001 GR. I think sometimes that as composers, if we don't have a clear idea about what we want to say we keep throwing ideas against the wall (a new synth patch, some bizarre metal percussion, a WATERPHONE with REVERB!) until there's just a lot of sound filling up the space. You know you've done it. Sometimes composing is simply peeling away most of the unessential ideas our conscious (ego) mind told us we should throw into the mix.

LOTS OF MUSIC

One little known fact about putting music in Facebook games is that the MP3s do not have to live inside of the game swf. You can have a couple of symphonies worth of audio files sitting on a server waiting for their call to come in and stream into the game whenever they are needed. Their playback will not affect the gameplay. The game just starts, and when the loop is buffered it starts to play. I had a lot of talks with John about exploiting this so that we could have different music for each level, and each submap. In addition, we also created looping ambiences for all of these game areas so if the player didn't want to hear music, they would hear these ambiences instead. But there was a different loop for every level and every submap and we didn't have to compress the life out of the files either.

One interesting note regarding music and ambiences in GRC is that when the player chose to listen to music, the music track actually had the ambience baked into the file. This came from several discussions between John and Brenda and I and our experiences in 2001 GR. For a while we only put ambience into the build levels, with no music, to see how it felt. Ultimately we decided that the player was probably going to want an experience closer to current shooter games, with the game defaulting to include the music, but we also wanted to hear the ambience (like the original game.) Baking the music with the ambience seemed like a good way to meet all of those needs, and if the player didn't want the music, they had the option for only ambience.

One of the concepts that struck me in playing both the original GR and GRC (certainly later in GR:FS) was the contrast of high tech weapons/communications/tactics etc versus the organic look of the jungles, the water, the rocks, the wood etc. So, I fiddled around with this idea in the music, contrasting featured tech sounding instruments (drum machine or sound design loops, arpeggiated synths etc) against organic instruments like a drum, cello or french horn. I felt like every level had to have elements of that contrast in the music.

In the first level's music, I found a tech sounding loop that I manipulated and slowed down and the use of this loop was a blueprint for the rest of the music levels. In every piece there would be some little 'tech loop' which I thought of as a Ghost Recon reminder..just to remind the player that tech was 'on their side', I guess. The 'tech loop' from the 1st level can be heard again in the 10th level's last musical piece where the player storms into Rivera's palace and goes after the big boss. However the loop is used in a much different type of music in the last level. I tried to build a dramatic arc in the music throughout the levels, starting with sparse, neutral music, which became sadder, darker and a bit aggressive until the last level where the player was rewarded with some uptempo 'kicking ass' kind of music. [In this clip here you can hear ](https://vimeo.com/57107502)the Level 1 music first and then the level 10 music which both use the same loop.

SOUND DESIGN

As I mentioned, we had most of the weapon sound assets provided by Red Storm/Ubisoft, so..cool, work is done! Well, even though it was a game which probably had low audio expectations, I still felt that in a shooter we had to at least have weapon shot variations. We had a largely data driven system at Loot Drop, and I worked with an engineer to find a way to include sound variations into the data. So I could load up a new sound swf, input new data and hear how everything sounded in my build whenever I wanted. Though I wasn't given a hard limit for the audio footprint, I tried to keep things reasonable, so we started with each weapon getting 3 shot variations that would randomize. In a game where ammunition was the currency, the shooting frequency was generally held to a minimum so that the player could keep playing (if you ran out of ammo you had to buy more, with real money, or wait until the game recharged the ammo). So 3 seemed like a number that would work in this situation. We ended up with about 20-25 different weapons, each with 3 shot variations. But we had a lot of dialog.

VO

Most of the dialog consisted of the Ghosts communicating back and forth to each other about where to go, what area to move to, what box to pick up etc. So we had to have a few distinctive voices with a lot of short lines. When the player first starts, there are 3 main voices for the Ghosts that are heard for a during the first few missions. They are all Loot Drop folks: Tom Hall did a Ghost, Alexander Davis (QA) did a Ghost and the last Ghost was a combo of Toby Hefflin (Animator) and myself. As the player got their friends into the game we had to add a few more Ghost voices to cover the 3 Ghost types that would be represented in the player's friend ladder. So we hired Alexander Brandon to cover those for us, and he did a wonderful job on them. He did 3 totally distinct and recognizable voices for the player Ghosts (and he did all of the hostage voices too).

Then we had some other voices from some of the NPCs in the game. The friendly and grateful rebels that the player was helping (voiced by Rex Cartagena, Loot Drop's native male spanish speaker) and the leader of the rebels, voiced by Loren Hernandez (Loot Drop's native female spanish speaker). Initially we had Rex voice all of the spanish speaking bad guys, but Rex is a nice guy, and his voice doesn't get too angry...so I learned the accent from Rex' recordings, and did the angry guys as best I could. In fact, there was one word that the bad guys would yell at the player that became an issue..we didn't know the degree of 'offensive' meaning that this word carried. We got conflicting reports on the egregious or not-so-egregious nature of this particular word depending on what part of the world it was being used in. It went from being a show stopping, "get this file out of the build NOW" to "oh, I think it's ok...don't worry". No, I won't tell you the word.

Like many military games, the dialog between Ghosts sounded like it was coming through a walkie talkie. At AES this year, at the Red Storm panel on Ghost Recon Future Soldier I learned that their sound team went through this rigorous recording process of putting dialog through a walkie talkie and recording the source from a speaker in a military vehicle to achieve ultimate realism. While I believe they were able to salvage some of that work, most of their ultimate walkie talkie realism came in the form of AudioEase's Speakerphone plugin. It turns out that this is the same plugin that I used for my dialog treatment, and it was also the choice of the Ubisoft team in Paris doing the single player GRFS campaign. We didn't plan this out, we just realized later that we all came up with the same solution.

The funniest moment of the dialog didn't make it into the game, unfortunately. If the player was successfully sneaking up on a couple of the bad guys, we wanted the player to hear a little bit of a conversation between the bad guys. The idea was that these guys were pretty unhappy, that they weren't being treated well and that they were getting sick. John had written some hilarious lines (if he wasn't making games, he could be a comedy writer) that were to occur between these guys. I brought Rex in to translate into Spanish, and read one of the parts. Since John wrote the lines, and has listened to his family speak Spanish his entire life, I wanted him to act the other part. I think we ended up just laughing in the sound room for about half of the day trying to get straight takes. My favorite line: "Hey, could you look at this lump on my back for me?"

FOLEY

The decision to include footsteps in the game was always being kicked around in my head throughout development. I was having the same dilemma on Pettington Park at the time. After trying a few tests with placeholder sounds and a little tweaking in the code (thanks Steve!), it seemed like we could make this work as long as we could easily determine what type of surface material the characters were walking on. The ground tiles had data attached to them that could tell the engine what surface footstep sound to use, and we could use our sound variation data and randomization to achieve a fairly realistic footstep sound. I believe we had 4 variations for each foot per surface type and I leaned towards subtlety on the sounds. These were supposed to be sneaky super soldiers, we couldn't have them clomping around the fields in loud boots. [Here's a little clip](https://vimeo.com/57103676) of some of the footsteps in game.

TANGO DOWN!

After working on so many Facebook games aimed at casual players (en masse) it was refreshing (and challenging) to be given the chance to expand the pallet of a Facebook game's sound picture. It's always a fortunate situation when everyone on the team gets along well, and is working together to make something which they want to be proud of, and this was certainly the situation with Ghost Recon Commander.

----------------


Dren McDonald is a composer, sound designer and audio director. His most recent title is Skulls of the Shogun, which releases on 1/30/13 on Xbox Live Arcade, Windows 8, Windows Surface, and Windows Phone. He serves on the Game Audio Network Guild (G.A.N.G.) as Director of Development, and recently has lectured and been on panels at GDC (Game Developers Conference), GameDesignCon, GameSoundCon and at several GANG Summits. [www.nerdtracks.com](http://www.nerdtracks.com) @drenmc

This article first appeared on [GameAudio101.com](http://gameaudio101.com/Ghost-Recon-Commander.php)