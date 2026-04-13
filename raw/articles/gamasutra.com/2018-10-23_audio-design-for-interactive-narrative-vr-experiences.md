---
title: Audio Design for Interactive Narrative VR Experiences
url: https://www.gamedeveloper.com/audio/audio-design-for-interactive-narrative-vr-experiences
author: Larry Yu-cheng Chang
published: '2018-10-23'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Audio Design for Interactive Narrative VR Experiences

Audio design for interactive VR narrative not only directly affects the immersion of the experience, but it also affects how the composer guides the audience’s emotion. This article shares some insights using The Price of Freedom as a case study.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

### Introduction

Audio is important in many forms of storytelling. George Lucas once said “Sound is half of the experience” It is even truer when it comes to Virtual Reality because the sound in VR can directly affect the immersion of the experience. For example, if we pick up a bottle in VR and drop it on the ground and it creates no sound or the sound does not match our expectation, then our subconscious will tell us immediately that there is something wrong in the virtual world we are trying to create. Because sound doesn’t work like that in our daily lives, we have to make sure the audio experience is intuitive enough that the audience won’t disconnect them from believing in the virtual world. Without a proper audio design, the narrative experience will lose its charm and the world won’t be as convincing.

While helping to create the interactive narrative of The Price of Freedom, I have come up with some ideas about what works and what doesn’t. Consider this as a post-mortem for The Price of Freedom, and I am eager to share with you some of the lessons that I learned.

The Price of Freedom is an interactive VR story based on the declassified true event of Project MK Ultra. Project MK Ultra was a highly controversial project that ran from the 1950s to the 1970s in which the CIA experimented with several methods including using LSD to brainwash its subjects. In the story, you take the role of a CIA agent and are given a task to kill Ben Miller, a radical who broke into CIA facilities and stole top-secret chemical weapons research. By exploring in the environment, the player discovers the true reason for their mission and who they really are.

Audio design for interactive experiences can be categorized into four elements: Sound Effects, Music, Ambience, and Dialogue. But how should we prioritize making these elements and where should we place them when it comes to VR?


### 1. The Importance of Collision & Interaction Sound

Integrating collision and interaction sounds into the experience in a very early stage of the production is a good idea. This can not only help the designer or developer of the team have a more concrete sense about how the virtual world they designed feels, but also help audio professionals examine how things actually sound in the VR environment so that we can spot potential problems and make changes as early as possible.

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/Screen-Shot-2018-06-20-at-7.51.08-PM.png?ssl=1&width=640&auto=webp&quality=80&disable=upscale)


At first, when creating the prototype of The Price of Freedom, there was only one collision sound clip for each object in the scene. Here is an example of how it sounded.

The sound experience needs more variation to be closer to reality in order for us to feel comfortable. Lacking diversity breaks the immersion because we don’t find it natural. So here are the solutions:

At Construct Studio, we designed a sound system that had two features. First, we created a list of common material sound folder like wood, metal, paper, stone and so on. Then we assigned them to every object based on their features. Second, the system receives the info of how strong the object’s collision force is each time it collides and then divided them into three groups: light, medium and heavy. Each group has a list of sound clips that will be selected to play randomly each time when the sound is triggered. On top of that, we also added the pitch variation to the sound clips to make sure that each time it would sound slightly different.

We have to apply this sound system to almost every object in the scene. Since the player has the freedom to interact with mostly everything they want in the scene, we have to make sure that everything they touch has satisfying sound feedback that won’t break the immersion. But if there are so many audio effects around the players, how are they going to receive more important information and find out what the story is about in VR?


### 2. Using Sound to Tell Story

When it comes to using audio to tell interactive narratives in VR, there is one concept to keep in mind: Indirect Control. It is a technique to use design to guide the player to certain expected actions without letting them realize the fact that they are being guided.

A well designed audio experience is a great opportunity for indirect control since audio has several key features that can be used to guide the player. First, it sets time and space of the experience for the player. In The Price of Freedom, for example, we have a radio in a scene that plays the music from the 60s, and a TV that broadcasts John F. Kennedy’s inauguration speech so that the players can clearly get it that they are in a specific time period. In this case, the 60s in the United States.

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/Screen-Shot-2018-06-20-at-8.07.49-PM.png?ssl=1&width=640&auto=webp&quality=80&disable=upscale)


Also, apart from the instructional dialogues that directly guide the player what to do, we also have reel to reel tapes with dialogue that can not only guide the player to focus on specific area of the space but also provides fragments of the story as reinforcement. The tapes, along with other elements like letters, documents, and pictures remind the player of the story over and over again. So that even if they miss some of the information, they are still able to have an overall understanding of the narrative.

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/Screen-Shot-2016-12-20-at-22.35.08.png?ssl=1&width=640&auto=webp&quality=80&disable=upscale)


The audio also sets emotional tone for the experience. Interactive music is a great way for us to affect the player’s emotional states while they are immersed in an interactive environment. We designed a music piece into several scales with different intensity of the emotion and then put them in sequence for the player to trigger in the scene.

Take the fire scene in The Price of Freedom for example. We designed the emotion of this scene into 4 levels of intensity. In the beginning, the player just read through a binder and discovered what terrible things they have done. We want the player to feel the emotion from feeling numb to grief gradually, just like the character would feel in the story. The first layer of intensity starts when the player finishes reading the binder, It is a pretty simple tune with a shade of gloominess. There is only one synthesizer simulating a heartbeat. As soon as the player lights the binder on fire, the second layer will be triggered. At this point, the emotion of sadness grows along with the fire. A piano melody added on to the second layer to indicates that the player’s conscience has been awakened.

Then, as soon as the player finds a way to exit the chamber they start in, the third layer of intensity is triggered. The sad emotion becomes more intense as a hint that everything is about to change in the character’s life. As the scene fades out we designed a tail for the ending of the music cue so that it sounds like a linear musical experience. Then the story goes on…

Speaking of music, some people may ask what the difference between writing music for VR and non-VR games may be. In my personal opinion, music in VR should be more subtle and be more intimate to the player. This is because it is the player’s personal and direct experience. With the first person’s perspective, music in VR is all about the player’s connection to the virtual world. They are the protagonist of the show and the music is built around them.

In The Price of Freedom, we have designed signature music combining both non-diegetic and diegetic forms for different themes of the narrative. We have developed theme music for Ben Miller’s daughter, Cathy Miller. It shows up the very first time in the experience with a diegetic form as a tune played on a music box which her father gave it to her as a birthday present. After that, whenever the plot or information of the story is related to Cathy, the player will be reminded of the same theme music.

Here is an example of the combination of two theme signature music:


Project Mk Ultra Theme:


Cathy’s Theme:


Combination (Ending):


Final Suite:

### 3. Spatial Audio Placement in VR

Now that we have created all the sound files, how should we place them in a VR environment? We want to make the player feels like they are actually in that space but, at the same time, we try to reinforce the clarity of some audio cues and make sure the player won’t miss it. In general, we separated them into two groups: the first group is the one where audio is placed in fixed locations in the environment; audio from the second group is placed in relative locations based on the player.

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/Screen-Shot-2018-06-20-at-7.48.40-PM.png?ssl=1&width=640&auto=webp&quality=80&disable=upscale)


The first group includes our ambiance sound, collision/ interaction sound, diegetic music and some of the dialogue. It attaches the sound to either a certain object or a place in the space that helps to create the audio environment of the player. Take our surrounding ambiance environmental sound as an example: We designed a 5 speakers system for each room, attached each mono sound file to each speaker, and place them in the space to simulate how we set 5.1 speakers in the real world.

The second group of sound; however, will move to correspond to the player’s location. This is sometimes called “head-locking” the audio. Examples include some of the dialogue and some of the non-diegetic music and audio from the cutscenes. This group is for the purpose of making sure the player would receive the full information of the audio content. Take the voiceover as an example: we have a voice from the doctor’s character that gives you orders about what you should do throughout the experience. We put the voice audio source right behind the player’s head all the time. This setting not only enables the players to always be able to get clear information from the same orientation but it also matches the setting of the story.


### 4. Mixing in VR

Now we have all the sound in place in VR. How are we going to mix it?

We figured that it would be easier for us to manage all audio sources by putting them into bigger groups (SFX, Music, Dialogue, and Ambience), assigning the groups to individual channels in the Unity mixer and mixing based on the group instead of individual files. Of course, for the files that are grouped into one channel, I have already adjusted their relative volume between each other in DAW first before putting them into the game engine. That being said, it is still very important to check your mix in VR because the audio you heard in DAW is definitely going to sound different in VR. it’s not a one-time thing, but a back and forth process.

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/Screen-Shot-2018-06-21-at-12.58.57-PM.png?ssl=1&width=640&auto=webp&quality=80&disable=upscale)


### 5. Conclusion

To sum up, working on collision and interaction sounds and putting them in the prototype as early as possible helps the developing process for both designers and audio professionals. Understanding how to use audio as guide the players enriches the interactive storytelling by addressing information to the players and manipulating their state of mind. Adopting the concept of signature music also enables the players to identify with the characters and plots in the story and have a more memorable experience. Last but not least, a good spatial audio placement strategy and mixing technique not only enhances the efficiency of the audio pipeline but also gives a more immersive result.